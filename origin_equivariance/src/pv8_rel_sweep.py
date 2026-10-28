# -*- coding: utf-8 -*-
"""Block length sensitivity of the reliability-weighted estimator (Eq. 15)."""
import glob
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores

P = os.path.join(C.OUT, "rel_sweep.txt")
L = []
CACHE4 = r"G:\Work_work\math\EEG\local_analysis\cache_seed4_iv"
K0 = {"2b": 20, "2a": 20, "gal": 20, "ner": 20, "seed": 50}
MS = (15, 25, 50)
SOURCE_ONLY = ("euc", "csp", "de", "Ftime", "pow")
FAMILY = {"MI": ("2a", "2b"), "emotion": ("seed",), "ErrP": ("ner",), "movement": ("gal",)}


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


def run(A, ya, Bt, yb, k0, m):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    K = len(classes)
    W = C.linear_weights(clf, A.shape[1], K)
    muA = A.mean(0)
    zA = W @ muA
    n = len(yb)
    S0 = scores(Bt, W, np.asarray(clf.intercept_, float).ravel(), K)
    blocks = [(t, min(t + m, n)) for t in range(k0, n, m)]
    zhat = [(Bt[a:b].mean(0)) @ W.T for a, b in blocks]
    S = S0.copy()
    for i, (a, b) in enumerate(blocks):
        if i == 0:
            continue
        Z = np.array(zhat[:i])
        zbar = Z.mean(0)
        if len(Z) >= 2:
            vb = Z.var(0).sum()
            lam = float(np.clip((zbar @ zbar) / (zbar @ zbar + K * vb / len(Z) + 1e-12), 0, 1))
        else:
            lam = 0.5
        S[a:b] = S0[a:b] - lam * zbar[None, :] + lam * zA[None, :]
    ba = C.ba(yb[k0:], classes[np.argmax(S[k0:], 1)])
    ba0 = C.ba(yb[k0:], classes[np.argmax(S0[k0:], 1)])
    return ba - ba0


def main():
    say("v33: block length sweep of the reliability-weighted estimator")
    gains = {}
    for ds in ("2b", "2a", "seed", "gal", "ner"):
        for m in MS:
            g = [run(p["A"], p["ya"], p["B"], p["yb"], K0[ds], m) for p in pairs(ds)]
            gains[(ds, m)] = float(np.mean(g))
        say("  %-5s " % ds + " ".join("m=%d %+.4f" % (m, gains[(ds, m)]) for m in MS))
    subs = sorted(set(int(os.path.basename(f).split("_")[0])
                      for f in glob.glob(os.path.join(CACHE4, "*.npz"))))
    for m in MS:
        g = []
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
                        g.append(run(S[i][0], S[i][1], S[j][0], S[j][1], 50, m))
        gains[("seed4", m)] = float(np.mean(g))
    say("  seed4 " + " ".join("m=%d %+.4f" % (m, gains[("seed4", m)]) for m in MS))
    say("")
    say("family LODO over m")
    for held, members in FAMILY.items():
        train = [d for d in ("2b", "2a", "seed", "gal", "ner") if d not in members]
        best = max(MS, key=lambda m: np.mean([gains[(d, m)] for d in train]))
        say("  hold %-9s -> m=%d  train %+.4f  held %+.4f"
            % (held, best, np.mean([gains[(d, best)] for d in train]),
               np.mean([gains[(d, best)] for d in members])))
    print("done", P)


if __name__ == "__main__":
    main()
