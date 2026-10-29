# -*- coding: utf-8 -*-
"""v43: direct measurement of the temporal structure of the real session shift.

For every cell we take the sequence of block displacements
d_b = P W (mu_b - mu_A) (b = 1 .. B, block length m) and summarise it by

  trend   ||slope|| * B / mean ||d_b||     Theil-Sen slope of each component,
                                           scaled to the whole session
  jump    median ||d_{b+1} - d_b|| / mean ||d_b||
  scatter std(d_b) / mean ||d_b||
  R2      share of the variance of d_b explained by a linear ramp

These are measurements of the data, not of a model, so they can say whether a
dataset looks trend-dominated (gal) or jump-dominated (SEED) without assuming
which mechanism is at work.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "drift_measure.txt")
L = []
M = 15
SOURCE_ONLY = ("euc", "csp", "de", "Ftime", "pow")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def pairs(ds):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    return [p for p in ps if p["rep"] in SOURCE_ONLY]


def theil(x, y):
    n = len(x)
    s = [(y[j] - y[i]) / (x[j] - x[i]) for i in range(n) for j in range(i + 1, n)]
    return float(np.median(s)) if s else 0.0


def cell(A, ya, Bt, m):
    clf = C.make("lda").fit(A, ya)
    K = len(np.asarray(clf.classes_))
    W = C.linear_weights(clf, A.shape[1], K)
    F = np.eye(K) - np.ones((K, K)) / K
    muA = A.mean(0)
    n = len(Bt)
    blocks = [(a, min(a + m, n)) for a in range(0, n, m)]
    D = np.array([F @ (W @ (Bt[a:b].mean(0) - muA)) for a, b in blocks])
    if len(D) < 4:
        return None
    scale = float(np.mean(np.linalg.norm(D, axis=1))) + 1e-12
    idx = np.arange(len(D))
    slope = np.array([theil(idx, D[:, k]) for k in range(K)])
    trend = float(np.linalg.norm(slope) * len(D) / scale)
    jump = float(np.median(np.linalg.norm(np.diff(D, axis=0), axis=1)) / scale)
    scatter = float(np.std(D, axis=0).mean() / scale)
    # R2 of a linear ramp per component, averaged
    r2 = []
    for k in range(K):
        p = np.polyfit(idx, D[:, k], 1)
        res = D[:, k] - np.polyval(p, idx)
        ss = float(np.sum((D[:, k] - D[:, k].mean()) ** 2)) + 1e-15
        r2.append(1.0 - float(np.sum(res ** 2)) / ss)
    return dict(trend=trend, jump=jump, scatter=scatter, r2=float(np.mean(r2)),
                B=len(D))


def main():
    say("v43: temporal structure of the real block-mean displacement, m=%d" % M)
    say("  trend = Theil-Sen slope x B / mean||d||   jump = median|d_{b+1}-d_b|/mean||d||")
    say("")
    say("  %-6s %-6s %-8s %-8s %-8s %-8s %-8s" %
        ("ds", "cells", "trend", "jump", "scatter", "R2", "blocks"))
    for ds in ("gal", "seed", "2b", "2a", "ner"):
        vals = []
        for p in pairs(ds):
            r = cell(p["A"], p["ya"], p["B"], M)
            if r:
                vals.append(r)
        if not vals:
            continue
        say("  %-6s %-6d %-8.3f %-8.3f %-8.3f %-8.3f %-8.1f"
            % (ds, len(vals), np.median([v["trend"] for v in vals]),
               np.median([v["jump"] for v in vals]),
               np.median([v["scatter"] for v in vals]),
               np.median([v["r2"] for v in vals]),
               np.median([v["B"] for v in vals])))
    say("")
    say("  Spearman over all cells: trend vs jump")
    from scipy import stats
    allv = []
    for ds in ("gal", "seed", "2b", "2a", "ner"):
        for p in pairs(ds):
            r = cell(p["A"], p["ya"], p["B"], M)
            if r:
                allv.append((ds, r))
    t = [v["trend"] for _, v in allv]
    j = [v["jump"] for _, v in allv]
    say("    rho(trend, jump) = %+.3f over %d cells" % (stats.spearmanr(t, j)[0], len(allv)))
    print("done", P)


if __name__ == "__main__":
    main()
