# RELATED_WORK_VERIFICATION.md

Verification level for every work cited in NOVELTY_MATRIX.md. "Abstract" means the official proceedings abstract
page was fetched and read on 1 November 2026; "full text" means the PDF was read.

| work | venue | verification | what was checked |
|---|---|---|---|
| SPDIM (Li, Kawanabe et al.) | ICLR 2025 | **abstract**, proceedings page fetched (HTTP 200) | task (SFUDA for EEG), the claim that Riemannian alignment hurts under label shift, the proposed manifold parameter, the datasets |
| PRED | IJCAI 2026 | **abstract**, proceedings page fetched (HTTP 200) | online EEG decoding, unsupervised subject-shift detection, prototype adaptation |
| NeuroAdapt-Bench | MLHC 2026 (PMLR v340) | **abstract**, page fetched (HTTP 200) | TTA benchmark for EEG foundation models; TTA effectiveness "largely underexplored" |
| Lipton et al., BBSE | ICML 2018 (PMLR v80) | abstract page fetched; the estimator is standard and our use is textbook | confusion-matrix label-shift estimator |
| EEG data leakage (2024) | PMC | page exists; not re-read this round | leakage channels in EEG decoding |
| Widmann et al. (2015) | J. Neurosci. Methods | publisher page is paywalled; not fetched | filter artefacts |
| MOABB | online docs | not fetched this round | benchmark harness |

## Attempted and failed

- ICLR full-text PDF: the fetch tool rejects `application/pdf` ("unsupported content type"), so the full text
  could not be read through it.
- PMLR PDF for NeuroAdapt-Bench: the constructed URL returned 404; the correct PDF path was not resolved.

## Consequence

The novelty claims rest on abstracts plus the standard content of the BBSE estimator. **Full-text verification of
SPDIM, PRED and NeuroAdapt-Bench remains undone** and is recorded as an open item. If SPDIM's full text contains a
decision-space analysis of mean correction, contribution B of this paper would have to be downgraded further; that
risk is stated in NOVELTY_RISK_REPORT.md.
