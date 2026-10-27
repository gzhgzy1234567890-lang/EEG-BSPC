# -*- coding: utf-8 -*-
"""v8 experiment K: the remaining computations demanded by the reject report.

K1  cluster-aware statistics: dataset-level analysis and a cluster bootstrap
    that resamples datasets, not units
K2  calibration on the full cell count (no uniform subsample)
K3  classifier sweep on the full cell count for BCI-2b and BCI-2a
K4  origin sweep with the a = 0 baseline reported alongside the directions
K5  does the z-score / none identity survive covariance shrinkage?
"""
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "exp12.txt")
L = []
DS = ("2a", "2b", "seed", "ner", "gal")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def pairs(ds, cap=None):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    if cap and len(ps) > cap:
        idx = np.linspace(0, len(ps) - 1, cap).astype(int)
        ps = [ps[i] for i in idx]
    return ps


def ece(yi, Pm, bins=10):
    conf, pred = Pm.max(1), Pm.argmax(1)
    hit = (pred == yi).astype(float)
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for i in range(bins):
        m = (conf > edges[i]) & (conf <= edges[i + 1])
        if m.sum():
            e += m.mean() * abs(hit[m].mean() - conf[m].mean())
    return float(e)


def main():
    t0 = time.time()
    say("v8 exp K   %s" % time.strftime("%H:%M:%S"))

    # ---- K1 cluster-aware statistics ----
    say("")
    say("=" * 88)
    say("K1  cluster-aware analysis of the screen")
    say("=" * 88)
    z = np.load(os.path.join(C.OUT, "screen.npz"))
    ds = np.array([str(s) for s in z["ds"]])
    rep = np.array([str(s) for s in z["rep"]])
    zT, pen = z["z"], z["pen"]
    say("  dataset level (one observation per dataset, n = 5)")
    say("  %-5s %-6s %-12s %-12s" % ("ds", "cells", "median z_T", "median penalty"))
    dz, dp = [], []
    for d in DS:
        m = ds == d
        dz.append(np.median(zT[m]))
        dp.append(np.median(pen[m]))
        say("  %-5s %-6d %-12.3f %-12.4f" % (d, int(m.sum()), dz[-1], dp[-1]))
    from scipy import stats as st
    r = st.spearmanr(dz, dp)
    say("  spearman across the five datasets: %+.3f (p = %.3f)" % (r[0], r[1]))
    # cluster bootstrap: resample datasets with replacement, then units within
    units = sorted(set(zip(ds, rep)))
    uval = np.array([[np.median(zT[(ds == a) & (rep == b)]),
                      np.median(pen[(ds == a) & (rep == b)])] for a, b in units])
    uds = np.array([a for a, b in units])
    rs = np.random.RandomState(0)
    out = []
    for _ in range(5000):
        pick = rs.choice(DS, len(DS), replace=True)
        idx = np.concatenate([np.where(uds == d)[0] for d in pick])
        if len(idx) < 5 or np.std(uval[idx, 0]) == 0 or np.std(uval[idx, 1]) == 0:
            continue
        out.append(st.spearmanr(uval[idx, 0], uval[idx, 1])[0])
    out = np.array(out)
    say("  cluster bootstrap (resampling the five datasets) of the unit-level rho:")
    say("    median %+.3f   95%% CI [%+.3f, %+.3f]   n = %d resamples"
        % (np.median(out), np.percentile(out, 2.5), np.percentile(out, 97.5), len(out)))

    # ---- K2 calibration on the full cell count ----
    say("")
    say("=" * 88)
    say("K2  calibration, every cell (no subsample)")
    say("=" * 88)
    say("  %-5s %-6s %-4s %-9s" % ("ds", "cond", "n", "median ECE"))
    for d in ("2b", "seed", "gal"):
        ps = pairs(d)
        for cond in ("none", "zero", "mean"):
            per = {}
            for p in ps:
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                clf = C.make("lda").fit(A, ya)
                classes = np.asarray(clf.classes_)
                g = Bt.mean(0) - A.mean(0)
                X = Bt if cond == "none" else (Bt - Bt.mean(0) if cond == "zero" else Bt - g)
                Pm = np.asarray(clf.predict_proba(X), float)
                yi = np.array([int(np.where(classes == c)[0][0]) for c in yb])
                per.setdefault(p["subj"], []).append(ece(yi, Pm))
            v = np.array([np.mean(x) for x in per.values()])
            say("  %-5s %-6s %-4d %-9.4f" % (d, cond, len(ps), np.median(v)))

    # ---- K3 classifier sweep, full cells for 2b ----
    say("")
    say("=" * 88)
    say("K3  classifier sweep on every cell of BCI-2b and BCI-2a")
    say("=" * 88)
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import LinearSVC

    def mk(kind, param):
        if kind == "lda":
            return LDA(solver="lsqr", shrinkage=param)
        if kind == "logit":
            return LogisticRegression(C=param, max_iter=4000, solver="lbfgs")
        return LinearSVC(C=param, max_iter=20000, dual=False, tol=1e-4)

    cfgs = ([("lda", s) for s in (0.1, 0.5, 0.9, "auto")] +
            [("logit", c) for c in (0.01, 1.0, 10.0)] +
            [("svm", c) for c in (0.001, 0.01, 0.1, 10.0)])
    for dsx, keep in (("2b", None), ("2a", [1, 2])):
        say("  %-5s %-6s %-6s %-9s %-9s %-9s" % (dsx, "clf", "param", "none", "zero", "damage"))
        for kind, param in cfgs:
            a, zz = [], []
            for p in pairs(dsx):
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                if keep:
                    ma, mb = np.isin(ya, keep), np.isin(yb, keep)
                    A, ya, Bt, yb = A[ma], ya[ma], Bt[mb], yb[mb]
                clf = mk(kind, param).fit(A, ya)
                if len(np.asarray(clf.classes_)) != 2:
                    continue
                cl = np.asarray(clf.classes_)
                a.append(C.ba(yb, cl[np.argmax(C.score_matrix(clf, Bt), 1)]))
                zz.append(C.ba(yb, cl[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)]))
            if a:
                say("  %-5s %-6s %-6s %-9.4f %-9.4f %-+9.4f"
                    % (dsx, kind, str(param), np.mean(a), np.mean(zz), np.mean(zz) - np.mean(a)))

    # ---- K4 direction baseline ----
    say("")
    say("=" * 88)
    say("K4  the direction experiment with its a = 0 baseline")
    say("=" * 88)
    rng = np.random.RandomState(13)
    for dsx in ("2b", "gal"):
        ps = pairs(dsx, 60)
        base = []
        for p in ps:
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            cl = np.asarray(clf.classes_)
            base.append(C.ba(yb, cl[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
                        - C.ba(yb, cl[np.argmax(C.score_matrix(clf, Bt), 1)]))
        say("  %-5s a=0 (no injected origin): median penalty %.4f" % (dsx, np.median(base)))
        for tag in ("parallel", "orthogonal"):
            for a in (2.0, 8.0):
                pen = []
                for p in ps:
                    A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                    clf = C.make("lda").fit(A, ya)
                    if len(np.asarray(clf.classes_)) != 2:
                        continue
                    w = np.asarray(clf.coef_, float).ravel()
                    sd = A.std(0).mean()
                    if tag == "parallel":
                        cdir = w / max(np.linalg.norm(w), 1e-12)
                    else:
                        u = rng.normal(size=A.shape[1])
                        u = u - (u @ w) / max(w @ w, 1e-12) * w
                        cdir = u / max(np.linalg.norm(u), 1e-12)
                    c = cdir * (a * sd)
                    A2, B2 = A + c, Bt + c
                    clf2 = C.make("lda").fit(A2, ya)
                    cl2 = np.asarray(clf2.classes_)
                    pen.append(C.ba(yb, cl2[np.argmax(C.score_matrix(clf2, B2 - B2.mean(0)), 1)])
                               - C.ba(yb, cl[np.argmax(C.score_matrix(clf, Bt), 1)]))
                say("  %-5s %-11s a=%-4.1f median penalty %.4f  (change %+.4f)"
                    % (dsx, tag, a, np.median(pen), np.median(pen) - np.median(base)))

    # ---- K5 shrinkage and the z-score identity ----
    say("")
    say("=" * 88)
    say("K5  z-score versus none: with and without covariance shrinkage")
    say("=" * 88)
    say("  %-5s %-12s %-12s" % ("ds", "shrink=auto", "shrink=0"))
    for dsx in ("2b", "2a", "gal"):
        agree = {}
        for shr in ("auto", 0.0):
            fr = []
            for p in pairs(dsx, 60):
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                sdA = np.where(A.std(0) < 1e-12, 1.0, A.std(0))
                clf = LDA(solver="lsqr", shrinkage=shr).fit(A, ya)
                cz = LDA(solver="lsqr", shrinkage=shr).fit((A - A.mean(0)) / sdA, ya)
                cl = np.asarray(clf.classes_)
                Pn = cl[np.argmax(C.score_matrix(clf, Bt), 1)]
                Pz = np.asarray(cz.classes_)[np.argmax(
                    C.score_matrix(cz, (Bt - A.mean(0)) / sdA), 1)]
                fr.append(float(np.mean(Pn == Pz)))
            agree[shr] = np.mean(fr)
        say("  %-5s %-12.3f %-12.3f" % (dsx, agree["auto"], agree[0.0]))

    say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", P)


if __name__ == "__main__":
    main()
