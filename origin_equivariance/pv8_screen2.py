# -*- coding: utf-8 -*-
"""v9: a direction-aware source-only screen, and its comparison with z_T.

The referee asks for a fair comparison with a source-only indicator that is
related to the decision direction.  Define

    z_w = | w' mu_A | / ( ||w|| sigma_s )

which uses only the source session (the fitted weights and the source mean), and
compare it with the norm-based statistic z_T = ||mu_A|| / || sd_A ||.
"""
import os
import sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "screen2.txt")
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


def main():
    rows = []
    for ds in DS:
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            muA = A.mean(0)
            sdA = np.maximum(A.std(0), 1e-12)
            SAl = C.score_matrix(clf, A)
            sig = np.maximum(SAl.std(0), 1e-12)
            W = C.linear_weights(clf, A.shape[1], K)
            zT = float(np.linalg.norm(muA) / np.linalg.norm(sdA))
            proj = W @ muA
            proj = proj - proj.mean()
            zw = float(np.linalg.norm(proj / sig) / np.sqrt(K))
            pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
                   - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
            rows.append(dict(ds=ds, rep=p["rep"], z=zT, zw=zw, pen=pen))

    say("v9 screen, direction-aware source-only statistic")
    say("")
    say("  margins (unit medians)")
    say("  %-5s %-7s %-5s %-9s %-9s %-9s" % ("ds", "rep", "n", "z_T", "z_w", "penalty"))
    units = []
    ds = np.array([r["ds"] for r in rows])
    rep = np.array([r["rep"] for r in rows])
    z = np.array([r["z"] for r in rows])
    zw = np.array([r["zw"] for r in rows])
    pen = np.array([r["pen"] for r in rows])
    for u in sorted(set(zip(ds, rep))):
        m = (ds == u[0]) & (rep == u[1])
        units.append((u[0], u[1], int(m.sum()), np.median(z[m]), np.median(zw[m]),
                      np.median(pen[m])))
        say("  %-5s %-7s %-5d %-9.2f %-9.3f %-9.4f" % units[-1])

    zu = np.array([u[3] for u in units])
    wu = np.array([u[4] for u in units])
    pu = np.array([u[5] for u in units])
    say("")
    say("  unit level, n = 11")
    say("    spearman(z_T, penalty) = %+.3f (p = %.3f)" % stats.spearmanr(zu, pu))
    say("    spearman(z_w, penalty) = %+.3f (p = %.3f)" % stats.spearmanr(wu, pu))
    say("  cell level, n = %d" % len(rows))
    say("    spearman(z_T, penalty) = %+.3f" % (stats.spearmanr(z, pen)[0],))
    say("    spearman(z_w, penalty) = %+.3f" % (stats.spearmanr(zw, pen)[0],))
    say("  dataset level, n = 5")
    dz = [np.median(z[ds == d]) for d in DS]
    dw = [np.median(zw[ds == d]) for d in DS]
    dp = [np.median(pen[ds == d]) for d in DS]
    say("    spearman(z_T, penalty) = %+.3f (p = %.3f)" % stats.spearmanr(dz, dp))
    say("    spearman(z_w, penalty) = %+.3f (p = %.3f)" % stats.spearmanr(dw, dp))

    # cluster bootstrap over datasets for both statistics
    uds = np.array([u[0] for u in units])
    rs = np.random.RandomState(0)
    out_t, out_w = [], []
    for _ in range(5000):
        pick = rs.choice(DS, len(DS), replace=True)
        idx = np.concatenate([np.where(uds == d)[0] for d in pick])
        if len(idx) < 5 or np.std(zu[idx]) == 0 or np.std(pu[idx]) == 0:
            continue
        out_t.append(stats.spearmanr(zu[idx], pu[idx])[0])
        out_w.append(stats.spearmanr(wu[idx], pu[idx])[0])
    for nm, arr in (("z_T", out_t), ("z_w", out_w)):
        arr = np.array(arr)
        say("  cluster bootstrap %s: median %+.3f, 95%% CI [%+.3f, %+.3f], n = %d"
            % (nm, np.median(arr), np.percentile(arr, 2.5), np.percentile(arr, 97.5), len(arr)))

    # leave-one-dataset-out: predict the held-out dataset's median penalty from
    # a monotone fit (rank regression on log z) on the other four datasets
    say("")
    say("  leave-one-dataset-out (fit on four datasets' units, predict the fifth)")
    say("  %-5s %-9s %-9s %-9s %-9s" % ("held", "z_T pred", "z_T obs", "z_w pred", "z_w obs"))
    lz = np.log(np.maximum(zu, 1e-2))
    lw = np.log(np.maximum(wu, 1e-2))
    for held in DS:
        tr = uds != held
        te = uds == held
        if tr.sum() < 3 or te.sum() < 1:
            continue
        bt = np.polyfit(lz[tr], pu[tr], 1)
        bw = np.polyfit(lw[tr], pu[tr], 1)
        say("  %-5s %-9.4f %-9.4f %-9.4f %-9.4f"
            % (held, np.polyval(bt, np.median(lz[te])), np.median(pu[te]),
               np.polyval(bw, np.median(lw[te])), np.median(pu[te])))
    print("done", P)


if __name__ == "__main__":
    main()
