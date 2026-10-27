# -*- coding: utf-8 -*-
"""Cluster-bootstrap interval for the source-only unit-level correlation."""
import os
import sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "sourceonly_ci.txt")
L = []
DS = ("2a", "2b", "seed", "ner", "gal")
TARGET_INFORMED = ("euc_ea", "tan")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def pairs(ds):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    return [p for p in ps if p["rep"] not in TARGET_INFORMED]


def main():
    rows = []
    for ds in DS:
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
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
            rows.append((ds, p["rep"], z, pen))
    ds = np.array([r[0] for r in rows])
    rep = np.array([r[1] for r in rows])
    z = np.array([r[2] for r in rows])
    pen = np.array([r[3] for r in rows])
    units = sorted(set(zip(ds, rep)))
    uz = np.array([np.median(z[(ds == a) & (rep == b)]) for a, b in units])
    up = np.array([np.median(pen[(ds == a) & (rep == b)]) for a, b in units])
    uds = np.array([a for a, b in units])
    say("source-only units: %d, cells %d" % (len(units), len(rows)))
    say("  rho = %+.3f" % stats.spearmanr(uz, up)[0])
    rs = np.random.RandomState(0)
    out = []
    for _ in range(5000):
        pick = rs.choice(DS, len(DS), replace=True)
        idx = np.concatenate([np.where(uds == d)[0] for d in pick])
        if len(idx) < 4 or np.std(uz[idx]) == 0 or np.std(up[idx]) == 0:
            continue
        out.append(stats.spearmanr(uz[idx], up[idx])[0])
    out = np.array(out)
    say("  cluster bootstrap (datasets): median %+.3f 95%% CI [%+.3f, %+.3f], n=%d"
        % (np.median(out), np.percentile(out, 2.5), np.percentile(out, 97.5), len(out)))
    print("done", P)


if __name__ == "__main__":
    main()
