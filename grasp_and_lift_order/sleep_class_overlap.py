# -*- coding: utf-8 -*-
"""Stratify the sleep-EDF cells by whether the target class set is covered by the source."""
import glob, json, math, os, re, sys, warnings
import numpy as np
import mne
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
ROOT = r'E:\data\sleep-edf\sleep-cassette'
STAGE5 = {'Sleep stage W': 0, 'Sleep stage 1': 1, 'Sleep stage 2': 2,
          'Sleep stage 3': 3, 'Sleep stage 4': 3, 'Sleep stage R': 4}
EPOCH, SERIES = 30.0, 60


def labels(night):
    base = night
    hypo = os.path.join(ROOT, re.sub(r'E\d-PSG\.edf$', 'EC-Hypnogram.edf', base))
    raw = mne.io.read_raw_edf(os.path.join(ROOT, base), preload=True, verbose='ERROR')
    ann = mne.read_annotations(hypo)
    n_ep = int(raw.n_times // int(EPOCH * raw.info['sfreq']))
    y = np.full(n_ep, -1, dtype=int)
    for onset, dur, desc in zip(ann.onset, ann.duration, ann.description):
        if desc not in STAGE5:
            continue
        s = int(round(onset / EPOCH)); span = max(1, int(round(dur / EPOCH)))
        for k in range(s, min(s + span, n_ep)):
            y[k] = STAGE5[desc]
    runs, start = [], None
    for i, v in enumerate(y):
        if v >= 0 and start is None:
            start = i
        elif v < 0 and start is not None:
            runs.append((start, i)); start = None
    if start is not None:
        runs.append((start, len(y)))
    series = []
    for (a, b) in runs:
        for s in range((b - a) // SERIES):
            e0 = a + s * SERIES
            series.append(y[e0:e0 + SERIES])
    return series


d = json.load(open('G:/Work_work/math/EEG/paper_v8/results/sleep_edf_frozen_cells.json'))
rows = d['cells']
by_night = {}
for r in rows:
    by_night.setdefault(r['night'], []).append(r)
cats = {'identical': [], 'subset': [], 'new class': []}
per_subj_cat = {}
for night, rs in by_night.items():
    sl = labels(night)
    for r in rs:
        cs = set(np.unique(sl[r['src']]))
        ct = set(np.unique(sl[r['tgt']]))
        if ct == cs:
            cat = 'identical'
        elif ct <= cs:
            cat = 'subset'
        else:
            cat = 'new class'
        cats[cat].append(r['delta'])
        per_subj_cat.setdefault(r['subj'], {}).setdefault(cat, []).append(r['delta'])
def binom2(k, n):
    m = min(k, n - k)
    tot = sum(math.factorial(n) // (math.factorial(i) * math.factorial(n - i)) for i in range(m + 1))
    return min(1.0, 2.0 * tot / 2.0 ** n)
print('cells by class-set relation:')
for k, v in cats.items():
    if not v:
        continue
    m = np.array(v)
    print('  %-10s n=%4d mean %+.4f neg %d pos %d' % (k, len(m), m.mean(), int((m < 0).sum()), int((m > 0).sum())))
print('\nsubject-level, by category:')
for cat in cats:
    vals = []
    for s, dd in per_subj_cat.items():
        if cat in dd:
            vals.append(np.mean(dd[cat]))
    if len(vals) < 3:
        print('  %-10s only %d subjects' % (cat, len(vals))); continue
    v = np.array(vals)
    neg = int((v < 0).sum()); pos = int((v > 0).sum())
    print('  %-10s subjects %2d mean %+.4f neg %d pos %d p=%.3g' % (cat, len(v), v.mean(), neg, pos, binom2(neg, neg + pos)))