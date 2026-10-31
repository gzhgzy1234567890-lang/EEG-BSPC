# -*- coding: utf-8 -*-
import json, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
rows = json.load(open(r'G:\Work_work\math\EEG\paper_v8\results\sleep_decomposition_fixed2.json'))
same = [r for r in rows if r['n_only_a'] == 0 and r['n_only_b'] == 0]
print('cells with identical class sets:', len(same), 'of', len(rows))
subs = {}
for r in same:
    subs.setdefault(r['subj'], {}).setdefault(r['night'], []).append(r)
def sm(k):
    return np.array([np.mean([np.mean([c[k] for c in v]) for v in n.values()]) for n in subs.values()])
base = sm('none')
for k in ('full', 'prior', 'cond'):
    d = sm(k) - base
    print('%-6s BA %.4f delta %+0.4f negative %d/%d' % (k, sm(k).mean(), d.mean(), int((d < 0).sum()), len(d)))