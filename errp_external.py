# -*- coding: utf-8 -*-
"""Pre-registered cross-session ERRp test on the BCI challenge dataset."""
import glob, json, os, re, sys
import numpy as np
import pandas as pd
from scipy.stats import binomtest, wilcoxon
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = r'E:\data\inria-bci-challenge'
BLOCK = 15
FS = 200.0
T0, T1 = 0.0, 0.6
OUT = r'G:\Work_work\math\EEG\paper_v8\results\errp_external.json'


def load_session(path):
    df = pd.read_csv(path, engine='c')
    cols = [c for c in df.columns if c not in ('Time', 'FeedBackEvent', 'EOG')]
    fb = df['FeedBackEvent'].values
    X = df[cols].values.astype(np.float32)
    idx = np.where(fb > 0)[0]
    i0, i1 = int(T0 * FS), int(T1 * FS)
    eps = [X[i + i0:i + i1] for i in idx if i + i1 <= X.shape[0]]
    return np.stack(eps) if eps else np.zeros((0, i1 - i0, len(cols)), np.float32), cols


def feats(E):
    n, t, c = E.shape
    edges = np.linspace(0, t, 5).astype(int)
    parts = [np.log(np.var(E[:, edges[k]:edges[k + 1], :], axis=1) + 1e-12) for k in range(4)]
    return np.concatenate(parts, axis=1)


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
    return float(bas(yB[keep], p1[keep]) - bas(yB[keep], p0[keep])), float(bas(yB[keep], p0[keep]))


def main():
    labels = pd.read_csv(os.path.join(ROOT, 'TrainLabels.csv'))
    lab = dict(zip(labels['IdFeedBack'], labels['Prediction']))
    files = sorted(glob.glob(os.path.join(ROOT, 'train', 'Data_S*_Sess*.csv')))
    subs = {}
    for f in files:
        m = re.search(r'Data_(S\d+)_Sess(\d+)\.csv$', f)
        subs.setdefault(m.group(1), {})[int(m.group(2))] = f
    rows = []
    for subj in sorted(subs):
        sess = subs[subj]
        cache = {}
        for s, f in sess.items():
            E, cols = load_session(f)
            ids = ['%s_Sess%02d_FB%03d' % (subj, s, k + 1) for k in range(len(E))]
            y = np.array([lab.get(i, -1) for i in ids])
            ok = y >= 0
            cache[s] = (feats(E[ok]), y[ok].astype(int))
        deltas = []
        for a, b in ((1, 2), (2, 3), (3, 4), (4, 5)):
            if a not in cache or b not in cache:
                continue
            FA, yA = cache[a]; FB, yB = cache[b]
            if len(np.unique(yA)) < 2 or len(yB) < BLOCK + 10 or len(np.unique(yB[BLOCK:])) < 2:
                continue
            d, b0 = run_cell(FA, yA, FB, yB)
            deltas.append((a, b, d, b0, float(np.mean(yA == 1)), float(np.mean(yB == 1)), len(yB)))
        if deltas:
            dm = float(np.mean([x[2] for x in deltas]))
            rows.append(dict(subj=subj, delta=dm, pairs=deltas))
            print('%s  pairs %d  mean delta %+0.4f  BA none %.3f' % (subj, len(deltas), dm, np.mean([x[3] for x in deltas])), flush=True)
    vals = np.array([r['delta'] for r in rows])
    print('---')
    print('subjects %d  mean %+0.4f  positive %d  sign p=%.4f  wilcoxon p=%.4f'
          % (len(vals), vals.mean(), int((vals > 0).sum()), binomtest(int((vals > 0).sum()), len(vals), 0.5).pvalue, wilcoxon(vals).pvalue))
    json.dump(rows, open(OUT, 'w'), indent=1)
    print('wrote', OUT)


if __name__ == '__main__':
    main()