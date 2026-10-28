# -*- coding: utf-8 -*-
"""v47: audit of the Kalman estimator before any claim is made about it.

Four configurations, same causal protocol, same blocks:

  k1  original: P0 = 1, q from the variance of successive differences, r from
      the within-block noise of the current block (the version used so far)
  k2  P0 = r                                (initialisation matched to the noise)
  k3  P0 = r, q = 0.05 r  fixed              (slow tracking)
  k4  P0 = r, q = 0.50 r  fixed              (fast tracking)

For every cell we log the gain trajectory, the fraction of blocks with gain
below 0.01 ("frozen"), the one-step error of the state against the block it is
applied to, and the balanced accuracy.  r is causal in k2-k4 (mean of the past
blocks' within-block noise); k1 keeps the original, slightly optimistic choice
so that the reported numbers can be reproduced.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores

P = os.path.join(C.OUT, "kalman_audit.txt")
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


def run(A, ya, Bt, yb, m):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    K = len(classes)
    W = C.linear_weights(clf, A.shape[1], K)
    F = np.eye(K) - np.ones((K, K)) / K
    muA = A.mean(0)
    n = len(yb)
    if n < 2 * m:
        return None
    S0 = scores(Bt, W, np.asarray(clf.intercept_, float).ravel(), K)
    blocks = [(a, min(a + m, n)) for a in range(0, n, m)]
    D = np.array([F @ (W @ (Bt[a:b].mean(0) - muA)) for a, b in blocks])
    # causal within-block noise per block
    r_b = []
    for a, b in blocks:
        Y = Bt[a:b] @ (F @ W).T
        Yc = Y - Y.mean(0, keepdims=True)
        r_b.append(float(np.sum(Yc * Yc) / max(b - a, 1) ** 2))
    r_b = np.array(r_b)

    variants = {
        "k1": dict(p0=1.0, qmode="diff", rmode="cur"),
        "k2": dict(p0="r", qmode="diff", rmode="past"),
        "k3": dict(p0="r", qmode=0.05, rmode="past"),
        "k4": dict(p0="r", qmode=0.50, rmode="past"),
    }
    out = {}
    for name, cfg in variants.items():
        S = S0.copy()
        state = np.zeros(K)
        Pk = None
        gains, errs = [], []
        for i, (a, b) in enumerate(blocks):
            if i == 0:
                state = D[0].copy()
                r0 = r_b[0]
                Pk = r0 if cfg["p0"] == "r" else float(cfg["p0"])
                gains.append(np.nan)
                continue
            r = r_b[i] if cfg["rmode"] == "cur" else float(np.mean(r_b[1:i]))
            if cfg["qmode"] == "diff":
                q = float(np.diff(D[:i], axis=0).var(0).sum()) / 2.0 if i >= 2 else r
            else:
                q = cfg["qmode"] * r
            Pk = Pk + q
            g = Pk / (Pk + max(r, 1e-12))
            state = state + g * (D[i - 1] - state)
            Pk = (1 - g) * Pk
            gains.append(float(g))
            errs.append(float(np.linalg.norm(state - D[i]) / (np.linalg.norm(D[i]) + 1e-12)))
            S[a:b] = S0[a:b] - state[None, :]
        ba = C.ba(yb[m:], classes[np.argmax(S[m:], 1)])
        g = np.array([x for x in gains if np.isfinite(x)])
        out[name] = dict(ba=ba, gain=float(np.mean(g)) if len(g) else np.nan,
                         frozen=float(np.mean(g < 0.01)) if len(g) else np.nan,
                         err=float(np.mean(errs)) if errs else np.nan,
                         traj=g)
    out["none"] = C.ba(yb[m:], classes[np.argmax(S0[m:], 1)])
    return out


def main():
    say("v47 Kalman audit, m=%d, source-only representations" % M)
    for ds in ("seed", "gal", "2b", "2a", "ner"):
        rows = []
        for p in pairs(ds):
            r = run(p["A"], p["ya"], p["B"], p["yb"], M)
            if r:
                rows.append(r)
        if not rows:
            continue
        say("")
        say("%s  (%d cells)" % (ds, len(rows)))
        say("  %-6s %-8s %-8s %-9s %-9s" % ("cfg", "BA", "mean K", "frozen%", "state err"))
        say("  %-6s %-8.4f %-8s %-9s %-9s" % ("none", np.mean([r["none"] for r in rows]), "-", "-", "-"))
        for k in ("k1", "k2", "k3", "k4"):
            say("  %-6s %-8.4f %-8.3f %-9.1f %-9.3f"
                % (k, np.mean([r[k]["ba"] for r in rows]),
                   np.nanmean([r[k]["gain"] for r in rows]),
                   100 * np.nanmean([r[k]["frozen"] for r in rows]),
                   np.nanmean([r[k]["err"] for r in rows])))
        # gain trajectory on the first blocks, averaged over cells
        L_ = min(10, min(len(r["k1"]["traj"]) for r in rows))
        if L_ > 1:
            say("  mean gain by block index (k1 / k2):")
            for k in ("k1", "k2"):
                tr = np.nanmean(np.array([r[k]["traj"][:L_] for r in rows]), axis=0)
                say("    %-3s %s" % (k, np.round(tr, 2)))
    print("done", P)


if __name__ == "__main__":
    main()
