# -*- coding: utf-8 -*-
"""Rebuild the grasp-and-lift cache in true acquisition order.

For each series: HandStart onsets from the events file; two samples per trial,
  class 0 = the 2 s before the onset, class 1 = the 2 s after it;
features = log power in 8 consecutive 250-ms windows x 32 channels = 256 dims;
the sequence is stored in trial order (0,1,0,1,...), i.e. real time.
"""
import glob, io, json, os, sys
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt

ROOT = r'E:\data\grasp-and-lift-eeg-detection\train'
OUT = r'G:\Work_work\math\EEG\local_analysis\cache_gal_time'
FS = 500.0
PRE, POST = 2.0, 2.0
NWIN = 8
os.makedirs(OUT, exist_ok=True)


def onsets(ev_path):
    E = pd.read_csv(ev_path)
    v = E['HandStart'].values
    on = np.where(v > 0)[0]
    return on[np.r_[True, np.diff(on) > 1]]


def features(seg, bb, aa):
    # seg: (n_samples, n_ch) already band-passed
    n = seg.shape[0] // NWIN
    out = np.empty(seg.shape[1] * NWIN)
    for k in range(NWIN):
        part = seg[k * n:(k + 1) * n]
        pv = np.mean(part ** 2, axis=0)
        out[k * seg.shape[1]:(k + 1) * seg.shape[1]] = np.log(pv + 1e-12)
    return out


def one(series):
    da = os.path.join(ROOT, series + '_data.csv')
    ev = os.path.join(ROOT, series + '_events.csv')
    df = pd.read_csv(da)
    ch = [c for c in df.columns if c != 'id']
    X = df[ch].values.astype(np.float64)
    on = onsets(ev)
    b, a = butter(4, [0.5 / (FS / 2), 30.0 / (FS / 2)], btype='band')
    X = filtfilt(b, a, X, axis=0)
    pre, post = int(PRE * FS), int(POST * FS)
    F, y = [], []
    for t in on:
        if t - pre < 0 or t + post > X.shape[0]:
            continue
        F.append(features(X[t - pre:t], b, a)); y.append(0)
        F.append(features(X[t:t + post], b, a)); y.append(1)
    F = np.asarray(F); y = np.asarray(y, dtype=np.int8)
    np.savez(os.path.join(OUT, series + '.npz'), F=F, y=y, ch=np.array(ch))
    return F.shape, int(y.sum()), len(on)


if __name__ == '__main__':
    pat = sys.argv[1] if len(sys.argv) > 1 else '*'
    files = sorted(glob.glob(os.path.join(ROOT, pat + '_data.csv')))
    for i, f in enumerate(files):
        s = os.path.basename(f).replace('_data.csv', '')
        try:
            shp, npos, ntr = one(s)
            print('%-18s %s pos %d trials %d' % (s, shp, npos, ntr), flush=True)
        except Exception as exc:
            print(s, 'FAILED', repr(exc)[:120], flush=True)