# -*- coding: utf-8 -*-
"""Fig. 2 with the held-out point."""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = r"G:\Work_work\math\EEG\paper_v8"
sys.path.insert(0, HERE)
import pv8_common as C

plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8,
                     "legend.fontsize": 6.5, "figure.dpi": 200, "savefig.bbox": "tight",
                     "axes.spines.top": False, "axes.spines.right": False})
z = np.load(os.path.join(C.OUT, "screen.npz"))
ds = np.array([str(x) for x in z["ds"]])
rep = np.array([str(x) for x in z["rep"]])
zw = z["rz"]
pen = z["pen"]
fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
for u in sorted(set(zip(ds, rep))):
    m = (ds == u[0]) & (rep == u[1])
    ax[0].scatter(np.median(zw[m]), np.median(pen[m]), s=np.sqrt(m.sum()) * 6 + 8,
                  color="#888888", edgecolor="k", lw=0.3)
ax[0].scatter(1.00, -0.070, s=150, marker="*", color="#c0392b", edgecolor="k",
              lw=0.4, label="SEED-IV (held out)", zorder=5)
ax[0].axhline(0, color="k", lw=0.5, ls=":")
ax[0].set_xlabel(r"source-only statistic $z_w$")
ax[0].set_ylabel("penalty of the one-sided pipeline")
ax[0].set_title("(a) unit medians and the held-out point", loc="left")
ax[0].legend(frameon=False, loc="lower left")
ax[1].scatter(np.log10(np.maximum(zw, 1e-2)), pen, s=3, color="#888888", alpha=0.5)
ax[1].scatter(0.0, -0.070, s=90, marker="*", color="#c0392b", edgecolor="k",
              lw=0.4, zorder=5)
ax[1].axhline(0, color="k", lw=0.5, ls=":")
ax[1].set_xlabel(r"$\log_{10} z_w$")
ax[1].set_ylabel("penalty")
ax[1].set_title("(b) every development cell", loc="left")
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(HERE, "figs", "fig2.%s" % ext))
print("fig2 redone")
