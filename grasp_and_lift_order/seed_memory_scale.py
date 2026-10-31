# -*- coding: utf-8 -*-
"""SEED: correction gain as a function of the memory scale of the mean estimator."""
import glob, json, os, re, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CACHE = os.environ.get('BSPC_CACHE_SEED', r'G:\Work_work\math\EEG\local_analysis\cache_seed')
BLOCK = 15
WINDOWS = (5, 10, 25, 50, 100, 200, 400)
ALPHAS = (0.2, 0.1, 0.05, 0.02, 0.01)
OUT = os.path.join(os.environ.get('BSPC_RESULTS', r'G:\Work_work\math\EEG\paper_v8\results'), 'seed_memory_scale_coldstart.json')


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
                keep = np.arange(n) >= BLOCK
                rec = {'subj': sub}
                p0 = clf.classes_[np.argmax(S, 1)]
                base_ba = bas(yB[keep], p0[keep])
                for w in WINDOWS:
                    m = np.zeros((n, K))
                    c = np.cumsum(d_t, axis=0)
                    cnt = np.arange(1, n + 1)[:, None]
                    cum = np.zeros((n, K)); cum[1:] = c[:-1] / cnt[:-1]
                    for t in range(BLOCK, n):
                        m[t] = cum[t] if w is None else d_t[max(0, t - w):t].mean(0)
                    pred = clf.classes_[np.argmax(S - m, 1)]
                    rec['w%d' % w] = float(bas(yB[keep], pred[keep]) - base_ba)
                for a in ALPHAS:
                    m = np.zeros((n, K))
                    run = d_t[:BLOCK].mean(0)          # prime with the warm-up block, as the windows do
                    for t in range(BLOCK, n):
                        m[t] = run.copy()
                        run = (1 - a) * run + a * d_t[t]
                    pred = clf.classes_[np.argmax(S - m, 1)]
                    rec['a%.2f' % a] = float(bas(yB[keep], pred[keep]) - base_ba)
                rows.append(rec)
    json.dump(rows, open(OUT, 'w'))
    print('cells', len(rows))
    for w in WINDOWS:
        v = np.array([r['w%d' % w] for r in rows])
        print('window %3d   %+0.4f   positive %d/%d' % (w, v.mean(), int((v > 0).sum()), len(v)))
    for a in ALPHAS:
        v = np.array([r['a%.2f' % a] for r in rows])
        print('alpha  %.2f  %+0.4f   positive %d/%d' % (a, v.mean(), int((v > 0).sum()), len(v)))


if __name__ == '__main__':
    main()