# -*- coding: utf-8 -*-
import io
import re

p = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace(
    "Any other correction makes the result depend on a convention the pipeline does not report, and five elaborations — projected, halved, low-ranked, standardised and label-fitted — do not improve on the mean correction.",
    "Any other correction makes the result depend on a convention the pipeline does not report; five elaborations, including one that uses target labels, do not improve on the mean correction.")
s = s.replace(
    "The benefit of the correction over doing nothing is not ordered by the same statistic, and we report that as a negative result.",
    "The benefit of the correction is not ordered by the same statistic (negative result).")
s = s.replace(
    "(BCI-IV-2a, 2b, SEED, NER2015, grasp-and-lift; 11 feature units; three classifier families)",
    "(BCI-IV-2a, 2b, SEED, NER2015, grasp-and-lift; 11 feature units)")
s = s.replace(
    "which on an imbalanced target is usually something else.",
    "which on an imbalanced target is usually not collapse.")
io.open(p, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("abstract words:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
