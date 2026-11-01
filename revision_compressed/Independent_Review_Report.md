# Independent review of the optimised manuscript — post-fix

Version: `Revised_Manuscript.docx`, **17 pages, 7,015 body words** (title through declarations, excluding the
reference list and table cells), 8 tables, 5 figures; supplement 34 pages, S1-S37.

## What the reviewer found, and what was done

| finding | verdict | fix |
|---|---|---|
| Proposition 1 contradicts Table 1 | **correct** | the uncorrected pipeline is also equivariant; only the one-sided pipeline is not. Rewritten. |
| Proposition 2's 'if and only if' is too strong (median is a counter-example) | **correct** | rewritten as the definition gamma(X + c1) = gamma(X) + c, with mean, median and training reference as examples |
| Proposition 3 names the wrong subspace | **correct** | the condition is F W d = 0, i.e. the null space of F W, not the span of the weights |
| Proposition 4 overreaches across score functions | **correct** | confined to one score function; the cross-function claim is withdrawn |
| proofs were pointed at S2, which is a direction-control study | **correct** | new S37 holds the four proofs |
| factorial called 2x2 but is 2x3 | **correct** | rewritten: composition at 2 levels, drift at 3 |
| optimum interval claimed to touch 1.0 while reported [0.8, 0.9] | **correct** | with composition present both intervals exclude 1.0; without it both include it |
| 'cost 0.0034 [-0.0046, -0.0020]' mixes sign conventions | **correct** | signed change -0.0034, stated as a cost of accuracy |
| Table 8 attributed the memory result to the strength grid | **correct** | the grid varies strength; the memory evidence is the one-to-three-block sweep |
| manifest CSV column misalignment | **correct** | uniform eight columns, commit in every row |
| checker hard-coded a Windows path | **correct** | resolves inputs relative to the archive; verified by unzipping the package and running `audit/submission_check.py` from it |
| no standalone Figure 1-5 files | **correct** | `Figures_main/` added, extracted from the submitted DOCX |
| word-count definition inconsistent | **correct** | the CSV now states the definition and the section sums add to the total |

## Verification after the fixes

```
SUBMISSION CHECK PASS   (16 checks, run from the unzipped archive)
manuscript 17 pages, 8,236 words by Word's count, 7,015 by the declared body definition
supplement 34 pages including the new S37 proofs
```

## Scores

| dimension | max | baseline | pre-fix | post-fix |
|---|---:|---:|---:|---:|
| theory boundary | 8 | 7.5 | 6.0 | **8.0** |
| online decomposition | 22 | 20.5 | 20.5 | 20.5 |
| factorial | 16 | 15.5 | 14.0 | **15.5** |
| temporal | 10 | 8.5 | 8.5 | 8.5 |
| protocol | 12 | 11.5 | 11.5 | 11.5 |
| statistics | 12 | 11.0 | 10.0 | **11.5** |
| reproducibility | 12 | 10.5 | 9.0 | **11.5** |
| structure | 8 | 6.5 | 7.5 | 8.0 |
| **total** | **100** | **91.5** | **80.0** | **94.5** |

The pre-fix column is the reviewer's 80 recomputed on the same rubric: the four wrong propositions cost the theory
dimension two points, the factorial and statistics statements one to one and a half, and the reproducibility
artefacts two and a half.

## What still cannot be closed

| item | reason |
|---|---|
| online decomposition 20.5/22 | one corpus; a second would need new data |
| temporal 8.5/10 | the SEED sweep is archived rather than rerun |
| statistics 11.5/12 | no confirmatory replication |
| reproducibility 11.5/12 | SEED archived figure still not regenerable; no third-party rerun |

## Decision

**Submission-ready at 94.5/100 after these corrections.** No new experiment was run and none is required for
submission; the four open items are stated rather than scored away.
## Part D. Final targeted revision after the second independent review

| finding | fix |
|---|---|
| the stability certificate mixed corrected and uncorrected scores in one inequality | rewritten with s_k(x) uncorrected on both sides, the corrected form stated separately, and the equivalence spelled out. The archived code already used the correct expression, so the empirical claim in the BCI-2b paragraph stands unchanged |
| "even when the displacement is not in the span" | corrected to "not in the null space of F W" |
| S37's Proposition 4 proof argued from within-class ordering | rewritten as [s_c(x+) + a] - [s_c(x-) + a] = s_c(x+) - s_c(x-), which is the one-vs-rest comparison an AUC actually uses |
| abstract described a two-term decomposition | now names all three terms, composition, within-class and unmatched-class, and states the anchoring |
| §4.5 pointed at "Tables 4 and 5" for the acquisition-order values | now points at Table 6, which is the grasp ordering table |
| "never adds them" appeared twice in one paragraph | the duplicate clause is removed |
| Table 8 said a composition-only correction must hurt without a model condition | now reads "must hurt in the symmetric two-class model" |
| cover letter named one AI-assisted panel, the manuscript names two | both now name Fig. 1(a) and Fig. 2(a) |
| checklist still said 16 pages, 33-page supplement, S1-S36 | updated to 17 pages, 34 pages, S1-S37 |
| DOCX core properties carried the old title | updated |

Two audits now run on the final files: the 16-check submission checker (file and numbering level) and a content
audit that tests the things the checker cannot see - the certificate wording, the null-space term, the abstract's
three components, the table cross-reference and the absence of absolute claims. Both pass.

## Part E. What the automated checker cannot see

The 16 checks verify file presence, figure and table numbering, highlight lengths, CSV shape and specific strings.
They cannot tell whether a cross-reference points at the *right* table, which is how "Tables 4 and 5" survived the
earlier round. The content audit above covers the cases that were found; it does not constitute a proof that no
other content error exists, and the independent review is the only check that has caught such errors so far.

## Part F. Final acceptance round

| finding | fix |
|---|---|
| content_audit.py still carried a hard-coded Windows path and failed when run from the unzipped package | rewritten to resolve its inputs relative to the archive; verified by unzipping the delivered ZIP and running both scripts from it |
| Section 2.3 wrote the displacement as two terms without qualification | now qualifies the split to the case where source and target share their class support, names the third term, and points to Section 4.6 |
| Section 4.4 inferred what a longer memory would do from Section 4.7 | the inference is withdrawn: the grid varies correction strength, not memory |
| the Discussion said both protocols estimate the target mean from the whole target session | now separates the transductive batch comparison of Section 4.1 from the block-wise past-only estimator of Sections 4.4 to 4.9 |
| word counts disagreed between the CSV and the manuscript | recomputed from the DOCX; every artefact now states 7,209 body words |
| supplement DOCX and PDF metadata kept the old title | core properties of both files updated |
| Elsevier AI disclosure for the annotated panels | Fig. 1 and Fig. 2 captions now name the tool and version and state that no image content was model-generated |

## Part G. Round after the third independent review

| finding | fix |
|---|---|
| S37 Proposition 1 mixed the two definitions of the mean pipeline and dropped a c | the proof now follows Table 1 exactly: none and mean cancel the shift against the intercepts, the refitted double-centring pipeline is invariant term by term, and zero is the one that fails. The false equality (X_B+c)-(mu_B+c)+(mu_A+c) = X_B-mu_B+mu_A is gone; the corrected line keeps the +c and shows it cancelling against -w'c |
| the within-session reference was called an upper bound while Table 3 shows 0.5355 against 0.6119 | now called a label-informed reference, not a ceiling, with the table cited |
| equations (2)-(6) had been removed but the supplement still cited them | main equations renumbered to (1)-(4) and every supplement citation repointed either to the renumbered equation or to the quantity by name |
| the two S35 tables sat at the end of the supplement after S37 | moved back under their captions in S35 and renumbered Table S9 and S10 to avoid clashing with the main text |
| five datasets announced, six listed | now states five development datasets supplying all 845 cells and a sixth (SEED-IV) used only for the implementation audit |
| Table 8 described the memory mechanism as stationarity | reworded to stability of the displacement over the window plus coverage of the class runs, which is what the sweep tests |

## Part H. After the fourth review

| finding | fix |
|---|---|
| S37's Setting still defined mean as fit on X_A - mu_A, apply to X_B - mu_B + mu_A, which is a third pipeline | the Setting now lists all five pipelines exactly as Table 1 does: none, mean (fit on X_A), dbl (fit on X_A - mu_A), zero, train-only |
| Table 4's fourth method column was headed Eq. (9), an equation that no longer exists | renamed to variance-ratio (Eq. 4) in the main table, and the two supplement tables that used the same header were renamed the same way |
| the AI declaration pointed at an Implementation and AI assistance section that did not exist | a Methods paragraph with that name now sits at the end of Section 3 and states the tool, version, the division of labour and the authors' responsibility; the declaration cites that paragraph by section |
