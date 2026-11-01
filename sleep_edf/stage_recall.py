# -*- coding: utf-8 -*-
"""Per-stage recall and flip rates from the online decomposition."""
import json, os, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'online_decomposition.json')))
stages = {0: 'W', 1: 'N1', 2: 'N2', 3: 'N3', 4: 'R'}
for c in sorted(stages):
    key = 'support_%d' % c
    sup = sum(r.get(key, 0) for r in rows)
    rn = [r['recall_none_%d' % c] for r in rows if 'recall_none_%d' % c in r]
    rf = [r['recall_full_%d' % c] for r in rows if 'recall_full_%d' % c in r]
    if rn:
        print('%-3s support %6d  recall none %.3f  full %.3f  change %+0.3f'
              % (stages[c], sup, np.mean(rn), np.mean(rf), np.mean(rf) - np.mean(rn)))
for k in ('full', 'mix', 'within', 'shared'):
    v = [r[k + '_flip'] for r in rows]
    print('flip rate %-8s %.3f' % (k, float(np.mean(v))))
