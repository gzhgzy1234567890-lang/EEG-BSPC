# -*- coding: utf-8 -*-
"""Unit test: score-space past-only correction equals the feature-space two-sided correction."""
import os, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(0)
for K in (2, 4):
    D, N, M = 12, 900, 300
    A = rng.normal(size=(N, D)) + rng.normal(size=(1, D))
    ya = rng.integers(0, K, N)
    B = rng.normal(size=(M, D)) + 0.7 * rng.normal(size=(1, D))
    yb = rng.integers(0, K, M)
    clf = LDA(solver='lsqr', shrinkage='auto').fit(A, ya)
    S = clf.decision_function(B)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    SA = clf.decision_function(A)
    if SA.ndim == 1:
        SA = np.column_stack([-SA, SA])
    Fm = np.eye(K) - np.ones((K, K)) / K
    n = len(yb)
    blocks = [(a, min(a + 15, n)) for a in range(0, n, 15)]
    muA = A.mean(0)
    corr_score = np.zeros_like(S)
    corr_feat = np.zeros_like(S)
    for k, (a, b) in enumerate(blocks):
        if k == 0:
            continue
        mu_hist = np.concatenate([B[x:y] for x, y in blocks[:k]]).mean(0)
        d = Fm @ (np.concatenate([S[x:y] for x, y in blocks[:k]]).mean(0) - SA.mean(0))
        corr_score[a:b] = d
        Xc = B[a:b] - mu_hist + muA
        Sc = clf.decision_function(Xc)
        if Sc.ndim == 1:
            Sc = np.column_stack([-Sc, Sc])
        corr_feat[a:b] = Sc - S[a:b]
    p_score = clf.classes_[np.argmax(S - corr_score, 1)]
    p_feat = clf.classes_[np.argmax(S + corr_feat, 1)]
    agree = float(np.mean(p_score == p_feat))
    print('K=%d  prediction agreement between score-space and feature-space correction: %.4f' % (K, agree))
    assert agree == 1.0, 'the two implementations must agree exactly'
print('UNIT TEST PASS')