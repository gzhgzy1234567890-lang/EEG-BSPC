# -*- coding: utf-8 -*-
"""Fig. 2 with the corrected (centred-scale) statistic, and the cache it needs."""
import os
import sys
import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

CACHE4 = r"G:\Work_work\math\EEG\local_analysis\cache_seed4_iv"
OUT = os.path.join(C.OUT, "screen_centred.npz")


def pairs(ds):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    return ps


def zw(A, ya, clf, classes):
    K = len(classes)
    S = C.score_matrix(clf, A)
    Sc = S - S.mean(1, keepdims=True)
    sig = np.maximum(Sc.std(0), 1e-12)
    W = C.linear_weights(clf, A.shape[1], K)
    proj = W @ A.mean(0)
    proj = proj - proj.mean()
    return float(np.linalg.norm(proj / sig) / np.sqrt(K))


def collect():
    rows = []
    for ds in ("2a", "2b", "seed", "ner", "gal"):
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            z = zw(A, ya, clf, classes)
            pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
                   - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
            rows.append((ds, p["rep"], z, pen))
    # SEED-IV
    subs = sorted(set(int(os.path.basename(p).split("_")[0])
                      for p in glob.glob(os.path.join(CACHE4, "*.npz"))))
    for sub in subs:
        S = {}
        for sess in (1, 2, 3):
            f = os.path.join(CACHE4, "%02d_%d.npz" % (sub, sess))
            if os.path.exists(f):
                z = np.load(f)
                S[sess] = (z["X"].astype(np.float64), z["y"].astype(int))
        for i in sorted(S):
            for j in sorted(S):
                if i == j:
                    continue
                A, ya = S[i]
                Bt, yb = S[j]
                clf = C.make("lda").fit(A, ya)
                classes = np.asarray(clf.classes_)
                z = zw(A, ya, clf, classes)
                pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
                       - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
                rows.append(("seed4", "de", z, pen))
    return rows


def main():
    rows = collect()
    ds = np.array([r[0] for r in rows])
    rep = np.array([r[1] for r in rows])
    z = np.array([r[2] for r in rows])
    pen = np.array([r[3] for r in rows])
    np.savez(OUT, ds=ds, rep=rep, zw=z, pen=pen)
    dev = ds != "seed4"
    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
    for u in sorted(set(zip(ds[dev], rep[dev]))):
        m = (ds == u[0]) & (rep == u[1])
        ax[0].scatter(np.median(z[m]), np.median(pen[m]), s=np.sqrt(m.sum()) * 6 + 8,
                      color="#888888", edgecolor="k", lw=0.3)
    m4 = ds == "seed4"
    ax[0].scatter(np.median(z[m4]), np.median(pen[m4]), s=150, marker="*",
                  color="#c0392b", edgecolor="k", lw=0.4,
                  label="SEED-IV (held out)", zorder=5)
    ax[0].axhline(0, color="k", lw=0.5, ls=":")
    ax[0].set_xscale("log")
    ax[0].set_xlabel(r"source-only statistic $z_w$")
    ax[0].set_ylabel("penalty of the one-sided pipeline")
    ax[0].set_title("(a) unit medians, held-out star", loc="left")
    ax[0].legend(frameon=False, loc="upper right")
    ax[1].scatter(np.log10(np.maximum(z[dev], 1e-2)), pen[dev], s=3,
                  color="#888888", alpha=0.5)
    ax[1].scatter(np.log10(np.maximum(z[m4], 1e-2)), pen[m4], s=6, marker="*",
                  color="#c0392b", alpha=0.8)
    ax[1].axhline(0, color="k", lw=0.5, ls=":")
    ax[1].set_xlabel(r"$\log_{10} z_w$")
    ax[1].set_ylabel("penalty")
    ax[1].set_title("(b) every cell", loc="left")
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(HERE, "figs", "fig2.%s" % ext))
    print("fig2 redone; dev cells", int(dev.sum()), "held out", int(m4.sum()))


if __name__ == "__main__":
    main()
