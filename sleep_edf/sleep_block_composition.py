# -*- coding: utf-8 -*-
"""Per-block composition and per-block loss: each scored block uses exactly the blocks that precede it."""
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
OUT = os.path.join(os.environ.get('BSPC_RESULTS', r'G:\Work_work\math\EEG\paper_v8\results'), 'sleep_block_composition.json')


def entropy(counts):
    p = counts / counts.sum()
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


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
    rows = []
    for k, (a, b) in enumerate(blocks):
        if k == 0 or (b - a) < 2:
            continue
        hist = yb[:a]
        if len(np.unique(hist)) < 2 or len(np.unique(yb[a:b])) < 2:
            continue
        counts = np.array([np.sum(hist == c) for c in np.unique(hist)], dtype=float)
        corr = d_b[:k].mean(0)
        p0 = clf.classes_[np.argmax(S[a:b], 1)]
        p1 = clf.classes_[np.argmax(S[a:b] - corr, 1)]
        rows.append({'subj': None, 'k': k, 'entropy': entropy(counts),
                     'maxfrac': float(counts.max() / counts.sum()), 'kcls': int(len(counts)),
                     'dba': float(bas(yb[a:b], p1) - bas(yb[a:b], p0)),
                     'hist_len': int(a)})
    return rows


def main():
    psg = sorted(glob.glob(os.path.join(F.ROOT, '*PSG.edf')))
    out = []
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
                for r in cell(Fl[i], yl[i], Fl[j], yl[j]):
                    r['subj'] = base[:5]
                    r['night'] = base
                    out.append(r)
        print(base, len(out), flush=True)
        json.dump(out, open(OUT, 'w'))
    print('block rows', len(out))


if __name__ == '__main__':
    main()