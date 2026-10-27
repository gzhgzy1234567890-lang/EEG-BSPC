# -*- coding: utf-8 -*-
"""Update the response letter's MC3 with the projected statistic and LODO."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\RESPONSE_to_reviewer.md"
s = io.open(P, encoding="utf-8").read()

old = """The independence problem is addressed by changing the level of inference. The
primary analysis is now at the dataset level (n = 5): median z_T against median
penalty gives a rank correlation of −0.80 with p = 0.10, and we say that this
has no power. The unit-level analysis is retained but its uncertainty is
estimated by a **cluster bootstrap that resamples datasets**, not units, giving
a 95 per cent interval of [−1.000, −0.275] over 4,993 resamples. The permutation
test over the eleven units that the earlier draft reported (p = 0.009) is
removed, and the 845-cell correlation (−0.382) is labelled descriptive. The
operational ranges of Section 5 are labelled "descriptive of the eleven units
studied, not validated thresholds". A leave-one-dataset-out evaluation is not
reported; with five datasets we would be fitting a one-parameter relation on
four and testing on one, and we say in Section 6.4 that an independent dataset
is what the claim would need. (Section 4.3 new; Section 4.4 rewritten; Section
5; Section 6.4 "The screen is direction-blind", "Five datasets cannot establish
a law".)"""

new = """We also did what the referee asked in the last paragraph of MC3: a fair
comparison with a source-only indicator related to the decision direction.
Define

  z_w = ||P W μ_A|| / (√K σ_s),

which uses only the source session — the fitted weights, the source mean and
the score spread. It is invariant to a translation orthogonal to W *by
construction*, so it passes the test that the norm-based z_T fails. It is also
better at every level: dataset level −0.90 (p = 0.035) against −0.80
(p = 0.10); unit level −0.855 (p = 0.001) against −0.755; cluster-bootstrap
interval [−1.00, −0.60] against [−1.00, −0.28]; cell level −0.502 against
−0.382. **z_w is now the screen the paper recommends; z_T is retained only as
the naive alternative whose failure the direction experiment measures.**

The independence problem is addressed by changing the level of inference. The
primary analysis is at the dataset level (n = 5), where the projected statistic
is significant. The unit-level analysis is retained but its uncertainty is
estimated by a **cluster bootstrap that resamples datasets**, not units. The
permutation test over the eleven units that the earlier draft reported is
removed, and the 845-cell correlation is labelled descriptive. The operational
ranges of Section 5 are labelled "descriptive of the eleven units studied, not
validated thresholds".

A **leave-one-dataset-out** evaluation is now reported: fitting log z_w against
the penalty on four datasets and predicting the fifth gives median absolute
errors of 0.021, 0.027 and 0.075 on grasp-and-lift, NER2015 and SEED, and
underestimates on the two BCI datasets (BCI-2b: predicted −0.074 against
observed −0.149). We report the failures as well as the successes and say that
four datasets are not a training set. (Section 4.3 new; Section 4.4 rewritten;
Section 2.3 Equation (2b); Section 5; Section 6.4.)"""

if old not in s:
    print("MISS")
s = s.replace(old, new)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
