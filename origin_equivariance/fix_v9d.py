# -*- coding: utf-8 -*-
"""v9c: trim the abstract and update the highlights."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()

s = s.replace(
    " and a leave-one-dataset-out fit reproduces the order of the three most damaged datasets.",
    ".")

old_h = """- The equivariant family of mean corrections is stated; uniqueness is not claimed.
- Prediction equivalence is characterized by the centred classifier weights.
- An equal-norm origin experiment shows the source-only screen is direction-blind.
- A signed damage law predicts the sign across classifier families.
- The collapse certificate is an algebraic diagnostic, not a predictor."""

new_h = """- The equivariant family of mean corrections is stated; uniqueness is not claimed.
- Prediction equivalence is characterized by the centred classifier weights.
- A norm-based origin statistic is direction-blind; the projected one is not.
- The projected statistic orders the damage across the five datasets (rho = -0.90).
- A signed damage law predicts the sign across classifier families."""

if old_h not in s:
    print("MISS highlights")
s = s.replace(old_h, new_h)
io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("abstract words:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
for b in re.findall(r"^- (.+)$", s.split("## Highlights")[1].split("## 1.")[0], re.M):
    print(len(b), b)
