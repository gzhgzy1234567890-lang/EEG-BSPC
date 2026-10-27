# -*- coding: utf-8 -*-
"""v18 experiment A: which representations are genuinely source-only?

`euc` and `csp` are built from the training session alone (CSP's filters are
fitted on A). `euc_ea` and `tan` use the covariance of both sessions, so a
classifier trained on them has already seen the target.  The source-only claim
must therefore be tested on the former.
"""
import os
import sys
import glob
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "sourceonly.txt")
L = []
CACHE4 = r"G:\Work_work\math\EEG\local_analysis\cache_seed4_iv"
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


def cell(A, ya, Bt, yb):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    K = len(classes)
    S = C.score_matrix(clf, A)
    Sc = S - S.mean(1, keepdims=True)
    sig = np.maximum(Sc.std(0), 1e-12)
    W = C.linear_weights(clf, A.shape[1], K)
    proj = W @ A.mean(0)
    proj = proj - proj.mean()
    z = float(np.linalg.norm(proj / sig) / np.sqrt(K))
    pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
           - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
    return z, pen


def auc(y, s):
    y = np.asarray(y, int)
    s = np.asarray(s, float)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    allv = np.concatenate([pos, neg])
    r = np.argsort(np.argsort(allv)) + 1.0
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)))


def main():
    rows = []
    for ds in DS:
        for p in pairs(ds):
            z, pen = cell(p["A"], p["ya"], p["B"], p["yb"])
            rows.append((ds, p["rep"], z, pen))
    # SEED-IV (DE features are computed per session by the dataset; source-only)
    subs = sorted(set(int(os.path.basename(f).split("_")[0])
                      for f in glob.glob(os.path.join(CACHE4, "*.npz"))))
    for sub in subs:
        S = {}
        for sess in (1, 2, 3):
            f = os.path.join(CACHE4, "%02d_%d.npz" % (sub, sess))
            if os.path.exists(f):
                d = np.load(f)
                S[sess] = (d["X"].astype(np.float64), d["y"].astype(int))
        for i in sorted(S):
            for j in sorted(S):
                if i != j:
                    z, pen = cell(S[i][0], S[i][1], S[j][0], S[j][1])
                    rows.append(("seed4", "de", z, pen))

    ds = np.array([r[0] for r in rows])
    rep = np.array([r[1] for r in rows])
    z = np.array([r[2] for r in rows])
    pen = np.array([r[3] for r in rows])
    target_informed = np.isin(rep, ["euc_ea", "tan"])

    say("v18 A: source-only versus target-informed representations")
    say("  (euc_ea and tan use both sessions' covariance; euc, csp and the")
    say("   single-representation datasets are source-only)")
    say("")
    say("  %-22s %-5s %-9s %-9s" % ("subset", "n", "unit rho", "cell AUC"))
    for name, m in (("all development", ds != "seed4"),
                    ("source-only only", (ds != "seed4") & ~target_informed),
                    ("target-informed only", (ds != "seed4") & target_informed)):
        u = sorted(set(zip(ds[m], rep[m])))
        uz = np.array([np.median(z[m][(ds[m] == a) & (rep[m] == b)]) for a, b in u])
        up = np.array([np.median(pen[m][(ds[m] == a) & (rep[m] == b)]) for a, b in u])
        y = (pen[m] < -0.05).astype(int)
        say("  %-22s %-5d %-9.3f %-9.3f"
            % (name, int(m.sum()),
               stats.spearmanr(uz, up)[0] if len(u) > 3 else np.nan,
               auc(y, z[m])))

    # source-only unit table
    say("")
    say("  source-only units")
    say("  %-5s %-7s %-5s %-9s %-9s" % ("ds", "rep", "n", "z_w", "penalty"))
    m = ~target_informed
    units = []
    for u in sorted(set(zip(ds[m], rep[m]))):
        k = m & (ds == u[0]) & (rep == u[1])
        units.append((u[0], u[1], int(k.sum()), np.median(z[k]), np.median(pen[k])))
        say("  %-5s %-7s %-5d %-9.3f %-9.4f" % units[-1])
    uz = np.array([v[3] for v in units])
    up = np.array([v[4] for v in units])
    say("  unit-level spearman, source-only: %+.3f (n=%d)" % (stats.spearmanr(uz, up)[0], len(uz)))
    # dataset medians, source-only, incl. held out
    say("")
    say("  dataset medians, source-only representations only")
    dsz = []
    for d in ("2a", "2b", "seed", "ner", "gal", "seed4"):
        k = (ds == d) & (~target_informed)
        if k.sum() == 0:
            continue
        dsz.append((np.median(z[k]), np.median(pen[k]), d))
    for v in dsz:
        say("    %-6s z_w %6.3f  penalty %+.4f" % (v[2], v[0], v[1]))
    if len(dsz) >= 5:
        r = stats.spearmanr([v[0] for v in dsz], [v[1] for v in dsz])
        say("    six-dataset spearman %+.3f" % r[0])
    print("done", P)


if __name__ == "__main__":
    main()
