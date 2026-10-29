# -*- coding: utf-8 -*-
"""v8 figures.

Fig 1  origin sweep: damage of the one-sided pipeline against z_T, collapse
       probability, and the exact flatness of the two invariant pipelines.
Fig 2  the screen: representation-level z_T against the fraction of the
       cross-session gap that the correction recovers.
Fig 3  variants of the correction, and calibration.

Output: figs/fig1.pdf, fig1.png, fig2.*, fig3.*
"""
import os
import sys
import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

FIG = os.path.join(HERE, "figs")
if not os.path.isdir(FIG):
    os.makedirs(FIG)

COL = {"2a": "#1b5e9c", "2b": "#c0392b", "seed": "#2e7d32", "ner": "#8e44ad",
       "gal": "#e67e22"}
LBL = {"2a": "BCI-2a", "2b": "BCI-2b", "seed": "SEED", "ner": "NER2015",
       "gal": "grasp-and-lift"}
plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8,
                     "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 200, "savefig.dpi": 300, "savefig.bbox": "tight"})


def load_sweep():
    out = {}
    for f in sorted(glob.glob(os.path.join(C.OUT, "exp4_*.npz"))):
        nm = os.path.basename(f).replace("exp4_", "").replace(".npz", "")
        z = np.load(f)
        per = len(z["a"]) // len(nm.split(","))
        for i, d in enumerate(nm.split(",")):
            if d in out:
                continue
            s = slice(i * per, (i + 1) * per)
            out[d] = {k: z[k][s] for k in ("a", "n", "zT", "none", "zero", "align", "coll")}
    return out


def fig1():
    sw = load_sweep()
    order = ["gal", "ner", "2a", "2b", "seed"]
    fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.35))
    for d in order:
        if d not in sw:
            continue
        s = sw[d]
        zt = np.maximum(s["zT"], 1e-2)
        dz = s["zero"] - s["zero"][0]
        ax[0].semilogx(zt, dz, "o-", ms=3, lw=1.0, color=COL[d], label=LBL[d])
        ax[1].semilogx(zt, s["coll"], "o-", ms=3, lw=1.0, color=COL[d])
    ax[0].axhline(0, color="k", lw=0.5, ls=":")
    ax[0].set_xlabel(r"origin offset $z_T$ (source-session SD units)")
    ax[0].set_ylabel(r"$\Delta$ balanced accuracy (one-sided)")
    ax[0].set_title("(a) the one-sided pipeline slides", loc="left")
    ax[0].legend(frameon=False, loc="lower left")
    ax[1].set_xlabel(r"$z_T$")
    ax[1].set_ylabel("fraction of cells at exact chance")
    ax[1].set_title("(b) and stops", loc="left")
    ax[1].set_ylim(-0.03, 1.03)

    # (c) flatness of the two invariant pipelines
    w = 0.35
    xs, ys = [], []
    for j, d in enumerate(order):
        if d not in sw:
            continue
        s = sw[d]
        dn = np.abs(s["none"] - s["none"][0]).max()
        da = np.abs(s["align"] - s["align"][0]).max()
        xs.append(j)
        ys.append((dn, da))
    ys = np.array(ys)
    ax[2].bar(np.array(xs) - w / 2, np.maximum(ys[:, 0], 1e-12), w, color="#555555",
              label="no correction")
    ax[2].bar(np.array(xs) + w / 2, np.maximum(ys[:, 1], 1e-12), w, color="#1b5e9c",
              label="two-sided")
    ax[2].set_yscale("log")
    ax[2].set_ylim(1e-14, 1e-1)
    ax[2].set_xticks(xs)
    ax[2].set_xticklabels([LBL[d] for d in order], rotation=30, ha="right")
    ax[2].set_ylabel("max |change| over the sweep")
    ax[2].set_title("(c) the other two are exactly flat", loc="left")
    ax[2].legend(frameon=False, loc="upper left")
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIG, "fig1.%s" % ext))
    plt.close(fig)


def fig2():
    z = np.load(os.path.join(C.OUT, "screen.npz"))
    ds = np.array([str(s) for s in z["ds"]])
    rep = np.array([str(s) for s in z["rep"]])
    zT, rz, pen, gain = z["z"], z["rz"], z["pen"], z["gain"]
    units = []
    for u in sorted(set(zip(ds, rep))):
        m = (ds == u[0]) & (rep == u[1])
        units.append((u[0], u[1], int(m.sum()), np.median(zT[m]), np.median(rz[m]),
                      np.median(pen[m]), np.median(gain[m])))
    fig, ax = plt.subplots(1, 3, figsize=(7.4, 2.45))
    for u in units:
        ax[0].scatter(u[3], u[5], s=np.sqrt(u[2]) * 6 + 8, color=COL[u[0]],
                      edgecolor="k", lw=0.4)
        if abs(u[5]) > 0.05 or u[3] > 5:
            ax[0].annotate("%s %s" % (LBL[u[0]], u[1]), (u[3], u[5]), fontsize=5.4,
                           xytext=(4, 2), textcoords="offset points")
    ax[0].annotate("six low-origin units\n(penalty within ±0.024)", (0.30, 0.012),
                   fontsize=5.2, ha="center", va="bottom")
    ax[0].axhline(0, color="k", lw=0.5, ls=":")
    ax[0].set_xscale("log")
    ax[0].set_xlabel(r"origin distance $z_T$")
    ax[0].set_ylabel("penalty of the one-sided pipeline")
    ax[0].set_title("(a) the screen, per unit", loc="left")

    for d in ("2a", "2b", "seed", "ner", "gal"):
        m = ds == d
        ax[1].scatter(np.log10(np.maximum(zT[m], 1e-2)), pen[m], s=3,
                      color=COL[d], alpha=0.55, label=LBL[d])
    ax[1].axhline(0, color="k", lw=0.5, ls=":")
    ax[1].set_xlabel(r"$\log_{10} z_T$")
    ax[1].set_ylabel("penalty")
    ax[1].set_title("(b) the same relation, per cell", loc="left")
    ax[1].legend(frameon=False, markerscale=2, loc="lower left", ncol=2, fontsize=6)

    for u in units:
        ax[2].scatter(u[3], u[4], s=np.sqrt(u[2]) * 6 + 8, color=COL[u[0]],
                      edgecolor="k", lw=0.4)
    ax[2].set_xscale("log")
    ax[2].set_yscale("log")
    ax[2].set_ylim(0.12, 60)
    ax[2].set_xlabel(r"origin distance $z_T$")
    ax[2].set_ylabel(r"induced displacement $\rho$")
    ax[2].set_title("(c) the feature statistic tracks the mediator", loc="left")
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIG, "fig2.%s" % ext))
    plt.close(fig)


def fig3():
    z = np.load(os.path.join(C.OUT, "final_2.npz"))
    ds = z["ds"]
    conds = ("none", "zero", "align")
    order = ["2a", "2b", "seed", "ner", "gal"]
    fig, ax = plt.subplots(1, 2, figsize=(6.6, 2.4))
    w = 0.26
    for j, c in enumerate(conds):
        vals = [z[c][ds == d].mean() for d in order]
        ax[0].bar(np.arange(len(order)) + (j - 1) * w, vals, w,
                  label={"none": "no correction", "zero": "one-sided",
                         "align": "two-sided"}[c],
                  color={"none": "#888888", "zero": "#c0392b", "align": "#1b5e9c"}[c])
    ax[0].set_xticks(np.arange(len(order)))
    ax[0].set_xticklabels([LBL[d] for d in order], rotation=30, ha="right")
    ax[0].set_ylabel("balanced accuracy")
    ax[0].set_title("(a) five datasets of cells", loc="left")
    ax[0].legend(frameon=False, ncol=3, loc="upper left")
    ax[0].set_ylim(0.3, 0.85)

    # per-dataset gain at the subject level
    gains = []
    for d in order:
        m = ds == d
        subs = sorted(set(z["subj"][m]))
        g = [np.mean(z["gain"][m & (z["subj"] == s)]) for s in subs]
        gains.append(np.array(g))
    bp = ax[1].boxplot(gains, widths=0.55, patch_artist=True, showfliers=False,
                       medianprops=dict(color="k", lw=1))
    for patch, d in zip(bp["boxes"], order):
        patch.set_facecolor(COL[d])
        patch.set_alpha(0.55)
    ax[1].axhline(0, color="k", lw=0.6, ls=":")
    ax[1].set_xticklabels([LBL[d] for d in order], rotation=30, ha="right")
    ax[1].set_ylabel("gain of two-sided over none")
    ax[1].set_title("(b) per subject", loc="left")
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIG, "fig3.%s" % ext))
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    print("fig1 done")
    fig2()
    print("fig2 done")
    fig3()
    print("fig3 done")
