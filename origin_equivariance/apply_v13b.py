# -*- coding: utf-8 -*-
"""v13b: report both parameterisations, the circularity, the 2a subproblem; trim
the abstract; rebuild the docx."""
import io
import os
import re
import subprocess

D = r"G:\Work_work\math\EEG\paper_v8"
P = os.path.join(D, "BSPC_draft_v9.md")
s = io.open(P, encoding="utf-8").read()

# trim abstract by four words
s = s.replace("Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We ask what the choice is, and what it can and cannot buy.",
              "Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We ask what the choice is, and what it can buy.")

# 2a subproblem in the per-cell table caption
s = s.replace("**Table 7.** Per-cell prediction of Equation (4).",
              "**Table 7.** Per-cell prediction of Equation (4). For BCI-2a the cells are the two-class subproblem of classes 1 and 2; the four-class problem is not covered by the law.")

# insert the two-parameterisation result before the classifier paragraph
anchor = "The classifier family is not the variable: t* is."
add = """**Two parameterisations, and which one the model requires.** The numbers in Table 7 use c = Φ⁻¹(BA_aligned) and a *pooled* score standard deviation. The equal-variance Gaussian derivation uses the *within-class* standard deviation and fixes c from the class separation, c = (m₁ − m₀)/(2σ_w), and these are not the same parameterisation: for two equal-variance classes σ²_pooled = σ²_with + (m₁ − m₀)²/4. We therefore recomputed the law the way the model requires. The fit degrades: for LDA on BCI-2b the correlation falls from 0.989 to 0.861 and the mean absolute error rises from 0.013 to 0.057; on BCI-2a from 0.902 to 0.874; on grasp-and-lift from 0.649 to 0.271, and on NER2015 the within-class scale is not estimable in enough cells to report. The model's own implied accuracy Φ(c) is also far from the observed aligned accuracy, by 0.096 on BCI-2b and 0.213 on grasp-and-lift, which is a direct statement that the equal-variance Gaussian assumption does not hold on these scores.

There is a second reason to be careful with the pooled-parameterisation figures. In that variant c is computed from BA_aligned, and BA_aligned also enters the observed change, so part of the high correlation is built in rather than predicted. We report both variants and treat the pooled one as a descriptive decomposition and the within-class one as the model check; neither supports the word "predictive law", and the paper no longer uses it.

"""
if anchor not in s:
    print("MISS anchor")
s = s.replace(anchor, add + anchor, 1)

io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("abstract:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))

# rebuild
d = re.sub(r"## Highlights\s*\n(?:- .*\n)+", "", s)
d = re.sub(r"(^\*\*Keywords:\*\*.*$)", r"\1\n\n---", d, flags=re.M)
d = re.sub(r"## Figure captions\s*\n.*\Z", "", d, flags=re.S)
io.open(os.path.join(D, "_v13_docx.md"), "w", encoding="utf-8").write(d)
b = io.open(os.path.join(D, "md2docx_v12.py"), encoding="utf-8").read()
b = b.replace("_v12_docx.md", "_v13_docx.md")
b = b.replace("BSPC_Manuscript_v12_with_figs.docx", "BSPC_Manuscript_v13_with_figs.docx")
b = b.replace("BSPC_Manuscript_v12.docx", "BSPC_Manuscript_v13.docx")
io.open(os.path.join(D, "md2docx_v13.py"), "w", encoding="utf-8").write(b)
r = subprocess.run(["python", "md2docx_v13.py", "--with-figs"], cwd=D, capture_output=True, text=True)
print((r.stdout or "").strip()[-80:])
from docx import Document
doc = Document(os.path.join(D, "BSPC_Manuscript_v13_with_figs.docx"))
ps = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
print("paras", len(ps), "tables", len(doc.tables), "images", len(doc.inline_shapes))
