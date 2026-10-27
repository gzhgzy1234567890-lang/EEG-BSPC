# -*- coding: utf-8 -*-
"""v10b: results sections — exact p, screening, per-cell law, paired calibration."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)
R = []

# ---------- 4.4 dataset level + screening ----------
R.append((
"""*Dataset level (n = 5).* Median z_w against median penalty gives a rank correlation of −0.90 (p = 0.035); the same analysis with z_T gives −0.80 (p = 0.10). This is the level at which the five datasets are independent observations, and it is the test the referee of an earlier version asked for.""",
"""*Dataset level (n = 5).* Median z_w against median penalty gives a rank correlation of −0.90. With five observations the exact two-sided permutation distribution has 5! = 120 orderings and ten of them are at least this extreme, so the exact p is 0.083; a normal approximation gives 0.035, and we report the exact value as primary and the approximation as secondary, as the referee asked. The same analysis with z_T gives −0.80. This is the level at which the five datasets are independent observations; the result is suggestive and does not reach 0.05."""))

R.append((
"""The honest reading is that the projected statistic is consistent across four levels and survives clustering, that it is the statistic the mechanism predicts (Section 2.3), and that it is still an empirical proxy rather than a law: five datasets cannot establish a law, and the leave-one-dataset-out fit is compressed. What the proxy is for is the decision it was designed for — is this feature family exposed? The screen does not order the *benefit* of the correction: across the eleven units the rank correlation between z_w and the gain is +0.19 (p = 0.57). The benefit is a property of the particular pair, not of the feature family.""",
"""*Is the proxy useful as a screen?* We tested the decision it is meant to support: flag a cell whose one-sided penalty exceeds 0.05 in magnitude. Across the 845 cells (228 positives) z_w reaches an AUC of 0.839 and a precision-recall AUC of 0.648, with a cluster-bootstrap interval for the AUC of [0.733, 0.881]. Within single datasets it reaches 0.834 on BCI-2a, 0.847 on BCI-2b, 0.857 on grasp-and-lift and 0.693 on NER2015, and it *inverts* on SEED (0.332), where the feature family is uniform and only the subject pairs vary.

The honest reading is therefore narrower than "the screen works". The statistic ranks feature families and datasets reliably, separates a severe loss with an AUC around 0.84, and survives a cluster bootstrap; it fails in two specific ways that we report rather than hide. Within BCI-2a the four representations have almost the same z_w (0.285 to 0.325) and penalties from +0.024 to −0.184, so the statistic cannot resolve which representation of a given dataset is exposed — the case that would matter most in practice. And within SEED its ordering is inverted. Five datasets cannot establish a law, the leave-one-dataset-out fit is compressed, and the screen does not order the *benefit* of the correction (rank correlation +0.19, p = 0.57)."""))

# ---------- 4.5 per-cell law ----------
R.append((
"""**Table 6.** Sign prediction from Equation (4). t* and s are in units of the source score SD; `sign ok` is the fraction of cells whose damage sign is predicted correctly.""",
"""**Table 6.** Per-cell prediction of Equation (4). `MAE` is the mean absolute difference between the predicted and the observed change on the *same* cell; `r` is Pearson; `sign` is the fraction of cells whose sign is predicted, `base` the majority-class rate on the same cells, and `bound` the fraction of cells satisfying the analytic bound |Δ| ≤ 0.1995|s| that follows from the derivative of Equation (3)."""))

R.append((
"""| dataset | classifier | n | median t* | median s | median damage | sign ok |
|---|---|---|---|---|---|---|
| BCI-2b | LDA | 60 | +0.019 | −0.110 | −0.1327 | 0.97 |
| BCI-2b | logistic | 60 | −0.010 | −0.098 | −0.1308 | 0.93 |
| BCI-2b | SVM | 60 | +0.059 | +0.016 | +0.0061 | 0.83 |
| BCI-2a | LDA | 36 | −0.070 | −0.161 | −0.0658 | 0.92 |
| BCI-2a | logistic | 36 | −0.031 | −0.242 | −0.0691 | 0.89 |
| BCI-2a | SVM | 36 | −0.081 | −0.138 | −0.0145 | 0.83 |
| grasp-and-lift | LDA | 60 | −0.042 | −0.275 | −0.0309 | 0.90 |
| grasp-and-lift | logistic | 60 | −0.053 | −0.232 | −0.0291 | 0.80 |
| grasp-and-lift | SVM | 60 | −0.085 | −0.019 | +0.0040 | 0.83 |""",
"""| dataset | classifier | n | MAE | r | sign | base | bound |
|---|---|---|---|---|---|---|---|
| BCI-2b | LDA | 108 | 0.0130 | 0.989 | 0.917 | 0.815 | 1.00 |
| BCI-2b | logistic | 108 | 0.0127 | 0.990 | 0.889 | 0.769 | 1.00 |
| BCI-2b | SVM | 108 | 0.0224 | 0.381 | 0.676 | 0.528 | 1.00 |
| BCI-2a | LDA | 36 | 0.0320 | 0.902 | 0.889 | 0.833 | 1.00 |
| BCI-2a | logistic | 36 | 0.0330 | 0.885 | 0.750 | 0.750 | 1.00 |
| BCI-2a | SVM | 36 | 0.0161 | 0.610 | 0.611 | 0.528 | 1.00 |
| grasp-and-lift | LDA | 336 | 0.0360 | 0.649 | 0.693 | 0.604 | 1.00 |
| grasp-and-lift | logistic | 336 | 0.0364 | 0.592 | 0.649 | 0.607 | 1.00 |
| grasp-and-lift | SVM | 336 | 0.0115 | 0.353 | 0.420 | 0.292 | 1.00 |
| NER2015 | LDA | 320 | 0.0285 | 0.385 | 0.556 | 0.406 | 1.00 |
| NER2015 | logistic | 320 | 0.0258 | 0.371 | 0.509 | 0.425 | 1.00 |
| NER2015 | SVM | 320 | 0.0434 | 0.458 | 0.666 | 0.503 | 1.00 |

Pooled over the 2,400 cells the predicted and observed changes have a mean absolute difference of 0.028 and a correlation of 0.825. The bound holds in every cell, as it must: the discrepancy that a reader might infer from comparing the median displacement with the median damage in an earlier version came from comparing medians of *different* quantities, not from a violation."""))
R.append((
"""The sign is predicted in 80–97 per cent of cells in all nine settings, including the four in which the median damage is positive. The classifier family is not the variable: t* is.""",
"""The law is quantitative where its Gaussian approximation is defensible — LDA and logistic regression on the two BCI datasets, with per-cell correlations of 0.89 to 0.99 and a mean absolute error of 0.013 to 0.033 — and it degrades to a sign-level account on grasp-and-lift and NER2015 (correlations 0.37 to 0.65) and for the support-vector machine (0.35 to 0.61). Its raw sign accuracy sits at or slightly above the majority-class rate, which is the reason we report the sign-discrimination AUC instead. In a split-sample test, with t* estimated on one half of the target and the sign evaluated on the other half, the AUC is 0.914 (2b, LDA), 0.846 (2b, logistic), 0.844 (2a, LDA), 0.877 (2a, logistic), 0.670 (grasp-and-lift, LDA) and 0.646 (grasp-and-lift, logistic), against 0.529, 0.846 and 0.503 for the SVM settings: the sign is genuinely discriminated for the mean-calibrated classifiers and at chance for the margin-based one.

The classifier family is not the variable: t* is."""))

# ---------- 4.7 paired calibration ----------
R.append((
"""The one-sided pipeline raises the expected calibration error sharply on the two datasets with an origin offset (0.099 to 0.347 on 2b, 0.547 to 0.672 on SEED) and moderately on the third (0.180 to 0.241). The two-sided pipeline returns calibration at or slightly below the uncorrected level: 0.0987 against 0.0989 on 2b, which is a tie, 0.240 against 0.547 on SEED, and 0.167 against 0.180 on grasp-and-lift. We therefore claim no calibration *improvement* from the correction on BCI-2b; what the correction does is restore the calibration that the one-sided pipeline destroys.""",
"""Because the pipelines are evaluated on the same subjects, we also report the paired difference per subject. The one-sided minus uncorrected difference is +0.254 [+0.229, +0.282] on BCI-2b, +0.129 [+0.098, +0.160] on SEED and +0.030 [+0.013, +0.047] on grasp-and-lift: the one-sided pipeline is worse on all three. The two-sided minus uncorrected difference is −0.014 [−0.036, +0.006] on BCI-2b, which is a tie, −0.251 [−0.296, −0.205] on SEED and −0.006 [−0.010, −0.002] on grasp-and-lift. We therefore claim no calibration *improvement* from the correction on BCI-2b; what the correction does there is restore the calibration that the one-sided pipeline destroys, and on SEED it improves on doing nothing."""))

for a, b in R:
    if a not in s:
        print("MISS:", a[:60].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
