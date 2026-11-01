# -*- coding: utf-8 -*-
"""Final audit: every headline number in the manuscript against its archive."""
import json, os, re, sys
import numpy as np
import docx
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SUB = r'G:\Work_work\math\EEG\submit'
R = r'G:\Work_work\math\EEG\paper_v8\results'
m = docx.Document(os.path.join(SUB, 'BSPC_Candidate_V8.docx'))
text = ' '.join(p.text for p in m.paragraphs)
for t in m.tables:
    for row in t.rows:
        for c in row.cells:
            text += ' ' + c.text

online = json.load(open(os.path.join(R, 'online_decomposition.json')))
fac = json.load(open(os.path.join(R, 'factorial_2x2_rich.json')))
lam = json.load(open(os.path.join(R, 'factorial_lambda.json')))
sw = json.load(open(os.path.join(R, 'sleep_memory_sweep.json')))
seeds = json.load(open(os.path.join(R, 'seed_transductive.json')))

def subj(rows, key):
    d = {}
    for r in rows:
        d.setdefault(r['subj'], {}).setdefault(r.get('night', 0), []).append(r[key])
    return np.array([np.mean([np.mean(v) for v in n.values()]) for n in d.values()])

checks = []
def chk(name, value, nd):
    s = '%.*f' % (nd, abs(value))
    ok = s in text
    checks.append((name, ('%+.*f' % (nd, value)), ok))

b0 = subj(online, 'none')
for cond in ('full', 'mix', 'within'):
    d = subj(online, cond) - b0
    chk('online ' + cond, d.mean(), 4)

def fcell(prior, drift, key='delta'):
    d = {}
    for r in fac:
        if r['prior_shift'] == prior and abs(r['drift'] - drift) < 1e-9:
            d.setdefault(r['subj'], []).append(r[key])
    return np.array([np.mean(v) for _, v in sorted(d.items())])

for name, (p, dr) in (('A', (0, 0.0)), ('B', (1, 0.0)), ('C', (0, 1.0)), ('D', (1, 1.0))):
    chk('factorial ' + name, fcell(p, dr).mean(), 4)

def scell(prior, drift, mm):
    d = {}
    for r in sw:
        d.setdefault(r['subj'], {}).setdefault(r['night'], []).append(r[mm] - r['none'])
    return np.array([np.mean([np.mean(v) for v in n.values()]) for n in d.values()])
for mm in ('mem1', 'mem2', 'mem3'):
    chk('sleep ' + mm, scell(0, 0, mm).mean(), 4)

chk('seed recomputed', np.mean([r['delta'] for r in seeds]), 3)

bad = [c for c in checks if not c[2]]
for name, s, ok in checks:
    print('%-18s %-9s %s' % (name, s, 'found' if ok else 'MISSING'))
print('FINAL AUDIT', 'PASS' if not bad else 'FAIL (%d)' % len(bad))