# Response to the reject report — v13 restructuring

The report is right on three substantive points, and the revision changes the
paper rather than defending it.

## 1. A binary model was used on four-class data

The per-cell analysis was always run on a *binary* subproblem for BCI-2a
(classes 1 and 2, left versus right hand); the manuscript never said so, and
Table 7 read as if it covered the four-class problem. Section 3 and the Table 7
caption now state that the 2a cells are the two-class subproblem and that the
four-class problem is not covered. No four-class claim remains anywhere.

## 2. The Gaussian parameterisation was inconsistent, and the check changes the claim

The report is correct that the law as printed uses a pooled score SD while the
equal-variance derivation needs the within-class SD, and that `c` cannot be
recovered from the aligned accuracy when the aligned threshold is displaced.
We recomputed the law the way the model requires — c = (m₁ − m₀)/(2σ_w) with
σ_w the within-class SD — and report both variants:

| dataset / classifier | old variant r, MAE | model variant r, MAE | |BA_aligned − Φ(c)| |
|---|---|---|---|
| BCI-2b / LDA | 0.989, 0.013 | 0.861, 0.057 | 0.096 |
| BCI-2b / logistic | 0.990, 0.013 | 0.852, 0.058 | 0.098 |
| BCI-2a / LDA | 0.902, 0.032 | 0.874, 0.041 | 0.149 |
| grasp-and-lift / LDA | 0.649, 0.036 | 0.271, 0.042 | 0.213 |
| NER2015 | 0.385, 0.029 | not estimable | — |

The model's own implied accuracy is 0.10–0.21 away from the observed aligned
accuracy, i.e. the equal-variance Gaussian assumption does not hold on these
scores. We also state the circularity the report implies: in the old variant `c`
is computed from BA_aligned and BA_aligned also enters the observed change, so
part of the high correlation is built in. The word "predictive law" is removed
from the abstract and the conclusion; the model is now presented as a
descriptive decomposition with a Gaussian interpretation, and its quantitative
form is reported honestly as weaker under its own assumptions.

## 3. The screen fails its external test, so it is no longer a headline claim

The external threshold test is in the paper: t = 0.354 fixed on the five
development datasets gives, on SEED-IV, sensitivity 1.000, specificity 0.000,
precision 0.544 — every cell flagged. The screen is now an exploratory section,
not a contribution; the title no longer promises a screen; the abstract says it
fails as an operational rule.

## 4. Novelty and the paper's identity

The report's central objection is that the theory is a corollary of affine
classification and the screen does not generalise. We accept the reframing it
recommends: the paper is now titled *Mean correction in cross-session EEG
decoding: equivariance, failure mechanism, and boundaries*, and Section 6.1
separates what is a corollary of linear discriminant theory (proved, not claimed
as discovery), what is an EEG-specific empirical regularity (which feature
families carry a free origin, how large the damage is, how it fails), and what
changes in practice (centre both sides, run the invariance test, do not use a
norm-based statistic). The detectability claim and the predictive-law claim are
gone.

## 5. Mechanical issues

- Equation numbering unified: one definition, Equation (2); the scalar form is
  restricted to K = 2.
- The duplicate Table 3 is gone: the scope statement is now a paragraph, so the
  levels table keeps its number.
- Fig. 2 caption now describes the two panels that exist, and the figure shows
  the held-out point.
- The "earlier version / earlier referee" language is removed throughout.
- The 80–97 per cent sign claim is gone; each number is given with its dataset,
  classifier and interval.
- Section 4.10 states explicitly that the centring of scores is across the class
  dimension (P), not across samples.

## What we have not done

A systematic audit of public pipelines, and validation on a feature family that
is independent of the four used here. We state both as open problems rather than
claiming them.
