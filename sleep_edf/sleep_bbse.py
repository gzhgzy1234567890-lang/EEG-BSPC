# -*- coding: utf-8 -*-
"""Label-free prior-shift (BBSE) correction on sleep-EDF: can the prior term be removed without labels?"""
import glob, json, os, re, sys, warnings
import numpy as np
import mne
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
sys.path.insert(0, os.environ.get('BSPC_SLEEP_CODE', r'G:\Work_work\math\EEG\paper_v8'))
import sleep_edf_frozen as F
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
from sklearn.model_selection import StratifiedKFold
BLOCK = F.BLOCK
OUT = os.path.join(os.environ.get('BSPC_RESULTS', r'G:\Work_work\math\EEG\paper_v8\results'), 'sleep_bbse.json')


def confusion(Fa, ya, classes):
    K = len(classes)
    C = np.zeros((K, K))
    counts = np.array([np.sum(ya == c) for c in classes])
    if counts.min() >= 5:
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
        for tr, te in skf.split(Fa, ya):
            if len(np.unique(ya[tr])) < 2:
                continue
            clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa[tr], ya[tr])
            pred = clf.predict(Fa[te])
            for t, p in zip(ya[te], pred):
                C[classes.index(t), classes.index(p)] += 1
    else:
        clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
        pred = clf.predict(Fa)
        for t, p in zip(ya, pred):
            C[classes.index(t), classes.index(p)] += 1
    if (C.sum(1) == 0).any():
        C = C + 0.5 * np.eye(K)
    C /= C.sum(1, keepdims=True)
    return 0.95 * C + 0.05 * np.eye(K)


def bbse(pred, C, classes):
    K = len(classes)
    phat = np.array([np.mean(pred == c) for c in classes])
    try:
        q = np.linalg.solve(C.T, phat)
    except np.linalg.LinAlgError:
        q = np.linalg.lstsq(C.T, phat, rcond=None)[0]
    q = np.clip(q, 0, None)
    s = q.sum()
    return q / s if s > 0 else phat


def cell(Fa, ya, Fb, yb):
    clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
    classes = list(clf.classes_)
    K = len(classes)
    W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(K) - np.ones((K, K)) / K
    muA = Fa.mean(0)
    S = clf.decision_function(Fb)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    pred = clf.classes_[np.argmax(S, 1)]
    keep = slice(BLOCK, len(yb))
    base = bas(yb[keep], pred[keep])
    muA_c = np.array([Fa[ya == c].mean(0) for c in classes])
    pa = np.array([np.mean(ya == c) for c in classes])
    C = confusion(Fa, ya, classes)
    q = bbse(pred, C, classes)
    out = {'none': float(base)}
    # estimate the displacement of the target mean from the source mean using estimated proportions only
    d_hat = (q - pa) @ muA_c
    corr_hat = Fm @ (W @ d_hat)
    out['bbse'] = float(bas(yb[keep], clf.classes_[np.argmax(S - corr_hat, 1)][keep]))
    # oracle version: true target proportions (uses labels; diagnostic only)
    pb = np.array([np.mean(yb == c) for c in classes])
    d_true = (pb - pa) @ muA_c
    corr_true = Fm @ (W @ d_true)
    out['oracle_prior'] = float(bas(yb[keep], clf.classes_[np.argmax(S - corr_true, 1)][keep]))
    out['q_err'] = float(np.abs(q - pb).sum() / 2)
    return out


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
                r = cell(Fl[i], yl[i], Fl[j], yl[j])
                r['night'] = base; r['subj'] = base[:5]
                rows.append(r)
        print(base, len(rows), flush=True)
        json.dump(rows, open(OUT, 'w'))
    print('cells', len(rows))


if __name__ == '__main__':
    main()