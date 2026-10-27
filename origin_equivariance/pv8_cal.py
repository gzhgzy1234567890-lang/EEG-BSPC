# -*- coding: utf-8 -*-
"""Calibration on every cell: per-subject ECE with a bootstrap interval."""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "cal.txt")
L = []


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def ece(yi, Pm, bins=10):
    conf, pred = Pm.max(1), Pm.argmax(1)
    hit = (pred == yi).astype(float)
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for i in range(bins):
        m = (conf > edges[i]) & (conf <= edges[i + 1])
        if m.sum():
            e += m.mean() * abs(hit[m].mean() - conf[m].mean())
    return float(e)


def boot(a, n=5000, seed=0):
    a = np.asarray(a, float)
    rs = np.random.RandomState(seed)
    m = [rs.choice(a, len(a), replace=True).mean() for _ in range(n)]
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def pairs(ds):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    return ps


def main():
    say("calibration, every cell, LDA")
    say("  %-5s %-6s %-4s %-10s %-22s" % ("ds", "cond", "n", "median ECE", "95% CI of the mean"))
    for ds in ("2b", "seed", "gal"):
        per = {"none": {}, "zero": {}, "mean": {}}
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            yi = np.array([int(np.where(classes == c)[0][0]) for c in yb])
            g = Bt.mean(0) - A.mean(0)
            for cond, X in (("none", Bt), ("zero", Bt - Bt.mean(0)), ("mean", Bt - g)):
                Pm = np.asarray(clf.predict_proba(X), float)
                per[cond].setdefault(p["subj"], []).append(ece(yi, Pm))
        for cond in ("none", "zero", "mean"):
            v = np.array([np.mean(x) for x in per[cond].values()])
            lo, hi = boot(v)
            say("  %-5s %-6s %-4d %-10.4f [%+.4f, %+.4f]" % (ds, cond, len(pairs(ds)),
                                                             np.median(v), lo, hi))
    print("done", P)


if __name__ == "__main__":
    main()
