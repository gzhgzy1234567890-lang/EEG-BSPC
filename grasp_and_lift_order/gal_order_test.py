# -*- coding: utf-8 -*-
"""Same estimator as the paper, run on the sorted cache and on the time-ordered cache."""
import glob, json, os, re, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas

SORTED = r'G:\Work_work\math\EEG\local_analysis\cache_gal'
TIME = r'G:\Work_work\math\EEG\local_analysis\cache_gal_time'
BLOCK = 15
LAMS = (0.0, 0.25, 0.5, 0.75, 1.0)


def load(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, '*.npz'))):
        m = re.match(r'(subj\d+)_series(\d+)\.npz', os.path.basename(f))
        z = np.load(f)
        out[(m.group(1), int(m.group(2)))] = (z['F'], z['y'])
    return out


def cell(Fa, ya, Fb, yb):
    clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
    kc = len(clf.classes_)
    W = clf.coef_ if kc > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(kc) - np.ones((kc, kc)) / kc
    muA = Fa.mean(0)
    S = clf.decision_function(Fb)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    n = len(yb)
    blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
    D = [Fm @ (W @ (Fb[a:b].mean(0) - muA)) for a, b in blocks]
    bm = np.zeros((n, kc))
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            bm[a:b] = np.mean(D[:k], axis=0)
    res = []
    for lam in LAMS:
        pred = clf.classes_[np.argmax(S - lam * bm, 1)]
        res.append(bas(yb[BLOCK:], pred[BLOCK:]))
    return np.array(res)


def run(cache, tag):
    data = load(cache)
    subs = {}
    for (s, i) in data:
        subs.setdefault(s, []).append(i)
    curves, deltas = [], []
    for s, idx in sorted(subs.items()):
        idx = sorted(idx)
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                Fa, ya = data[(s, idx[a])]
                Fb, yb = data[(s, idx[b])]
                curves.append(cell(Fa, ya, Fb, yb))
    C = np.array(curves)
    print('%-8s cells %3d  BA(lambda) %s' % (tag, len(C), np.round(C.mean(0), 4)))
    print('         delta(1-0) = %+.4f' % (C[:, -1] - C[:, 0]).mean())
    return C


if __name__ == '__main__':
    run(SORTED, 'sorted')
    if os.path.isdir(TIME) and glob.glob(os.path.join(TIME, '*.npz')):
        run(TIME, 'time')