# -*- coding: utf-8 -*-
"""v25: a direction-consistency gate.

For each block of m trials, take the displacement that would bring that block's
mean back to the source mean, in score space:
    d_b = P W (mu_b - mu_A)  in R^K .
If a session's blocks all need the *same* displacement, the session carries a
stable offset and the correction is safe; if the directions rotate, the mean is
drifting and a single estimate is stale.  The weight is the mean cosine between
the block displacements and their own mean direction, clipped to [0, 1]:
    kappa_t = mean_b cos(d_b, dbar) ,   lambda_t = clip((kappa_t - 0.5)/0.5, 0, 1): chance-level agreement means no correction .
No target labels are used.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores, TAU

P = os.path.join(C.OUT, "dirgate.txt")
L = []
K0 = {"2b": 20, "2a": 20, "gal": 20, "ner": 20, "seed": 50}
MB = 25


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


def kappa(Bt, W, P, muA, m, upto):
    k = upto // m
    if k < 2:
        return np.nan
    B = Bt[:k * m].reshape(k, m, -1).mean(1)          # k x D block means
    D = (B - muA[None, :]) @ W.T                       # k x K
    D = D @ P.T                                        # centre across classes
    nrm = np.linalg.norm(D, axis=1)
    ok = nrm > 1e-12
    if ok.sum() < 2:
        return np.nan
    U = D[ok] / nrm[ok, None]
    ref = U.mean(0)
    rn = np.linalg.norm(ref)
    if rn < 1e-12:
        return 0.0
    return float(np.mean(U @ (ref / rn)))


def run(A, ya, Bt, yb, k0):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    K = len(classes)
    W = C.linear_weights(clf, A.shape[1], K)
    P = np.eye(K) - np.ones((K, K)) / K
    muA = A.mean(0)
    n = len(yb)
    S0 = scores(Bt, W, np.asarray(clf.intercept_, float).ravel(), K)
    cs = np.cumsum(Bt, axis=0)
    cnt = np.arange(1, n + 1)[:, None]
    mu_prev = np.vstack([np.zeros((1, Bt.shape[1])), (cs / cnt)[:-1]])

    lam = np.ones(n)
    ks = []
    t = k0
    while t < n:
        kv = kappa(Bt, W, P, muA, MB, t)
        if not np.isfinite(kv):
            kv = 0.5
        ks.append(kv)
        lam[t:min(t + MB, n)] = float(np.clip((kv - 0.5) / 0.5, 0.0, 1.0))
        t += MB

    def ba(S):
        return C.ba(yb[k0:], classes[np.argmax(S[k0:], 1)])

    out = {}
    out["none"] = ba(S0)
    out["cum"] = ba(S0 - mu_prev @ W.T + (W @ muA)[None, :])
    neff = np.arange(n)[:, None].astype(float)
    lt = neff / (neff + TAU)
    out["shrunk"] = ba(S0 - lt * mu_prev @ W.T + lt * (W @ muA)[None, :])
    out["dirgate"] = ba(S0 - lam[:, None] * mu_prev @ W.T + lam[:, None] * (W @ muA)[None, :])
    best = -1
    for l in np.linspace(0, 1, 11):
        best = max(best, ba(S0 - l * mu_prev @ W.T + l * (W @ muA)[None, :]))
    out["oracle"] = best
    out["kappa"] = float(np.mean(ks)) if ks else np.nan
    return out


def main():
    say("v25: direction-consistency gate, lambda = mean cos(d_b, dbar)")
    say("")
    for ds in ("2b", "2a", "seed", "gal", "ner"):
        k0 = K0[ds]
        rows = [run(p["A"], p["ya"], p["B"], p["yb"], k0) for p in pairs(ds)]
        keys = ["none", "cum", "shrunk", "dirgate", "oracle"]
        say("=" * 72)
        say("%s  (k0=%d, %d cells)  mean kappa = %+.2f"
            % (ds, k0, len(rows), np.nanmean([r["kappa"] for r in rows])))
        say("=" * 72)
        say("  " + " ".join("%-9s" % k for k in keys))
        say("  " + " ".join("%-9.4f" % np.mean([r[k] for r in rows]) for k in keys))
        say("")
    print("done", P)


if __name__ == "__main__":
    main()
