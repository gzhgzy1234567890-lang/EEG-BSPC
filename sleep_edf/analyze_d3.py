# -*- coding: utf-8 -*-
"""Evaluate several matching specifications from the per-block D3 records."""
import json, os, sys, itertools
from collections import defaultdict
import numpy as np
from scipy.stats import wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
recs = json.load(open(os.path.join(HERE, 'results', 'd3_blocks.json')))
print('block records', len(recs), '| subjects', len({r['subj'] for r in recs}))


def spec(name, keyfn, min_blocks=2):
    strata = defaultdict(list)
    for r in recs:
        strata[(r['subj'],) + keyfn(r)].append(r['delta'])
    subj = defaultdict(list)
    used = 0
    for (s, *_), v in strata.items():
        if len(v) >= min_blocks:
            subj[s].append(float(np.mean(v)))
            used += 1
    vals = np.array([np.mean(v) for v in subj.values()])
    if len(vals) < 3:
        print('%-38s too few subjects (%d)' % (name, len(vals)))
        return
    p = wilcoxon(vals).pvalue
    print('%-38s subjects %2d  strata %3d  mean %+0.4f  positive %2d  p=%.3f'
          % (name, len(vals), used, vals.mean(), int((vals > 0).sum()), p))
    return vals


spec('A exact classes+prior(0.01)', lambda r: (tuple(r['classes_block']), tuple(r['classes_hist']), r['prior']))
spec('B classes+prior bin 0.1', lambda r: (tuple(r['classes_block']), tuple(r['classes_hist']), round(r['prior'], 1)))
spec('C classes only', lambda r: (tuple(r['classes_block']), tuple(r['classes_hist'])))
spec('D classes+prior 0.1+block index', lambda r: (tuple(r['classes_block']), tuple(r['classes_hist']), round(r['prior'], 1), r['block']))
spec('E exact classes+prior, >=3 blocks', lambda r: (tuple(r['classes_block']), tuple(r['classes_hist']), r['prior']), min_blocks=3)
spec('F balanced prior only (0.5)', lambda r: (tuple(r['classes_block']), tuple(r['classes_hist']), 0.5 if abs(r['prior'] - 0.5) < 0.05 else 9.9))