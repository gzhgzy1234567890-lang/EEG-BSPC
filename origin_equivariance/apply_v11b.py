# -*- coding: utf-8 -*-
"""v11b: held-out results, bound caveat, split-sample CIs, invariances, ref [19]."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)
R = []

# ---------- 4.4 dataset level: six datasets ----------
R.append((
"""*Dataset level (n = 5).* Median z_w against median penalty gives a rank correlation of −0.90. With five observations the exact two-sided permutation distribution has 5! = 120 orderings and ten of them are at least this extreme, so the exact p is 0.083; a normal approximation gives 0.035, and we report the exact value as primary and the approximation as secondary, as the referee asked. The same analysis with z_T gives −0.80. This is the level at which the five datasets are independent observations; the result is suggestive and does not reach 0.05.""",
"""*Dataset level (n = 6, including the held-out dataset).* Median z_w against median penalty over the six datasets gives a rank correlation of −0.943. With six observations the exact two-sided permutation distribution has 6! = 720 orderings and twelve of them are at least this extreme, so the exact p is 0.017; over the five datasets used to develop the statistic the correlation was −0.90 with exact p = 0.083, and the normal approximation to that value is 0.035. The held-out dataset is what moves the result below 0.05, and it is the only dataset that played no part in choosing the statistic: SEED-IV has median z_w = 1.00 and median penalty −0.070, and it lands where the five-dataset relation predicts.

*Within the held-out dataset.* The statistic does not order the cells of SEED-IV (AUC 0.482 for a severe loss), which is consistent with what the five development datasets already showed: z_w ranks feature families and datasets, not cells or representations."""))

# ---------- 4.4 operating points ----------
R.append((
"""*Is the proxy useful as a screen?* We tested the decision it is meant to support: flag a cell whose one-sided penalty exceeds 0.05 in magnitude. Across the 845 cells (228 positives) z_w reaches an AUC of 0.839 and a precision-recall AUC of 0.648, with a cluster-bootstrap interval for the AUC of [0.733, 0.881]. Within single datasets it reaches 0.834 on BCI-2a, 0.847 on BCI-2b, 0.857 on grasp-and-lift and 0.693 on NER2015, and it *inverts* on SEED (0.332), where the feature family is uniform and only the subject pairs vary.""",
"""*Is the proxy useful as a screen?* We tested the decision it is meant to support: flag a cell whose one-sided penalty exceeds 0.05 in magnitude. Across the 845 development cells (228 positives) z_w reaches an AUC of 0.839 and a precision-recall AUC of 0.648, with a cluster-bootstrap interval of [0.733, 0.881]. Within single datasets it reaches 0.834 on BCI-2a, 0.847 on BCI-2b, 0.857 on grasp-and-lift and 0.693 on NER2015, and it *inverts* on SEED (0.332).

An AUC is not a screening rule, so we also report an operating point: a threshold chosen by maximising Youden's J on four datasets and applied to the fifth.

**Table 6b.** Leave-one-dataset-out operating point for the screen. The threshold is chosen on the four training datasets; sensitivity, specificity and precision are measured on the held-out one.

| held out | n | threshold | sensitivity | specificity | precision |
|---|---|---|---|---|---|
| BCI-2a | 36 | 0.354 | 0.714 | 0.864 | 0.769 |
| BCI-2b | 108 | 0.354 | 1.000 | 0.574 | 0.753 |
| SEED | 45 | 0.354 | 1.000 | 0.000 | 0.489 |
| NER2015 | 320 | 0.475 | 0.273 | 0.864 | 0.188 |
| grasp-and-lift | 336 | 0.369 | 0.704 | 0.828 | 0.627 |

The transferable operating point works on three of the five held-out datasets and fails on two: on SEED it flags everything (specificity 0.000), and on NER2015 it misses most of the severe cases (sensitivity 0.273, precision 0.188). A laboratory that used this rule would therefore be roughly right on three datasets and wrong on two, which is not yet a screening instrument."""))

# ---------- 4.5 bound caveat ----------
R.append((
"""Pooled over the 2,400 cells the predicted and observed changes have a mean absolute difference of 0.028 and a correlation of 0.825. The bound holds in every cell, as it must: the discrepancy that a reader might infer from comparing the median displacement with the median damage in an earlier version came from comparing medians of *different* quantities, not from a violation.""",
"""Pooled over the 2,400 cells the predicted and observed changes have a mean absolute difference of 0.028 and a correlation of 0.825.

**The bound applies to the model, not to the data.** The inequality |Δ| ≤ 0.1995|s| follows from the derivative of Equation (3), so it constrains the *predicted* change and holds for it in every cell by construction. The *observed* change is a step function of the sample scores: moving a threshold across a handful of trials moves balanced accuracy by a multiple of 1/n_c, and nothing in the Gaussian model prevents that step from being large. We therefore counted both. Over the 800 binary cells the prediction violates the bound in 0 of 800 cases, and the observation violates it in 185, i.e. 23.1 per cent, with a median ratio |Δ_obs|/|s| of 0.29 among the violations and a maximum of 4.1. The correct reading is that the model's own quantity obeys its own bound, while the empirical quantity is discrete and can jump; the correlation of 0.83 is the evidence for the model, not the bound."""))

# ---------- 4.5 split-sample CIs and SVM wording ----------
R.append((
"""In a split-sample test, with t* estimated on one half of the target and the sign evaluated on the other half, the AUC is 0.914 (2b, LDA), 0.846 (2b, logistic), 0.844 (2a, LDA), 0.877 (2a, logistic), 0.670 (grasp-and-lift, LDA) and 0.646 (grasp-and-lift, logistic), against 0.529, 0.846 and 0.503 for the SVM settings: the sign is genuinely discriminated for the mean-calibrated classifiers and at chance for the margin-based one.""",
"""In a split-sample test, with t* estimated on one half of the target and the sign evaluated on the other half, the sign-discrimination AUC is 0.914 [0.853, 0.958] (BCI-2b, LDA), 0.848 [0.767, 0.917] (BCI-2b, logistic), 0.848 [0.705, 0.955] (BCI-2a, LDA), 0.786 [0.618, 0.924] (BCI-2a, logistic), 0.667 [0.606, 0.725] (grasp-and-lift, LDA) and 0.662 [0.599, 0.721] (grasp-and-lift, logistic), with intervals from a bootstrap over cells. The support-vector machine is neither uniformly at chance nor uniformly above it: 0.571 [0.446, 0.689] on BCI-2b, 0.328 [0.160, 0.506] on BCI-2a and 0.478 [0.387, 0.570] on grasp-and-lift. We therefore describe it as unstable across settings rather than as at chance, and we do not claim the law for it."""))

# ---------- 4.10 invariance checks ----------
R.append((
"""Two checks that a reader reproducing this work will need.""",
"""**The two invariances of z_w.** We verified both numerically over 60 cells spanning three datasets: an offset added to every class score changes z_w by at most 1.4 × 10⁻¹⁴, and a feature translation in the null space of P W changes it by at most 2.5 × 10⁻¹³. The choice of scale convention matters: taking the standard deviations of the *centred* scores instead of the uncentred ones changes z_w by as much as 24, so Equation (2c) must be read with the uncentred convention, which is what the code implements.

**The held-out dataset.** SEED-IV was converted from the distributed features with the session labels in its ReadMe, cached per session, and evaluated with the models and thresholds fixed in earlier rounds. No parameter was tuned on it.

Two checks that a reader reproducing this work will need."""))
R.append(("[18] MOABB developers,",
          "[18] MOABB developers,"))

for a, b in R:
    if a not in s:
        print("MISS:", a[:60].replace("\n", " "))
    s = s.replace(a, b)

# reference [19]
s = s.replace("""https://github.com/NeuroTechX/moabb""",
              """https://github.com/NeuroTechX/moabb

[19] W.-L. Zheng, W. Liu, Y. Lu, B.-L. Lu, A. Cichocki, EmotionMeter: a multimodal framework for recognizing human emotions, IEEE Trans. Cybern. 49 (2019) 1110–1122.""", 1)

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
