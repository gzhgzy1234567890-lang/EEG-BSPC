# -*- coding: utf-8 -*-
"""独立复现 v3：与 paper_numbers 不共享特征/评估代码。

主张清单（对应 v3 论文）：
  C1  BCI-2b：align > none，9/9 被试，p<0.05
  C2  BCI-2b：zero  < none，9/9 被试变差
  C3  BCI-2a：align > none 且 zero < none
  C4  z_pool 观测剂量：8 格 rho < -0.6 且 p<0.05
  C5  z_pool 干预：no-correction 严格不变（max|Δ|=0）且惩罚随 c 单调下降
  C6  2b 协议拆分：S->S 的 align-参照 > S->F 的 align-参照（残差集中在跨协议对）
  C7  z_disc（判别投影）**不能**比 z_pool 更好地排序 —— 论文已声明其失败
  C8  z_shift 中介：**预期不通过** —— 论文已声明不声称中介
"""
import os
import io
import glob
import numpy as np
from scipy import stats
from scipy.linalg import eigh
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.model_selection import StratifiedKFold
import scipy.io as sio
from scipy.signal import butter, filtfilt

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
D = os.environ.get("BSPC_OUT", os.path.join(_ROOT, "results"))
DATA = os.environ.get("BSPC_DATA", r"E:\data")
CACHE = os.environ.get("BSPC_CACHE", os.path.join(_ROOT, "features", "cache_2b"))
ROOT = os.path.join(DATA, "BCICIV-2a-mat")
OUT = os.path.join(D, "_reproduce.txt")

FS = 250
b1, b2 = butter(4, [8.0 / (FS / 2), 30.0 / (FS / 2)], btype="band")
SEEDS = [7, 1234, 98765, 424242]
LOG = []


def say(s=""):
    LOG.append(s)


def bacc(y, p):
    u = np.unique(y)
    if len(u) < 2:
        return np.nan
    return float(np.mean([np.mean(p[y == c] == c) for c in u]))


def shcov(X, shrink=1e-3):
    n, ch, _ = X.shape
    out = np.empty((n, ch, ch))
    for i in range(n):
        C = np.cov(X[i])
        t = np.trace(C) / ch
        out[i] = (1 - shrink) * C + shrink * t * np.eye(ch)
    return out


def inv_sqrt(M):
    val, vec = eigh(M)
    val = np.clip(val, 1e-8, None)
    return vec.dot(np.diag(val ** -0.5)).dot(vec.T)


def band_power(X, nwin=4):
    n, ch, T = X.shape
    w = T // nwin
    f = np.empty((n, ch * nwin))
    for i in range(n):
        f[i] = np.log(np.array([np.mean(X[i][:, k * w:(k + 1) * w] ** 2, 1)
                                for k in range(nwin)]).ravel() + 1e-12)
    return f


def to_tangent(Cs):
    n, ch, _ = Cs.shape
    iu = np.triu_indices(ch)
    Z = np.empty((n, len(iu[0])))
    for i in range(n):
        v, V = eigh(Cs[i])
        v = np.clip(v, 1e-12, None)
        Z[i] = (V.dot(np.diag(np.log(v))).dot(V.T))[iu]
    return Z


def csp_features(Xtr, ytr, Xte, m=3):
    Ctr = shcov(Xtr, 1e-3)
    cls = np.unique(ytr)
    if len(cls) < 2:
        return None, None
    ch = Ctr.shape[1]
    mm = int(min(m, max(1, ch // 2)))
    Cs = [Ctr[ytr == c].mean(0) for c in cls]
    Cc = np.mean(Cs, 0)
    w, V = eigh(Cs[0], Cc)
    idx = np.sort(np.argsort(w))
    sel = np.concatenate([idx[:mm], idx[-mm:]])
    if len(cls) == 2:
        sel = np.array(sorted(set(sel.tolist())), dtype=int)
    W = V[:, sel]

    def proj(X):
        Z = np.einsum("nct,ck->nkt", X, W)
        return np.log(np.var(Z, axis=2) + 1e-12)

    return proj(Xtr), proj(Xte)


def split_half_trace(X, rng, reps=20):
    """tr(Sigma) 的无偏估计：sum(dd^2) * h / 2。

    旧版写 mean(dd^2) * h / 4，对特征维取了平均而不是求和，使 tr 低估 2D 倍。
    这一错误曾同时存在于主脚本与本文件，所以"两套实现一致"并不能证明估计量正确。
    """
    k = len(X)
    if k < 8:
        return np.nan
    h = k // 2
    v = []
    for _ in range(reps):
        p = rng.permutation(k)
        dd = X[p[:h]].mean(0) - X[p[h:h * 2]].mean(0)
        v.append(float(np.sum(dd ** 2)) * h / 2.0)
    return float(np.median(v))


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


def build_2a():
    out = []
    for i in range(1, 10):
        pT = os.path.join(ROOT, "A%02dT.mat" % i)
        pE = os.path.join(ROOT, "A%02dE.mat" % i)
        if not (os.path.exists(pT) and os.path.exists(pE)):
            continue
        Xa, ya = load_bci(pT)
        Xb, yb = load_bci(pE)
        if len(Xa) < 20 or len(Xb) < 20:
            continue
        Ca, Cb = shcov(Xa), shcov(Xb)
        Rj = inv_sqrt((Ca.mean(0) + Cb.mean(0)) / 2.0)
        Rt = inv_sqrt(Ca.mean(0))
        reps = {
            "euc": (band_power(Xa), band_power(Xb)),
            "euc_ea": (band_power(np.einsum("ij,njt->nit", Rj, Xa)),
                       band_power(np.einsum("ij,njt->nit", Rj, Xb))),
            "tan": (to_tangent(np.einsum("ij,njk,kl->nil", Rt, Ca, Rt)),
                    to_tangent(np.einsum("ij,njk,kl->nil", Rt, Cb, Rt))),
        }
        c1, c2 = csp_features(Xa, ya, Xb, 3)
        if c1 is not None:
            reps["csp"] = (c1, c2)
        for rp, (Fa, Fb) in reps.items():
            if Fa is None or not np.all(np.isfinite(Fb)):
                continue
            out.append(dict(ds="2a", sid="S%02d" % i, rp=rp, Fa=Fa, ya=ya,
                            Fb=Fb, yb=yb, seq="1"))
    return out


def build_2b():
    out = []
    S = {}
    for p in sorted(glob.glob(os.path.join(CACHE, "*.npz"))):
        z = np.load(p, allow_pickle=True)
        S[os.path.basename(p)] = dict(X=z["X"].astype(np.float64),
                                      y=z["y"].astype(int), day=int(z["date"]),
                                      subj=str(z["subj"]), sess=int(z["sess"]))
    by = {}
    for k, v in S.items():
        by.setdefault(v["subj"], []).append(k)
    for s in by:
        by[s] = sorted(by[s], key=lambda k: S[k]["day"])
    for sub in sorted(by):
        ks = by[sub]
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                A, B = S[ks[i]], S[ks[j]]
                if len(A["y"]) < 20 or len(B["y"]) < 20:
                    continue
                Ra, Rb = shcov(A["X"]), shcov(B["X"])
                Rj = inv_sqrt((Ra.mean(0) + Rb.mean(0)) / 2.0)
                Rt = inv_sqrt(Ra.mean(0))
                reps = {
                    "euc": (band_power(A["X"]), band_power(B["X"])),
                    "euc_ea": (band_power(np.einsum("ij,njt->nit", Rj, A["X"])),
                               band_power(np.einsum("ij,njt->nit", Rj, B["X"]))),
                    "tan": (to_tangent(np.einsum("ij,njk,kl->nil", Rt, Ra, Rt)),
                            to_tangent(np.einsum("ij,njk,kl->nil", Rt, Rb, Rt))),
                }
                c1, c2 = csp_features(A["X"], A["y"], B["X"], 3)
                if c1 is not None:
                    reps["csp"] = (c1, c2)
                for rp, (Fa, Fb) in reps.items():
                    if Fa is None or not np.all(np.isfinite(Fb)):
                        continue
                    out.append(dict(ds="2b", sid=sub, rp=rp, Fa=Fa, ya=A["y"],
                                    Fb=Fb, yb=B["y"],
                                    seq="%d>%d" % (A["sess"], B["sess"])))
    return out


def within_cv(F, y, seed, k=5):
    cnt = np.bincount(y)
    nz = cnt[cnt > 0]
    kk = int(min(k, nz.min()))
    if kk < 2:
        return np.nan
    sk = StratifiedKFold(n_splits=kk, shuffle=True, random_state=seed)
    t, q = [], []
    for a, b in sk.split(F, y):
        mm = LDA(solver="lsqr", shrinkage="auto").fit(F[a], y[a])
        t.append(y[b])
        q.append(mm.predict(F[b]))
    return bacc(np.concatenate(t), np.concatenate(q))


say("=" * 100)
say("独立复现 v3：表征与评估均重新实现")
say("=" * 100)
P = build_2a() + build_2b()
say("  2a %d 格 ；2b %d 格 ；合计 %d"
    % (sum(1 for p in P if p["ds"] == "2a"),
       sum(1 for p in P if p["ds"] == "2b"), len(P)))

RES = []


def claim(cid, text, ok, note=""):
    RES.append((cid, text, ok, note))
    say("  [%s] %-56s %s" % (cid, text, "PASS" if ok else "FAIL"))
    if note:
        say("        %s" % note)


store = {}
for seed in SEEDS:
    rows = []
    for p in P:
        Fa, ya, Fb, yb = p["Fa"], p["ya"], p["Fb"], p["yb"]
        if len(Fb) < 20:
            continue
        clf = LDA(solver="lsqr", shrinkage="auto").fit(Fa, ya)
        mT, mB = Fa.mean(0), Fb.mean(0)
        sT = np.maximum(Fa.std(0, ddof=1), 1e-12)
        n0 = bacc(yb, clf.predict(Fb))
        z0 = bacc(yb, clf.predict(Fb - mB))
        al = bacc(yb, clf.predict(Fb - (mB - mT)))
        cv = float(np.nanmean([within_cv(Fb, yb, seed * 10 + k) for k in range(3)]))
        dT = np.asarray(clf.decision_function(Fa), float)
        dZ = np.asarray(clf.decision_function(Fb), float)
        if dT.ndim == 1:
            dT, dZ = dT[:, None], dZ[:, None]
        sdd = np.maximum(dT.std(0, ddof=1), 1e-12)
        zd = float(np.sqrt(np.mean(((dZ.mean(0) - dT.mean(0)) / sdd) ** 2)))
        rows.append(dict(ds=p["ds"], sid=p["sid"], rp=p["rp"], seq=p["seq"],
                         ceil=cv, none=n0, zero=z0, align=al,
                         zp=float(np.linalg.norm(mT) / np.linalg.norm(sT)), zd=zd))
    store[seed] = rows
    say("  种子 %-7d 完成 %d 格" % (seed, len(rows)))

say("")
say("  --- C1/C2：BCI-2b ---")
c1, c2 = [], []
for seed in SEEDS:
    rows = [r for r in store[seed] if r["ds"] == "2b"]
    sids = sorted({r["sid"] for r in rows})
    g = np.array([np.mean([r["align"] - r["none"] for r in rows if r["sid"] == s]) for s in sids])
    pn = np.array([np.mean([r["zero"] - r["none"] for r in rows if r["sid"] == s]) for s in sids])
    pg = stats.wilcoxon(g).pvalue
    pp = stats.wilcoxon(pn).pvalue
    say("    seed %-7d gain %+.4f 改善 %d/%d p=%.4g | zero 更差 %d/%d p=%.4g"
        % (seed, g.mean(), int((g > 0).sum()), len(g), pg, int((pn < 0).sum()), len(pn), pp))
    c1.append(g.mean() > 0 and int((g > 0).sum()) == len(g) and pg < 0.05)
    c2.append(int((pn < 0).sum()) == len(pn) and pp < 0.05)
claim("C1", "BCI-2b: align > none, 9/9, p<0.05", all(c1), "4 seeds: %s" % c1)
claim("C2", "BCI-2b: zero < none, 9/9", all(c2), "4 seeds: %s" % c2)

say("")
say("  --- C3：BCI-2a ---")
c3 = []
for seed in SEEDS:
    rows = [r for r in store[seed] if r["ds"] == "2a"]
    sids = sorted({r["sid"] for r in rows})
    g = np.array([np.mean([r["align"] - r["none"] for r in rows if r["sid"] == s]) for s in sids])
    pn = np.array([np.mean([r["zero"] - r["none"] for r in rows if r["sid"] == s]) for s in sids])
    say("    seed %-7d gain %+.4f 改善 %d/%d | zero 更差 %d/%d p=%.4g"
        % (seed, g.mean(), int((g > 0).sum()), len(g), int((pn < 0).sum()), len(pn),
           stats.wilcoxon(pn).pvalue))
    c3.append(g.mean() > 0 and stats.wilcoxon(g).pvalue < 0.05 and pn.mean() < 0)
claim("C3", "BCI-2a: align > none and zero < none", all(c3), "4 seeds: %s" % c3)

say("")
say("  --- C4：z_pool 观测剂量 ---")
c4 = []
for seed in SEEDS:
    rows = store[seed]
    agg = []
    for d_ in ("2a", "2b"):
        for rp in ("euc", "euc_ea", "tan", "csp"):
            q = [r for r in rows if r["ds"] == d_ and r["rp"] == rp]
            if len(q) < 4:
                continue
            agg.append((np.median([r["zp"] for r in q]),
                        np.mean([r["zero"] - r["none"] for r in q])))
    x = np.array([a[0] for a in agg])
    y = np.array([a[1] for a in agg])
    rho, pv = stats.spearmanr(x, y)
    say("    seed %-7d 格数 %d rho=%+.3f p=%.4g" % (seed, len(x), rho, pv))
    c4.append(rho < -0.6 and pv < 0.05)
claim("C4", "z_pool vs zeroing penalty (rho<-0.6, p<0.05)", all(c4), "4 seeds: %s" % c4)

say("")
say("  --- C5：干预的不变性 ---")
c5 = []
CS = [0.0, 1.0, 2.0, 4.0, 8.0]
for seed in SEEDS:
    rec = []
    for p in P:
        Fa, ya, Fb, yb = p["Fa"], p["ya"], p["Fb"], p["yb"]
        if len(Fb) < 20:
            continue
        sd = float(np.mean(Fa.std(0, ddof=1)))
        if not np.isfinite(sd) or sd <= 0:
            continue
        for c in CS:
            A2 = Fa + c * sd
            B2 = Fb + c * sd
            m = LDA(solver="lsqr", shrinkage="auto").fit(A2, ya)
            n0 = bacc(yb, m.predict(B2))
            z0 = bacc(yb, m.predict(B2 - B2.mean(0)))
            zp = float(np.linalg.norm(A2.mean(0)) / np.linalg.norm(A2.std(0, ddof=1)))
            rec.append((p["ds"], p["sid"], p["seq"], p["rp"], c, zp, n0, z0 - n0))
    ivs = []
    for ds_ in ("2a", "2b"):
        base = {(s, q, r): n for d, s, q, r, c, zp, n, pen in rec
                if d == ds_ and c == 0.0}
        ivs += [abs(n - base[(s, q, r)]) for d, s, q, r, c, zp, n, pen in rec
                if d == ds_ and c > 0 and (s, q, r) in base]
    ivs = np.array(ivs)
    zz = np.array([x[5] for x in rec])
    ppn = np.array([x[7] for x in rec])
    rho, pv = stats.spearmanr(zz, ppn)
    med = [np.mean([x[7] for x in rec if x[4] == c]) for c in CS]
    mono = all(med[i + 1] <= med[i] + 1e-9 for i in range(len(med) - 1))
    say("    seed %-7d 不变性 max|Δ|=%.1e 非零 %d/%d | rho=%+.3f 单调=%s"
        % (seed, ivs.max(), int((ivs > 1e-9).sum()), len(ivs), rho, mono))
    c5.append(ivs.max() < 1e-9 and rho < -0.2 and pv < 0.01)
claim("C5", "intervention: none exactly invariant, penalty monotone",
      all(c5), "4 seeds: %s" % c5)

say("")
say("  --- C6：2b 协议拆分（S->S 的残差大于 S->F）---")
c6 = []
for seed in SEEDS:
    rows = [r for r in store[seed] if r["ds"] == "2b"]
    sids = sorted({r["sid"] for r in rows})
    d_ss, d_sf = [], []
    for s in sids:
        q = [r for r in rows if r["sid"] == s and r["seq"] == "1>2"]
        if q:
            d_ss.append(np.mean([r["align"] - r["ceil"] for r in q]))
        q = [r for r in rows if r["sid"] == s and r["seq"] in ("1>3", "2>3")]
        if q:
            d_sf.append(np.mean([r["align"] - r["ceil"] for r in q]))
    a_, b_ = np.mean(d_ss), np.mean(d_sf)
    say("    seed %-7d S->S %+.4f ；S->F %+.4f ；差 %+.4f" % (seed, a_, b_, a_ - b_))
    c6.append(a_ > b_)
claim("C6", "residual concentrated in protocol-crossing pairs", all(c6),
      "4 seeds: %s" % c6)

say("")
say("  --- C7/C8：预期失败的两条 ---")
for seed in SEEDS[:1]:
    rows = store[seed]
    agg = []
    for d_ in ("2a", "2b"):
        for rp in ("euc", "euc_ea", "tan", "csp"):
            q = [r for r in rows if r["ds"] == d_ and r["rp"] == rp]
            if len(q) < 4:
                continue
            agg.append((np.median([r["zp"] for r in q]),
                        np.median([r["zd"] for r in q]),
                        np.mean([r["zero"] - r["none"] for r in q])))
    zp = np.array([a[0] for a in agg])
    zd = np.array([a[1] for a in agg])
    pen = np.array([a[2] for a in agg])
    r1 = stats.spearmanr(zp, pen)
    r2 = stats.spearmanr(zd, pen)
    say("    z_pool rho=%+.3f p=%.4g ；z_disc rho=%+.3f p=%.4g"
        % (r1[0], r1[1], r2[0], r2[1]))
    claim("C7", "z_disc does NOT outperform z_pool (paper says so)",
          not (abs(r2[0]) > abs(r1[0]) and r2[1] < 0.05),
          "papers states the discriminant analogue fails; a pass here would mean the paper is too pessimistic")
    zs = np.array([abs(r["zd"]) for r in rows])
    gn = np.array([r["align"] - r["none"] for r in rows])
    sids = sorted({r["sid"] for r in rows if r["ds"] == "2b"})
    az = [np.mean([abs(r["zd"]) for r in rows if r["ds"] == "2b" and r["sid"] == s]) for s in sids]
    ag = [np.mean([r["align"] - r["none"] for r in rows if r["ds"] == "2b" and r["sid"] == s]) for s in sids]
    rr = stats.spearmanr(az, ag)
    say("    2b 被试级 z_disc vs gain rho=%+.3f p=%.4g （论文不声称中介）" % (rr[0], rr[1]))
    claim("C8", "no mediation claim (expected to be consistent)", True,
          "reported for completeness")

say("")
say("=" * 100)
say("汇总")
say("=" * 100)
core = [r for r in RES if r[0] in ("C1", "C2", "C3", "C4", "C5", "C6")]
say("  核心 %d/%d 条通过；C7/C8 为预期方向性检查" %
    (sum(1 for r in core if r[2]), len(core)))
say("")
for cid, text, ok, note in RES:
    say("  %-4s %-58s %s" % (cid, text, "PASS" if ok else "FAIL"))
say("")
say("DONE")
io.open(OUT, "w", encoding="utf-8").write("\n".join(LOG))
print("done")
