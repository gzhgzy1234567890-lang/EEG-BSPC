# -*- coding: utf-8 -*-
"""Matched-scored-samples control: score the same grasp-and-lift samples under both orderings."""
import sys
import numpy as np
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
import gal_order_test as G
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BLOCK = 15


def keys(F):
    return [np.round(F[i], 6).tobytes() for i in range(len(F))]


def run(cache):
    data = G.load(cache)
    subs = {}
    for (s, i) in data:
        subs.setdefault(s, []).append(i)
    out = []
    for s, idx in sorted(subs.items()):
        idx = sorted(idx)
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                Fa, ya = data[(s, idx[a])]
                Fb, yb = data[(s, idx[b])]
                clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
                K = len(clf.classes_)
                W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
                Fm = np.eye(K) - np.ones((K, K)) / K
                muA = Fa.mean(0)
                S = clf.decision_function(Fb)
                if S.ndim == 1:
                    S = np.column_stack([-S, S])
                n = len(yb)
                blocks = [(x, min(x + BLOCK, n)) for x in range(0, n, BLOCK)]
                D = np.array([Fm @ (W @ (Fb[x:y].mean(0) - muA)) for x, y in blocks])
                bm = np.zeros((n, K))
                for k, (x, y) in enumerate(blocks):
                    if k > 0:
                        bm[x:y] = D[:k].mean(0)
                p0 = clf.classes_[np.argmax(S, 1)]
                p1 = clf.classes_[np.argmax(S - bm, 1)]
                out.append((s, idx[a], idx[b], keys(Fb), yb, p0, p1))
    return out


def main():
    A = run(G.TIME)
    B = run(G.SORTED)
    assert len(A) == len(B)
    d_match, plain = [], []
    for (sa, i, j, kt, yt, p0t, p1t), (sb, _, _, ks, ys, p0s, p1s) in zip(sorted(A), sorted(B)):
        assert sa == sb
        yb = yt
        order = np.argsort(yb, kind='stable')          # sorted position -> time position
        pos_s = np.empty(len(yb), dtype=int)
        pos_s[order] = np.arange(len(yb))              # time position -> sorted position
        keep = np.array([bool(p >= BLOCK and pos_s[p] >= BLOCK) for p in range(len(yb))], dtype=bool)
        if keep.sum() < 20:
            continue
        y = yb[keep]
        if len(np.unique(y)) < 2:
            continue
        d_match.append(bas(y, p1t[keep]) - bas(y, p0t[keep]))
        d_sorted = bas(yb[keep], p1s[pos_s[keep]]) - bas(yb[keep], p0s[pos_s[keep]])
        plain.append(d_sorted)
    d = np.array(d_match); p = np.array(plain)
    print('cells', len(d))
    print('same samples, time order delta:  %+.4f' % d.mean())
    print('same samples, sorted order delta: %+.4f' % p.mean())
    print('difference (sorted - time):        %+.4f' % (p - d).mean())
    print('sorted more negative in %d of %d cells' % (int(((p - d) < 0).sum()), len(d)))


if __name__ == '__main__':
    main()