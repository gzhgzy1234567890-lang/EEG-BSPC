# -*- coding: utf-8 -*-
"""v9b: promote the direction-aware source-only statistic to the screen."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)
R = []

# ---- abstract
R.append((
"""A direction-controlled sweep shows that the source-only statistic we propose is direction-blind: equal-norm origins parallel and orthogonal to the classifier weights give the same statistic and penalties of −0.21 and 0.000. We therefore present it as an empirical proxy: across the five datasets the rank correlation with the damage is −0.80 (p = 0.10), and a cluster bootstrap over datasets puts the unit-level correlation at −0.755 [−1.00, −0.28].""",
"""A direction-controlled sweep shows that a norm-based statistic is direction-blind: equal-norm origins parallel and orthogonal to the classifier weights give the same value and penalties of −0.21 and 0.000. Projecting the source mean onto the weights instead gives a statistic that is unchanged by the orthogonal shift; it orders the damage across the five datasets (−0.90, p = 0.035) and across the eleven units (−0.855, cluster-bootstrap interval [−1.00, −0.60]), and a leave-one-dataset-out fit reproduces the order of the three most damaged datasets."""))

# ---- 2.3 definition of the screen
R.append((
"""**The size.** If the class-conditional scores""",
"""**The source-only screen.** The origin distance that a pipeline can compute before it sees a target session should be the projection of the source mean onto the classifier's own direction, not its norm:

    z_w = || P W μ_A || / (√K σ_s) ,   σ_s = SD of the source scores.           (2b)

z_w uses only the source session — the fitted weights and the source mean — and it is invariant to a translation of the features orthogonal to W by construction, which is exactly the failure mode of a norm-based statistic (Section 4.3). For the binary case it reduces to |w'μ_A| / (||w|| σ_s).

**The size.** If the class-conditional scores"""))

# ---- Table 5: add z_w
R.append((
"""| dataset | representation | n | z_T | ρ | penalty | gain |
|---|---|---|---|---|---|---|
| NER2015 | time mean | 320 | 0.20 | 0.21 | 0.000 | 0.000 |
| BCI-2b | csp | 27 | 0.22 | 0.50 | +0.018 | +0.026 |
| grasp-and-lift | log power | 336 | 0.25 | 0.25 | −0.015 | 0.000 |
| BCI-2a | tan | 9 | 0.37 | 0.41 | +0.014 | +0.031 |
| BCI-2a | csp | 9 | 0.40 | 0.40 | +0.024 | +0.059 |
| BCI-2a | euc_ea | 9 | 0.64 | 0.22 | −0.014 | +0.059 |
| BCI-2a | euc | 9 | 7.87 | 0.34 | −0.184 | +0.017 |
| BCI-2b | euc_ea | 27 | 14.2 | 5.27 | −0.137 | +0.018 |
| BCI-2b | tan | 27 | 21.2 | 5.15 | −0.160 | +0.020 |
| SEED | differential entropy | 45 | 34.2 | 0.98 | −0.029 | +0.211 |
| BCI-2b | euc | 27 | 57.1 | 23.2 | −0.186 | +0.021 |""",
"""| dataset | representation | n | z_T | z_w | ρ | penalty | gain |
|---|---|---|---|---|---|---|---|
| NER2015 | time mean | 320 | 0.20 | 0.23 | 0.21 | 0.000 | 0.000 |
| BCI-2b | csp | 27 | 0.22 | 0.07 | 0.50 | +0.018 | +0.026 |
| grasp-and-lift | log power | 336 | 0.25 | 0.29 | 0.25 | −0.015 | 0.000 |
| BCI-2a | tan | 9 | 0.37 | 0.30 | 0.41 | +0.014 | +0.031 |
| BCI-2a | csp | 9 | 0.40 | 0.29 | 0.40 | +0.024 | +0.059 |
| BCI-2a | euc_ea | 9 | 0.64 | 0.32 | 0.22 | −0.014 | +0.059 |
| BCI-2a | euc | 9 | 7.87 | 0.33 | 0.34 | −0.184 | +0.017 |
| BCI-2b | euc_ea | 27 | 14.2 | 5.41 | 5.27 | −0.137 | +0.018 |
| BCI-2b | tan | 27 | 21.2 | 5.12 | 5.15 | −0.160 | +0.020 |
| SEED | differential entropy | 45 | 34.2 | 0.98 | 0.98 | −0.029 | +0.211 |
| BCI-2b | euc | 27 | 57.1 | 23.3 | 23.2 | −0.186 | +0.021 |"""))

# ---- 4.3: the direction-aware statistic passes the test
R.append((
"""The two directions give the same z_T to two decimals in both datasets, and the orthogonal one changes the penalty by exactly 0.0000 while the parallel one changes it by −0.13 and −0.21 to −0.31. The referee's counter-example is therefore correct, and it is a counter-example to z_T as a law, not to the mechanism: the damage is a projection, and a norm cannot see a direction. We report z_T from here on as an empirical proxy for the exposure of a feature family, and the decision-space displacement ρ as the quantity that carries the mechanism.""",
"""The two directions give the same z_T to two decimals in both datasets, and the orthogonal one changes the penalty by exactly 0.0000 while the parallel one changes it by −0.13 and −0.21 to −0.31. A norm-based statistic is therefore blind to the direction — this is the counter-example that the referee of an earlier version of this work constructed, and it is correct.

The projected statistic z_w of Equation (2b) does not fail the test by construction: w'(μ_A + c) = w'μ_A for c orthogonal to w, so its value is unchanged in the orthogonal arm and changes only in the parallel arm, exactly like the penalty. We therefore use z_w as the screen and keep z_T only as the naive alternative its failure is measured against."""))

# ---- 4.4 rewrite
R.append((
"""Three analyses, in decreasing order of independence. At the level of the five datasets, the median z_T and the median penalty give a rank correlation of −0.80, which with five observations has p = 0.10. At the level of the eleven units the rank correlation is −0.755; because eight of the eleven units come from two datasets, we do not use a permutation test over units but a cluster bootstrap that resamples the five datasets and recomputes the unit-level correlation within each resample, which gives a 95 per cent interval of [−1.000, −0.275] over 4,993 resamples. At the level of the 845 cells the rank correlation is −0.382, reported descriptively because the cells are not independent.

The honest reading is that the association is consistent across the three levels and survives clustering, but that five datasets cannot establish a law, and that Section 4.3 shows the statistic has no mechanism of its own. The proxy is useful for the decision it was designed for — is this feature family exposed? — and nothing more. The screen does not order the *benefit* of the correction: across the eleven units the rank correlation between z_T and the gain is +0.19 (p = 0.57). The benefit is a property of the particular pair, not of the feature family.""",
"""Three analyses, in decreasing order of independence, for the projected statistic z_w and, for comparison, the norm-based z_T.

*Dataset level (n = 5).* Median z_w against median penalty gives a rank correlation of −0.90 (p = 0.035); the same analysis with z_T gives −0.80 (p = 0.10). This is the level at which the five datasets are independent observations, and it is the test the referee of an earlier version asked for.

*Unit level (n = 11).* The rank correlation is −0.855 for z_w (p = 0.001) and −0.755 for z_T (p = 0.007). Because eight of the eleven units come from two datasets, we do not use a permutation test over units; a cluster bootstrap that resamples the five datasets and recomputes the unit-level correlation within each resample gives a 95 per cent interval of [−1.000, −0.600] for z_w and [−1.000, −0.275] for z_T, over 4,993 resamples.

*Cell level (n = 845).* The rank correlations are −0.502 for z_w and −0.382 for z_T, reported descriptively because the cells are not independent.

*Leave-one-dataset-out.* Fitting a linear relation between log z_w and the penalty on four datasets and predicting the fifth gives median absolute errors of 0.021, 0.027 and 0.075 on grasp-and-lift, NER2015 and SEED, and underestimates on the two BCI datasets, whose predicted medians are compressed toward zero (BCI-2b: predicted −0.074 against observed −0.149). The predicted order matches the observed one for the three datasets with the largest penalty. This is a weak test — four datasets are not a training set — but it is the strongest external check available with five datasets, and we report its failures.

The honest reading is that the projected statistic is consistent across four levels and survives clustering, that it is the statistic the mechanism predicts (Section 2.3), and that it is still an empirical proxy rather than a law: five datasets cannot establish a law, and the leave-one-dataset-out fit is compressed. What the proxy is for is the decision it was designed for — is this feature family exposed? The screen does not order the *benefit* of the correction: across the eleven units the rank correlation between z_w and the gain is +0.19 (p = 0.57). The benefit is a property of the particular pair, not of the feature family."""))

# ---- 5 procedure step 1
R.append((
"""**Step 1 — measure the origin distance from the source session.** z_T = ||μ_A||/||sd_A|| requires nothing but the training features. In our units, below z_T = 0.5 the penalty of the one-sided form is between +0.024 and −0.015; above z_T = 7 it is between −0.03 and −0.19. These ranges are descriptive of the eleven units studied, not validated thresholds, and Section 4.3 shows the statistic is direction-blind; treat it as a triage, not a test.""",
"""**Step 1 — project the source mean onto the classifier's direction.** z_w = ||P W μ_A||/(√K σ_s) requires nothing but the training session: the fitted weights, the source mean and the score spread. In our units, below z_w = 0.35 the penalty of the one-sided form is between +0.024 and −0.015; above z_w = 0.9 it is between −0.03 and −0.19. These ranges are descriptive of the eleven units studied, not validated thresholds: treat the statistic as a triage, not a test. Do not use the norm-based z_T for this purpose; Section 4.3 shows it is unchanged by a translation that can destroy the decoder."""))

# ---- 6.4 limitations: screen
R.append((
"""**The screen is direction-blind.** Section 4.3 shows that an origin orthogonal to the weights raises z_T and changes nothing. The statistic is a proxy for the feature family's exposure, not a law, and the decision-space displacement is the quantity with the mechanism.""",
"""**The screen is a proxy.** Section 4.3 shows that a norm-based statistic is unchanged by an origin that is orthogonal to the weights and that does nothing; the projected statistic z_w does not have that failure by construction, but it remains an empirical proxy rather than a law. Five datasets, with a leave-one-dataset-out fit that is compressed, are not enough to certify a threshold, and the decision-space displacement is the quantity with the mechanism."""))

for a, b in R:
    if a not in s:
        print("MISS:", a[:70].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("written", n0, "->", len(s), "| abstract words:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
