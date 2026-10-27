# -*- coding: utf-8 -*-
"""v8 experiment D: two controlled experiments.

D1  origin sweep.  Add a constant a * sbar to every feature, in both sessions
    alike, and sweep a.  The data are unchanged up to an unreported convention,
    so:
      * the two-sided pipeline (align) and the uncorrected pipeline (none) must
        return exactly the same predictions at every a -- this is checked, not
        assumed;
      * the one-sided pipeline (zero) must slide and finally collapse.
    The sweep therefore measures the damage as a function of z_T with the cells
    held fixed, which removes the between-cell confound of the cross-sectional
    analysis.

D2  mean-neutral perturbations.  Each of four perturbations is applied twice:
    once as is, once with its induced mean difference removed.  If the repair
    works by removing a mean, the first version is repaired and the second is
    not.  The comparison is the mechanism test.

Output: results/exp4_<tag>.txt
"""
import os
import sys
import time
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

TAG = sys.argv[1] if len(sys.argv) > 1 else "2b,seed"
LOG = []
P = os.path.join(C.OUT, "exp4_%s.txt" % TAG)
RNG = np.random.RandomState(11)
ALPHAS = (0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0)
NCELL = 40


def say(s=""):
    LOG.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


def fit_pred(A, ya, Bt, classes):
    clf = C.make("lda").fit(A, ya)
    S = C.score_matrix(clf, Bt)
    return clf, classes[np.argmax(S, 1)]


def main():
    t0 = time.time()
    dss = tuple(TAG.split(","))
    say("v8 exp D   datasets=%s  %s" % (TAG, time.strftime("%H:%M:%S")))

    # ---------------- D1 origin sweep ----------------
    say("")
    say("=" * 108)
    say("D1  origin sweep: features f -> f + a*sbar*1 in both sessions")
    say("=" * 108)
    say("  %-5s %-8s %-5s %-7s %-8s %-8s %-8s %-8s %-8s %-9s"
        % ("ds", "a", "n", "z_T", "none", "zero", "align", "dNone", "dAlign", "collapsed"))
    sweep = []
    for ds in dss:
        pairs = C.all_pairs((ds,))
        if ds == "gal":
            pairs = [p for p in pairs
                     if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        if len(pairs) > NCELL:
            idx = np.linspace(0, len(pairs) - 1, NCELL).astype(int)
            pairs = [pairs[i] for i in idx]
        base = {}
        for p in pairs:
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            base[p["pid"]] = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)])
        for a in ALPHAS:
            res = []
            for p in pairs:
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                sb = 0.5 * (A.std(0).mean() + Bt.std(0).mean())
                d = a * sb
                A2, B2 = A + d, Bt + d
                clf = C.make("lda").fit(A2, ya)
                classes = np.asarray(clf.classes_)
                g = B2.mean(0) - A2.mean(0)
                p_none = classes[np.argmax(C.score_matrix(clf, B2), 1)]
                p_zero = classes[np.argmax(C.score_matrix(clf, B2 - B2.mean(0)), 1)]
                p_alig = classes[np.argmax(C.score_matrix(clf, B2 - g), 1)]
                n = C.ba(yb, p_none)
                z = C.ba(yb, p_zero)
                q = C.ba(yb, p_alig)
                zT = float(np.linalg.norm(A2.mean(0)) / np.linalg.norm(np.maximum(A2.std(0), 1e-12)))
                coll = float(abs(z - 1.0 / len(classes)) < 1e-9)
                res.append(dict(ds=ds, a=a, zT=zT, none=n, zero=z, align=q,
                                dNone=n - base[p["pid"]], dAlign=q - base[p["pid"]],
                                coll=coll,
                                pi=float((p_zero == classes[0]).mean())))
            n = len(res)
            mean = lambda k: np.mean([r[k] for r in res])
            say("  %-5s %-8.2f %-5d %-7.2f %-8.4f %-8.4f %-8.4f %-8.1e %-8.1e %-9.2f"
                % (ds, a, n, mean("zT"), mean("none"), mean("zero"), mean("align"),
                   np.max(np.abs([r["dNone"] for r in res])),
                   np.max(np.abs([r["dAlign"] for r in res])), mean("coll")))
            sweep.append(dict(ds=ds, a=a, n=n, zT=mean("zT"), none=mean("none"),
                              zero=mean("zero"), align=mean("align"),
                              coll=mean("coll")))
        say("")
    # invariance check
    inv_n = max(abs(s["none"] - [q for q in sweep if q["ds"] == s["ds"] and q["a"] == 0][0]["none"])
                for s in sweep)
    inv_a = max(abs(s["align"] - [q for q in sweep if q["ds"] == s["ds"] and q["a"] == 0][0]["align"])
                for s in sweep)
    say("  invariance over the whole sweep:  max|none - none(a=0)| = %.2e ;  max|align - align(a=0)| = %.2e"
        % (inv_n, inv_a))

    # ---------------- D2 mean-neutral perturbations ----------------
    say("")
    say("=" * 108)
    say("D2  mean-neutral control: the repair should track the induced mean, not the perturbation")
    say("=" * 108)
    say("  %-14s %-10s %-10s %-10s %-10s %-8s"
        % ("perturbation", "dam-shift", "rec-shift", "dam-neutral", "rec-neutral", "n"))
    for flavour in ("translation", "gain", "rotation", "classcond"):
        d_sh, r_sh, d_ne, r_ne = [], [], [], []
        for ds in dss:
            pairs = C.all_pairs((ds,))
            if ds == "gal":
                pairs = [p for p in pairs
                         if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
            if len(pairs) > NCELL:
                idx = np.linspace(0, len(pairs) - 1, NCELL).astype(int)
                pairs = [pairs[i] for i in idx]
            for p in pairs:
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                clf = C.make("lda").fit(A, ya)
                classes = np.asarray(clf.classes_)
                sd = np.maximum(A.std(0), 1e-9)
                base = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)])
                base_al = C.ba(yb, classes[np.argmax(
                    C.score_matrix(clf, Bt - (Bt.mean(0) - A.mean(0))), 1)])
                K = len(classes)
                if flavour == "translation":
                    u = RNG.normal(size=A.shape[1])
                    u = u / np.linalg.norm(u) * np.sqrt(A.shape[1])
                    pert = 20.0 * sd * u
                    Bp = Bt + pert[None, :]
                elif flavour == "gain":
                    beta = RNG.normal(0.0, 0.4, A.shape[1])
                    Bp = Bt * (1.0 + beta)[None, :]
                elif flavour == "rotation":
                    i, j = RNG.choice(A.shape[1], 2, replace=False)
                    th = 0.6
                    Q = np.eye(A.shape[1])
                    Q[i, i] = np.cos(th)
                    Q[j, j] = np.cos(th)
                    Q[i, j] = -np.sin(th)
                    Q[j, i] = np.sin(th)
                    Bp = Bt @ Q
                else:
                    h = RNG.normal(size=A.shape[1]) * sd
                    Bp = Bt.copy()
                    for ci, c in enumerate(classes):
                        Bp[yb == c] += (h if ci == 0 else -h) * 1.0
                # with the induced mean, and with it removed
                for tag, Bq in (("shift", Bp), ("neutral", Bp - (Bp.mean(0) - Bt.mean(0))[None, :])):
                    clf2 = C.make("lda").fit(A, ya)
                    pn = classes[np.argmax(C.score_matrix(clf2, Bq), 1)]
                    pa = classes[np.argmax(C.score_matrix(
                        clf2, Bq - (Bq.mean(0) - A.mean(0))[None, :]), 1)]
                    dam = C.ba(yb, pn) - base
                    rec = C.ba(yb, pa) - C.ba(yb, pn)
                    if tag == "shift":
                        d_sh.append(dam)
                        r_sh.append(rec)
                    else:
                        d_ne.append(dam)
                        r_ne.append(rec)
        f = lambda v: np.mean(v) if v else np.nan
        say("  %-14s %-10.4f %-10.4f %-10.4f %-10.4f %-8d"
            % (flavour, f(d_sh), f(r_sh), f(d_ne), f(r_ne), len(d_sh)))

    np.savez(os.path.join(C.OUT, "exp4_%s.npz" % TAG),
             **{k: np.array([s[k] for s in sweep], float)
                for k in ("a", "n", "zT", "none", "zero", "align", "coll")})
    say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", P)


if __name__ == "__main__":
    main()
