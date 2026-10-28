# -*- coding: utf-8 -*-
"""v50: correction strength versus adaptive timing.

Every method corrects by the same displacement (the mean of the completed
blocks) and differs only in the weight it puts on it:

  fixed lam in {0, .1, .25, .5, .75, 1}   a constant weight, the same on every block
  eq9      the variance-ratio weight
  loo      the leave-one-block-out predictive weight
  fwd      the forward-predictive weight
  matched  a constant equal to the cell's own mean loo weight -- same magnitude,
           no timing
  shuffled loo's weights permuted across the blocks of the cell -- same
           distribution, no timing (post-hoc diagnostic, not deployable)

If `matched` or `shuffled` does as well as `loo`, the timing carries no
information and only the magnitude matters.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores

P = os.path.join(C.OUT, "lambda_control.txt")
L = []
M = 15
SOURCE_ONLY = ("euc", "csp", "de", "Ftime", "pow")
LAMS = (0.0, 0.1, 0.25, 0.5, 0.75, 1.0)


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


def ci(v, reps=6000):
    v = np.asarray(v, float)
    rs = np.random.RandomState(0)
    bs = np.array([np.mean(rs.choice(v, len(v))) for _ in range(reps)])
    return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def run(A, ya, Bt, yb, m, seed=0):
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
    D = [F @ (W @ (Bt[a:b].mean(0) - muA)) for a, b in blocks]

    lam_eq, lam_loo, lam_fwd = [], [], []
    for i in range(len(blocks)):
        if i == 0:
            lam_eq.append(0.0)
            lam_loo.append(0.0)
            lam_fwd.append(1.0 / 4.0)
            continue
        H = np.array(D[:i])
        dbar = H.mean(0)
        if len(H) >= 2:
            noise = K * float(H.var(0, ddof=1).sum()) / len(H)
        else:
            Y = Bt[blocks[i][0] - m:blocks[i][0]] @ (F @ W).T
            noise = float(np.sum((Y - Y.mean(0)) ** 2) / (m * m))
        lam_eq.append(float(np.clip((dbar @ dbar) / (dbar @ dbar + noise + 1e-12), 0, 1)))
        if len(H) >= 3:
            num = den = 0.0
            for j in range(len(H)):
                o = np.delete(H, j, axis=0).mean(0)
                num += float(H[j] @ o)
                den += float(o @ o)
            lam_loo.append(float(np.clip(num / den, 0, 1)) if den > 1e-15 else 0.0)
        else:
            lam_loo.append(len(H) / (len(H) + 3.0))
        if len(H) >= 2:
            num = den = 0.0
            for j in range(1, len(H)):
                past = H[:j].mean(0)
                num += float(H[j] @ past)
                den += float(past @ past)
            lam_fwd.append(float(np.clip(num / den, 0, 1)) if den > 1e-15 else 0.0)
        else:
            lam_fwd.append(0.25)

    lam_loo = np.array(lam_loo)
    lam_eq = np.array(lam_eq)
    lam_fwd = np.array(lam_fwd)
    mean_loo = float(np.mean(lam_loo[1:])) if len(lam_loo) > 1 else 0.0
    rng = np.random.RandomState(seed + 17)
    lam_sh = lam_loo[1:].copy()
    rng.shuffle(lam_sh)
    lam_sh = np.concatenate([[lam_loo[0]], lam_sh])

    out = {}
    # fixed weights
    for lam in LAMS:
        S = S0.copy()
        for i, (a, b) in enumerate(blocks):
            if i == 0:
                continue
            S[a:b] = S0[a:b] - lam * np.array(D[:i]).mean(0)[None, :]
        out["fix%.2f" % lam] = C.ba(yb[m:], classes[np.argmax(S[m:], 1)])
    # dynamic and controls
    for name, lam in (("eq9", lam_eq), ("loo", lam_loo), ("fwd", lam_fwd),
                      ("matched", np.full(len(blocks), mean_loo)),
                      ("shuffled", lam_sh)):
        S = S0.copy()
        for i, (a, b) in enumerate(blocks):
            if i == 0:
                continue
            S[a:b] = S0[a:b] - lam[i] * np.array(D[:i]).mean(0)[None, :]
        out[name] = C.ba(yb[m:], classes[np.argmax(S[m:], 1)])
    out["_mean_loo"] = mean_loo
    return out


def main():
    say("v50: correction strength vs adaptive timing, m=%d, source-only" % M)
    for ds in ("gal", "seed", "2b", "2a", "ner"):
        rows = []
        for p in pairs(ds):
            r = run(p["A"], p["ya"], p["B"], p["yb"], M)
            if r:
                rows.append((p["subj"], r))
        if not rows:
            continue
        keys = ["fix0.00", "fix0.10", "fix0.25", "fix0.50", "fix0.75", "fix1.00",
                "eq9", "loo", "fwd", "matched", "shuffled"]
        say("")
        say("=" * 100)
        say("%s  (%d cells, %d subjects)  mean loo weight %.2f"
            % (ds, len(rows), len(set(s for s, _ in rows)),
               np.mean([r["_mean_loo"] for _, r in rows])))
        say("=" * 100)
        say("  " + " ".join("%-8s" % k for k in keys))
        say("  " + " ".join("%-8.4f" % np.mean([r[k] for _, r in rows]) for k in keys))
        say("")
        for a, b in (("loo", "matched"), ("loo", "shuffled"), ("loo", "fix0.25"),
                     ("matched", "fix0.25"), ("loo", "eq9")):
            by = {}
            for s, r in rows:
                by.setdefault(s, []).append(r[a] - r[b])
            d = {s: np.mean(v) for s, v in by.items()}
            lo, hi = ci(list(d.values()))
            mu = float(np.mean(list(d.values())))
            say("    %-8s - %-8s %+.4f [%+.4f, %+.4f]  %s"
                % (a, b, mu, lo, hi, "better" if lo > 0 else ("worse" if hi < 0 else "tie")))
    print("done", P)


if __name__ == "__main__":
    main()
