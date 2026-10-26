# -*- coding: utf-8 -*-
"""
新论文的图与数字总表（单一来源）
==================================
一次算出全文引用的所有数字，存 paper_numbers_v2.npz，并出 4 张图。
复现脚本会用不同种子重跑并与此比对。
"""
import os, io, glob
import numpy as np
from scipy import stats
from scipy.linalg import eigh
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold
import scipy.io as sio
from scipy.signal import butter, filtfilt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 7.4, "axes.linewidth": 0.75, "xtick.major.width": 0.65,
    "ytick.major.width": 0.65, "font.family": "DejaVu Sans",
    "axes.titlesize": 7.8, "axes.labelsize": 7.4, "legend.fontsize": 6.3,
    "xtick.labelsize": 6.6, "ytick.labelsize": 6.6,
})

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
D = os.environ.get("BSPC_OUT", os.path.join(_ROOT, "results"))
DATA = os.environ.get("BSPC_DATA", r"E:\data")
CACHE = os.environ.get("BSPC_CACHE", os.path.join(_ROOT, "features", "cache_2b"))
ROOT = os.path.join(DATA, "BCICIV-2a-mat")
FIGD = os.path.join(D, "figs_paper")
if not os.path.isdir(FIGD):
    os.makedirs(FIGD)
OUT = os.path.join(D, "_paper_v2_numbers.txt")
RNG = np.random.RandomState(20261026)
LOG = []


def say(s=""):
    LOG.append(s)
    io.open(OUT, "w", encoding="utf-8").write("\n".join(LOG))


def bacc(y, p):
    u = np.unique(y)
    if len(u) < 2:
        return np.nan
    return float(np.mean([(p[y == c] == c).mean() for c in u]))


def mk(kind="lda"):
    if kind == "lda":
        return LDA(solver="lsqr", shrinkage="auto")
    if kind == "logit":
        return LogisticRegression(max_iter=3000, C=0.3, solver="lbfgs")
    return LinearSVC(C=0.02, max_iter=20000)


def cv_bacc(X, y, kind="lda", folds=5, seed=0):
    cnt = np.bincount(y)
    nz = cnt[cnt > 0]
    if len(nz) < 2:
        return np.nan
    k = int(min(folds, nz.min()))
    if k < 2:
        return np.nan
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=seed)
    pr, tr_ = [], []
    for a, b in skf.split(X, y):
        try:
            pr.append(mk(kind).fit(X[a], y[a]).predict(X[b]))
        except Exception:
            pr.append(np.full(len(b), -1))
        tr_.append(y[b])
    return bacc(np.concatenate(tr_), np.concatenate(pr))


def covs(X, shrink=1e-3):
    n, ch, _ = X.shape
    out = np.empty((n, ch, ch))
    for i in range(n):
        C = np.atleast_2d(np.cov(X[i]))
        s = np.trace(C) / ch
        out[i] = (1 - shrink) * C + shrink * s * np.eye(ch)
    return out


def msqrt_inv(Cs, eps=1e-8):
    R = Cs.mean(0)
    w, V = eigh(R)
    w = np.maximum(w, eps)
    return V @ np.diag(w ** -0.5) @ V.T


def tangent(Cs):
    n, ch, _ = Cs.shape
    iu = np.triu_indices(ch)
    Z = np.empty((n, len(iu[0])))
    for i in range(n):
        w, V = eigh(Cs[i])
        w = np.maximum(w, 1e-12)
        Z[i] = (V @ np.diag(np.log(w)) @ V.T)[iu]
    return Z


def logpow(segs, nwin=4):
    n, ch, T = segs.shape
    w = T // nwin
    out = np.empty((n, ch * nwin))
    for i in range(n):
        pv = np.array([np.mean(segs[i][:, k * w:(k + 1) * w] ** 2, 1) for k in range(nwin)])
        out[i] = np.log(pv.ravel() + 1e-12)
    return out


def csp_feat(Xtr, ytr, Xte, m=3):
    Ctr = covs(Xtr, 1e-3)
    cls = np.unique(ytr)
    if len(cls) < 2:
        return None, None
    Cs = [Ctr[ytr == c].mean(0) for c in cls]
    Cc = np.mean(Cs, 0)
    w, V = eigh(Cs[0], Cc)
    idx = np.argsort(w)
    sel = np.concatenate([idx[:m], idx[-m:]])
    W = V[:, sel]

    def proj(X):
        Z = np.einsum("nct,ck->nkt", X, W)
        return np.log(np.var(Z, axis=2) + 1e-12)

    return proj(Xtr), proj(Xte)


def tr_sigma(X, nrep=20):
    k = len(X)
    if k < 8:
        return np.nan
    h = k // 2
    v = []
    for _ in range(nrep):
        p = RNG.permutation(k)
        dd = X[p[:h]].mean(0) - X[p[h:2 * h]].mean(0)
        v.append(float(np.mean(dd ** 2)) * h / 4.0)
    return float(np.median(v))


FS = 250
b1, b2 = butter(4, [8.0 / (FS / 2), 30.0 / (FS / 2)], btype="band")


def load_bci(path):
    m = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
    runs = np.atleast_1d(m["data"])
    segs, ys = [], []
    for rr in runs:
        try:
            X = np.asarray(rr.X, dtype=np.float64)[:, :22]
            tr = np.asarray(rr.trial, dtype=int).ravel()
            yy = np.asarray(rr.y, dtype=int).ravel()
        except Exception:
            continue
        if len(tr) == 0 or len(yy) == 0:
            continue
        X = filtfilt(b1, b2, X, axis=0)
        i0, i1 = int(2.0 * FS), int(6.0 * FS)
        for t, lab in zip(tr, yy):
            if lab <= 0:
                continue
            sg = X[t + i0:t + i1]
            if sg.shape[0] < (i1 - i0):
                continue
            segs.append(sg.T)
            ys.append(int(lab))
    if not segs:
        return np.zeros((0, 22, 10)), np.zeros(0, int)
    return np.array(segs), np.array(ys)


say("构建表征 ...")
PAIRS = []
for i in range(1, 10):
    pT = os.path.join(ROOT, "A%02dT.mat" % i)
    pE = os.path.join(ROOT, "A%02dE.mat" % i)
    if not (os.path.exists(pT) and os.path.exists(pE)):
        continue
    XT, yT = load_bci(pT)
    XE, yE = load_bci(pE)
    if not len(XT) or not len(XE) or len(np.unique(yE)) < 2:
        continue
    CT, CE = covs(XT), covs(XE)
    Rj = msqrt_inv(np.concatenate([CT, CE], 0))
    Rt = msqrt_inv(CT)
    reps = {}
    reps["euc"] = (logpow(XT), logpow(XE))
    # 修正：EA 必须作用在**原始信号**上，再提 log 功率
    # EA on raw signal is a single left-multiplication by R^{-1/2} (channel space)
    reps["euc_ea"] = (logpow(np.einsum("ij,njt->nit", Rj, XT)),
                      logpow(np.einsum("ij,njt->nit", Rj, XE)))
    reps["tan"] = (tangent(np.einsum("ij,njk,kl->nil", Rt, CT, Rt)),
                   tangent(np.einsum("ij,njk,kl->nil", Rt, CE, Rt)))
    cT, cE = csp_feat(XT, yT, XE, 3)
    if cT is not None:
        reps["csp"] = (cT, cE)
    for rep, (A, B) in reps.items():
        if A is None or not np.all(np.isfinite(B)):
            continue
        PAIRS.append(dict(ds="2a", tag="S%02d" % i, rep=rep, A=A, ya=yT, B=B, yb=yE))

S = {}
for p in sorted(glob.glob(os.path.join(CACHE, "*.npz"))):
    z = np.load(p, allow_pickle=True)
    S[os.path.basename(p).replace(".npz", "")] = dict(
        X=z["X"].astype(np.float64), y=z["y"].astype(int),
        date=int(z["date"]), subj=str(z["subj"]), sess=int(z["sess"]))
bysub = {}
for k, v in S.items():
    bysub.setdefault(v["subj"], []).append(k)
for s in bysub:
    bysub[s] = sorted(bysub[s], key=lambda k: S[k]["date"])

for sub in sorted(bysub):
    ks = bysub[sub]
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            ka, kb = ks[i], ks[j]
            A, ya = S[ka]["X"], S[ka]["y"]
            B, yb = S[kb]["X"], S[kb]["y"]
            if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
                continue
            CA, CB = covs(A), covs(B)
            Rj = msqrt_inv(np.concatenate([CA, CB], 0))
            Rt = msqrt_inv(CA)
            reps = {}
            reps["euc"] = (logpow(A), logpow(B))
            reps["euc_ea"] = (logpow(np.einsum("ij,njt->nit", Rj, A)),
                              logpow(np.einsum("ij,njt->nit", Rj, B)))
            reps["tan"] = (tangent(np.einsum("ij,njk,kl->nil", Rt, CA, Rt)),
                           tangent(np.einsum("ij,njk,kl->nil", Rt, CB, Rt)))
            cT, cE = csp_feat(A, ya, B, 3)
            if cT is not None:
                reps["csp"] = (cT, cE)
            for rep, (FA, FB) in reps.items():
                if FA is None or not np.all(np.isfinite(FB)):
                    continue
                PAIRS.append(dict(ds="2b", tag="%s:%d>%d" % (sub, S[ka]["sess"], S[kb]["sess"]),
                                  rep=rep, A=FA, ya=ya, B=FB, yb=yb))
say("  组合数 = %d" % len(PAIRS))

say("")
say("=" * 100)
say("逐组合：三种操作、z_pool、z_shift、天花板")
say("=" * 100)
R = []
for p in PAIRS:
    A, ya, B, yb = p["A"], p["ya"], p["B"], p["yb"]
    if len(B) < 20 or len(A) < 20:
        continue
    clf = mk("lda").fit(A, ya)
    muT, muB = A.mean(0), B.mean(0)
    sdT = np.maximum(A.std(0, ddof=1), 1e-12)
    zp = float(np.linalg.norm(muT) / max(np.linalg.norm(sdT), 1e-12))
    dT = np.asarray(clf.decision_function(A), float)
    dB = np.asarray(clf.decision_function(B), float)
    if dT.ndim == 1:
        dT, dB = dT[:, None], dB[:, None]
    sdv = np.maximum(dT.std(0, ddof=1), 1e-12)
    zsh = float(np.sqrt(np.mean(((dB.mean(0) - dT.mean(0)) / sdv) ** 2)))
    B_al = B - (muB - muT)
    dA = np.asarray(clf.decision_function(B_al), float)
    if dA.ndim == 1:
        dA = dA[:, None]
    zsh_after = float(np.sqrt(np.mean(((dA.mean(0) - dT.mean(0)) / sdv) ** 2)))
    n0 = bacc(yb, clf.predict(B))
    z0 = bacc(yb, clf.predict(B - muB))
    al = bacc(yb, clf.predict(B_al))
    cb = float(np.nanmean([cv_bacc(B, yb, "lda", seed=s) for s in range(5)]))
    s2 = tr_sigma(B)
    Dn = s2 / len(B) if np.isfinite(s2) else np.nan
    Do = float(np.mean((muB - muT) ** 2))
    Dt = max(Do - Dn, 0.0) if np.isfinite(Dn) else np.nan
    exc = Dt / Dn if (np.isfinite(Dn) and Dn > 0) else np.nan
    R.append(dict(ds=p["ds"], tag=p["tag"], rep=p["rep"], n_b=len(B),
                  ceil=cb, none=n0, zero=z0, align=al,
                  zp=zp, zsh=zsh, zsh_after=zsh_after, excess=exc))

say("  n = %d" % len(R))
for ds in ("2a", "2b"):
    for rep in ("euc", "euc_ea", "tan", "csp"):
        q = [r for r in R if r["ds"] == ds and r["rep"] == rep]
        if not q:
            continue
        say("  %-3s %-8s %-4d  ceil %.4f  none %.4f  zero %.4f  align %.4f  zp %.3f"
            % (ds, rep, len(q), np.nanmedian([r["ceil"] for r in q]),
               np.median([r["none"] for r in q]), np.median([r["zero"] for r in q]),
               np.median([r["align"] for r in q]), np.median([r["zp"] for r in q])))

say("")
say("=" * 100)
say("Table 2：BCI-2b 被试级（每被试 27 格取均值，n=9）")
say("=" * 100)
per2b = []
for sub in sorted({r["tag"].split(":")[0] for r in R if r["ds"] == "2b"}):
    q = [r for r in R if r["ds"] == "2b" and r["tag"].startswith(sub + ":")]
    if not q:
        continue
    d = dict(sub=sub, n=len(q),
             ceil=np.nanmean([r["ceil"] for r in q]),
             zero=np.nanmean([r["zero"] for r in q]),
             none=np.mean([r["none"] for r in q]),
             align=np.mean([r["align"] for r in q]))
    d["gain"] = d["align"] - d["none"]
    d["pen"] = d["zero"] - d["none"]
    per2b.append(d)
    say("  %-5s n=%-3d ceil %.4f  zero %.4f  none %.4f  align %.4f  gain %+.4f  pen %+.4f"
        % (d["sub"], d["n"], d["ceil"], d["zero"], d["none"], d["align"],
           d["gain"], d["pen"]))

g2b = np.array([d["gain"] for d in per2b])
p2b = np.array([d["pen"] for d in per2b])
say("")
say("  gain(align-none) 均值 %+.4f 中位 %+.4f  %d/%d 改善  p=%.4g"
    % (g2b.mean(), np.median(g2b), int((g2b > 0).sum()), len(g2b),
       stats.wilcoxon(g2b).pvalue))
say("  pen(zero-none)   均值 %+.4f 中位 %+.4f  %d/%d 改善  p=%.4g"
    % (p2b.mean(), np.median(p2b), int((p2b > 0).sum()), len(p2b),
       stats.wilcoxon(p2b).pvalue))
bs = np.array([np.mean(RNG.choice(g2b, len(g2b))) for _ in range(4000)])
say("  gain bootstrap 95%% CI = [%+.4f, %+.4f]"
    % (np.percentile(bs, 2.5), np.percentile(bs, 97.5)))
dAC = np.array([d["align"] - d["ceil"] for d in per2b])
say("  align-ceil 中位 %+.4f 均值 %+.4f ；p=%.4g ；|差|<0.02 的 %d/%d"
    % (np.median(dAC), dAC.mean(), stats.wilcoxon(dAC).pvalue,
       int((np.abs(dAC) < 0.02).sum()), len(dAC)))
bs2 = np.array([np.mean(RNG.choice(dAC, len(dAC))) for _ in range(4000)])
say("  align-ceil bootstrap 95%% CI = [%+.4f, %+.4f]"
    % (np.percentile(bs2, 2.5), np.percentile(bs2, 97.5)))

say("")
say("Table 1：BCI-2a 被试级（每被试 12 格取均值，n=9）")
per2a = []
for sub in sorted({r["tag"] for r in R if r["ds"] == "2a"}):
    q = [r for r in R if r["ds"] == "2a" and r["tag"] == sub]
    d = dict(sub=sub, n=len(q),
             ceil=np.nanmean([r["ceil"] for r in q]),
             zero=np.mean([r["zero"] for r in q]),
             none=np.mean([r["none"] for r in q]),
             align=np.mean([r["align"] for r in q]))
    d["gain"] = d["align"] - d["none"]
    d["pen"] = d["zero"] - d["none"]
    per2a.append(d)
    say("  %-5s n=%-3d ceil %.4f  zero %.4f  none %.4f  align %.4f  gain %+.4f"
        % (d["sub"], d["n"], d["ceil"], d["zero"], d["none"], d["align"], d["gain"]))
g2a = np.array([d["gain"] for d in per2a])
p2a = np.array([d["pen"] for d in per2a])
say("  gain 均值 %+.4f  %d/%d  p=%.4g" % (g2a.mean(), int((g2a > 0).sum()), len(g2a),
                                          stats.wilcoxon(g2a).pvalue))
say("  pen  均值 %+.4f  %d/%d  p=%.4g" % (p2a.mean(), int((p2a > 0).sum()), len(p2a),
                                          stats.wilcoxon(p2a).pvalue))

say("")
say("=" * 100)
say("z_pool 干预（Fig 2b）")
say("=" * 100)
CS = [0.0, 1.0, 2.0, 4.0, 8.0]
intA = []
for p in PAIRS:
    A, ya, B, yb = p["A"], p["ya"], p["B"], p["yb"]
    if len(B) < 20 or len(A) < 20:
        continue
    sd = float(np.mean(A.std(0, ddof=1)))
    if not np.isfinite(sd) or sd <= 0:
        continue
    for c in CS:
        Fa = A + c * sd
        Fb = B + c * sd
        clf = mk("lda").fit(Fa, ya)
        n0 = bacc(yb, clf.predict(Fb))
        z0 = bacc(yb, clf.predict(Fb - Fb.mean(0)))
        zp = float(np.linalg.norm(Fa.mean(0)) / max(np.linalg.norm(Fa.std(0, ddof=1)), 1e-12))
        intA.append(dict(tag=p["tag"], rep=p["rep"], c=c, zp=zp, none=n0, pen=z0 - n0))
say("  %-6s %-10s %-10s %-12s" % ("c", "z_pool中位", "none", "归零惩罚"))
for c in CS:
    q = [r for r in intA if r["c"] == c]
    say("  %-6.1f %-10.2f %-10.4f %+.4f"
        % (c, np.median([r["zp"] for r in q]), np.median([r["none"] for r in q]),
           np.mean([r["pen"] for r in q])))
zz = np.array([r["zp"] for r in intA])
pp = np.array([r["pen"] for r in intA])
rho_i, p_i = stats.spearmanr(zz, pp)
say("  全部 %d 点：rho=%+.3f p=%.3g" % (len(zz), rho_i, p_i))
base = {(r["tag"], r["rep"]): r["none"] for r in intA if r["c"] == 0.0}
for c in CS[1:]:
    d = [r["none"] - base[(r["tag"], r["rep"])] for r in intA
         if r["c"] == c and (r["tag"], r["rep"]) in base]
    say("  c=%.1f  none 相对 c=0 变化：中位 %+.5f 均值 %+.5f"
        % (c, np.median(d), np.mean(d)))

say("")
say("=" * 100)
say("收缩：子采样把 excess 压进 [1,5]（Fig 4）")
say("=" * 100)
NS = [5, 10, 20, 40]
shr = []
for p in PAIRS:
    A, ya, B, yb = p["A"], p["ya"], p["B"], p["yb"]
    if len(B) < 40 or len(A) < 40:
        continue
    clf = mk("lda").fit(A, ya)
    muT = A.mean(0)
    s2 = tr_sigma(B)
    if not np.isfinite(s2) or s2 <= 0:
        continue
    Do = float(np.mean((B.mean(0) - muT) ** 2))
    n0 = bacc(yb, clf.predict(B))
    for n in NS:
        nn = min(n, len(B))
        Dn = s2 / nn
        Dt_raw = Do - Dn
        Dt = max(Dt_raw, 0.0)
        E = Dt / Dn if Dn > 0 else np.nan
        E_raw = Dt_raw / Dn if Dn > 0 else np.nan
        wo = float(np.clip(1 - 1.0 / max(E, 1e-9), 0.0, 1.0))
        wn = float(E / (1.0 + E))
        wn_raw = E_raw / (1.0 + E_raw) if (np.isfinite(E_raw) and E_raw != -1) else np.nan
        go, gn, g1 = [], [], []
        for _ in range(12):
            idx = RNG.choice(len(B), size=nn, replace=False)
            off = B[idx].mean(0) - muT
            go.append(bacc(yb, clf.predict(B - wo * off)))
            gn.append(bacc(yb, clf.predict(B - wn * off)))
            g1.append(bacc(yb, clf.predict(B - off)))
        shr.append(dict(tag=p["tag"], rep=p["rep"], n=nn, E=E, E_raw=E_raw, none=n0,
                        wo=float(np.nanmedian(go)), wn=float(np.nanmedian(gn)),
                        wn_raw=wn_raw, w1=float(np.nanmedian(g1))))

say("")
say("  公式 (5) 的整流项是否必要（未截断时的估计）")
er = np.array([r["E_raw"] for r in shr if np.isfinite(r["E_raw"])])
say("    %d 个估计中 E_raw<0 的 %d 个 (%.1f%%)；最小 E_raw %.3f"
    % (len(er), int((er < 0).sum()), 100.0 * (er < 0).sum() / len(er), er.min()))
wraw = np.array([r["wn_raw"] for r in shr if np.isfinite(r["wn_raw"])])
bad = wraw[(wraw < 0) | (wraw > 1)]
say("    若不截断，w=E/(1+E) 落在 [0,1] 之外的 %d 个；极端值 min %.2f max %.2f"
    % (len(bad), bad.min() if len(bad) else np.nan, bad.max() if len(bad) else np.nan))
say("  %-6s %-9s %-10s %-9s %-9s %-9s %-9s" %
    ("n", "excess中位", "none", "1-1/E", "E/(1+E)", "w=1", "最优"))
for n in NS:
    q = [r for r in shr if r["n"] == n]
    a = np.nanmean([r["wo"] - r["none"] for r in q])
    b_ = np.nanmean([r["wn"] - r["none"] for r in q])
    c_ = np.nanmean([r["w1"] - r["none"] for r in q])
    say("  %-6d %-9.2f %-10.4f %+.4f  %+.4f  %+.4f  %s"
        % (n, np.median([r["E"] for r in q]), np.median([r["none"] for r in q]),
           a, b_, c_, "E/(1+E)" if b_ > max(a, c_) else ("1-1/E" if a > c_ else "w=1")))
sub = [r for r in shr if 1.0 <= r["E"] <= 5.0]
say("")
say("  excess in [1,5]: %d cases" % len(sub))
for lab, k in (("none", None), ("1-1/E", "wo"), ("E/(1+E)", "wn"), ("w=1", "w1")):
    v = np.zeros(len(sub)) if k is None else np.array([r[k] - r["none"] for r in sub])
    say("    %-10s 均值 %+.4f 中位 %+.4f  %d/%d 改善" % (lab, v.mean(), np.median(v),
                                                        int((v > 0).sum()), len(v)))
lowE = [r for r in shr if r["E"] < 2.0]
say("")
say("  excess<2: %d cases" % len(lowE))
for lab, k in (("1-1/E", "wo"), ("E/(1+E)", "wn"), ("w=1 全减", "w1")):
    v = np.array([r[k] - r["none"] for r in lowE])
    say("    %-12s 均值 %+.4f  %d/%d 改善" % (lab, v.mean(), int((v > 0).sum()), len(v)))

say("")
say("  Table 6b：E<2 内部按 regime 拆分（同一批 case，故合计等于上表）")
for lo, hi, nm in ((0.0, 1.0, "E<1"), (1.0, 2.0, "1<=E<2")):
    q = [r for r in lowE if lo <= r["E"] < hi]
    if not q:
        continue
    say("    %-10s n=%-4d" % (nm, len(q)))
    for lab, k in (("1-1/E", "wo"), ("E/(1+E)", "wn"), ("w=1 全减", "w1")):
        v = np.array([r[k] - r["none"] for r in q])
        say("        %-10s 均值 %+.4f  改善 %d/%d  (%.0f%%)"
            % (lab, v.mean(), int((v > 0).sum()), len(v), 100.0 * (v > 0).sum() / len(v)))
        # 增益分布的偏度，用于解释"均值 vs 比例"分歧
        if k == "w1" and len(v) > 3:
            say("            增益分布：min %+.4f  q25 %+.4f  中位 %+.4f  q75 %+.4f  max %+.4f  偏度 %+.2f"
                % (v.min(), np.percentile(v, 25), np.median(v),
                   np.percentile(v, 75), v.max(), float(stats.skew(v))))

say("")
say("  z_pool 干预：per-cell 剂量反应（不依赖格间可比性）")
pc = {}
for r in intA:
    pc.setdefault((r["tag"], r["rep"]), []).append((r["zp"], r["pen"]))
prim = []
for key, v in pc.items():
    v = sorted(v)
    if len(v) < 5:
        continue
    z_ = np.array([x[0] for x in v])
    p_ = np.array([x[1] for x in v])
    if len(np.unique(z_)) < 3:
        continue
    rr, pp_ = stats.spearmanr(z_, p_)
    if np.isfinite(rr):
        prim.append((key[0], rr))
rr_ = np.array([x[1] for x in prim])
nneg = int((rr_ < 0).sum())
say("    有 5 个 c 点的格 = %d ；per-cell rho<0 : %d (%.0f%%) ；rho 中位 %+.3f"
    % (len(rr_), nneg, 100.0 * nneg / len(rr_), np.median(rr_)))
try:
    from scipy.stats import binomtest
    pbin = binomtest(nneg, len(rr_), 0.5).pvalue
except Exception:
    pbin = stats.binom_test(nneg, len(rr_), 0.5)
say("    符号检验 p = %.3g" % pbin)
for ds_ in ("2a", "2b"):
    q = np.array([x[1] for x in prim if x[0] == ds_])
    if len(q):
        say("      %-3s n=%d  rho 中位 %+.3f  为负 %d/%d"
            % (ds_, len(q), np.median(q), int((q < 0).sum()), len(q)))

say("")
say("=" * 100)
say("中介：z_shift vs gain")
say("=" * 100)
zs = np.array([abs(r["zsh"]) for r in R])
gn = np.array([r["align"] - r["none"] for r in R])
rg, pg = stats.spearmanr(zs, gn)
say("  全部 %d 格：rho=%+.3f p=%.3g" % (len(zs), rg, pg))
za = np.array([r["zsh_after"] for r in R])
say("  对齐后 |z_shift| 中位 %.5f（对齐前 %.3f）" % (np.median(za), np.median(zs)))
sub_zs, sub_gn = [], []
for sub_ in sorted({r["tag"] for r in R if r["ds"] == "2a"}):
    q = [r for r in R if r["ds"] == "2a" and r["tag"] == sub_]
    sub_zs.append(np.mean([abs(r["zsh"]) for r in q]))
    sub_gn.append(np.mean([r["align"] - r["none"] for r in q]))
r2, p2v = stats.spearmanr(sub_zs, sub_gn)
say("  BCI-2a 被试级 n=%d：rho=%+.3f p=%.4g" % (len(sub_zs), r2, p2v))

np.savez(os.path.join(D, "numbers.npz"),
         r_ds=np.array([r["ds"] for r in R]),
         r_tag=np.array([r["tag"] for r in R]),
         r_rep=np.array([r["rep"] for r in R]),
         r_ceil=np.array([r["ceil"] for r in R]),
         r_none=np.array([r["none"] for r in R]),
         r_zero=np.array([r["zero"] for r in R]),
         r_align=np.array([r["align"] for r in R]),
         r_zp=np.array([r["zp"] for r in R]),
         r_zsh=np.array([r["zsh"] for r in R]),
         r_exc=np.array([r["excess"] for r in R]),
         int_c=np.array([r["c"] for r in intA]),
         int_zp=np.array([r["zp"] for r in intA]),
         int_pen=np.array([r["pen"] for r in intA]),
         shr_E=np.array([r["E"] for r in shr]),
         shr_n=np.array([r["n"] for r in shr]),
         shr_wo=np.array([r["wo"] for r in shr]),
         shr_wn=np.array([r["wn"] for r in shr]),
         shr_w1=np.array([r["w1"] for r in shr]),
         shr_none=np.array([r["none"] for r in shr]),
         p2b_gain=g2b, p2b_pen=p2b, p2a_gain=g2a, p2a_pen=p2a, dAC=dAC)
say("")
say("  数字已存 paper_numbers_v2.npz")
say("DONE")
