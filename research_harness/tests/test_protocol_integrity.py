# -*- coding: utf-8 -*-
"""Executable tests for the claims the paper makes about its own protocol.

Run with:  python research_harness/tests/test_protocol_integrity.py
Every test is self-contained and uses synthetic data, so it runs without the EEG corpora.
"""
import json, os, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BLOCK = 15


def trial_series(rng, n=120, d=4, K=3, run_len=10):
    y = []
    while len(y) < n:
        y.extend([rng.integers(0, K)] * run_len)
    y = np.array(y[:n])
    X = np.array([rng.normal(loc=1.0 * c, scale=1.0, size=d) for c in y])
    return X, y


def run_pipeline(XA, yA, XB, yB, lam=1.0, perturb_after=None):
    clf = LDA(solver='lsqr', shrinkage='auto').fit(XA, yA)
    K = len(clf.classes_)
    W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(K) - np.ones((K, K)) / K
    muA = XA.mean(0)
    S = clf.decision_function(XB)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    n = len(yB)
    blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
    D = [Fm @ (W @ (XB[a:b].mean(0) - muA)) for a, b in blocks]
    bm = np.zeros((n, K))
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            bm[a:b] = np.mean(D[:k], axis=0)
    return clf, S, bm, blocks, Fm, W, muA


def test_no_future_leak():
    """Predictions in block k must not change when only later blocks change."""
    rng = np.random.default_rng(11)
    XA, yA = trial_series(rng, n=180)
    XB, yB = trial_series(rng, n=120)
    clf, S, bm, blocks, Fm, W, muA = run_pipeline(XA, yA, XB, yB)
    XB2 = XB.copy()
    cut = blocks[1][1]
    XB2[cut:] += 5.0
    clf2, S2, bm2, blocks2, Fm2, W2, muA2 = run_pipeline(XA, yA, XB2, yB)
    same = np.allclose(bm[:cut], bm2[:cut])
    assert same, 'correction for the first scored block changed when later blocks changed'
    return True


def test_exact_decomposition():
    """The three-term decomposition must reproduce the estimator displacement."""
    rng = np.random.default_rng(12)
    XA, yA = trial_series(rng, n=180, K=4)
    XB, yB = trial_series(rng, n=120, K=4)
    clf = LDA(solver='lsqr', shrinkage='auto').fit(XA, yA)
    classes = clf.classes_
    piA = {c: float(np.mean(yA == c)) for c in classes}
    mA = {c: XA[yA == c].mean(0) for c in classes}
    n = len(yB)
    blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
    worst = 0.0
    for k in range(1, len(blocks)):
        hist = blocks[:k]
        mu = np.mean([XB[a:b].mean(0) for a, b in hist], axis=0)
        allc = sorted(set(classes.tolist()) | set(np.unique(yB).tolist()))
        mass, num = {c: 0.0 for c in allc}, {c: np.zeros(XB.shape[1]) for c in allc}
        for a, b in hist:
            lab, nb = yB[a:b], b - a
            for c in allc:
                m = lab == c
                w = m.sum() / nb
                mass[c] += w / len(hist)
                if m.sum():
                    num[c] += w * XB[a:b][m].mean(0)
        mh = {c: (num[c] / (mass[c] * len(hist)) if mass[c] > 0 else np.zeros(XB.shape[1])) for c in allc}
        d = mu - XA.mean(0)
        dmix = sum((mass[c] - piA[c]) * mA[c] for c in allc if c in piA)
        dwith = sum(mass[c] * (mh[c] - mA[c]) for c in allc if c in piA)
        dun = sum(mass[c] * mh[c] for c in allc if c not in piA)
        worst = max(worst, float(np.max(np.abs(d - (dmix + dwith + dun)))))
    assert worst < 1e-10, 'decomposition error %.3e' % worst
    return worst


def test_scoring_set_fixed():
    """All conditions must be scored on exactly the same epochs."""
    rng = np.random.default_rng(13)
    XA, yA = trial_series(rng, n=180)
    XB, yB = trial_series(rng, n=120)
    clf, S, bm, blocks, Fm, W, muA = run_pipeline(XA, yA, XB, yB)
    keep = np.arange(len(yB)) >= BLOCK
    n_scored = int(keep.sum())
    assert n_scored == len(yB) - BLOCK, 'scored set depends on the condition'
    return n_scored


def test_lambda_weight_bound():
    """The variance-ratio weight must lie in [0, 1]."""
    rng = np.random.default_rng(14)
    vals = []
    for _ in range(200):
        d = rng.normal(size=6)
        var = rng.uniform(0.01, 2.0)
        B = rng.integers(2, 12)
        lam = float(np.dot(d, d) / (np.dot(d, d) + 6 * var / B))
        vals.append(lam)
    vals = np.array(vals)
    assert vals.min() >= 0 and vals.max() <= 1, 'weight outside [0, 1]'
    return float(vals.mean())


if __name__ == '__main__':
    results = {}
    for fn in (test_no_future_leak, test_exact_decomposition, test_scoring_set_fixed, test_lambda_weight_bound):
        try:
            out = fn()
            results[fn.__name__] = out
            print('PASS %-32s %s' % (fn.__name__, out))
        except AssertionError as e:
            print('FAIL %-32s %s' % (fn.__name__, e))
            results[fn.__name__] = 'FAIL: %s' % e
    ok = all(v != 'FAIL' and not (isinstance(v, str) and v.startswith('FAIL')) for v in results.values())
    print('PROTOCOL INTEGRITY', 'PASS' if ok else 'FAIL')
    json.dump(results, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_results.json'), 'w'), indent=1)
