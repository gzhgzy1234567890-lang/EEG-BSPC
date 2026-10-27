# -*- coding: utf-8 -*-
"""v10 experiment Q: SEED-IV as the held-out dataset.

SEED-IV was not used to build z_w, to choose its thresholds or to select the
classifier; it enters here only as a test.
"""
import os
import sys
import itertools
import numpy as np
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

CACHE = r"G:\Work_work\math\EEG\local_analysis\cache_seed4_iv"
P = os.path.join(C.OUT, "exp18.txt")
L = []


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


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
                      for p in glob.glob(os.path.join(CACHE, "*.npz"))))
    for sub in subs:
        S = {}
        for sess in (1, 2, 3):
            p = os.path.join(CACHE, "%02d_%d.npz" % (sub, sess))
            if os.path.exists(p):
                z = np.load(p)
                S[sess] = (z["X"].astype(np.float64), z["y"].astype(int))
        for i in sorted(S):
            for j in sorted(S):
                if i != j:
                    out.append((S[i][0], S[i][1], S[j][0], S[j][1]))
    return out


def compute(A, ya, Bt, yb):
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
    gain = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - (Bt.mean(0) - muA)), 1)])
            - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
    return zw, pen, gain


def main():
    say("v10 exp Q: SEED-IV, held out")
    rows = []
    for A, ya, Bt, yb in seed4_pairs():
        zw, pen, gain = compute(A, ya, Bt, yb)
        rows.append((zw, pen, gain))
    z = np.array([r[0] for r in rows])
    p = np.array([r[1] for r in rows])
    g = np.array([r[2] for r in rows])
    say("  cells %d" % len(rows))
    say("  median z_w %.3f   mean penalty %+.4f   mean gain %+.4f" % (np.median(z), p.mean(), g.mean()))
    y = (p < -0.05).astype(int)
    say("  severe-loss cells %d/%d ; AUC of z_w within SEED-IV = %.3f" % (y.sum(), len(y), auc(y, z)))

    # six-dataset exact permutation test
    five_z = [0.298, 4.918, 0.979, 0.230, 0.289]
    five_p = [-0.0139, -0.0722, -0.0287, 0.0000, -0.0147]
    z6 = five_z + [float(np.median(z))]
    p6 = five_p + [float(np.median(p))]
    say("")
    say("  six datasets: z_w %s" % np.round(z6, 3))
    say("               penalty %s" % np.round(p6, 4))
    from scipy.stats import spearmanr
    rho = spearmanr(z6, p6)[0]
    cnt = tot = 0
    for perm in itertools.permutations(range(6)):
        rr = spearmanr(z6, [p6[i] for i in perm])[0]
        tot += 1
        if abs(rr) >= abs(rho) - 1e-12:
            cnt += 1
    say("  spearman rho = %+.3f ; exact two-sided permutation p = %d/%d = %.4f"
        % (rho, cnt, tot, cnt / float(tot)))
    print("done", P)


if __name__ == "__main__":
    main()
