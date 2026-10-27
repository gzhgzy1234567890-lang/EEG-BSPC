# -*- coding: utf-8 -*-
"""v8: per-subject calibration with a bootstrap interval (referee item 1)."""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "exp10.txt")
L = []


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def ece(yi, P, bins=10):
    conf = P.max(1)
    pred = P.argmax(1)
    hit = (pred == yi).astype(float)
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for i in range(bins):
        m = (conf > edges[i]) & (conf <= edges[i + 1])
        if m.sum() == 0:
            continue
        e += m.mean() * abs(hit[m].mean() - conf[m].mean())
    return float(e)


def proba(clf, X):
    P = np.asarray(clf.predict_proba(X), float)
    return P


def boot(a, n=5000, seed=0):
    a = np.asarray(a, float)
    rs = np.random.RandomState(seed)
    m = [rs.choice(a, len(a), replace=True).mean() for _ in range(n)]
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main():
    say("v8 calibration per subject (LDA, 60 cells per dataset)")
    say("  %-5s %-6s %-4s %-9s %-20s" % ("ds", "cond", "n", "median ECE", "bootstrap 95% CI of the mean"))
    for ds in ("2b", "seed", "gal"):
        ps = C.all_pairs((ds,))
        if ds == "gal":
            ps = [p for p in ps
                  if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        if len(ps) > 60:
            idx = np.linspace(0, len(ps) - 1, 60).astype(int)
            ps = [ps[i] for i in idx]
        for cond in ("none", "zero", "mean"):
            per = {}
            for p in ps:
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                clf = C.make("lda").fit(A, ya)
                classes = np.asarray(clf.classes_)
                g = Bt.mean(0) - A.mean(0)
                X = Bt if cond == "none" else (Bt - Bt.mean(0) if cond == "zero" else Bt - g)
                Pm = proba(clf, X)
                yi = np.array([int(np.where(classes == c)[0][0]) for c in yb])
                per.setdefault(p["subj"], []).append(ece(yi, Pm))
            vals = np.array([np.mean(v) for v in per.values()])
            lo, hi = boot(vals)
            say("  %-5s %-6s %-4d %-9.4f [%+.4f, %+.4f]" % (ds, cond, len(vals),
                                                             np.median(vals), lo, hi))
    print("done", P)


if __name__ == "__main__":
    main()
