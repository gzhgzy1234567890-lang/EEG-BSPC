# -*- coding: utf-8 -*-
"""v8 screen analysis with the two statistics kept apart.

There are two different questions and they need two different statistics.

  z_T = || mu_S || / || sd_S ||     distance of the feature origin from the
                                    data centre of the source session.  It says
                                    whether a *one-sided* pipeline is exposed,
                                    and it is computable before any target data.
  t   = || W (mu_T - mu_S) || / sd(score)   the displacement induced by the
                                    cross-session offset.  It says how much the
                                    *two-sided* correction has to repair, and it
                                    needs the target features but no labels.

Output: results/screen.txt
"""
import os
import sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "screen.txt")
L = []
DS = ("2a", "2b", "seed", "ner", "gal")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    rows = []
    for ds in DS:
        ps = C.all_pairs((ds,))
        if ds == "gal":
            ps = [p for p in ps
                  if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        for p in ps:
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            muA, muB = A.mean(0), Bt.mean(0)
            sdA = np.maximum(A.std(0), 1e-12)
            z_org = float(np.linalg.norm(muA) / np.linalg.norm(sdA))
            W = C.linear_weights(clf, A.shape[1], K)
            SAl = C.score_matrix(clf, A)
            sdS = np.maximum(SAl.std(0), 1e-12)
            d = W @ (muB - muA)
            d = d - d.mean()
            t_off = float(np.linalg.norm(d / sdS) / np.sqrt(K))
            dz = W @ muB
            dz = dz - dz.mean()
            rho_zero = float(np.linalg.norm(dz / sdS) / np.sqrt(K))
            none = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)])
            zero = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - muB), 1)])
            mn = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - (muB - muA)), 1)])
            ref = C.cv_ref_cached(Bt, yb, ("ref", ds, p["sid_b"]), p["groups_b"])
            rows.append(dict(ds=ds, rep=p["rep"], subj=p["subj"], z=z_org, t=t_off,
                             rz=rho_zero,
                             none=none, zero=zero, mean=mn, ref=ref,
                             gap=ref - none, gain=mn - none, pen=zero - none))
    z = lambda k: np.array([r[k] for r in rows], float)
    ds = np.array([r["ds"] for r in rows])
    rep = np.array([r["rep"] for r in rows])

    say("v8 screen analysis")
    say("")
    say("S1  cell level (n=%d)" % len(rows))
    for a, b in (("z", "pen"), ("z", "gain"), ("z", "gap"),
                 ("t", "gain"), ("t", "pen"), ("t", "gap"),
                 ("rz", "pen"), ("rz", "z")):
        r = stats.spearmanr(z(a), z(b))
        say("  spearman(%-4s, %-4s) = %+.3f  (p=%.1e)" % (a, b, r[0], r[1]))
    say("")
    say("S2  unit level (dataset x representation), medians")
    say("  %-5s %-7s %-5s %-9s %-9s %-9s %-9s %-9s %-9s"
        % ("ds", "rep", "n", "z_origin", "rho_zero", "gain", "pen", "gap", "frac"))
    units = []
    for u in sorted(set(zip(ds, rep))):
        m = (ds == u[0]) & (rep == u[1])
        g = np.median(z("gap")[m])
        fr = np.nan
        if g > 0.02:
            fr = np.median(z("gain")[m]) / g
        units.append((u[0], u[1], int(m.sum()), np.median(z("z")[m]), np.median(z("rz")[m]),
                      np.median(z("gain")[m]), np.median(z("pen")[m]), g, fr))
        say("  %-5s %-7s %-5d %-9.2f %-9.3f %-9.4f %-9.4f %-9.4f %-9.3f"
            % units[-1])
    zu = np.array([u[3] for u in units])
    tu = np.array([u[4] for u in units])
    fu = np.array([u[8] for u in units])
    pu = np.array([u[6] for u in units])
    gu = np.array([u[5] for u in units])
    ok = np.isfinite(fu)
    say("")
    say("  fraction vs rho_zero  : spearman %+.3f (p=%.3f, n=%d)"
        % (stats.spearmanr(tu[ok], fu[ok])[0], stats.spearmanr(tu[ok], fu[ok])[1], ok.sum()))
    say("  fraction vs z_origin  : spearman %+.3f (p=%.3f, n=%d)"
        % (stats.spearmanr(zu[ok], fu[ok])[0], stats.spearmanr(zu[ok], fu[ok])[1], ok.sum()))
    say("  gain     vs rho_zero  : spearman %+.3f (p=%.3f, n=%d)"
        % (stats.spearmanr(tu, gu)[0], stats.spearmanr(tu, gu)[1], len(tu)))
    say("  pen      vs z_origin  : spearman %+.3f (p=%.3f, n=%d)"
        % (stats.spearmanr(zu, pu)[0], stats.spearmanr(zu, pu)[1], len(zu)))
    say("  pen      vs rho_zero  : spearman %+.3f (p=%.3f, n=%d)"
        % (stats.spearmanr(tu, pu)[0], stats.spearmanr(tu, pu)[1], len(tu)))
    say("  z_origin vs rho_zero  : spearman %+.3f (p=%.3f, n=%d)"
        % (stats.spearmanr(zu, tu)[0], stats.spearmanr(zu, tu)[1], len(tu)))
    np.savez(os.path.join(C.OUT, "screen.npz"),
             **{k: z(k) for k in ("z", "t", "rz", "none", "zero", "mean", "ref",
                                  "gap", "gain", "pen")},
             ds=ds, rep=rep)
    print("done", P)


if __name__ == "__main__":
    main()
