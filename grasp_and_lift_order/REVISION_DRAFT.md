# V9 revision draft — grasp-and-lift correction

Prepared 31 October 2026 from `GRASP_AND_LIFT_ORDER_AUDIT.md`. This file contains the replacement text for
every claim that depends on the grasp-and-lift cache; it has **not** been applied to the DOCX yet, because
the figures and two tables have to be replaced in the same pass.

## 1. What was wrong

The published cache (`cache_gal`) stores the trials **sorted by class**: in all 96 series the labels are
28 or 34 zeros followed by the same number of ones, with the switch at exactly half the file. The raw
recordings have 28-34 HandStart trials each and two samples per trial, so the acquisition order is
`0 1 0 1 ...`, not `0 0 ... 0 1 1 ... 1`.

Rebuilt in acquisition order with the same features (2 s before / 2 s after HandStart; 32 channels;
0.5-30 Hz; log power in 8 x 250 ms windows), the same estimator gives:

| cache | BA(lambda = 0 -> 1) | delta | subjects negative |
|---|---|---|---|
| published (class-sorted) | 0.7727 -> 0.6652 | **-0.1075** | 12 of 12 |
| rebuilt features, class-sorted (control) | 0.7925 -> 0.7025 | -0.0901 | 12 of 12 |
| rebuilt features, acquisition order | 0.7874 -> 0.7889 | **+0.0014** | 6 of 12 |

The control isolates the cause: identical features, identical estimator, only the storage order changes.
With the true order every subject lies within [-0.016, +0.020].

The other four caches are not sorted (SEED: 12 class switches in 3,394 segments; BCI-2b: 51-57 switches per
session; NER2015: 18-26), so their results stand.

## 2. New abstract (replace paragraph 8)

> Mean correction is a routine first step in cross-session EEG decoding, yet removing an estimate of the
> target mean can help or hurt classification. We separate three questions - whether a displacement reaches
> the decision, how much is removed, and what the estimated mean contains - on five public benchmarks and
> two held-out cohorts. For a fixed affine decoder only the component of a displacement that projects onto
> the centred classifier weights can change a score difference, an exact condition for a correction to be
> harmless. The sign is a property of the benchmark: full-strength past-only correction gains 0.214 balanced
> accuracy on SEED and about 0.03 on two motor-imagery datasets, while on sleep-EDF, a task the analysis
> never touched, it loses 0.102, with all 32 subjects and all 45 recordings negative. A sixth comparison
> looked like a second negative case until its cache was audited: the stored trials were sorted by class, a
> construction that manufactures a loss of 0.108 (12 of 12 subjects negative) which falls to +0.001 when the
> same features are stored in acquisition order. The cause of the genuine loss is not identified: class
> composition covaries with time in every dataset used here, and a cell-level partial correlation leaves no
> residual association. An external cross-day cohort (Lee2019-MI, 54 subjects) is positive under the executed
> window (sign test p = 0.027) but not under the development pipeline (+0.010, p = 0.10), so a positive gain
> is not established. Past-only mean correction can help or hurt; the conditions that decide which are not
> yet identified, and trial order in a cache is one of them.

## 3. New overview (replace paragraph 57)

> **Overview of the findings.** Within a single recording, full-strength past-only mean correction can be
> harmful: on sleep-EDF - a task the analysis never touched - it lowers balanced accuracy by 0.102 over 4,983
> cells, negative in all 32 subjects and in all 45 recordings (Section 4.7). It can also help: SEED gains
> 0.214 and the two motor-imagery datasets about 0.03. A third within-recording benchmark, grasp-and-lift,
> was the paper's original negative case; after its cache was rebuilt in acquisition order the effect
> disappeared (+0.001, Section 4.5), and the class-sorted storage that produced the original -0.108 is now
> reported as a methodological result in its own right. The cause of the sleep-EDF loss is not identified:
> class composition covaries with time, and a cell-level partial correlation leaves no residual association
> (Section 4.6). The external cross-day cohort is positive under the executed window but not under the
> development pipeline (+0.010, p = 0.10), so it establishes no gain (Section 4.7).

## 4. New Section 3 paragraph for grasp-and-lift (replace the dataset sentence)

> Grasp-and-lift: twelve subjects, eight series recorded within one session with the cap left in place.
> Each series contains 28-34 grasp trials; a trial is scored twice, once on the 2 s before the HandStart
> marker (class 0) and once on the 2 s after it (class 1), giving 56-68 samples per series of 32 channels
> and eight 250-ms windows of log power. Samples are stored in acquisition order - the two windows of a
> trial adjacent, trials in the order they occurred. 336 unordered series pairs. This is the same-cap
> control, so it provides a cross-series rather than a cross-day contrast. Section 4.5 reports what happens
> when the same trials are stored sorted by class instead, which is how the cache was first built.

## 5. New Section 4.5 (replace the trend section, its figure and Table 11)

> **4.5. Trial order in the cache, and a negative transfer that was an artefact of it.**
>
> The comparison in Section 4.4 used a cached feature table in which the samples of each series were stored
> sorted by class. Every one of the 96 series contained 28 or 34 class-0 samples followed by the same number
> of class-1 samples, with the switch at exactly half the file. The recordings do not have that structure:
> they contain 28-34 grasp trials, and the two windows of a trial are adjacent in time.
>
> Rebuilding the same features from the raw recordings and the event files, with the samples in acquisition
> order, changes the result completely. Table 11 reports the three orderings. With the published cache the
> full-strength correction lowers balanced accuracy by 0.108 and every one of the twelve subjects is
> negative; with the same features stored class-sorted the loss is 0.090, again in twelve of twelve; with
> the samples in acquisition order the difference is +0.001, and six subjects improve while six worsen
> (range -0.016 to +0.020). The strength curve is flat to within 0.004 at every setting of lambda.
>
> The mechanism is straightforward and has nothing to do with EEG non-stationarity. In the sorted order the
> target sequence changes class once, at its midpoint, so a running mean over blocks of 15 carries a large
> class-prior step in the second half of every cell and the correction moves the scores away from the
> minority class. In acquisition order every block of 15 covers about seven trials and contains both
> classes, so the running mean is close to zero and the correction is nearly inert. The block-composition
> analysis of Section 4.6 describes this structure exactly; its subject is the cache, not the recording.
>
> The remaining grasp-and-lift numbers computed on the sorted cache - the estimator comparison of Section
> 4.2, the ablation of Section 4.3.1, the interaction term and the trend association previously reported in
> this section - are withdrawn and are being recomputed on the acquisition-order cache. They are not used
> for any claim in this version.

Table 11 (replacement, 3 rows):

| cache | BA at lambda = 0 | BA at lambda = 1 | delta | subjects negative |
|---|---|---|---|---|
| published cache (class-sorted) | 0.7727 | 0.6652 | -0.1075 | 12 of 12 |
| same features, class-sorted | 0.7925 | 0.7025 | -0.0901 | 12 of 12 |
| same features, acquisition order | 0.7874 | 0.7889 | +0.0014 | 6 of 12 |

Fig. 5 (replacement): two panels - (a) BA against lambda for the three orderings; (b) per-subject delta for
the three orderings, one dot per subject.

## 6. New Section 4.6 opening (replace the first two paragraphs)

> **4.6. What the block composition of the cached grasp-and-lift series shows.**
>
> The composition analysis below was written when the sorted cache was believed to be in acquisition order.
> It describes that cache accurately and it now serves a different purpose: it identifies the structure that
> produced the artefact of Section 4.5, and it shows why the between-subject association reported there
> could not be a mechanism.
>
> [the recorded block count, the two profiles [0, 0.133, 1, 1] and [0, 0, 0.733, 1, 1], the 456 blocks and
> the 0.500 class rate remain as written] ... A composition regressor therefore has no between-subject
> variance to explain; what varied between subjects was where the block boundaries fell relative to the
> fixed switch, which is a property of the sorted cache. This is a statement about identifiability, not
> about importance.

## 7. New conclusion paragraphs (replace 146 and 148)

> The negative side is now supported by one dataset rather than two. Full-strength past-only correction
> lowers balanced accuracy by 0.102 on sleep-EDF, with all 32 subjects and all 45 recordings negative, and
> the sign holds in the subset where the source and target class sets are identical (-0.061, 29 of 32). The
> second negative case, grasp-and-lift, did not survive an audit of its cache: the stored trials were sorted
> by class, which by itself produces a loss of 0.09-0.11 with every subject negative; in acquisition order
> the same features give +0.001. We report that artefact because it is a concrete warning about how easily a
> preprocessing cache can manufacture a negative transfer, and because it is the kind of error that the
> transparency of a frozen protocol does not catch.
>
> The positive side is unchanged and is real but narrower than a first reading suggests: SEED gains 0.214 and
> the two motor-imagery datasets about 0.03, so the sign is a property of the benchmark. The independent
> cross-day cohort does not settle it: +0.032 under the executed window, +0.010 (p = 0.10) under the
> development pipeline. No external gain is claimed. The cause of the sleep-EDF loss is not identified:
> composition and time covary there as they do everywhere in this study, and the design that would separate
> them is a class-order-randomised recording.

## 8. New highlights

- Online mean correction gains 0.214 on SEED and loses 0.102 on sleep-EDF.
- The sleep-EDF loss holds in all 32 subjects and all 45 recordings.
- A class-sorted trial cache manufactured a 0.108 loss that is +0.001 in time order.
- Composition and time are confounded, so the mechanism is not identified.
- A frozen cross-day test gives +0.010 (p = 0.10): no positive gain is established.

## 9. Figures and tables to rebuild

| item | action |
|---|---|
| Fig. 4 (strength curves) | rebuild panel (a)/(b) with the acquisition-order grasp-and-lift curve (flat) instead of the sorted one |
| Fig. 5 (trend vs loss) | **delete**, replaced by the ordering figure above |
| Table 9 (strength response) | gal row -> acquisition-order values (0.7874 -> 0.7889, D = +0.001, 6/12 negative) |
| Table 11 (temporal structure) | **delete**, replaced by the ordering table |
| §4.2, §4.3, §4.3.1 grasp-and-lift numbers | recompute on the acquisition-order cache before anything is claimed |

## 10. What remains valid without change

- Section 2 (theory), Section 3 (other datasets, statistics), Section 4.1, 4.2 (except the gal numbers),
  4.3/4.3.1 (synthetic; unaffected by the cache), 4.4 (except the gal row), 4.7 (sleep-EDF and Lee2019-MI),
  Section 5.1 limitations (with the new paragraph), Data availability.
- The sleep-EDF class-set stratification to be added to S22: identical class sets -0.0608 (29 of 32),
  subset -0.1473 (31 of 32), new class -0.0918 (32 of 32).

## 11. Repository additions needed

`build_gal_time.py`, `make_sorted_control.py`, `gal_order_test.py`, `gal_estimators_order.py`,
`sleep_class_overlap.py` and the three caches' summary files, plus a README entry under "A record of
defects": the cache was class-sorted; the effect it produced is reproduced and quantified.
