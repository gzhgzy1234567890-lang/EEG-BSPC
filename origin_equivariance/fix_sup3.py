# -*- coding: utf-8 -*-
"""Use a dagger for equal contribution so no footnote line starts with a caret."""
import io
import os
import subprocess

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(P, encoding="utf-8").read()
s = s.replace("Zihao Gong ^a,1^, Jiran Li ^b,1^", "Zihao Gong ^a,\u2020^, Jiran Li ^b,\u2020^")
s = s.replace("^1^ These authors contributed equally to this work.",
              "\u2020 These authors contributed equally to this work.")
s = s.replace("^*^ Corresponding author. E-mail address:",
              "* Corresponding author. E-mail address:")
io.open(P, "w", encoding="utf-8").write(s)
for cmd in (["python", "prep_docx2.py"], ["python", "md2docx_v8.py", "--with-figs"]):
    r = subprocess.run(cmd, cwd=os.path.dirname(P), capture_output=True, text=True)
    print(cmd[-1], (r.stdout or "").strip()[-70:])
