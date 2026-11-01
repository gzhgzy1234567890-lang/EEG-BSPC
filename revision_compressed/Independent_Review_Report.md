# Independent review of the optimised manuscript — post-fix

Version: `Revised_Manuscript.docx`, **17 pages, 6,846 body words** (title through declarations, excluding the
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
manuscript 17 pages, 8,236 words by Word's count, 6,846 by the declared body definition
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
