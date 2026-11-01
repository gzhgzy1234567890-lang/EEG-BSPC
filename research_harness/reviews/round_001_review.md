# Round 001 review — after Tasks A, B and C

Version: manuscript BSPC_Candidate_V8.docx (20 pages, 9 tables) plus four new evidence documents:
ONLINE_DECOMPOSITION.md, FACTORIAL_2X2.md, TEMPORAL_MEMORY.md, BLOCK_SENSITIVITY_2B.md.
Git: a4c3ff8 (Task A), 0e38816 (Task B), ee7888f (Task C).

## What this round actually executed

| task | experiment | output | status |
|---|---|---|---|
| A | online decomposition of the estimator's own past-only displacement, 4,983 cells, 14,949 blocks | online_decomposition.json, online_decomposition_blocks.json | **done**, reconstruction error 2.6e-14 |
| B | 2x2 factorial (class proportions x drift) on real sleep-EDF statistics, 1,440 runs | factorial_2x2.json, factorial_2x2_rich.json | **done** |
| C | memory x class duration x drift, 2,592 runs; SEED sweep; sleep run lengths | temporal_memory.json | **done** |

## Key numbers produced this round

- full past-only correction -0.1023 [-0.1141, -0.0898], 32/32 negative;
- mix-only -0.1257, within-only **+0.0202** (29/32 positive); shared-class subset full -0.1639;
- factorial: prior change -0.0064 (p=0.001), drift +0.0634 (p=0.0005), interaction +0.0020 (p=0.027);
- |drift| > |composition| gives +0.0398 against -0.0057 when it does not;
- temporal: no-drift floor -0.0033 at 16 blocks, -0.2749 at 1 block with 25-epoch runs; drift 1.0 +0.0216 at 16 blocks;
- SEED crossing between 50 and 100 s of memory; sleep stage runs median 1.5 min, majority class 68 per cent.

## Scores on the fixed 100-point rubric

| dimension | max | score | basis |
|---|---:|---:|---|
| scientific question and theoretical boundary | 8 | 7.5 | theory corrected, Monte Carlo over 27 cells, claims bounded; the Gaussian model is still the only analytic case |
| online mechanism decomposition | 22 | 21 | exact reconstruction, same estimator, five conditions, shared-class subset, oracle clearly labelled |
| controlled mechanism intervention | 16 | 14.5 | 2x2 with real statistics, controls, 20 seeds, interaction, score-space criterion; generator is Gaussian |
| temporal-scale explanation | 10 | 8 | SEED sweep and two controlled grids; the link to the real corpora remains correlational |
| data protocol and reliability | 12 | 11 | grasp cache audit, 2x2 causal filter audit, boundaries stated |
| statistical rigour | 12 | 11 | subject-level inference, intervals, evidence tiers, non-additivity reported |
| reproducibility | 12 | 10 | code, JSON and seeds archived; no third-party replication; SEED and grasp rows not machine-traced |
| structure and expression | 8 | 5 | **the three new results are not yet in the manuscript**; length 11,595 words; title unchanged |
| **total** | **100** | **88** | |

## Hard gates

| gate | status |
|---|---|
| no fabricated data | pass |
| core results traceable | pass for the new ones; 2 of 7 Table 9 rows still untraced |
| no undisclosed leakage | pass (oracle labels used only for diagnosis, stated) |
| decomposition consistent with the estimator | **now pass** (was failing before Task A) |
| reconstruction exact | pass (2.6e-14) |
| oracle not sold as deployable | pass |
| observational not sold as causal | pass |
| contrary results not hidden | pass |
| cells not treated as subjects | pass |
| numeric contradictions | pass |
| grasp artefact not sold as EEG transfer | pass |
| sleep not sold as cross-day | pass |
| all core mechanism experiments present | **A, B, C now present** |

## Decision

**Major Revision.** The evidence base is now complete on the mechanism side, but the manuscript does not yet
contain it: the paper still reports the global decomposition as the mechanism result, has no factorial section and
no temporal-scale section, and its structure and length were not revised. That is why the structure score is 5/8.

## Next round

1. rewrite Section 4.5 around the online decomposition, demoting the global decomposition to a sensitivity check;
2. add Results III (factorial) and Results IV (temporal scale);
3. cut 20-25 per cent of the non-core text, moving detail to the supplement;
4. re-title only if the new evidence supports the wording;
5. rebuild the evidence registry and re-run the traceability and consistency checks.
