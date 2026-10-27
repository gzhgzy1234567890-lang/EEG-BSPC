# -*- coding: utf-8 -*-
"""Round 4b: figure legend fix + insert image links for the docx build."""
import io
import re
import os

MD = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(MD, encoding="utf-8").read()

# 1. image links immediately before each caption
for n, f in ((1, "figs/fig1.png"), (2, "figs/fig2.png"), (3, "figs/fig3.png")):
    tag = "**Fig. %d.**" % n
    if tag in s and ("](%s)" % f) not in s:
        s = s.replace(tag, "![Figure %d](%s)\n%s" % (n, f, tag), 1)

# 2. a captions section at the end, which the docx builder expects
if "## Figure captions" not in s:
    caps = []
    for n in (1, 2, 3):
        m = re.search(r"\*\*Fig\. %d\.\*\* (.*?)(?=\n\n|\n\*\*|\Z)" % n, s, re.S)
        if m:
            caps.append("**Fig. %d.** %s" % (n, m.group(1).strip()))
    s = s.rstrip() + "\n\n## Figure captions\n\n" + "\n\n".join(caps) + "\n"

io.open(MD, "w", encoding="utf-8").write(s)
print("md patched; image links:", s.count("](figs/fig"), "captions section:", "## Figure captions" in s)
