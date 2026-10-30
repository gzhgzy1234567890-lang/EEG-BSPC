# -*- coding: utf-8 -*-
"""Independent test on sleep-EDF, as frozen in INDEPENDENT_TEST_PROTOCOL.md.

Each night is split into consecutive 30-min series; every ordered pair of series in a night is a
cell (source earlier, target later). Features, classifier and correction follow the protocol.
"""
import glob
import json
import os
import re
import sys

import numpy as np

try:
    import mne
except Exception as exc:  # pragma: no cover
    print("mne unavailable:", exc)
    sys.exit(2)

ROOT = r"E:\data\sleep-edf\sleep-cassette"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "sleep_edf_cells.json")
BANDS = ((0.5, 4), (4, 8), (8, 12), (12, 30))
SERIES_EPOCHS = 60      # 30 min of 30-s epochs
BLOCK = 15              # 7.5 min
LAMS = (0.0, 1.0)
STAGES = ("Sleep stage W", "Sleep stage 1", "Sleep stage 2", "Sleep stage 3", "Sleep stage 4", "Sleep stage R")


def feats_epochs(raw, ann):
    """Epoch features and labels for one night."""
    sf = raw.info["sfreq"]
    raw = raw.copy().pick_channels(["EEG Fpz-Cz", "EEG Pz-Oz"])
    raw.filter(0.5, 30.0, fir_design="firwin", verbose="ERROR")
    data = raw.get_data()
    n_ep = int(data.shape[1] // (30 * sf))
    # per-epoch band power
    F = np.zeros((n_ep, data.shape[0], len(BANDS)))
    from scipy.signal import butter, filtfilt
    for bi, (lo, hi) in enumerate(BANDS):
        b, a = butter(4, [lo / (sf / 2), min(hi, sf / 2 - 1) / (sf / 2)], btype="band")
        filt = filtfilt(b, a, data, axis=1)
        for e in range(n_ep):
            seg = filt[:, e * 30 * int(sf):(e + 1) * 30 * int(sf)]
            F[e, :, bi] = np.var(seg, axis=1) + 1e-30
    F = np.log(F).reshape(n_ep, -1)
    # labels from the hypnogram
    y = np.full(n_ep, -1)
    for onset, dur, desc in zip(ann.onset, ann.duration, ann.description):
        if desc not in STAGES:
            continue
        start = int(onset // 30)
        span = max(1, int(round(dur / 30.0)))
        for idx in range(start, min(start + span, n_ep)):
            y[idx] = STAGES.index(desc)
    return F, y


def analyse(F, y):
    """Return per-cell paired differences for one night."""
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    from sklearn.metrics import balanced_accuracy_score as bas
    keep = y >= 0
    F, y = F[keep], y[keep]
    n_ser = len(F) // SERIES_EPOCHS
    if n_ser < 2:
        return []
    series = [(F[i * SERIES_EPOCHS:(i + 1) * SERIES_EPOCHS], y[i * SERIES_EPOCHS:(i + 1) * SERIES_EPOCHS])
              for i in range(n_ser)]
    K = len(np.unique(y))
    rows = []
    for i in range(n_ser):
        for j in range(i + 1, n_ser):
            (Fa, ya), (Fb, yb) = series[i], series[j]
            if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
                continue
            clf = LDA(solver="lsqr", shrinkage="auto").fit(Fa, ya)
            Kc = len(clf.classes_)
            W = clf.coef_ if Kc > 2 else np.vstack([-clf.coef_, clf.coef_])
            Fm = np.eye(Kc) - np.ones((Kc, Kc)) / Kc
            muA = Fa.mean(0)
            S = clf.decision_function(Fb)
            if S.ndim == 1:
                S = np.column_stack([-S, S])
            n = len(yb)
            blocks = [(a, min(a + BLOCK, n)) for a in range(0, n, BLOCK)]
            D = [Fm @ (W @ (Fb[a:b].mean(0) - muA)) for a, b in blocks]
            bm = np.zeros((n, Kc))
            for k, (a, b) in enumerate(blocks):
                if k > 0:
                    bm[a:b] = np.mean(D[:k], axis=0)
            res = {}
            for lam in LAMS:
                pred = clf.classes_[np.argmax(S - lam * bm, 1)]
                res[lam] = bas(yb[BLOCK:], pred[BLOCK:])
            rows.append({"src": i, "tgt": j, "delta": res[1.0] - res[0.0]})
    return rows


def main():
    psg = sorted(glob.glob(os.path.join(ROOT, "*PSG.edf")))
    print("nights found:", len(psg))
    all_rows = []
    for f in psg:
        subj = os.path.basename(f)[:6]
        base = os.path.basename(f)
        hypo = os.path.join(ROOT, re.sub(r"E\d-PSG\.edf$", "EC-Hypnogram.edf", base))
        if not os.path.exists(hypo):
            continue
        try:
            raw = mne.io.read_raw_edf(f, preload=True, verbose="ERROR")
            ann = mne.read_annotations(hypo)
            F, y = feats_epochs(raw, ann)
            rows = analyse(F, y)
            for r in rows:
                r["night"] = os.path.basename(f)
                r["subj"] = subj
            all_rows += rows
            print(subj, os.path.basename(f), "cells", len(rows), flush=True)
        except Exception as exc:
            print(subj, "FAILED", repr(exc)[:120], flush=True)
        json.dump(all_rows, open(OUT, "w"), indent=1)
    print("total cells", len(all_rows))


if __name__ == "__main__":
    main()
