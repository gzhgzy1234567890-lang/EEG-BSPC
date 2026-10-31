# -*- coding: utf-8 -*-
import json, os, sys
import numpy as np
from scipy.stats import binomtest
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'sleep_blocks_all.json')))
for r in rows:
    r['net'] = (r['err1'] - r['err0']) / float(r['n'])
    r['arm'] = 'hi' if r['maxfrac'] >= 0.8 else ('lo' if r['maxfrac'] < 0.6 else None)
def run(minc):
    cells = {}
    for r in rows:
        if r['arm'] is None:
            continue
        key = (r['subj'], r['ncls_block'], r['ncls_hist'], r['hist_len'])
        cells.setdefault(key, {'lo': [], 'hi': []})[r['arm']].append(r['net'])
    ok = {k: v for k, v in cells.items() if len(v['lo']) >= minc and len(v['hi']) >= minc}
    per = {}
    for (s, a, b, c), v in ok.items():
        per.setdefault(s, []).append(np.mean(v['hi']) - np.mean(v['lo']))
    d = np.array([np.mean(x) for x in per.values()])
    k = int((d > 0).sum())
    print('min blocks/arm=%d: cells %d, subjects %d, mean %+0.4f, positive %d/%d, p=%.3f'
          % (minc, len(ok), len(d), d.mean(), k, len(d), binomtest(k, len(d), 0.5).pvalue))
for m in (1, 2, 3, 5):
    run(m)