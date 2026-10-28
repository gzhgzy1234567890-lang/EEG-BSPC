# -*- coding: utf-8 -*-
"""v32: a class-balanced observation of the offset, and a reliability weight
for how much of it to apply.

Observation.  A block mean of the scores mixes the session offset with the
class proportions of that block.  Estimating the offset *within each predicted
class* and averaging over classes removes the mixture:

    zhat_b = (1/K) sum_k mean{ s_i : argmax s_i = k, i in block b } .      (15)

Weight.  The offset is worth applying in proportion to how reliable it is
relative to its own sampling error across blocks:

    lambda = ||zbar||^2 / ( ||zbar||^2 + K * var_b(zhat_b) / B ) ,        (16)

the fraction of the estimated displacement that is signal rather than noise.
lambda -> 0 when the blocks disagree (drift), lambda -> 1 when they agree.
"""
import glob
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores, TAU

P = os.path.join(C.OUT, "reliability.txt")
L = []
CACHE4 = r"G:\Work_work\math\EEG\local_analysis\cache_seed4_iv"
K0 = {"2b": 20, "2a": 20, "gal": 20, "ner": 20, "seed": 50}
M = 25
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


def balanced_obs(S, K):
    pred = S.argmax(1)
    vecs = [S[pred == k].mean(0) for k in range(K) if np.any(pred == k)]
    if not vecs:
        return S.mean(0)
    return np.mean(vecs, axis=0)


def run(A, ya, Bt, yb, k0):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    K = len(classes)
    W = C.linear_weights(clf, A.shape[1], K)
    muA = A.mean(0)
    zA = W @ muA
    n = len(yb)
    S0 = scores(Bt, W, np.asarray(clf.intercept_, float).ravel(), K)
    cs = np.cumsum(Bt, axis=0)
    cnt = np.arange(1, n + 1)[:, None]
    mu_prev = np.vstack([np.zeros((1, Bt.shape[1])), (cs / cnt)[:-1]])

    blocks = [(t, min(t + M, n)) for t in range(k0, n, M)]
    zhat = [balanced_obs(S0[a:b], K) for a, b in blocks]

    S = S0.copy()
    for i, (a, b) in enumerate(blocks):
        if i == 0:
            continue
        Z = np.array(zhat[:i])
        zbar = Z.mean(0)
        if len(Z) >= 2:
            vb = Z.var(0).sum()
            lam = float(np.clip((zbar @ zbar) / (zbar @ zbar + K * vb / len(Z) + 1e-12), 0, 1))
        else:
            lam = 0.5
        S[a:b] = S0[a:b] - lam * zbar[None, :] + lam * zA[None, :]

    out = {}
    out["none"] = C.ba(yb[k0:], classes[np.argmax(S0[k0:], 1)])
    out["cum"] = C.ba(yb[k0:], classes[np.argmax((S0 - mu_prev @ W.T + (W @ muA)[None, :])[k0:], 1)])
    neff = np.arange(n)[:, None].astype(float)
    lt = neff / (neff + TAU)
    out["shrunk"] = C.ba(yb[k0:], classes[np.argmax((S0 - lt * mu_prev @ W.T + lt * (W @ muA)[None, :])[k0:], 1)])
    # balanced observation with full weight (does the observation fix the noise?)
    S2 = S0.copy()
    for i, (a, b) in enumerate(blocks):
        if i == 0:
            continue
        zbar = np.array(zhat[:i]).mean(0)
        S2[a:b] = S0[a:b] - zbar[None, :] + zA[None, :]
    out["balanced"] = C.ba(yb[k0:], classes[np.argmax(S2[k0:], 1)])
    out["rel"] = C.ba(yb[k0:], classes[np.argmax(S[k0:], 1)])
    return out


def report(ds, rows, tag):
    keys = ["none", "cum", "shrunk", "balanced", "rel"]
    say("%-8s %-5s " % (tag, ds) + " ".join("%-9s" % k for k in keys))
    say("%-8s %-5s " % ("", "") + " ".join("%-9.4f" % np.mean([r[k] for r in rows]) for k in keys))
    for k in ("balanced", "rel"):
        d = np.array([r[k] - r["none"] for r in rows])
        m, lo, hi = ci(d)
        say("    %-8s vs none %+.4f [%+.4f, %+.4f]  %s" % (k, m, lo, hi,
            "better" if lo > 0 else ("worse" if hi < 0 else "tie")))


def main():
    say("v32: class-balanced offset observation (15) and reliability weight (16)")
    say("")
    for ds in ("2b", "2a", "seed", "gal", "ner"):
        rows = [run(p["A"], p["ya"], p["B"], p["yb"], K0[ds]) for p in pairs(ds)]
        report(ds, rows, "dev")
    subs = sorted(set(int(os.path.basename(f).split("_")[0])
                      for f in glob.glob(os.path.join(CACHE4, "*.npz"))))
    rows = []
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
                    rows.append(run(S[i][0], S[i][1], S[j][0], S[j][1], 50))
    say("")
    report("seed4", rows, "heldout")
    print("done", P)


if __name__ == "__main__":
    main()
