# THEORY_TEST_RESULTS.md

Revision 2. Revision 1's tests passed while the document contained three errors; this revision records what
changed, what the referee found, and the regression tests that now fail if the errors return.

## What revision 1 got wrong

| item | revision 1 | correct | caught by |
|---|---|---|---|
| second-order coefficient | (d^2 / (2 s^2)) phi(a/s) | (a d^2 / (2 s^3)) phi(a/s) | independent referee, MC1 |
| BA''(0) | "−phi'(a/s)/s^2 < 0" | phi'(a/s)/s^2 = −a phi(a/s)/s^3 < 0 | numeric second difference |
| residual threshold | (1−lambda) b + lambda c | (1−lambda) b − lambda c | direct evaluation |
| optimal weight | b/(b+c) unconstrained | clip_{[0,1]}(b/(b+c)), undefined if b+c = 0 | the case (b,c) = (0.5,−0.4) gives 5 |
| threshold t | feature space in Prop 2, score space in the model | feature space throughout, score threshold = w t | the case a=2, s=1, w=4, t=1: 0.9200 vs 0.9739 |
| Proposition 5 | sign flip "open" | proved by a two-labelling counterexample | referee's construction |

The coefficient error survived revision 1 because every numerical check used a = s, where a/s^3 = 1/s^2. That is
now impossible: the regression test uses (a, s) = (2, 1), (0.5, 2) and (2, 0.7).

## Regression tests (revision 2), all passing

| test | result |
|---|---|
| second-order coefficient at a != s | relative error 8e-8, 7e-8, 9e-7 at the three parameter pairs |
| BA''(0) = −a phi(a/s)/s^3 | numeric −0.107982 against formula −0.107982 (a=2, s=1); −0.241971 (1,1); −0.024167 (0.5, 2) |
| threshold rescaling | feature threshold 0.25 gives 0.9739; misreading the score threshold as a feature threshold gives 0.9200 |
| constrained weight | (0.5,−0.4) -> 1.00; (0.8,0.2) -> 0.80; (0,0.5) -> 0.00; (0.5,−0.5) -> undefined |
| residual convention | 0.800 / 0.250 / −0.300 at lambda = 0 / 0.5 / 1 |
| numerical optimum of lambda | grid 0.533 against formula 0.533 |
| finite-sample sign flip | −0.250 and +0.167 on the same features |
| certificate tie convention | strict condition holds when no tie; a tie can only relax it |

`THEORY TEST PASS`.

## Earlier results retained

- closed form BA(t) against Monte Carlo within 1e-3 at five settings (unchanged, the formula was right);
- numerical maximiser t* = 0.000000 (unchanged);
- harm monotone in |2 pi_B − 1| (unchanged);
- the D1 50-cell simulation reproduced the predicted sign in 50 of 50 cells (unchanged, it uses the sign of the
  effect, not the second-order coefficient);
- the certificate matched the observed flip pattern for 400 of 400 simulated samples and for all scored trials on
  three BCI-2b subjects (unchanged).

## What this episode says about the first gate

The first quality gate reported "theory verified" while the coefficient was wrong. Numerical checks that only probe
signs and optima cannot catch a coefficient error; the gate was therefore not a substitute for independent
review, and this document now records that explicitly.
