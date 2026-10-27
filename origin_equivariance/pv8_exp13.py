# -*- coding: utf-8 -*-
"""v9 additions: calibration intervals on every cell, and streaming variance."""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "exp13.txt")
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


def pairs(ds):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    return ps


def boot(a, n=5000, seed=0):
    a = np.asarray(a, float)
    rs = np.random.RandomState(seed)
    m = [rs.choice(a, len(a), replace=True).mean() for _ in range(n)]
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main():
    say("v9 exp L")
    say("")
    say("L1  calibration per subject, every cell")
    say("  %-5s %-6s %-4s %-10s %-22s" % ("ds", "cond", "n", "median ECE", "95% CI of the mean"))
    for ds in ("2b", "seed", "gal"):
        ps = pairs(ds)
        for cond in ("none", "zero", "mean"):
            per = {}
            for p in ps:
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                clf = C.make("lda").fit(A, ya)
                classes = np.asarray(clf.classes_)
                g = Bt.mean(0) - A.mean(0)
                X = Bt if cond == "none" else (Bt - Bt.mean(0) if cond == "zero" else Bt - g)
                Pm = np.asarray(clf.predict_proba(X), float)
                yi = np.array([int(np.where(classes == c)[0][0]) for c in yb])
                per.setdefault(p["subj"], []).append(ece(yi, Pm))
            v = np.array([np.mean(x) for x in per.values()])
            lo, hi = boot(v)
            say("  %-5s %-6s %-4d %-10.4f [%+.4f, %+.4f]" % (ds, cond, len(ps), np.median(v), lo, hi))
    say("")
    say("L2  streaming, random order, five permutations")
    say("  %-5s %-8s %-18s %-9s" % ("ds", "k", "mean acc", "sd over seeds"))
    for ds in ("2b", "seed", "gal"):
        ps = pairs(ds)
        if len(ps) > 60:
            idx = np.linspace(0, len(ps) - 1, 60).astype(int)
            ps = [ps[i] for i in idx]
        for k in (5, 20):
            vals = []
            for seed in range(5):
                rng = np.random.RandomState(100 + seed)
                acc = []
                for p in ps:
                    A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                    clf = C.make("lda").fit(A, ya)
                    classes = np.asarray(clf.classes_)
                    order = rng.permutation(len(yb))
                    B2, y2 = Bt[order], yb[order]
                    run = A.mean(0).copy()
                    preds = np.empty(len(y2), dtype=classes.dtype)
                    for i in range(len(y2)):
                        preds[i] = classes[np.argmax(C.score_matrix(
                            clf, (B2[i] - run + A.mean(0))[None, :]), 1)[0]]
                        run = run + (B2[i] - run) / (i + 2.0)
                    if len(y2) > k + 5:
                        acc.append(C.ba(y2[k:], preds[k:]))
                vals.append(np.mean(acc))
            say("  %-5s %-8d %-18.4f %-9.4f" % (ds, k, np.mean(vals), np.std(vals)))
    print("done", P)


if __name__ == "__main__":
    main()
