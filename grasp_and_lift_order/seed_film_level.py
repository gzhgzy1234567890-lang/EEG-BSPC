# -*- coding: utf-8 -*-
"""SEED: film-level true-class recall for no correction vs full correction, subject level."""
import glob, math, os, re, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
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


def film_recall(y, pred, g):
    out = []
    for f in np.unique(g):
        m = g == f
        if m.sum() == 0:
            continue
        c = np.bincount(y[m], minlength=3).argmax()
        out.append(float(np.mean(pred[m] == c)))
    return float(np.mean(out))


def main():
    by = load()
    per_subj = {}
    for sub, sess in sorted(by.items()):
        sess = sorted(sess)
        for i in range(len(sess)):
            for j in range(i + 1, len(sess)):
                _, XA, yA, gA = sess[i]
                _, XB, yB, gB = sess[j]
                clf = LDA(solver='lsqr', shrinkage='auto').fit(XA, yA)
                kc = len(clf.classes_)
                W = clf.coef_ if kc > 2 else np.vstack([-clf.coef_, clf.coef_])
                Fm = np.eye(kc) - np.ones((kc, kc)) / kc
                muA = XA.mean(0)
                S = clf.decision_function(XB)
                n = len(yB)
                blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
                D = np.array([Fm @ (W @ (XB[a:b].mean(0) - muA)) for a, b in blocks])
                bm = np.zeros((n, kc))
                for k, (a, b) in enumerate(blocks):
                    if k > 0:
                        bm[a:b] = D[:k].mean(0)
                p0 = clf.classes_[np.argmax(S, 1)]
                p1 = clf.classes_[np.argmax(S - bm, 1)]
                r0 = film_recall(yB, p0, gB)
                r1 = film_recall(yB, p1, gB)
                per_subj.setdefault(sub, []).append(r1 - r0)
    vals = np.array([np.mean(v) for v in per_subj.values()])
    rng = np.random.default_rng(20261030)
    boot = [rng.choice(vals, len(vals), replace=True).mean() for _ in range(10000)]
    lo, hi = np.percentile(boot, [2.5, 97.5])
    neg = int((vals < 0).sum()); pos = int((vals > 0).sum())
    n = len(vals)
    p = min(1.0, 2.0 * sum(math.factorial(n) // (math.factorial(i) * math.factorial(n - i)) for i in range(min(neg, pos) + 1)) / 2.0 ** n)
    print('SEED film-level recall, full correction minus none:')
    print('  subjects %d  mean %+.4f  CI [%+.4f, %+.4f]  negative %d positive %d  sign p %.3g'
          % (n, vals.mean(), lo, hi, neg, pos, p))
    print('  per-subject:', np.round(vals, 3))


if __name__ == '__main__':
    main()