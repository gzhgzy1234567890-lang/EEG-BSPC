# -*- coding: utf-8 -*-
"""Same label-free statistics on SEED, to test whether a sleep-fitted gate keeps the SEED gain."""
import glob, json, os, re, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
D = r'G:\Work_work\math\EEG\local_analysis\cache_seed'
BLOCK = 15
OUT = r'G:\Work_work\math\EEG\paper_v8\results\seed_risk.json'


def load():
    by = {}
    for f in sorted(glob.glob(os.path.join(D, '*.npz'))):
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
                blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
                d_b = np.array([Fm @ (W @ (XB[a:b].mean(0) - muA)) for a, b in blocks])
                bm = np.zeros((n, K))
                for k, (a, b) in enumerate(blocks):
                    if k > 0:
                        bm[a:b] = d_b[:k].mean(0)
                p0 = clf.classes_[np.argmax(S, 1)]
                p1 = clf.classes_[np.argmax(S - bm, 1)]
                keep = np.arange(n) >= BLOCK
                Ss = np.sort(S, axis=1); margin = Ss[:, -1] - Ss[:, -2]
                run = np.zeros(K); expo = np.zeros((n, K))
                for t in range(n):
                    expo[t] = run
                    if t >= BLOCK:
                        run = 0.95 * run + 0.05 * (Fm @ (W @ (XB[t] - muA)))
                rows.append({'subj': sub, 'delta': float(bas(yB[keep], p1[keep]) - bas(yB[keep], p0[keep])),
                             'flip': float(np.mean(p0[keep] != p1[keep])),
                             'dmargin': float(np.mean(np.abs((S - bm)[keep] - S[keep]).max(1))),
                             'dnorm': float(np.mean(np.linalg.norm(bm[keep], axis=1))),
                             'disagree': float(np.linalg.norm((bm - expo)[keep].mean(0)) / max(np.linalg.norm(bm[keep].mean(0)), 1e-9))})
    json.dump(rows, open(OUT, 'w'))
    d = np.array([r['delta'] for r in rows])
    print('SEED cells %d  mean raw gain %+0.4f' % (len(rows), d.mean()))
    for key, t in (('flip', 0.044), ('dmargin', 2.041), ('dnorm', 2.719)):
        g = np.array([r['delta'] if r[key] < t else 0.0 for r in rows])
        fired = np.mean([r[key] < t for r in rows])
        print('gate %-8s t=%.3f  keeps %+0.4f (%.0f%% of the gain), fires on %.0f%% of cells' % (key, t, g.mean(), 100 * g.mean() / d.mean(), 100 * fired))


if __name__ == '__main__':
    main()