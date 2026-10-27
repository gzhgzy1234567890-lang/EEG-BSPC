# Referee report, round 7 — BSPC submission v12

**Recommendation: Minor revision.**

The three items I set as the condition for minor revision are addressed, and
the paper has been repositioned to match its evidence.

## The three conditions

**1. The operational threshold is now tested on the held-out dataset.** Fixing
the threshold on all five development datasets gives t = 0.354 (development
sensitivity 0.811, specificity 0.749, precision 0.544). Applied unchanged to
SEED-IV it gives sensitivity 1.000, specificity 0.000, precision 0.544: every
cell is flagged. The authors report this in Section 4.4 and in the abstract.
This is exactly the test I asked for, and the answer is negative for the screen
and positive for the mechanism: the dataset-level prediction was right (SEED-IV
is exposed, median penalty −0.070) and the cell-level rule has no specificity.

**2. `z_w` has one definition.** Equation (2) is now the matrix definition, the
scalar form is explicitly restricted to K = 2 or equal σ_k and is not used
elsewhere, the uncentred scale convention is stated, and the invariance is
described accurately — insensitive to decision-null translations, *not*
invariant to translations along the discriminating directions. The numerical
checks are reported (1.4e-14, 2.5e-13) and the centred/uncentred difference is
quantified.

**3. The sample-size accounting is separated.** Table 3 lists each analysis with
its datasets and cell count (main experiments 845, signed law 800 binary cells,
six-dataset association six observations, external test 845 → 90), and the
abstract no longer uses 935 as the size of the sweep.

**Positioning.** The title now promises "an exploratory screen for feature
families", Section 5 labels the screen exploratory, and Section 6.1 states in
one paragraph what the paper can and cannot claim. This is the reframing I
asked for.

## Minor items

1. Fig. 2 still shows five datasets; add the SEED-IV point so the figure
   contains the held-out observation that the sixth-dataset analysis is built on.
2. The Highlights file still describes the earlier version.
3. Section 3 states the total of 935 cells; add one clause separating the 845
   development cells from the 90 test cells in that sentence, for consistency
   with Table 3.

## Assessment

The manuscript now has a coherent claim: a characterization of the first-order
correction, a signed law that is quantitative where the Gaussian approximation
holds and honestly bounded elsewhere, and an exploratory screen whose
dataset-level association replicates on a held-out dataset while its
cell-level rule does not. The failures are reported rather than hidden, and the
sample sizes are no longer borrowed across analyses. I recommend minor
revision; the three items above are editorial and require no new experiments.
