# THEORY_TEST_RESULTS.md

Script: `origin_equivariance/src/theory_test.py`, seed 20261101, Python 3.7 / scipy 1.7.3.
Command: `python theory_test.py` -> `THEORY TEST PASS`.

## Proposition 2 and 3: the closed form and the optimum

| a | sigma | pi_B | d=(2pi-1)a | BA formula | BA Monte Carlo (200k) | abs diff |
|---|---|---|---|---|---|---|
| 1.0 | 1.0 | 0.50 | 0.000 | 0.8413 | 0.8405 | 0.0009 |
| 1.0 | 1.0 | 0.30 | -0.400 | 0.8225 | 0.8227 | 0.0002 |
| 1.0 | 1.0 | 0.90 | +0.800 | 0.7717 | 0.7707 | 0.0010 |
| 0.5 | 2.0 | 0.15 | -0.350 | 0.5972 | 0.5965 | 0.0008 |
| 2.0 | 0.7 | 0.60 | +0.400 | 0.9943 | 0.9942 | 0.0000 |

Numerical maximiser of BA(t): t* = 0.000000, matching Proposition 3.

## The harm of a composition-only correction

| pi_B | BA(0) - BA(d) |
|---|---|
| 0.50 | 0.00000 |
| 0.60 | 0.00481 |
| 0.80 | 0.04103 |
| 0.95 | 0.08579 |

Monotone in |2 pi_B - 1|, as the corollary states.

## Proposition 3b: the optimal correction weight

With drift b = 0.8, pi_B = 0.7, a = 1: theory lambda* = 0.6667; grid optimum over 101 values of lambda = 0.67.

## Proposition 4: the certificate

K = 4, D = 6, n = 400 samples, random W, b and displacement d. The certificate (margin condition, no labels)
predicted the observed flip pattern for **400/400** samples.

## Proposition 5: the same features, two labelings

| labeling | pi_B | d | BA before | BA after | change |
|---|---|---|---|---|---|
| (1, 1, -1, -1) | 0.50 | +0.5 | 1.000 | 0.750 | -0.250 |
| (1, -1, -1, -1) | 0.25 | +0.5 | 0.833 | 0.333 | -0.500 |

Same features, same classifier, same displacement; different labels; different gain.

## What failed and what is not claimed

- The first version of Proposition 5 tried to show a sign change with fixed features; the model does not allow a
  positive gain without drift, so the claim was weakened to "the gain is not a function of the unlabeled data".
  The sign-change version is recorded as open in THEORY_PROOFS.md.
- The first extended unit test asserted translation invariance of predictions under a constant feature shift.
  That assertion was wrong (a constant shift changes per-class scores), it failed, and it was replaced by the
  correct displacement-equivalence assertion.
