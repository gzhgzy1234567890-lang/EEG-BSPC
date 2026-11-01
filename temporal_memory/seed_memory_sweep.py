# -*- coding: utf-8 -*-
"""SEED memory-length sweep at subject level (seed_memory_scale.json)."""
import json, os, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
R = r'G:\Work_work\math\EEG\paper_v8\results'
for name in ('seed_memory_scale.json', 'seed_memory_scale_runs.json'):
    p = os.path.join(R, name)
    if not os.path.exists(p):
        continue
    s = json.load(open(p, encoding='utf-8'))
    keys = [k for k in s[0] if k.startswith(('w', 'a'))]
    print('===', name, 'subjects', len({r['subj'] for r in s}), 'keys', keys)
    rng = np.random.default_rng(20261101)
    for k in keys:
        d = {}
        for r in s:
            d.setdefault(r['subj'], []).append(r[k])
        v = np.array([np.mean(x) for _, x in sorted(d.items())])
        b = [rng.choice(v, len(v), replace=True).mean() for _ in range(10000)]
        print('  %-6s mean %+0.4f  [%+0.4f, %+0.4f]  positive %d/%d'
              % (k, v.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5), int((v > 0).sum()), len(v)))
