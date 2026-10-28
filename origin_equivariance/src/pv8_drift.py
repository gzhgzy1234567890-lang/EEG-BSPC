# -*- coding: utf-8 -*-
"""v22: real session shifts decomposed into the classifier-sensitive subspace and
its complement; plus Holm-adjusted tests across the five datasets."""
import os
import sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "drift.txt")
L = []
DS = ("2a", "2b", "seed", "ner", "gal")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def pairs(ds):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    return ps


def main():
    say("v22 A: the real session shift, decomposed (LDA)")
    say("  score shift = ||P W d||, null part = ||d - W^+ W d||, d = mu_B - mu_A")
    say("")
    rows = []
    for ds in DS:
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            W = C.linear_weights(clf, A.shape[1], K)
            d = Bt.mean(0) - A.mean(0)
            s = W @ d
            s = s - s.mean()
            Wp = np.linalg.pinv(W)
            d_null = d - Wp @ (W @ d)
            pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
                   - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
            gain = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - (Bt.mean(0) - A.mean(0))), 1)])
                    - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
            rows.append((ds, float(np.linalg.norm(s)), float(np.linalg.norm(d_null)), pen, gain))
    arr = np.array([[r[1], r[2], r[3], r[4]] for r in rows])
    for name, k in (("score-space shift", 0), ("null part", 1)):
        say("  %-18s vs penalty: rho %+.3f (n=%d)   vs gain: rho %+.3f"
            % (name, stats.spearmanr(arr[:, k], arr[:, 2])[0], len(arr),
               stats.spearmanr(arr[:, k], arr[:, 3])[0]))
    # within-dataset, to remove the between-family effect
    say("")
    say("  within-dataset correlations (median over the five):")
    ws, wn = [], []
    for ds in DS:
        m = np.array([r[0] == ds for r in rows])
        if m.sum() < 12:
            continue
        ws.append(stats.spearmanr(arr[m, 0], arr[m, 2])[0])
        wn.append(stats.spearmanr(arr[m, 1], arr[m, 2])[0])
    say("    score-space shift: %s" % np.round(ws, 3))
    say("    null part:         %s" % np.round(wn, 3))

    say("")
    say("v22 B: Holm across the five per-dataset Wilcoxon tests of mean - none")
    ps = {"2a": 3.9e-3, "2b": 3.9e-3, "seed": 6.1e-5, "ner": 0.32, "gal": 0.052}
    order = sorted(ps, key=lambda k: ps[k])
    m = len(ps)
    adj = {}
    run = 0.0
    for i, k in enumerate(order):
        val = min(1.0, (m - i) * ps[k])
        run = max(run, val)
        adj[k] = run
    for k in order:
        say("  %-5s raw %.2e  Holm %.3f" % (k, ps[k], adj[k]))
    print("done", P)


if __name__ == "__main__":
    main()
