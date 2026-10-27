# -*- coding: utf-8 -*-
"""v8 experiment C: which component of a cross-session change does each
correction remove?

We perturb the target session in four controlled ways and ask which correction
recovers the damage:

    translation      B + c,          c = alpha * sd * u        -> centring
    gain             B * (1 + beta), beta per feature            -> moment match
    rotation         B Q,            Q near identity             -> none of them
    class-conditional B_c + h_c,     h zero-mean over classes    -> needs labels

A correction that removes component X should recover X and only X.  This turns
the "what is drift?" question into a four-way controlled experiment on the same
cells, with the unperturbed cell as its own control.

Output: results/exp3_<tag>.txt
"""
import os
import sys
import time
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

TAG = sys.argv[1] if len(sys.argv) > 1 else "2b,gal"
LOG = []
P = os.path.join(C.OUT, "exp3_%s.txt" % TAG)
RNG = np.random.RandomState(7)


def say(s=""):
    LOG.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


def moment_match(A, Bt):
    muA, mA = A.mean(0), Bt.mean(0)
    sA = np.maximum(A.std(0), 1e-9)
    sB = np.maximum(Bt.std(0), 1e-9)
    return muA + (Bt - mA) * (sA / sB)


def evaluate(A, ya, Bt, yb, classes, clf):
    S = C.score_matrix(clf, Bt)
    return C.ba(yb, classes[np.argmax(S, 1)])


def main():
    t0 = time.time()
    dss = tuple(TAG.split(","))
    say("v8 exp C: component-specific recovery   datasets=%s  %s"
        % (TAG, time.strftime("%H:%M:%S")))
    rec = []
    for ds in dss:
        pairs = C.all_pairs((ds,))
        if ds == "gal":
            pairs = [p for p in pairs
                     if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        # subsample deterministically for speed
        if len(pairs) > 60:
            idx = np.linspace(0, len(pairs) - 1, 60).astype(int)
            pairs = [pairs[i] for i in idx]
        say("=== %s : %d cells ===" % (ds, len(pairs)))
        for k, p in enumerate(pairs):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            g = Bt.mean(0) - A.mean(0)
            sd = np.maximum(A.std(0), 1e-9)
            ref = C.cv_ref_cached(Bt, yb, ("ref", ds, p["sid_b"]), p["groups_b"])
            base_none = evaluate(A, ya, Bt, yb, classes, clf)
            base_al = evaluate(A, ya, Bt - g, yb, classes, clf)
            base_mm = evaluate(A, ya, moment_match(A, Bt), yb, classes, clf)
            base = dict(none=base_none, centre=base_al, mom=base_mm, ref=ref)

            u = RNG.normal(size=A.shape[1])
            u = u / np.linalg.norm(u) * np.sqrt(A.shape[1])     # unit rms
            alpha = 40.0                                        # big origin shift
            Bt_t = Bt + alpha * sd * u
            tr_none = evaluate(A, ya, Bt_t, yb, classes, clf)
            tr_al = evaluate(A, ya, Bt_t - (Bt_t.mean(0) - A.mean(0)), yb, classes, clf)

            beta = RNG.normal(0.0, 0.25, A.shape[1])
            Bt_g = Bt * (1.0 + beta)
            ga_none = evaluate(A, ya, Bt_g, yb, classes, clf)
            ga_mm = evaluate(A, ya, moment_match(A, Bt_g), yb, classes, clf)

            # small rotation in a random 2-plane
            i, j = RNG.choice(A.shape[1], 2, replace=False)
            th = 0.5
            Q = np.eye(A.shape[1])
            Q[i, i] = np.cos(th)
            Q[j, j] = np.cos(th)
            Q[i, j] = -np.sin(th)
            Q[j, i] = np.sin(th)
            Bt_r = Bt @ Q
            ro_none = evaluate(A, ya, Bt_r, yb, classes, clf)
            ro_al = evaluate(A, ya, Bt_r - (Bt_r.mean(0) - A.mean(0)), yb, classes, clf)

            # class-conditional offset: +h on one class, -h on the other
            h = RNG.normal(size=A.shape[1]) * sd
            Bt_c = Bt.copy()
            for ci, c in enumerate(classes):
                Bt_c[yb == c] += (h if ci == 0 else -h) * 0.5
            cc_none = evaluate(A, ya, Bt_c, yb, classes, clf)
            cc_al = evaluate(A, ya, Bt_c - (Bt_c.mean(0) - A.mean(0)), yb, classes, clf)

            rec.append(dict(ds=ds, subj=p["subj"],
                            ref=ref, none=base_none,
                            base_centre=base_al, base_mom=base_mm,
                            tr_none=tr_none, tr_centre=tr_al,
                            ga_none=ga_none, ga_mom=ga_mm,
                            ro_none=ro_none, ro_centre=ro_al,
                            cc_none=cc_none, cc_centre=cc_al))
            if (k + 1) % 25 == 0:
                say("    %d/%d %.0fs" % (k + 1, len(pairs), time.time() - t0))

    say("")
    say("=" * 108)
    say("D1  absolute levels (mean balanced accuracy)")
    say("=" * 108)
    say("  %-5s %-4s %-8s %-8s | %-9s %-9s | %-9s %-9s | %-9s %-9s | %-9s %-9s"
        % ("ds", "n", "ref", "none", "tr_none", "tr_cen", "ga_none", "ga_mom",
           "ro_none", "ro_cen", "cc_none", "cc_cen"))
    for ds in dss + ("pooled",):
        q = rec if ds == "pooled" else [r for r in rec if r["ds"] == ds]
        if not q:
            continue
        f = lambda k: np.mean([r[k] for r in q])
        say("  %-5s %-4d %-8.4f %-8.4f | %-9.4f %-9.4f | %-9.4f %-9.4f | %-9.4f %-9.4f | %-9.4f %-9.4f"
            % (ds, len(q), f("ref"), f("none"), f("tr_none"), f("tr_centre"),
               f("ga_none"), f("ga_mom"), f("ro_none"), f("ro_centre"),
               f("cc_none"), f("cc_centre")))

    say("")
    say("=" * 108)
    say("D2  recovery of each perturbation (fraction of the induced damage removed)")
    say("=" * 108)
    say("  %-5s %-10s %-10s %-10s %-10s" % ("ds", "translation", "gain", "rotation", "class-cond"))
    for ds in dss + ("pooled",):
        q = rec if ds == "pooled" else [r for r in rec if r["ds"] == ds]
        if not q:
            continue
        out = []
        for a, b, c in (("tr_none", "tr_centre", "none"), ("ga_none", "ga_mom", "none"),
                        ("ro_none", "ro_centre", "none"), ("cc_none", "cc_centre", "none")):
            dam = np.array([r[a] - r[c] for r in q])
            rec_ = np.array([r[b] - r[a] for r in q])
            ok = dam < -0.005
            out.append(np.median(rec_[ok] / dam[ok]) if ok.sum() > 3 else np.nan)
        say("  %-5s %-10.3f %-10.3f %-10.3f %-10.3f" % (ds, out[0], out[1], out[2], out[3]))

    say("")
    say("=" * 108)
    say("D3  the same, restricted to perturbations that actually did damage (< -0.01)")
    say("=" * 108)
    for name, a, b in (("translation", "tr_none", "tr_centre"),
                       ("gain", "ga_none", "ga_mom"),
                       ("rotation", "ro_none", "ro_centre"),
                       ("class-cond", "cc_none", "cc_centre")):
        q = [r for r in rec if r[a] - r["none"] < -0.01]
        if not q:
            continue
        dam = np.array([r[a] - r["none"] for r in q])
        rv = np.array([r[b] - r[a] for r in q])
        say("  %-12s n=%-4d damage %+.4f  recovered %+.4f  median fraction %.3f  recovery>0 in %d/%d"
            % (name, len(q), dam.mean(), rv.mean(), np.median(rv / dam),
               int((rv > 0).sum()), len(q)))

    say("")
    say("=" * 108)
    say("D4  does the translation perturbation reproduce the real effect?")
    say("=" * 108)
    q = rec
    d_real = np.array([r["base_centre"] - r["none"] for r in q])
    d_inj = np.array([r["tr_centre"] - r["tr_none"] for r in q])
    say("  real centring gain median %+.4f ; injected-translation centring gain median %+.4f"
        % (np.median(d_real), np.median(d_inj)))
    say("  correlation across cells rho=%.3f (p=%.2e)"
        % stats.spearmanr(d_real, d_inj))

    np.savez(os.path.join(C.OUT, "exp3_%s.npz" % TAG),
             **{k: np.array([r[k] for r in rec], float)
                for k in ("ref", "none", "base_centre", "base_mom", "tr_none",
                          "tr_centre", "ga_none", "ga_mom", "ro_none", "ro_centre",
                          "cc_none", "cc_centre")})
    say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", P)


if __name__ == "__main__":
    main()
