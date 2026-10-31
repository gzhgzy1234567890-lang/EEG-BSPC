# NOVELTY_MATRIX.md

Built from **full texts** of SPDIM, PRED and NeuroAdapt-Bench (downloaded and text-extracted on 1 November 2026)
and from abstracts for the rest. See RELATED_WORK_VERIFICATION.md for the verification level of every row.

## The papers

### SPDIM — ICLR 2025 (Li, Kawanabe, Kobler)
Source-free unsupervised domain adaptation for EEG. Full text states: "Under label shift, aligning the moments of
the marginal feature distributions **can increase the generalization error** (Bakas et al., 2023)", and that
Riemannian alignment "can compensate for the conditional distribution shifts ... but **hurt generalization under
additional label shifts**". Remedy: one SPD-manifold parameter per target domain, optimised by information
maximisation. Data: public BCI and sleep-staging EEG.

**Overlap.** The qualitative "alignment hurts under label shift" is prior art, twice over (Bakas et al. 2023, as
cited by SPDIM; and SPDIM's own analysis). **Not new in this paper.**

**Difference.** SPDIM operates on second-order SPD structure and proposes a deployable method; it does not derive a
first-order displacement formula, a per-sample stability certificate, or audit filtering and trial order.

### PRED — IJCAI 2026 (Zhang et al.)
Full text read: Subject Shift Detector (policy stability) plus Prototype-guided Shift Correction with a
multi-granular memory; three public datasets; claims plasticity and stability.

**Overlap.** Online adaptation under shift, without subject labels.

**Difference.** PRED proposes a detector and a correction network; this paper reports that the gates we tested do
not work across tasks, and analyses why the displacement, not the detector, decides the sign.

### NeuroAdapt-Bench — MLHC 2026 (Lee et al.)
Full text read: "the evaluated TTA methods yield **inconsistent gains and often degrade performance** under
distribution shift"; optimization-free methods are more stable; T3A is the only method with a positive mean
balanced-accuracy change, largest +18.9 points on CHB-MIT.

**Overlap.** Instability of test-time adaptation on EEG is documented there. This is **corroboration** of our
negative results, and it is cited as such [25].

**Difference.** They benchmark accuracy outcomes of TTA methods on foundation models; we analyse one classical
estimator's displacement in decision space, with a per-sample certificate and a protocol audit.

### Lipton et al., BBSE — ICML 2018
Label-shift estimator, imported, not proposed.

### Bakas et al. (2023) — cited inside SPDIM
Label-shift alignment can increase generalisation error. Not read directly; treated as second-hand prior art. Our
contribution A is explicitly a corollary of this line.

## Candidate contributions

| candidate | prior art | what is actually new | allowed strength |
|---|---|---|---|
| A. Composition contamination of first-order mean correction with a quantitative boundary | Bakas 2023 / SPDIM (label shift); Saerens 2002; Lipton 2018 | the decision-space formula for a mean-correction pipeline (Props 1-3b) including lambda* = b/(b+(2pi-1)a) | **MODERATE**: a corollary, not a new phenomenon |
| B. Per-sample stability certificate and non-identifiability of the gain | margin certificates in robust classification; label-shift identifiability | the certificate for a **correction displacement** (Prop 4) and the demonstration that the gain is not a function of unlabeled data (Prop 5) | **MODERATE**: Prop 4 is an identity; the sign version is open |
| C. Protocol audit: filter causality, alignment reference, trial order, block memory | EEG leakage work; Widmann; MOABB | the 2x2 factorial on one dataset pair, the grasp-and-lift cache-order artefact, and the rule that protocol effects must be decomposed | **MODERATE-STRONG**: the decomposition and the artefact, as far as this audit found, are not published together |

## Forbidden words

"first", "novel", "unprecedented", "state of the art" appear nowhere in the manuscript. The strongest sentence is
"as far as we were able to check, not previously reported together".

## Open verification items

- Bakas et al. (2023) was not read directly.
- Widmann et al. (2015) and MOABB were not re-read this round.
