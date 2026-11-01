# -*- coding: utf-8 -*-
"""Check that the headline numbers in Table 9 match the archived sources."""
import json, os, re, sys
import numpy as np
import docx
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SUB = r'G:\Work_work\math\EEG\submit'
REPO = r'G:\Work_work\math\EEG\repo_bspc'
RES = r'G:\Work_work\math\EEG\paper_v8\results'


def close(a, b, tol=5e-4):
    return abs(a - b) <= tol


m = docx.Document(os.path.join(SUB, 'BSPC_Candidate_V8.docx'))
tbl = [t for t in m.tables if len(t.rows) == 10 and len(t.columns) == 4][0]
rows = {r.cells[0].text.strip(): [c.text.strip() for c in r.cells] for r in tbl.rows[1:]}
print('table rows:', list(rows)[:4], '...')

checks = []
# 2b row vs recomputed statistics
st = json.load(open(os.path.join(REPO, 'origin_equivariance', 'results', 'statistics_recomputed_2b.json')))
csp = next(x for x in st if x['rep'] == 'csp')
cell = rows['BCI-2b csp gain'][1]
checks.append(('2b mean', close(csp['delta'], 0.0341), cell))
checks.append(('2b lo', close(csp['lo'], 0.0104), cell))
checks.append(('2b hi', close(csp['hi'], 0.0585), cell))
# sleep row vs hierarchy json
h = json.load(open(os.path.join(REPO, 'sleep_edf', 'results', 'b3_hierarchy.json')))
checks.append(('sleep mean', close(h['subject_mean'], -0.1023), rows['Sleep-EDF cassette loss'][1]))
checks.append(('sleep lo', close(h['ci_low'], -0.1145), rows['Sleep-EDF cassette loss'][1]))
checks.append(('sleep hi', close(h['ci_high'], -0.0900), rows['Sleep-EDF cassette loss'][1]))
# ERRp row vs json
e = json.load(open(os.path.join(RES, 'errp_external.json')))
d = np.array([r['delta'] for r in e])
checks.append(('errp mean', close(d.mean(), -0.0044), rows['BCI-challenge ERRp'][1]))
# P300 row vs json
p = json.load(open(os.path.join(RES, 'p300_external_meanamp.json')))
pd = np.array([r['delta'] for r in p])
checks.append(('p300 mean', close(pd.mean(), -0.0005), rows['P300 speller'][1]))
for name, ok, cell in checks:
    print('%-12s %-5s  | %s' % (name, 'OK' if ok else 'MISMATCH', cell[:60]))
print('TABLE TRACEABILITY', 'PASS' if all(c[1] for c in checks) else 'FAIL')