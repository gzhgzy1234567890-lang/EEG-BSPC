# -*- coding: utf-8 -*-
"""v8 check: the correction can be applied in decision space.

Corollary of Proposition 2: for an affine model only W(mu_B - mu_A) matters, so
subtracting that K-vector from the K scores must reproduce the feature-space
correction exactly, with no access to the features.  Verified for three linear
families on two datasets.

Output: results/exp9.txt
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

L = []
P = os.path.join(C.OUT, "exp9.txt")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    say("v8 exp I: decision-space form of the correction")
    say("  delta_k = w_k'(mu_B - mu_A); scores shifted by -delta, then argmax")
    say("")
    say("  %-5s %-6s %-5s %-9s %-9s %-12s" % ("ds", "clf", "n", "feat-space", "dec-space", "max |diff|"))
    for ds in ("2b", "2a", "gal"):
        ps = C.all_pairs((ds,))
        if ds == "gal":
            ps = [p for p in ps
                  if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        if len(ps) > 60:
            idx = np.linspace(0, len(ps) - 1, 60).astype(int)
            ps = [ps[i] for i in idx]
        for kind in ("lda", "logit", "svm"):
            a, b, dmax = [], [], 0.0
            for p in ps:
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                clf = C.make(kind).fit(A, ya)
                classes = np.asarray(clf.classes_)
                K = len(classes)
                g = Bt.mean(0) - A.mean(0)
                Pf = classes[np.argmax(C.score_matrix(clf, Bt - g), 1)]
                W = C.linear_weights(clf, A.shape[1], K)
                delta = W @ g
                S = C.score_matrix(clf, Bt)
                Pd = classes[np.argmax(S - delta[None, :], 1)]
                a.append(C.ba(yb, Pf))
                b.append(C.ba(yb, Pd))
                dmax = max(dmax, float(np.mean(Pf != Pd)))
            if not a:
                continue
            say("  %-5s %-6s %-5d %-9.4f %-9.4f %-12.1e"
                % (ds, kind, len(ps), np.mean(a), np.mean(b), dmax))
    say("")
    say("  A value of 0.0e+00 in the last column means the two forms returned")
    say("  identical predictions for every sample of every cell.")
    print("done", P)


if __name__ == "__main__":
    main()
