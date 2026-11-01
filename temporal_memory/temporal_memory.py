# -*- coding: utf-8 -*-
"""Task C: memory length x class duration x drift speed, controlled simulation on real statistics."""
import json, os, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'results', 'factorial_cache.npz')
OUT = os.path.join(HERE, 'results', 'temporal_memory_v2.json')
BLOCK = 15
z = np.load(CACHE, allow_pickle=True)
mus_all, covs_all = z['mus'], z['covs']


def series(r, mus, cov, n, run_len):
    K, d = mus.shape
    y = []
    while len(y) < n:
        c = r.integers(0, K)
        y.extend([c] * max(1, int(run_len)))
    y = np.array(y[:n])
    return y, np.array([r.multivariate_normal(mus[c], cov) for c in y])


def run_series(r, mus, cov, prior_shift, drift_speed, run_len, mem):
    n = 1200
    FA_y, FA = series(r, mus, cov, 600, run_len=1)   # source must be balanced iid, otherwise
                                                     # source and target proportions differ and the
                                                     # 'no drift' cell is contaminated by composition
    FB_y, FB = series(r, mus, cov, n, run_len=run_len)
    if prior_shift:
        keep = r.random(n) < 0.75
        keep[FB_y == 0] = True
        FB, FB_y = FB[keep], FB_y[keep]
    if drift_speed > 0:
        step = drift_speed * np.sqrt(np.trace(cov) / cov.shape[0]) / np.sqrt(cov.shape[0])
        FB = FB + np.outer(np.arange(len(FB)) / len(FB), r.normal(size=cov.shape[0]) * step)
    clf = LDA(solver='lsqr', shrinkage='auto').fit(FA, FA_y)
    K = len(clf.classes_)
    W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(K) - np.ones((K, K)) / K
    muA = FA.mean(0)
    S = clf.decision_function(FB)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    blocks = [(a, min(a + BLOCK, len(FB))) for a in range(0, len(FB), BLOCK)]
    D = [Fm @ (W @ (FB[a:b].mean(0) - muA)) for a, b in blocks]
    bm = np.zeros((len(FB), K))
    hist = []
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            hist.append(D[k - 1])
            use = hist[-mem:] if mem else hist
            bm[a:b] = np.mean(use, axis=0)
    keep = np.arange(len(FB)) >= BLOCK
    p0 = clf.classes_[np.argmax(S, 1)]
    p1 = clf.classes_[np.argmax(S - bm, 1)]
    return float(bas(FB_y[keep], p1[keep]) - bas(FB_y[keep], p0[keep]))


rows = []
for si in range(min(12, len(mus_all))):
    mus, cov = mus_all[si], covs_all[si]
    for seed in range(4):
        r = np.random.default_rng(7000 + seed)
        for prior in (0, 1):
            for speed in (0.0, 0.5, 1.0):
                for run_len in (1, 5, 25):
                    for mem in (1, 4, 16):
                        d = run_series(r, mus, cov, prior, speed, run_len, mem)
                        rows.append({'subj': int(si), 'seed': seed, 'prior': prior, 'speed': speed,
                                     'run_len': run_len, 'mem_blocks': mem, 'delta': d})
    print('subject', si, len(rows), flush=True)
    json.dump(rows, open(OUT, 'w'))
print('rows', len(rows))