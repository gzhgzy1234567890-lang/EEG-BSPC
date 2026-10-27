# -*- coding: utf-8 -*-
"""Print the per-unit table for the corrected (centred-scale) z_w."""
import os
import sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "units_centred.txt")
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
    rows = []
    for ds in DS:
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            S = C.score_matrix(clf, A)
            Sc = S - S.mean(1, keepdims=True)
            sig = np.maximum(Sc.std(0), 1e-12)
            W = C.linear_weights(clf, A.shape[1], K)
            proj = W @ A.mean(0)
            proj = proj - proj.mean()
            zw = float(np.linalg.norm(proj / sig) / np.sqrt(K))
            zT = float(np.linalg.norm(A.mean(0)) / np.linalg.norm(np.maximum(A.std(0), 1e-12)))
            pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
                   - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
            gain = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - (Bt.mean(0) - A.mean(0))), 1)])
                    - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
            rows.append((ds, p["rep"], zw, zT, pen, gain))
    say("  %-5s %-7s %-5s %-9s %-9s %-9s %-9s"
        % ("ds", "rep", "n", "z_T", "z_w", "penalty", "gain"))
    units = []
    for u in sorted(set((r[0], r[1]) for r in rows)):
        q = [r for r in rows if r[0] == u[0] and r[1] == u[1]]
        v = (u[0], u[1], len(q), np.median([r[3] for r in q]),
             np.median([r[2] for r in q]), np.median([r[4] for r in q]),
             np.median([r[5] for r in q]))
        units.append(v)
        say("  %-5s %-7s %-5d %-9.2f %-8.3f %-9.4f %-9.4f"
            % (v[0], v[1], v[2], v[3], v[4], v[5], v[6]))
    z = np.array([u[4] for u in units])
    p = np.array([u[5] for u in units])
    g = np.array([u[6] for u in units])
    say("")
    say("  unit level: spearman(z_w, penalty) %+.3f ; spearman(z_w, gain) %+.3f"
        % (stats.spearmanr(z, p)[0], stats.spearmanr(z, g)[0]))
    print("done", P)


if __name__ == "__main__":
    main()
