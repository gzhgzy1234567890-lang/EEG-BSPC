# -*- coding: utf-8 -*-
import io
import re

p = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace(
    "Removing a session mean is the standard first step in cross-session EEG decoding, and two operations circulate under that description",
    "Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description")
io.open(p, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("abstract words:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
