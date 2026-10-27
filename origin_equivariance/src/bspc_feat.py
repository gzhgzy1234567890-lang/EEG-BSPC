# -*- coding: utf-8 -*-
"""共用特征层：2a / 2b 的表征构建与缓存。

修过的实现要点（每一条都对应一次真实 bug）：
  * EA 作用在**原始信号**上且只乘一次（R @ X），不是 R @ C @ R
  * CSP 滤波器数受通道数约束 mm = min(m, ch//2)，否则 3 导会得到重复滤波器
  * tr(Sigma) 用 sum(dd^2) * h / 2；写成 mean(dd^2)*h/4 会低估 2D 倍
  * tag 唯一化用 "被试:起>终"，下游一律 split(":")[0] 取被试，禁止 split(">")[0]
"""
import os
import glob
import numpy as np
from scipy.linalg import eigh
import scipy.io as sio
from scipy.signal import butter, filtfilt

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.environ.get("BSPC_OUT", os.path.dirname(HERE))
DATA = os.environ.get("BSPC_DATA", r"E:\data")
CACHE2B = os.environ.get("BSPC_CACHE", os.path.join(D, "cache_2b"))
CACHE2A = os.path.join(D, "cache_2a")
FS = 250

_b1, _b2 = butter(4, [8.0 / (FS / 2), 30.0 / (FS / 2)], btype="band")


def bacc(y, p):
    u = np.unique(y)
    if len(u) < 2:
        return np.nan
    return float(np.mean([(p[y == c] == c).mean() for c in u]))


def covs(X, shrink=1e-3):
    n, ch, _ = X.shape
    out = np.empty((n, ch, ch))
    for i in range(n):
        C = np.atleast_2d(np.cov(X[i]))
        s = np.trace(C) / ch
        out[i] = (1 - shrink) * C + shrink * s * np.eye(ch)
    return out


def msqrt_inv(C, eps=1e-8):
    """C 必须是单个 (ch,ch) 矩阵。传堆栈进来会静默算出错误形状。"""
    C = np.asarray(C, float)
    if C.ndim == 3:
        C = C.mean(0)
    w, V = eigh(C)
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
    ch = Ctr.shape[1]
    mm = int(min(m, max(1, ch // 2)))
    Cs = [Ctr[ytr == c].mean(0) for c in cls]
    Cc = np.mean(Cs, 0)
    w, V = eigh(Cs[0], Cc)
    idx = np.argsort(w)
    sel = np.concatenate([idx[:mm], idx[-mm:]])
    if len(cls) == 2:
        sel = np.array(sorted(set(sel.tolist())), dtype=int)
    W = V[:, sel]

    def proj(X):
        Z = np.einsum("nct,ck->nkt", X, W)
        return np.log(np.var(Z, axis=2) + 1e-12)

    return proj(Xtr), proj(Xte)


# ---------------- 2a ----------------

def load_bci(path):
    """BCICIV-2a 单文件。窗口取 trial 起点后 2.0-6.0 s。

    注意：官方时序里 cue 出现在 trial 起点后 2 s，所以这等价于 cue 后
    0-4 s，而不是"cue 后 2-6 s"。论文里必须写清楚参照点。
    """
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
        X = filtfilt(_b1, _b2, X, axis=0)
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


def build_2a(verbose=True):
    if not os.path.isdir(CACHE2A):
        os.makedirs(CACHE2A)
    root = os.path.join(DATA, "BCICIV-2a-mat")
    out = {}
    for i in range(1, 10):
        f = os.path.join(CACHE2A, "S%02d.npz" % i)
        if os.path.exists(f):
            z = np.load(f, allow_pickle=True)
            out[i] = dict({k: z[k] for k in z.files})
            continue
        pT = os.path.join(root, "A%02dT.mat" % i)
        pE = os.path.join(root, "A%02dE.mat" % i)
        if not (os.path.exists(pT) and os.path.exists(pE)):
            continue
        XT, yT = load_bci(pT)
        XE, yE = load_bci(pE)
        if not len(XT) or not len(XE) or len(np.unique(yE)) < 2:
            continue
        CT, CE = covs(XT), covs(XE)
        Rj = msqrt_inv((CT.mean(0) + CE.mean(0)) / 2.0)
        Rt = msqrt_inv(CT.mean(0))
        d = dict(ya=yT, yb=yE)
        d["A_euc"], d["B_euc"] = logpow(XT), logpow(XE)
        d["A_euc_ea"] = logpow(np.einsum("ij,njt->nit", Rj, XT))
        d["B_euc_ea"] = logpow(np.einsum("ij,njt->nit", Rj, XE))
        d["A_tan"] = tangent(np.einsum("ij,njk,kl->nil", Rt, CT, Rt))
        d["B_tan"] = tangent(np.einsum("ij,njk,kl->nil", Rt, CE, Rt))
        cT, cE = csp_feat(XT, yT, XE, 3)
        d["A_csp"], d["B_csp"] = cT, cE
        np.savez(f, **d)
        out[i] = d
        if verbose:
            print("  2a S%02d  nT=%d nE=%d" % (i, len(yT), len(yE)))
    return out


def pairs_2a():
    C = build_2a()
    P = []
    for i in sorted(C):
        d = C[i]
        for rep in ("euc", "euc_ea", "tan", "csp"):
            A = d.get("A_" + rep)
            B = d.get("B_" + rep)
            if A is None or B is None:
                continue
            if not (np.all(np.isfinite(A)) and np.all(np.isfinite(B))):
                continue
            P.append(dict(ds="2a", tag="S%02d" % i, rep=rep,
                          A=np.asarray(A, float), ya=np.asarray(d["ya"], int),
                          B=np.asarray(B, float), yb=np.asarray(d["yb"], int)))
    return P


# ---------------- 2b ----------------

def pairs_2b():
    S = {}
    for p in sorted(glob.glob(os.path.join(CACHE2B, "*.npz"))):
        z = np.load(p, allow_pickle=True)
        S[os.path.basename(p).replace(".npz", "")] = dict(
            X=z["X"].astype(np.float64), y=z["y"].astype(int),
            date=int(z["date"]), subj=str(z["subj"]), sess=int(z["sess"]))
    bysub = {}
    for k, v in S.items():
        bysub.setdefault(v["subj"], []).append(k)
    for s in bysub:
        bysub[s] = sorted(bysub[s], key=lambda k: S[k]["date"])
    P = []
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
                Rj = msqrt_inv((CA.mean(0) + CB.mean(0)) / 2.0)
                Rt = msqrt_inv(CA.mean(0))
                reps = {}
                reps["euc"] = (logpow(A), logpow(B))
                reps["euc_ea"] = (logpow(np.einsum("ij,njt->nit", Rj, A)),
                                  logpow(np.einsum("ij,njt->nit", Rj, B)))
                reps["tan"] = (tangent(np.einsum("ij,njk,kl->nil", Rt, CA, Rt)),
                               tangent(np.einsum("ij,njk,kl->nil", Rt, CB, Rt)))
                cT, cE = csp_feat(A, ya, B, 3)
                reps["csp"] = (cT, cE)
                tag = "%s:%d>%d" % (sub, S[ka]["sess"], S[kb]["sess"])
                gap = abs(S[kb]["date"] - S[ka]["date"])
                for rep, (FA, FB) in reps.items():
                    if FA is None or FB is None:
                        continue
                    if not (np.all(np.isfinite(FA)) and np.all(np.isfinite(FB))):
                        continue
                    P.append(dict(ds="2b", tag=tag, rep=rep, seq="%d>%d" % (S[ka]["sess"], S[kb]["sess"]),
                                  gap=gap, A=np.asarray(FA, float), ya=ya,
                                  B=np.asarray(FB, float), yb=yb))
    return P


def all_pairs():
    return pairs_2a() + pairs_2b()


def subject_of(tag):
    """2b 的 tag 是 'S01:1>2'，被试必须取冒号前；2a 是 'S01'。"""
    return str(tag).split(":")[0]
