# THEORY_PROOFS.md — two-class composition model and decision-stability certificate

Revision 2 (after an independent referee report). The changes from revision 1 are listed at the end; three of
them are corrections of errors, not clarifications.

Status: Propositions 1, 2, 3, 3b and 4 are proved below and verified numerically in THEORY_TEST_RESULTS.md.
Proposition 5 is proved in the finite-sample form and its population form is stated separately. Nothing here is
claimed for multi-class EEG beyond the linear-algebra identity of Proposition 4.

## Model

- One-dimensional feature x (the multi-dimensional case is recovered by projecting onto w; see the remark after
  Proposition 2).
- X | Y=+1 ~ N(a, sigma^2), X | Y=-1 ~ N(-a, sigma^2), a > 0.
- Source prior P_A(+1) = 1/2; target prior P_B(+1) = pi_B.
- Classifier: affine score s(x) = w x with w > 0, and the decision rule "predict +1 iff x > t", where **t is a
  threshold in feature space**. Equivalently the rule is s(x) > w t, so a threshold quoted in score space is w t.
  Every t in this document is a feature-space threshold unless it is written w t.

## Proposition 1 (the target mean shift is pure class composition)

With no nuisance drift, mu_A = 0 and mu_B = (2 pi_B - 1) a, so

    mu_B - mu_A = (2 pi_B - 1) a.

Proof. mu_A = 1/2 a + 1/2 (-a) = 0; mu_B = pi_B a + (1 - pi_B)(-a) = (2 pi_B - 1) a. The class-conditional means
are identical in source and target by assumption. QED.

## Proposition 2 (balanced accuracy as a function of the feature-space threshold)

    BA(t) = 1/2 [ Phi((a - t)/sigma) + Phi((a + t)/sigma) ].

Proof. A +1 sample is correct iff x > t with x ~ N(a, sigma^2), probability Phi((a - t)/sigma). A -1 sample is
correct iff x < t with x ~ N(-a, sigma^2), probability Phi((a + t)/sigma). Average. QED.

Remark (dimension). The formula is stated for a feature-space threshold. If a threshold is quoted in score space,
s(x) > tau, the equivalent feature threshold is t = tau / w, and substituting it is mandatory; using tau directly
in the formula above is correct only when w = 1. Revision 1 of this document made exactly that mistake, and the
referee's numerical example (a = 2, sigma = 1, w = 4, tau = 1: 0.9200 against the correct 0.9739) is reproduced in
THEORY_TEST_RESULTS.md as a regression test.

For a D-dimensional feature with a linear score w'x, the same argument applies to the projected variable
u = w'x / ||w||, whose class-conditional distributions are again normal with equal variance; the threshold is then
expressed on u. The formula is therefore not restricted to one dimension, but it is restricted to equal class
variances in the projected direction.

## Proposition 3 (the balanced-optimal threshold does not depend on the class prior)

BA(t) is maximised at t = 0 for every pi_B. The loss from a threshold displacement d is

    BA(0) - BA(d) = 1/2 [ 2 Phi(a/sigma) - Phi((a - d)/sigma) - Phi((a + d)/sigma) ] >= 0,

with equality iff d = 0. Its second-order expansion is

    BA(0) - BA(d) = (a d^2 / (2 sigma^3)) phi(a/sigma) + O(d^4).

Proof. Differentiating,

    BA'(t)  = [ phi((a + t)/sigma) - phi((a - t)/sigma) ] / (2 sigma),
    BA''(t) = [ phi'((a + t)/sigma) + phi'((a - t)/sigma) ] / (2 sigma^2).

BA'(0) = 0 and BA''(0) = phi'(a/sigma)/sigma^2 = -(a/sigma) phi(a/sigma)/sigma^2 = -a phi(a/sigma)/sigma^3 < 0 for
a > 0, so t = 0 is the unique maximiser by symmetry and unimodality. The Taylor expansion gives
BA(d) = BA(0) + 1/2 BA''(0) d^2 + O(d^4), hence the stated coefficient. QED.

Corollary (harm of a composition-only correction). If the correction removes d = (2 pi_B - 1) a and there is no
drift, the corrected balanced accuracy is BA(d) < BA(0) whenever pi_B != 1/2, and the loss grows like
a d^2 phi(a/sigma) / (2 sigma^3).

Note the coefficient: it is proportional to a / sigma^3, not to 1 / sigma^2. The two agree only when a = sigma,
which is exactly the parameter choice at which revision 1 checked the expansion, which is why the error survived
that check. The regression test now uses a != sigma.

## Proposition 3b (with genuine baseline drift, and the constrained optimal weight)

Let both class-conditional means be shifted by b in the target. The balanced-optimal threshold is then t* = b, the
mean displacement is d = c + b with c = (2 pi_B - 1) a, and correcting with weight lambda in [0, 1] leaves the
residual threshold

    r(lambda) = b - lambda (c + b) = (1 - lambda) b - lambda c.

The unconstrained zero of r is lambda_0 = b / (b + c) when b + c != 0, and the constrained optimum is

    lambda* = clip_{[0,1]} ( b / (b + c) ).

If b + c = 0 the displacement is zero, r(lambda) = b for every lambda, and all weights give the same decisions.

Proof. Shifting both means by b shifts the feature distribution by b, so the optimal threshold moves from 0 to b.
The displacement removed at weight lambda is lambda (c + b), hence the residual. Setting r = 0 gives
lambda = b / (b + c); if that value lies outside [0, 1] the loss is monotone in lambda on the interval and the
optimum is at the nearer endpoint, which is the clip. If b + c = 0 the correction removes nothing and the residual
is b regardless of lambda. QED.

Worked boundary cases: (b, c) = (0.5, -0.4) gives lambda_0 = 5 and lambda* = 1; (b, c) = (0.8, 0.2) gives 0.8;
(b, c) = (0, 0.5) gives 0. Revision 1 printed lambda* = 5 for the first case, which is outside the allowed range.

## Proposition 4 (decision-stability certificate, multi-class)

Assumption: ties are broken by a fixed rule, and we say the prediction is stable if the tie-broken argmax is
unchanged. Let a fixed affine classifier give scores s_k(x) = w_k'x + b_k, let the correction displace scores by d
in R^K, and let k* be the predicted class before correction.

Sufficient and necessary condition for stability, when no corrected score is tied with the top score:
s_{k*}(x) - s_j(x) > d_{k*} - d_j for every j != k*. With ties permitted the condition becomes non-strict
(>=) for the classes that tie, because a tie broken toward k* leaves the prediction unchanged.

Proof. Corrected scores are s_k - d_k. k* remains the argmax iff s_{k*} - d_{k*} >= s_j - d_j for all j, with
strict inequality required exactly when the tie-break would otherwise favour j. Rearranging gives the statement.
QED.

Remarks. The certificate is exact and per-sample and needs no labels; it certifies **stability of the
prediction**, not accuracy; the flip rate computed from it is not an accuracy estimate.

## Proposition 5 (finite-sample non-identifiability) and its population counterpart

**Finite sample.** For a fixed feature set, a fixed feature-only correction rule and a fixed classifier, two label
assignments consistent with the same features can give correction gains of opposite sign.

Construction (the referee's, independently verified here): features (0.4, 1.2, -1.2, -1.2), threshold 0,
displacement 0.5.

| labels | BA before | BA after | change |
|---|---|---|---|
| (+, +, -, -) | 1.000 | 0.750 | -0.250 |
| (-, +, -, -) | 0.833 | 1.000 | +0.167 |

The features, the classifier and the displacement are identical; only the labels differ. QED.

**Population, symmetric Gaussian with equal variances.** In the model of Proposition 1-3b, a positive *expected*
gain requires b != 0: with no drift the optimal threshold is 0 for every prior, so any non-zero displacement
removed is harmful in expectation. This is consistent with the finite-sample statement: the counterexample above is
not restricted to that population model, and the two statements answer different questions.

Revision 1 called the sign-flip case "open"; that was wrong, and the referee's construction settles it.

## Scope

Propositions 1-3b are statements about a symmetric, equal-variance Gaussian model with a linear threshold; they do
not extend to multi-class EEG. Proposition 4 is an identity with a stated tie convention. Proposition 5's finite
sample part is a statement about identifiability from unlabeled data, not a claim about any dataset.

## Changes from revision 1

1. **Corrected**: the second-order coefficient was (d^2 / (2 sigma^2)) phi(a/sigma); it is
   (a d^2 / (2 sigma^3)) phi(a/sigma). The sign remark on BA''(0) was also wrong (-phi'/sigma^2 has the wrong
   sign and the wrong derivative).
2. **Corrected**: the residual threshold was written (1 - lambda) b + lambda c; it is (1 - lambda) b - lambda c.
3. **Corrected**: the threshold t is now defined in feature space, with the score-space equivalent w t stated
   explicitly; revision 1 switched between the two silently.
4. **Completed**: the optimal weight now carries the [0, 1] constraint, the zero-denominator case and worked
   boundary examples.
5. **Corrected**: Proposition 5's finite-sample sign flip is proved, not open.
6. **Completed**: Proposition 4 states its tie convention.
