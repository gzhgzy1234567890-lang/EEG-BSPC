# -*- coding: utf-8 -*-
"""v11 -> v12: the threshold fixed on the five development datasets, applied to
the held-out SEED-IV dataset."""
import os
import sys
import glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "external.txt")
L = []
DS = ("2a", "2b", "seed", "ner", "gal")
CACHE4 = r"G:\Work_work\math\EEG\local_analysis\cache_seed4_iv"


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


def zw_pen(A, ya, Bt, yb):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    K = len(classes)
    muA = A.mean(0)
    S = C.score_matrix(clf, A)
    sig = np.maximum(S.std(0), 1e-12)
    W = C.linear_weights(clf, A.shape[1], K)
    proj = W @ muA
    proj = proj - proj.mean()
    zw = float(np.linalg.norm(proj / sig) / np.sqrt(K))
    pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
           - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
    return zw, pen


def seed4():
    out = []
    subs = sorted(set(int(os.path.basename(p).split("_")[0])
                      for p in glob.glob(os.path.join(CACHE4, "*.npz"))))
    for sub in subs:
        S = {}
        for sess in (1, 2, 3):
            p = os.path.join(CACHE4, "%02d_%d.npz" % (sub, sess))
            if os.path.exists(p):
                z = np.load(p)
                S[sess] = (z["X"].astype(np.float64), z["y"].astype(int))
        for i in sorted(S):
            for j in sorted(S):
                if i != j:
                    out.append((S[i][0], S[i][1], S[j][0], S[j][1]))
    return out


def main():
    # development set
    zd, pd = [], []
    for ds in DS:
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            z, pen = zw_pen(A, ya, Bt, yb)
            zd.append(z)
            pd.append(pen)
    zd, pd = np.array(zd), np.array(pd)
    yd = (pd < -0.05).astype(int)
    # pooled Youden threshold on the five development datasets
    cand = np.unique(zd)
    best, thr = -1e9, cand[0]
    for t in cand:
        se = np.mean(zd[yd == 1] > t) if (yd == 1).sum() else 0
        sp = np.mean(zd[yd == 0] <= t) if (yd == 0).sum() else 0
        if se + sp - 1 > best:
            best, thr = se + sp - 1, t
    se = np.mean(zd[yd == 1] > thr)
    sp = np.mean(zd[yd == 0] <= thr)
    pr = (zd[yd == 1] > thr).sum() / max((zd > thr).sum(), 1)
    say("development (five datasets), n=%d, positives=%d" % (len(zd), yd.sum()))
    say("  pooled Youden threshold t* = %.3f ; sens %.3f spec %.3f prec %.3f"
        % (thr, se, sp, pr))

    # held-out SEED-IV
    zs, ps = [], []
    for A, ya, Bt, yb in seed4():
        z, pen = zw_pen(A, ya, Bt, yb)
        zs.append(z)
        ps.append(pen)
    zs, ps = np.array(zs), np.array(ps)
    ys = (ps < -0.05).astype(int)
    tp = np.sum((zs > thr) & (ys == 1))
    fp = np.sum((zs > thr) & (ys == 0))
    fn = np.sum((zs <= thr) & (ys == 1))
    tn = np.sum((zs <= thr) & (ys == 0))
    say("")
    say("held out (SEED-IV), n=%d, positives=%d, threshold fixed above" % (len(zs), ys.sum()))
    say("  sensitivity %.3f  specificity %.3f  precision %.3f  accuracy %.3f"
        % (tp / max(tp + fn, 1), tn / max(tn + fp, 1),
           tp / max(tp + fp, 1), (tp + tn) / float(len(zs))))
    say("  TP %d FP %d FN %d TN %d ; fraction flagged %.3f"
        % (tp, fp, fn, tn, np.mean(zs > thr)))
    print("done", P)


if __name__ == "__main__":
    main()
