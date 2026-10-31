# -*- coding: utf-8 -*-
"""Pre-registered P300 test: does a composition-dominated displacement hurt on an independent dataset?"""
import json, os, pickle, sys
import numpy as np
from scipy.stats import binomtest, wilcoxon
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BLOCK = 15
SRC = r'E:\data\Event-Related Potentials (P300, EEG) - BCI dataset\data_allsubjects'
OUT = r'G:\Work_work\math\EEG\paper_v8\results\p300_external_meanamp.json'


def feats(X):
    n, c, t = X.shape
    edges = np.linspace(0, t, 5).astype(int)
    cols = []
    for k in range(4):
        seg = X[:, :, edges[k]:edges[k + 1]]
        cols.append(np.mean(seg, axis=2))
    return np.concatenate(cols, axis=1)


def run_cell(FA, yA, FB, yB):
    clf = LDA(solver='lsqr', shrinkage='auto').fit(FA, yA)
    K = len(clf.classes_)
    S = clf.decision_function(FB)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    SA = clf.decision_function(FA)
    if SA.ndim == 1:
        SA = np.column_stack([-SA, SA])
    Fm = np.eye(K) - np.ones((K, K)) / K
    n = len(yB)
    blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
    D = [Fm @ (S[a:b].mean(0) - SA.mean(0)) for a, b in blocks]
    bm = np.zeros((n, K))
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            bm[a:b] = np.mean(D[:k], axis=0)
    keep = np.arange(n) >= BLOCK
    p0 = clf.classes_[np.argmax(S, 1)]
    p1 = clf.classes_[np.argmax(S - bm, 1)]
    return (float(bas(yB[keep], p0[keep])) - float(bas(yB[keep], p1[keep])),
            float(bas(yB[keep], p0[keep])), float(bas(yB[keep], p1[keep])),
            float(np.mean(yA == 1)), float(np.mean(yB[keep] == 1)))


def main():
    obj = pickle.load(open(SRC, 'rb'))
    rows = []
    for i, e in enumerate(obj, start=1):
        X = e.get_data()
        y = e.events[:, 2].astype(int)
        y = np.where(y > 0, 1, 0)
        half = len(y) // 2
        FA, FB = feats(X[:half]), feats(X[half:])
        yA, yB = y[:half], y[half:]
        d, b0, b1, piA, piB = run_cell(FA, yA, FB, yB)
        rows.append(dict(subj=i, delta=-d, ba_none=b0, ba_corr=b1, pi_A=piA, pi_B=piB, n=int(len(yB) - BLOCK)))
        print('subject %2d  BA none %.4f  corrected %.4f  delta %+0.4f  pi_A %.2f pi_B %.2f' % (i, b0, b1, -d, piA, piB), flush=True)
    vals = np.array([r['delta'] for r in rows])
    pos = int((vals > 0).sum())
    print('---')
    print('subjects %d  mean delta %+0.4f  positive %d  sign p=%.4f  wilcoxon p=%.4f'
          % (len(vals), vals.mean(), pos, binomtest(pos, len(vals), 0.5).pvalue, wilcoxon(vals).pvalue))
    json.dump(rows, open(OUT, 'w'), indent=1)
    print('wrote', OUT)


if __name__ == '__main__':
    main()