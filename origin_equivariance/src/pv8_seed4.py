# -*- coding: utf-8 -*-
"""Build SEED-IV session-level features and run the held-out screen test.

SEED-IV is not used anywhere else in the paper: the statistic, the thresholds
and the classifier were fixed before this dataset was opened.
"""
import os
import re
import glob
import sys
import numpy as np
import scipy.io as sio

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

RAW = r"E:\data\SEED-all\seediv\seediv\eeg_feature_smooth"
CACHE = os.path.join(r"G:\Work_work\math\EEG\local_analysis", "cache_seed4_iv")
OUT = os.path.join(C.OUT, "seediv.txt")

LAB = {
    1: [1, 2, 3, 0, 2, 0, 0, 1, 0, 1, 2, 1, 1, 1, 2, 3, 2, 2, 3, 3, 0, 3, 0, 3],
    2: [2, 1, 3, 0, 0, 2, 0, 2, 3, 3, 2, 3, 2, 0, 1, 1, 2, 1, 0, 3, 0, 1, 3, 1],
    3: [1, 2, 2, 1, 3, 3, 3, 1, 1, 2, 1, 0, 2, 3, 3, 0, 2, 3, 0, 0, 2, 0, 1, 0],
}


def build():
    if not os.path.isdir(CACHE):
        os.makedirs(CACHE)
    for sess in (1, 2, 3):
        for f in sorted(glob.glob(os.path.join(RAW, str(sess), "*.mat"))):
            sub = int(os.path.basename(f).split("_")[0])
            out = os.path.join(CACHE, "%02d_%d.npz" % (sub, sess))
            if os.path.exists(out):
                continue
            m = sio.loadmat(f)
            X, y = [], []
            for k in range(1, 25):
                a = m.get("de_LDS%d" % k)
                if a is None:
                    continue
                a = np.asarray(a, float)                 # (62, T, 5)
                t = a.shape[1]
                X.append(a.transpose(1, 0, 2).reshape(t, -1))
                y += [LAB[sess][k - 1]] * t
            np.savez_compressed(out, X=np.vstack(X).astype(np.float32),
                                y=np.array(y, np.int32))
            print("  built", os.path.basename(out), len(y), flush=True)


def pairs():
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
                if i == j:
                    continue
                out.append(dict(ds="seed4", rep="de", subj="S%02d" % sub,
                                A=S[i][0], ya=S[i][1], B=S[j][0], yb=S[j][1]))
    return out


def run():
    L = []

    def say(s=""):
        L.append(str(s))
        with open(OUT, "w", encoding="utf-8") as f:
            f.write("\n".join(L) + "\n")

    ps = pairs()
    say("SEED-IV held-out test: %d cells, %d subjects" % (len(ps), len(set(p["subj"] for p in ps))))
    zs, pens, gains, tiers = [], [], [], []
    for p in ps:
        A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
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
        zT = float(np.linalg.norm(muA) / np.linalg.norm(np.maximum(A.std(0), 1e-12)))
        g = Bt.mean(0) - A.mean(0)
        none = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)])
        zero = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
        mean = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - g), 1)])
        zs.append(zw)
        tiers.append(zT)
        pens.append(zero - none)
        gains.append(mean - none)
    say("  median z_w %.3f   median z_T %.3f" % (np.median(zs), np.median(tiers)))
    say("  mean penalty (zero - none) %+.4f" % np.mean(pens))
    say("  mean gain (mean - none)    %+.4f" % np.mean(gains))
    say("  fraction of cells with penalty < -0.05: %.3f" % np.mean(np.array(pens) < -0.05))
    print("done", OUT)


if __name__ == "__main__":
    if "--build" in sys.argv:
        build()
    run()
