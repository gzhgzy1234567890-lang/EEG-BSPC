# -*- coding: utf-8 -*-
"""Final cross-document consistency check."""
import csv, hashlib, io, os, re, sys
import docx
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SUB = r'G:\Work_work\math\EEG\submit'
m = docx.Document(os.path.join(SUB, 'BSPC_Candidate_V8.docx'))
paras = [p.text for p in m.paragraphs]
abstract = paras[8]
body = ' '.join(paras[9:])
nums = set(re.findall(r'\d+\.\d{3,4}', abstract))
missing = [n for n in nums if n not in body]
print('abstract numbers:', sorted(nums))
print('numbers in abstract but not in body:', missing)
claims = list(csv.DictReader(io.open(os.path.join(SUB, 'CLAIM_EVIDENCE_MATRIX.csv'), encoding='utf-8')))
secs = set()
for p in m.paragraphs:
    mm = re.match(r'^(\d+(?:\.\d+)?)\.', p.text.strip())
    if mm:
        secs.add(mm.group(1))
bad = []
for c in claims:
    loc = c['manuscript_location']
    found = [s for s in re.findall(r'\d+(?:\.\d+)?', loc) if s in secs]
    ok = bool(found) or 'WITHDRAWN' in c['evidence_class'] or loc.endswith('.md') or re.match(r'^S\d', loc) or 'Discussion' in loc
    if not ok:
        bad.append((c['claim'][:50], loc))
print('claims whose manuscript location is not a known section:', bad)
fr = io.open(os.path.join(SUB, 'FREEZE_RECORD.md'), encoding='utf-8').read()
rows = re.findall(r'\|\s*([\w./-]+\.(?:docx|pdf|png))\s*\|\s*\d+\s*\|\s*([0-9a-f]{16})\s*\|', fr)
mism = []
for name, h in rows:
    p = os.path.join(SUB, name.replace('/', os.sep))
    if not os.path.exists(p):
        mism.append((name, 'missing')); continue
    real = hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    if real != h:
        mism.append((name, 'hash'))
print('freeze rows', len(rows), 'mismatches', mism)
print('CONSISTENCY', 'PASS' if not missing and not bad and not mism else 'FAIL')