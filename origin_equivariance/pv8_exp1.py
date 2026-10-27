# -*- coding: utf-8 -*-
"""v8 experiment A: geometry of the offset, the damage law, and the three
estimators of the correction.

Run:  python pv8_exp1.py 2b ner gal        (fast subset)
      python pv8_exp1.py all               (all five datasets)

Output: results/exp1_<tag>.txt and results/exp1_<tag>.npz
"""
import os
import sys
import time
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

LOG = []
TAG = sys.argv[1] if len(sys.argv) > 1 else "all"
LOG_PATH = os.path.join(C.OUT, "exp1_%s.txt" % TAG)


def say(s=""):
    LOG.append(str(s))
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


def r2(y, yh):
    y = np.asarray(y, float)
    yh = np.asarray(yh, float)
    ok = np.isfinite(y) & np.isfinite(yh)
    y, yh = y[ok], yh[ok]
    if len(y) < 3:
        return np.nan, np.nan, np.nan
    ss = ((y - y.mean()) ** 2).sum()
    r = 1.0 - ((y - yh) ** 2).sum() / max(ss, 1e-12)
    pr = stats.pearsonr(y, yh)
    rmse = float(np.sqrt(np.mean((y - yh) ** 2)))
    return float(r), float(pr[0]), rmse


def main():
    t0 = time.time()
    if TAG == "all":
        dss = ("2a", "2b", "seed", "ner", "gal")
    else:
        dss = tuple(TAG.split(","))
    say("v8 experiment A   datasets=%s   %s" % (",".join(dss), time.strftime("%H:%M:%S")))
    say("")
    rows = []
    for ds in dss:
        pairs = C.all_pairs((ds,))
        say("=== %s : %d cells ===" % (ds, len(pairs)))
        for k, p in enumerate(pairs):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            S = C.score_matrix(clf, Bt)
            pred = classes[np.argmax(S, 1)]
            ref = C.cv_ref(Bt, yb, p["groups_b"])
            src = C.cv_ref(A, ya)
            muA, muB = A.mean(0), Bt.mean(0)
            g = muB - muA
            geo = C.offset_decomposition(A, ya, Bt, yb, classes)
            dis = C.displacement(A, ya, Bt, clf, classes)
            tval = dis["t"]

            ba_none = C.ba(yb, pred)
            ba_zero = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - muB), 1)])
            ba_align = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - g), 1)])
            g_cgm, info = C.cgm_recentre(A, ya, Bt, classes)
            ba_cgm = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - g_cgm), 1)])
            g_or, _ = C.balanced_offset_oracle(A, ya, Bt, yb, classes)
            ba_or = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - g_or), 1)])
            # class-conditional oracle: per-class mean correction (uses labels)
            mB = C.class_means(Bt, yb, classes)
            mA = C.class_means(A, ya, classes)
            Bcc = Bt.copy()
            for i, c in enumerate(classes):
                Bcc[yb == c] -= (mB[i] - mA[i])
            ba_cc = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bcc), 1)])

            pi_hat = info["pi"]
            pi_true = np.array([(yb == c).mean() for c in classes], float)
            rows.append(dict(
                ds=ds, rep=p["rep"], subj=p["subj"], pid=p["pid"],
                dpi=geo["dpi"], alpha=geo["alpha_n"],
                ort=float(np.linalg.norm(geo["g_ort"]) / max(np.linalg.norm(g), 1e-12)),
                gn=float(np.linalg.norm(g)), t=tval,
                ref=ref, src=src, none=ba_none, zero=ba_zero, align=ba_align,
                cgm=ba_cgm, oracle=ba_or, cc=ba_cc,
                pi_err=float(np.abs(np.asarray(pi_hat) - pi_true).max()),
                pred_none=C.predict_ba(src, tval) if len(classes) == 2 else np.nan,
                pred_align=src))
            if (k + 1) % 25 == 0:
                say("    %d/%d  %.0fs" % (k + 1, len(pairs), time.time() - t0))

    # ---------------- summary ----------------
    keys = ("ref", "src", "none", "zero", "align", "cgm", "oracle", "cc")
    say("")
    say("=" * 100)
    say("A1  balanced accuracy by dataset")
    say("=" * 100)
    say("  %-5s %-5s %-8s" % ("ds", "n", "gap(ref-none)") +
        "".join("%-9s" % k for k in keys))
    for ds in dss:
        q = [r for r in rows if r["ds"] == ds]
        say("  %-5s %-5d %-8.4f" % (ds, len(q), np.mean([r["ref"] - r["none"] for r in q])) +
            "".join("%-9.4f" % np.mean([r[k] for r in q]) for k in keys))

    say("")
    say("=" * 100)
    say("A2  repair: gain over no correction, and residual to the within-session reference")
    say("=" * 100)
    say("  %-5s %-9s %-9s %-9s %-9s | %-9s %-9s %-9s"
        % ("ds", "align-none", "cgm-none", "oracle-none", "cc-none",
           "align-ref", "cgm-ref", "cc-ref"))
    for ds in dss:
        q = [r for r in rows if r["ds"] == ds]
        f = lambda k: np.mean([r[k] for r in q])
        say("  %-5s %-9.4f %-9.4f %-9.4f %-9.4f | %-9.4f %-9.4f %-9.4f"
            % (ds, f("align") - f("none"), f("cgm") - f("none"), f("oracle") - f("none"),
               f("cc") - f("none"), f("align") - f("ref"), f("cgm") - f("ref"),
               f("cc") - f("ref")))

    say("")
    say("=" * 100)
    say("A3  decomposition of the offset: parallel (label-shift-like) vs orthogonal (nuisance)")
    say("=" * 100)
    say("  %-5s %-7s %-9s %-9s %-9s %-9s %-9s"
        % ("ds", "n", "mean|dpi|", "mean|alpha|", "sd alpha", "||g_ort||/||g||", "corr(alpha,dpi)"))
    for ds in dss:
        q = [r for r in rows if r["ds"] == ds]
        a = np.array([r["alpha"] for r in q], float)
        dp = np.array([r["dpi"] for r in q], float)
        ok = np.isfinite(a) & np.isfinite(dp)
        cc = stats.pearsonr(a[ok], dp[ok])[0] if ok.sum() > 3 and a[ok].std() > 0 and dp[ok].std() > 0 else np.nan
        say("  %-5s %-7d %-9.3f %-9.3f %-9.3f %-9.3f %-9.3f"
            % (ds, len(q), np.mean(np.abs(dp)), np.mean(np.abs(a)), a.std(),
               np.mean([r["ort"] for r in q]), cc))
    q = [r for r in rows if np.isfinite(r["dpi"])]
    if len(q) > 5:
        a = np.array([r["alpha"] for r in q])
        dp = np.array([r["dpi"] for r in q])
        sl, ic, rr, pp, se = stats.linregress(dp, a)
        say("  pooled regression  alpha = %.3f * dpi %+.3f   r=%.3f  R2=%.3f  p=%.2e  n=%d"
            % (sl, ic, rr, rr ** 2, pp, len(q)))

    say("")
    say("=" * 100)
    say("A4  the damage law: predict the no-correction accuracy from (source CV, t)")
    say("=" * 100)
    q = [r for r in rows if r["ds"] in ("2b", "ner", "gal")]
    if len(q) > 5:
        obs = np.array([r["none"] for r in q])
        prd = np.array([r["pred_none"] for r in q])
        say("  binary cells n=%d" % len(q))
        say("  observed mean %.4f  predicted mean %.4f  bias %+.4f" %
            (obs.mean(), prd.mean(), prd.mean() - obs.mean()))
        r2v, rv, rm = r2(obs, prd)
        say("  R2=%.3f  r=%.3f  RMSE=%.4f" % (r2v, rv, rm))
        for ds in ("2b", "ner", "gal"):
            z = [r for r in q if r["ds"] == ds]
            o = np.array([r["none"] for r in z])
            p = np.array([r["pred_none"] for r in z])
            r2v, rv, rm = r2(o, p)
            say("    %-4s n=%-3d obs %.4f pred %.4f  R2=%.3f r=%.3f RMSE=%.4f"
                % (ds, len(z), o.mean(), p.mean(), r2v, rv, rm))
        # alternative: use the target reference as the aligned accuracy
        obs2 = np.array([r["align"] for r in q])
        prd2 = np.array([C.predict_ba(r["ref"], r["t"]) for r in q])
        r2v, rv, rm = r2(obs2, prd2)
        say("  (using the target-session reference as the aligned level) R2=%.3f r=%.3f RMSE=%.4f"
            % (r2v, rv, rm))
        say("  correlation t vs observed damage: rho=%.3f p=%.2e"
            % stats.spearmanr([r["t"] for r in q], [r["ref"] - r["none"] for r in q]))

    say("")
    say("=" * 100)
    say("A5  CGM vs plain centring as a function of the prior change")
    say("=" * 100)
    q = [r for r in rows if np.isfinite(r["dpi"])]
    d = np.array([r["cgm"] - r["align"] for r in q])
    dp = np.array([abs(r["dpi"]) for r in q])
    say("  all cells n=%d : cgm-align mean %+.4f median %+.4f ; cgm better %d/%d"
        % (len(q), d.mean(), np.median(d), int((d > 0).sum()), len(q)))
    for thr in (0.05, 0.1, 0.2):
        m = dp >= thr
        if m.sum() > 2:
            say("  |dpi| >= %.2f  n=%-3d  cgm-align mean %+.4f  median %+.4f  better %d/%d"
                % (thr, int(m.sum()), d[m].mean(), np.median(d[m]),
                   int((d[m] > 0).sum()), int(m.sum())))
    say("  prior estimation error (max abs over classes) vs |dpi|: rho=%.3f p=%.2e"
        % stats.spearmanr(dp, [r["pi_err"] for r in q]))

    np.savez(os.path.join(C.OUT, "exp1_%s.npz" % TAG),
             **{k: np.array([r[k] for r in rows], float)
                for k in ("dpi", "alpha", "ort", "gn", "t", "ref", "src", "none",
                          "zero", "align", "cgm", "oracle", "cc", "pi_err",
                          "pred_none", "pred_align")})
    say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", LOG_PATH)


if __name__ == "__main__":
    main()
