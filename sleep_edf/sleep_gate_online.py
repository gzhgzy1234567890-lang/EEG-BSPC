# -*- coding: utf-8 -*-
"""Strictly online (block-wise) risk gate on sleep-EDF and SEED."""
import glob, json, os, re, sys, warnings
import numpy as np
import mne
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
import sleep_edf_frozen as F
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
BLOCK = F.BLOCK
THRESH = 0.044


def policy(S, d_b, blocks, K):
    n = S.shape[0]
    out = S.copy()
    fired = []
    for k, (a, b) in enumerate(blocks):
        if k == 0:
            continue
        prev = d_b[:k].mean(0)                      # completed blocks only
        past = slice(BLOCK, a)                      # trials scored before this block
        if a <= BLOCK:
            flip = 1.0                              # no evidence yet -> no correction
        else:
            p0 = np.argmax(S[past], 1)
            p1 = np.argmax(S[past] - prev, 1)
            flip = float(np.mean(p0 != p1))
        decision = flip < THRESH
        fired.append(1.0 if decision else 0.0)
        out[a:b] = S[a:b] - prev if decision else S[a:b]
    return out, float(np.mean(fired)) if fired else 0.0


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
    keep = np.arange(n) >= BLOCK
    p_none = clf.classes_[np.argmax(S, 1)]
    p_all = clf.classes_[np.argmax(S - bm, 1)]
    Sg, frac = policy(S, d_b, blocks, K)
    p_gate = clf.classes_[np.argmax(Sg, 1)]
    return {'none': float(bas(yb[keep], p_none[keep])),
            'all': float(bas(yb[keep], p_all[keep])),
            'gate': float(bas(yb[keep], p_gate[keep])),
            'frac_corrected': frac}


def sleep():
    OUT = r'G:\Work_work\math\EEG\paper_v8\results\sleep_gate_online.json'
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
    print('sleep cells', len(rows))


if __name__ == '__main__':
    sleep()