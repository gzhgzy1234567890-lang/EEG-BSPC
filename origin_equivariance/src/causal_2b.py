# -*- coding: utf-8 -*-
"""BCI-IV-2b: causal vs non-causal filter x source-only / both-session alignment, three forward pairs."""
import glob, json, os, re, sys
import numpy as np
import mne
from scipy.linalg import eigh
from scipy.signal import butter, filtfilt, lfilter
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
mne.set_log_level('ERROR')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
DATA = os.environ.get('BSPC_DATA', r'E:\data')
OUT = os.environ.get('BSPC_RESULTS', r'G:\Work_work\math\EEG\paper_v8\results')
FS, BLOCK = 250, 15
T0, T1 = 0.5, 3.5
CH = ['EEG:C3', 'EEG:Cz', 'EEG:C4']
b_, a_ = butter(4, [8.0 / (FS / 2), 30.0 / (FS / 2)], btype='band')
PAIRS = [(1, 2), (1, 3), (2, 3)]


def load(path, causal):
    raw = mne.io.read_raw_gdf(path, preload=True, verbose='ERROR')
    raw.pick_channels(CH, ordered=True)
    X = raw.get_data().astype(np.float64)
    X = lfilter(b_, a_, X, axis=1) if causal else filtfilt(b_, a_, X, axis=1)
    ann = raw.annotations
    ons = ann.onset
    desc = np.array([str(x) for x in ann.description])
    rej = set(np.round(ons[desc == '1023'], 3).tolist())
    st = np.round(ons[desc == '768'], 3)
    bad = set()
    for r in rej:
        near = st[np.abs(st - r) < 0.01]
        bad.update(near.tolist())
    st = np.round(ons[desc == '768'], 3)
    rej_trial_starts = set()
    for r in rej:
        near = st[np.abs(st - r) < 0.01]
        if len(near):
            rej_trial_starts.update(near.tolist())
        else:
            rej_trial_starts.add(r)
    cues = [(o, 0) for o in ons[desc == '769']] + [(o, 1) for o in ons[desc == '770']]
    cues = sorted(cues, key=lambda t: t[0])
    i0, i1 = int(T0 * FS), int(T1 * FS)
    segs, ys = [], []
    for o, lab in cues:
        prev = st[st <= o + 1e-6]
        if len(prev) and prev[-1] in rej_trial_starts:
            continue
        a = int(round(o * FS)) + i0
        b2 = int(round(o * FS)) + i1
        if b2 > X.shape[1] or a < 0:
            continue
        segs.append(X[:, a:b2].astype(np.float32))
        ys.append(lab)
    if not segs:
        return np.zeros((0, 3, i1 - i0), np.float32), np.zeros(0, int)
    return np.stack(segs, 0).astype(np.float64), np.array(ys)


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


def logpow(segs, nwin=4):
    n, ch, T = segs.shape
    w = T // nwin
    out = np.empty((n, ch * nwin))
    for i in range(n):
        pv = np.array([np.mean(segs[i][:, k * w:(k + 1) * w] ** 2, 1) for k in range(nwin)])
        out[i] = np.log(pv.ravel() + 1e-12)
    return out


def tangent(Cs):
    n, ch, _ = Cs.shape
    iu = np.triu_indices(ch)
    Z = np.empty((n, len(iu[0])))
    for i in range(n):
        w, V = np.linalg.eigh(Cs[i])
        w = np.maximum(w, 1e-12)
        Z[i] = (V @ np.diag(np.log(w)) @ V.T)[iu]
    return Z


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
    SA = clf.decision_function(A)
    if SA.ndim == 1:
        SA = np.column_stack([-SA, SA])
    Fm = np.eye(K) - np.ones((K, K)) / K
    n = len(yb)
    blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
    d_b = np.array([Fm @ (S[a:b].mean(0) - SA.mean(0)) for a, b in blocks])
    corr = np.zeros_like(S)
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            corr[a:b] = d_b[:k].mean(0)
    keep = slice(BLOCK, n)
    p0 = clf.classes_[np.argmax(S, 1)]
    p1 = clf.classes_[np.argmax(S - corr, 1)]
    return bas(yb[keep], p0[keep]), bas(yb[keep], p1[keep])


def features(XT, yT, XE, ea):
    CT, CE = covs(XT), covs(XE)
    Rj = msqrt_inv((CT.mean(0) + CE.mean(0)) / 2.0) if ea == 'archived' else msqrt_inv(CT.mean(0))
    Rt = msqrt_inv(CT.mean(0))
    return {
        'euc': (logpow(XT), logpow(XE)),
        'euc_ea': (logpow(np.einsum('ij,njt->nit', Rj, XT)), logpow(np.einsum('ij,njt->nit', Rj, XE))),
        'tan': (tangent(np.einsum('ij,njk,kl->nil', Rt, CT, Rt)), tangent(np.einsum('ij,njk,kl->nil', Rt, CE, Rt))),
        'csp': csp_feat(XT, yT, XE, 3),
    }


def main():
    root = os.path.join(DATA, 'BCICIV-2b')
    rows = []
    for s in range(1, 10):
        for (p, q) in PAIRS:
            fT = os.path.join(root, 'B%02d%02dT.gdf' % (s, p))
            fE = os.path.join(root, 'B%02d%02dT.gdf' % (s, q))
            if not (os.path.exists(fT) and os.path.exists(fE)):
                continue
            rec = {'subj': s, 'pair': '%d>%d' % (p, q)}
            for mode, causal, ea in (('causal_so', True, 'source'), ('causal_arch', True, 'archived'),
                                     ('noncausal_so', False, 'source'), ('noncausal', False, 'archived')):
                XT, yT = load(fT, causal)
                XE, yE = load(fE, causal)
                if len(np.unique(yT)) < 2 or len(np.unique(yE)) < 2 or len(yE) < 2 * BLOCK:
                    continue
                F = features(XT, yT, XE, ea)
                for rep in F:
                    b0, b1 = run_cell(F[rep][0], yT, F[rep][1], yE)
                    rec['%s|%s|none' % (mode, rep)] = float(b0)
                    rec['%s|%s|lam1' % (mode, rep)] = float(b1)
            rows.append(rec)
            print(rec['subj'], rec['pair'], 'done', flush=True)
            json.dump(rows, open(os.path.join(OUT, 'causal_2b.json'), 'w'))
    print('cells', len(rows))


if __name__ == '__main__':
    main()