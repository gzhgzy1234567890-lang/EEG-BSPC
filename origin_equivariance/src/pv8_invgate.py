# -*- coding: utf-8 -*-
"""v34: the estimator made origin-invariant.

The weight must be built from displacements relative to the source session, not
from absolute projections: with d_b = P W (mu_b - mu_A) the weight

    lambda = ||dbar||^2 / (||dbar||^2 + K V_d / B)

is unchanged by a common translation of the features (every d_b is), while the
previous version used ||zbar||^2 with z_b = W mu_b, which is not.  The corrected
scores are s - lambda dbar.
"""
import glob
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores

P = os.path.join(C.OUT, "invgate.txt")
L = []
CACHE4 = r"G:\Work_work\math\EEG\local_analysis\cache_seed4_iv"
K0 = {"2b": 20, "2a": 20, "gal": 20, "ner": 20, "seed": 50}
MS = (15, 25, 50)
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


def ci(v):
    rs = np.random.RandomState(0)
    b = np.array([np.mean(rs.choice(v, len(v))) for _ in range(4000)])
    return v.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5)


def run(A, ya, Bt, yb, k0, m):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    K = len(classes)
    W = C.linear_weights(clf, A.shape[1], K)
    Pm = np.eye(K) - np.ones((K, K)) / K
    muA = A.mean(0)
    n = len(yb)
    S0 = scores(Bt, W, np.asarray(clf.intercept_, float).ravel(), K)
    blocks = [(t, min(t + m, n)) for t in range(k0, n, m)]
    d = [Pm @ (W @ (Bt[a:b].mean(0) - muA)) for a, b in blocks]

    S = S0.copy()
    for i, (a, b) in enumerate(blocks):
        if i == 0:
            continue
        D = np.array(d[:i])
        dbar = D.mean(0)
        if len(D) >= 2:
            vd = D.var(0).sum()
            lam = float(np.clip((dbar @ dbar) / (dbar @ dbar + K * vd / len(D) + 1e-12), 0, 1))
        else:
            lam = 0.5
        S[a:b] = S0[a:b] - lam * dbar[None, :]
    ba = C.ba(yb[k0:], classes[np.argmax(S[k0:], 1)])
    ba0 = C.ba(yb[k0:], classes[np.argmax(S0[k0:], 1)])
    # translation check: shift every feature by c, refit, and compare predictions
    c = A.std(0) * 0.5
    clf2 = C.make("lda").fit(A + c, ya)
    S2 = scores(Bt + c, C.linear_weights(clf2, A.shape[1], K),
                np.asarray(clf2.intercept_, float).ravel(), K)
    blocks2 = blocks
    d2 = [Pm @ (C.linear_weights(clf2, A.shape[1], K) @ ((Bt + c)[a:b].mean(0) - (A + c).mean(0)))
          for a, b in blocks2]
    S2c = S2.copy()
    for i, (a, b) in enumerate(blocks2):
        if i == 0:
            continue
        D = np.array(d2[:i])
        dbar = D.mean(0)
        vd = D.var(0).sum() if len(D) >= 2 else 0.0
        lam = float(np.clip((dbar @ dbar) / (dbar @ dbar + K * vd / len(D) + 1e-12), 0, 1)) if len(D) >= 2 else 0.5
        S2c[a:b] = S2[a:b] - lam * dbar[None, :]
    same = float(np.mean(S2c[k0:].argmax(1) == S[k0:].argmax(1))) if len(S[k0:]) else np.nan
    return ba - ba0, same


def main():
    say("v34: origin-invariant weight, lambda from ||dbar||^2 with d_b = PW(mu_b - mu_A)")
    say("")
    for ds in ("2b", "2a", "seed", "gal", "ner"):
        for m in MS:
            g, sh = zip(*[run(p["A"], p["ya"], p["B"], p["yb"], K0[ds], m) for p in pairs(ds)])
            lo, hi = ci(np.array(g))[1:]
            say("  %-5s m=%-3d gain %+.4f [%+.4f, %+.4f]  translation agreement %.3f"
                % (ds, m, np.mean(g), lo, hi, np.nanmean(sh)))
        say("")
    subs = sorted(set(int(os.path.basename(f).split("_")[0])
                      for f in glob.glob(os.path.join(CACHE4, "*.npz"))))
    for m in MS:
        g = []
        for sub in subs:
            S = {}
            for sess in (1, 2, 3):
                f = os.path.join(CACHE4, "%02d_%d.npz" % (sub, sess))
                if os.path.exists(f):
                    d = np.load(f)
                    S[sess] = (d["X"].astype(np.float64), d["y"].astype(int))
            for i in sorted(S):
                for j in sorted(S):
                    if i != j:
                        g.append(run(S[i][0], S[i][1], S[j][0], S[j][1], 50, m)[0])
        lo, hi = ci(np.array(g))[1:]
        say("  seed4 m=%-3d gain %+.4f [%+.4f, %+.4f]" % (m, np.mean(g), lo, hi))
    print("done", P)


if __name__ == "__main__":
    main()
