# -*- coding: utf-8 -*-
"""Regenerate the concentration contrast: per-block records with class concentration."""
import glob, json, os, re, sys, warnings
import numpy as np
import mne
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
sys.path.insert(0, os.environ.get('BSPC_SLEEP_CODE', r'G:\Work_work\math\EEG\paper_v8'))
import sleep_edf_frozen as F
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
BLOCK = F.BLOCK
OUT = os.path.join(os.environ.get('BSPC_RESULTS', r'G:\Work_work\math\EEG\paper_v8\results'), 'd3_concentration.json')


def blocks_of(Fa, ya, Fb, yb):
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
    D = [Fm @ (W @ (Fb[a:b].mean(0) - muA)) for a, b in blocks]
    bm = np.zeros((n, K))
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            bm[a:b] = np.mean(D[:k], axis=0)
    out = []
    for k, (a, b) in enumerate(blocks):
        if k == 0:
            continue
        y_true = yb[a:b]
        if len(np.unique(y_true)) < 2:
            continue
        p0 = clf.classes_[np.argmax(S[a:b], 1)]
        p1 = clf.classes_[np.argmax(S[a:b] - bm[a:b], 1)]
        hist = yb[:a]
        _, cnt = np.unique(y_true, return_counts=True)
        conc = float(cnt.max()) / len(y_true)
        out.append({'conc': conc, 'delta': float(bas(y_true, p1)) - float(bas(y_true, p0)),
                    'k_block': len(np.unique(y_true)), 'k_hist': len(np.unique(hist)),
                    'hist_len': k, 'block': k})
    return out


def main():
    recs = []
    psg = sorted(glob.glob(os.path.join(F.ROOT, '*PSG.edf')))
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
        Fl, yl = [], []
        for (a, b) in F.contiguous_runs(y):
            for s in range((b - a) // F.SERIES_EPOCHS):
                e0 = a + s * F.SERIES_EPOCHS
                seg = raw.get_data(picks=idx, start=int(e0 * F.EPOCH * sf),
                                   stop=int((e0 + F.SERIES_EPOCHS) * F.EPOCH * sf))
                if seg.shape[1] < int(F.SERIES_EPOCHS * F.EPOCH * sf):
                    continue
                Fl.append(F.series_features(seg, sf))
                yl.append(y[e0:e0 + F.SERIES_EPOCHS])
        for i in range(len(Fl)):
            for j in range(i + 1, len(Fl)):
                if len(np.unique(yl[i])) < 2 or len(np.unique(yl[j])) < 2:
                    continue
                for r in blocks_of(Fl[i], yl[i], Fl[j], yl[j]):
                    r['subj'] = base[:5]; r['night'] = base
                    recs.append(r)
        print(base, len(recs), flush=True)
        json.dump(recs, open(OUT, 'w'))
    print('blocks', len(recs))


if __name__ == '__main__':
    main()