# -*- coding: utf-8 -*-
"""v13 -> v14: z_w with the scale taken from the *centred* scores.

The referee's counter-example: adding a class-common linear function a'x to
every score leaves all predictions unchanged but changes the per-class score
SDs, hence the uncentred z_w.  With sigma taken from P S, the centred scores,
both the numerator and the scale are invariant.  This script recomputes every
number the screen rests on with that definition, checks the invariance under
the referee's transformation, and re-runs the held-out test.
"""
import os
import sys
import glob
import itertools
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "zw_centred.txt")
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


def zw_centred(clf, A, classes):
    K = len(classes)
    S = C.score_matrix(clf, A)
    Sc = S - S.mean(1, keepdims=True)
    sig = np.maximum(Sc.std(0), 1e-12)
    W = C.linear_weights(clf, A.shape[1], K)
    proj = W @ A.mean(0)
    proj = proj - proj.mean()
    return float(np.linalg.norm(proj / sig) / np.sqrt(K))


def cell(ds, A, ya, Bt, yb):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    z = zw_centred(clf, A, classes)
    pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
           - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
    return z, pen, clf, classes


def auc(y, s):
    y = np.asarray(y, int)
    s = np.asarray(s, float)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    allv = np.concatenate([pos, neg])
    r = np.argsort(np.argsort(allv)) + 1.0
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)))


def seed4_pairs():
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
    say("v14: z_w with the scale from the centred scores")
    say("")

    # invariance under the referee's transformation
    A, ya = pairs("2b")[0]["A"], pairs("2b")[0]["ya"]
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    z0 = zw_centred(clf, A, classes)
    S = C.score_matrix(clf, A)
    # identical decision function, different score representation: s -> s + a'x
    # emulated by adding a constant to the score matrix columns is not enough;
    # instead transform the weights: W' = W + 1 a', equivalently scores scaled
    # in a class-common way.  We emulate with a'x = 0.5 * column of x.
    a = 0.5 * np.eye(A.shape[1])[:, 0]
    Sp = S + (A @ a)[:, None]
    sc = Sp - Sp.mean(1, keepdims=True)
    sig = np.maximum(sc.std(0), 1e-12)
    W = C.linear_weights(clf, A.shape[1], len(classes))
    proj = W @ A.mean(0)
    proj = proj - proj.mean()
    z1 = float(np.linalg.norm(proj / sig) / np.sqrt(len(classes)))
    say("  invariance under a class-common linear score term: |z'-z| = %.2e" % abs(z1 - z0))

    # development cells
    rows = []
    for ds in DS:
        for p in pairs(ds):
            z, pen, _, _ = cell(ds, p["A"], p["ya"], p["B"], p["yb"])
            rows.append((ds, p["rep"], z, pen))
    ds = np.array([r[0] for r in rows])
    rep = np.array([r[1] for r in rows])
    zw = np.array([r[2] for r in rows])
    pen = np.array([r[3] for r in rows])
    y = (pen < -0.05).astype(int)
    say("")
    say("  development cells %d, positives %d" % (len(y), y.sum()))
    say("  AUC %.3f" % auc(y, zw))
    units = sorted(set(zip(ds, rep)))
    uz = np.array([np.median(zw[(ds == a) & (rep == b)]) for a, b in units])
    up = np.array([np.median(pen[(ds == a) & (rep == b)]) for a, b in units])
    say("  unit-level spearman(z_w, penalty) = %+.3f" % stats.spearmanr(uz, up)[0])
    dz = [np.median(zw[ds == d]) for d in DS]
    dp = [np.median(pen[ds == d]) for d in DS]
    say("  dataset medians z_w %s" % np.round(dz, 3))
    say("  dataset medians pen %s" % np.round(dp, 4))
    say("  five-dataset spearman %+.3f" % stats.spearmanr(dz, dp)[0])

    # SEED-IV held out
    sz, sp = [], []
    for A_, ya_, B_, yb_ in seed4_pairs():
        z, pen_, _, _ = cell("seed4", A_, ya_, B_, yb_)
        sz.append(z)
        sp.append(pen_)
    sz, sp = np.array(sz), np.array(sp)
    y4 = (sp < -0.05).astype(int)
    say("")
    say("  SEED-IV: n=%d, median z_w %.3f, median penalty %.4f, AUC %.3f"
        % (len(sz), np.median(sz), np.median(sp), auc(y4, sz)))

    # six datasets
    z6 = dz + [float(np.median(sz))]
    p6 = dp + [float(np.median(sp))]
    rho = stats.spearmanr(z6, p6)[0]
    cnt = tot = 0
    for perm in itertools.permutations(range(6)):
        rr = stats.spearmanr(z6, [p6[i] for i in perm])[0]
        tot += 1
        if abs(rr) >= abs(rho) - 1e-12:
            cnt += 1
    say("  six-dataset spearman %+.3f, exact p = %d/%d = %.4f" % (rho, cnt, tot, cnt / float(tot)))

    # external threshold from the five development datasets
    cand = np.unique(zw)
    best, thr = -1e9, cand[0]
    for t in cand:
        se = np.mean(zw[y == 1] > t)
        spc = np.mean(zw[y == 0] <= t)
        if se + spc - 1 > best:
            best, thr = se + spc - 1, t
    tp = np.sum((sz > thr) & (y4 == 1))
    fp = np.sum((sz > thr) & (y4 == 0))
    fn = np.sum((sz <= thr) & (y4 == 1))
    tn = np.sum((sz <= thr) & (y4 == 0))
    say("  external threshold %.3f -> SEED-IV sens %.3f spec %.3f prec %.3f"
        % (thr, tp / max(tp + fn, 1), tn / max(tn + fp, 1), tp / max(tp + fp, 1)))
    print("done", P)


if __name__ == "__main__":
    main()
