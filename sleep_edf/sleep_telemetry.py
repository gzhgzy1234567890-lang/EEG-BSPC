# -*- coding: utf-8 -*-
"""Sleep telemetry validation, frozen protocol (PROTOCOL_SLEEP_TELEMETRY.md)."""
import glob, json, os, re, sys, warnings
import numpy as np
import mne
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
import sleep_edf_frozen as F
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
ROOT = r'E:\data\sleep-edf\sleep-telemetry'
OUT = r'G:\Work_work\math\EEG\paper_v8\results\sleep_telemetry_cells.json'


def main():
    psg = sorted(glob.glob(os.path.join(ROOT, '*PSG.edf')))
    HYPO = {}
    for h in glob.glob(os.path.join(ROOT, '*Hypnogram.edf')):
        HYPO[os.path.basename(h)[:5]] = h
    print('recordings', len(psg), 'hypnograms', len(HYPO), flush=True)
    rows = []
    for f in psg:
        base = os.path.basename(f)
        hypo = HYPO.get(base[:5])
        if hypo is None:
            print('no hypnogram', base); continue
        raw = mne.io.read_raw_edf(f, preload=True, verbose='ERROR')
        ann = mne.read_annotations(hypo)
        sf = raw.info['sfreq']
        y = F.night_labels(ann, int(raw.n_times // int(F.EPOCH * sf)))
        if len(np.unique(y[y >= 0])) < 2:
            continue
        names = [c for c in ('EEG Fpz-Cz', 'EEG Pz-Oz') if c in raw.ch_names]
        if len(names) < 2:
            print('channels missing', base, raw.ch_names[:6]); continue
        idx = [raw.ch_names.index(c) for c in names]
        F_list, y_list = [], []
        for (a, b) in F.contiguous_runs(y):
            for s in range((b - a) // F.SERIES_EPOCHS):
                e0 = a + s * F.SERIES_EPOCHS
                seg = raw.get_data(picks=idx, start=int(e0 * F.EPOCH * sf),
                                   stop=int((e0 + F.SERIES_EPOCHS) * F.EPOCH * sf))
                if seg.shape[1] < int(F.SERIES_EPOCHS * F.EPOCH * sf):
                    continue
                F_list.append(F.series_features(seg, sf))
                y_list.append(y[e0:e0 + F.SERIES_EPOCHS])
        night_rows = 0
        for i in range(len(F_list)):
            for j in range(i + 1, len(F_list)):
                Fa, ya = F_list[i], y_list[i]
                Fb, yb = F_list[j], y_list[j]
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
                blocks = [(x, min(x + F.BLOCK, n)) for x in range(0, n, F.BLOCK)]
                D = [Fm @ (W @ (Fb[x:y].mean(0) - muA)) for x, y in blocks]
                bm = np.zeros((n, K))
                for k, (x, y2) in enumerate(blocks):
                    if k > 0:
                        bm[x:y2] = np.mean(D[:k], axis=0)
                p0 = clf.classes_[np.argmax(S, 1)]
                p1 = clf.classes_[np.argmax(S - bm, 1)]
                d = bas(yb[F.BLOCK:], p1[F.BLOCK:]) - bas(yb[F.BLOCK:], p0[F.BLOCK:])
                rows.append({'night': base, 'subj': base[:5], 'delta': float(d)})
                night_rows += 1
        print(base, 'series', len(F_list), 'cells', night_rows, flush=True)
        json.dump(rows, open(OUT, 'w'))
    print('cells', len(rows))


if __name__ == '__main__':
    main()