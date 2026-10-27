# -*- coding: utf-8 -*-
"""Figure 4: per-cell predicted against observed change (LDA)."""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_exp14 import best_thr, ba_thr, D

FIG = os.path.join(HERE, "figs")
COL = {"2a": "#1b5e9c", "2b": "#c0392b", "seed": "#2e7d32", "ner": "#8e44ad",
       "gal": "#e67e22"}
LBL = {"2a": "BCI-2a", "2b": "BCI-2b", "seed": "SEED", "ner": "NER2015",
       "gal": "grasp-and-lift"}
plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8,
                     "legend.fontsize": 6.5, "xtick.labelsize": 7, "ytick.labelsize": 7,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 200, "savefig.bbox": "tight"})


def pairs(ds):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    return ps


def main():
    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.7))
    allh, allo = [], []
    for ds in ("2b", "2a", "gal", "ner", "seed"):
        dh, do = [], []
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            if ds == "2a":
                ma, mb = np.isin(ya, [1, 2]), np.isin(yb, [1, 2])
                A, ya, Bt, yb = A[ma], ya[ma], Bt[mb], yb[mb]
            if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
                continue
            clf = C.make("lda").fit(A, ya)
            if len(np.asarray(clf.classes_)) != 2:
                continue
            classes = np.asarray(clf.classes_)
            w = np.asarray(clf.coef_, float).ravel()
            sA = np.asarray(clf.decision_function(A), float).ravel()
            sig = max(sA.std(), 1e-9)
            muA, muB = A.mean(0), Bt.mean(0)
            s_al = np.asarray(clf.decision_function(Bt - muB + muA), float).ravel()
            s_ze = np.asarray(clf.decision_function(Bt - muB), float).ravel()
            ts = best_thr(s_al, yb, classes) / sig
            sh = float(w @ muA) / sig
            ba = ba_thr(s_al, yb, classes, 0.0)
            c = norm.ppf(np.clip(ba, 0.01, 0.99))
            dh.append(D(c, ts - sh) - D(c, ts))
            do.append(ba_thr(s_ze, yb, classes, 0.0) - ba)
        if not dh:
            continue
        ax[0].scatter(dh, do, s=5, color=COL[ds], alpha=0.6, label=LBL[ds], lw=0)
        allh += dh
        allo += do
    ax[0].plot([-0.4, 0.2], [-0.4, 0.2], "k:", lw=0.7)
    ax[0].axhline(0, color="k", lw=0.4)
    ax[0].axvline(0, color="k", lw=0.4)
    ax[0].set_xlabel("predicted change (Equation 4)")
    ax[0].set_ylabel("observed change")
    ax[0].set_title("(a) per cell, LDA, binary cells", loc="left")
    ax[0].legend(frameon=False, markerscale=2, loc="upper left")
    ax[0].set_xlim(-0.45, 0.25)
    ax[0].set_ylim(-0.45, 0.25)

    allh = np.array(allh)
    allo = np.array(allo)
    ax[1].hist([allh - allo], bins=40, color="#555555")
    ax[1].set_xlabel("prediction error")
    ax[1].set_ylabel("cells")
    ax[1].set_title("(b) MAE %.3f" % np.mean(np.abs(allh - allo)), loc="left")
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIG, "fig4.%s" % ext))
    print("fig4 done", len(allh), "cells")


if __name__ == "__main__":
    main()
