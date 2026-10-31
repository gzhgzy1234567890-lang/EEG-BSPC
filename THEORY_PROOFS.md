# THEORY_PROOFS.md — two-class composition model and decision-stability certificate

Status: propositions 1-4 are proved below and verified numerically in THEORY_TEST_RESULTS.md. They hold for the
stated model only; nothing here is claimed for multi-class EEG beyond the linear-algebra identity of
Proposition 4.

## Model

- Features X in R^D, two classes Y in {+1, -1}.
- Conditional distributions: X | Y=+1 ~ N(a, S), X | Y=-1 ~ N(-a, S), with S = sigma^2 I and a != 0.
- Source prior: P_A(+1) = P_A(-1) = 1/2. Target prior: P_B(+1) = pi_B.
- No nuisance drift in Proposition 1-3; drift is added in Proposition 3b.
- Classifier: affine, w = 2a/S (the LDA direction for equal covariances and equal priors), score s(x) = w'x,
  decision by sign of s(x) - t.

## Proposition 1 (the target mean shift is pure class composition)

Under the model, mu_A = 0 and mu_B = (2 pi_B - 1) a, so the difference of class-conditional means is zero and

    mu_B - mu_A = (2 pi_B - 1) a.

Proof. mu_A = 1/2 a + 1/2 (-a) = 0. mu_B = pi_B a + (1 - pi_B)(-a) = (2 pi_B - 1) a. The class-conditional
means a and -a are identical in the two domains by assumption. QED.

Consequence: the displacement that a mean correction removes is, in this model, exactly the class-composition
term; there is no nuisance component to remove.

## Proposition 2 (balanced accuracy as a function of the threshold)

For a threshold t,

    BA(t) = 1/2 [ Phi((a - t)/sigma) + Phi((a + t)/sigma) ].

Proof. A +1 sample is classified correctly iff w'x > t, i.e. x > t (since w > 0 up to the sign convention), and
x ~ N(a, sigma^2), so the probability is Phi((a - t)/sigma). A -1 sample is correct iff x < t, with x ~ N(-a,
sigma^2), probability Phi((a + t)/sigma). Average. QED.

## Proposition 3 (the balanced-optimal threshold does not depend on the class prior)

BA(t) is maximised at t = 0 for every pi_B, and

    BA(0) - BA(d) = 1/2 [ 2 Phi(a/sigma) - Phi((a - d)/sigma) - Phi((a + d)/sigma) ] >= 0,

with equality iff d = 0. For small |d| the loss is second order, BA(0) - BA(d) = (d^2 / (2 sigma^2)) phi(a/sigma)
+ O(d^4).

Proof. BA'(t) = (1/(2 sigma)) [ -phi((a - t)/sigma) + phi((a + t)/sigma) ], which vanishes at t = 0; the second
derivative at 0 is -phi'(a/sigma)/sigma^2 < 0 for a > 0, so t = 0 is the unique maximiser by symmetry and
unimodality. Substituting d = (2 pi_B - 1) a gives the stated expression; it is 0 only when pi_B = 1/2. The
expansion follows from Taylor expansion of Phi around a/sigma. QED.

Corollary (the harm of a composition-only correction). If a mean correction removes d = mu_B - mu_A and there is
no drift, the corrected balanced accuracy is BA(d), which is strictly below BA(0) whenever pi_B != 1/2. The loss
increases with |2 pi_B - 1| for |d| below a sigma.

## Proposition 3b (with genuine baseline drift)

Let both class-conditional means be shifted by b in the target: X | Y=+1 ~ N(a + b, sigma^2), X | Y=-1 ~
N(-a + b, sigma^2). Then the balanced-optimal threshold is t* = b, and the mean difference is
mu_B - mu_A = (2 pi_B - 1) a + b. A correction that removes the full displacement d = (2 pi_B - 1) a + b leaves the
threshold at 0 in the drift-free frame, which is optimal if and only if pi_B = 1/2. A partial correction with
weight lambda in [0, 1] leaves the threshold at (1 - lambda) b + lambda (2 pi_B - 1) a, and the optimal lambda is

    lambda* = b / (b + (2 pi_B - 1) a)   when the denominator is non-zero,

i.e. full correction when the composition term vanishes, and less than full correction when it does not.

Proof. Shifting both means by b shifts the score distribution by w'b, so the balanced-optimal threshold moves from
0 to b. The mean difference follows from Proposition 1 applied to the shifted means. The residual threshold after
removing lambda d is b - lambda d, which is zero exactly when lambda = b / d. QED.

Corollary. Correction can help and harm in the same model: it helps when |b| > |(2 pi_B - 1) a| and pi_B is near
1/2, and it harms when the composition term dominates.

## Proposition 4 (decision-stability certificate, multi-class)

Let a fixed affine classifier give scores s_k(x) = w_k'x + b_k, let the correction displace scores by d in R^K,
and let k* = argmax_k s_k(x). The corrected prediction equals k* if and only if

    s_{k*}(x) - s_j(x) > d_{k*} - d_j   for every j != k*.

Proof. Corrected scores are s_k - d_k. k* remains the argmax iff s_{k*} - d_{k*} > s_j - d_j for all j != k*;
rearranging gives the stated inequality. QED.

Remarks.
1. The certificate is exact and per-sample; it needs no labels.
2. It certifies **stability of the prediction**, not accuracy. A sample can keep its prediction and still be wrong,
   and a sample can flip from wrong to right. The flip rate computed from it is not an accuracy estimate and must
   never be presented as one.
3. The stability region is a polyhedron in d for each sample; the correction is decision-invariant on the
   intersection over the scored samples, which is the "prediction-invariant subspace" of the linear case.

## Proposition 5 (the gain is not a function of the unlabeled target features)

For a fixed classifier, a fixed target feature set X_B and a fixed correction displacement d (which depends only
on X_B and the source), the change in balanced accuracy produced by the correction depends on the target labels.
It is therefore not a function of the unlabeled target data.

Proof by construction. Let X_B = {0.4, 1.2, -1.2, -1.2}, a = 1, and d = 0.5 (any labelling-independent
displacement). With labels (1, 1, -1, -1) the uncorrected balanced accuracy is 1.0 and the corrected one is 0.75,
a change of -0.25. With labels (1, -1, -1, -1) the same features and the same displacement give 0.833 before and
0.333 after, a change of -0.5. The features, the classifier and the displacement are identical; only the labels
differ. QED.

What this does and does not establish.

- It establishes that no estimator of the gain can be a function of X_B alone, for this displacement rule.
- It does **not** establish that the sign of the gain can be either sign for fixed features. In this model a
  positive gain requires a genuine drift term b (Proposition 3b), which is a property of the features rather than
  the labels, so the sign question needs a separate construction. That construction is **open** and is not
  claimed here.

Relation to the literature. Label-shift theory (Saerens 2002; Lipton 2018) assumes that the class-conditional
distributions are unchanged and estimates the prior from unlabeled data; under that assumption the *prior* is
identifiable, and our Proposition 5 is consistent with it: what is not identifiable is the effect of a fixed
displacement on balanced accuracy, because that depends on the joint of features and labels. No claim of priority
is made.
