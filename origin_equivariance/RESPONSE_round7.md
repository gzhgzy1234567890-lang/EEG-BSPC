# Response to round-7 report — minor revision requested

Manuscript v12 (`BSPC_draft_v9.md`, `BSPC_Manuscript_v12_with_figs.docx`,
`BSPC_Highlights_v12.docx`).

| referee condition | change |
|---|---|
| apply the development threshold to the held-out dataset | done: threshold t = 0.354 fixed on all five development datasets (development sensitivity 0.811, specificity 0.749, precision 0.544), applied unchanged to SEED-IV: sensitivity 1.000, specificity 0.000, precision 0.544, accuracy 0.544; all 90 cells flagged (Section 4.4, abstract) |
| one unambiguous multiclass `z_w` | Equation (2) is now the matrix definition `‖D_σ⁻¹ P W μ_A‖/√K`; the scalar form is explicitly restricted to K = 2 or equal σ_k and not used elsewhere; the invariance is described as "insensitive to decision-null translations", not as full origin invariance (Section 2.3) |
| 845 vs 935 accounting | new Table 3 lists every analysis with its datasets and cell count; the abstract states 845 development cells and 90 held-out cells separately; Section 3 states the total explicitly and says the 845 are the only cells used for the main analyses and the sweep |
| positioning | title changed to "…what mean correction repairs, and an exploratory screen for feature families"; Section 5 labels the screen exploratory; Section 6.1 states in one paragraph what the paper can and cannot claim |
| minor: Fig. 2 held-out point | added (star at z_w = 1.00, penalty −0.070) |
| minor: highlights | regenerated as `BSPC_Highlights_v12.docx` |

New scripts: `pv8_external.py` (external threshold test), `pv8_fig2.py`
(updated Fig. 2). Output in `results/external.txt`.

Remaining cosmetic: in Fig. 2a the legend sits on a data point; to be moved
during production.
