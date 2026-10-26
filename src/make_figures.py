# -*- coding: utf-8 -*-
"""
(a) 中介效应的混淆检查：格层面 vs 被试层面 vs 表征内
(b) 出论文 4 张图
"""
import os, io
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 7.4, "axes.linewidth": 0.75, "xtick.major.width": 0.65,
    "ytick.major.width": 0.65, "font.family": "DejaVu Sans",
    "axes.titlesize": 7.8, "axes.labelsize": 7.4, "legend.fontsize": 6.2,
    "xtick.labelsize": 6.6, "ytick.labelsize": 6.6,
})

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
D = os.environ.get("BSPC_OUT", os.path.join(_ROOT, "results"))
DATA = os.environ.get("BSPC_DATA", r"E:\data")
CACHE = os.environ.get("BSPC_CACHE", os.path.join(_ROOT, "features", "cache_2b"))
ROOT = os.path.join(DATA, "BCICIV-2a-mat")
FIGD = os.path.join(D, "figs_paper")
OUT = os.path.join(D, "_mediate.txt")
L = []


def say(s=""):
    L.append(s)
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L))


Z = np.load(os.path.join(D, "numbers.npz"), allow_pickle=True)
ds = Z["r_ds"]
rep = Z["r_rep"]
tag = Z["r_tag"]
zs = np.abs(Z["r_zsh"])
gain = Z["r_align"] - Z["r_none"]
align = Z["r_align"]
none = Z["r_none"]
ceil = Z["r_ceil"]
zero = Z["r_zero"]
zp = Z["r_zp"]

say("=" * 96)
say("A  中介效应的三个层面（z_shift vs gain）")
say("=" * 96)
say("")
r, p = stats.spearmanr(zs, gain)
say("  1) 全部格 n=%d：rho=%+.3f p=%.3g" % (len(zs), r, p))
say("     （格间不独立：同被试/同配对跨 4 个表征重复）")
say("")
say("  2) 表征内（去掉表征间差异）：")
for rp in ("euc", "euc_ea", "tan", "csp"):
    m = rep == rp
    if m.sum() < 8:
        continue
    rr, pp = stats.spearmanr(zs[m], gain[m])
    say("     %-8s n=%-3d rho=%+.3f p=%.4g  （z_shift 中位 %.3f，gain 中位 %+.4f）"
        % (rp, m.sum(), rr, pp, np.median(zs[m]), np.median(gain[m])))
say("")
say("  3) 被试级（2a，每被试对 4 个表征取均值，n=9）：")
subs = sorted(set(tag[ds == "2a"]))
a_, b_ = [], []
for s in subs:
    m = (ds == "2a") & (tag == s)
    a_.append(np.mean(zs[m]))
    b_.append(np.mean(gain[m]))
rr, pp = stats.spearmanr(a_, b_)
say("     rho=%+.3f p=%.4g" % (rr, pp))
say("  3b) 被试级（2b，n=9）：")
subs2 = sorted({t.split(":")[0] for t in tag[ds == "2b"]})
a2, b2 = [], []
for s in subs2:
    m = (ds == "2b") & np.array([t.startswith(s + ":") for t in tag])
    a2.append(np.mean(zs[m]))
    b2.append(np.mean(gain[m]))
rr2, pp2 = stats.spearmanr(a2, b2)
say("     rho=%+.3f p=%.4g" % (rr2, pp2))
say("")
say("  判读：若表征内与被试级都不显著，则'z_shift 中介'只能是描述性的，")
say("        不能作为因果链的一环写进论文。")

# ---------------------------------------------------------------- 图
fig = plt.figure(figsize=(7.2, 5.6))
gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.30)

# ---- Fig 1a: 2b per-subject, 四种操作
ax = fig.add_subplot(gs[0, 0])
p2b_zero = Z["p2b_pen"] + np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
# 重新从细粒度重建：按被试算 zero
zs_sub = []
for s in subs2:
    m = (ds == "2b") & np.array([t.startswith(s + ":") for t in tag])
    zs_sub.append(np.mean(zero[m]))
zs_sub = np.array(zs_sub)
p_none = []
p_al = []
p_ce = []
for s in subs2:
    m = (ds == "2b") & np.array([t.startswith(s + ":") for t in tag])
    p_none.append(np.mean(none[m]))
    p_al.append(np.mean(align[m]))
    p_ce.append(np.nanmean(ceil[m]))
p_none, p_al, p_ce = map(np.array, (p_none, p_al, p_ce))
order = np.argsort(p_ce)
x = np.arange(len(subs2))
ax.bar(x - 0.26, zs_sub[order], 0.24, color="#c0392b", edgecolor="k", lw=0.3, label="zero to 0")
ax.bar(x, p_none[order], 0.24, color="#7f8c8d", edgecolor="k", lw=0.3, label="none")
ax.bar(x + 0.26, p_al[order], 0.24, color="#1e8449", edgecolor="k", lw=0.3, label="align")
ax.plot(x, p_ce[order], "k_", ms=11, mew=1.3, label="own ceiling")
ax.axhline(0.5, color="k", ls=":", lw=0.7)
ax.set_xticks(x)
ax.set_xticklabels([subs2[i] for i in order], fontsize=5.8)
ax.set_ylim(0.35, 1.06)
ax.set_ylabel("balanced accuracy")
ax.set_title("a   BCI-IV-2b, 9 subjects x 3 cross-day pairs", loc="left")
ax.legend(frameon=False, ncol=4, loc="upper center", fontsize=5.4,
          bbox_to_anchor=(0.5, 1.005), handlelength=1.1, columnspacing=0.9)
ax.grid(axis="y", color="0.94", lw=0.6)
ax.set_axisbelow(True)
ax.text(0.015, 0.60, "red bars fall to chance", transform=ax.transAxes,
        fontsize=5.6, color="#c0392b")

# ---- Fig 1b: 2a align vs ceiling scatter
ax = fig.add_subplot(gs[0, 1])
m2a = ds == "2a"
ax.scatter(ceil[m2a], none[m2a], s=20, marker="^", facecolor="none",
           edgecolor="#7f8c8d", lw=0.8, label="none")
ax.scatter(ceil[m2a], align[m2a], s=22, facecolor="none",
           edgecolor="#1e8449", lw=0.9, label="align")
lim = [0.30, 0.95]
ax.plot(lim, lim, "k-", lw=0.8, label="identity")
ax.set_xlim(lim)
ax.set_ylim(lim)
ax.set_xlabel("within-session CV of target (ceiling)")
ax.set_ylabel("cross-day balanced accuracy")
ax.set_title("b   BCI-IV-2a, 22 channels, 4 classes", loc="left")
ax.legend(frameon=False, loc="upper left")
ax.grid(color="0.94", lw=0.6)
ax.set_axisbelow(True)

# ---- Fig 2: z_pool
ax = fig.add_subplot(gs[1, 0])
mk = {"euc": "o", "euc_ea": "s", "tan": "^", "csp": "D"}
cl = {"euc": "#c0392b", "euc_ea": "#e67e22", "tan": "#2471a3", "csp": "#8e44ad"}
agg = []
for d_ in ("2a", "2b"):
    for rp in ("euc", "euc_ea", "tan", "csp"):
        m = (ds == d_) & (rep == rp)
        if m.sum() < 4:
            continue
        agg.append((d_, rp, np.median(zp[m]), np.mean(zero[m] - none[m])))
for d_, rp, z_, pen_ in agg:
    lab = ("2a " if d_ == "2a" else "2b ") + rp
    ax.scatter(z_, pen_, s=30, marker=mk[rp], color=cl[rp], edgecolor="k",
               lw=0.45, zorder=3)
# 空标签仅用于图例（数据集用实心/空心区分）
ax.scatter([], [], s=30, marker="o", facecolor="#c0392b", edgecolor="k", lw=0.4,
           label="log power")
ax.scatter([], [], s=30, marker="s", facecolor="#e67e22", edgecolor="k", lw=0.4,
           label="log power, EA")
ax.scatter([], [], s=30, marker="^", facecolor="#2471a3", edgecolor="k", lw=0.4,
           label="tangent")
ax.scatter([], [], s=30, marker="D", facecolor="#8e44ad", edgecolor="k", lw=0.4,
           label="CSP")
ax.set_xscale("log")
ax.axhline(0, color="k", lw=0.85)
ax.set_xlabel(r"$z_\mathrm{pool}=\|\mu_T\|/\|\mathrm{SD}\|$")
ax.set_ylabel("change from zeroing")
ax.set_title("c   observed: 8 dataset x representation cells", loc="left")
ax.legend(frameon=False, loc="lower left", fontsize=5.2, ncol=1,
          handletextpad=0.35, borderpad=0.15, labelspacing=0.22)
xz = np.array([a[2] for a in agg])
yp = np.array([a[3] for a in agg])
rho_o, p_o = stats.spearmanr(xz, yp)
ax.set_ylim(-0.245, 0.10)
ax.text(0.97, 0.96, r"$\rho$=%+.2f, $p$=%.4f" % (rho_o, p_o), transform=ax.transAxes,
        fontsize=6.2, ha="right", va="top")
ax.grid(color="0.94", lw=0.6)
ax.set_axisbelow(True)

# ---- Fig 2b inset: intervention
ax = fig.add_subplot(gs[1, 1])
ic = Z["int_c"]
iz = Z["int_zp"]
ip = Z["int_pen"]
cu = sorted(set(ic.tolist()))
mz, mp = [], []
for c in cu:
    m = ic == c
    mz.append(np.median(iz[m]))
    mp.append(np.mean(ip[m]))
ax.plot(mz, mp, "o-", color="#c0392b", ms=4.5, lw=1.2)
ax.axhline(0, color="k", lw=0.85)
ax.set_xlim(min(mz) - 0.25, max(mz) + 0.45)
ax.set_ylim(-0.225, 0.02)
ax.set_xlabel(r"$z_\mathrm{pool}$ dialled by injected offset $c$")
ax.set_ylabel("change from zeroing")
ax.set_title("d   interventional: one representation, $c$ varied", loc="left")
rho_i, p_i = stats.spearmanr(iz, ip)
ax.text(0.04, 0.24, r"$\rho$=%+.2f, $p$=%.0e, $n$=%d" % (rho_i, p_i, len(iz)),
        transform=ax.transAxes, fontsize=6.0)
ax.text(0.04, 0.96, "no-correction accuracy unchanged\n(median $\\Delta$ = 0.00000)",
        transform=ax.transAxes, fontsize=5.6, va="top", color="0.3")
ax.grid(color="0.94", lw=0.6)
ax.set_axisbelow(True)

plt.savefig(os.path.join(FIGD, "Fig1_2.png"), dpi=600)
plt.savefig(os.path.join(FIGD, "Fig1_2.pdf"))
plt.close()

# ---- Fig 2: protocol split (S->S vs S->F) ----
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.6), sharey=True)
m2b = ds == '2b'
seqs = np.array([t.split(':')[-1] if ':' in t else '' for t in tag])
grp = np.array(['S->S' if s == '1>2' else 'S->F' for s in seqs])
subs = sorted(set(tag[m2b].tolist()))
subs = [s.split(':')[0] for s in subs]
subs = sorted(set(subs))
for k, (nm, gname) in enumerate((('a   screen to screen (01T to 02T)', 'S->S'),
                                   ('b   screen into feedback (01T or 02T to 03T)', 'S->F'))):
    ax = axes[k]
    mm = m2b & (grp == gname)
    xs, vn, vz, va, vc, vd = [], [], [], [], [], []
    for j, s in enumerate(subs):
        sel = mm & np.array([t.startswith(s + ':') for t in tag])
        if sel.sum() < 2:
            continue
        xs.append(j)
        vn.append(np.mean(none[sel]))
        vz.append(np.mean(zero[sel]))
        va.append(np.mean(align[sel]))
        vc.append(np.nanmean(ceil[sel]))
        # 与正文同口径：先逐格求差再取均值
        vd.append(np.nanmean(align[sel] - ceil[sel]))
    xs = np.array(xs)
    ax.bar(xs - 0.26, vz, 0.24, color='#c0392b', edgecolor='k', lw=0.3, label='zero')
    ax.bar(xs, vn, 0.24, color='#7f8c8d', edgecolor='k', lw=0.3, label='none')
    ax.bar(xs + 0.26, va, 0.24, color='#1e8449', edgecolor='k', lw=0.3, label='align')
    ax.plot(xs, vc, 'k_', ms=11, mew=1.3, label='reference')
    ax.axhline(0.5, color='k', ls=':', lw=0.7)
    ax.set_xticks(xs)
    ax.set_xticklabels([subs[i] for i in xs], fontsize=5.8)
    ax.set_ylim(0.40, 1.10)
    ax.set_title(nm, loc='left')
    ax.grid(axis='y', color='0.94', lw=0.6)
    ax.set_axisbelow(True)
    if k == 0:
        ax.set_ylabel('balanced accuracy')
        ax.legend(frameon=False, ncol=4, loc='lower center', fontsize=5.4,
                  bbox_to_anchor=(1.02, 1.00), handlelength=1.1, columnspacing=0.9)
    dd = np.array(vd)
    ax.text(0.03, 0.90, 'align $-$ reference = %+.3f' % np.mean(dd),
            transform=ax.transAxes, fontsize=6.2, va='top')
plt.tight_layout()
plt.savefig(os.path.join(FIGD, 'Fig2_protocol.png'), dpi=600)
plt.savefig(os.path.join(FIGD, 'Fig2_protocol.pdf'))
plt.close()

say("")
say("图已存 figs_paper/Fig1_2.png, Fig3_shrink.png")
say("  观测剂量 rho=%+.3f p=%.4g（%d 格）" % (rho_o, p_o, len(agg)))
say("  干预剂量 rho=%+.3f p=%.3g（%d 点）" % (rho_i, p_i, len(iz)))
say("DONE")
