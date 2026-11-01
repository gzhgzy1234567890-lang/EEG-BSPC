# -*- coding: utf-8 -*-
"""Task C on the real corpus: memory sweep on sleep-EDF (last 1, 2, 3 blocks, or all)."""
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
OUT = r'G:\Work_work\math\EEG\paper_v8\results\sleep_memory_sweep.json'
MEMS = (1, 2, 3, 99)


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
                Fa, ya, Fb, yb = Fl[i], yl[i], Fl[j], yl[j]
                if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
                    continue
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
                keep = np.arange(n) >= BLOCK
                rec = {'subj': base[:5], 'night': base, 'src': i, 'tgt': j}
                rec['none'] = float(bas(yb[keep], clf.classes_[np.argmax(S, 1)][keep]))
                hist = []
                for mm in MEMS:
                    bm = np.zeros((n, K))
                    hist = []
                    for k, (a, b) in enumerate(blocks):
                        if k > 0:
                            hist.append(D[k - 1])
                            use = hist[-mm:] if mm < 99 else hist
                            bm[a:b] = np.mean(use, axis=0)
                    p = clf.classes_[np.argmax(S - bm, 1)]
                    rec['mem%d' % mm] = float(bas(yb[keep], p[keep]))
                rows.append(rec)
        print(base, len(rows), flush=True)
        json.dump(rows, open(OUT, 'w'))
    print('cells', len(rows))


if __name__ == '__main__':
    main()
