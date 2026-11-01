# -*- coding: utf-8 -*-
"""Machine traceability of Table 9: parse the manuscript cells, then compare with archives."""
import json, os, re, sys
import numpy as np
import docx
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SUB = r'G:\Work_work\math\EEG\submit'
REPO = r'G:\Work_work\math\EEG\repo_bspc'
PAPER = r'G:\Work_work\math\EEG\paper_v8\results'
rng = np.random.default_rng(20261101)


def boot_ci(v, n=20000):
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(n)]
    return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


NUM = re.compile(r'[+-]?\d+\.\d+')
m = docx.Document(os.path.join(SUB, 'BSPC_Candidate_V8.docx'))
tbl = [t for t in m.tables if len(t.rows) == 10 and len(t.columns) == 4][0]
cells = {r.cells[0].text.strip(): r.cells[1].text.strip() for r in tbl.rows[1:]}


def parsed(row):
    return [float(x) for x in NUM.findall(cells[row])]


checks = []
def check(name, row, expected, tol=1.5e-3):
    vals = parsed(row)
    ok = len(vals) >= len(expected) and all(abs(a - b) <= tol for a, b in zip(vals, expected))
    checks.append((name, ok, cells[row], vals[:len(expected)], expected))


# 1. BCI-2b, from the independent recomputation
st = json.load(open(os.path.join(REPO, 'origin_equivariance', 'results', 'statistics_recomputed_2b.json')))
csp = next(x for x in st if x['rep'] == 'csp')
check('2b', 'BCI-2b csp gain', [round(csp['delta'], 4), round(csp['lo'], 4), round(csp['hi'], 4)])

# 2. Sleep-EDF, from the hierarchy recomputation
h = json.load(open(os.path.join(REPO, 'sleep_edf', 'results', 'b3_hierarchy.json')))
check('sleep', 'Sleep-EDF cassette loss', [round(h['subject_mean'], 3), round(h['ci_low'], 3), round(h['ci_high'], 3)], tol=2.5e-3)

# 3. BCI-2a, from the 2x2 archive
rows2a = json.load(open(os.path.join(REPO, 'origin_equivariance', 'results', 'causal_2a.json'), encoding='utf-8'))
v2a = np.array([r['causal_so|euc_ea|lam1'] - r['causal_so|euc_ea|none'] for r in rows2a])
lo2a, hi2a = boot_ci(v2a)
check('2a', 'BCI-2a euc_ea gain', [round(v2a.mean(), 3), round(lo2a, 3), round(hi2a, 3)])

# 4. ERRp, from the archived per-subject deltas
e = json.load(open(os.path.join(PAPER, 'errp_external.json')))
dv = np.array([r['delta'] for r in e])
loe, hie = boot_ci(dv)
check('errp', 'BCI-challenge ERRp', [round(dv.mean(), 4), round(loe, 4), round(hie, 4)])

# 5. P300, from the archived per-subject deltas
p3 = json.load(open(os.path.join(PAPER, 'p300_external_meanamp.json')))
dp = np.array([r['delta'] for r in p3])
lop, hip = boot_ci(dp)
check('p300', 'P300 speller', [round(dp.mean(), 4), round(lop, 4), round(hip, 4)])

for name, ok, cell, got, exp in checks:
    print('%-6s %-5s cell=[%s]' % (name, 'OK' if ok else 'FAIL', cell))
    print('        parsed %s vs archive %s' % (['%+0.4f' % g for g in got], ['%+0.4f' % x for x in exp]))
untraced = ['SEED correction gain', 'Grasp-and-lift artefact']
print('not machine-traced (no per-subject archive in this checkout):', untraced)
status = 'PASS' if all(c[1] for c in checks) else 'FAIL'
print('TABLE TRACEABILITY', status, '(%d of 7 data rows traced)' % len(checks))
json.dump({'status': status, 'traced': [{'row': c[0], 'ok': c[1]} for c in checks], 'untraced': untraced},
          open(os.path.join(PAPER, 'table9_traceability.json'), 'w'), indent=1)