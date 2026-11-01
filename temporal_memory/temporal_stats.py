# -*- coding: utf-8 -*-
import json, os, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'temporal_memory_v2.json')))
print('runs', len(rows), 'subjects', len({r['subj'] for r in rows}))
rng = np.random.default_rng(20261101)


def cell(prior, speed, run_len, mem):
    d = {}
    for r in rows:
        if r['prior'] == prior and abs(r['speed'] - speed) < 1e-9 and r['run_len'] == run_len and r['mem_blocks'] == mem:
            d.setdefault(r['subj'], []).append(r['delta'])
    return np.array([np.mean(v) for _, v in sorted(d.items())])


print()
print('%-34s %-9s %-24s %s' % ('condition', 'delta', '95% CI', 'negative'))
for run_len in (1, 5, 25):
    for mem in (1, 4, 16):
        v = cell(0, 0.0, run_len, mem)
        b = [rng.choice(v, len(v), replace=True).mean() for _ in range(10000)]
        print('%-34s %+0.4f    [%+0.4f, %+0.4f]    %d/%d'
              % ('no drift, run %d, mem %d' % (run_len, mem),
                 v.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5), int((v < 0).sum()), len(v)))
print()
for run_len in (1, 25):
    for mem in (1, 16):
        for speed in (0.0, 0.5, 1.0):
            v = cell(0, speed, run_len, mem)
            b = [rng.choice(v, len(v), replace=True).mean() for _ in range(10000)]
            print('%-34s %+0.4f    [%+0.4f, %+0.4f]    %d/%d'
                  % ('drift %.1f, run %d, mem %d' % (speed, run_len, mem),
                     v.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5), int((v < 0).sum()), len(v)))