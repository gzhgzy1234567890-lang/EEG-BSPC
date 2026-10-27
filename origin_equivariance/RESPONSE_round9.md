# Response to the round-9 report — the counter-example is correct, and it costs the paper its screen

## 1. `z_w` was not invariant to decision-equivalent score representations

The counter-example is correct. Adding a class-common linear term a'x to every
score leaves every prediction unchanged and changes the raw per-class score
spreads; with W = [1; −1] and a'x = 0.5x the statistic goes from 1.00 to 1.49 on
an identical decision function. The definition was wrong.

**Fix.** The scale must be taken from the *centred* scores,
σ_k = sd of column k of P S. Then P(W + 1a') = PW and P(S + a'x) = P S, so both
numerator and scale are invariant. We verified the invariance under the
referee's transformation: |Δz_w| = 4.4 × 10⁻¹⁶ (Section 4.10, `results/zw_centred.txt`).

**Consequence — the screening claim does not survive.** Every number the screen
rested on was recomputed with the corrected definition:

| quantity | old (uncentred σ) | corrected (centred σ) |
|---|---|---|
| five-dataset Spearman | −0.90 | **−0.80** |
| six-dataset Spearman | −0.94 | **−0.77** |
| six-dataset exact permutation p | 0.017 | **0.103** |
| SEED-IV median z_w | 1.00 | **24.4** |
| SEED-IV operating point | sens 1.000, spec 0.000 | unchanged (spec 0.000) |

The association is no longer significant once the statistic is well defined.
We therefore **removed risk screening from the abstract, the title and the
contributions**, and Section 4.4 now reports the corrected numbers and says that
the statistic is not a screening tool. The paper's claims are the
characterization, the failure mechanism and the boundaries.

## 2. The Gaussian model

- The oracle-assisted parameterisation and the model-required parameterisation
  are now reported side by side (r 0.989 vs 0.861 on BCI-2b; 0.649 vs 0.271 on
  grasp-and-lift; not estimable on NER2015).
- The circularity is stated: in the oracle variant c is computed from
  BA_aligned, which also enters the observed change.
- The "80–97 per cent" sentence was removed from the introduction; each figure is
  now given with its dataset and classifier.
- The model's implied accuracy differs from the observed aligned accuracy by
  0.10–0.21, which is reported as evidence that the equal-variance assumption
  fails on these scores.
- The word "predictive law" is gone from the abstract and the conclusion.

## 3. Origin sweep

The referee is right that a common translation cancelling in a linear model with
an intercept is algebra, and that `none` is also equivariant. The sweep is now
presented as an implementation check and as the calibration of the mechanism,
not as independent EEG evidence; the EEG-specific evidence is the distribution of
z_T across feature families and the failure of the one-sided form on real
sessions (Section 1 and Section 4.2 are phrased accordingly).

## 4. Statistics and units

- 845 cells are now described as dataset–representation–subject–session-pair
  cells, and the number of distinct session pairs is given (737: 9 + 27 + 45 +
  320 + 336).
- Subject-level aggregation and the cluster bootstrap over datasets are stated
  where they are used; the cell-level numbers are labelled descriptive.
- A direction table is added to Section 3 (which pairs, in which direction, and
  why).

## 5. Mechanics

- Equation (6) is now stated with non-strict inequalities and a tie-breaking
  rule.
- The unit test is described as a test with a specified translation vector and
  tolerance, and with the caveat that a translation in the null space of PW, or
  a sample that does not cross the boundary, will not trigger it.
- The direction-blind sentence in the Introduction now refers to z_T, not to the
  proposed statistic.
- Figure numbering follows first citation.
- "drives the one-sided pipeline to exact chance" is qualified per dataset.
- Table 4's 0.49/0.50 discrepancy is corrected in the text.
- Section 4.7 reports paired differences rather than two marginal intervals.
- Section 6.4 states what "held out" means for SEED-IV (not used for any choice;
  same feature family as SEED).
- The "earlier version / referee" language is removed.

## What is still open

Tables 5 and 6 still carry the old (uncentred) per-unit values and must be
regenerated with the corrected definition; the manuscript says so explicitly in
the table notes until they are. A systematic audit of public pipelines remains
undone and is stated as an open problem.
