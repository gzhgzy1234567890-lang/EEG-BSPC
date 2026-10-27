# Response to round-6 report — minor revision requested

Manuscript v11 (`BSPC_draft_v9.md`, `BSPC_Manuscript_v11_with_figs.docx`).

| referee item | change |
|---|---|
| bound applied to the wrong quantity | both rates now reported: 0/800 for the prediction, 185/800 (23.1 %) for the observation, with the step-function explanation (Section 4.5) |
| multiclass `z_w` definition | Equation (2c) with `D_σ⁻¹`, uncentred convention stated, both invariances checked (1.4e-14, 2.5e-13), centred-vs-uncentred difference reported (Section 2.3, Section 4.10) |
| generalization to a held-out dataset | SEED-IV, opened only after the statistic was fixed: 90 cells, median `z_w` 1.00, penalty −0.070; six-dataset exact p = 12/720 = 0.017; within-SEED-IV AUC 0.482; LODO operating point with sensitivity/specificity/precision (Section 3, Section 4.4, Table 6) |
| label requirements | separated per quantity (Table/paragraph in Section 2.3 and Section 6.4); sign claim restricted; split-sample AUCs with bootstrap intervals; SVM described as unstable |
| Fig. 2 with the held-out point | open — the figure is regenerated during revision |
| Highlights | updated: held-out dataset and within-family failure |
| Table 2 SEED-IV row | corrected from 1.00 (a `z_w` value) to 56.3 (`z_T`) |
| Step 1 ranges | the held-out point at `z_w` = 1.00, penalty −0.070 is now named as support for the upper range |

New scripts: `pv8_seed4.py` (SEED-IV session cache and held-out run),
`pv8_exp17.py` (bound rates, invariances, operating points, split-sample CIs),
`pv8_exp18.py` (held-out statistics and the six-dataset exact test). Their output
is in `results/seediv.txt`, `results/exp17.txt`, `results/exp18.txt`.

Remaining at the time of writing: Fig. 2 does not yet show the SEED-IV point.
