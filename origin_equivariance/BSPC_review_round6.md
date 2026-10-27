# Referee report, round 6 — BSPC submission v11

**Recommendation: Minor revision.**

The three issues that kept the previous version at major revision are now
closed, and one of them — external validation — is closed with a real
experiment rather than an argument.

## The three items from the last report

**The theoretical bound is now applied to the right quantity.** The authors
counted both violation rates: 0 of 800 for the model's own prediction (which is
what the bound constrains) and 185 of 800, 23.1 per cent, for the observed
change, with a median ratio of 0.29 and a maximum of 4.1 among the violations.
The text now says that empirical balanced accuracy is a step function and that
the correlation, not the bound, is the evidence for the model. This is exactly
the distinction I asked for, and the paper is more honest for it.

**`z_w` now has a matrix definition with the invariance proved and checked.**
Equation (2c) defines the statistic through D_σ⁻¹, the authors state that the
uncentred convention is used and that the centred one would differ (by up to
24, which we verified in their Section 4.10), and both invariances are checked
numerically to 10⁻¹⁴ and 10⁻¹³. The binary reduction is derived rather than
asserted. The multiclass ambiguity I raised is gone.

**Generalization is now tested on a held-out dataset.** SEED-IV, which the
authors state was opened only after the statistic was fixed, gives a sixth
dataset point at median z_w = 1.00 and median penalty −0.070. The six-dataset
rank correlation is −0.943 with an exact permutation p of 12/720 = 0.017, and
the five-dataset value (p = 0.083) is still reported beside it. The authors also
report that within SEED-IV the statistic has an AUC of 0.482, that it cannot
separate the four BCI-2a representations, and that a leave-one-dataset-out
operating point fails on SEED and NER2015. This is the right way to report a
validation: the prediction that was made in advance is confirmed at the level of
datasets and disconfirmed at the level of cells, and both are stated.

**The remaining points.** The label requirements are now separated in a table
(z_w source-only, ρ target features without labels, t* target labels), the sign
claim is restricted to the settings where it holds, the split-sample AUCs carry
bootstrap intervals, and the SVM is described as unstable (0.571, 0.328, 0.478
with intervals) rather than uniformly at chance.

## Minor items (no new experiments)

1. Fig. 2 still plots five datasets. Add the SEED-IV unit (z_w = 1.00, penalty
   −0.070) so that the reader can see the held-out point in the figure the
   argument rests on.
2. The Highlights still describe the earlier version; they should mention the
   held-out dataset and the within-dataset failure.
3. Table 2's SEED-IV row previously carried 1.00 in the z_T column, which is the
   z_w value; it now reads 56.3. Please double-check the other rows.
4. Section 5's Step 1 still gives z_w ranges "0.35 to 0.9" chosen from the five
   development datasets; the held-out dataset sits at 1.00 and should be named
   as support for the upper range.

## Assessment

The paper now states what it proves, measures the quantities it claims to
measure, tests its screen outside the data that produced it, and reports the
places where the screen fails. The characterization and the signed law are
solid contributions of the kind BSPC publishes; the screen is a bounded,
honestly described empirical finding. I recommend minor revision, and I expect
to accept once the four items above are addressed.
