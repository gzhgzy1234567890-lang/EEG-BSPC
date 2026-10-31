# -*- coding: utf-8 -*-
"""Corrected decomposition: original classifier, original scored set, no refit, no sample filtering."""
import glob, json, os, re, sys, warnings
import numpy as np
import mne
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
import sleep_edf_frozen as F
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
OUT = r'G:\Work_work\math\EEG\paper_v8\results\sleep_decomposition_fixed3.json'
BLOCK = F.BLOCK


def cell(Fa, ya, Fb, yb):
    clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
    K = len(clf.classes_)
    W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(K) - np.ones((K, K)) / K
    muA, muB = Fa.mean(0), Fb.mean(0)
    src = [c for c in clf.classes_ if np.any(ya == c)]
    tgt = [c for c in clf.classes_ if np.any(yb == c)]
    shared = [c for c in src if c in tgt]
    only_a = [c for c in src if c not in tgt]
    only_b = [c for c in np.unique(yb) if c not in src]
    prior = np.zeros_like(muA); cond = np.zeros_like(muA); rest = np.zeros_like(muA)
    for c in shared:
        a_c = ya == c; b_c = yb == c
        ma = Fa[a_c].mean(0)
        prior += (b_c.mean() - a_c.mean()) * ma
        cond += b_c.mean() * (Fb[b_c].mean(0) - ma)
    for c in only_a:
        rest += -(ya == c).mean() * Fa[ya == c].mean(0)
    for c in only_b:
        rest += (yb == c).mean() * Fb[yb == c].mean(0)
    rec = prior + cond + rest
    err = float(np.linalg.norm(rec - (muB - muA)) / max(np.linalg.norm(muB - muA), 1e-12))
    S = clf.decision_function(Fb)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    keep = np.arange(len(yb)) >= BLOCK
    p0 = clf.classes_[np.argmax(S, 1)]
    out = {'none': float(bas(yb[keep], p0[keep])), 'recon_err': err,
           'prior_norm': float(np.linalg.norm(Fm @ (W @ prior))),
           'cond_norm': float(np.linalg.norm(Fm @ (W @ cond))),
           'rest_norm': float(np.linalg.norm(Fm @ (W @ rest))),
           'total_norm': float(np.linalg.norm(Fm @ (W @ (muB - muA)))),
           'n_only_a': len(only_a), 'n_only_b': len(only_b)}
    for name, shift in (('full', muB - muA), ('prior', prior), ('cond', cond), ('mixture', prior + rest)):
        pred = clf.classes_[np.argmax(S - (Fm @ (W @ shift)), 1)]
        out[name] = float(bas(yb[keep], pred[keep]))
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