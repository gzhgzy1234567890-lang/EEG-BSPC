# -*- coding: utf-8 -*-
"""Round 3b: report the (small) code audit honestly."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)

old = """**Prevalence is not measured.** We do not know how often one-sided centring occurs in released code, and we put no number on it. What we show is that the conventions differ in an invariance they do or do not possess, that the difference is large enough to be worth checking, and that the check is free. A reader who believes the one-sided form is rare should read the paper as a statement about origin dependence rather than about prevalence; the recommendation survives that reading."""

new = """**Prevalence is measured only anecdotally.** We inspected one published cross-session example in detail — the MOABB cross-session motor-imagery script, which evaluates CSP+LDA and Riemannian tangent space + logistic regression with leave-one-session-out [18]. Neither pipeline centres the target at prediction time, and every transform is fitted inside the training fold. The example is therefore equivariant by construction and cannot exhibit the failure this paper is about. That is the correct way to build a cross-session pipeline, and it is also the reason the ambiguity is invisible in framework code: the framework fixes the reference to the training fold. The exposure is in pipelines that add a normalisation step at prediction time, outside the fold, which is what Section 1 describes and what the unit test of Section 5 detects. We have not surveyed that population, and we put no number on its size. A reader who believes the one-sided form is rare should read the paper as a statement about origin dependence rather than about prevalence; the recommendation survives that reading, and the unit test is the cheap way to settle the question for any particular codebase."""

if old not in s:
    print("MISS limitations")
s = s.replace(old, new)

old2 = """A reader may reasonably ask why the algebra of two conventions deserves a paper."""
new2 = """The two forms are not equally common in practice, and the reason is instructive: a framework that fits every transform inside the training fold never has to choose, because the reference is the fold; a custom pipeline that patches a normalisation step at prediction time does have to choose, and usually does so without saying which one it chose (Section 6.4).

A reader may reasonably ask why the algebra of two conventions deserves a paper."""
if old2 not in s:
    print("MISS intro")
s = s.replace(old2, new2)

# add the reference
old3 = "[17] F. Lotte, L. Bougrain"
new3 = "[18] S. Chevallier, A. Barachant, et al., MOABB: a framework for reproducible EEG-based brain-computer interface research, in: Cross-Session Motor Imagery example, NeuroTechX/moabb, 2024. https://github.com/NeuroTechX/moabb\n\n[17] F. Lotte, L. Bougrain"
if old3 not in s:
    print("MISS refs")
s = s.replace(old3, new3, 1)
# reorder: 17 should come before 18; the replace put 18 before 17, fix by swapping blocks
s = s.replace("""[18] S. Chevallier, A. Barachant, et al., MOABB: a framework for reproducible EEG-based brain-computer interface research, in: Cross-Session Motor Imagery example, NeuroTechX/moabb, 2024. https://github.com/NeuroTechX/moabb

[17] F. Lotte, L. Bougrain, A. Cichocki, M. Clerc, M. Congedo, A. Rakotomamonjy, F. Yger, A review of classification algorithms for EEG-based brain-computer interfaces: a 10 year update, J. Neural Eng. 15 (2018) 031005.""",
"""[17] F. Lotte, L. Bougrain, A. Cichocki, M. Clerc, M. Congedo, A. Rakotomamonjy, F. Yger, A review of classification algorithms for EEG-based brain-computer interfaces: a 10 year update, J. Neural Eng. 15 (2018) 031005.

[18] MOABB developers, Cross-session motor imagery example (CSP+LDA and Riemannian geometry + logistic regression, leave-one-session-out), NeuroTechX/moabb, 2024. https://github.com/NeuroTechX/moabb""")

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
