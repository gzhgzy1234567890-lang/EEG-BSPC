# -*- coding: utf-8 -*-
"""Real class-run lengths and class proportions in sleep-EDF (for the temporal-scale reading)."""
import glob, os, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
import sleep_edf_frozen as F
import mne
mne.set_log_level('ERROR')
runs_all, props = [], []
night = 0
for f in sorted(glob.glob(os.path.join(F.ROOT, '*PSG.edf'))):
    base = os.path.basename(f)
    hypo = os.path.join(F.ROOT, base.replace('E0-PSG.edf', 'EC-Hypnogram.edf').replace('E1-PSG.edf', 'EC-Hypnogram.edf').replace('E2-PSG.edf', 'EC-Hypnogram.edf'))
    if not os.path.exists(hypo):
        continue
    raw = mne.io.read_raw_edf(f, preload=False, verbose='ERROR')
    ann = mne.read_annotations(hypo)
    sf = raw.info['sfreq']
    y = F.night_labels(ann, int(raw.n_times // int(F.EPOCH * sf)))
    y = y[y >= 0]
    if len(y) < 100:
        continue
    cur, n = y[0], 1
    for v in y[1:]:
        if v == cur:
            n += 1
        else:
            runs_all.append(n); cur, n = v, 1
    runs_all.append(n)
    props.append(np.bincount(y, minlength=5) / len(y))
    night += 1
    if night >= 20:
        break
runs = np.array(runs_all) * 30.0 / 60.0
props = np.array(props)
print('nights', len(props), '| runs', len(runs))
print('stage run length (minutes): median %.1f  mean %.1f  p10 %.1f  p90 %.1f'
      % (np.median(runs), runs.mean(), np.percentile(runs, 10), np.percentile(runs, 90)))
print('class proportions: ' + ' '.join('%.3f' % v for v in props.mean(0)))
print('per-night share of the majority class: median %.2f max %.2f' % (np.median(props.max(1)), props.max(1).max()))
