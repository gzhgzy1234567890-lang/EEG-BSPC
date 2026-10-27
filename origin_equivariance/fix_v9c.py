# -*- coding: utf-8 -*-
"""Add per-subject bootstrap intervals to the calibration table."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()

old = """| dataset | n | pipeline | BA | median ECE | Brier | log loss |
|---|---|---|---|---|---|---|
| BCI-2b | 108 | none | 0.7046 | 0.0989 | 0.3842 | 0.5690 |
| BCI-2b | 108 | zero | 0.5831 | 0.3468 | 0.7224 | 4.7724 |
| BCI-2b | 108 | mean | 0.7375 | 0.0987 | 0.3437 | 0.5084 |
| SEED | 45 | none | 0.4591 | 0.5467 | 1.0781 | 14.8384 |
| SEED | 45 | zero | 0.3377 | 0.6716 | 1.3355 | 18.4447 |
| SEED | 45 | mean | 0.7094 | 0.2404 | 0.5769 | 7.8051 |
| grasp-and-lift | 336 | none | 0.7770 | 0.1802 | 0.3641 | 1.1935 |
| grasp-and-lift | 336 | zero | 0.7484 | 0.2408 | 0.4187 | 1.4418 |
| grasp-and-lift | 336 | mean | 0.7815 | 0.1671 | 0.3545 | 1.1277 |"""

new = """| dataset | n | pipeline | BA | median ECE | 95% CI of the mean ECE | Brier | log loss |
|---|---|---|---|---|---|---|---|
| BCI-2b | 108 | none | 0.7046 | 0.0989 | [0.0786, 0.1330] | 0.3842 | 0.5690 |
| BCI-2b | 108 | zero | 0.5831 | 0.3468 | [0.3391, 0.3815] | 0.7224 | 4.7724 |
| BCI-2b | 108 | mean | 0.7375 | 0.0987 | [0.0710, 0.1086] | 0.3437 | 0.5084 |
| SEED | 45 | none | 0.4591 | 0.5467 | [0.5086, 0.5692] | 1.0781 | 14.8384 |
| SEED | 45 | zero | 0.3377 | 0.6716 | [0.6617, 0.6725] | 1.3355 | 18.4447 |
| SEED | 45 | mean | 0.7094 | 0.2404 | [0.2335, 0.3504] | 0.5769 | 7.8051 |
| grasp-and-lift | 336 | none | 0.7770 | 0.1802 | [0.1552, 0.2259] | 0.3641 | 1.1935 |
| grasp-and-lift | 336 | zero | 0.7484 | 0.2408 | [0.1941, 0.2476] | 0.4187 | 1.4418 |
| grasp-and-lift | 336 | mean | 0.7815 | 0.1671 | [0.1494, 0.2201] | 0.3545 | 1.1277 |"""

if old not in s:
    print("MISS table")
s = s.replace(old, new)
s = s.replace(
    "ECE uses ten equal-width bins and is averaged within subject before taking the median.",
    "ECE uses ten equal-width bins, is averaged within subject, and the interval is a bootstrap (5,000 resamples) over subjects of the mean; because the three pipelines are evaluated on the same subjects, the intervals should be read as descriptive and a paired test would be more efficient.")
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
