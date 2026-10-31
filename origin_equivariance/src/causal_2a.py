# -*- coding: utf-8 -*-
"""Unified source-only, past-only test on BCI-IV-2a: causal vs non-causal filtering, delta_protocol."""
import argparse, json, os, sys
import numpy as np
import scipy.io as sio
from scipy.linalg import eigh
from scipy.signal import butter, filtfilt, lfilter
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
DATA = os.environ.get('BSPC_DATA', r'E:\data')
OUT = os.environ.get('BSPC_RESULTS', r'G:\Work_work\math\EEG\paper_v8\results')
FS = 250
BLOCK = 15
b1, b2 = butter(4, [8.0 / (FS / 2), 30.0 / (FS / 2)], btype='band')


def load_bci(path, causal):
    m = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
    runs = np.atleast_1d(m['data'])
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
        X = lfilter(b1, b2, X, axis=0) if causal else filtfilt(b1, b2, X, axis=0)
        i0, i1 = int(2.0 * FS), int(6.0 * FS)
        for t, lab in zip(tr, yy):
            if lab <= 0:
                continue
            sg = X[t + i0:t + i1]
            if sg.shape[0] < (i1 - i0):
                continue
            segs.append(sg.T)
            ys.append(int(lab))
    return np.array(segs), np.array(ys)


def covs(X, shrink=1e-3):
    n, ch, _ = X.shape
    out = np.empty((n, ch, ch))
    for i in range(n):
        C = np.atleast_2d(np.cov(X[i]))
        s = np.trace(C) / ch
        out[i] = (1 - shrink) * C + shrink * s * np.eye(ch)
    return out


def msqrt_inv(C, eps=1e-8):
    C = np.asarray(C, float)
    if C.ndim == 3:
        C = C.mean(0)
    w, V = np.linalg.eigh(C)
    w = np.maximum(w, eps)
    return V @ np.diag(w ** -0.5) @ V.T


def tangent(Cs):
    n, ch, _ = Cs.shape
    iu = np.triu_indices(ch)
    Z = np.empty((n, len(iu[0])))
    for i in range(n):
        w, V = np.linalg.eigh(Cs[i])
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
    sel = np.array(sorted(set(sel.tolist())), dtype=int)
    W = V[:, sel]
    proj = lambda X: np.log(np.var(np.einsum('nct,ck->nkt', X, W), axis=2) + 1e-12)
    return proj(Xtr), proj(Xte)


def run_cell(A, ya, B, yb):
    clf = LDA(solver='lsqr', shrinkage='auto').fit(A, ya)
    K = len(clf.classes_)
    S = clf.decision_function(B)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    Fm = np.eye(K) - np.ones((K, K)) / K
    n = len(yb)
    blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
    d_b = np.array([Fm @ (S[a:b].mean(0)) for a, b in blocks])
    corr = np.zeros_like(S)
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            corr[a:b] = d_b[:k].mean(0)
    p0 = clf.classes_[np.argmax(S, 1)]
    p1 = clf.classes_[np.argmax(S - corr, 1)]
    keep = slice(BLOCK, n)
    return bas(yb[keep], p0[keep]), bas(yb[keep], p1[keep])


def features(XT, yT, XE, mode):
    CT, CE = covs(XT), covs(XE)
    Rj = msqrt_inv((CT.mean(0) + CE.mean(0)) / 2.0) if mode == 'archived' else msqrt_inv(CT.mean(0))
    Rt = msqrt_inv(CT.mean(0))
    out = {}
    out['euc'] = (logpow(XT), logpow(XE))
    out['euc_ea'] = (logpow(np.einsum('ij,njt->nit', Rj, XT)), logpow(np.einsum('ij,njt->nit', Rj, XE)))
    out['tan'] = (tangent(np.einsum('ij,njk,kl->nil', Rt, CT, Rt)), tangent(np.einsum('ij,njk,kl->nil', Rt, CE, Rt)))
    out['csp'] = csp_feat(XT, yT, XE, 3)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()
    root = os.path.join(DATA, 'BCICIV-2a-mat')
    rows = []
    for i in range(1, 10):
        if args.limit and i > args.limit:
            break
        pT = os.path.join(root, 'A%02dT.mat' % i)
        pE = os.path.join(root, 'A%02dE.mat' % i)
        if not (os.path.exists(pT) and os.path.exists(pE)):
            continue
        rec = {'subj': i}
        for mode, causal, ea in (('causal_so', True, 'source'), ('causal_arch', True, 'archived'), ('noncausal', False, 'archived')):
            XT, yT = load_bci(pT, causal)
            XE, yE = load_bci(pE, causal)
            F = features(XT, yT, XE, ea)
            for rep in F:
                b0, b1_ = run_cell(F[rep][0], yT, F[rep][1], yE)
                rec['%s|%s|none' % (mode, rep)] = float(b0)
                rec['%s|%s|lam1' % (mode, rep)] = float(b1_)
        rows.append(rec)
        print('subject', i, 'done', flush=True)
        json.dump(rows, open(os.path.join(OUT, 'causal_2a.json'), 'w'))
    print('subjects', len(rows))


if __name__ == '__main__':
    main()