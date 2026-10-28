# -*- coding: utf-8 -*-
"""v23: a label-free gate that decides per block whether to correct, plus the
fixed-lambda and oracle-lambda baselines the referee asked for.

Gate: at the end of each block of m trials, compare the top-1 margin
distribution of the corrected scores with that of the source session, and the
same for the uncorrected scores; apply the correction in the next block only if
its margin distribution is closer to the source's.  Labels are never used.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores, TAU

P = os.path.join(C.OUT, "gate.txt")
L = []
K0 = {"2b": 20, "2a": 20, "gal": 20, "ner": 20, "seed": 50}
M = 25


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


def top1(S):
    s = np.sort(S, axis=1)
    return s[:, -1] - s[:, -2] if S.shape[1] > 1 else np.abs(s[:, -1])


def run(A, ya, Bt, yb, kind, k0):
    clf = C.make(kind).fit(A, ya)
    classes = np.asarray(clf.classes_)
    K = len(classes)
    W = C.linear_weights(clf, A.shape[1], K)
    muA = A.mean(0)
    n = len(yb)
    S0 = scores(Bt, W, np.asarray(clf.intercept_, float).ravel(), K)
    ms = top1(S0[:len(A)])
    m0, s0 = ms.mean(), ms.std() + 1e-9
    cs = np.cumsum(Bt, axis=0)
    cnt = np.arange(1, n + 1)[:, None]
    mu_cum = cs / cnt
    mu_prev = np.vstack([np.zeros((1, Bt.shape[1])), mu_cum[:-1]])
    corr = S0 - mu_prev @ W.T + (W @ muA)[None, :]
    unc = S0
    # fixed lambda
    out = {}
    for lam in (0.0, 0.25, 0.5, 0.75, 1.0):
        S = S0 - lam * mu_prev @ W.T + lam * (W @ muA)[None, :]
        out["lam%.2f" % lam] = C.ba(yb[k0:], classes[np.argmax(S[k0:], 1)])
    # shrunk
    neff = np.arange(n)[:, None].astype(float)
    lam_t = neff / (neff + TAU)
    S = S0 - lam_t * mu_prev @ W.T + lam_t * (W @ muA)[None, :]
    out["shrunk"] = C.ba(yb[k0:], classes[np.argmax(S[k0:], 1)])
    # gated: decide per block
    use = np.ones(n, dtype=bool)
    state = True
    t = k0
    while t < n:
        if state:
            S = corr
        else:
            S = unc
        bt = slice(t, min(t + M, n))
        mc = top1(S[bt]).mean()
        dc = abs(mc - m0) / s0
        mu_ = top1(unc[bt]).mean()
        du = abs(mu_ - m0) / s0
        state = dc < du
        use[t:min(t + M, n)] = state
        t += M
    S = np.where(use[:, None], corr, unc)
    out["gate"] = C.ba(yb[k0:], classes[np.argmax(S[k0:], 1)])
    out["none"] = C.ba(yb[k0:], classes[np.argmax(unc[k0:], 1)])
    # oracle lambda per cell (offline only)
    best = -1
    for lam in np.linspace(0, 1, 11):
        S = S0 - lam * mu_prev @ W.T + lam * (W @ muA)[None, :]
        best = max(best, C.ba(yb[k0:], classes[np.argmax(S[k0:], 1)]))
    out["oracle"] = best
    return out


def main():
    say("v23: a label-free gate, fixed-lambda baselines and the oracle")
    say("  gate: apply the correction in a block only if the corrected margin")
    say("  distribution is closer to the source's than the uncorrected one")
    say("")
    for kind in ("lda", "logit"):
        for ds in ("2b", "2a", "seed", "gal", "ner"):
            if kind == "logit" and ds not in ("2b", "gal"):
                continue
            k0 = K0[ds]
            rows = []
            for p in pairs(ds):
                rows.append(run(p["A"], p["ya"], p["B"], p["yb"], kind, k0))
            keys = ["none", "lam0.25", "lam0.50", "lam0.75", "lam1.00", "shrunk", "gate", "oracle"]
            say("=" * 84)
            say("%s / %s  (k0=%d, %d cells)" % (ds, kind, k0, len(rows)))
            say("=" * 84)
            say("  " + " ".join("%-8s" % k for k in keys))
            say("  " + " ".join("%-8.4f" % np.mean([r[k] for r in rows]) for k in keys))
            say("")
    print("done", P)


if __name__ == "__main__":
    main()
