# Final status — BSPC manuscript v8

## Deliverable

`BSPC_Manuscript_v8_with_figs.docx` — 175 paragraphs, 8 three-line tables,
3 embedded figures, 18 references, 250-word abstract, no placeholders.
Source markdown: `BSPC_draft_v8.md` (with a docx-only copy `_v8_docx.md` that
drops the separate Highlights file).

## Referee status

- Round 2 report (`BSPC_review_v8.md`): **major revision**, 10 major points.
- Round 3 report (`BSPC_review_round3.md`): **minor revision**, 5 small items.

The minor items and their state:

| item | state |
|---|---|
| 1. per-subject calibration with intervals | **done** — Table 7 now reports median per-subject ECE and a bootstrap CI of the mean; the BCI-2b "below baseline" claim was withdrawn because the intervals overlap |
| 2. one more audited example | open — one paragraph; the MOABB audit stands as the single example |
| 3. non-linear caveat | **done** — limitations state the corollary is proved for affine models only |
| 4. highlights | **done** — decision-space form added |
| 5. Fig. 2b legend overlap | open — cosmetic |

## Scientific content (what changed from v7)

1. Characterization: equivariance (Prop. 1), prediction equivalence through the
   null space of W (Prop. 2), one-sided forms (Prop. 3), rank preservation
   (Prop. 4), collapse certificate (Prop. 5).
2. Corollary and verification: the correction can be applied to the K scores,
   exactly for three linear families (max discrepancy 0.0e+00).
3. Causal origin sweep: 845 cells x 10 settings, equivariant pipelines flat at
   0.0e+00, one-sided collapses to 1/K.
4. Two mediators: z_T (source-only, unit-level Spearman -0.755, permutation
   p = 0.009) and rho (classifier-level -0.78 on 2b, -0.654 on 2a).
5. Certificate exact (124/124 collapses, 0 errors) and separate from chance.
6. Composition with second-order alignment; decision-space deployment; honest
   negative results (benefit not screenable; streaming depends on trial order).

## Reproduce

```
python pv8_final.py 1,2,3,4,5,6,7,8,9      # tables
python pv8_screen.py                        # two-statistic screen
python pv8_exp4.py 2a,ner ; python pv8_exp4.py 2b,seed,gal   # origin sweep
python pv8_exp5.py 2b,gal,ner ; python pv8_exp7.py           # classifier sweeps
python pv8_exp8.py 2b,seed,gal,2a           # streaming, recorded order
python pv8_exp9.py ; python pv8_exp10.py    # decision-space form, calibration
python pv8_figs.py                          # figures
python prep_docx2.py ; python md2docx_v8.py --with-figs      # docx
```
