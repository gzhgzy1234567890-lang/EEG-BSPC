# STATISTICAL_ANALYSIS_PLAN.md

Frozen before any further analysis. Written after Phase A (A1-A5) and before Phase B.

## Unit of analysis

The subject. For BCI-2b a subject contributes three forward pairs; the three per-pair differences are averaged
first, and the subject value enters the test. No test treats trials, blocks or cells as independent subjects.

## Sampling, effect and interval

- Effect: subject-level mean of (balanced accuracy after correction - balanced accuracy before correction).
- Interval: percentile bootstrap over subjects, 10,000 resamples, seed 20261101, reported as the interval for the
  **mean**.
- Test: two-sided Wilcoxon signed-rank on the subject values, as the protocol names it.
- Robustness: exact two-sided sign test on the number of positive subjects.
- These three answer different questions (mean, ranked symmetry, median sign); disagreement between them is
  reported, never "resolved" by dropping one.

## Families

| family | endpoint | evidence class | Holm? |
|---|---|---|---|
| F1 | BCI-2b csp, causal, source-only EA | PROSPECTIVE-IN-EXPLORED-DATA | yes, within F1 |
| F2 | SEED DE past-only | BLOCKED for the causal raw pipeline | no corrected p reported |
| - | BCI-2a euc_ea and all secondary representations | EXPLORATORY | never corrected, never called confirmatory |
| - | Sleep-EDF, grasp-and-lift, telemetry | existing confirmatory results from earlier protocols | unchanged |

With F2 blocked, F1 contains a single test; its uncorrected p (0.039) is reported as such and **not** described
as family-corrected.

## Rules that cannot change after seeing results

- No endpoint moves between families.
- No secondary representation is promoted to a primary endpoint.
- No dataset that was already used in development is called an independent confirmation.
- Non-significant results stay in the paper with their intervals.

## Multiplicity across the paper

The paper reports many analyses. Only F1 is a pre-specified test; everything else is labelled EXPLORATORY or
CONFIRMATORY from an earlier protocol and is not combined into a single corrected family.

With one live test in the family, Holm is the identity and no adjusted p-value is reported; the 2b p of 0.039 is quoted as uncorrected and is never described as family-corrected.
