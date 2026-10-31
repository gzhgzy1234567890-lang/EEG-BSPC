# NOVELTY_MATRIX.md

Built from the abstracts of the named papers, fetched on 1 November 2026 (PMLR page for BBSE, ICLR proceedings
page for SPDIM, IJCAI proceedings page for PRED, PMLR page for NeuroAdapt-Bench). Full texts were not read; where
a claim rests only on an abstract it is marked "(abstract)".

## The papers

### SPDIM — ICLR 2025 (Li, Kawanabe et al.)
Source-free unsupervised domain adaptation for EEG under conditional and **label** shift. The abstract states that
"prior Riemannian statistical alignment methods on the SPD manifold can compensate for specific marginal and
conditional distribution shifts but **hurt generalization under label shifts**", and proposes manifold
optimisation with information maximisation. Data: public BCI and sleep-staging EEG.

**Overlap with this work.** The qualitative claim "alignment under label shift can hurt" is already published
here, for Riemannian alignment. Our claim must not be presented as new in that form.

**Where this work differs.** (i) Object of correction: a first-order mean displacement, not a second-order
Riemannian alignment; (ii) method of analysis: an exact decision-space decomposition and a per-sample stability
certificate, rather than a learned manifold parameter; (iii) scope: a protocol audit (causal vs zero-phase
filtering, trial order) that SPDIM does not study; (iv) SPDIM proposes a deployable method, this paper does not.

### PRED — IJCAI 2026
Prototype-driven online EEG decoding with unsupervised subject-shift detection and soft adaptation boundaries.

**Overlap.** Online adaptation under distribution shift, decided without subject labels, is the same problem
family as the label-free gate studied here.

**Where this work differs.** PRED proposes a detector and an adaptation strategy; our paper reports that the
gates we tested do not work across tasks (a negative result) and analyses why the decision-space displacement, not
the detector output, determines the outcome. No detector is proposed.

### NeuroAdapt-Bench — MLHC 2026
Benchmark of test-time adaptation for EEG foundation models. Abstract: TTA effectiveness "for EEG remains largely
underexplored"; the benchmark evaluates representative TTA methods across foundation models and downstream tasks.

**Overlap.** Instability of adaptation on EEG is part of their scope.

**Where this work differs.** They benchmark existing TTA methods on foundation models with accuracy as the
outcome; we analyse a single classical estimator in decision space, with a per-trial certificate, and audit the
evaluation protocol itself (filter causality, trial order). Different object, different level of analysis.

### Lipton et al., BBSE — ICML 2018
Label-shift detection and correction with black-box predictors, including the confusion-matrix estimator used in
our S33. **No overlap with any claim of novelty here**; the estimator is imported, not proposed.

### EEG data leakage (2024, PMC)
Documents leakage channels in EEG decoding studies. Our trial-order audit is an instance of the same concern; we
do not claim to have discovered the problem class.

### Widmann et al. (2015), EEG filter design
Filter artefacts and their consequences. Our causal-vs-zero-phase contrast is a direct application; the finding
that the two filters differ in amplitude and phase response as well as in future access is theirs, not ours.

### MOABB
A benchmark harness for BCI pipelines. Not a competitor; a candidate platform for replication.

## Candidate contributions of this paper

| candidate | prior art | what is actually new | strength of claim allowed |
|---|---|---|---|
| A. Class-composition contamination of first-order mean correction, with a quantitative failure boundary | label-shift literature (Saerens 2002, Lipton 2018) and SPDIM (label shift hurts alignment) cover the phenomenon | the explicit decision-space formula for a mean-correction pipeline (Props 1-3b), including the optimal correction weight lambda* = b/(b+(2pi-1)a) | MODERATE: a corollary of known label-shift theory applied to first-order correction; not a new phenomenon |
| B. Per-sample prediction-stability certificate and the non-identifiability of the gain | margin-based certificates exist in robust classification; label-shift identifiability is known | the certificate for a **correction displacement** (Prop 4) and the explicit demonstration that the gain is not a function of unlabeled data (Prop 5) | MODERATE: Prop 4 is an identity; Prop 5 is a small counterexample, and the sign-change version is open |
| C. Protocol audit framework: filter causality, EA reference, trial order, block memory | EEG leakage work; Widmann; MOABB | the four-way factorial on one dataset pair, the grasp-and-lift cache-order artefact, and the rule that protocol effects must be decomposed rather than summed | MODERATE-STRONG: the specific decomposition and the documented artefact are, as far as this audit found, not published together |

## Forbidden words

"first", "novel", "unprecedented", "state of the art" are not used anywhere in the paper. The strongest phrase
allowed by this analysis is "as far as we were able to check, not previously reported together".

## Unverified items

- Full texts of SPDIM, PRED and NeuroAdapt-Bench were not read; if their full text contains a decision-space
  correction analysis, contribution B weakens and the paper must say so.
- MOABB's current task coverage was not checked against our datasets.
