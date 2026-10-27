# -*- coding: utf-8 -*-
"""v15: one definition, one set of numbers, no revision history."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)

# ---- 1. remove the contradicting uncentred-scale sentence and the meta prefix
s = s.replace("*The scale must come from the centred scores.* The first version of this analysis took σ_k from the raw score columns, and a referee's counter-example shows why that is wrong:",
              "*The scale comes from the centred scores.* Taking σ_k from the raw score columns is not admissible:")
s = s.replace(" We verified the invariance numerically under that transformation: |Δz_w| = 4.4 × 10⁻¹⁶ (Section 4.10). Every number in Section 4.4 uses this definition.",
              " We verified the invariance numerically under that transformation: |Δz_w| = 4.4 × 10⁻¹⁶ (Section 4.10). Every number in Section 4.4 uses this definition; the code computes σ_k from the centred scores.")

# ---- 2. stale numbers
s = s.replace("rho = -0.94", "rho = -0.77")
s = s.replace("rho = −0.94", "rho = −0.77")
s = s.replace("exact p = 0.017", "exact p = 0.103")
s = s.replace("p = 0.017", "p = 0.103")
s = s.replace("AUC 0.482", "AUC 0.515")
s = s.replace("(AUC 0.332)", "(AUC 0.332)")
s = s.replace("median z_w = 1.00", "median z_w = 24.4")
s = s.replace("z_w = 1.00, penalty −0.070", "z_w = 24.4, penalty −0.070")
s = s.replace("sits at 1.00", "sits at 24.4")
s = s.replace("SEED-IV's z_w sits at 1.00", "SEED-IV's z_w sits at 24.4")
s = s.replace("its within-SEED-IV ordering is inverted (AUC 0.332)", "its within-SEED ordering is inverted (AUC 0.332)")

# ---- 3. table 5 with the corrected definition
old_rows = [
 "| NER2015 | time mean | 320 | 0.20 | 0.23 | 0.21 | 0.000 | 0.000 |",
 "| BCI-2b | csp | 27 | 0.22 | 0.07 | 0.50 | +0.018 | +0.026 |",
 "| grasp-and-lift | log power | 336 | 0.25 | 0.29 | 0.25 | −0.015 | 0.000 |",
 "| BCI-2a | tan | 9 | 0.37 | 0.30 | 0.41 | +0.014 | +0.031 |",
 "| BCI-2a | csp | 9 | 0.40 | 0.29 | 0.40 | +0.024 | +0.059 |",
 "| BCI-2a | euc_ea | 9 | 0.64 | 0.32 | 0.22 | −0.014 | +0.059 |",
 "| BCI-2a | euc | 9 | 7.87 | 0.33 | 0.34 | −0.184 | +0.017 |",
 "| BCI-2b | euc_ea | 27 | 14.2 | 5.41 | 5.27 | −0.137 | +0.018 |",
 "| BCI-2b | tan | 27 | 21.2 | 5.12 | 5.15 | −0.160 | +0.020 |",
 "| SEED | differential entropy | 45 | 34.2 | 0.98 | 0.98 | −0.029 | +0.211 |",
 "| BCI-2b | euc | 27 | 57.1 | 23.3 | 23.2 | −0.186 | +0.021 |",
]
new_rows = [
 "| BCI-2b | csp | 27 | 0.22 | 0.068 | +0.018 | +0.026 |",
 "| NER2015 | time mean | 320 | 0.20 | 0.230 | 0.000 | 0.000 |",
 "| grasp-and-lift | log power | 336 | 0.25 | 0.289 | −0.015 | 0.000 |",
 "| BCI-2a | csp | 9 | 0.40 | 0.287 | +0.024 | +0.059 |",
 "| BCI-2a | tan | 9 | 0.37 | 0.309 | +0.014 | +0.031 |",
 "| BCI-2a | euc_ea | 9 | 0.64 | 0.597 | −0.014 | +0.059 |",
 "| BCI-2a | euc | 9 | 7.87 | 4.399 | −0.184 | +0.017 |",
 "| BCI-2b | tan | 27 | 21.2 | 5.117 | −0.160 | +0.020 |",
 "| BCI-2b | euc_ea | 27 | 14.2 | 5.405 | −0.137 | +0.018 |",
 "| SEED | differential entropy | 45 | 34.2 | 12.36 | −0.029 | +0.211 |",
 "| BCI-2b | euc | 27 | 57.1 | 23.31 | −0.186 | +0.021 |",
]
for a in old_rows:
    if a not in s:
        print("MISS row:", a[:40])
    s = s.replace(a, "")
s = s.replace("**Table 5.** The screen at the level of dataset-by-representation units, medians within a unit. z_T is the origin distance ‖μ_A‖/‖sd_A‖ of the source session; z_w is the displacement of Equation (2); penalty = zero − none; gain = mean − none. Sorted by z_T.",
              "**Table 5.** The source-only statistic at the level of dataset-by-representation units, medians within a unit. z_T is the origin distance ‖μ_A‖/‖sd_A‖; z_w is Equation (2) with the scale taken from the centred scores; penalty = zero − none; gain = mean − none. Sorted by z_w.")
header_old = "| dataset | representation | n | z_T | z_w | ρ | penalty | gain |\n|---|---|---|---|---|---|---|---|"
header_new = "| dataset | representation | n | z_T | z_w | penalty | gain |\n|---|---|---|---|---|---|---|"
if header_old not in s:
    print("MISS header")
s = s.replace(header_old, header_new)
anchor = "| BCI-2b | euc | 27 | 57.1 | 23.31 | −0.186 | +0.021 |"
if anchor not in s:
    print("MISS anchor") 
s = s.replace("| dataset | representation | n | z_T | z_w | penalty | gain |\n|---|---|---|---|---|---|---|\n",
              "| dataset | representation | n | z_T | z_w | penalty | gain |\n|---|---|---|---|---|---|---|\n" + "\n".join(new_rows) + "\n")

# ---- 4. meta-language
for a, b in [
    ("Two comments, because earlier versions of this work got them wrong.", "Two comments."),
    ("Standardisation with training statistics is a related but different operation, and earlier versions of this work conflated them.", "Standardisation with training statistics is a related but different operation."),
    ("The paper's claim is about a *mechanism* and an *exploratory* screen, and it is worth saying so in one place because the title of an earlier version promised a detector.", "The paper's claim is about a mechanism and its boundaries, and it is worth saying so in one place."),
]:
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
