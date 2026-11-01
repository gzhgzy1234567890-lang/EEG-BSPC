# -*- coding: utf-8 -*-
"""Anchored online decomposition (origin-invariant), with a translation check on real data."""
import glob, json, os, sys, warnings
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
warnings.filterwarnings('ignore')
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
import sleep_edf_frozen as F
import mne
mne.set_log_level('ERROR')
BLOCK = F.BLOCK
OUT = r'G:\Work_work\math\EEG\paper_v8\results\online_decomposition_anchored.json'
MAXNIGHTS = int(os.environ.get('BSPC_MAXNIGHTS', '999'))


def parts(Fb, yb, hist, classes):
    Bn = len(hist)
    allc = sorted(set(classes.tolist()) | set(np.unique(yb).tolist()))
    mass = {c: 0.0 for c in allc}
    num = {c: np.zeros(Fb.shape[1]) for c in allc}
    for (x, y) in hist:
        lab, nb = yb[x:y], y - x
        for c in allc:
            m = lab == c
            w = m.sum() / nb
            mass[c] += w / Bn
            if m.sum():
                num[c] += w * Fb[x:y][m].mean(0)
    mh = {c: (num[c] / (mass[c] * Bn) if mass[c] > 0 else np.zeros(Fb.shape[1])) for c in allc}
    mu = sum(mass[c] * mh[c] for c in allc)
    return mu, mass, mh, allc


def run_cell(Fa, ya, Fb, yb, clf, shift=0.0):
    """shift is added to every feature as a test of origin invariance."""
    a = np.full(Fa.shape[1], shift)
    Fa = Fa + a
    Fb = Fb + a
    classes = clf.classes_
    K = len(classes)
    W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(K) - np.ones((K, K)) / K
    muA = Fa.mean(0)
    piA = {c: float(np.mean(ya == c)) for c in classes}
    mA = {c: Fa[ya == c].mean(0) for c in classes}
    n = len(yb)
    blocks = [(x, min(x + BLOCK, n)) for x in range(0, n, BLOCK)]
    S = clf.decision_function(Fb)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    corr = {k: np.zeros_like(S) for k in ('full', 'mix', 'within', 'shared', 'unmatched', 'mix_unanchored')}
    err = 0.0
    for k, (x, y) in enumerate(blocks):
        if k == 0:
            continue
        mu, mass, mh, allc = parts(Fb, yb, blocks[:k], classes)
        d = mu - muA
        mix = np.zeros_like(d); wit = np.zeros_like(d); unm = np.zeros_like(d); mix_un = np.zeros_like(d)
        for c in allc:
            if c in piA:
                mix += (mass[c] - piA[c]) * (mA[c] - muA)      # anchored
                mix_un += (mass[c] - piA[c]) * mA[c]           # unanchored, for comparison
                wit += mass[c] * (mh[c] - mA[c])
            else:
                unm += mass[c] * (mh[c] - muA)                 # anchored
        err = max(err, float(np.max(np.abs(d - (mix + wit + unm)))))
        for name, vec in (('full', d), ('mix', mix), ('within', wit), ('shared', mix + wit),
                          ('unmatched', unm), ('mix_unanchored', mix_un)):
            corr[name][x:y] = Fm @ (W @ vec)
    keep = np.arange(n) >= BLOCK
    out = {'err': err}
    for name in corr:
        p = clf.classes_[np.argmax(S - corr[name], 1)]
        out[name] = float(bas(yb[keep], p[keep]))
    out['none'] = float(bas(yb[keep], clf.classes_[np.argmax(S, 1)][keep]))
    return out


def main():
    psg = sorted(glob.glob(os.path.join(F.ROOT, '*PSG.edf')))
    rows = []
    nights = 0
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
                Fa, ya, Fb, yb = Fl[i], yl[i], Fl[j], yl[j]
                if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
                    continue
                clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
                r0 = run_cell(Fa, ya, Fb, yb, clf, shift=0.0)
                if i == 0 and j == 1:
                    r1 = run_cell(Fa, ya, Fb, yb, clf, shift=2.5)
                    r0['shift_check'] = {k: float(abs(r1[k] - r0[k])) for k in ('mix', 'within', 'unmatched')}
                r0.update({'subj': base[:5], 'night': base, 'src': i, 'tgt': j})
                rows.append(r0)
        nights += 1
        print(base, len(rows), flush=True)
        json.dump(rows, open(OUT, 'w'))
        if nights >= MAXNIGHTS:
            break
    print('cells', len(rows))


if __name__ == '__main__':
    main()
