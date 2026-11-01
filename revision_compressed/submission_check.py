# -*- coding: utf-8 -*-
"""Self-contained submission checker: resolves paths relative to the archive."""
import csv, docx, os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
def resolve(name):
    for base in (HERE, os.path.join(HERE, '..'), os.path.dirname(HERE)):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return os.path.abspath(p)
    return None
M = resolve('Revised_Manuscript.docx'); S = resolve('Revised_Supplementary.docx')
H = resolve('Revised_Highlights.docx'); C = resolve('Revised_Cover_Letter.docx')
missing = [n for n, p in (('manuscript', M), ('supplement', S), ('highlights', H), ('cover letter', C)) if p is None]
if missing:
    print('CANNOT LOCATE:', missing, '- run from the unzipped package')
    sys.exit(2)
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ((' :: ' + detail) if detail and not ok else ''))
    if not ok:
        fails.append(name)
m = docx.Document(M); s = docx.Document(S); h = docx.Document(H); c = docx.Document(C)
body = ' '.join(p.text for p in m.paragraphs)
abstract = m.paragraphs[8].text
check('abstract numbers in body', not [n for n in re.findall(r'\d+\.\d+', abstract) if n not in body])
caps = [p.text.strip() for p in m.paragraphs if re.match(r'^(Table|Fig\.)', p.text.strip())]
tabs = [int(x.split()[1].rstrip('.')) for x in caps if x.startswith('Table')]
figs = [int(x.split()[1].rstrip('.')) for x in caps if x.startswith('Fig')]
check('tables sequential', tabs == list(range(1, len(tabs) + 1)), str(tabs))
check('figures sequential', figs == list(range(1, len(figs) + 1)), str(figs))
check('table elements match captions', len(m.tables) == len(tabs), '%d vs %d' % (len(m.tables), len(tabs)))
heads = set()
for p in m.paragraphs:
    if p.style.name.startswith('BSPC Heading'):
        g = re.match(r'(\d+(?:\.\d+)?)\.', p.text.strip())
        if g:
            heads.add(g.group(1))
bad = [r for r in set(re.findall(r'Section (\d+(?:\.\d+)?)', body)) if r not in heads]
check('section references resolve', not bad, str(bad))
s_heads = {x.group(0) for p in s.paragraphs for x in [re.match(r'S\d+', p.text.strip())] if x}
bad_s = [r for r in set(re.findall(r'\bS\d{1,2}\b', body)) if r not in s_heads]
check('supplement references resolve', not bad_s, str(bad_s))
items = [p.text.strip() for p in h.paragraphs if p.text.strip() and not p.text.strip().lower().startswith('highlights')]
check('five highlights', len(items) == 5, str(len(items)))
check('highlights within 85 characters', all(len(x) <= 85 for x in items), str([len(x) for x in items]))
cl = ' '.join(p.text for p in c.paragraphs)
check('cover-letter numbers in manuscript', all(k in body for k in ['0.214', '0.102', '0.0715', '0.0202']))
check('cover letter carries the current title', 'decision geometry, temporal memory' in cl.lower())
words = len(body.split())
check('body within 6500-7500', 6500 <= words <= 7500, str(words))
st = ' '.join(p.text for p in s.paragraphs)
check('factorial arithmetic stated', '1,440 runs' in body or '1,440 independent data streams' in st)
check('strength sweep arithmetic stated', '2,880 strength-condition rows' in st)
check('commit ef8c890 cited', 'ef8c890' in body)
man = resolve('Result_to_Code_Manifest.csv')
if man:
    rows_ = list(csv.reader(open(man, encoding='utf-8')))
    check('manifest columns uniform', len({len(r) for r in rows_}) == 1, str(sorted({len(r) for r in rows_})))
    check('manifest commit column filled', all(r[-1] == 'ef8c890' for r in rows_[1:]))
print()
print('SUBMISSION CHECK', 'PASS' if not fails else 'FAIL (%d)' % len(fails))
