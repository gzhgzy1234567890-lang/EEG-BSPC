# Submission readiness checklist (optimised package)

## Files

| item type | file | note |
|---|---|---|
| Manuscript | `Revised_Manuscript.docx` / `.pdf` | 17 pages, 7,015 body words, 5 figures, 8 tables |
| Supplementary Material | `Revised_Supplementary.pdf` | 34 pages, S1-S37 (S37 holds the four proofs) |
| Highlights | `Revised_Highlights.docx` | 5 items, 60-77 characters |
| Cover Letter | `Revised_Cover_Letter.pdf` | 1 page |
| Graphical Abstract | `Figures/Graphical_Abstract_BSPC.pdf` | unchanged |

## Before pressing submit

- [ ] open the merged PDF; check Tables 1-8, Figs 1-5 and the equations render; Table 7 is the evidence table at the end of Results and Table 8 the mechanism matrix at the start of the Discussion;
- [ ] approve the PDF;
- [ ] confirm commit `ef8c890` is reachable (it is an ancestor of origin/main and holds every result cited).

## Numbers all documents must agree on

| quantity | value | where |
|---|---|---|
| full past-only correction on sleep-EDF | -0.1023 [-0.1145, -0.0900], 32/32 | §4.6, abstract, cover letter |
| composition term (anchored) | -0.0715 [-0.0792, -0.0635] | §4.6, abstract |
| within-class term | +0.0202 [+0.0151, +0.0252] | §4.6, abstract |
| unmatched residual | -0.0148 | §4.6, S36 |
| reconstruction error | 2.7e-14 | §4.6, S36 |
| composition alone vs floor | 0.0097 against 0.0034 | §4.7, abstract |
| drift alone | 0.0172 and 0.0601 | §4.7, abstract |
| measured optimum strength | 0.6 [0.5, 0.8] with composition; 0.8-0.9 without | §4.7 |
| SEED gain | +0.214 archived, +0.236 recomputed | §4.4 |
| sleep memory sweep | -0.1138 / -0.1057 / -0.1023, no sign change | §4.4 |
| grasp artefact | -0.108 sorted, +0.001 in order | §4.5 |

## Open risks

1. Length is now 7,015 body words; the third-party index reports a 5,000-word figure for this journal and the official
   guide could not be reached from this environment (HTTP 403). The paper was not cut below 6,500 because that would
   remove evidence.
2. No independent end-to-end replication; the SEED archived figure cannot be regenerated exactly.
3. Sleep-EDF remains a within-recording result.