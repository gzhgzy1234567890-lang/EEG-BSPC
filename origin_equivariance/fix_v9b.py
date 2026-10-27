# -*- coding: utf-8 -*-
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
s = s.replace("We separate three questions that are often conflated.",
              "We separate three questions.")
s = s.replace("this family contains more than the sample mean, and we state the family rather than claiming uniqueness.",
              "this family contains more than the sample mean, and we do not claim uniqueness.")
s = s.replace("for a finite sample the condition is sufficient but not necessary.",
              "for a finite sample it is sufficient, not necessary.")
io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("abstract words:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
print("[1-3] cited:", "[1-3]" in s, " [5-8] cited:", "[5-8]" in s)
