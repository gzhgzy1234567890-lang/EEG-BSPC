# -*- coding: utf-8 -*-
"""v12 -> v13: is the signed law the same law when it is parameterised the way
the Gaussian model requires?

Variant A (previous drafts): c = Phi^{-1}(BA_aligned), sigma = pooled SD of the
source scores, s and t* in pooled units.
Variant B (this script): c = (m1 - m0) / (2 sigma_w) from the source scores,
sigma_w = pooled within-class SD, s and t* in within-class units.  This is the
parameterisation the equal-variance Gaussian derivation actually uses.
"""
import os
import sys
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_exp14 import best_thr, ba_thr

P = os.path.join(C.OUT, "law2.txt")
L = []


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


def D(c, u):
    return 0.5 * (norm.cdf(c + u) + norm.cdf(c - u))


def auc(y, s):
    y = np.asarray(y, int)
    s = np.asarray(s, float)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    allv = np.concatenate([pos, neg])
    r = np.argsort(np.argsort(allv)) + 1.0
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)))


def main():
    say("v13: two parameterisations of the signed law")
    say("  %-5s %-6s %-5s %-8s %-8s %-8s %-8s %-8s"
        % ("ds", "clf", "n", "MAE_A", "r_A", "MAE_B", "r_B", "BAcheck"))
    for ds in ("2b", "2a", "gal", "ner"):
        for kind in ("lda", "logit", "svm"):
            dA, dB, obs, bachk = [], [], [], []
            for p in pairs(ds):
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                if ds == "2a":
                    ma, mb = np.isin(ya, [1, 2]), np.isin(yb, [1, 2])
                    A, ya, Bt, yb = A[ma], ya[ma], Bt[mb], yb[mb]
                if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
                    continue
                clf = C.make(kind).fit(A, ya)
                if len(np.asarray(clf.classes_)) != 2:
                    continue
                classes = np.asarray(clf.classes_)
                w = np.asarray(clf.coef_, float).ravel()
                sA = np.asarray(clf.decision_function(A), float).ravel()
                m0 = sA[ya == classes[0]].mean()
                m1 = sA[ya == classes[1]].mean()
                v0 = sA[ya == classes[0]].var(ddof=1)
                v1 = sA[ya == classes[1]].var(ddof=1)
                sig_p = max(sA.std(), 1e-9)
                sig_w = max(np.sqrt(0.5 * (v0 + v1)), 1e-9)
                muA, muB = A.mean(0), Bt.mean(0)
                s_al = np.asarray(clf.decision_function(Bt - muB + muA), float).ravel()
                s_ze = np.asarray(clf.decision_function(Bt - muB), float).ravel()
                ba_al = ba_thr(s_al, yb, classes, 0.0)
                ba_ze = ba_thr(s_ze, yb, classes, 0.0)
                # variant A
                tsA = best_thr(s_al, yb, classes) / sig_p
                shA = float(w @ muA) / sig_p
                cA = norm.ppf(np.clip(ba_al, 0.01, 0.99))
                dA.append(D(cA, tsA - shA) - D(cA, tsA))
                # variant B: within-class scale, c from the source separation
                tsB = best_thr(s_al, yb, classes) / sig_w
                shB = float(w @ muA) / sig_w
                cB = (m1 - m0) / (2.0 * sig_w)
                dB.append(D(cB, tsB - shB) - D(cB, tsB))
                obs.append(ba_ze - ba_al)
                bachk.append((ba_al, norm.cdf(cB)))
            if not dA:
                continue
            dA, dB, obs = np.array(dA), np.array(dB), np.array(obs)
            bc = np.mean(np.abs(np.array(bachk)[:, 0] - np.array(bachk)[:, 1]))
            say("  %-5s %-6s %-5d %-8.4f %-8.3f %-8.4f %-8.3f %-8.3f"
                % (ds, kind, len(dA), np.mean(np.abs(dA - obs)),
                   np.corrcoef(dA, obs)[0, 1], np.mean(np.abs(dB - obs)),
                   np.corrcoef(dB, obs)[0, 1], bc))
    say("")
    say("  BAcheck = mean |BA_aligned - Phi(c_B)| : how far the Gaussian model's")
    say("  implied accuracy is from the observed aligned accuracy.")
    print("done", P)


if __name__ == "__main__":
    main()
