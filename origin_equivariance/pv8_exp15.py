# -*- coding: utf-8 -*-
"""v9 experiment N: the arithmetic and statistics the referee asks for.

N1  z_w: three candidate scalings, and which one the code uses
N2  exact permutation p for the dataset-level Spearman (n = 5)
N3  screening capability: ROC/PR for a severe loss, with a cluster bootstrap
N4  the BCI-2a representation anomaly
N5  BCI-2b pair-type levels, not only gains
N6  paired bootstrap for the calibration differences
"""
import os
import sys
import itertools
import numpy as np
from scipy.stats import norm, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "exp15.txt")
L = []
DS = ("2a", "2b", "seed", "ner", "gal")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def pairs(ds):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    return ps


def auc(y, s):
    y = np.asarray(y, int)
    s = np.asarray(s, float)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    # rank-based AUC
    allv = np.concatenate([pos, neg])
    r = np.argsort(np.argsort(allv)) + 1.0
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)))


def main():
    say("v9 exp N")

    cells = []
    for ds in DS:
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            muA = A.mean(0)
            sdA = np.maximum(A.std(0), 1e-12)
            S = C.score_matrix(clf, A)
            sig = np.maximum(S.std(0), 1e-12)
            W = C.linear_weights(clf, A.shape[1], K)
            proj = W @ muA
            proj = proj - proj.mean()
            zT = float(np.linalg.norm(muA) / np.linalg.norm(sdA))
            zw = float(np.linalg.norm(proj / sig) / np.sqrt(K))
            pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
                   - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
            cells.append(dict(ds=ds, rep=p["rep"], zT=zT, zw=zw, pen=pen, K=K))
    ds = np.array([c["ds"] for c in cells])
    rep = np.array([c["rep"] for c in cells])
    zT = np.array([c["zT"] for c in cells])
    zw = np.array([c["zw"] for c in cells])
    pen = np.array([c["pen"] for c in cells])

    # ---------------- N1 definitions ----------------
    say("")
    say("=" * 84)
    say("N1  z_w: the code computes ||P W mu_A|| / (sqrt(K) sigma_s), sigma_s = sd of")
    say("    the source scores per column.  Binary check: W = [w; -w] gives")
    say("    ||P W mu|| = sqrt(2)|w'mu| and sqrt(K)=sqrt(2), so z_w = |w'mu|/sigma_s.")
    say("=" * 84)
    diff = 0.0
    for c in cells[:200]:
        if c["K"] != 2:
            continue
        p = [q for q in pairs(c["ds"]) if q["rep"] == c["rep"]][0]
        A, ya = p["A"], p["ya"]
        clf = C.make("lda").fit(A, ya)
        w = np.asarray(clf.coef_, float).ravel()
        sA = np.asarray(clf.decision_function(A), float).ravel()
        sig = sA.std()
        d = abs(abs(float(w @ A.mean(0))) / sig - c["zw"])
        diff = max(diff, d)
    say("  max |binary formula - code| over 200 cells: %.2e" % diff)

    # ---------------- N2 exact permutation p ----------------
    say("")
    say("=" * 84)
    say("N2  dataset-level Spearman: exact permutation p (n = 5)")
    say("=" * 84)
    dz = [np.median(zw[ds == d]) for d in DS]
    dp = [np.median(pen[ds == d]) for d in DS]
    rho = spearmanr(dz, dp)[0]
    say("  medians z_w  %s" % np.round(dz, 3))
    say("  medians pen  %s" % np.round(dp, 4))
    say("  spearman rho = %+.3f" % rho)
    cnt = tot = 0
    for perm in itertools.permutations(range(5)):
        rr = spearmanr(dz, [dp[i] for i in perm])[0]
        tot += 1
        if abs(rr) >= abs(rho) - 1e-12:
            cnt += 1
    say("  exact two-sided permutation p = %d/%d = %.4f" % (cnt, tot, cnt / float(tot)))

    # ---------------- N3 screening capability ----------------
    say("")
    say("=" * 84)
    say("N3  can z_w screen a severe loss (penalty < -0.05)?")
    say("=" * 84)
    for thr in (-0.05, -0.10):
        y = (pen < thr).astype(int)
        a = auc(y, -zw)   # larger z_w -> more likely severe, so use -z_w
        say("  cell level, threshold %.2f: positives %d/%d, AUC = %.3f"
            % (thr, int(y.sum()), len(y), a))
    # unit level
    units = sorted(set(zip(ds, rep)))
    uz = np.array([np.median(zw[(ds == a) & (rep == b)]) for a, b in units])
    up = np.array([np.median(pen[(ds == a) & (rep == b)]) for a, b in units])
    for thr in (-0.05, -0.10):
        y = (up < thr).astype(int)
        say("  unit level, threshold %.2f: positives %d/%d, AUC = %.3f"
            % (thr, int(y.sum()), len(y), auc(y, -uz)))
    # cluster bootstrap of the cell-level AUC
    rs = np.random.RandomState(0)
    for thr in (-0.05,):
        y = (pen < thr).astype(int)
        out = []
        for _ in range(2000):
            pick = rs.choice(DS, len(DS), replace=True)
            idx = np.concatenate([np.where(ds == d)[0] for d in pick])
            a = auc(y[idx], -zw[idx])
            if np.isfinite(a):
                out.append(a)
        out = np.array(out)
        say("  cluster bootstrap AUC (threshold %.2f): median %.3f, 95%% CI [%.3f, %.3f]"
            % (thr, np.median(out), np.percentile(out, 2.5), np.percentile(out, 97.5)))

    # ---------------- N4 the 2a anomaly ----------------
    say("")
    say("=" * 84)
    say("N4  the BCI-2a representation anomaly")
    say("=" * 84)
    say("  %-6s %-9s %-9s %-9s" % ("rep", "z_w", "penalty", "n"))
    for b in sorted(set(rep[ds == "2a"])):
        m = (ds == "2a") & (rep == b)
        say("  %-6s %-9.3f %-9.4f %-9d" % (b, np.median(zw[m]), np.median(pen[m]), int(m.sum())))

    # ---------------- N5 BCI-2b pair types ----------------
    say("")
    say("=" * 84)
    say("N5  BCI-2b: levels by pair type, not only gains")
    say("=" * 84)
    say("  %-6s %-5s %-9s %-9s %-9s" % ("pair", "n", "none", "mean", "gain"))
    for p in pairs("2b"):
        pass
    acc = {}
    for p in pairs("2b"):
        A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
        clf = C.make("lda").fit(A, ya)
        cl = np.asarray(clf.classes_)
        g = Bt.mean(0) - A.mean(0)
        acc.setdefault(p["meta"]["seq"], []).append(
            (C.ba(yb, cl[np.argmax(C.score_matrix(clf, Bt), 1)]),
             C.ba(yb, cl[np.argmax(C.score_matrix(clf, Bt - g), 1)])))
    for k in sorted(acc):
        a = np.array(acc[k])
        say("  %-6s %-5d %-9.4f %-9.4f %-9.4f" % (k, len(a), a[:, 0].mean(), a[:, 1].mean(),
                                                 (a[:, 1] - a[:, 0]).mean()))

    # ---------------- N6 paired calibration bootstrap ----------------
    say("")
    say("=" * 84)
    say("N6  calibration: paired difference (mean over subjects), bootstrap interval")
    say("=" * 84)

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

    for d in ("2b", "seed", "gal"):
        per = {"none": {}, "zero": {}, "mean": {}}
        for p in pairs(d):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            yi = np.array([int(np.where(classes == c)[0][0]) for c in yb])
            g = Bt.mean(0) - A.mean(0)
            for cond, X in (("none", Bt), ("zero", Bt - Bt.mean(0)), ("mean", Bt - g)):
                per[cond].setdefault(p["subj"], []).append(ece(yi, clf.predict_proba(X)))
        subs = sorted(per["none"])
        a = np.array([np.mean(per["zero"][s]) - np.mean(per["none"][s]) for s in subs])
        b = np.array([np.mean(per["mean"][s]) - np.mean(per["none"][s]) for s in subs])
        rs = np.random.RandomState(0)
        for nm, v in (("zero-none", a), ("mean-none", b)):
            bs = [rs.choice(v, len(v), replace=True).mean() for _ in range(5000)]
            say("  %-5s %-11s mean %+.4f  95%% CI [%+.4f, %+.4f]"
                % (d, nm, v.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)))
    print("done", P)


if __name__ == "__main__":
    main()
