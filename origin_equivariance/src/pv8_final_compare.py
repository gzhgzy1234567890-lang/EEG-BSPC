# -*- coding: utf-8 -*-
"""v39: one protocol, one table.  Every method corrects by a *displacement*
estimate in the score space of the classifier and differs only in which history
it uses and how much weight it gives:

  none    : no correction
  cum     : displacement of the running mean, per trial, weight 1
  block1  : mean of all completed blocks, weight 1
  eq9     : variance-ratio weight on the mean of completed blocks
  loo     : leave-one-block-out least-squares weight on the same mean
  fwd     : forward-predictive weight -- every term of the least-squares
            criterion predicts block b from blocks strictly *before* b:
                lam = clip( sum_{b>=2} <d_b, dbar_{<b}> / sum_{b>=2} ||dbar_{<b}>||^2 )
  adwin   : ADWIN over block displacements, weight 1
  kalman  : random-walk state over block displacements, weight 1

Fixes relative to the earlier scripts: the displacement is built from the
*features* (d_b = P W (mu_b - mu_A)), never from score means, so the intercept is
not subtracted twice; intervals are subject-level paired bootstraps.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores

P = os.path.join(C.OUT, "final_compare.txt")
L = []
M = 15
SOURCE_ONLY = ("euc", "csp", "de", "Ftime", "pow")
KEYS = ("none", "cum", "block1", "eq9", "loo", "fwd", "adwin", "kalman")


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


def boot_ci(d, reps=6000):
    d = np.asarray(d, float)
    rs = np.random.RandomState(0)
    bs = np.array([np.mean(rs.choice(d, len(d))) for _ in range(reps)])
    return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def adwin_starts(bm, delta=0.002):
    starts = [0]
    for i in range(len(bm)):
        starts.append(starts[-1])
        lo = starts[-1]
        n = i + 1 - lo
        if n < 4:
            continue
        arr = np.array(bm[lo:i + 1])
        for cut in range(1, n):
            if cut < 2 or n - cut < 2:
                continue
            diff = np.linalg.norm(arr[cut:].mean(0) - arr[:cut].mean(0))
            eps = 3.0 * np.sqrt(np.log(4.0 / delta) / (2.0 * min(cut, n - cut)))
            if diff > eps:
                starts[-1] = lo + cut
                break
    return starts[1:]


def run_one(A, ya, Bt, yb, m):
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
    d_b = [F @ (W @ (Bt[a:b].mean(0) - muA)) for a, b in blocks]

    # per-trial running displacement for `cum`
    cum_feat = np.cumsum(Bt, axis=0) / np.arange(1, n + 1)[:, None]
    cum_prev = np.vstack([np.zeros((1, Bt.shape[1])), cum_feat[:-1]])
    d_cum = (cum_prev - muA[None, :]) @ W.T @ F.T

    S = {k: S0.copy() for k in KEYS}
    S["cum"] = S0 - d_cum

    starts = adwin_starts(d_b)
    state = np.zeros(K)
    Pk = 1.0
    lam_hist = {k: [] for k in ("eq9", "loo", "fwd")}
    for i, (a, hi) in enumerate(blocks):
        if i == 0:
            continue
        D = np.array(d_b[:i])                     # blocks strictly before i
        dbar = D.mean(0)
        # eq9
        if len(D) >= 2:
            noise = K * float(D.var(0, ddof=1).sum()) / len(D)
        else:
            Y = Bt[a - m:a] @ (F @ W).T
            noise = K * float(np.sum((Y - Y.mean(0)) ** 2) / (m * m))
        l_eq = float(np.clip((dbar @ dbar) / (dbar @ dbar + noise + 1e-12), 0, 1))
        # loo
        if len(D) >= 3:
            num = den = 0.0
            for j in range(len(D)):
                o = np.delete(D, j, axis=0).mean(0)
                num += float(D[j] @ o)
                den += float(o @ o)
            l_loo = float(np.clip(num / den, 0, 1)) if den > 1e-15 else 0.0
        else:
            l_loo = len(D) / (len(D) + 3.0)
        # forward-predictive
        if len(D) >= 2:
            num = den = 0.0
            for j in range(1, len(D)):
                past = D[:j].mean(0)
                num += float(D[j] @ past)
                den += float(past @ past)
            l_fwd = float(np.clip(num / den, 0, 1)) if den > 1e-15 else 0.0
        else:
            l_fwd = 1.0 / 4.0
        S["block1"][a:hi] = S0[a:hi] - dbar[None, :]
        S["eq9"][a:hi] = S0[a:hi] - l_eq * dbar[None, :]
        S["loo"][a:hi] = S0[a:hi] - l_loo * dbar[None, :]
        S["fwd"][a:hi] = S0[a:hi] - l_fwd * dbar[None, :]
        lo = starts[i - 1] if i - 1 < len(starts) else 0
        S["adwin"][a:hi] = S0[a:hi] - np.mean(d_b[lo:i], axis=0)[None, :]
        # kalman over the same displacement sequence
        q = 0.0
        if i >= 2:
            q = float(np.diff(D, axis=0).var(0).sum()) / 2.0
        r = noise if len(D) >= 2 else noise
        Pk += q
        g = Pk / (Pk + max(r, 1e-12))
        state = state + g * (D[-1] - state)
        Pk = (1 - g) * Pk
        S["kalman"][a:hi] = S0[a:hi] - state[None, :]
        lam_hist["eq9"].append(l_eq)
        lam_hist["loo"].append(l_loo)
        lam_hist["fwd"].append(l_fwd)

    lo = m
    out = {}
    for k in KEYS:
        out[k] = C.ba(yb[lo:], classes[np.argmax(S[k][lo:], 1)])
    out["_lam"] = {k: float(np.mean(v)) if v else np.nan for k, v in lam_hist.items()}
    return out


def main():
    say("v39: single protocol, m = %d, subject-level paired bootstraps" % M)
    for ds in ("gal", "seed", "2b", "2a", "ner"):
        rows = []
        for p in pairs(ds):
            r = run_one(p["A"], p["ya"], p["B"], p["yb"], M)
            if r:
                rows.append((p["subj"], r))
        if not rows:
            continue
        say("")
        say("=" * 96)
        say("%s   %d cells, %d subjects" % (ds, len(rows), len(set(s for s, _ in rows))))
        say("=" * 96)
        say("  " + " ".join("%-7s" % k for k in KEYS))
        say("  " + " ".join("%-7.4f" % np.mean([r[k] for _, r in rows]) for k in KEYS))
        lams = {k: np.nanmean([r["_lam"][k] for _, r in rows]) for k in ("eq9", "loo", "fwd")}
        say("  mean lambda: eq9 %.2f  loo %.2f  fwd %.2f" % (lams["eq9"], lams["loo"], lams["fwd"]))
        say("")
        for target in ("eq9", "loo", "fwd"):
            for base in ("none", "eq9", "block1"):
                if target == base:
                    continue
                by = {}
                for s, r in rows:
                    by.setdefault(s, []).append(r[target] - r[base])
                d = {s: np.mean(v) for s, v in by.items()}
                mu = float(np.mean(list(d.values())))
                lo_, hi_ = boot_ci(list(d.values()))
                say("    %-5s - %-6s  %+.4f  [%+.4f, %+.4f]  %s"
                    % (target, base, mu, lo_, hi_,
                       "better" if lo_ > 0 else ("worse" if hi_ < 0 else "tie")))
        say("")
    print("done", P)


if __name__ == "__main__":
    main()
