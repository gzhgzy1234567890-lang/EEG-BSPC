# -*- coding: utf-8 -*-
"""Effect sizes for the online decomposition conditions."""
import json, os, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'online_decomposition.json')))


def subj(key):
    d = {}
    for r in rows:
        d.setdefault(r['subj'], {}).setdefault(r['night'], []).append(r[key])
    return np.array([np.mean([np.mean(v) for v in n.values()]) for n in d.values()])


base = subj('none')
for cond in ('full', 'mix', 'within', 'shared', 'unmatched'):
    d = subj(cond) - base
    dz = d.mean() / d.std(ddof=1)
    print('%-10s delta %+0.4f  sd %.4f  dz %+0.2f' % (cond, d.mean(), d.std(ddof=1), dz))
