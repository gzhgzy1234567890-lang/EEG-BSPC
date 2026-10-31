# -*- coding: utf-8 -*-
"""Block-wise decomposition keeping the causal time boundary: full vs mix-only vs conditional-only correction."""
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
OUT = os.path.join(os.environ.get('BSPC_RESULTS', r'G:\Work_work\math\EEG\paper_v8\results'), 'sleep_blockwise.json')


def split_terms(Fa, ya, Fb, yb, W, Fm, muA, classes):
    muB = Fb.mean(0)
    src = [c for c in classes if np.any(ya == c)]
    tgt = [c for c in classes if np.any(yb == c)]
    prior = np.zeros_like(muA); cond = np.zeros_like(muA); rest = np.zeros_like(muA)
    for c in src:
        a_c = ya == c
        b_c = yb == c
        ma = Fa[a_c].mean(0)
        if c in tgt:
            prior += (b_c.mean() - a_c.mean()) * ma
            cond += b_c.mean() * (Fb[b_c].mean(0) - ma)
        else:
            prior += (0.0 - a_c.mean()) * ma
    for c in tgt:
        if c not in src:
            b_c = yb == c
            rest += b_c.mean() * Fb[b_c].mean(0)
    return prior + rest, cond


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
    mix, cnd, full = [], [], []
    for (a, b) in blocks:
        m, c = split_terms(Fa, ya, Fb[a:b], yb[a:b], W, Fm, muA, clf.classes_)
        mix.append(Fm @ (W @ m)); cnd.append(Fm @ (W @ c))
        full.append(Fm @ (W @ (Fb[a:b].mean(0) - muA)))
    mix, cnd, full = np.array(mix), np.array(cnd), np.array(full)
    out = {}
    for name, arr in (('full', full), ('mix', mix), ('cond', cnd)):
        corr = np.zeros((n, K))
        for k, (a, b) in enumerate(blocks):
            if k > 0:
                corr[a:b] = arr[:k].mean(0)
        pred = clf.classes_[np.argmax(S - corr, 1)]
        out[name] = float(bas(yb[BLOCK:], pred[BLOCK:]))
    pred0 = clf.classes_[np.argmax(S, 1)]
    out['none'] = float(bas(yb[BLOCK:], pred0[BLOCK:]))
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