# -*- coding: utf-8 -*-
"""v21: causal mean estimators, including a shrink-to-source estimator whose
shrinkage is set by the estimator's own effective sample size.

    corrected x_t = x_t - lam * mu_hat + lam * mu_A ,   lam = n_eff / (n_eff + tau)

with n_eff the effective sample size of the estimator (k for a cumulative mean,
1/alpha for an exponential one).  lam -> 0 at the start, so the correction
falls back to no correction when the estimate is unreliable; lam -> 1 as the
estimate stabilises.  Also reports the one-sided patch (x - mu_hat, no mu_A),
which is the pipeline the paper warns about.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "causal.txt")
L = []
TAU = 50.0
KS = {"2b": 20, "2a": 20, "gal": 20, "ner": 20, "seed": 50}


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


def scores(Bt, W, b, K):
    if K == 2:
        raw = (Bt @ W[1][None, :].T).ravel() + b[0]
        return np.column_stack([-raw, raw])
    return Bt @ W.T + b[None, :]


def run_cell(A, ya, Bt, yb, k):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    K = len(classes)
    W = C.linear_weights(clf, A.shape[1], K)
    b = np.asarray(clf.intercept_, float).ravel()
    muA = A.mean(0)
    n = len(yb)
    T = np.arange(k, n)
    out = {}

    def ba_of(S):
        return C.ba(yb[T], classes[np.argmax(S, 1)])

    out["none"] = ba_of(scores(Bt[T], W, b, K))
    mu_b = Bt.mean(0)
    out["batch"] = ba_of(scores(Bt[T] - mu_b + muA, W, b, K))

    cs = np.cumsum(Bt, axis=0)
    cnt = np.arange(1, n + 1)[:, None]
    mu_cum = cs / cnt                       # mean of trials 1..i
    mu_cum_prev = np.vstack([np.zeros((1, Bt.shape[1])), mu_cum[:-1]])

    # cumulative, two-sided
    out["cum"] = ba_of(scores(Bt[T] - mu_cum_prev[T] + muA, W, b, K))
    # cumulative, one-sided patch (no mu_A)
    out["cum_1s"] = ba_of(scores(Bt[T] - mu_cum_prev[T], W, b, K))

    # sliding window
    Wn = 50
    mu_win = np.array([Bt[max(0, i - Wn):i].mean(0) if i > 0 else Bt[0] for i in range(n)])
    out["win"] = ba_of(scores(Bt[T] - mu_win[T] + muA, W, b, K))

    # exponential moving average, alpha = 0.05
    al = 0.05
    mu_ema = np.zeros_like(Bt)
    m = Bt[0].copy()
    for i in range(n):
        if i > 0:
            m = (1 - al) * m + al * Bt[i - 1]
        mu_ema[i] = m
    out["ema"] = ba_of(scores(Bt[T] - mu_ema[T] + muA, W, b, K))

    # uncertainty-shrunk causal mean: lam = n_eff/(n_eff+tau), n_eff = i
    neff = np.arange(n)[:, None].astype(float)
    lam = neff / (neff + TAU)
    mu_usc = mu_cum_prev * lam
    out["usc"] = ba_of(scores(Bt[T] - mu_usc[T] + lam[T] * muA, W, b, K))

    # uncertainty-shrunk exponential
    neff_e = np.full((n, 1), 1.0 / al) * np.minimum(1.0, np.arange(n)[:, None] / 20.0)
    lam_e = neff_e / (neff_e + TAU)
    mu_usce = mu_ema * lam_e
    out["usce"] = ba_of(scores(Bt[T] - mu_usce[T] + lam_e[T] * muA, W, b, K))
    return out


def main():
    say("v21: causal estimators of the target mean, LDA, two-sided unless marked")
    say("  tau = %.0f for the shrunk estimator; window = 50; alpha = 0.05" % TAU)
    say("")
    for ds in ("2b", "2a", "gal", "ner", "seed"):
        k = KS[ds]
        rows = []
        for p in pairs(ds):
            r = run_cell(p["A"], p["ya"], p["B"], p["yb"], k)
            rows.append((p["subj"], r))
        keys = ["none", "batch", "cum", "win", "ema", "usc", "usce", "cum_1s"]
        vals = {m: np.array([r[m] for _, r in rows]) for m in keys}
        say("=" * 78)
        say("%s (k=%d, %d cells, %d subjects)" % (ds, k, len(rows), len(set(s for s, _ in rows))))
        say("=" * 78)
        say("  " + "  ".join("%-9s" % m for m in keys))
        say("  " + "  ".join("%-9.4f" % vals[m].mean() for m in keys))
        # subject-level paired differences against none
        say("  paired vs none (subject level):")
        for m in ("batch", "cum", "win", "ema", "usc", "usce", "cum_1s"):
            by = {}
            for s, r in rows:
                by.setdefault(s, []).append(r[m] - r["none"])
            d = np.array([np.mean(v) for v in by.values()])
            rs = np.random.RandomState(0)
            bs = np.array([np.mean(rs.choice(d, len(d))) for _ in range(4000)])
            say("    %-8s %+.4f  95%% CI [%+.4f, %+.4f]  %s"
                % (m, d.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5),
                   "better" if np.percentile(bs, 2.5) > 0 else
                   ("worse" if np.percentile(bs, 97.5) < 0 else "tie")))
        say("")
    print("done", P)


if __name__ == "__main__":
    main()
