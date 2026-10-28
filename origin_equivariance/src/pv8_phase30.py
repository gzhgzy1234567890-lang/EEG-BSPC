# -*- coding: utf-8 -*-
"""v49: 30 paired seeds per cell, with the four statistics the referee asked for.

For each cell of the synthetic grid the same 30 seeds are used for every method,
so the comparisons are paired.  Reported per cell:

    mean BA of none / cumulative / eq9 / predictive / Kalman / ADWIN
    loo - eq9     mean and 95% bootstrap CI over seeds
    loo - none    mean and 95% bootstrap CI
    P(BA < BA_none) and P(BA < BA_none - 0.01)   negative-transfer probability
    10th percentile of (method - none)           worst-case tail

Kalman is kept in the table but flagged: its implementation did not pass the
audit of Section 4.12.1, so it is not used as evidence.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pv8_phase import one

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "phase30.txt")
L = []
SEEDS = tuple(range(30))
SEP = 0.25


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def ci(v, reps=4000):
    v = np.asarray(v, float)
    rs = np.random.RandomState(0)
    bs = np.array([np.mean(rs.choice(v, len(v))) for _ in range(reps)])
    return float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def cell_stats(res, name):
    keys = ("none", "cum", "eq9", "loo", "fwd", "adwin", "kalman")
    arr = {k: np.array([r[k] for r in res]) for k in keys}
    d_eq = arr["loo"] - arr["eq9"]
    d_none = arr["loo"] - arr["none"]
    lo1, hi1 = ci(d_eq)
    lo2, hi2 = ci(d_none)
    pneg_loo = float(np.mean(arr["loo"] < arr["none"]))
    pneg_eq = float(np.mean(arr["eq9"] < arr["none"]))
    pneg_kal = float(np.mean(arr["kalman"] < arr["none"]))
    tail = {k: float(np.percentile(arr[k] - arr["none"], 10)) for k in ("eq9", "loo")}
    say("  %-22s %-7.3f %-7.3f %-7.3f %-7.3f %-7.3f %-7.3f | %+.3f [%+.3f,%+.3f] | %+.3f [%+.3f,%+.3f] | %.2f %.2f %.2f | %+.3f %+.3f"
        % (name, arr["none"].mean(), arr["cum"].mean(), arr["eq9"].mean(),
           arr["loo"].mean(), arr["fwd"].mean(), arr["adwin"].mean(),
           d_eq.mean(), lo1, hi1, d_none.mean(), lo2, hi2,
           pneg_loo, pneg_eq, pneg_kal, tail["eq9"], tail["loo"]))
    return dict(eq=float(d_eq.mean()), lo=lo1, hi=hi1, pneg=pneg_loo, tail=tail["loo"])


def main():
    say("v49: 30 paired seeds per cell; sep=%.2f" % SEP)
    say("  %-22s %-7s %-7s %-7s %-7s %-7s %-7s | %-19s | %-19s | %-13s | %-13s"
        % ("cell", "none", "cum", "eq9", "loo", "fwd", "adwin",
           "loo-eq9 [95% CI]", "loo-none [95% CI]", "Pneg loo/eq9/kal", "tail10 eq9/loo"))
    out = []
    for a_rho in (0.0, 0.5, 1.0):
        for v_rho in (0.0, 0.5, 1.0, 2.0):
            res = [one(s, SEP, a_rho=a_rho, v_rho=v_rho) for s in SEEDS]
            out.append(cell_stats(res, "a=%.1f v=%.1f" % (a_rho, v_rho)))

    say("")
    say("B. step changes (a = 1)")
    for period in (4, 8):
        jumps = tuple(range(1, (600 // 15) // period + 1))
        res = [one(s, SEP, a_rho=1.0, jumps_rho=jumps, jump_period=period) for s in SEEDS]
        out.append(cell_stats(res, "jumps every %d" % period))

    say("")
    say("C. class priors only")
    for sh in (0.2, 0.4):
        def prior(i, n, s=sh):
            frac = i / max(n - 1, 1) - 0.5
            p = np.ones(4) / 4
            p[0] += s * frac
            p[1] -= s * frac
            p = np.clip(p, 1e-3, None)
            return p / p.sum()
        res = [one(s, SEP, a_rho=0.0, prior=prior) for s in SEEDS]
        out.append(cell_stats(res, "priors %.1f" % sh))

    say("")
    say("E. block-level priors (period 8) with and without an offset")
    for a_rho in (0.0, 1.0):
        def prior(i, n, per=8):
            blk = i // (per * 15)
            frac = 0.5 + (0.35 if blk % 2 == 0 else -0.35)
            p = np.ones(4) / 4
            p[0] += (frac - 0.5)
            p[1] -= (frac - 0.5)
            p = np.clip(p, 1e-3, None)
            return p / p.sum()
        res = [one(s, SEP, a_rho=a_rho, prior=prior) for s in SEEDS]
        out.append(cell_stats(res, "blk priors a=%.1f" % a_rho))

    say("")
    n_pos = sum(1 for o in out if o["lo"] > 0)
    n_neg = sum(1 for o in out if o["hi"] < 0)
    n_tie = len(out) - n_pos - n_neg
    say("summary over %d cells: loo-eq9 CI entirely >0 in %d, entirely <0 in %d, straddling 0 in %d"
        % (len(out), n_pos, n_neg, n_tie))
    say("median loo-eq9 %+.4f ; median tail10(loo) %+.4f"
        % (float(np.median([o["eq"] for o in out])),
           float(np.median([o["tail"] for o in out]))))
    print("done", P)


if __name__ == "__main__":
    main()
