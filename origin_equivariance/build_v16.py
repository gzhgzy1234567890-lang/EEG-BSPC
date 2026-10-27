# -*- coding: utf-8 -*-
"""Build BSPC_Manuscript_v16_with_figs.docx from the rewritten manuscript."""
import io
import os
import re
import subprocess

D = r"G:\Work_work\math\EEG\paper_v8"
src = os.path.join(D, "BSPC_draft_v16.md")
s = io.open(src, encoding="utf-8").read()

d = re.sub(r"## Highlights\s*\n(?:- .*\n)+", "", s)
d = re.sub(r"(^\*\*Keywords:\*\*.*$)", r"\1\n\n---", d, flags=re.M)
d = re.sub(r"## Figure captions\s*\n.*\Z", "", d, flags=re.S)
io.open(os.path.join(D, "_v16_docx.md"), "w", encoding="utf-8").write(d)

b = io.open(os.path.join(D, "md2docx_v13.py"), encoding="utf-8").read()
b = b.replace("_v13_docx.md", "_v16_docx.md")
b = b.replace("BSPC_Manuscript_v13_with_figs.docx", "BSPC_Manuscript_v16_with_figs.docx")
b = b.replace("BSPC_Manuscript_v13.docx", "BSPC_Manuscript_v16.docx")
io.open(os.path.join(D, "md2docx_v16.py"), "w", encoding="utf-8").write(b)
r = subprocess.run(["python", "md2docx_v16.py", "--with-figs"], cwd=D,
                   capture_output=True, text=True)
print((r.stdout or "").strip()[-90:])
print((r.stderr or "").strip()[-200:])

from docx import Document
doc = Document(os.path.join(D, "BSPC_Manuscript_v16_with_figs.docx"))
ps = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
body = "\n".join(ps)
print("paras", len(ps), "tables", len(doc.tables), "images", len(doc.inline_shapes))
print("carets", body.count("^"), "| '(' placeholders:", body.count("TODO"))
print("tables:", [p[:9] for p in ps if p.startswith("Table ")])
print("figs:", [p[:8] for p in ps if p.startswith("Fig. ") and "." in p[:7]])

# numeric consistency: no stale values
for pat in ["−0.94", "−0.90 (p", "0.017", "0.482", "z_w = 1.00", "80–97", "earlier version", "referee"]:
    c = body.count(pat)
    if c:
        print("STALE", repr(pat), c)
