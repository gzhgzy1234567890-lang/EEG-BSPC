# -*- coding: utf-8 -*-
"""Structural check for a manuscript file given on the command line."""
import io
import re
import sys

P = sys.argv[1] if len(sys.argv) > 1 else r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
w = re.findall(r"[A-Za-z][A-Za-z\-']*", ab)
print("abstract words:", len(w))
refs = re.findall(r"^\[(\d+)\]", s.split("## References")[1], re.M)
body = s.split("## References")[0]
cited = set()
for m in re.finditer(r"\[([0-9,\-\s]+)\]", body):
    for part in m.group(1).split(","):
        part = part.strip()
        if part.isdigit():
            cited.add(part)
print("refs listed:", len(refs), "cited:", len(cited))
print("listed but not cited:", sorted(set(refs) - cited))
print("cited but not listed:", sorted(cited - set(refs)))
print("figures in body:", sorted(set(re.findall(r"Fig\. \d", body))))
print("tables in body:", sorted(set(re.findall(r"Table \d", body))))
print("headings:", [h for h in re.findall(r"^#{2,3} (.+)$", s, re.M)][:30])
