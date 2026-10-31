# -*- coding: utf-8 -*-
"""Four causal estimators plus the predictive rule, on the acquisition-order grasp-and-lift cache."""
import glob, json, os, re, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CACHE = r'G:\Work_work\math\EEG\local_analysis\cache_gal_time'
BLOCK = 15
LAM = 1.0


def load():
    out = {}
    for f in sorted(glob.glob(os.path.join(CACHE, '*.npz'))):
        m = re.match(r'(subj\d+)_series(\d+)\.npz', os.path.basename(f))
        z = np.load(f)
        out[(m.group(1), int(m.group(2)))] = (z['F'], z['y'])
    return out


def estimates(Fb, yb, blocks, W, Fm, muA):
    n = len(yb)
    D = np.array([Fm @ (W @ (Fb[a:b].mean(0) - muA)) for a, b in blocks])
    nblk = len(blocks)
    def running_mean(kind):
        bm = np.zeros((n, D.shape[1]))
        for k, (a, b) in enumerate(blocks):
            if k == 0:
                continue
            if kind == 'cum':
                m = D[:k].mean(0)
            elif kind == 'win':
                m = D[max(0, k - 50 // BLOCK):k].mean(0)
            elif kind == 'exp':
                w = np.array([(1 - 0.05) ** (k - 1 - i) for i in range(k)])
                m = (D[:k] * w[:, None]).sum(0) / w.sum()
            bm[a:b] = m
        return bm
    out = {}
    for kind in ('cum', 'win', 'exp'):
        bm = running_mean(kind)
        out[kind] = bm
    # completed-block mean
    bm = np.zeros((n, D.shape[1]))
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            bm[a:b] = D[:k].mean(0)
    out['block'] = bm
    # variance-ratio weight
    dbar = D[:-1].mean(0) if nblk > 1 else D.mean(0)
    if nblk > 2:
        Vd = float(((D[1:] - D[1:].mean(0)) ** 2).mean())
        lam = float(np.dot(dbar, dbar) / (np.dot(dbar, dbar) + D.shape[1] * Vd / max(1, nblk - 1) + 1e-12))
    else:
        lam = 0.0
    out['eq9'] = out['block'] * lam
    # predictive, leave-one-block-out
    lam_hat = 0.0
    if nblk >= 3:
        num = 0.0; den = 0.0
        for b in range(1, nblk):
            others = np.delete(D, b, axis=0)
            m = others.mean(0)
            num += float(np.dot(D[b], m)); den += float(np.dot(m, m))
        lam_hat = min(1.0, max(0.0, num / den)) if den > 1e-15 else 0.0
    out['pred'] = out['block'] * lam_hat
    return out


data = load()
subs = {}
for (s, i) in data:
    subs.setdefault(s, []).append(i)
rows = []
for s, idx in sorted(subs.items()):
    idx = sorted(idx)
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            Fa, ya = data[(s, idx[a])]
            Fb, yb = data[(s, idx[b])]
            clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
            kc = len(clf.classes_)
            W = clf.coef_ if kc > 2 else np.vstack([-clf.coef_, clf.coef_])
            Fm = np.eye(kc) - np.ones((kc, kc)) / kc
            muA = Fa.mean(0)
            S = clf.decision_function(Fb)
            if S.ndim == 1:
                S = np.column_stack([-S, S])
            n = len(yb)
            blocks = [(a2, min(a2 + BLOCK, n)) for a2 in range(0, n, BLOCK)]
            est = estimates(Fb, yb, blocks, W, Fm, muA)
            base = bas(yb[BLOCK:], clf.classes_[np.argmax(S, 1)][BLOCK:])
            rec = {'subj': s, 'none': base}
            for k, bm in est.items():
                pred = clf.classes_[np.argmax(S - LAM * bm, 1)]
                rec[k] = bas(yb[BLOCK:], pred[BLOCK:])
            rows.append(rec)
keys = ['none', 'cum', 'win', 'exp', 'block', 'eq9', 'pred']
A = {k: np.array([r[k] for r in rows]) for k in keys}
print('cells', len(rows))
for k in keys:
    d = A[k] - A['none']
    print('%-6s BA %.4f  delta %+.4f' % (k, A[k].mean(), d.mean()))
per = {}
for r in rows:
    per.setdefault(r['subj'], []).append(r)
print('subject-level delta (mean over subjects):')
for k in keys[1:]:
    v = np.array([np.mean([c[k] - c['none'] for c in cs]) for cs in per.values()])
    print('  %-6s %+.4f  (min %+.4f max %+.4f)' % (k, v.mean(), v.min(), v.max()))