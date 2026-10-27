# -*- coding: utf-8 -*-
"""v10e: Fig. 4, contribution layering, conclusion."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)
R = []

# Fig. 4 reference + caption in 4.5
R.append((
"""The law is quantitative where its Gaussian approximation is defensible""",
"""Fig. 4 plots the per-cell prediction against the per-cell observation for LDA on the 800 binary cells, with the identity line; the error distribution is centred on zero with a mean absolute value of 0.030 and no systematic dependence on the size of the change.

**Fig. 4.** (a) Predicted change of Equation (4) against the observed change, one point per cell, LDA, the 800 binary cells of the four binary datasets; the dotted line is the identity. (b) Distribution of the prediction error.

The law is quantitative where its Gaussian approximation is defensible"""))

# layering in 6.1
R.append((
"""The practical content of Propositions 1–3 is a decision:""",
"""Three kinds of statement are mixed in a paper of this shape, and it is worth separating them, because only the second is specific to EEG. The first kind is a corollary of linear discriminant theory: a constant added to a feature vector moves the intercept, so a fixed model is not invariant to it, and the prediction-relevant content of a reference is its projection onto the weights. We prove these and do not claim them as discoveries. The second kind is an empirical regularity of cross-session EEG features: which feature families carry a large free origin (log-power and differential entropy, z_T from 8 to 57; time-domain contrasts, 0.2), how large the resulting damage is on five public datasets, and the two ways in which a source-only screen fails on them. The third kind is a change in practice: centre both sessions, verify the invariance with a one-line test, and do not use a norm-based origin statistic. We have tried to keep the three apart in the text, and the abstract now leads with the second and third.

The practical content of Propositions 1–3 is a decision:"""))

# conclusion
old_concl_start = s.find("## 7. Conclusion")
old_concl_end = s.find("## CRediT authorship contribution statement")
new_concl = """## 7. Conclusion

Two centrings circulate under one name. The two-sided form is invariant to the coordinate origin; the invariant family is wider than the sample mean, and we state it rather than claiming uniqueness. Two corrections shift every score difference by the same amount exactly when their projections onto the centred weights agree, with the caveat that label predictions can agree even when score differences do not and that a degenerate class can be shifted for free.

Whether the correction helps is a separate question, and the answer is quantitative only where the Gaussian approximation holds. On the BCI datasets the signed law predicts the per-cell change of balanced accuracy with a correlation of 0.99 and a mean absolute error of 0.013 for LDA, its sign discrimination survives a split-sample test (AUC 0.91), and it degrades to a sign-level account on two other datasets and to chance for a support-vector machine. We report the degradation rather than a single accuracy figure.

Empirically, an origin sweep on 845 session pairs from five datasets leaves the equivariant pipelines unchanged by 0.000 and drives the one-sided one to exact chance; an equal-norm direction control shows that a norm-based statistic is blind to the direction of the origin and that only the component along the weights damages the decoder; and a projected source-only statistic orders the damage across the five datasets (rho = −0.90, exact p = 0.083) and separates a severe loss with an AUC of 0.84, while failing to resolve the four representations of one dataset and inverting within another. What the correction cannot repair is a change of class priors, which is confounded with a class-conditional offset unless the label-shift assumption is granted; where the priors do change, labels recover a further 0.013.

"""
if old_concl_start < 0 or old_concl_end < 0:
    print("MISS conclusion")
else:
    s = s[:old_concl_start] + new_concl + s[old_concl_end:]

for a, b in R:
    if a not in s:
        print("MISS:", a[:60].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
