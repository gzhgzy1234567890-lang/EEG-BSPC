# -*- coding: utf-8 -*-
import json, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
rows = json.load(open(r'G:\Work_work\math\EEG\paper_v8\results\sleep_decomposition_fixed3.json'))
per = {}
for r in rows:
    i = (r['full'] - r['none']) - ((r['mixture'] - r['none']) + (r['cond'] - r['none']))
    per.setdefault(r['subj'], {}).setdefault(r['night'], []).append(i)
vals = np.array([np.mean([np.mean(v) for v in n.values()]) for n in per.values()])
rng = np.random.default_rng(20261101)
boot = [rng.choice(vals, len(vals), replace=True).mean() for _ in range(10000)]
lo, hi = np.percentile(boot, [2.5, 97.5])
print('non-additivity I: subjects %d  mean %+0.4f  CI [%+0.4f, %+0.4f]  negative %d/%d'
      % (len(vals), vals.mean(), lo, hi, int((vals < 0).sum()), len(vals)))
print('aggregate check: full %+0.4f  mixture %+0.4f  cond %+0.4f  I %+0.4f'
      % (np.mean([r['full'] - r['none'] for r in rows]),
         np.mean([r['mixture'] - r['none'] for r in rows]),
         np.mean([r['cond'] - r['none'] for r in rows]),
         np.mean([(r['full'] - r['none']) - ((r['mixture'] - r['none']) + (r['cond'] - r['none'])) for r in rows])))