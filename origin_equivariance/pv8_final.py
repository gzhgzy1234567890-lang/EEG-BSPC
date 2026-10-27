# -*- coding: utf-8 -*-
"""v8 final numbers: every table and statistic reported in the manuscript.

Sections
  1  inventory
  2  main levels and subject-level statistics
  3  representation-level screen (z_T vs recovered fraction)
  4  variants of the correction (equivalence class and partial corrections)
  5  classifier family
  6  calibration
  7  collapse certificate
  8  what the residual is

Usage:  python pv8_final.py [section,...]      (default: all)
Output: results/final_<section>.txt
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

DS = ("2a", "2b", "seed", "ner", "gal")
LOGS = {}


def say(sec, s=""):
    LOGS.setdefault(sec, []).append(str(s))
    with open(os.path.join(C.OUT, "final_%s.txt" % sec), "w", encoding="utf-8") as f:
        f.write("\n".join(LOGS[sec]) + "\n")


def pairs_of(ds, cap=None, iu=False):
    ps = C.all_pairs((ds,))
    if iu and ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    if cap and len(ps) > cap:
        idx = np.linspace(0, len(ps) - 1, cap).astype(int)
        ps = [ps[i] for i in idx]
    return ps


def ece(y, p, K, bins=10):
    """Expected calibration error for a predicted class-probability matrix."""
    conf = p.max(1)
    pred = p.argmax(1)
    hit = (pred == y).astype(float)
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for i in range(bins):
        m = (conf > edges[i]) & (conf <= edges[i + 1])
        if m.sum() == 0:
            continue
        e += m.mean() * abs(hit[m].mean() - conf[m].mean())
    return float(e)


def proba(clf, X):
    try:
        return np.asarray(clf.predict_proba(X), float)
    except Exception:
        s = np.asarray(clf.decision_function(X), float)
        if s.ndim == 1:
            s = np.stack([-s, s], 1)
        s = s - s.max(1, keepdims=True)
        e = np.exp(s)
        return e / e.sum(1, keepdims=True)


def wilcox(a):
    a = np.asarray(a, float)
    a = a[np.isfinite(a)]
    if len(a) < 5:
        return np.nan, np.nan
    r = stats.wilcoxon(a)
    return float(np.median(a)), float(r.pvalue)


def boot(a, n=10000, seed=0):
    a = np.asarray(a, float)
    a = a[np.isfinite(a)]
    if len(a) < 3:
        return np.nan, np.nan
    rs = np.random.RandomState(seed)
    m = [rs.choice(a, len(a), replace=True).mean() for _ in range(n)]
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


# ---------------------------------------------------------------- section 1
def sec1():
    sec = "1"
    say(sec, "v8 inventory  %s" % time.strftime("%H:%M:%S"))
    say(sec, "")
    say(sec, "  %-5s %-11s %-7s %-5s %-6s %-6s %-8s" %
        ("ds", "representation", "subj", "cells", "K", "D", "n_target"))
    for ds in DS:
        ps = pairs_of(ds, iu=True)
        reps = sorted(set(p["rep"] for p in ps))
        for r in reps:
            q = [p for p in ps if p["rep"] == r]
            if not q:
                continue
            say(sec, "  %-5s %-11s %-7d %-5d %-6d %-6d %-8d"
                % (ds, r, len(set(p["subj"] for p in q)), len(q),
                   len(np.unique(q[0]["ya"])), q[0]["A"].shape[1],
                   int(np.median([len(p["yb"]) for p in q]))))
    say(sec, "")
    tot = sum(len(pairs_of(d)) for d in DS)
    say(sec, "  total cells (ordered pairs) = %d" % tot)
    say(sec, "  note: for the same-cap control (gal) only unordered pairs are used, n=%d"
        % len(pairs_of("gal", iu=True)))


# ---------------------------------------------------------------- section 2
def sec2():
    sec = "2"
    say(sec, "v8 main levels and subject-level statistics  %s" % time.strftime("%H:%M:%S"))
    say(sec, "")
    rows = []
    for ds in DS:
        ps = pairs_of(ds, iu=(ds == "gal"))
        for p in ps:
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            g = Bt.mean(0) - A.mean(0)
            S = C.score_matrix(clf, Bt)
            none = C.ba(yb, classes[np.argmax(S, 1)])
            zero = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
            alig = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - g), 1)])
            ref = C.cv_ref_cached(Bt, yb, ("ref", ds, p["sid_b"]), p["groups_b"])
            src = C.cv_ref_cached(A, ya, ("src", ds, p["sid_a"]), p.get("groups_a"))
            rows.append(dict(ds=ds, rep=p["rep"], subj=p["subj"], none=none, zero=zero,
                             align=alig, ref=ref, src=src,
                             gain=alig - none, pen=zero - none))
    say(sec, "  %-5s %-5s %-8s %-8s %-8s %-8s %-8s %-8s"
        % ("ds", "n", "none", "zero", "align", "ref", "src", "gain"))
    for ds in DS:
        q = [r for r in rows if r["ds"] == ds]
        f = lambda k: np.mean([r[k] for r in q])
        say(sec, "  %-5s %-5d %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f"
            % (ds, len(q), f("none"), f("zero"), f("align"), f("ref"), f("src"), f("gain")))
    q = rows
    f = lambda k: np.mean([r[k] for r in q])
    say(sec, "  %-5s %-5d %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f"
        % ("all", len(q), f("none"), f("zero"), f("align"), f("ref"), f("src"), f("gain")))

    say(sec, "")
    say(sec, "  subject level: gain = align - none, one number per subject per dataset")
    say(sec, "  %-5s %-4s %-9s %-22s %-8s %-8s %-8s %-8s"
        % ("ds", "n", "median", "bootstrap 95% CI", "dz", "wilcox p", "up/n", "zero up"))
    all_g = []
    for ds in DS:
        q = [r for r in rows if r["ds"] == ds]
        subs = sorted(set(r["subj"] for r in q))
        g = np.array([np.mean([r["gain"] for r in q if r["subj"] == s]) for s in subs])
        z = np.array([np.mean([r["pen"] for r in q if r["subj"] == s]) for s in subs])
        lo, hi = boot(g)
        dz = g.mean() / max(g.std(ddof=1), 1e-9)
        med, pv = wilcox(g)
        say(sec, "  %-5s %-4d %-9.4f [%+.4f, %+.4f]   %-8.2f %-8.2e %-8d %-8d"
            % (ds, len(subs), med, lo, hi, dz, pv, int((g > 0).sum()), int((z > 0).sum())))
        all_g += list(g)
    say(sec, "  (no pooled test across datasets: the gain is on a different scale per dataset)")
    np.savez(os.path.join(C.OUT, "final_2.npz"),
             **{k: np.array([r[k] for r in rows], float)
                for k in ("none", "zero", "align", "ref", "src", "gain", "pen")},
             ds=np.array([r["ds"] for r in rows]), rep=np.array([r["rep"] for r in rows]),
             subj=np.array([r["subj"] for r in rows]))


# ---------------------------------------------------------------- section 3
def sec3():
    sec = "3"
    say(sec, "v8 representation-level screen  %s" % time.strftime("%H:%M:%S"))
    z = np.load(os.path.join(C.OUT, "exp2_2a,2b,seed,ner,gal.npz"))
    meta = []
    for ds in DS:
        ps = pairs_of(ds, iu=(ds == "gal"))
        for p in ps:
            meta.append((ds, p["rep"], p["subj"]))
    assert len(meta) == len(z["zT"])
    ds = np.array([m[0] for m in meta])
    rep = np.array([m[1] for m in meta])
    zT, gap, rec, resid = z["zT"], z["gap"], z["recover"], z["resid"]
    ok = (gap > 0.02)
    frac = np.where(ok, rec / np.maximum(gap, 1e-9), np.nan)
    say(sec, "  %-5s %-7s %-4s %-9s %-9s %-10s %-9s"
        % ("ds", "rep", "n", "median zT", "median gap", "median gain", "median frac"))
    units = []
    for u in sorted(set(zip(ds, rep))):
        m = (ds == u[0]) & (rep == u[1])
        units.append((u[0], u[1], int(m.sum()), np.median(zT[m]), np.median(gap[m]),
                      np.median(rec[m]), np.nanmedian(frac[m])))
        say(sec, "  %-5s %-7s %-4d %-9.3f %-9.4f %-10.4f %-9.3f"
            % (u[0], u[1], units[-1][2], units[-1][3], units[-1][4], units[-1][5], units[-1][6]))
    zt = np.array([u[3] for u in units])
    fr = np.array([u[6] for u in units])
    good = np.isfinite(fr)
    r = stats.spearmanr(zt[good], fr[good])
    say(sec, "")
    say(sec, "  across %d units: spearman(z_T, recovered fraction) = %+.3f (p=%.3f)"
        % (int(good.sum()), r[0], r[1]))
    say(sec, "  units with z_T < 0.3: n=%d, median recovered %.2f"
        % (int((zt < 0.3).sum()), np.nanmedian(fr[zt < 0.3])))
    say(sec, "  units with z_T > 0.5: n=%d, median recovered %.2f"
        % (int((zt > 0.5).sum()), np.nanmedian(fr[zt > 0.5])))
    say(sec, "")
    say(sec, "  the screen is representation-level: within a unit, z_T does not order the outcome")
    for u in sorted(set(zip(ds, rep))):
        m = (ds == u[0]) & (rep == u[1]) & ok
        if m.sum() < 10 or np.nanstd(frac[m]) == 0:
            continue
        rr = stats.spearmanr(zT[m], frac[m])
        say(sec, "    %-5s %-7s n=%-4d rho=%+.3f (p=%.2f)" % (u[0], u[1], int(m.sum()), rr[0], rr[1]))


# ---------------------------------------------------------------- section 4
def sec4():
    sec = "4"
    say(sec, "v8 variants of the correction  %s" % time.strftime("%H:%M:%S"))
    say(sec, "  none       no correction")
    say(sec, "  zero       target centred only (one-sided)")
    say(sec, "  mean       two-sided, sample mean (the equivariant correction)")
    say(sec, "  zscore     train-stat standardisation (claimed equivalent)")
    say(sec, "  proj       subtract only the component in the row space of W")
    say(sec, "  shrink     subtract half the offset")
    say(sec, "  low5       subtract the offset projected on the top-5 source PCA directions")
    say(sec, "  bal        class-balanced offset (uses target labels; upper bound)")
    say(sec, "")
    say(sec, "  %-5s %-5s %-8s %-8s %-8s %-8s %-8s %-8s %-8s %-10s"
        % ("ds", "n", "none", "zero", "mean", "zscore", "proj", "shrink", "low5", "bal"))
    for ds in DS:
        ps = pairs_of(ds, iu=(ds == "gal"))
        acc = {k: [] for k in ("none", "zero", "mean", "zscore", "proj", "shrink", "low5", "bal")}
        diff = {"zscore": [], "proj": []}
        for p in ps:
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            muA, muB = A.mean(0), Bt.mean(0)
            g = muB - muA
            W = C.linear_weights(clf, A.shape[1], K)
            # projection onto row space of W
            U, S, Vt = np.linalg.svd(W, full_matrices=False)
            P = Vt.T @ Vt
            # top-5 PCA of the source session
            Ac = A - muA
            Cva = np.cov(Ac, rowvar=False)
            w, V = np.linalg.eigh(Cva)
            idx = np.argsort(w)[::-1][:5]
            V5 = V[:, idx]
            P5 = V5 @ V5.T

            def pred(X):
                return classes[np.argmax(C.score_matrix(clf, X), 1)]

            Pn = pred(Bt)
            Pz = pred(Bt - Bt.mean(0))
            Pm = pred(Bt - g)
            sdA = np.where(A.std(0) < 1e-12, 1.0, A.std(0))
            # zscore: refit on standardised source, apply to standardised target
            cz = C.make("lda").fit((A - muA) / sdA, ya)
            Pzs = np.asarray(cz.classes_)[np.argmax(
                C.score_matrix(cz, (Bt - muA) / sdA), 1)]
            Pp = pred(Bt - (P @ g))
            Ps = pred(Bt - 0.5 * g)
            Pl = pred(Bt - (P5 @ g))
            # class-balanced offset (labels)
            gt = C.class_means(Bt, yb, classes)
            ga = C.class_means(A, ya, classes)
            gb = (gt - ga).mean(0)
            Pb = pred(Bt - gb)
            for k, v in (("none", Pn), ("zero", Pz), ("mean", Pm), ("proj", Pp),
                         ("shrink", Ps), ("low5", Pl), ("bal", Pb)):
                acc[k].append(C.ba(yb, v))
            acc["zscore"].append(C.ba(yb, Pzs))
            diff["zscore"].append(float(np.mean(Pzs == Pm)))
            diff["proj"].append(float(np.mean(Pp == Pm)))
        f = lambda k: np.mean(acc[k])
        say(sec, "  %-5s %-5d %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f %-10.4f"
            % (ds, len(ps), f("none"), f("zero"), f("mean"), f("zscore"),
               f("proj"), f("shrink"), f("low5"), f("bal")))
        say(sec, "        identical predictions to mean: zscore %.3f of samples ; proj %.3f"
            % (np.mean(diff["zscore"]), np.mean(diff["proj"])))


# ---------------------------------------------------------------- section 5
def sec5():
    sec = "5"
    say(sec, "v8 classifier family  %s" % time.strftime("%H:%M:%S"))
    say(sec, "  %-5s %-6s %-5s %-8s %-8s %-8s %-8s %-8s"
        % ("ds", "clf", "n", "none", "zero", "mean", "gain", "pen"))
    for ds in ("2b", "seed", "gal"):
        ps = pairs_of(ds, cap=60, iu=(ds == "gal"))
        for kind in ("lda", "logit", "svm"):
            a = {"none": [], "zero": [], "mean": []}
            for p in ps:
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                clf = C.make(kind).fit(A, ya)
                classes = np.asarray(clf.classes_)
                g = Bt.mean(0) - A.mean(0)
                a["none"].append(C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
                a["zero"].append(C.ba(yb, classes[np.argmax(
                    C.score_matrix(clf, Bt - Bt.mean(0)), 1)]))
                a["mean"].append(C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - g), 1)]))
            f = lambda k: np.mean(a[k])
            say(sec, "  %-5s %-6s %-5d %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f"
                % (ds, kind, len(ps), f("none"), f("zero"), f("mean"),
                   f("mean") - f("none"), f("zero") - f("none")))


# ---------------------------------------------------------------- section 6
def sec6():
    sec = "6"
    say(sec, "v8 calibration  %s" % time.strftime("%H:%M:%S"))
    say(sec, "  %-5s %-5s %-8s %-8s %-8s %-8s %-8s"
        % ("ds", "cond", "BA", "ECE", "Brier", "NLL", "n"))
    for ds in ("2b", "seed", "gal"):
        ps = pairs_of(ds, cap=60, iu=(ds == "gal"))
        for cond in ("none", "zero", "mean"):
            b, e, br, nl = [], [], [], []
            for p in ps:
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                clf = C.make("lda").fit(A, ya)
                classes = np.asarray(clf.classes_)
                g = Bt.mean(0) - A.mean(0)
                if cond == "none":
                    X = Bt
                elif cond == "zero":
                    X = Bt - Bt.mean(0)
                else:
                    X = Bt - g
                P = proba(clf, X)
                pred = classes[np.argmax(P, 1)]
                yi = np.array([int(np.where(classes == c)[0][0]) for c in yb])
                b.append(C.ba(yb, pred))
                e.append(ece(yi, P, len(classes)))
                br.append(float(np.mean(np.sum(P ** 2, 1) - 2 * P[np.arange(len(yi)), yi] + 1)))
                nl.append(float(-np.mean(np.log(np.maximum(P[np.arange(len(yi)), yi], 1e-12)))))
            say(sec, "  %-5s %-5s %-8.4f %-8.4f %-8.4f %-8.4f %-8d"
                % (ds, cond, np.mean(b), np.mean(e), np.mean(br), np.mean(nl), len(ps)))


# ---------------------------------------------------------------- section 7
def sec7():
    sec = "7"
    say(sec, "v8 collapse certificate  %s" % time.strftime("%H:%M:%S"))
    say(sec, "  criterion (label-free): the classifier has collapsed onto class c iff")
    say(sec, "      min_k!=c [ (delta_k - delta_c) - max_x (s_k(x) - s_c(x)) ] > 0")
    say(sec, "  with delta_k = -w_k'mu_T, evaluated on the target scores.")
    say(sec, "  %-5s %-4s %-9s %-9s %-6s %-4s %-4s %-4s %-4s"
        % ("ds", "K", "collapsed", "predicted", "TP", "FP", "FN", "TN", "BA=1/K"))
    for ds in DS:
        ps = pairs_of(ds, iu=(ds == "gal"))
        tp = fp = fn = tn = ex = ch = 0
        for p in ps:
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            X = Bt - Bt.mean(0)
            S0 = C.score_matrix(clf, Bt)      # uncentred: the criterion needs the raw scores
            S = C.score_matrix(clf, X)
            pred = classes[np.argmax(S, 1)]
            # collapse is defined by the predictions, not by the accuracy: in an
            # imbalanced target, chance-level balanced accuracy does not imply
            # that every sample was given the same label.
            obs = len(np.unique(pred)) == 1
            ch += int(C.ba(yb, pred) <= 1.0 / K + 1e-9)
            # label-free criterion: test-only centring removes w_k'mu_T from
            # score k, so collapse onto c needs (delta_k - delta_c) to exceed
            # the largest observed score difference s_k - s_c.
            delta = C.linear_weights(clf, Bt.shape[1], K) @ Bt.mean(0)
            predc = False
            for c in range(K):
                ok = True
                for k in range(K):
                    if k == c:
                        continue
                    if (delta[k] - delta[c]) <= (S0[:, k] - S0[:, c]).max():
                        ok = False
                        break
                if ok:
                    predc = True
            if obs and predc:
                tp += 1
            elif obs and not predc:
                fn += 1
            elif (not obs) and predc:
                fp += 1
            else:
                tn += 1
            if obs:
                ex += 1
        say(sec, "  %-5s %-4s %-9d %-9d %-6d %-4d %-4d %-4d %-4d"
            % (ds, "-", ex, tp + fp, tp, fp, fn, tn, ch))
        say(sec, "        (last column: cells whose balanced accuracy is exactly 1/K, "
                 "collapse or not)")


# ---------------------------------------------------------------- section 8
def sec8():
    sec = "8"
    say(sec, "v8 what the residual is  %s" % time.strftime("%H:%M:%S"))
    z = np.load(os.path.join(C.OUT, "exp2_2a,2b,seed,ner,gal.npz"))
    meta = []
    for ds in DS:
        for p in pairs_of(ds, iu=(ds == "gal")):
            meta.append((ds, p["rep"]))
    ds = np.array([m[0] for m in meta])
    say(sec, "  residual = ref - align ; z_T = ||g||/||sd|| ; h = class-conditional part")
    say(sec, "  %-5s %-5s %-9s %-11s %-11s %-11s"
        % ("ds", "n", "resid", "rho(zT,res)", "rho(h,res)", "rho(dcov,res)"))
    for d in DS:
        m = (ds == d)
        if m.sum() < 10:
            continue
        r1 = stats.spearmanr(z["zT"][m], z["resid"][m])
        r2 = stats.spearmanr(z["h"][m], z["resid"][m])
        r3 = stats.spearmanr(z["dcov"][m], z["resid"][m])
        say(sec, "  %-5s %-5d %-9.4f %-11.3f %-11.3f %-11.3f (p=%.1e/%.1e/%.1e)"
            % (d, int(m.sum()), np.median(z["resid"][m]), r1[0], r2[0], r3[0],
               r1[1], r2[1], r3[1]))
    m = np.ones(len(ds), bool)
    say(sec, "  pooled: rho(zT,resid)=%.3f  rho(h,resid)=%.3f  rho(dcov,resid)=%.3f"
        % (stats.spearmanr(z["zT"][m], z["resid"][m])[0],
           stats.spearmanr(z["h"][m], z["resid"][m])[0],
           stats.spearmanr(z["dcov"][m], z["resid"][m])[0]))


# ---------------------------------------------------------------- section 9
def sec9():
    sec = "9"
    say(sec, "v8 origin sweep, all datasets  %s" % time.strftime("%H:%M:%S"))
    say(sec, "  features f -> f + a*sbar*1 in both sessions; a is the unreported origin")
    say(sec, "  %-5s %-7s %-7s %-8s %-8s %-8s %-9s %-9s"
        % ("ds", "a", "z_T", "none", "zero", "align", "dNone", "collapse"))
    import glob
    files = sorted(glob.glob(os.path.join(C.OUT, "exp4_*.npz")))
    seen = {}
    for f in files:
        nm = os.path.basename(f).replace("exp4_", "").replace(".npz", "")
        z = np.load(f)
        n = len(z["a"])
        per = n // len(nm.split(","))
        for i, d in enumerate(nm.split(",")):
            s = slice(i * per, (i + 1) * per)
            a = z["a"][s]
            if d in seen:
                continue
            seen[d] = True
            zt, none, zero, alig = z["zT"][s], z["none"][s], z["zero"][s], z["align"][s]
            dn = none - none[0]
            for j in range(len(a)):
                say(sec, "  %-5s %-7.2f %-7.2f %-8.4f %-8.4f %-8.4f %-9.1e %-9.2f"
                    % (d, a[j], zt[j], none[j], zero[j], alig[j], abs(dn[j]),
                       z["coll"][s][j]))
            say(sec, "")


if __name__ == "__main__":
    which = sys.argv[1].split(",") if len(sys.argv) > 1 else ["1", "2", "3", "4", "5", "6", "7", "8"]
    t0 = time.time()
    for s in which:
        {"1": sec1, "2": sec2, "3": sec3, "4": sec4, "5": sec5,
         "6": sec6, "7": sec7, "8": sec8, "9": sec9}[s]()
        print("section %s done %.0fs" % (s, time.time() - t0))
