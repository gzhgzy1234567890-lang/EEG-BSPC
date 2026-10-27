# -*- coding: utf-8 -*-
"""v10c: replace the inserted definitions table with a list (numbering), and
finish the protocol/procedure/discussion edits."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)
R = []

# ---------- definitions table -> list ----------
R.append((
"""**Table 2.** The two statistics, and what each one needs.

| symbol | definition | inputs | role |
|---|---|---|---|
| z_T | ‖μ_A‖ / ‖sd_A‖ | source features | naive origin distance; direction-blind (Section 4.3) |
| z_w | ‖P W μ_A‖ / (√K σ_s) | source features and fitted weights | source-only screen recommended here |
| ρ | ‖P W μ_B‖ / (√K σ_s) | target features, no labels | the displacement that carries the mechanism |
| s | w'μ_A / σ_s (binary) | source features and fitted weights | signed displacement of the one-sided relative to the two-sided pipeline |

**The size.**""",
"""Four quantities are used below, and they differ in what they need. The *origin distance* z_T = ‖μ_A‖/‖sd_A‖ uses the source features only and is direction-blind (Section 4.3). The *projected screen* z_w = ‖P W μ_A‖/(√K σ_s) uses the source features and the fitted weights. The *displacement* ρ = ‖P W μ_B‖/(√K σ_s) uses the target features and carries the mechanism, and its signed binary counterpart is s = w'μ_A/σ_s. All three are scale-invariant in the features, since numerator and denominator scale together.

**The size.**"""))

# ---------- 3: SEED dependence + 2b pair levels ----------
R.append((
"""*SEED* [14,15]: three emotion classes, 62 channels, 15 subjects, three sessions on different days; the distributed 1 s differential-entropy features, 3394 segments per session in 15 film-defined blocks. The reference uses `StratifiedGroupKFold` with the film as group.""",
"""*SEED* [14,15]: three emotion classes, 62 channels, 15 subjects, three sessions on different days; the distributed 1 s differential-entropy features, 3394 segments per session in 15 film-defined blocks. The reference uses `StratifiedGroupKFold` with the film as group, because adjacent segments of one film are not independent; the *target mean* used by the correction is computed over all 3394 segments of the session, without any grouping, since it is a first moment and not an estimate of generalisation. The same films appear in different sessions, so a film-level dependence remains in the sense that the two sessions share stimuli; we do not model it and report SEED's screening result (Section 4.4) as the failure case it is."""))

R.append((
"""The three pair types do not contribute equally to a possible feedback confound, so we report the gain separately: 1→2 (screening only) +0.0308, 1→3 +0.0247, 2→3 +0.0433; the effect is not carried by the sessions that introduce feedback.""",
"""The three pair types do not contribute equally to a possible feedback confound, so we report both levels and the gain for each: 1→2 (screening only) 0.6461 → 0.6769, gain +0.0308; 1→3 0.7430 → 0.7677, +0.0247; 2→3 0.7247 → 0.7680, +0.0433. The gains are of the same size across the three types, and the differences in level reflect how well each session decodes in the first place; the effect is not carried by the sessions that introduce feedback."""))

# ---------- 5 procedure: screening ----------
R.append((
"""**Step 1 — project the source mean onto the classifier's direction.** z_w = ‖P W μ_A‖/(√K σ_s) requires nothing but the training session: the fitted weights, the source mean and the score spread. In our units, below z_w = 0.35 the penalty of the one-sided form is between +0.024 and −0.015; above z_w = 0.9 it is between −0.03 and −0.19. These ranges are descriptive of the eleven units studied, not validated thresholds: treat the statistic as a triage, not a test. Do not use the norm-based z_T for this purpose; Section 4.3 shows it is unchanged by a translation that can destroy the decoder.""",
"""**Step 1 — project the source mean onto the classifier's direction.** z_w = ‖P W μ_A‖/(√K σ_s) requires nothing but the training session: the fitted weights, the source mean and the score spread. In our units, below z_w = 0.35 the penalty of the one-sided form is between +0.024 and −0.015; above z_w = 0.9 it is between −0.03 and −0.19. Across all 845 cells the statistic separates a loss larger than 0.05 from the rest with an AUC of 0.84 (Section 4.4). These are descriptive operating characteristics of the eleven units studied, not validated thresholds: use the statistic to triage a feature family, not to certify that a particular representation is safe — the four BCI-2a representations have almost the same z_w and penalties that differ by 0.21. Do not use the norm-based z_T at all; Section 4.3 shows it is unchanged by a translation that can destroy the decoder."""))

# ---------- 6.4 limitations: screening failures ----------
R.append((
"""**The screen is a proxy.** Section 4.3 shows that a norm-based statistic is unchanged by an origin that is orthogonal to the weights and that does nothing; the projected statistic z_w does not have that failure by construction, but it remains an empirical proxy rather than a law. Five datasets, with a leave-one-dataset-out fit that is compressed, are not enough to certify a threshold, and the decision-space displacement is the quantity with the mechanism.""",
"""**The screen is a proxy, and it fails in two reported cases.** Section 4.3 shows that a norm-based statistic is unchanged by an origin orthogonal to the weights that does nothing; the projected statistic z_w does not have that failure by construction, but it remains an empirical proxy. It separates a severe loss with an AUC of 0.84 across cells and 0.83–0.86 within BCI-2a, BCI-2b and grasp-and-lift, but it cannot resolve the four BCI-2a representations (z_w 0.285–0.325, penalties +0.024 to −0.184) and its within-SEED ordering is inverted (AUC 0.332). Five datasets, with a leave-one-dataset-out fit that is compressed, are not enough to certify a threshold, and a sixth dataset that played no role in choosing the statistic has not been tested."""))

for a, b in R:
    if a not in s:
        print("MISS:", a[:60].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
