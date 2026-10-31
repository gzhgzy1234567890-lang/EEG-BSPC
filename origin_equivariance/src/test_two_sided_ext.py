# -*- coding: utf-8 -*-
"""Extended assertions for the two-sided past-only correction (A4)."""
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA


def build(K, D=10, N=600, M=240, shift=0.0, seed=0):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(N, D)) + rng.normal(size=(1, D))
    ya = rng.integers(0, K, N)
    B = rng.normal(size=(M, D)) + shift * rng.normal(size=(1, D)) + 0.4 * rng.normal(size=(1, D))
    yb = rng.integers(0, K, M)
    return A, ya, B, yb


def scores(clf, X):
    S = clf.decision_function(X)
    return np.column_stack([-S, S]) if S.ndim == 1 else S


def corrections(clf, A, B, K, block):
    S = scores(clf, B); SA = scores(clf, A)
    Fm = np.eye(K) - np.ones((K, K)) / K
    n = len(B)
    blocks = [(a, min(a + block, n)) for a in range(0, n, block)]
    out = np.zeros_like(S)
    for k, (a, b) in enumerate(blocks):
        if k == 0:
            continue
        d = Fm @ (np.concatenate([S[x:y] for x, y in blocks[:k]]).mean(0) - SA.mean(0))
        out[a:b] = d
    return S, out


def feature_predictions(clf, A, B, K, block):
    muA = A.mean(0)
    n = len(B)
    blocks = [(a, min(a + block, n)) for a in range(0, n, block)]
    pred = np.zeros(n, dtype=int)
    for k, (a, b) in enumerate(blocks):
        if k == 0:
            pred[a:b] = clf.predict(B[a:b])
        else:
            mu_hist = np.concatenate([B[x:y] for x, y in blocks[:k]]).mean(0)
            pred[a:b] = clf.predict(B[a:b] - mu_hist + muA)
    return clf.classes_[pred]


for K in (2, 3, 4):
    A, ya, B, yb = build(K)
    clf = LDA(solver='lsqr', shrinkage='auto').fit(A, ya)
    S, D = corrections(clf, A, B, K, 15)
    S2, D2 = corrections(clf, A, B, K, 15)
    assert np.array_equal(D, D2), 'determinism'
    p_score = clf.classes_[np.argmax(S - D, 1)]
    p_feat = feature_predictions(clf, A, B, K, 15)
    agree = float(np.mean(p_score == p_feat))
    print('K=%d score-vs-feature label agreement %.4f' % (K, agree))
    assert agree == 1.0, 'score and feature space must agree exactly'
    # per-sample centered score difference
    S3, D3 = corrections(clf, A, B, K, 15)
    assert np.abs((S - D) - (S3 - D3)).max() < 1e-12, 'centered scores must be identical'
    # the score-space displacement equals the projected feature-space displacement
    Fm = np.eye(K) - np.ones((K, K)) / K
    W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
    n = len(B)
    blocks = [(a, min(a + 15, n)) for a in range(0, n, 15)]
    for k, (a, b) in enumerate(blocks):
        if k == 0:
            continue
        mu_past = np.concatenate([B[x:y] for x, y in blocks[:k]]).mean(0)
        d_feat = Fm @ (W @ (mu_past - A.mean(0)))
        assert np.abs(d_feat - D[a]).max() < 1e-10, 'score-space and feature-space displacement must coincide'
    # past-only: changing future trials must not change earlier corrections
    Bp = B.copy(); Bp[9 * 15:] += 5.0
    S5, D5 = corrections(clf, A, Bp, K, 15)
    assert np.abs(D5[:9 * 15] - D[:9 * 15]).max() < 1e-12, 'future trials leaked into the past correction'
    # block length and incomplete last block
    for blk in (5, 15, 20):
        Sb, Db = corrections(clf, A, B[:200], K, blk)
        assert Db[:blk].max() == 0 and Db[blk:].max() > 0, 'first block must be unscored'
    print('K=%d  translation invariance OK; future-perturbation invariance OK; block lengths OK' % K)

print('ALL ASSERTIONS PASSED')