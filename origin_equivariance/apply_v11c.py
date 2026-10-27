# -*- coding: utf-8 -*-
"""v11c: table renumbering, limitations, and the docx build."""
import io
import os
import re
import subprocess

D = r"G:\Work_work\math\EEG\paper_v8"
P = os.path.join(D, "BSPC_draft_v9.md")
s = io.open(P, encoding="utf-8").read()

# renumber: the operating-point table becomes Table 6, the rest shift by one
s = s.replace("**Table 6b.** Leave-one-dataset-out operating point",
              "**Table 6.** Leave-one-dataset-out operating point")
s = s.replace("**Table 6.** Per-cell prediction of Equation (4).",
              "**Table 7.** Per-cell prediction of Equation (4).")
s = s.replace("**Table 7.** Alternatives to the mean correction.",
              "**Table 8.** Alternatives to the mean correction.")
s = s.replace("**Table 8.** Calibration, LDA, every cell",
              "**Table 9.** Calibration, LDA, every cell")
# in-text references
s = s.replace("Table 3 showed that the sign of the one-sided effect",
              "Table 3 showed that the sign of the one-sided effect")

# limitations: update the held-out and operating-point status
s = s.replace(
"""Five datasets, with a leave-one-dataset-out fit that is compressed, are not enough to certify a threshold, and a sixth dataset that played no role in choosing the statistic has not been tested.""",
"""A sixth dataset that played no role in choosing the statistic has now been tested at the level of datasets: SEED-IV lands where the relation predicts, and the six-dataset exact permutation p is 0.017. At the level of cells and representations the picture does not improve: within SEED-IV the statistic has an AUC of 0.48, within BCI-2a it cannot separate the four representations, and the leave-one-dataset-out operating point fails on two of five held-out datasets. What survives is a between-family triage, not a screening instrument, and we do not claim more.""")

io.open(P, "w", encoding="utf-8").write(s)

# docx
d = re.sub(r"## Highlights\s*\n(?:- .*\n)+", "", s)
d = re.sub(r"(^\*\*Keywords:\*\*.*$)", r"\1\n\n---", d, flags=re.M)
d = re.sub(r"## Figure captions\s*\n.*\Z", "", d, flags=re.S)
io.open(os.path.join(D, "_v11_docx.md"), "w", encoding="utf-8").write(d)

b = io.open(os.path.join(D, "md2docx_v10.py"), encoding="utf-8").read()
b = b.replace("_v10_docx.md", "_v11_docx.md")
b = b.replace("BSPC_Manuscript_v10_with_figs.docx", "BSPC_Manuscript_v11_with_figs.docx")
b = b.replace("BSPC_Manuscript_v10.docx", "BSPC_Manuscript_v11.docx")
io.open(os.path.join(D, "md2docx_v11.py"), "w", encoding="utf-8").write(b)
r = subprocess.run(["python", "md2docx_v11.py", "--with-figs"], cwd=D,
                   capture_output=True, text=True)
print((r.stdout or "").strip()[-90:])

from docx import Document
doc = Document(os.path.join(D, "BSPC_Manuscript_v11_with_figs.docx"))
ps = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
b2 = "\n".join(ps)
print("paras", len(ps), "tables", len(doc.tables), "images", len(doc.inline_shapes),
      "carets", b2.count("^"))
print("tables captioned:", [p[:12] for p in ps if p.startswith("Table ")])
