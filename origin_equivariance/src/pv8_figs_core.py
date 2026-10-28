# -*- coding: utf-8 -*-
"""v53: the two core figures, drawn from results/master_cells.csv only."""
import io
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "results", "master_cells.csv")
FIG = os.path.join(HERE, "figs")
LAMS = (0.0, 0.1, 0.25, 0.5, 0.75, 1.0)
ORDER = ("gal", "seed", "2b", "2a", "ner")
LABEL = {"gal": "grasp-and-lift", "seed": "SEED", "2b": "BCI-IV-2b",
         "2a": "BCI-IV-2a", "ner": "NER2015"}
COLOR = {"gal": "#c0392b", "seed": "#2e86c1", "2b": "#27ae60",
         "2a": "#8e44ad", "ner": "#7f8c8d"}


def load():
    rows = []
    with io.open(CSV, encoding="utf-8") as f:
        head = f.readline().strip().split(",")
        for line in f:
            v = line.strip().split(",")
            if len(v) != len(head):
                continue
            r = dict(zip(head, v))
            for k in head[3:]:
                r[k] = float(r[k])
            rows.append(r)
    return rows


def boot(v, reps=4000):
    v = np.asarray(v, float)
    rs = np.random.RandomState(0)
    bs = np.array([np.mean(rs.choice(v, len(v))) for _ in range(reps)])
    return v.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)


def fig_lambda(rows):
    fig, ax = plt.subplots(1, 2, figsize=(7.6, 3.1))
    for ds in ORDER:
        sel = [r for r in rows if r["ds"] == ds]
        by = {}
        for r in sel:
            by.setdefault(r["subj"], []).append(r)
        mu, lo, hi = [], [], []
        for l in LAMS:
            means = [np.mean([r["ba%.2f" % l] for r in v]) for v in by.values()]
            m, a, b = boot(means)
            mu.append(m); lo.append(a); hi.append(b)
        ax[0].plot(LAMS, mu, "-o", ms=3, color=COLOR[ds], label=LABEL[ds], lw=1.6)
        ax[0].fill_between(LAMS, lo, hi, color=COLOR[ds], alpha=0.15, lw=0)
        base = np.array(mu)[0]
        ax[1].plot(LAMS, np.array(mu) - base, "-o", ms=3, color=COLOR[ds],
                   label=LABEL[ds], lw=1.6)
        ax[1].fill_between(LAMS, np.array(lo) - base, np.array(hi) - base,
                           color=COLOR[ds], alpha=0.15, lw=0)
    ax[0].set_xlabel(r"correction strength $\lambda$")
    ax[0].set_ylabel("balanced accuracy")
    ax[0].set_title("(a) absolute", loc="left", fontsize=9)
    ax[1].axhline(0, color="k", lw=0.6)
    ax[1].set_xlabel(r"correction strength $\lambda$")
    ax[1].set_ylabel(r"$\Delta$BA vs $\lambda=0$")
    ax[1].set_title("(b) change from no correction", loc="left", fontsize=9)
    ax[0].legend(frameon=False, fontsize=7)
    for a in ax:
        a.tick_params(labelsize=7)
        a.set_xticks(list(LAMS))
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIG, "fig_lambda.%s" % ext), dpi=300)
    plt.close(fig)


def fig_trend(rows):
    fig, ax = plt.subplots(1, 2, figsize=(7.6, 3.1))
    for ds in ORDER:
        sel = [r for r in rows if r["ds"] == ds]
        by = {}
        for r in sel:
            by.setdefault(r["subj"], []).append(r)
        x = [np.median([r["dR2"] for r in v]) for v in by.values()]
        y = [np.median([r["loss"] for r in v]) for v in by.values()]
        ax[0].scatter(x, y, s=22, color=COLOR[ds], alpha=0.85,
                      edgecolor="k", lw=0.3, label=LABEL[ds])
    ax[0].axhline(0, color="k", lw=0.6)
    ax[0].axvline(0, color="k", lw=0.6)
    ax[0].set_xlabel(r"excess trend $\Delta R^2$ (subject median)")
    ax[0].set_ylabel("correction loss  BA($\\lambda$=0) $-$ BA($\\lambda$=1)")
    ax[0].set_title("(a) all datasets, one point per subject", loc="left", fontsize=9)
    ax[0].legend(frameon=False, fontsize=7)
    gal = [r for r in rows if r["ds"] == "gal"]
    by = {}
    for r in gal:
        by.setdefault(r["subj"], []).append(r)
    x = [np.median([r["dR2"] for r in v]) for v in by.values()]
    y = [np.median([r["loss"] for r in v]) for v in by.values()]
    ax[1].scatter(x, y, s=26, color=COLOR["gal"], alpha=0.9, edgecolor="k", lw=0.4)
    p = np.polyfit(x, y, 1)
    xs = np.linspace(min(x), max(x), 20)
    ax[1].plot(xs, np.polyval(p, xs), "k--", lw=0.8)
    ax[1].set_xlabel(r"excess trend $\Delta R^2$")
    ax[1].set_ylabel("correction loss")
    ax[1].set_title("(b) grasp-and-lift, 12 subjects", loc="left", fontsize=9)
    for a in ax:
        a.tick_params(labelsize=7)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIG, "fig_trend.%s" % ext), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    rows = load()
    fig_lambda(rows)
    fig_trend(rows)
    print("figures written:", os.path.join(FIG, "fig_lambda.png"),
          os.path.join(FIG, "fig_trend.png"))
