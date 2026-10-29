# -*- coding: utf-8 -*-
"""Compare the numbers in the packaged manuscript against the local code outputs."""
import re
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

DOC = r"F:\data\BSPC_Enhanced_V2_Complete_Submission_Package\Manuscript\BSPC_Failure_Regimes_Enhanced_V2.docx"


def blocks(doc):
    out, cap = [], ""
    for child in doc.element.body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            t = Paragraph(child, doc).text.strip()
            if re.match(r"^Table (\d+)\.", t):
                cap = int(re.match(r"^Table (\d+)", t).group(1))
        elif tag == "tbl":
            t = Table(child, doc)
            rows = [[c.text.strip() for c in r.cells] for r in t.rows]
            out.append((cap, rows))
            cap = ""
    return out


def nums(row):
    out = []
    for x in row:
        m = re.findall(r"[−-]?\d+\.\d+", x.replace("−", "-"))
        out += [float(v) for v in m]
    return out


EXPECT = {
    5: {
        "BCI-2b": [0.7062, 0.7383, 0.7385, 0.7359, 0.7332, 0.030],
        "BCI-2a": [0.4970, 0.5291, 0.5261, 0.5258, 0.5291, 0.029],
        "SEED": [0.4594, 0.6730, 0.6736, 0.6706, 0.6747, 0.211],
        "grasp-and-lift": [0.7727, 0.6577, 0.6652, 0.6774, 0.7621, -0.095],
        "NER2015": [0.5916, 0.5873, 0.5873, 0.5888, 0.5898, -0.003],
    },
    14: {
        "a = 0, v = 0": [0.701, 0.699, 0.701, 0.701, 0.698],
        "a = 1, v = 0": [0.500, 0.699, 0.699, 0.693, 0.698],
        "a = 0, v = 1": [0.619, 0.675, 0.667, 0.672, 0.682],
        "a = 0, v = 2": [0.519, 0.617, 0.602, 0.611, 0.663],
        "a = 1, v = 2": [0.379, 0.617, 0.609, 0.607, 0.663],
        "steps every 8": [0.342, 0.440, 0.432, 0.430, 0.607],
        "class priors only": [0.704, 0.691, 0.697, 0.695, 0.690],
        "block priors": [0.706, 0.693, 0.698, 0.698, 0.688],
    },
    15: {"fixed λ = 0.25": 0.7584, "fixed λ = 0.50": 0.7318, "matched": 0.7617,
         "shuffled": 0.7622, "predictive": 0.7621, "variance-ratio": 0.6774},
    16: {
        "grasp-and-lift": [0.7727, 0.7674, 0.7584, 0.7318, 0.6997, 0.6652],
        "SEED": [0.4594, 0.4727, 0.4930, 0.5447, 0.6178, 0.6736],
        "BCI-2b": [0.7062, 0.7128, 0.7190, 0.7304, 0.7359, 0.7385],
        "BCI-2a": [0.4970, 0.5023, 0.5102, 0.5236, 0.5255, 0.5261],
        "NER2015": [0.5916, 0.5919, 0.5905, 0.5890, 0.5880, 0.5873],
    },
    17: {
        "grasp-and-lift": [5, 0.800, 0.255, 0.528, 0.65, 0.102],
        "SEED": [227, 0.063, 0.004, 0.059, 0.95, -0.181],
        "BCI-2b": [9, 0.104, 0.130, -0.017, -0.16, -0.020],
        "BCI-2a": [20, 0.120, 0.053, 0.067, 0.17, -0.024],
        "NER2015": [4, 0.213, 0.329, -0.096, -0.39, 0.000],
    },
}

doc = docx.Document(DOC)
tabs = blocks(doc)
print("tables found:", [(c, len(r)) for c, r in tabs])
bad = total = 0
for cap, rows in tabs:
    exp = EXPECT.get(cap)
    if not exp:
        continue
    for row in rows:
        key = None
        for k in exp:
            if row and row[0].startswith(k):
                key = k
                break
        if key is None:
            continue
        if cap == 15:
            got = nums(row)[-1:]
        elif cap == 17:
            got = nums(row)
        else:
            got = nums(row[1:])
        want = exp[key] if isinstance(exp[key], list) else [exp[key]]
        if len(got) < len(want):
            print("  short row", cap, key, got)
            continue
        got = got[:len(want)]
        for g, w in zip(got, want):
            total += 1
            if abs(g - w) > 0.0016:
                bad += 1
                print("  MISMATCH T%d %-16s got %.4f want %.4f" % (cap, key, g, w))
print("checked", total, "numbers; mismatches", bad)
