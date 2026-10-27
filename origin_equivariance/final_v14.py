# -*- coding: utf-8 -*-
"""Trim the abstract and rebuild the v13 docx."""
import io
import os
import re
import subprocess

D = r"G:\Work_work\math\EEG\paper_v8"
P = os.path.join(D, "BSPC_draft_v9.md")
s = io.open(P, encoding="utf-8").read()
s = s.replace(" and its held-out operating point (specificity 0.000) do not support it as a screening tool. We therefore report it as an exploratory analysis and not as a contribution. What the paper claims is a mechanism and its boundaries.",
              " and its held-out operating point (specificity 0.000) do not support screening. We report it as exploratory, not as a contribution.")
io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("abstract:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))

d = re.sub(r"## Highlights\s*\n(?:- .*\n)+", "", s)
d = re.sub(r"(^\*\*Keywords:\*\*.*$)", r"\1\n\n---", d, flags=re.M)
d = re.sub(r"## Figure captions\s*\n.*\Z", "", d, flags=re.S)
io.open(os.path.join(D, "_v13_docx.md"), "w", encoding="utf-8").write(d)
r = subprocess.run(["python", "md2docx_v13.py", "--with-figs"], cwd=D,
                   capture_output=True, text=True)
print((r.stdout or "").strip()[-70:])
