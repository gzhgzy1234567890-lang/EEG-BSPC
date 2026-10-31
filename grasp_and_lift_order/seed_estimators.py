# -*- coding: utf-8 -*-
"""SEED: five estimators under one protocol (same scoring set, same warm-up)."""
import glob, json, os, re, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CACHE = os.environ.get('BSPC_CACHE_SEED', r'G:\Work_work\math\EEG\local_analysis\cache_seed')
BLOCK = 15
OUT = r'G:\Work_work\math\EEG\paper_v8\results\seed_estimators.json'


def load():
    by = {}
    for f in sorted(glob.glob(os.path.join(CACHE, '*.npz'))):
        m = re.match(r'(\d+)_(\d+)\.npz', os.path.basename(f))
        if not m:
            continue
        z = np.load(f, allow_pickle=True)
        by.setdefault(int(m.group(1)), []).append((int(m.group(2)), z['X'].astype(float), z['y'].astype(int)))
    return by


def main():
    by = load(); rows = []
    for sub, sess in sorted(by.items()):
        sess = sorted(sess)
        for i in range(len(sess)):
            for j in range(i + 1, len(sess)):
                _, XA, yA = sess[i]; _, XB, yB = sess[j]
                clf = LDA(solver='lsqr', shrinkage='auto').fit(XA, yA)
                K = len(clf.classes_)
                W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
                Fm = np.eye(K) - np.ones((K, K)) / K
                muA = XA.mean(0)
                S = clf.decision_function(XB)
                if S.ndim == 1:
                    S = np.column_stack([-S, S])
                n = len(yB)
                d_t = (XB - muA) @ W.T @ Fm.T
                blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
                d_b = np.array([d_t[a:b].mean(0) for a, b in blocks])
                est = {}
                m = np.zeros((n, K))
                for k, (a, b) in enumerate(blocks):
                    if k > 0:
                        m[a:b] = d_b[:k].mean(0)
                est['block'] = m
                c = np.cumsum(d_t, axis=0); idx = np.arange(1, n + 1)[:, None]
                m = np.zeros((n, K)); m[1:] = c[:-1] / idx[:-1]; m[:BLOCK] = 0.0
                est['cumulative'] = m
                m = np.zeros((n, K))
                for t in range(n):
                    if t >= BLOCK:
                        m[t] = d_t[max(0, t - 50):t].mean(0)
                est['window50'] = m
                m = np.zeros((n, K)); run = np.zeros(K)
                for t in range(n):
                    if t >= BLOCK:
                        m[t] = run.copy()
                        run = 0.95 * run + 0.05 * d_t[t]
                est['exponential'] = m
                V = d_b.var(axis=0, ddof=1).sum() if len(d_b) > 2 else 1e-12
                m = np.zeros((n, K))
                for k, (a, b) in enumerate(blocks):
                    if k > 0:
                        dbar = d_b[:k].mean(0)
                        lam = float(np.dot(dbar, dbar) / (np.dot(dbar, dbar) + max(V, 1e-12) / max(k, 1)))
                        m[a:b] = lam * dbar
                est['varratio'] = m
                keep = np.arange(n) >= BLOCK
                rec = {'subj': sub}
                for name, mm in est.items():
                    p0 = clf.classes_[np.argmax(S, 1)]
                    p1 = clf.classes_[np.argmax(S - mm, 1)]
                    rec[name] = float(bas(yB[keep], p1[keep]) - bas(yB[keep], p0[keep]))
                rec['none'] = float(bas(yB[keep], p0[keep]))
                rows.append(rec)
    json.dump(rows, open(OUT, 'w'))
    print('cells', len(rows))
    for name in ('block', 'cumulative', 'window50', 'exponential', 'varratio'):
        v = np.array([r[name] for r in rows])
        print('%-12s %+0.4f  positive %d/%d' % (name, v.mean(), int((v > 0).sum()), len(v)))


if __name__ == '__main__':
    main()