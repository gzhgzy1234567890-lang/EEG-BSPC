# -*- coding: utf-8 -*-
"""Automated submission consistency check (goal section 8.4)."""
import csv, docx, os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SUB = r'G:\Work_work\math\EEG\submit'
M = os.path.join(SUB, 'Revised_Manuscript.docx')
S = os.path.join(SUB, 'Revised_Supplementary.docx')
H = os.path.join(SUB, 'Revised_Highlights.docx')
C = os.path.join(SUB, 'Revised_Cover_Letter.docx')
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ((' :: ' + detail) if detail and not ok else ''))
    if not ok:
        fails.append(name)

m = docx.Document(M); s = docx.Document(S); h = docx.Document(H); c = docx.Document(C)
body = ' '.join(p.text for p in m.paragraphs)
abstract = m.paragraphs[8].text

# 1 abstract numbers appear in the body
nums = re.findall(r'\d+\.\d+', abstract)
missing = [n for n in nums if n not in body]
check('abstract numbers in body', not missing, str(missing))

# 2 table and figure numbering
caps = [p.text.strip() for p in m.paragraphs if re.match(r'^(Table|Fig\.)', p.text.strip())]
tabs = [int(x.split()[1].rstrip('.')) for x in caps if x.startswith('Table')]
figs = [int(x.split()[1].rstrip('.')) for x in caps if x.startswith('Fig')]
check('tables sequential', tabs == sorted(tabs) and tabs == list(range(1, len(tabs) + 1)), str(tabs))
check('figures sequential', figs == sorted(figs) and figs == list(range(1, len(figs) + 1)), str(figs))
check('table count matches documents', len(m.tables) == len(tabs), '%d elements, %d captions' % (len(m.tables), len(tabs)))

# 3 every referenced section exists
heads = set()
for p in m.paragraphs:
    if p.style.name.startswith('BSPC Heading'):
        g = re.match(r'(\d+(?:\.\d+)?)\.', p.text.strip())
        if g:
            heads.add(g.group(1))
refs = set(re.findall(r'Section (\d+(?:\.\d+)?)', body))
missing_secs = [r for r in refs if r not in heads]
check('section references resolve', not missing_secs, str(missing_secs))

# 4 supplement S numbers exist
s_heads = {x.group(0) for p in s.paragraphs for x in [re.match(r'S\d+', p.text.strip())] if x}
s_refs = set(re.findall(r'\bS\d{1,2}\b', body))
missing_s = sorted(r for r in s_refs if r not in s_heads)
check('supplement references resolve', not missing_s, str(missing_s))

# 5 highlights length
items = [p.text.strip() for p in h.paragraphs if p.text.strip() and not p.text.strip().lower().startswith('highlights')]
check('five highlights', len(items) == 5, str(len(items)))
check('highlight length <= 85', all(len(x) <= 85 for x in items), str([len(x) for x in items]))

# 6 cover letter numbers agree with the manuscript
cl = ' '.join(p.text for p in c.paragraphs)
key = ['0.214', '0.102', '0.0715', '0.0202']
check('cover letter numbers present in manuscript', all(k in body for k in key), str([k for k in key if k not in body]))
check('cover letter uses the current title', 'decision geometry, temporal memory' in cl.lower())

# 7 word counts
words = len(body.split())
check('body within 6500-7500', 6500 <= words <= 7500, str(words))

# 8 experiment arithmetic in the supplement
st = ' '.join(p.text for p in s.paragraphs)
check('factorial arithmetic stated', '1,440 independent data streams' in st)
check('strength sweep arithmetic stated', '2,880 strength-condition rows' in st or '5,760 strength evaluations' in st)

# 9 commit reference
check('commit ef8c890 cited', 'ef8c890' in body)

print()
print('SUBMISSION CHECK', 'PASS' if not fails else 'FAIL (%d)' % len(fails))