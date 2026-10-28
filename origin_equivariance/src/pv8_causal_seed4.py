# -*- coding: utf-8 -*-
"""Held-out validation of the causal estimators on SEED-IV."""
import glob
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores, TAU

CACHE4 = r"G:\Work_work\math\EEG\local_analysis\cache_seed4_iv"
P = os.path.join(C.OUT, "causal_seed4.txt")
L = []
K = 50


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    subs = sorted(set(int(os.path.basename(f).split("_")[0])
                      for f in glob.glob(os.path.join(CACHE4, "*.npz"))))
    rows = []
    for sub in subs:
        S = {}
        for sess in (1, 2, 3):
            f = os.path.join(CACHE4, "%02d_%d.npz" % (sub, sess))
            if os.path.exists(f):
                d = np.load(f)
                S[sess] = (d["X"].astype(np.float64), d["y"].astype(int))
        for i in sorted(S):
            for j in sorted(S):
                if i == j:
                    continue
                A, ya = S[i]
                Bt, yb = S[j]
                clf = C.make("lda").fit(A, ya)
                classes = np.asarray(clf.classes_)
                n = len(yb)
                W = C.linear_weights(clf, A.shape[1], len(classes))
                b = np.asarray(clf.intercept_, float).ravel()
                muA = A.mean(0)
                T = np.arange(K, n)
                out = {}
                out["none"] = C.ba(yb[T], classes[np.argmax(scores(Bt[T], W, b, len(classes)), 1)])
                out["batch"] = C.ba(yb[T], classes[np.argmax(
                    scores(Bt[T] - Bt.mean(0) + muA, W, b, len(classes)), 1)])
                cs = np.cumsum(Bt, axis=0)
                cnt = np.arange(1, n + 1)[:, None]
                mu_cum = cs / cnt
                mu_prev = np.vstack([np.zeros((1, Bt.shape[1])), mu_cum[:-1]])
                out["cum"] = C.ba(yb[T], classes[np.argmax(
                    scores(Bt[T] - mu_prev[T] + muA, W, b, len(classes)), 1)])
                neff = np.arange(n)[:, None].astype(float)
                lam = neff / (neff + TAU)
                out["usc"] = C.ba(yb[T], classes[np.argmax(
                    scores(Bt[T] - mu_prev[T] * lam[T] + lam[T] * muA, W, b, len(classes)), 1)])
                out["cum_1s"] = C.ba(yb[T], classes[np.argmax(
                    scores(Bt[T] - mu_prev[T], W, b, len(classes)), 1)])
                rows.append((sub, out))
    keys = ["none", "batch", "cum", "usc", "cum_1s"]
    say("SEED-IV held out, k=%d, %d cells, %d subjects" % (K, len(rows), len(set(s for s, _ in rows))))
    say("  " + "  ".join("%-9s" % k for k in keys))
    say("  " + "  ".join("%-9.4f" % np.mean([r[k] for _, r in rows]) for k in keys))
    for m in ("batch", "cum", "usc", "cum_1s"):
        by = {}
        for s, r in rows:
            by.setdefault(s, []).append(r[m] - r["none"])
        d = np.array([np.mean(v) for v in by.values()])
        rs = np.random.RandomState(0)
        bs = np.array([np.mean(rs.choice(d, len(d))) for _ in range(4000)])
        say("  %-8s %+.4f  95%% CI [%+.4f, %+.4f]" % (m, d.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)))
    print("done", P)


if __name__ == "__main__":
    main()
