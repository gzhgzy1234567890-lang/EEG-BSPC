# Align, don't zero

Code and results for

> **Align, don't zero: consistent feature centring for cross-session EEG decoding**

This repository contains the analysis pipeline, the independent re-implementation used for
reproduction, the feature builder for BCI-IV-2b, and the raw text output of every number
reported in the paper.

---

## What the paper claims, and where each claim is computed

| Claim | Where |
|---|---|
| The two centring conventions differ in score by exactly `wᵀμ_T` | `src/paper_numbers.py` (Eq. 4 is algebra) |
| Centring on zero collapses 3 of 4 feature sets of BCI-IV-2b to chance | `src/paper_numbers.py` |
| Aligning improves balanced accuracy in 9/9 subjects on both datasets | `src/paper_numbers.py` |
| `z_pool` orders the damage across eight representations | `src/paper_numbers.py` |
| The intervention leaves the other conditions exactly unchanged (576/576) | `src/paper_numbers.py` |
| Alignment is non-inferior to the within-session reference on 2b, not on 2a | `src/paper_numbers.py` |
| The residual is concentrated in protocol-crossing pairs | `src/paper_numbers.py` |
| All of the above reproduce under an independent implementation, four seeds | `src/reproduce.py` |

`src/reproduce.py` shares no feature-extraction or evaluation code with `src/paper_numbers.py`
on purpose. It re-derives log band power, Euclidean-aligned log power, tangent-space features,
CSP log variance and balanced accuracy from scratch, and re-runs six pre-registered claims under
four random seeds. Two claims are included as *directional* checks: the discriminant-projection
descriptor `z_disc` is expected **not** to outperform `z_pool` (it does not, rho = +0.50 against
-0.90), and no mediation is claimed.

---

## A note on a bug that this repository previously contained

An early version of both `paper_numbers.py` and `reproduce.py` estimated `tr(Σ)` as

```python
np.mean(dd ** 2) * h / 4.0        # WRONG: averages over features instead of summing
```

which underestimates `tr(Σ)` by a factor of `2D` — a factor of 176 at `D = 88`. Because the same
expression appeared in both files, the fact that four random seeds agreed did not detect it. A
Monte Carlo with a known covariance confirms the ratio `code/true = 1/(2D)` to three digits; the
correct estimator is

```python
np.sum(dd ** 2) * h / 2.0         # E[sum_j dd_j^2] = 2 tr(Σ) / h
```

The correction reverses the conclusion of the paper's former Section 6 on shrinkage: with an
unbiased noise estimate the excess energy is small enough that full subtraction beats every
shrunken weighting, and that section has been removed. If you are re-using the shrinkage code
from an earlier version, do not.

A second bug affected the CSP representation: with 3 channels and `m = 3`,
`idx[:m]` and `idx[-m:]` select the same three eigenvectors, so the "6-dimensional" CSP feature of
the 3-channel dataset was three filters each counted twice. The fix caps the number of filters at
`ch // 2`.

---

## Data

Both datasets are public and are **not** included here.

**BCI Competition IV 2a** — nine subjects, four motor-imagery classes, 22 EEG channels.
Download `A01T.mat` … `A09T.mat` and `A01E.mat` … `A09E.mat` from
<https://www.bbci.de/competition/iv/#dataset1> into one directory:

```
$BSPC_DATA/BCICIV-2a-mat/A01T.mat
$BSPC_DATA/BCICIV-2a-mat/A01E.mat
...
```

**BCI Competition IV 2b** — nine subjects, two motor-imagery classes, three bipolar channels.
Download the 45 `.gdf` files (`B0101T.gdf` … `B0905E.gdf`) from
<https://www.bbci.de/competition/iv/#dataset2>:

```
$BSPC_DATA/BCICIV-2b/B0101T.gdf
...
```

### Session structure of 2b, read from the files

The event codes matter and are worth stating, because the dataset is often described as having
"three screening sessions". It does not:

| Session | Trials | Labels (769/770) | Feedback marker 781 |
|---|---|---|---|
| 01T | 120 | 60 / 60 | 0 |
| 02T | 120 | 60 / 60 | 0 |
| **03T** | **160** | **80 / 80** | **160** |
| 04E, 05E | 160 | withheld | 160 |

So 01T and 02T are screening sessions, **03T is a feedback session**, and only 04E/05E lack
labels. Of the 27 ordered cross-day pairs, nine (01T→02T) differ only in recording date and
eighteen (01T→03T, 02T→03T) also cross the introduction of feedback. The paper reports them
separately; the residual against the within-session reference is +0.009 for the first group and
-0.028 for the second.

---

## Running it

Python 3.7 was used; nothing newer is required.

```
numpy==1.21.6  scipy==1.7.3  scikit-learn==1.0.2  matplotlib==3.5.3  mne==1.3.1
```

`mne` is needed only to read the GDF headers in the optional Step 1.

**Step 0 — point the scripts at your data.** Three optional environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `BSPC_DATA` | `E:\data` | directory containing `BCICIV-2a-mat/` and `BCICIV-2b/` |
| `BSPC_CACHE` | `<repo>/features/cache_2b` | where the 2b feature cache lives |
| `BSPC_OUT` | `<repo>/results` | where outputs are written |

**Step 1 — the 2b feature cache is already here.** `features/cache_2b/` contains the 27
session-level `.npz` files (26 MB) that Step 2 reads, so you can skip this step. To rebuild them:

```bash
python src/make_features_2b.py
```

**Step 2 — compute every number in the paper:**

```bash
python src/paper_numbers.py          # ~1 min
```

**Step 3 — reproduce independently:**

```bash
python src/reproduce.py              # ~2 min, four seeds
```

**Step 4 — regenerate both figures:**

```bash
python src/make_figures.py
```

All scripts write plain text; nothing is hidden behind a plotting call. Compare your output
against `results/`.

---

## Repository layout

```
src/paper_numbers.py       main pipeline: features, tables, figures, all reported numbers
src/reproduce.py           independent re-implementation + six pre-registered claims
src/make_features_2b.py    GDF -> feature cache
src/make_figures.py        figure assembly
features/cache_2b/         27 session-level .npz files for BCI-IV-2b
results/                   raw text output, one file per script
figures/                   Figure 1 and Figure 2 as submitted
```

---

## License

MIT. See `LICENSE`.
