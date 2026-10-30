# -*- coding: utf-8 -*-
"""Protocol-faithful re-run of the sleep-EDF independent test.

Implements INDEPENDENT_TEST_PROTOCOL.md literally:
  * five stages, S3 and S4 merged into N3;
  * 0.5-30 Hz fourth-order Butterworth, zero-phase, applied to each 30-min series separately;
  * series are 60 consecutive epochs on the original time axis; a series never crosses an
    unlabelled epoch, because the night is cut only inside contiguous labelled runs;
  * a night is dropped if fewer than four complete series remain or fewer than two stages occur;
  * the correction is the completed-block mean of the decision-space displacement, blocks of 15,
    first block unscored, lambda in {0, 1}.
"""
import glob, json, os, re, sys, time, warnings
import numpy as np
from scipy.signal import butter, filtfilt
import mne

warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
ROOT = r'E:\data\sleep-edf\sleep-cassette'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', 'sleep_edf_frozen_cells.json')
OUT_INCL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', 'sleep_edf_frozen_incl.json')
INCL = False
BANDS = ((0.5, 4.0), (4.0, 8.0), (8.0, 12.0), (12.0, 30.0))
EPOCH = 30.0
SERIES_EPOCHS = 60
BLOCK = 15
LAMS = (0.0, 1.0)
STAGE5 = {'Sleep stage W': 0, 'Sleep stage 1': 1, 'Sleep stage 2': 2,
          'Sleep stage 3': 3, 'Sleep stage 4': 3, 'Sleep stage R': 4}


def night_labels(ann, n_ep):
    y = np.full(n_ep, -1, dtype=int)
    for onset, dur, desc in zip(ann.onset, ann.duration, ann.description):
        if desc not in STAGE5:
            continue
        s = int(round(onset / EPOCH))
        span = max(1, int(round(dur / EPOCH)))
        for k in range(s, min(s + span, n_ep)):
            y[k] = STAGE5[desc]
    return y


def contiguous_runs(y):
    runs, start = [], None
    for i, v in enumerate(y):
        if v >= 0 and start is None:
            start = i
        elif v < 0 and start is not None:
            runs.append((start, i))
            start = None
    if start is not None:
        runs.append((start, len(y)))
    return runs


def series_features(seg, sf):
    """seg: (2, n) raw series; returns (n_epoch, 8) log band variances."""
    b, a = butter(4, [0.5 / (sf / 2), 30.0 / (sf / 2)], btype='band')
    base = filtfilt(b, a, seg, axis=1)
    n_ep = base.shape[1] // int(EPOCH * sf)
    out = np.zeros((n_ep, base.shape[0] * len(BANDS)))
    for bi, (lo, hi) in enumerate(BANDS):
        bb, aa = butter(4, [lo / (sf / 2), min(hi, sf / 2 - 1) / (sf / 2)], btype='band')
        band = filtfilt(bb, aa, base, axis=1)
        for e in range(n_ep):
            seg_e = band[:, e * int(EPOCH * sf):(e + 1) * int(EPOCH * sf)]
            var = np.var(seg_e, axis=1) + 1e-30
            out[e, bi * base.shape[0]:(bi + 1) * base.shape[0]] = np.log(var)
    return out


def analyse_night(F_list, y_list, night, subj, include_tgt_single=False):
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    from sklearn.metrics import balanced_accuracy_score as bas
    rows = []
    stat = {'pairs': 0, 'drop_src': 0, 'drop_tgt': 0}
    for i in range(len(F_list)):
        for j in range(i + 1, len(F_list)):
            Fa, ya = F_list[i], y_list[i]
            Fb, yb = F_list[j], y_list[j]
            stat['pairs'] += 1
            if len(np.unique(ya)) < 2:
                stat['drop_src'] += 1
                continue
            if len(np.unique(yb)) < 2 and not include_tgt_single:
                stat['drop_tgt'] += 1
                continue
            clf = LDA(solver='lsqr', shrinkage='auto').fit(Fa, ya)
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
            rows.append({'src': i, 'tgt': j, 'night': night, 'subj': subj,
                         'k_src': int(Kc), 'delta': float(res[1.0] - res[0.0])})
    return rows, stat


def main(limit=None, incl=False):
    t0 = time.time()
    psg = sorted(glob.glob(os.path.join(ROOT, '*PSG.edf')))
    global INCL
    INCL = incl
    all_rows, nights, skipped = [], [], {}
    for k, f in enumerate(psg):
        if limit and k >= limit:
            break
        base = os.path.basename(f)
        hypo = os.path.join(ROOT, re.sub(r'E\d-PSG\.edf$', 'EC-Hypnogram.edf', base))
        if not os.path.exists(hypo):
            skipped[base] = 'no hypnogram'
            continue
        raw = mne.io.read_raw_edf(f, preload=True, verbose='ERROR')
        ann = mne.read_annotations(hypo)
        sf = raw.info['sfreq']
        y = night_labels(ann, int(raw.n_times // int(EPOCH * sf)))
        if len(np.unique(y[y >= 0])) < 2:
            skipped[base] = 'fewer than two stages'
            continue
        idx = [raw.ch_names.index(c) for c in ('EEG Fpz-Cz', 'EEG Pz-Oz')]
        F_list, y_list = [], []
        for (a, b) in contiguous_runs(y):
            n_ser = (b - a) // SERIES_EPOCHS
            for s in range(n_ser):
                e0 = a + s * SERIES_EPOCHS
                lo = int(round(e0 * EPOCH * sf))
                hi = int(round((e0 + SERIES_EPOCHS) * EPOCH * sf))
                seg = raw.get_data(picks=idx, start=lo, stop=hi)
                if seg.shape[1] < SERIES_EPOCHS * int(EPOCH * sf):
                    continue
                F_list.append(series_features(seg, sf))
                y_list.append(y[e0:e0 + SERIES_EPOCHS])
        if len(F_list) < 4:
            skipped[base] = 'fewer than four complete series'
            continue
        rows, stat = analyse_night(F_list, y_list, base, base[:5], INCL)
        all_rows += rows
        nights.append({'night': base, 'subj': base[:5], 'series': len(F_list),
                       'cells': len(rows), 'pairs': stat['pairs'],
                       'drop_src': stat['drop_src'], 'drop_tgt': stat['drop_tgt']})
        print('%-22s series %2d cells %3d pairs %3d drop_src %3d drop_tgt %3d %5.0fs'
              % (base, len(F_list), len(rows), stat['pairs'], stat['drop_src'],
                 stat['drop_tgt'], time.time() - t0), flush=True)
        json.dump({'cells': all_rows, 'nights': nights, 'skipped': skipped,
                   'include_single_class_target': incl},
                  open(OUT_INCL if incl else OUT, 'w'), indent=1)
    print('nights kept', len(nights), 'cells', len(all_rows), 'skipped', len(skipped))
    print('elapsed %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    lim = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    main(lim, incl=('incl' in sys.argv))