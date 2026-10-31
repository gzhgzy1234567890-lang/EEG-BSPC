# RELATED_WORK_VERIFICATION.md

Verification level for every work cited in NOVELTY_MATRIX.md. Updated after full texts were obtained for three
papers (1 November 2026).

| work | venue | verification | key statement read |
|---|---|---|---|
| **SPDIM** (Li, Kawanabe, Kobler) | ICLR 2025 | **full text** (25 pages, arXiv 2411.07249 / ICLR camera-ready) | "Under label shift, aligning the moments of the marginal feature distributions **can increase the generalization error** (Bakas et al., 2023)"; Riemannian alignment "can compensate for the conditional distribution shifts ... but **hurt generalization under additional label shifts**"; remedy is a single SPD-manifold parameter optimised with information maximisation |
| **PRED** (Zhang et al.) | IJCAI 2026 | **full text** (9 pages) | Subject Shift Detector based on policy stability plus Prototype-guided Shift Correction with a multi-granular memory; evaluated on three public datasets; claims plasticity and stability |
| **NeuroAdapt-Bench** (Lee et al.) | MLHC 2026 | **full text** (37 pages) | "the evaluated TTA methods yield **inconsistent gains and often degrade performance** under distribution shift"; optimization-free methods more stable; T3A the only method with a positive mean BA change, largest +18.9 points on CHB-MIT |
| Lipton et al., BBSE | ICML 2018 | abstract + standard content | confusion-matrix label-shift estimator |
| Bakas et al. (2023) | cited inside SPDIM | **second-hand** | label-shift alignment can increase generalisation error; not read directly |
| EEG data leakage (2024) | PMC | not re-read this round | leakage channels |
| Widmann et al. (2015) | J. Neurosci. Methods | paywalled | filter artefacts |
| MOABB | docs | not fetched | benchmark harness |

## Consequence for this paper's claims

1. The qualitative claim "alignment can hurt under label shift" is **published twice over** (Bakas et al. 2023 via
   SPDIM; SPDIM's own analysis). The paper must not present it as new, and does not: the related-work paragraph
   attributes it to SPDIM [23].
2. NeuroAdapt-Bench independently documents that TTA gains on EEG are inconsistent and often negative. This is
   **corroboration**, not a threat: our contribution is the mechanism (first-order displacement) rather than the
   observation of instability.
3. What remains ours after the full-text check: the decision-space decomposition for a **mean correction** with the
   optimal-weight formula, the per-sample stability certificate, and the protocol audit (filter vs alignment
   factorial, cache-order artefact).

## What changed versus the abstract-only reading

The abstract-only reading could not tell whether SPDIM analysed mean correction specifically. The full text shows
it analyses **second-order (SPD) alignment** and cites the first-order/label-shift warning to others; it does not
derive a decision-space displacement formula. Contribution B therefore stands, and contribution A is explicitly a
corollary of prior label-shift theory.
