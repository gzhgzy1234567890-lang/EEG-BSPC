# -*- coding: utf-8 -*-
"""Sleep-EDF: estimator x strength matrix (P0 experiment requested by the referee)."""
import glob, json, os, sys, time, warnings
import numpy as np
from scipy.signal import butter, filtfilt
import mne
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
from sleep_edf_frozen import (ROOT, night_labels, contiguous_runs, series_features,
                              EPOCH, SERIES_EPOCHS, BLOCK)
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas

LAMS = (0.0, 0.25, 0.5, 0.75, 1.0)
OUT = r'G:\Work_work\math\EEG\paper_v8\results\sleep_edf_estimator_matrix.json'


def cell(Fa, ya, Fb, yb):
    clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
    Kc = len(clf.classes_)
    W = clf.coef_ if Kc > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(Kc) - np.ones((Kc, Kc)) / Kc
    muA = Fa.mean(0)
    S = clf.decision_function(Fb)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    n = len(yb)
    d_t = (Fb - muA) @ W.T @ Fm.T          # (n, Kc) trial-level displacement
    blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
    d_b = np.array([d_t[a:b].mean(0) for a, b in blocks])
    est = {}
    # block mean: mean of completed blocks (same contract as the main analysis)
    m = np.zeros((n, Kc))
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            m[a:b] = d_b[:k].mean(0)
    est['block'] = m
    # cumulative trial mean of all trials before t
    c = np.cumsum(d_t, axis=0)
    idx = np.arange(1, n + 1)[:, None]
    m = np.zeros((n, Kc))
    m[1:] = c[:-1] / idx[:-1]
    m[:BLOCK] = 0.0
    est['cumulative'] = m
    # sliding window 50
    m = np.zeros((n, Kc))
    for t in range(n):
        if t >= BLOCK:
            m[t] = d_t[max(0, t - 50):t].mean(0)
    est['window50'] = m
    # exponential alpha = 0.05
    m = np.zeros((n, Kc)); run = np.zeros(Kc)
    for t in range(n):
        if t >= BLOCK:
            m[t] = run.copy() if t > BLOCK else 0.0
        run = 0.95 * run + 0.05 * d_t[t] if t >= BLOCK else run
    est['exponential'] = m
    # variance-ratio weight on the block mean
    V = d_b.var(axis=0, ddof=1).sum() if len(d_b) > 2 else 1e-12
    m = np.zeros((n, Kc))
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            dbar = d_b[:k].mean(0)
            lam = float(np.dot(dbar, dbar) / (np.dot(dbar, dbar) + max(V, 1e-12) / max(k, 1)))
            m[a:b] = lam * dbar
    est['varratio'] = m
    out = {}
    for name, mm in est.items():
        for lam in LAMS:
            pred = clf.classes_[np.argmax(S - lam * mm, 1)]
            out['%s|%.2f' % (name, lam)] = float(bas(yb[BLOCK:], pred[BLOCK:]))
    return out


def main():
    psg = sorted(glob.glob(os.path.join(ROOT, '*PSG.edf')))
    rows, nights = [], []
    for k, f in enumerate(psg):
        base = os.path.basename(f)
        import re
        hypo = os.path.join(ROOT, re.sub(r'E\d-PSG\.edf$', 'EC-Hypnogram.edf', base))
        if not os.path.exists(hypo):
            continue
        raw = mne.io.read_raw_edf(f, preload=True, verbose='ERROR')
        ann = mne.read_annotations(hypo)
        sf = raw.info['sfreq']
        y = night_labels(ann, int(raw.n_times // int(EPOCH * sf)))
        if len(np.unique(y[y >= 0])) < 2:
            continue
        F_list, y_list = [], []
        for (a, b) in contiguous_runs(y):
            for s in range((b - a) // SERIES_EPOCHS):
                e0 = a + s * SERIES_EPOCHS
                idx = [raw.ch_names.index(c) for c in ('EEG Fpz-Cz', 'EEG Pz-Oz')]
                seg = raw.get_data(picks=idx, start=int(e0 * EPOCH * sf),
                                   stop=int((e0 + SERIES_EPOCHS) * EPOCH * sf))
                if seg.shape[1] < int(SERIES_EPOCHS * EPOCH * sf):
                    continue
                F_list.append(series_features(seg, sf))
                y_list.append(y[e0:e0 + SERIES_EPOCHS])
        for i in range(len(F_list)):
            for j in range(i + 1, len(F_list)):
                if len(np.unique(y_list[i])) < 2 or len(np.unique(y_list[j])) < 2:
                    continue
                r = cell(F_list[i], y_list[i], F_list[j], y_list[j])
                r['night'] = base
                r['subj'] = base[:5]
                rows.append(r)
        nights.append(base)
        print(base, len(rows), flush=True)
        json.dump(rows, open(OUT, 'w'))
    print('cells', len(rows), 'nights', len(nights))


if __name__ == '__main__':
    main()