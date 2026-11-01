# -*- coding: utf-8 -*-
"""Task A, pass 2: per-block records so the shared-class subset can be analysed."""
import glob, json, os, sys, warnings
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
warnings.filterwarnings('ignore')
sys.path.insert(0, os.environ.get('BSPC_SLEEP_CODE', r'G:\Work_work\math\EEG\paper_v8'))
import sleep_edf_frozen as F
import mne
mne.set_log_level('ERROR')
BLOCK = F.BLOCK
OUT = os.path.join(os.environ.get('BSPC_RESULTS', r'G:\Work_work\math\EEG\paper_v8\results'), 'online_decomposition_blocks.json')


def components(Fb, yb, hist, classes):
    Bn = len(hist)
    allc = sorted(set(classes.tolist()) | set(np.unique(yb).tolist()))
    num = {c: np.zeros(Fb.shape[1]) for c in allc}
    mass = {c: 0.0 for c in allc}
    for (x, y) in hist:
        lab = yb[x:y]
        nb = y - x
        for c in allc:
            m = lab == c
            w = m.sum() / nb
            mass[c] += w / Bn
            if m.sum():
                num[c] += w * Fb[x:y][m].mean(0)
    m_hat = {c: (num[c] / (mass[c] * Bn) if mass[c] > 0 else np.zeros(Fb.shape[1])) for c in allc}
    mu = sum(mass[c] * m_hat[c] for c in allc)
    return mu, mass, m_hat, allc


def run_cell(Fa, ya, Fb, yb, clf, meta):
    classes = clf.classes_
    Kc = len(classes)
    W = clf.coef_ if Kc > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(Kc) - np.ones((Kc, Kc)) / Kc
    muA = Fa.mean(0)
    piA = {c: float(np.mean(ya == c)) for c in classes}
    mA = {c: (Fa[ya == c].mean(0) if np.any(ya == c) else np.zeros(Fa.shape[1])) for c in classes}
    n = len(yb)
    blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
    S = clf.decision_function(Fb)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    corr = {k: np.zeros_like(S) for k in ('full', 'mix', 'within', 'shared', 'unmatched')}
    out = []
    for k, (a, b) in enumerate(blocks):
        if k == 0:
            continue
        hist = blocks[:k]
        mu, mass, m_hat, allc = components(Fb, yb, hist, classes)
        d = mu - muA
        d_mix = np.zeros_like(d); d_with = np.zeros_like(d); d_un = np.zeros_like(d)
        for c in allc:
            if c in piA:
                d_mix += (mass[c] - piA[c]) * mA[c]
                d_with += mass[c] * (m_hat[c] - mA[c])
            else:
                d_un += mass[c] * m_hat[c]
        err = float(np.max(np.abs(d - (d_mix + d_with + d_un))))
        for name, vec in (('full', d), ('mix', d_mix), ('within', d_with),
                          ('shared', d_mix + d_with), ('unmatched', d_un)):
            corr[name][a:b] = Fm @ (W @ vec)
        ytrue = yb[a:b]
        rec = {'k': k, 'n': int(b - a), 'unmatched_mass': float(sum(mass[c] for c in allc if c not in piA)),
               'err': err, 'classes': [int(c) for c in classes]}
        for name in ('none', 'full', 'mix', 'within', 'shared', 'unmatched'):
            cvec = np.zeros_like(S) if name == 'none' else corr[name]
            p = clf.classes_[np.argmax(S[a:b] - cvec[a:b], 1)]
            rec[name + '_tp'] = [int(np.sum((ytrue == c) & (p == c))) for c in classes]
            rec[name + '_n'] = [int(np.sum(ytrue == c)) for c in classes]
        out.append(rec)
    return out


def main():
    psg = sorted(glob.glob(os.path.join(F.ROOT, '*PSG.edf')))
    rows = []
    for f in psg:
        base = os.path.basename(f)
        hypo = os.path.join(F.ROOT, base.replace('E0-PSG.edf', 'EC-Hypnogram.edf').replace('E1-PSG.edf', 'EC-Hypnogram.edf').replace('E2-PSG.edf', 'EC-Hypnogram.edf'))
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
                Fa, ya = Fl[i], yl[i]
                Fb, yb = Fl[j], yl[j]
                if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
                    continue
                clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
                for rec in run_cell(Fa, ya, Fb, yb, clf, (base, i, j)):
                    rec.update({'subj': base[:5], 'night': base, 'src': i, 'tgt': j})
                    rows.append(rec)
        print(base, len(rows), flush=True)
        json.dump(rows, open(OUT, 'w'))
    print('blocks', len(rows))


if __name__ == '__main__':
    main()
