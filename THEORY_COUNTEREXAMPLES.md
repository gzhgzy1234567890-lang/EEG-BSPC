# THEORY_COUNTEREXAMPLES.md

Every proposition in THEORY_PROOFS.md was attacked with the counterexamples the goal requires. The table records
what was tried, whether the proposition survived, and how the scope was narrowed when it did not.

| probe | construction | result |
|---|---|---|
| **Asymmetric class variances** | X | Y=+1 ~ N(a, s1^2), X | Y=-1 ~ N(-a, s0^2), s1 != s0 | Proposition 1 (mixture mean) survives. Proposition 2's closed form for BA(t) survives with Phi((a-t)/s1), Phi((a+t)/s0); Proposition 3's "optimal threshold is 0" **fails**: the optimum is (a s0 - a s1 ... ) shifted, in general not 0. **Scope narrowed**: Prop 3-3b assume equal variances and say so. |
| **Correlated features** | 2-D with covariance S not equal to sigma^2 I | The displacement formula survives (it is linear algebra), the BA(t) formula **fails** because the score is a projection and the two class projections have different variances. **Not claimed**: the closed form is one-dimensional. |
| **Non-uniform source priors** | p_A(+1) = 0.7 instead of 0.5 | mu_A is no longer 0, so d = mu_B - mu_A includes the source imbalance. Prop 1 must be restated with p_A; the paper uses balanced sources and says so. |
| **Multi-class** | K = 4 with classes at +a, -a, +a', -a' | Props 1-3b **do not apply** (no single threshold). Only Prop 4 (certificate) holds, as an identity. **Scope narrowed** in the manuscript. |
| **Non-linear classifier** | quadratic discriminant | Prop 4 **fails** (score differences are no longer linear in x), so the certificate is stated for fixed affine classifiers only. |
| **Weight error** | classifier trained on a shifted source (w' = w + delta) | Prop 3's optimum is no longer exactly 0; the loss from a composition correction persists but its size changes. Not quantified; flagged as an assumption. |
| **Unequal class costs** | weighted accuracy with cost ratio 3:1 | The balanced-optimal threshold moves away from 0, so a composition correction can accidentally help. **Not claimed**: the paper evaluates balanced accuracy. |
| **Label noise** | 10 per cent flipped labels in the target | Prop 1's displacement is attenuated by (1-2e); the qualitative conclusion holds, the quantitative one does not. Not tested in the paper; noted as a limitation. |

## The two failed constructions, recorded

1. **Translation invariance of predictions.** I first asserted that adding a constant to all features leaves the
   corrected predictions unchanged. It does not: a constant c adds w_k'c to each class score, and w_k differ. The
   assertion was wrong, the test failed, and it was replaced by the correct statement that the score-space
   displacement equals the projected feature-space displacement (verified to 1e-10).

2. **Sign change with fixed features (Proposition 5).** I tried to build two labelings of the *same* features for
   which the correction helps in one and harms in the other. In the symmetric model this is impossible without a
   drift term, because the optimal threshold does not depend on the prior. The claim was weakened to "the gain is
   not a function of the unlabeled features", which is provable with a two-labeling example (-0.25 vs -0.50), and
   the sign-change version is marked **open** in THEORY_PROOFS.md.

Both failures are recorded rather than hidden: the first in THEORY_TEST_RESULTS.md, the second in THEORY_PROOFS.md
and here.
