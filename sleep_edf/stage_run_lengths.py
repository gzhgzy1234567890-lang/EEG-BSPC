# -*- coding: utf-8 -*-
import glob, os, re, sys
import numpy as np
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
import sleep_edf_frozen as F
import mne, warnings
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
runs = []
for h in sorted(glob.glob(os.path.join(F.ROOT, '*Hypnogram.edf'))):
    ann = mne.read_annotations(h)
    y = F.night_labels(ann, 4000)
    y = y[y >= 0]
    if len(y) < 100:
        continue
    cur = 1
    for t in range(1, len(y)):
        if y[t] == y[t-1]:
            cur += 1
        else:
            runs.append(cur); cur = 1
    runs.append(cur)
runs = np.array(runs)
print('hypnograms %d  runs %d' % (len(glob.glob(os.path.join(F.ROOT, '*Hypnogram.edf'))), len(runs)))
print('stage run length in epochs: median %.0f  mean %.0f  (30 s epochs -> %.1f / %.1f min)' % (np.median(runs), runs.mean(), np.median(runs)*0.5, runs.mean()*0.5))
print('75th percentile %.0f epochs (%.0f min)' % (np.percentile(runs, 75), np.percentile(runs, 75)*0.5))