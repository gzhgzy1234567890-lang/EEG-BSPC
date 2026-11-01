# Round 008 review — responding to the independent re-review that scored 73

The referee found a mathematical defect that invalidates part of the previous round's headline. It is correct,
it was reproduced before any edit, and the previous 96 is withdrawn.

## The defect, reproduced first

With an unmatched class of mass u in the history, translating every feature by a moves the unanchored composition
term by -u a and the residual by +u a. Reproduced in a standalone check: mix moved from [-0.01 ...] to
[-0.57 ...] under a 3.7 shift while the sum stayed fixed. Revision 2 of the decomposition was therefore reporting
an origin-dependent quantity.

## What was re-run and what changed

| item | before | after |
|---|---|---|
| decomposition | unanchored, mix -0.1257 | **anchored, mix -0.0715 [-0.0792, -0.0635]**, 32/32 negative |
| unmatched residual | -0.0544 | **-0.0148** |
| within-class | +0.0202 | +0.0202 (it was already invariant) |
| reconstruction | 2.6e-14 | 2.7e-14 |
| invariance test | none | anchored terms move < 1e-9, unanchored > 1e-3 under a translation of four |

The ordering survives, the magnitude nearly halves, and the old numbers are kept only as a stated diagnostic.

## The other five items

| referee item | action |
|---|---|
| dense strength grid and uncertainty | eleven strengths, bootstrap intervals on the argmax: 0.8 [0.7, 1.0], 0.9 [0.9, 1.0], 0.6 [0.5, 0.8], 0.9 [0.8, 0.9] against predicted 1.00, 1.00, 0.60, 0.75; the closed form is now called a heuristic for the direction and a strict prediction where the mass is largest |
| methods for the new experiments | new supplement S36: generator, definitions, design, inference unit, checks, boundaries |
| temporal contradiction | abstract no longer claims a shared flip; the crossing is stated as a quarter to a half of a film; the 'whole class episode' reading is explicitly withdrawn; the -0.1129 sign typo is fixed |
| reproducibility | Data availability now cites 6443357; target-only centring is defined; S36 documents the new experiments; the 73-item audit archive is separate from the 10-file submission and that is stated |
| document consistency | evidence table moved to the end of Results (Table 7 now follows Table 6 in reading order); Section 4.8 references for the two-factor audit corrected to 4.11; duplicate S35 removed; supplement and cover letter carry the new title; a three-panel Figure 5 now shows the decomposition, the strength sweep and the memory sweep |
| statistics | inference unit stated (12 subjects, seeds averaged within subject); recall denominators stated |

## Scores after the repairs

| dimension | max | referee | r7 (withdrawn) | r8 |
|---|---:|---:|---:|---:|
| theory boundary | 8 | 7 | 7.5 | 7.5 |
| online decomposition | 22 | 16 | 21.5 | **20.5** |
| factorial | 16 | 12 | 15.5 | 15.5 |
| temporal | 10 | 7 | 9 | 8.5 |
| protocol | 12 | 10 | 12 | 11.5 |
| statistics | 12 | 9 | 12 | 11 |
| reproducibility | 12 | 7 | 11.5 | 10.5 |
| structure | 8 | 5 | 7 | 6.5 |
| **total** | **100** | **73** | ~~96.0~~ | **91.5** |

## Why this is below the 96 bar and stays there

1. **Reproducibility (10.5).** The SEED archived figure still cannot be regenerated exactly; the recomputation
   gives +0.236 against +0.214 and the discrepancy is disclosed rather than resolved. No third-party rerun exists.
2. **Structure (6.5).** 11,787 words; the paper grew by the new figure and methods, and the length target is still
   not met.
3. **Statistics (11).** The factorial and the decomposition are single-corpus; the inference unit is now stated,
   but there is no confirmatory replication.

## Decision

**Major Revision, 91.5/100.** The 96 recorded in round 7 depended on a decomposition that was not origin-invariant;
it is struck from the history rather than quietly revised.
