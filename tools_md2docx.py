# -*- coding: utf-8 -*-
"""Minimal markdown -> docx converter for the response letter."""
import io, os, re, sys
import docx
from docx.shared import Pt
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SRC = r'G:\Work_work\math\EEG\submit\RESPONSE_TO_REFEREE.md'
OUT = r'G:\Work_work\math\EEG\submit\Response_to_Reviewers.docx'
lines = io.open(SRC, encoding='utf-8').read().splitlines()
d = docx.Document()
d.styles['Normal'].font.name = 'Calibri'
d.styles['Normal'].font.size = Pt(10.5)
i = 0
while i < len(lines):
    line = lines[i].rstrip()
    if not line.strip():
        i += 1; continue
    if line.startswith('# '):
        d.add_heading(line[2:].strip(), level=1); i += 1; continue
    if line.startswith('## '):
        d.add_heading(line[3:].strip(), level=2); i += 1; continue
    if line.startswith('|'):
        block = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            row = [c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not re.match(r'^[-: ]+$', ''.join(row)):
                block.append(row)
            i += 1
        if block:
            t = d.add_table(rows=len(block), cols=max(len(r) for r in block))
            for a, row in enumerate(block):
                for b, cell in enumerate(row):
                    if b < len(t.rows[a].cells):
                        t.rows[a].cells[b].text = cell
                        for p in t.rows[a].cells[b].paragraphs:
                            for r in p.runs:
                                r.font.size = Pt(8.5)
            t.style = 'Table Grid'
        continue
    if line.startswith('- '):
        d.add_paragraph(line[2:].strip(), style='List Bullet'); i += 1; continue
    para = [line.strip()]
    i += 1
    while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||- )', lines[i].strip()):
        para.append(lines[i].strip()); i += 1
    d.add_paragraph(' '.join(para))
d.save(OUT)
print('wrote', OUT, 'paragraphs', len(d.paragraphs), 'tables', len(d.tables))