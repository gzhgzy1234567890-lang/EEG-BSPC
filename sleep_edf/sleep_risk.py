# -*- coding: utf-8 -*-
"""Label-free risk statistics per sleep-EDF cell, for a held-out gate test."""
import glob, json, os, re, sys, warnings
import numpy as np
import mne
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
import sleep_edf_frozen as F
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
OUT = r'G:\Work_work\math\EEG\paper_v8\results\sleep_risk.json'
BLOCK = F.BLOCK


def cell(Fa, ya, Fb, yb):
    clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
    K = len(clf.classes_)
    W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(K) - np.ones((K, K)) / K
    muA = Fa.mean(0)
    S = clf.decision_function(Fb)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    n = len(yb)
    blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
    d_b = np.array([Fm @ (W @ (Fb[a:b].mean(0) - muA)) for a, b in blocks])
    bm = np.zeros((n, K))
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            bm[a:b] = d_b[:k].mean(0)
    p0 = clf.classes_[np.argmax(S, 1)]
    p1 = clf.classes_[np.argmax(S - bm, 1)]
    keep = np.arange(n) >= BLOCK
    if keep.sum() < 15:
        return None
    delta = bas(yb[keep], p1[keep]) - bas(yb[keep], p0[keep])
    Ss = np.sort(S, axis=1)
    margin = Ss[:, -1] - Ss[:, -2]
    flip = float(np.mean(p0[keep] != p1[keep]))
    dmargin = float(np.mean(np.abs((S - bm)[keep] - S[keep]).max(1)))
    dnorm = float(np.mean(np.linalg.norm(bm[keep], axis=1)))
    # disagreement between block-mean and exponential mean in decision space
    run = np.zeros(K); expo = np.zeros((n, K))
    for t in range(n):
        expo[t] = run
        if t >= BLOCK:
            run = 0.95 * run + 0.05 * (Fm @ (W @ (Fb[t] - muA)))
    disagree = float(np.linalg.norm((bm - expo)[keep].mean(0)) / max(np.linalg.norm(bm[keep].mean(0)), 1e-9))
    return {'delta': float(delta), 'flip': flip, 'dmargin': dmargin,
            'margin': float(np.mean(margin[keep])), 'dnorm': dnorm, 'disagree': disagree}


def main():
    psg = sorted(glob.glob(os.path.join(F.ROOT, '*PSG.edf')))
    rows = []
    for f in psg:
        base = os.path.basename(f)
        hypo = os.path.join(F.ROOT, re.sub(r'E\d-PSG\.edf$', 'EC-Hypnogram.edf', base))
        if not os.path.exists(hypo):
            continue
        raw = mne.io.read_raw_edf(f, preload=True, verbose='ERROR')
        ann = mne.read_annotations(hypo)
        sf = raw.info['sfreq']
        y = F.night_labels(ann, int(raw.n_times // int(F.EPOCH * sf)))
        if len(np.unique(y[y >= 0])) < 2:
            continue
        idx = [raw.ch_names.index(c) for c in ('EEG Fpz-Cz', 'EEG Pz-Oz')]
        F_list, y_list = [], []
        for (a, b) in F.contiguous_runs(y):
            for s in range((b - a) // F.SERIES_EPOCHS):
                e0 = a + s * F.SERIES_EPOCHS
                seg = raw.get_data(picks=idx, start=int(e0 * F.EPOCH * sf),
                                   stop=int((e0 + F.SERIES_EPOCHS) * F.EPOCH * sf))
                if seg.shape[1] < int(F.SERIES_EPOCHS * F.EPOCH * sf):
                    continue
                F_list.append(F.series_features(seg, sf))
                y_list.append(y[e0:e0 + F.SERIES_EPOCHS])
        for i in range(len(F_list)):
            for j in range(i + 1, len(F_list)):
                if len(np.unique(y_list[i])) < 2 or len(np.unique(y_list[j])) < 2:
                    continue
                r = cell(F_list[i], y_list[i], F_list[j], y_list[j])
                if r is None:
                    continue
                r['night'] = base; r['subj'] = base[:5]
                rows.append(r)
        print(base, len(rows), flush=True)
        json.dump(rows, open(OUT, 'w'))
    print('cells', len(rows))


if __name__ == '__main__':
    main()