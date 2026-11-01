# -*- coding: utf-8 -*-
"""Append S34 to the supplement with the material moved out of the main text."""
import io, os, sys
import docx
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
S = 'G:/Work_work/math/EEG/submit/Supplementary_Material.docx'
m = docx.Document(S)
h_style = m.paragraphs[0].style
body = None
for p in m.paragraphs:
    if p.text.strip().startswith('S33'):
        h_style = p.style
        break
for p in m.paragraphs[1:]:
    if p.style.name == 'Normal' and len(p.text.strip().split()) > 30:
        body = p.style
        break
m.add_paragraph('S34. Material moved from the main text', style=h_style)
intro = ('This section holds analyses that the main text now summarises in one or two sentences. Nothing here is '
         'new: it is the text removed during the revision that added Sections 4.6 to 4.8, kept so that the numbers '
         'cited in the main text remain checkable.')
m.add_paragraph(intro, style=body)
parts = []
for name in ('trimmed_text.txt', 'trimmed_text2.txt', 'trimmed_text3.txt', 'trimmed_text4.txt'):
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        parts.append(io.open(p, encoding='utf-8').read())
text = '\n\n'.join(parts)
m.add_paragraph('Removed text, by original paragraph index.', style=body)
for chunk in text.split('\n\n'):
    c = chunk.strip()
    if c:
        m.add_paragraph(c, style=body)
m.save(S)
print('S34 appended; paragraphs now', len(m.paragraphs))
