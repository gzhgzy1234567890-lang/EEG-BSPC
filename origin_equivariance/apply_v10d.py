# -*- coding: utf-8 -*-
"""v10d: the Step 1 replacement (ASCII bars in the source)."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
old = """**Step 1 — project the source mean onto the classifier's direction.** z_w = ||P W μ_A||/(√K σ_s) requires nothing but the training session: the fitted weights, the source mean and the score spread. In our units, below z_w = 0.35 the penalty of the one-sided form is between +0.024 and −0.015; above z_w = 0.9 it is between −0.03 and −0.19. These ranges are descriptive of the eleven units studied, not validated thresholds: treat the statistic as a triage, not a test. Do not use the norm-based z_T for this purpose; Section 4.3 shows it is unchanged by a translation that can destroy the decoder."""
new = """**Step 1 — project the source mean onto the classifier's direction.** z_w = ||P W μ_A||/(√K σ_s) requires nothing but the training session: the fitted weights, the source mean and the score spread. In our units, below z_w = 0.35 the penalty of the one-sided form is between +0.024 and −0.015; above z_w = 0.9 it is between −0.03 and −0.19. Across all 845 cells the statistic separates a loss larger than 0.05 from the rest with an AUC of 0.84 (Section 4.4). These are descriptive operating characteristics of the eleven units studied, not validated thresholds: use the statistic to triage a feature family, not to certify that a particular representation is safe — the four BCI-2a representations have almost the same z_w and penalties that differ by 0.21. Do not use the norm-based z_T at all; Section 4.3 shows it is unchanged by a translation that can destroy the decoder."""
assert old in s
s = s.replace(old, new)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
