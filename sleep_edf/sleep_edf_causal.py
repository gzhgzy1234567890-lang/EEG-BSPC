# -*- coding: utf-8 -*-
"""Strictly causal version of the sleep-EDF replication: forward-only filters with carried state."""
import glob, json, math, os, re, sys, warnings
import numpy as np
from scipy.signal import butter, lfilter
import mne
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
import sklearn
sys.path.insert(0, 'G:/Work_work/math/EEG/paper_v8')
from sleep_edf_frozen import night_labels, contiguous_runs, analyse_night, OUT

ROOT = r'E:\data\sleep-edf\sleep-cassette'
OUT2 = os.path.join(os.path.dirname(os.path.abspath('G:/Work_work/math/EEG/paper_v8/x')), 'results', 'sleep_edf_causal_cells.json')
BANDS = ((0.5, 4.0), (4.0, 8.0), (8.0, 12.0), (12.0, 30.0))
EPOCH, SERIES = 30.0, 60


def causal_features(night, series_index):
    raw = mne.io.read_raw_edf(os.path.join(ROOT, night), preload=True, verbose='ERROR')
    sf = raw.info['sfreq']
    idx = [raw.ch_names.index(c) for c in ('EEG Fpz-Cz', 'EEG Pz-Oz')]
    X = raw.get_data(picks=idx).astype(np.float64)
    b, a = butter(4, [0.5 / (sf / 2), 30.0 / (sf / 2)], btype='band')
    X = lfilter(b, a, X, axis=1)
    bands = []
    for lo, hi in BANDS:
        bb, aa = butter(4, [lo / (sf / 2), min(hi, sf / 2 - 1) / (sf / 2)], btype='band')
        bands.append(lfilter(bb, aa, X, axis=1))
    n_ep = X.shape[1] // int(EPOCH * sf)
    var = np.zeros((n_ep, len(idx) * len(BANDS)))
    for e in range(n_ep):
        s0, s1 = e * int(EPOCH * sf), (e + 1) * int(EPOCH * sf)
        for bi, sig in enumerate(bands):
            v = np.var(sig[:, s0:s1], axis=1) + 1e-30
            var[e, bi * len(idx):(bi + 1) * len(idx)] = v
    return np.log(var)


def main(limit=None):
    psg = sorted(glob.glob(os.path.join(ROOT, '*PSG.edf')))
    cells, nights = [], []
    for k, f in enumerate(psg):
        if limit and k >= limit:
            break
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
        F_all = causal_features(base, None)
        seriesF, seriesY = [], []
        for (a, b) in contiguous_runs(y):
            for s in range((b - a) // SERIES):
                e0 = a + s * SERIES
                seriesF.append(F_all[e0:e0 + SERIES])
                seriesY.append(y[e0:e0 + SERIES])
        if len(seriesF) < 4:
            continue
        rows, stat = analyse_night(seriesF, seriesY, base, base[:5])
        cells += rows
        nights.append({'night': base, 'subj': base[:5], 'series': len(seriesF), 'cells': len(rows)})
        print('%-22s series %2d cells %3d' % (base, len(seriesF), len(rows)), flush=True)
        json.dump({'cells': cells, 'nights': nights}, open(OUT2, 'w'), indent=1)
    print('nights', len(nights), 'cells', len(cells))


if __name__ == '__main__':
    main()