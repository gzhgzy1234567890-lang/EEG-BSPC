# -*- coding: utf-8 -*-
"""v51: is the trend real, and does it explain the loss?

Per cell, with block length m:
  d_b            P W (mu_b - mu_A), b = 1..B
  R2             mean over the K score components of r(index, d_b)^2
  R2_null        the same statistic after permuting the block order (500 draws),
                 which is the zero model that matches this B and this set of
                 block means
  dR2            R2 - mean(R2_null): the part that the observed order explains
  loss           BA(lambda = 0) - BA(lambda = 1), i.e. how much full correction
                 costs on this cell (positive = correction hurts)
  lag1           lag-one autocorrelation of the block means, to show what the
                 iid permutation destroys

Then, at the subject level: Spearman(dR2, loss) across subjects, and the same
within each dataset, with the 12 gal subjects listed individually.
"""
import os
import sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores

P = os.path.join(C.OUT, "trend_test.txt")
CSV = os.path.join(C.OUT, "trend_cells.csv")
L = []
M = 15
NPERM = 500
SOURCE_ONLY = ("euc", "csp", "de", "Ftime", "pow")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def pairs(ds):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    return [p for p in ps if p["rep"] in SOURCE_ONLY]


def r2_of(idx, Y):
    """mean over columns of squared Pearson r between idx and each column"""
    x = idx - idx.mean()
    xc = x / (np.linalg.norm(x) + 1e-12)
    Yc = Y - Y.mean(0)
    den = np.linalg.norm(Yc, axis=0) + 1e-12
    r = xc @ Yc / den
    return float(np.mean(r ** 2))


def cell(A, ya, Bt, yb, m, rng):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    K = len(classes)
    W = C.linear_weights(clf, A.shape[1], K)
    F = np.eye(K) - np.ones((K, K)) / K
    muA = A.mean(0)
    n = len(yb)
    if n < 2 * m:
        return None
    S0 = scores(Bt, W, np.asarray(clf.intercept_, float).ravel(), K)
    blocks = [(a, min(a + m, n)) for a in range(0, n, m)]
    D = np.array([F @ (W @ (Bt[a:b].mean(0) - muA)) for a, b in blocks])
    B = len(D)
    if B < 4:
        return None
    idx = np.arange(B)
    r2 = r2_of(idx, D)
    null = np.array([r2_of(idx, D[rng.permutation(B)]) for _ in range(NPERM)])
    # loss at full correction, applied causally block by block
    S1 = S0.copy()
    for i, (a, b) in enumerate(blocks):
        if i == 0:
            continue
        S1[a:b] = S0[a:b] - D[:i].mean(0)[None, :]
    ba0 = C.ba(yb[m:], classes[np.argmax(S0[m:], 1)])
    ba1 = C.ba(yb[m:], classes[np.argmax(S1[m:], 1)])
    # lag-1 autocorrelation of the block means (mean over components)
    if B >= 3:
        Dc = D - D.mean(0)
        a1 = np.mean([np.corrcoef(Dc[:-1, k], Dc[1:, k])[0, 1] if np.std(Dc[:, k]) > 0 else 0.0
                      for k in range(K)])
    else:
        a1 = np.nan
    # first four blocks only
    r2_4 = r2_of(np.arange(4), D[:4]) if B >= 4 else np.nan
    return dict(B=B, R2=r2, R2n=float(null.mean()), dR2=r2 - float(null.mean()),
                loss=ba0 - ba1, lag1=float(a1), r2_4=float(r2_4),
                dnrm=float(np.mean(np.linalg.norm(D, axis=1))))


def main():
    rng = np.random.RandomState(0)
    allrows = []
    for ds in ("gal", "seed", "2b", "2a", "ner"):
        rows = []
        for p in pairs(ds):
            r = cell(p["A"], p["ya"], p["B"], p["yb"], M, rng)
            if r:
                r.update(ds=ds, subj=p["subj"], pid=p["pid"])
                rows.append(r)
        if not rows:
            continue
        allrows += rows
        say("%-5s cells=%-4d median B=%-4.0f R2 %.3f  null %.3f  dR2 %.3f  lag1 %+.2f  loss %+.4f"
            % (ds, len(rows), np.median([r["B"] for r in rows]),
               np.median([r["R2"] for r in rows]),
               np.median([r["R2n"] for r in rows]),
               np.median([r["dR2"] for r in rows]),
               np.median([r["lag1"] for r in rows]),
               np.median([r["loss"] for r in rows])))
    with open(CSV, "w", encoding="utf-8") as f:
        f.write("ds,subj,pid,B,R2,R2null,dR2,loss,lag1,r2_4,dnrm\n")
        for r in allrows:
            f.write("%s,%s,%s,%d,%.4f,%.4f,%.4f,%.4f,%.3f,%.4f,%.3f\n"
                    % (r["ds"], r["subj"], r["pid"], r["B"], r["R2"], r["R2n"],
                       r["dR2"], r["loss"], r["lag1"], r["r2_4"], r["dnrm"]))

    say("")
    say("subject-level association between excess trend and correction loss")
    for ds in ("gal", "seed", "2b", "2a", "ner"):
        sel = [r for r in allrows if r["ds"] == ds]
        by = {}
        for r in sel:
            by.setdefault(r["subj"], []).append(r)
        sub_d = [np.median([x["dR2"] for x in v]) for v in by.values()]
        sub_l = [np.median([x["loss"] for x in v]) for v in by.values()]
        if len(by) < 5:
            say("  %-5s too few subjects" % ds)
            continue
        rho, p = stats.spearmanr(sub_d, sub_l)
        say("  %-5s %2d subjects  rho(dR2, loss) %+.3f  p=%.3f" % (ds, len(by), rho, p))

    gal = [r for r in allrows if r["ds"] == "gal"]
    by = {}
    for r in gal:
        by.setdefault(r["subj"], []).append(r)
    say("")
    say("gal per subject: median R2, null, dR2, loss")
    for s in sorted(by):
        v = by[s]
        say("  %-5s R2 %.3f  null %.3f  dR2 %+.3f  loss %+.3f  (B=%d)"
            % (s, np.median([x["R2"] for x in v]), np.median([x["R2n"] for x in v]),
               np.median([x["dR2"] for x in v]), np.median([x["loss"] for x in v]),
               int(np.median([x["B"] for x in v]))))
    # pooled, clustered by subject
    ds_all = [r for r in allrows if r["ds"] in ("gal", "seed", "2b")]
    by = {}
    for r in ds_all:
        by.setdefault(r["subj"], []).append(r)
    sub_d = np.array([np.median([x["dR2"] for x in v]) for v in by.values()])
    sub_l = np.array([np.median([x["loss"] for x in v]) for v in by.values()])
    rho = stats.spearmanr(sub_d, sub_l)[0]
    rs = np.random.RandomState(0)
    bs = []
    for _ in range(3000):
        idx = rs.choice(len(sub_d), len(sub_d))
        if np.std(sub_d[idx]) > 1e-9 and np.std(sub_l[idx]) > 1e-9:
            bs.append(stats.spearmanr(sub_d[idx], sub_l[idx])[0])
    say("")
    say("pooled gal+seed+2b, clustered by subject: rho %+.3f  95%% CI [%+.3f, %+.3f]  (%d subjects)"
        % (rho, np.percentile(bs, 2.5), np.percentile(bs, 97.5), len(sub_d)))
    print("done", P)


if __name__ == "__main__":
    main()
