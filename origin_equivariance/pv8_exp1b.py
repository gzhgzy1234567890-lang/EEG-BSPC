# -*- coding: utf-8 -*-
"""v8 experiment A2: is cross-session damage the Gaussian displacement law?

With a two-class linear score s(x) = w'x + b fitted on the source session:

    m0, m1     source class means of s
    sigma      pooled within-class SD of s
    c          (m1 - m0) / (2 sigma)
    t          |w'g| / sigma,   g = mean(target) - mean(source)
    D(c, t)    Phi(c) - [Phi(c-t) + Phi(c+t)] / 2

D is the damage that leaving the target uncentred must produce if the only
thing that changed between sessions were a common additive offset.  c comes
from the source session, t from the unlabelled target features: both are
available before a single target label.

Output: results/exp1b_<tag>.txt
"""
import os
import sys
import time
import numpy as np
from scipy import stats
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

TAG = sys.argv[1] if len(sys.argv) > 1 else "2b,ner,gal"
LOG = []
P = os.path.join(C.OUT, "exp1b_%s.txt" % TAG)


def say(s=""):
    LOG.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


def r2(y, yh):
    y, yh = np.asarray(y, float), np.asarray(yh, float)
    ok = np.isfinite(y) & np.isfinite(yh)
    y, yh = y[ok], yh[ok]
    if len(y) < 3:
        return np.nan
    ss = ((y - y.mean()) ** 2).sum()
    return float(1.0 - ((y - yh) ** 2).sum() / max(ss, 1e-12))


def main():
    t0 = time.time()
    dss = tuple(TAG.split(","))
    say("v8 exp A2: displacement law   datasets=%s  %s" % (TAG, time.strftime("%H:%M:%S")))
    rows = []
    for ds in dss:
        pairs = C.all_pairs((ds,))
        if ds == "gal":
            pairs = [p for p in pairs
                     if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        say("=== %s : %d cells ===" % (ds, len(pairs)))
        for k, p in enumerate(pairs):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            if len(np.asarray(clf.classes_)) != 2:
                continue
            sA = np.asarray(clf.decision_function(A), float).ravel()
            sB = np.asarray(clf.decision_function(Bt), float).ravel()
            classes = np.asarray(clf.classes_)
            i0, i1 = (ya == classes[0]), (ya == classes[1])
            m0, m1 = sA[i0].mean(), sA[i1].mean()
            sig = np.sqrt(0.5 * (sA[i0].var(ddof=1) + sA[i1].var(ddof=1)))
            c = (m1 - m0) / (2.0 * sig)
            g = Bt.mean(0) - A.mean(0)
            w = np.asarray(clf.coef_, float).ravel()
            t = abs(float(w @ g)) / sig
            ref = C.cv_ref_cached(Bt, yb, ("ref", ds, p["sid_b"]), p["groups_b"])
            src = C.cv_ref_cached(A, ya, ("src", ds, p["sid_a"]))
            ba_none = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)])
            ba_align = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - g), 1)])
            d_hat = C.damage_law(c, t)
            c_ref = norm.ppf(np.clip(ref, 0.01, 0.99))
            rows.append(dict(ds=ds, rep=p["rep"], subj=p["subj"], pid=p["pid"],
                             c=c, t=t, sig=sig, ref=ref, src=src,
                             none=ba_none, align=ba_align,
                             d_obs=ba_align - ba_none, d_hat=d_hat,
                             d_hat_ref=C.damage_law(c_ref, t),
                             none_hat=0.5 * (norm.cdf(c - t) + norm.cdf(c + t)),
                             align_hat=norm.cdf(c)))
            if (k + 1) % 100 == 0:
                say("    %d/%d %.0fs" % (k + 1, len(pairs), time.time() - t0))

    say("")
    say("=" * 104)
    say("B1  ingredients (medians)")
    say("=" * 104)
    say("  %-5s %-5s %-8s %-8s %-8s %-8s %-8s %-8s"
        % ("ds", "n", "c", "t", "D_hat", "d_obs", "ref", "none"))
    for ds in dss:
        q = [r for r in rows if r["ds"] == ds]
        if not q:
            continue
        say("  %-5s %-5d %-8.3f %-8.3f %-8.4f %-8.4f %-8.4f %-8.4f"
            % (ds, len(q), np.median([r["c"] for r in q]), np.median([r["t"] for r in q]),
               np.median([r["d_hat"] for r in q]), np.median([r["d_obs"] for r in q]),
               np.median([r["ref"] for r in q]), np.median([r["none"] for r in q])))

    say("")
    say("=" * 104)
    say("B2  predicted vs observed damage  (d_obs = BA_align - BA_none)")
    say("=" * 104)
    groups = [("pooled", rows)] + [(d, [r for r in rows if r["ds"] == d]) for d in dss]
    for name, dd in groups:
        if len(dd) < 5:
            continue
        o = np.array([r["d_obs"] for r in dd])
        h = np.array([r["d_hat"] for r in dd])
        hr = np.array([r["d_hat_ref"] for r in dd])
        rho = stats.spearmanr(o, h)
        rho2 = stats.spearmanr(o, hr)
        say("  %-7s n=%-4d  D_hat bias %+.4f R2 %+.3f rho %+.3f (p=%.1e) | with target ref: R2 %+.3f rho %+.3f"
            % (name, len(dd), (h - o).mean(), r2(o, h), rho[0], rho[1], r2(o, hr), rho2[0]))
        sl, ic, rr, pp, se = stats.linregress(h, o)
        say("           obs = %.3f*D_hat %+.4f  (r=%.3f)   median |err| %.4f"
            % (sl, ic, rr, np.median(np.abs(o - h))))

    say("")
    say("=" * 104)
    say("B3  level prediction from (c, t) alone: BA_none and BA_align")
    say("=" * 104)
    for name, dd in groups:
        if len(dd) < 5:
            continue
        o = np.array([r["none"] for r in dd])
        h = np.array([r["none_hat"] for r in dd])
        oa = np.array([r["align"] for r in dd])
        ha = np.array([r["align_hat"] for r in dd])
        say("  %-7s n=%-4d  none: bias %+.4f R2 %+.3f RMSE %.4f | align: bias %+.4f R2 %+.3f RMSE %.4f"
            % (name, len(dd), (h - o).mean(), r2(o, h), np.sqrt(np.mean((h - o) ** 2)),
               (ha - oa).mean(), r2(oa, ha), np.sqrt(np.mean((ha - oa) ** 2))))

    say("")
    say("=" * 104)
    say("B4  does damage grow with the quality of the decoder (c)?  (cells with t>0.1)")
    say("=" * 104)
    q = [r for r in rows if r["t"] > 0.1]
    if len(q) > 10:
        cs = np.array([r["c"] for r in q])
        do = np.array([r["d_obs"] for r in q])
        ts = np.array([r["t"] for r in q])
        for lo, hi in ((-1, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 2.0)):
            m = (cs >= lo) & (cs < hi)
            if m.sum() > 2:
                say("  c in [%.2f,%.2f) n=%-4d  mean t %.2f  mean d_obs %+.4f  mean D_hat %+.4f"
                    % (lo, hi, int(m.sum()), ts[m].mean(), do[m].mean(),
                       np.array([r["d_hat"] for r in q])[m].mean()))
        say("  spearman(c, d_obs) = %+.3f (p=%.1e); spearman(t, d_obs) = %+.3f (p=%.1e)"
            % (stats.spearmanr(cs, do)[0], stats.spearmanr(cs, do)[1],
               stats.spearmanr(ts, do)[0], stats.spearmanr(ts, do)[1]))

    np.savez(os.path.join(C.OUT, "exp1b_%s.npz" % TAG),
             **{k: np.array([r[k] for r in rows], float)
                for k in ("c", "t", "sig", "ref", "src", "none", "align",
                          "d_obs", "d_hat", "d_hat_ref", "none_hat", "align_hat")})
    say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", P)


if __name__ == "__main__":
    main()
