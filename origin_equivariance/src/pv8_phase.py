# -*- coding: utf-8 -*-
"""v41: synthetic phase diagram, with shifts measured in *score* standard
deviations so that the axes mean the same thing on every grid point.

Calibration chooses the class separation so that the uncorrected target scores
about 0.68 balanced accuracy; without that the task is trivially separable and
no correction can matter (which is what v40 showed: BA = 1.000 everywhere).

  A  constant offset a (score sd) x drift per session v (score sd)
  B  jump amplitude x jump period
  C  prior shift only
  D  direction of the offset relative to the discriminant subspace
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_final_compare import run_one

P = os.path.join(C.OUT, "phase2.txt")
L = []
D_DIM = 40
K = 4
SEEDS = (0, 1, 2, 3, 4)
M = 15
N_TGT = 600
N_SRC = 1000


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def means_for(seed, sep):
    return np.random.RandomState(seed).randn(K, D_DIM) * sep


def subs(means):
    Mc = means - means.mean(0, keepdims=True)
    _, _, Vt = np.linalg.svd(Mc)
    return Vt[:K - 1].T, Vt[K - 1:].T


def gen(means, rng, n, off, prior=None):
    if prior is None:
        y = rng.randint(0, K, n)
    else:
        y = np.array([rng.choice(K, p=prior(i, n)) for i in range(n)])
    return means[y] + rng.randn(n, D_DIM) + off, y


def one(seed, sep, a_rho=0.0, v_rho=0.0, jumps_rho=(), jump_period=0,
        prior=None, theta_deg=0.0):
    rng = np.random.RandomState(seed * 977 + 13)
    means = means_for(seed, sep)
    par, perp = subs(means)
    up = par @ rng.randn(par.shape[1])
    up /= np.linalg.norm(up)
    uq = perp @ rng.randn(perp.shape[1])
    uq /= np.linalg.norm(uq)
    th = np.deg2rad(theta_deg)
    u = np.cos(th) * up + np.sin(th) * uq

    Xs, ys = gen(means, rng, N_SRC, np.zeros(D_DIM))
    # unit of offset: the mean pairwise distance between the class means, so the
    # axes mean the same on every grid point and an offset orthogonal to the
    # discriminant really has no effect on the scores
    dcls = float(np.mean([np.linalg.norm(means[i] - means[j])
                          for i in range(K) for j in range(i + 1, K)]))
    scale = dcls

    off = np.zeros((N_TGT, D_DIM))
    if a_rho:
        off += (a_rho * scale * u)[None, :]
    if v_rho:
        ramp = np.linspace(0.0, 1.0, N_TGT)[:, None]
        off += ramp * (v_rho * scale * u)[None, :]
    for k in jumps_rho:
        st = min(k * jump_period * M, N_TGT - 1)
        off[st:] += (k * scale * u)[None, :]

    Xt, yt = gen(means, rng, N_TGT, off, prior)
    return run_one(Xs, ys, Xt, yt, M)


def avg(res):
    keys = ("none", "cum", "block1", "eq9", "loo", "fwd", "adwin", "kalman")
    return {k: float(np.mean([r[k] for r in res])) for k in keys}


def calibrate():
    best = None
    for sep in (0.15, 0.2, 0.25, 0.3, 0.35, 0.45):
        res = [one(s, sep, a_rho=0.0) for s in SEEDS[:3]]
        ba = np.mean([r["none"] for r in res])
        say("  sep=%.2f -> none BA %.3f" % (sep, ba))
        if best is None or abs(ba - 0.68) < abs(best[1] - 0.68):
            best = (sep, ba)
    return best[0]


def main():
    say("v41 phase diagram; shifts in units of the score sd")
    say("")
    say("calibration (target 0.68):")
    sep = calibrate()
    say("  chosen sep = %.2f" % sep)
    say("")

    say("A. constant offset x total drift (score sd)")
    say("  %-16s %-7s %-7s %-7s %-7s %-7s %-7s %-7s %-9s"
        % ("setting", "none", "cum", "eq9", "loo", "fwd", "kalman", "adwin", "loo-eq9"))
    for a_rho in (0.0, 0.25, 0.5, 1.0):
        for v_rho in (0.0, 0.25, 0.5, 1.0, 2.0):
            m = avg([one(s, sep, a_rho=a_rho, v_rho=v_rho) for s in SEEDS])
            say("  a=%.1f v=%.1f      %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %+.4f"
                % (a_rho, v_rho, m["none"], m["cum"], m["eq9"], m["loo"], m["fwd"],
                   m["kalman"], m["adwin"], m["loo"] - m["eq9"]))

    say("")
    say("B. jumps (amplitude in score sd, period in blocks), no drift, a = 1")
    say("  %-16s %-7s %-7s %-7s %-7s %-7s %-7s %-7s %-9s"
        % ("setting", "none", "cum", "eq9", "loo", "fwd", "kalman", "adwin", "loo-eq9"))
    for amp in (0.25, 0.5, 1.0):
        for period in (2, 4, 8):
            jumps = tuple(range(1, (N_TGT // M) // period + 1))
            m = avg([one(s, sep, a_rho=1.0, jumps_rho=jumps, jump_period=period)
                     for s in SEEDS])
            say("  amp=%.1f every %d   %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %+.4f"
                % (amp, period, m["none"], m["cum"], m["eq9"], m["loo"], m["fwd"],
                   m["kalman"], m["adwin"], m["loo"] - m["eq9"]))

    say("")
    say("C. prior shift only (no offset, no drift)")
    say("  %-16s %-7s %-7s %-7s %-7s %-7s %-7s %-7s %-9s"
        % ("setting", "none", "cum", "eq9", "loo", "fwd", "kalman", "adwin", "loo-eq9"))
    for sh in (0.0, 0.2, 0.4):
        def prior(i, n, s=sh):
            frac = i / max(n - 1, 1) - 0.5
            p = np.ones(K) / K
            p[0] += s * frac
            p[1] -= s * frac
            p = np.clip(p, 1e-3, None)
            return p / p.sum()
        m = avg([one(s, sep, a_rho=0.0, prior=prior) for s in SEEDS])
        say("  shift=%.1f        %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %+.4f"
            % (sh, m["none"], m["cum"], m["eq9"], m["loo"], m["fwd"],
               m["kalman"], m["adwin"], m["loo"] - m["eq9"]))

    say("")
    say("D. direction of a = 2 offset")
    say("  %-16s %-7s %-7s %-7s %-7s %-7s %-7s %-7s"
        % ("setting", "none", "cum", "eq9", "loo", "fwd", "kalman", "adwin"))
    for th in (0, 45, 90):
        m = avg([one(s, sep, a_rho=2.0, theta_deg=th) for s in SEEDS])
        say("  theta=%d deg      %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f %-7.4f"
            % (th, m["none"], m["cum"], m["eq9"], m["loo"], m["fwd"], m["kalman"], m["adwin"]))
    print("done", P)


if __name__ == "__main__":
    main()
