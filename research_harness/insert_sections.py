# -*- coding: utf-8 -*-
"""Insert the three mechanism sections and renumber the later ones (v2)."""
import json, os, sys
import docx
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
M = 'G:/Work_work/math/EEG/submit/BSPC_Candidate_V8.docx'
m = docx.Document(M)
block = json.load(open(os.path.join(HERE, 'new_sections.json'), encoding='utf-8'))


def find_para(prefix):
    for p in m.paragraphs:
        if p.text.strip().startswith(prefix):
            return p
    raise SystemExit('not found: ' + prefix)


def set_text(p, text):
    runs = [r for r in p.runs if r.text]
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r.text = ''
    else:
        p.add_run(text)


renames = [('4.8. ', '4.11. '), ('4.7. ', '4.10. '), ('4.6. ', '4.9. ')]
for old, new in renames:
    p = find_para(old)
    set_text(p, new + p.text.strip()[len(old):])
print('renamed:', [find_para(x).text.strip()[:30] for x in ('4.9.', '4.10.', '4.11.')])

anchor = find_para('4.9. ')
h_style = anchor.style
body_style = m.paragraphs[42].style
seq = [('h', block['h1']), ('p', block['p1']), ('p', block['p2']), ('p', block['p3']),
       ('h', block['h2']), ('p', block['q1']), ('p', block['q2']), ('p', block['q3']),
       ('h', block['h3']), ('p', block['r1']), ('p', block['r2'])]
added = 0
for kind, text in seq:
    p = anchor.insert_paragraph_before(text, style=(h_style if kind == 'h' else body_style))
    added += 1
m.save(M)
print('inserted', added)
print('paragraph words', len(' '.join(p.text for p in m.paragraphs).split()))
