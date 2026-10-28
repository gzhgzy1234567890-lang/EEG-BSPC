# -*- coding: utf-8 -*-
"""Sensitivity of the shrunk estimator to tau."""
import io
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import pairs, scores, KS

P = os.path.join(C.OUT, "causal_tau.txt")
L = []


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    say("tau sensitivity of Equation (9); paired difference against none")
    for ds in ("2b", "2a", "seed", "gal", "ner"):
        k = KS[ds]
        out = {}
        for tau in (20.0, 50.0, 200.0):
            vals = []
            for p in pairs(ds):
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                clf = C.make("lda").fit(A, ya)
                classes = np.asarray(clf.classes_)
                K = len(classes)
                W = C.linear_weights(clf, A.shape[1], K)
                b = np.asarray(clf.intercept_, float).ravel()
                muA = A.mean(0)
                n = len(yb)
                T = np.arange(k, n)
                cs = np.cumsum(Bt, axis=0)
                cnt = np.arange(1, n + 1)[:, None]
                mu_cum = cs / cnt
                mu_prev = np.vstack([np.zeros((1, Bt.shape[1])), mu_cum[:-1]])
                neff = np.arange(n)[:, None].astype(float)
                lam = neff / (neff + tau)
                S = scores(Bt[T] - mu_prev[T] * lam[T] + lam[T] * muA, W, b, K)
                ba = C.ba(yb[T], classes[np.argmax(S, 1)])
                S0 = scores(Bt[T], W, b, K)
                ba0 = C.ba(yb[T], classes[np.argmax(S0, 1)])
                vals.append(ba - ba0)
            out[tau] = np.mean(vals)
        say("  %-5s tau=20 %+.4f   tau=50 %+.4f   tau=200 %+.4f"
            % (ds, out[20.0], out[50.0], out[200.0]))
    print("done", P)


if __name__ == "__main__":
    main()
