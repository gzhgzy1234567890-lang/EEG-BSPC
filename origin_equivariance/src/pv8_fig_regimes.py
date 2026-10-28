# -*- coding: utf-8 -*-
"""v58: three-panel failure-regime figure, parsed from results/phase30.txt."""
import io
import os
import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "results", "phase30.txt")
FIG = os.path.join(HERE, "figs")
TXT = io.open(SRC, encoding="utf-8").read().split("\n")

ROW = re.compile(r"^\s{2}(.+?)\s{2,}([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+\|\s+([+-][0-9.]+)\s+\[([+-][0-9.]+),([+-][0-9.]+)\]")
A = {}
B = {}
C = {}
for line in TXT:
    m = ROW.match(line)
    if not m:
        continue
    label = m.group(1).strip()
    vals = [float(m.group(i)) for i in range(2, 8)]   # none cum eq9 loo fwd adwin
    d, lo, hi = float(m.group(8)), float(m.group(9)), float(m.group(10))
    rec = dict(none=vals[0], cum=vals[1], eq9=vals[2], loo=vals[3], adwin=vals[5],
               d=d, lo=lo, hi=hi, label=label)
    mm = re.match(r"a=([\d.]+) v=([\d.]+)", label)
    if mm:
        A[(float(mm.group(1)), float(mm.group(2)))] = rec
        continue
    mm = re.match(r"jumps every (\d+)", label)
    if mm:
        B[int(mm.group(1))] = rec
        continue
    C[label] = rec

print("A cells", len(A), "B", len(B), "C", len(C))

fig, ax = plt.subplots(1, 3, figsize=(10.2, 3.1))

av = sorted({k[0] for k in A})
vv = sorted({k[1] for k in A})
M = np.full((len(av), len(vv)), np.nan)
cross = np.zeros_like(M, bool)
for i, a in enumerate(av):
    for j, v in enumerate(vv):
        r = A.get((a, v))
        if r:
            M[i, j] = r["d"]
            cross[i, j] = (r["lo"] < 0 < r["hi"])
im = ax[0].imshow(M, cmap="RdBu_r", vmin=-0.01, vmax=0.01, origin="lower", aspect="auto")
for (i, j), val in np.ndenumerate(M):
    if np.isnan(val):
        continue
    ax[0].text(j, i, ("%.3f" % val) + ("*" if cross[i, j] else ""),
               ha="center", va="center", fontsize=6)
ax[0].set_xticks(range(len(vv)))
ax[0].set_xticklabels([("%.1f" % v) for v in vv], fontsize=7)
ax[0].set_yticks(range(len(av)))
ax[0].set_yticklabels([("%.1f" % a) for a in av], fontsize=7)
ax[0].set_xlabel("drift $v$", fontsize=8)
ax[0].set_ylabel("constant offset $a$", fontsize=8)
ax[0].set_title("(a) predictive $-$ variance ratio", loc="left", fontsize=8)
fig.colorbar(im, ax=ax[0], fraction=0.046, pad=0.03).ax.tick_params(labelsize=6)

labels = ["cum", "eq9", "loo", "adwin"]
x = np.arange(len(B))
w = 0.2
for k, meth in enumerate(labels):
    vals = [B[p][meth] - B[p]["none"] for p in sorted(B)]
    ax[1].bar(x + (k - 1.5) * w, vals, w, label=meth)
ax[1].set_xticks(x)
ax[1].set_xticklabels(["every %d blocks" % p for p in sorted(B)], fontsize=7)
ax[1].axhline(0, color="k", lw=0.6)
ax[1].set_ylabel(r"$\Delta$BA vs no correction", fontsize=8)
ax[1].set_title("(b) step changes", loc="left", fontsize=8)
ax[1].legend(frameon=False, fontsize=6)

names = sorted(C)
x = np.arange(len(names))
for k, meth in enumerate(labels):
    vals = [C[n][meth] - C[n]["none"] for n in names]
    ax[2].bar(x + (k - 1.5) * w, vals, w, label=meth)
ax[2].set_xticks(x)
ax[2].set_xticklabels([n.replace("priors", "priors\n").replace("blk ", "block\n") for n in names],
                      fontsize=6, rotation=0)
ax[2].axhline(0, color="k", lw=0.6)
ax[2].set_ylabel(r"$\Delta$BA vs no correction", fontsize=8)
ax[2].set_title("(c) class-prior change", loc="left", fontsize=8)
ax[2].legend(frameon=False, fontsize=6)

for a in ax:
    a.tick_params(labelsize=7)
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(FIG, "fig_regimes.%s" % ext), dpi=300)
print("written", os.path.join(FIG, "fig_regimes.png"))
