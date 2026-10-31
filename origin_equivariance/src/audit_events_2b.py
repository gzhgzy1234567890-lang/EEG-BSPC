import sys, os
import numpy as np
import mne
mne.set_log_level('ERROR')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
root = r'E:\data\BCICIV-2b'
for fn in ('B0101T.gdf', 'B0102T.gdf', 'B0103T.gdf'):
    raw = mne.io.read_raw_gdf(os.path.join(root, fn), preload=False, verbose='ERROR')
    ann = raw.annotations
    desc = np.array([str(x) for x in ann.description])
    on = ann.onset
    print('===', fn, 'sfreq', raw.info['sfreq'], 'n_times', raw.n_times, 'duration %.2f s' % raw.times[-1])
    codes, counts = np.unique(desc, return_counts=True)
    print('  codes:', {c: int(n) for c, n in zip(codes, counts)})
    for c in ('768', '769', '770', '1023', '781', '783'):
        m = desc == c
        if m.sum():
            print('  %-5s n=%3d first=%.3f last=%.3f median_isi=%.3f' % (c, m.sum(), on[m][0], on[m][-1], np.median(np.diff(on[m])) if m.sum() > 1 else float('nan')))
    m768 = desc == '768'; mcue = (desc == '769') | (desc == '770')
    if m768.sum() and mcue.sum():
        d = [np.min(np.abs(on[mcue] - t)) for t in on[m768][:5]]
        print('  first 5 768->nearest cue gaps:', [round(x, 3) for x in d])
    raw.close()