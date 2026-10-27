# -*- coding: utf-8 -*-
"""Build a docx-ready markdown: drop the Highlights block (BSPC wants it as a
separate file) and the duplicate captions section, then rebuild the docx."""
import io
import os
import re
import subprocess
import sys

D = r"G:\Work_work\math\EEG\paper_v8"
s = io.open(os.path.join(D, "BSPC_draft_v8.md"), encoding="utf-8").read()

# remove the Highlights section (heading + bullets up to the next '## ')
s = re.sub(r"## Highlights\s*\n(?:- .*\n)+", "", s)
# remove the captions section if present
s = re.sub(r"## Figure captions\s*\n.*\Z", "", s, flags=re.S)

io.open(os.path.join(D, "_v8_docx.md"), "w", encoding="utf-8").write(s)

# point the builder at the docx-only markdown
b = io.open(os.path.join(D, "md2docx_v8.py"), encoding="utf-8").read()
b = b.replace('BSPC_draft_v8.md', '_v8_docx.md')
io.open(os.path.join(D, "md2docx_v8.py"), "w", encoding="utf-8").write(b)
print("ready")
