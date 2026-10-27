# -*- coding: utf-8 -*-
"""Round 4: per-subject calibration with intervals (referee minor item 1)."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)

old_tab = """| dataset | pipeline | BA | ECE | Brier | log loss |
|---|---|---|---|---|---|
| BCI-2b | none | 0.7018 | 0.1123 | 0.3842 | 0.5690 |
| BCI-2b | zero | 0.6038 | 0.3384 | 0.7224 | 4.7724 |
| BCI-2b | mean | 0.7365 | 0.0918 | 0.3437 | 0.5084 |
| SEED | none | 0.4591 | 0.5391 | 1.0781 | 14.8384 |
| SEED | zero | 0.3377 | 0.6677 | 1.3355 | 18.4447 |
| SEED | mean | 0.7094 | 0.2885 | 0.5769 | 7.8051 |
| grasp-and-lift | none | 0.7897 | 0.1783 | 0.3641 | 1.1935 |
| grasp-and-lift | zero | 0.7629 | 0.2076 | 0.4187 | 1.4418 |
| grasp-and-lift | mean | 0.7938 | 0.1736 | 0.3545 | 1.1277 |"""

new_tab = """| dataset | pipeline | BA | ECE (median per subject) | 95% CI of the mean | Brier | log loss |
|---|---|---|---|---|---|---|
| BCI-2b | none | 0.7018 | 0.1041 | [0.0822, 0.1418] | 0.3842 | 0.5690 |
| BCI-2b | zero | 0.6038 | 0.3557 | [0.3033, 0.3774] | 0.7224 | 4.7724 |
| BCI-2b | mean | 0.7365 | 0.0900 | [0.0710, 0.1075] | 0.3437 | 0.5084 |
| SEED | none | 0.4591 | 0.5467 | [0.5086, 0.5692] | 1.0781 | 14.8384 |
| SEED | zero | 0.3377 | 0.6716 | [0.6617, 0.6725] | 1.3355 | 18.4447 |
| SEED | mean | 0.7094 | 0.2404 | [0.2335, 0.3504] | 0.5769 | 7.8051 |
| grasp-and-lift | none | 0.7897 | 0.1484 | [0.1416, 0.2176] | 0.3641 | 1.1935 |
| grasp-and-lift | zero | 0.7629 | 0.1909 | [0.1791, 0.2391] | 0.4187 | 1.4418 |
| grasp-and-lift | mean | 0.7938 | 0.1466 | [0.1358, 0.2153] | 0.3545 | 1.1277 |"""

old_txt = """On BCI-2b the one-sided form raises expected calibration error from 0.112 to 0.338 and log loss from 0.569 to 4.772, and the two-sided pipeline returns calibration below its uncorrected value, 0.092 against 0.112. On SEED every pipeline is poorly calibrated because the features are not probabilities of anything, but the ordering is the same and the magnitude larger, 0.539 to 0.668 to 0.289. On grasp-and-lift the correction again leaves a small improvement, 0.174 against 0.178, consistent with a small z_T."""

new_txt = """The table reports, for each pipeline, the median of the per-subject expected calibration error and a bootstrap interval for its mean over subjects, so that the comparison is not carried by a pooled average over cells that are not independent. On BCI-2b the one-sided form raises the median expected calibration error from 0.104 to 0.356 and log loss from 0.569 to 4.772, with intervals that do not overlap; the two-sided pipeline returns 0.090 against 0.104, a difference whose intervals overlap and which we therefore do not claim as an improvement. On SEED every pipeline is poorly calibrated because the features are not probabilities of anything, but the ordering is the same and the magnitude larger, 0.547 to 0.672 to 0.240, again with non-overlapping intervals. On grasp-and-lift the differences are small and the intervals overlap, consistent with the small z_T of that dataset."""

for a, b in ((old_tab, new_tab), (old_txt, new_txt)):
    if a not in s:
        print("MISS:", a[:60].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
