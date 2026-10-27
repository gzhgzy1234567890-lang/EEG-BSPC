# -*- coding: utf-8 -*-
"""v17: add the code audit, merge the two law tables, fix the figure caption."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v16.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)

# ---------- 1. merge Tables 7 and 8 ----------
start = s.find("**Table 7.** Per-cell prediction")
end = s.find("The oracle parameterisation fits well")
if start < 0 or end < 0:
    print("MISS law tables")
else:
    merged = """**Table 7.** Per-cell prediction of Equation (4) under the two parameterisations. For BCI-2a the cells are the two-class subproblem of classes 1 and 2. `MAE` is the mean absolute difference between prediction and observation on the same cell; `r` is Pearson; `sign` and `base` are the sign accuracy and the majority-class rate under the oracle parameterisation; `BA gap` is the mean absolute difference between the model's implied accuracy Φ(c) and the observed aligned accuracy under the model parameterisation.

| dataset | classifier | n | oracle r | oracle MAE | oracle sign (base) | model r | model MAE | BA gap |
|---|---|---|---|---|---|---|---|---|
| BCI-2b | LDA | 108 | 0.989 | 0.0130 | 0.917 (0.815) | 0.861 | 0.0567 | 0.096 |
| BCI-2b | logistic | 108 | 0.990 | 0.0127 | 0.889 (0.769) | 0.852 | 0.0578 | 0.098 |
| BCI-2b | SVM | 108 | 0.381 | 0.0224 | 0.676 (0.528) | 0.655 | 0.0203 | 0.107 |
| BCI-2a | LDA | 36 | 0.902 | 0.0320 | 0.889 (0.833) | 0.874 | 0.0414 | 0.149 |
| BCI-2a | logistic | 36 | 0.885 | 0.0330 | 0.750 (0.750) | 0.824 | 0.0563 | 0.128 |
| BCI-2a | SVM | 36 | 0.610 | 0.0161 | 0.611 (0.528) | 0.711 | 0.0217 | 0.095 |
| grasp-and-lift | LDA | 336 | 0.649 | 0.0360 | 0.693 (0.604) | 0.271 | 0.0420 | 0.213 |
| grasp-and-lift | logistic | 336 | 0.592 | 0.0364 | 0.649 (0.607) | 0.531 | 0.0355 | 0.212 |
| grasp-and-lift | SVM | 336 | 0.353 | 0.0115 | 0.420 (0.292) | 0.191 | 0.0127 | 0.248 |
| NER2015 | LDA | 320 | 0.385 | 0.0285 | 0.556 (0.406) | not estimable | — | — |
| NER2015 | logistic | 320 | 0.371 | 0.0258 | 0.509 (0.425) | not estimable | — | — |
| NER2015 | SVM | 320 | 0.458 | 0.0434 | 0.666 (0.503) | not estimable | — | — |

"""
    s = s[:start] + merged + s[end:]

# ---------- 2. figure 1 caption ----------
s = s.replace("The equivariant pipelines change by 0.0e+00 in every cell at every setting.",
              "The equivariant pipelines change by 0.0e+00 in every cell at every setting; the one-sided pipeline decays toward 1/K without reaching it uniformly within the sweep.")

# ---------- 3. the code audit subsection ----------
anchor = "## 5. The audit procedure"
audit = """### 4.11 A small audit of released preprocessing components

The paper's practical premise is that a pipeline can be built with a reference
that is fixed at prediction time. We inspected the components of three widely
used frameworks that a cross-session pipeline actually uses, and recorded which
data each one takes its reference from.

**Table 9.** What the inspected components centre on. Quoted lines are from the
public sources; the audit is small and reported as such (`results/code_audit.txt`
in the archive).

| component | what it does | reference taken from | exposed at prediction time? |
|---|---|---|---|
| MOABB cross-session example [18] | `CrossSessionEvaluation` with CSP+LDA and tangent-space+logistic pipelines | every transform is fitted inside the training fold | no |
| MNE `Scaler` [mne/decoding/transformer.py] | wraps scikit-learn `StandardScaler`; `fit` then `transform` | the data passed to `fit`, i.e. the training fold | no |
| Braindecode `exponential_moving_demean` [braindecode/preprocessing/preprocess.py] | causal exponential moving average, initialised from the first block of each trial | the signal up to the current sample | no, if the running window covers the session offset |

None of the three centres the target session at prediction time, and all three
therefore satisfy the invariance of Proposition 1 by construction: the reference
is the training fold, or a causal running mean that sees the session offset as
part of the signal. The failure mode audited in this paper is consequently not
present in the framework components we inspected; it belongs to code that
patches a normalisation step onto features at prediction time, outside the fold.
We did not audit that population, and the audit above is too small to estimate
its size.

## 5. The audit procedure"""
if anchor not in s:
    print("MISS audit anchor")
s = s.replace(anchor, audit, 1)

# renumber the later tables (the old Table 9 variants, Table 10 calibration)
s = s.replace("**Table 9.** Alternatives to the mean correction.", "**Table 10.** Alternatives to the mean correction.")
s = s.replace("**Table 10.** Calibration, LDA, every development cell;", "**Table 11.** Calibration, LDA, every development cell;")

# ---------- 4. limitations: the audit is done, small ----------
s = s.replace("""**Prevalence is measured only anecdotally.** We inspected one published cross-session example, the MOABB cross-session motor-imagery script, which evaluates CSP+LDA and Riemannian tangent space + logistic regression with leave-one-session-out [18]. Neither pipeline centres the target at prediction time and every transform is fitted inside the training fold, so the example is equivariant by construction and cannot exhibit the failure. That is the correct way to build a cross-session pipeline, and it is why the ambiguity is invisible in framework code. We have not surveyed the population of custom pipelines that patch a normalisation step at prediction time, and we put no number on its size. A systematic audit is the natural next study, and the invariance test of Section 5 is the instrument it would use.""",
"""**Prevalence is measured on three components, not on the field.** Section 4.11 audits the MOABB cross-session example, the MNE `Scaler` and the Braindecode causal demean; all three take their reference from the training fold or from a causal running mean, so none of them can exhibit the failure, and we put no number on the frequency of the mistake in custom code. The audit is small by design: it establishes that the failure is an implementation choice and not a property of the frameworks, and the invariance test of Section 5 is the instrument that would settle any particular codebase.""")

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
