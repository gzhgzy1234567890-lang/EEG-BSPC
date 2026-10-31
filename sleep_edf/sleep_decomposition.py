# -*- coding: utf-8 -*-
"""Sleep-EDF diagnostic decomposition: class-prior vs class-conditional displacement."""
import glob, json, os, re, sys, warnings
import numpy as np
from scipy.signal import butter, filtfilt
import mne
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
from sleep_edf_frozen import ROOT, night_labels, contiguous_runs, series_features, EPOCH, SERIES_EPOCHS
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
OUT = r'G:\Work_work\math\EEG\paper_v8\results\sleep_edf_decomposition3.json'


def cell(Fa, ya, Fb, yb):
    clf0 = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
    common = [c for c in clf0.classes_ if np.any(yb == c)]
    if len(common) < 2:
        return None
    ma_ = np.isin(ya, common); mb_ = np.isin(yb, common)
    Fa, ya = Fa[ma_], ya[ma_]
    Fb, yb = Fb[mb_], yb[mb_]
    if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
        return None
    if len(ya) <= len(np.unique(ya)) or len(yb) <= len(np.unique(yb)):
        return None
    if min(np.bincount(np.unique(ya, return_inverse=True)[1])) < 2:
        return None
    clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
    K = len(clf.classes_)
    W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(K) - np.ones((K, K)) / K
    muA, muB = Fa.mean(0), Fb.mean(0)
    prior = np.zeros_like(muA); cond = np.zeros_like(muA)
    for c in clf.classes_:
        a_c = ya == c; b_c = yb == c
        ma_v = Fa[a_c].mean(0); mb_v = Fb[b_c].mean(0)
        prior += (b_c.mean() - a_c.mean()) * ma_v
        cond += b_c.mean() * (mb_v - ma_v)
    rec = prior + cond
    err = np.linalg.norm(rec - (muB - muA)) / max(np.linalg.norm(muB - muA), 1e-12)
    S = clf.decision_function(Fb)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    out = {'recon_err': float(err),
           'prior_norm': float(np.linalg.norm(Fm @ (W @ prior))),
           'cond_norm': float(np.linalg.norm(Fm @ (W @ cond))),
           'total_norm': float(np.linalg.norm(Fm @ (W @ (muB - muA))))}
    base = bas(yb, clf.classes_[np.argmax(S, 1)])
    for name, shift in (('full', muB - muA), ('prior', prior), ('cond', cond)):
        pred = clf.classes_[np.argmax(S - Fm @ (W @ shift), 1)]
        out[name] = float(bas(yb, pred))
    out['none'] = float(base)
    return out


def main():
    psg = sorted(glob.glob(os.path.join(ROOT, '*PSG.edf')))
    rows = []
    for f in psg:
        base = os.path.basename(f)
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
        idx = [raw.ch_names.index(c) for c in ('EEG Fpz-Cz', 'EEG Pz-Oz')]
        for (a, b) in contiguous_runs(y):
            for s in range((b - a) // SERIES_EPOCHS):
                e0 = a + s * SERIES_EPOCHS
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
                if r is None:
                    continue
                r['night'] = base; r['subj'] = base[:5]
                rows.append(r)
        print(base, len(rows), flush=True)
        json.dump(rows, open(OUT, 'w'))
    print('cells', len(rows))


if __name__ == '__main__':
    main()