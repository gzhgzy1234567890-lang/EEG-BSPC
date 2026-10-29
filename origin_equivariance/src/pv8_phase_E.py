# -*- coding: utf-8 -*-
"""v42: experiment E -- jumps that are *caused by* class-prior changes.

In SEED a new film block changes both the features and the class mixture.  B
alone (a common shift per block) is benign for a tracker; C alone (prior change
with no shift) is benign for everything.  E combines them: the block-level
change is a prior change, so a state tracker that follows block means is
following the label mix rather than a sensor offset.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pv8_phase import one, avg, SEEDS, N_TGT, M

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "phase_E.txt")
L = []
SEP = 0.25


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def prior_block(i, n, shift, period):
    """class proportions change abruptly at block boundaries of `period` blocks"""
    blk = i // (period * M)
    frac = 0.5 + (shift if blk % 2 == 0 else -shift)
    p = np.ones(4) / 4
    p[0] += (frac - 0.5)
    p[1] -= (frac - 0.5)
    p = np.clip(p, 1e-3, None)
    return p / p.sum()


def main():
    say("E. block-level class-prior changes (film blocks), no common shift")
    say("  %-24s %-7s %-7s %-7s %-7s %-7s %-7s"
        % ("setting", "none", "cum", "eq9", "loo", "kalman", "adwin"))
    for shift in (0.0, 0.2, 0.35):
        for period in (4, 8):
            def pr(i, n, s=shift, per=period):
                return prior_block(i, n, s, per)
            res = [one(s, SEP, a_rho=0.0, prior=pr) for s in SEEDS]
            m = avg(res)
            say("  shift=%-4.2f period=%-3d   %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f"
                % (shift, period, m["none"], m["cum"], m["eq9"], m["loo"],
                   m["kalman"], m["adwin"]))
    say("")
    say("E2. same, plus a constant common offset of 1 class-distance")
    say("  %-24s %-7s %-7s %-7s %-7s %-7s %-7s"
        % ("setting", "none", "cum", "eq9", "loo", "kalman", "adwin"))
    for shift in (0.0, 0.2, 0.35):
        def pr(i, n, s=shift):
            return prior_block(i, n, s, 8)
        res = [one(s, SEP, a_rho=1.0, prior=pr) for s in SEEDS]
        m = avg(res)
        say("  shift=%-4.2f period=8     %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f"
            % (shift, m["none"], m["cum"], m["eq9"], m["loo"], m["kalman"], m["adwin"]))
    print("done", P)


if __name__ == "__main__":
    main()
