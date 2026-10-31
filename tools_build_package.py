# -*- coding: utf-8 -*-
import hashlib, os, shutil, zipfile, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BT = chr(96)
sub = 'G:/Work_work/math/EEG/submit'
pkg = 'G:/Work_work/math/EEG/submit_package'
zip_path = 'G:/Work_work/math/EEG/BSPC_Submission_Package_final.zip'
arch = 'G:/Work_work/math/EEG/archive'
docs = ['BSPC_Candidate_V8.docx','BSPC_Candidate_V8.pdf','BSPC_Highlights_V8.docx','BSPC_Highlights_V8.pdf',
        'COMPOSITION_CONFOUND.md','Cover_Letter_BSPC.docx','Cover_Letter_BSPC.pdf','EXECUTION_TIMELINE.md','GRASP_AND_LIFT_ORDER_AUDIT.md',
        'FINAL_RESULTS_SUMMARY.md','FREEZE_RECORD.md','INDEPENDENT_TEST_DEVIATIONS.md','INDEPENDENT_TEST_PROTOCOL.md',
        'INDEPENDENT_TEST_RESULT.md','OPENBMI_FROZEN_PROTOCOL.md','PAGE_CHECK_LIST.md',
        'PAGE_VISUAL_CHECK.md','PRESUBMISSION_AUDIT.md','PROTOCOL_DEVIATIONS.md','PROTOCOL_SLEEP_TELEMETRY.md','AUDIT_BASELINE.md','AUDIT_BCI2B_EA.md','CLAIM_EVIDENCE_MATRIX.csv','EVENT_AND_WINDOW_AUDIT.md','STATISTICAL_ANALYSIS_PLAN.md','GOAL_ROUND_LOG.md','THEORY_PROOFS.md','THEORY_TEST_RESULTS.md','FINAL_QUALITY_GATE.md','REVIEWER_1_REPORT.md','REVIEWER_2_REPORT.md','CURRENT_BLOCKERS.md','PROTOCOL_CAUSAL_V16.md','REPRODUCIBILITY.md','RESEARCH_PLAN_FOR_ACCEPTANCE.md','REVISION_V9_DRAFT.md','SUBMISSION_CHECKLIST.md',
        'SENSITIVITY_ANALYSIS.md','STATS_VERIFICATION.md',
        'NOVELTY_MATRIX.md','RELATED_WORK_VERIFICATION.md','NOVELTY_RISK_REPORT.md','SLEEP_MECHANISM_AUDIT.md','MECHANISM_LIMITATIONS.md','STATISTICAL_AUDIT.md','EXTERNAL_VALIDATION_REPORT.md','LIMITATIONS_AND_BLOCKERS.md','REPRODUCIBILITY_REPORT.md','MANUSCRIPT_CHANGELOG.md','FILE_PROVENANCE.csv','THEORY_COUNTEREXAMPLES.md','D3_MATCHED_REGENERATION.md','CONCENTRATION_RECONCILIATION.md','C2_CERTIFICATE_RESULTS.md','SEED_RAW_CAUSAL_BLOCKED.md','Supplementary_Material.docx','Supplementary_Material.pdf']
figs = ['Fig_1.png','Fig_2.png','Fig_3.png','Fig_4.png','Fig_S1.png','Fig_S2.png','Fig_S3.png',
        'Graphical_Abstract_BSPC.pdf','Graphical_Abstract_BSPC.png']
import docx as _docx
def highlight_rows():
    d = _docx.Document(os.path.join(sub, 'BSPC_Highlights_V8.docx'))
    out = []
    for p in d.paragraphs:
        s = p.text.strip()
        if len(s) > 20:
            out.append('- %d: %s' % (len(s), s))
    return out[:5]

missing = [f for f in docs if not os.path.exists(os.path.join(sub, f))]
missing += ['Figures/' + f for f in figs if not os.path.exists(os.path.join(sub, 'Figures', f))]
if missing:
    print('MISSING:', missing); sys.exit(1)
if os.path.exists(zip_path):
    shutil.copy2(zip_path, os.path.join(arch, 'BSPC_Submission_Package_final_prev.zip'))
shutil.rmtree(pkg, ignore_errors=True)
os.makedirs(os.path.join(pkg, 'Figures'))
for f in docs:
    shutil.copy2(os.path.join(sub, f), os.path.join(pkg, f))
for f in figs:
    shutil.copy2(os.path.join(sub, 'Figures', f), os.path.join(pkg, 'Figures', f))
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()
files = []
for root, dirs, names in os.walk(pkg):
    dirs.sort(); names.sort()
    for n in names:
        if n == 'MANIFEST.md':
            continue
        full = os.path.join(root, n)
        files.append((os.path.relpath(full, pkg).replace(os.sep, '/'), full))
files.sort()
rows = ['| %s | %d bytes | %s%s%s |' % (rel, os.path.getsize(full), BT, sha(full), BT) for rel, full in files]
head = ['# BSPC submission package', '',
        'Assembled 31 October 2026. Manuscript 18 pages, 9,345 words, 8 tables, 4 figures; supplement 26 pages,',
        'sections S1-S32. The grasp-and-lift negative transfer of',
        'earlier drafts was an artefact of a class-sorted feature cache; Section 4.2 and S32 record the withdrawal.', '',
        '## Manuscript', '',
        '- 9,345 words (Word count; about 8,600 excluding references), 18 pages',
        '- abstract 250 words; 8 tables, 4 figures; supplement 27 pages, sections S1-S33', '',
        '## The independent replication', '',
        '- protocol-consistent run: 45 recordings, 32 subjects, 4,983 cells, -0.102 ([-0.114, -0.090]),',
        '- strict-causality re-run (forward-only filters, state carried): -0.102 ([-0.114, -0.089]), 32 of 32 negative',
        '  32 of 32 subjects negative (p = 4.7e-10), 45 of 45 recordings (p = 5.7e-14)',
        '- target-side sensitivity (single-stage targets included): 14,492 cells, -0.152, 32 of 32 negative',
        '- sleep-EDF estimator matrix: cumulative -0.107, block -0.102, window -0.108, exponential -0.052, variance-ratio -0.082, each 32 of 32',
        '- matched scored trials (ordering control): +0.001 acquisition order vs -0.108 sorted cache, identical trial set, 292 of 336 cells',
        '- SEED film-level check, five rotations over all 15 films: +0.189 ([+0.162, +0.218]), 15 of 15 positive',
        '- first implementation: 5,537 cells, -0.108 ([-0.121, -0.096]); both runs and every deviation in',
        '  INDEPENDENT_TEST_DEVIATIONS.md', '',
        '## Highlights (5 items, character counts, read from the file)', ''] + highlight_rows() + ['',
        '## Files and SHA256', '', '| file | size | sha256 |', '|---|---|---|']
notes = ['', '## Notes', '',
         '- PRESUBMISSION_AUDIT.md records all four audit rounds, including the frozen-protocol comparison',
         '  (six differences found and corrected), the target-side sensitivity and this consistency pass.',
         '- Data availability names the public repository and the current commit (8660894); a6c696a is an earlier commit in the same history.',
         '- 0001_fix_secondary_analysis.patch is retired: e05e3af, f5220f9, 98f3238, d426c14 and 1eca5be are on origin/main.',
         '- Raw data remain at D:/data/mne_data and E:/data; nothing was deleted.', '',
         '## Archived', '',
         '- archive/BSPC_Submission_Package_final_V6_20261030.zip (21-page V6 package)',
         '- archive/BSPC_Submission_Package_final_prev.zip (previous V8 package)']
manifest = '\n'.join(head + rows + notes) + '\n'
with open(os.path.join(pkg, 'MANIFEST.md'), 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(manifest)
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, names in os.walk(pkg):
        dirs.sort(); names.sort()
        for n in names:
            full = os.path.join(root, n)
            z.write(full, os.path.relpath(full, pkg).replace(os.sep, '/'))
print('files in package:', len(files) + 1)
print('zip sha256:', sha(zip_path))
print('zip bytes:', os.path.getsize(zip_path))