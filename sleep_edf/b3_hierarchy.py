# -*- coding: utf-8 -*-
"""B3: hierarchical recomputation of the sleep-EDF result from the archived cells."""
import json, os, sys
import numpy as np
from scipy.stats import wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, 'results', 'sleep_edf_frozen_cells.json')))
cells = d['cells']
print('cells', len(cells), '| nights', len(d['nights']), '| subjects', len({c['subj'] for c in cells}))
delta = np.array([c['delta'] for c in cells])
print('cell-level mean delta %+0.4f  (this is NOT the inferential statistic)' % delta.mean())
by_subj = {}
for c in cells:
    by_subj.setdefault(c['subj'], {}).setdefault(c['night'], []).append(c['delta'])
subj_vals = np.array([np.mean([np.mean(v) for v in nights.values()]) for nights in by_subj.values()])
print('subject-level mean %+0.4f  sd %.4f  negative %d/%d  wilcoxon p=%.3g'
      % (subj_vals.mean(), subj_vals.std(ddof=1), int((subj_vals < 0).sum()), len(subj_vals), wilcoxon(subj_vals).pvalue))
rng = np.random.default_rng(20261101)
b = [rng.choice(subj_vals, len(subj_vals), replace=True).mean() for _ in range(10000)]
print('bootstrap 95%% interval [%+0.4f, %+0.4f]' % tuple(np.percentile(b, [2.5, 97.5])))
night_vals = []
for subj, nights in by_subj.items():
    for night, vals in nights.items():
        night_vals.append(np.mean(vals))
night_vals = np.array(night_vals)
print('recording-level mean %+0.4f  negative %d/%d  (descriptive)' % (night_vals.mean(), int((night_vals < 0).sum()), len(night_vals)))
within_subj_sd = np.mean([np.std([np.mean(v) for v in nights.values()]) for nights in by_subj.values() if len(nights) > 1])
print('between-subject sd %.4f | mean within-subject (between-night) sd %.4f' % (subj_vals.std(ddof=1), within_subj_sd))
out = {'n_cells': len(cells), 'n_subjects': int(len(subj_vals)), 'n_recordings': int(len(night_vals)),
       'subject_mean': float(subj_vals.mean()), 'subject_sd': float(subj_vals.std(ddof=1)),
       'negative_subjects': int((subj_vals < 0).sum()), 'wilcoxon_p': float(wilcoxon(subj_vals).pvalue),
       'ci_low': float(np.percentile(b, 2.5)), 'ci_high': float(np.percentile(b, 97.5)),
       'recording_mean': float(night_vals.mean()), 'negative_recordings': int((night_vals < 0).sum())}
json.dump(out, open(os.path.join(HERE, 'results', 'b3_hierarchy.json'), 'w'), indent=1)
print('B3 done')