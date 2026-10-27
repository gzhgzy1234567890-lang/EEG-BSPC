# -*- coding: utf-8 -*-
"""Round 3c: minor items 3 and 4 from the referee."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(P, encoding="utf-8").read()

old = """- The benefit of the correction is not screenable; the risk is."""
new = """- The correction can be applied to the K scores, not the D features."""
assert old in s
s = s.replace(old, new)

old2 = """**No streaming protocol of the kind used online.**"""
new2 = """**The decision-space form is proved for affine models only.** Section 4.6 verifies the corollary for LDA, logistic regression and a linear support-vector machine. For a non-linear model the same shift is an approximation whose accuracy we did not measure, and a reader who deploys a non-linear decoder should check it on their own data before relying on the K-number form.

**No streaming protocol of the kind used online.**"""
assert old2 in s
s = s.replace(old2, new2)

io.open(P, "w", encoding="utf-8").write(s)
print("ok")
