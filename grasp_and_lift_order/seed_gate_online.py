# -*- coding: utf-8 -*-
"""Same strictly online gate applied to SEED."""
import glob, os, re, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
from sleep_gate_online import policy, THRESH, BLOCK
D = r'G:\Work_work\math\EEG\local_analysis\cache_seed'


def main():
    by = {}
    for f in sorted(glob.glob(os.path.join(D, '*.npz'))):
        m = re.match(r'(\d+)_(\d+)\.npz', os.path.basename(f))
        if not m:
            continue
        z = np.load(f, allow_pickle=True)
        by.setdefault(int(m.group(1)), []).append((int(m.group(2)), z['X'].astype(float), z['y'].astype(int)))
    deltas, fracs = [], []
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
                keep = np.arange(n) >= BLOCK
                p_none = clf.classes_[np.argmax(S, 1)]
                Sg, frac = policy(S, d_b, blocks, K)
                p_gate = clf.classes_[np.argmax(Sg, 1)]
                deltas.append(bas(yB[keep], p_gate[keep]) - bas(yB[keep], p_none[keep]))
                fracs.append(frac)
    d = np.array(deltas)
    print('SEED online gate: cells %d  mean delta %+0.4f  positive %d/%d  blocks corrected %.2f'
          % (len(d), d.mean(), int((d > 0).sum()), len(d), np.mean(fracs)))


if __name__ == '__main__':
    main()