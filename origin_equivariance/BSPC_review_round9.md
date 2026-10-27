# Referee report, round 9 — BSPC submission v14

**Recommendation: Major Revision** (previous round: Reject).

The decisive item of the last report — the representation-dependence of `z_w` —
was correct, and the authors fixed it in the only way that works: they moved the
scale to the centred scores, showed the invariance to 4 × 10⁻¹⁶ under my
transformation, and then recomputed everything the screen rested on. The
recomputation costs them the screen, and they removed it from the abstract, the
title and the contributions rather than reporting the old numbers.

## The decisive item

With the corrected definition the six-dataset association is rho = −0.77 with
exact p = 0.103, the held-out median z_w is 24.4 rather than 1.00, and the
operating threshold still has specificity 0.000 on SEED-IV. The claim "a
source-only statistic orders the exposure of feature families" therefore does
not survive a well-defined statistic. The paper now says this in Section 4.4 and
in the abstract. This is the correct response to a counter-example, and it is
more valuable than a defended but ill-defined index would have been.

## The remaining items

**Fixed.** The circularity of the oracle parameterisation is stated; the two
parameterisations are reported side by side; the model's implied accuracy is
compared with the observed one; "predictive law" is gone; Equation (6) now has a
tie-breaking rule; the unit test has a specified vector, tolerance and caveat;
the cell-versus-pair count (845 cells, 737 distinct pairs) is corrected; the
direction-blind sentence refers to z_T; the paired calibration difference
replaces the two marginal intervals; the "earlier version" language is removed.

**Still to do.**

1. **Tables 5 and 6 carry the old numbers.** The authors acknowledge this in
   their response and say the tables must be regenerated with the corrected
   definition. They may not leave a table that contradicts the text; this is a
   blocking item for me even though it is mechanical.
2. **The audit.** Still one example, and the paper still cannot say whether the
   failure mode occurs in practice. Since the screen is now gone, the practical
   motivation rests entirely on this question, so it matters more than before,
   not less.
3. **The Gaussian model's role.** With the screen removed, the paper's empirical
   weight shifts onto the displacement model, and its honest performance under
   the correct parameterisation (r 0.86 on one dataset, 0.27 on another, not
   estimable on a third) is modest. The authors should decide whether the model
   is a contribution or a lens, and write accordingly; at present Section 4.5
   still reads as if it were a contribution.

## Assessment

The paper is now a correct, narrow study of a mechanism and its boundaries, with
two negative results that are useful to the field. That is publishable in BSPC if
the three items above are resolved: the tables regenerated, the audit added, and
the model's status settled. I would then expect to recommend minor revision.
