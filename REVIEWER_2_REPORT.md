# REVIEWER_2_REPORT.md — Theory and novelty

Internal adversarial review. Not an external referee.

## Summary judgement

**Major revision / borderline reject on novelty.** The theory is correct but thin, and the closest prior work
already contains the qualitative claim.

## T1. Proposition 1 is an identity, not a discovery (Section 2.3, p. 5)

mu_B - mu_A = sum_k (p_Bk - p_Ak) m_k follows from the definition of a mixture mean. It is true, useful for
framing, and not new. Severity: high for a novelty claim, low for correctness. Requirement: never call it a
finding; the paper currently does not, which is good, but the abstract's "the algebra sets the terms" borders on
implying novelty.

## T2. SPDIM (ICLR 2025) already reports that alignment hurts under label shift

The abstract states that Riemannian alignment "can compensate ... but hurt generalization under label shifts".
Our contribution A is a first-order version of the same qualitative statement. Severity: high. Requirement: the
introduction must cite SPDIM for the qualitative claim and claim only the first-order decision-space formula and
the lambda* result as new. Currently SPDIM is not cited at all in the manuscript.

## T3. Proposition 5 is the only non-trivial statement, and it is weak

"The gain is not a function of unlabeled features" is shown by a four-point example with different labelings.
That is a counterexample to a strong claim nobody makes; the interesting version (the sign can be either) is
admitted open. Severity: moderate. Requirement: keep it, but do not present it as an impossibility result about
label-free prediction in general.

## T4. The theory is one-dimensional and Gaussian

Everything except the certificate is derived for symmetric Gaussians. The paper says so; the abstract does not.
Severity: moderate. Requirement: the abstract should not imply the model covers multi-class EEG.

## T5. Novelty statement

After removing what SPDIM, BBSE, the EEG-leakage literature and Widmann already cover, the remainder is: a
first-order correction-specific failure formula, a per-sample certificate for a correction displacement, and a
protocol audit that separates filter from alignment. That is a modest but real contribution for BSPC; it is not a
new method.

## Verdict

Major revision. T2 is the blocking item: SPDIM must be cited and the claim narrowed.
