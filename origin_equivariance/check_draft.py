# -*- coding: utf-8 -*-
import io
import re

s = io.open(r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md", encoding="utf-8").read()
ab = re.search(r"## Abstract\s*(.*?)\*\*Keywords", s, re.S).group(1)
w = re.findall(r"[A-Za-z][A-Za-z\-']*", ab)
print("abstract words:", len(w))
print("sections:", re.findall(r"^## (.+)$", s, re.M))
print("tables:", len(re.findall(r"^\*\*Table \d", s, re.M)),
      "figures:", len(re.findall(r"^\*\*Fig\. \d", s, re.M)))
refs = re.findall(r"^\[(\d+)\]", s.split("## References")[1], re.M)
body = s.split("## References")[0]
cited = set()
for m in re.finditer(r"\[([0-9,\-\s]+)\]", body):
    for part in m.group(1).replace("\u2013", "-").split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")[:2]
            try:
                for k in range(int(a), int(b) + 1):
                    cited.add(str(k))
            except Exception:
                pass
        elif part.isdigit():
            cited.add(part)
print("refs listed:", len(refs), "cited:", len(cited))
print("cited but not listed:", sorted(set(cited) - set(refs)))
print("listed but not cited:", sorted(set(refs) - cited))
