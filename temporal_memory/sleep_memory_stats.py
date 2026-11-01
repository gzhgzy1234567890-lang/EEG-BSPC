# -*- coding: utf-8 -*-
"""Sleep-EDF memory sweep: subject-level statistics."""
import json, os, sys
import numpy as np
from scipy.stats import wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'sleep_memory_sweep.json')))
print('cells', len(rows), 'subjects', len({r['subj'] for r in rows}))
rng = np.random.default_rng(20261101)


def subj(key):
    d = {}
    for r in rows:
        d.setdefault(r['subj'], {}).setdefault(r['night'], []).append(r[key])
    return np.array([np.mean([np.mean(v) for v in n.values()]) for n in d.values()])


base = subj('none')
print('none BA %.4f' % base.mean())
for mm in ('mem1', 'mem2', 'mem3', 'mem99'):
    v = subj(mm) - base
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(10000)]
    p = wilcoxon(v).pvalue if np.any(v != 0) else float('nan')
    print('%-6s delta %+0.4f [%+0.4f, %+0.4f]  negative %d/%d  p=%.3g'
          % (mm, v.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5), int((v < 0).sum()), len(v), p))
