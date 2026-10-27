# -*- coding: utf-8 -*-
"""v9 experiment N2: corrected arithmetic checks.

Fixes two errors of the first version of this script:
  * the binary-formula check must use the same cell, not the first cell of the
    representation;
  * the ROC must be reported with the sign of the statistic that is claimed
    (larger z_w -> more severe), and split into between- and within-dataset AUC.
"""
import os
import sys
import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "exp16.txt")
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
    allv = np.concatenate([pos, neg])
    r = np.argsort(np.argsort(allv)) + 1.0
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)))


def prauc(y, s):
    y = np.asarray(y, int)
    o = np.argsort(-np.asarray(s, float))
    yy = y[o]
    tp = np.cumsum(yy)
    prec = tp / np.arange(1, len(yy) + 1)
    rec = tp / max(yy.sum(), 1)
    return float(np.sum(prec * yy) / max(yy.sum(), 1))


def main():
    say("v9 exp N2")
    rows = []
    for d in DS:
        for p in pairs(d):
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
            zw = float(np.linalg.norm(proj / sig) / np.sqrt(K))
            pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
                   - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
            # same-cell binary check
            binf = np.nan
            if K == 2:
                w = np.asarray(clf.coef_, float).ravel()
                sA = np.asarray(clf.decision_function(A), float).ravel()
                binf = abs(float(w @ muA)) / max(sA.std(), 1e-12)
            rows.append(dict(ds=d, rep=p["rep"], zw=zw, pen=pen, binf=binf))

    ds = np.array([r["ds"] for r in rows])
    zw = np.array([r["zw"] for r in rows])
    pen = np.array([r["pen"] for r in rows])
    diff = max(abs(r["binf"] - r["zw"]) for r in rows if np.isfinite(r["binf"]))
    say("")
    say("N1  binary reduction check, same cell: max | |w'mu|/sd(s) - z_w | = %.2e" % diff)

    say("")
    say("N3  screening a severe loss (penalty < -0.05), LDA, 845 cells")
    y = (pen < -0.05).astype(int)
    say("  positives %d / %d" % (int(y.sum()), len(y)))
    say("  AUC(z_w) = %.3f   PR-AUC(z_w) = %.3f" % (auc(y, zw), prauc(y, zw)))
    say("  AUC(z_T) = %.3f" % auc(y, np.array([0.0] * len(y))) if False else "")
    # within-dataset
    say("  within dataset:")
    for d in DS:
        m = ds == d
        if len(np.unique(y[m])) < 2:
            say("    %-5s no positives or no negatives (%d cells)" % (d, m.sum()))
            continue
        say("    %-5s n=%-4d positives=%-3d AUC=%.3f" % (d, m.sum(), int(y[m].sum()), auc(y[m], zw[m])))
    # unit level
    units = sorted(set(zip(ds, [r["rep"] for r in rows])))
    uz = np.array([np.median(zw[(ds == a) & ([r["rep"] for r in rows] == b)]) for a, b in units])
    up = np.array([np.median(pen[(ds == a) & ([r["rep"] for r in rows] == b)]) for a, b in units])
    yu = (up < -0.05).astype(int)
    say("  unit level: positives %d/11, AUC = %.3f" % (int(yu.sum()), auc(yu, uz)))
    # cluster bootstrap
    rs = np.random.RandomState(0)
    out = []
    for _ in range(2000):
        pick = rs.choice(DS, len(DS), replace=True)
        idx = np.concatenate([np.where(ds == d)[0] for d in pick])
        a = auc(y[idx], zw[idx])
        if np.isfinite(a):
            out.append(a)
    out = np.array(out)
    say("  cluster bootstrap AUC: median %.3f, 95%% CI [%.3f, %.3f]"
        % (np.median(out), np.percentile(out, 2.5), np.percentile(out, 97.5)))
    print("done", P)


if __name__ == "__main__":
    main()
