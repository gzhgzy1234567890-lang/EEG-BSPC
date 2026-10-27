# Referee report, round 5 — BSPC submission v10

**Recommendation: Major Revision** (previous round: Major Revision). One
requirement keeps this from minor revision, and it is the same one as last
round: the screen has still not been tested outside the five datasets that
produced it.

## The two critical items

**MC1 (signed law).** Resolved, and the resolution is stronger than I expected.
The authors now compute the predicted and the observed change on the *same*
cell, which is what I asked for: 2,400 cells, pooled MAE 0.028, r = 0.825; for
LDA/logistic on BCI-2b, r = 0.989/0.990 with MAE 0.013; the analytic bound
|Δ| ≤ 0.1995|s| holds in every cell, and Fig. 4 is the scatter I requested. The
apparent inconsistency I flagged was indeed a comparison of medians of different
quantities, and the authors say so plainly. They also report where the law
fails (correlation 0.37–0.65 on two datasets, 0.35–0.61 for the SVM) instead of
averaging it away.

The majority-class point I raised was correct, and the authors concede it: raw
sign accuracy 0.869 against a baseline of 0.889 on BCI-2b. They then provide the
right statistic — a split-sample sign-discrimination AUC of 0.914, 0.846, 0.844
and 0.877 in four LDA/logistic settings and 0.50–0.53 for the SVM. That is a
genuine, honestly bounded claim.

**MC2 (z_w).** Resolved. The binary reduction is derived, it contains no ||w||,
and the closed form agrees with the implementation to 4 × 10⁻¹⁴. The definitions
of z_T, z_w, ρ and s are now collected in one place with their inputs. This was
a real inconsistency and it is gone.

## The other items

**MC3.** The exact permutation p (0.083, ten of 120 orderings) replaces the
asymptotic 0.035, and the paper now says the dataset-level result does not reach
0.05. Correct and appropriately modest.

**MC4.** Proposition 3 is restated as score-difference equivalence with label
equivalence as a corollary, and the degenerate-class case I constructed is
acknowledged. Sound.

**MC5.** The screening claim is now tested as a decision: AUC 0.839 [0.733,
0.881], PR-AUC 0.648, within-dataset 0.83–0.86 on three datasets, 0.69 on
NER2015, and 0.332 — inverted — on SEED. The BCI-2a representation anomaly is
reported as the clearest failure. The claim is narrowed to triage of a feature
family, which is what the evidence supports.

**MC6.** Addressed by the split-sample test and by reporting the majority
baseline. The response is candid about where the sign accuracy does not beat that
baseline.

**MC7, MC8 and the minors.** The transductive limitation is stated; the three
kinds of contribution are separated in Section 6.1 (corollary of linear
discriminant theory / EEG-specific empirical regularity / change in practice);
Equation (5) is corrected so that the h term drops out under the authors' own
constraint; the multiclass direction control is flagged as not run; the BCI-2b
pair-type levels are reported; the calibration comparison is now a paired
bootstrap.

## What remains

**External validation of the screen, and nothing else.** The authors have
not run a sixth dataset that played no role in choosing z_w; the
leave-one-dataset-out fit is compressed and they say so. With the screen now
narrowed to a triage of feature families, one held-out dataset with a different
feature family (SEED-IV, SEED-VII or Alljoined, all available to the authors)
would settle whether the ordering transfers. This is a finite, well-defined
experiment, and it is the difference between "consistent across our five" and
"replicated outside our five".

I would also like one more audited public pipeline, but I will not hold the
paper for it.

## Assessment

The manuscript has no remaining mathematical error that I can find, its claims
are now proportionate to its evidence, and two of its three contributions (the
characterization, the signed law) are solid. The third (the screen) is real but
local. If the authors add the held-out dataset and it behaves as the five do, I
expect to recommend minor revision; if it does not, the screening section should
be cut and the paper resubmitted as a characterization plus sign-law paper,
which would still be publishable here.
