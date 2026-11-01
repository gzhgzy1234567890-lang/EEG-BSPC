# -*- coding: utf-8 -*-
"""Move Tables 4 and 5 to S35 and renumber the rest in one pass (no cascades)."""
import copy, os, re, sys
import docx
from docx.oxml.ns import qn
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
M = 'G:/Work_work/math/EEG/submit/BSPC_Candidate_V8.docx'
S = 'G:/Work_work/math/EEG/submit/Supplementary_Material.docx'
m = docx.Document(M)
s = docx.Document(S)


def caption(prefix):
    for p in m.paragraphs:
        if p.text.strip().startswith(prefix):
            return p
    return None


pairs = []
for pref in ('Table 4.', 'Table 5.'):
    cap = caption(pref)
    el = cap._p.getnext()
    tbl_el = None
    while el is not None:
        if el.tag == qn('w:tbl'):
            tbl_el = el
            break
        el = el.getnext()
    pairs.append((cap, tbl_el))

h_style = body_style = None
for p in s.paragraphs:
    if p.text.strip().startswith('S34'):
        h_style = p.style
        break
for p in s.paragraphs[1:]:
    if p.style.name == 'Normal' and len(p.text.strip().split()) > 30:
        body_style = p.style
        break
s.add_paragraph('S35. Estimator comparison tables moved from the main text', style=h_style)
s.add_paragraph('The tables of the estimator comparison are kept here. The main text reports the pattern and the '
                'controlled comparisons, and points to this section for the full ranking.', style=body_style)
for cap, tbl_el in pairs:
    s.add_paragraph(cap.text, style=cap.style)
    if tbl_el is not None:
        s.element.body.append(copy.deepcopy(tbl_el))
s.save(S)

for cap, tbl_el in pairs:
    if tbl_el is not None:
        tbl_el.getparent().remove(tbl_el)
    cap._p.getparent().remove(cap._p)

# one pass, protect with placeholders
mapping = {9: 7, 8: 6, 7: 5, 6: 4}
changed = 0
for p in m.paragraphs:
    full = p.text
    if not re.search(r'Table [6-9]\b', full):
        continue
    new = full
    for old, newnum in mapping.items():
        new = re.sub(r'Table %d\b' % old, 'Table @@%d@@' % newnum, new)
    new = new.replace('@@', '')
    if new != full:
        runs = [r for r in p.runs if r.text]
        runs[0].text = new
        for r in runs[1:]:
            r.text = ''
        changed += 1
p = next(x for x in m.paragraphs if x.text.strip().startswith('Table 4 includes the two target-informed'))
runs = [r for r in p.runs if r.text]
runs[0].text = ('The comparison that follows uses source-only representations; the two target-informed ones are '
                'reported in the supplement (S35).')
for r in runs[1:]:
    r.text = ''
m.save(M)
print('renumbered paragraphs:', changed)
print('captions:', [p.text.strip()[:26] for p in m.paragraphs if p.text.strip().startswith('Table ')])
print('tables:', len(m.tables))
