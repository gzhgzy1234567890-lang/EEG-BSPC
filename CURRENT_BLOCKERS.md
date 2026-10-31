# CURRENT_BLOCKERS.md

| id | blocker | consequence | evidence | resolution path |
|---|---|---|---|---|
| B1 | SEED raw waveforms are not available locally (only ExtractedFeatures 1s/4s) | no strict causal raw-to-feature rerun for SEED; the SEED claim stays at the level of past-only mean estimation on released features | `AUDIT_BASELINE.md`, data listing of E:\data\SEED-all | obtain Preprocessed_EEG (or the 12-subject .cnt set), then re-freeze the five-band protocol |
| B2 | no third-party end-to-end replication | reproducibility section may claim archived-output consistency only, never independent reproduction | REPRODUCIBILITY.md | hand the repository and README to an uninvolved person; record what breaks |
| B3 | BCI-2a euc_ea is exploratory (chosen after seeing a run) | cannot be presented as confirmatory | CLAIM_EVIDENCE_MATRIX.csv | none: report as exploratory; only 2b csp is prospective |
| B4 | BCI-2b dataset was used during development | the 2b test is prospective-in-explored-data, not independent | CLAIM_EVIDENCE_MATRIX.csv | state this in the paper; an independent EEG dataset would be needed for confirmation |
| B5 | filter contrast is lfilter vs filtfilt, not "future access only" | the filter effect cannot be attributed to information access alone | AUDIT_BCI2B_EA.md, protocol Rev B/C | report effective magnitude/phase responses; a matched-response control would be needed to isolate future access |

## Blockers closed this round

- the BCI-2b alignment factor was identically zero because of an absolute whitening floor; fixed by a relative
  floor, re-run, and documented in AUDIT_BCI2B_EA.md.
