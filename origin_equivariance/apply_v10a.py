# -*- coding: utf-8 -*-
"""v10: the referee's two critical items and the supporting corrections."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)
R = []

# ---------- abstract ----------
new_ab = """Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We separate three questions. Equivariance: a correction is invariant to the coordinate origin if it translates by a translation-equivariant estimate of the target mean; this family contains more than the sample mean, and we do not claim uniqueness. Score-difference equivalence: two corrections shift every class score by the same amount exactly when their references differ by a vector whose projection onto the centred classifier weights vanishes; for a finite sample that is sufficient but not necessary for identical predictions. Performance: no equivariant correction is optimal in general. A signed law predicts the change in balanced accuracy from the pre-existing threshold error; on the BCI datasets it is quantitative per cell (r = 0.99, MAE 0.013 for LDA) and its sign discrimination survives a split-sample test (AUC 0.91), while for a support-vector machine it is at chance.

On 845 session pairs from five public datasets an origin sweep leaves the equivariant pipelines unchanged by 0.000 in balanced accuracy and drives the one-sided one to exact chance. A direction-controlled sweep shows that a norm-based statistic is direction-blind; a projected source-only statistic orders the damage across the five datasets (rho = −0.90, exact permutation p = 0.083, ten of 120 permutations) and detects a severe loss with AUC 0.84 [0.73, 0.88], with two failure cases that we report. What the correction cannot repair is a change of class priors.
"""
ab_old = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(0)
s = s.replace(ab_old, "## Abstract\n\n" + new_ab + "\n**Keywords")

# ---------- Prop 3 ----------
R.append((
"""**Proposition 3 (prediction equivalence).** Two references γ and γ' give the same predictions for every input x if and only if W(γ − γ') is a class-constant vector, equivalently P W(γ − γ') = 0.""",
"""**Proposition 3 (score-difference equivalence).** The score differences s_j − s_k are identical for every input x and every pair (j,k) if and only if W(γ − γ') is a class-constant vector, equivalently P W(γ − γ') = 0."""))

R.append((
"""For a finite target sample the condition is sufficient but not necessary: if PW(γ − γ') ≠ 0 but no target sample crosses the boundary that the difference moves, the predictions agree. Section 4.6 reports both the exact condition and the observed agreement, which is 100.0 per cent for the projected correction because that correction lies in the null space.""",
"""Two caveats, both of which the referee of an earlier version asked for. First, identical score differences are sufficient for identical predictions on every input but not necessary: a class whose score is dominated everywhere by another class can be shifted without changing any decision, so the label-equivalence class is strictly larger than the score-difference class. Second, for a finite target sample the condition is again sufficient but not necessary, because no sample may cross the boundary that moves. We therefore state the proposition for score differences and treat prediction agreement as a corollary, which is all the paper uses. Section 4.6 reports the exact condition and the observed agreement, which is 100.0 per cent for the projected correction because that correction lies in the null space."""))

# ---------- 2.3 binary reduction ----------
R.append((
"""z_w uses only the source session — the fitted weights and the source mean — and it is invariant to a translation of the features orthogonal to W by construction, which is exactly the failure mode of a norm-based statistic (Section 4.3). For the binary case it reduces to |w'μ_A| / (||w|| σ_s).""",
"""z_w uses only the source session — the fitted weights and the source mean — and it is invariant to a translation of the features orthogonal to W by construction, which is exactly the failure mode of a norm-based statistic (Section 4.3). The binary reduction is exact and contains no ||w||: with W = [w'; −w'] one has P W μ = [w'μ; −w'μ], so ||P W μ|| = √2 |w'μ| and, since √K = √2, z_w = |w'μ_A|/σ_s. (An earlier version wrote |w'μ_A|/(||w|| σ_s); that was wrong, and the code has always used the correct expression — we verified the agreement to 4 × 10⁻¹⁴ across 200 cells.) The quantity σ_s is the standard deviation of the source decision values s(x) = w'x + b, pooled over classes and samples; for K > 2 it is the vector of per-column standard deviations of the score matrix, divided elementwise."""))
# ---------- 2.3 definitions table ----------
R.append((
"""**The size.** If the class-conditional scores""",
"""**Table 2.** The two statistics, and what each one needs.

| symbol | definition | inputs | role |
|---|---|---|---|
| z_T | ‖μ_A‖ / ‖sd_A‖ | source features | naive origin distance; direction-blind (Section 4.3) |
| z_w | ‖P W μ_A‖ / (√K σ_s) | source features and fitted weights | source-only screen recommended here |
| ρ | ‖P W μ_B‖ / (√K σ_s) | target features, no labels | the displacement that carries the mechanism |
| s | w'μ_A / σ_s (binary) | source features and fitted weights | signed displacement of the one-sided relative to the two-sided pipeline |

**The size.** If the class-conditional scores"""))

# ---------- 2.4 equation ----------
R.append((
"""Write the target class-conditional means as m_kB = m_kA + ḡ + h_k with Σ_k π_kB h_k = 0, where ḡ is the class-balanced offset. Then

    μ_B − μ_A = ḡ + Σ_k π_kB h_k + Σ_k (π_kB − π_kA) m_kA ,                    (5)

and the last term — the change in the mixture of the source class means — is present even when nothing about the class-conditional distributions changes. Subtracting μB − μA therefore removes three things at once: the recording offset, the class-conditional offset, and the prior-induced mixture term. On a balanced design the last two terms are small and the correction is close to what one wants; when the priors change they are not.""",
"""Write m_kB = m_kA + ḡ + h_k where ḡ = Σ_k π_kB (m_kB − m_kA) is the *prior-weighted* class-conditional offset, so that Σ_k π_kB h_k = 0 by construction. Then

    μ_B − μ_A = ḡ + Σ_k (π_kB − π_kA) m_kA .                                   (5)

The second term is the change in the mixture of the source class means; it is present even when nothing about the class-conditional distributions changes. Under the constraint the h_k do not enter the mean at all — they enter the class-conditional placement, which is where the residual of Section 4.9 comes from. Subtracting μB − μA therefore removes two things at once: the prior-weighted class-conditional offset and the prior-induced mixture term. On a balanced design the second term vanishes; when the priors change it does not."""))

# ---------- 4.3 multiclass note ----------
R.append((
"""The projected statistic z_w of Equation (2b) does not fail the test by construction:""",
"""The orthogonality in this experiment is defined with respect to w, which is the binary case; for K > 2 the direction that leaves the decision unchanged is the null space of P W, and we did not run the multiclass version of the control. This is a limitation of the experiment, not of the statistic, which is defined through P W for any K.

The projected statistic z_w of Equation (2b) does not fail the test by construction:"""))

for a, b in R:
    if a not in s:
        print("MISS:", a[:60].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("written", n0, "->", len(s), "| abstract:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
