# -*- coding: utf-8 -*-
"""SEED film-disjoint check: train on a subset of films, evaluate on unseen films."""
import glob, os, re, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
D = r'G:\Work_work\math\EEG\local_analysis\cache_seed'
BLOCK = 15


def load():
    by = {}
    for f in sorted(glob.glob(os.path.join(D, '*.npz'))):
        m = re.match(r'(\d+)_(\d+)\.npz', os.path.basename(f))
        if not m:
            continue
        z = np.load(f, allow_pickle=True)
        by.setdefault(int(m.group(1)), []).append(
            (int(m.group(2)), z['X'].astype(float), z['y'].astype(int), z['g'].astype(int)))
    return by


def films_by_class(y, g):
    d = {}
    for f in np.unique(g):
        d.setdefault(int(np.bincount(y[g == f], minlength=3).argmax()), []).append(int(f))
    return d


def main():
    by = load()
    res = {}
    for sub, sess in sorted(by.items()):
        sess = sorted(sess)
        for i in range(len(sess)):
            for j in range(i + 1, len(sess)):
                _, XA, yA, gA = sess[i]
                _, XB, yB, gB = sess[j]
                fc = films_by_class(yA, gA)
                if len(fc) < 3:
                    continue
                # hold out the last film of each class, train on the rest
                test_f, train_f = [], []
                for k, fs in fc.items():
                    test_f.append(fs[-1]); train_f += fs[:-1]
                mtrain = np.isin(gA, train_f); mtest = np.isin(gB, test_f)
                if mtrain.sum() < 50 or mtest.sum() < 50:
                    continue
                if len(np.unique(yB[mtest])) < 3:
                    continue
                clf = LDA(solver='lsqr', shrinkage='auto').fit(XA[mtrain], yA[mtrain])
                K = len(clf.classes_)
                W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
                Fm = np.eye(K) - np.ones((K, K)) / K
                muA = XA[mtrain].mean(0)
                S = clf.decision_function(XB)
                if S.ndim == 1:
                    S = np.column_stack([-S, S])
                n = len(yB)
                blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
                Dd = np.array([Fm @ (W @ (XB[a:b].mean(0) - muA)) for a, b in blocks])
                bm = np.zeros((n, K))
                for k, (a, b) in enumerate(blocks):
                    if k > 0:
                        bm[a:b] = Dd[:k].mean(0)
                p0 = clf.classes_[np.argmax(S, 1)]
                p1 = clf.classes_[np.argmax(S - bm, 1)]
                keep = mtest & (np.arange(n) >= BLOCK)
                if keep.sum() < 30:
                    continue
                d = float(bas(yB[keep], p1[keep]) - bas(yB[keep], p0[keep]))
                res.setdefault(sub, []).append(d)
    vals = np.array([np.mean(v) for v in res.values()])
    rng = np.random.default_rng(20261031)
    boot = [rng.choice(vals, len(vals), replace=True).mean() for _ in range(10000)]
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print('film-disjoint: subjects %d  mean %+0.4f  CI [%+0.4f, %+0.4f]  positive %d' %
          (len(vals), vals.mean(), lo, hi, int((vals > 0).sum())))
    print('per subject:', np.round(vals, 3))


if __name__ == '__main__':
    main()