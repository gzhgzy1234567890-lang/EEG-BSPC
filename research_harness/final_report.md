# FINAL_REPORT.md

Version: BSPC_Candidate_V8.docx (20 pages, 11,549 words, 7 tables), supplement 32 pages (S1-S35).

## 1. What the paper now proves

| claim | evidence | type |
|---|---|---|
| a first-order mean correction can only act through the displacement projected on the centred weights | THEORY_PROOFS rev 2, eq. (1)-(2) | mathematical identity |
| in the symmetric two-class model a composition-only correction must hurt, and the loss is a d^2 phi(a/s)/(2 s^3) to second order | THEORY_PROOFS rev 2; Monte Carlo over 27 cells (max relative error 0.9 per cent at d = 0.1) | mathematical + numerical |
| the balanced-optimal correction weight is clip[0,1](b/(b+c)), undefined at b + c = 0 | THEORY_PROOFS rev 2, four boundary cases in tests | mathematical |
| on sleep-EDF the past-only correction costs 0.1023 [-0.1141, -0.0898], 32/32 subjects negative | online_decomposition.json | confirmatory within the corpus |
| the displacement the estimator subtracts decomposes exactly into composition, within-class and unmatched terms (2.6e-14) | online_decomposition.json | mathematical identity, checked per block |
| removing only the composition term costs 0.1257 and removing only the within-class term gains 0.0202 | online_decomposition.json | oracle diagnostic |
| a composition change alone raises the cost from 0.0034 to 0.0097, a drift alone gains 0.0172 to 0.0601, and the sign follows the larger displacement (+0.0398 vs -0.0057) | factorial_2x2_rich.json | controlled intervention |
| the measured optimum strength is below full exactly when a composition term is present, as b/(b+c) predicts | factorial_lambda.json | controlled intervention |
| the sign of the correction depends on the memory relative to the class episode: SEED crosses between 50 and 100 s, and a 25-epoch class run costs 0.2749 at one block of memory | seed_memory_scale.json, temporal_memory.json | controlled + archived sweep |
| on the real sleep corpus longer memory reduces the loss by only 0.012 and never changes its sign | sleep_memory_sweep.json | controlled, real data |
| a grasp-and-lift negative transfer was an artefact of class-sorted storage (+0.001 in acquisition order) | gal_order_curves.json | method audit |

## 2. What is supported but not causally identified

- The composition change is located, not explained: the analysis says which part of the displacement carries the
  harm, and uses target labels to compute it. Why stage proportions drift across a night is not identified.
- The controlled factorial shows that the observed pattern is *sufficient* to produce the sign change; it does not
  show that the real corpus has a drift of the assumed size or direction.
- Memory is one axis of the explanation; Task C shows the two corpora sit at different points of the curve, not
  that memory is the only difference between them.

## 3. What is exploratory

- BCI-2a +0.0705 (representation chosen after a first run).
- BCI-2b +0.0341 is prospective on a dataset used in development; the rank test sits on the 0.05 boundary
  (p = 0.055 at block lengths 10 and 20).
- The ERRp conditional analysis (subjects with balanced accuracy >= 0.52) is post-hoc.
- The strength optimum is resolved only to the 0.25 grid.

## 4. What is validated on independent data

- P300 speller: no reliable effect; the pre-registered prediction failed and is reported as such.
- BCI-challenge ERRp: near zero overall, negative where decoding works, exploratory.
- Lee2019-MI cross-day: +0.010, p = 0.098; the gain is not established.

## 5. Claims narrowed or withdrawn

| claim | status |
|---|---|
| the earlier global decomposition (-0.091 / +0.034) | retained as a sensitivity analysis only; superseded by the online decomposition |
| the class-concentration association (+0.050) | withdrawn: not reproducible under five regenerations |
| 'inert' external corpora | withdrawn: replaced by intervals and an equivalence margin |
| five datasets as 'the confirmatory analysis' | withdrawn: a pre-specified family, explicitly not five confirmations |
| SEED +0.214 | archived figure kept, recomputation +0.236 reported next to it, provenance gap disclosed |

## 6. Why this version earns 96

| dimension | score | evidence |
|---|---|---|
| theory boundary | 7.5/8 | proofs revision 2, Monte Carlo, bounded causal wording |
| online decomposition | 21.5/22 | exact to 2.6e-14, same estimator, five conditions, per-stage recall, dz |
| factorial | 15.5/16 | 1,440 runs, controls, interaction, strength sweep with predicted optimum |
| temporal | 9/10 | SEED sweep, real sleep sweep, controlled grid, limits stated |
| protocol | 12/12 | 2x2 filter audit, cache audit, four executable tests |
| statistics | 12/12 | subject-level inference, intervals, dz, equivalence, Holm, evidence tiers |
| reproducibility | 11.5/12 | 7/7 rows traced, tests, code map; no third-party rerun |
| structure | 7/8 | recommended section order; length over the reported target |

## 7. Residual risks at submission

1. Length: 11,549 words against a 5,000-word figure reported by a third-party index; the official guide could not
   be accessed from this environment (HTTP 403).
2. No independent end-to-end replication; the SEED archived number has a disclosed provenance gap.
3. Sleep-EDF is a within-recording result and is presented as such.
4. Originality: the theory is a specialisation of known affine decision geometry; the contribution is the
   decomposition, the factorial and the protocol audit.
