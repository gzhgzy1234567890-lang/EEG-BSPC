# -*- coding: utf-8 -*-
import json, os, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, 'results')
GAL = os.path.join(HERE, '..', 'grasp_and_lift_order', 'results')

def sm(rows, k):
    subs = {}
    for r in rows:
        subs.setdefault(r['subj'], {}).setdefault(r['night'], []).append(r[k])
    return np.array([np.mean([np.mean(v) for v in n.values()]) for n in subs.values()])

ok = True
bw = json.load(open(os.path.join(RES, 'sleep_blockwise.json')))
base = sm(bw, 'none')
for k, want in (('full', -0.102), ('mix', -0.092), ('cond', 0.020)):
    got = (sm(bw, k) - base).mean()
    good = abs(got - want) < 0.006
    ok &= good
    print('blockwise %-5s %+0.4f (want %+0.4f) %s' % (k, got, want, 'ok' if good else 'FAIL'))
print('max per-block reconstruction error %.1e' % max(r['recon_err_max'] for r in bw))
ms = json.load(open(os.path.join(GAL, 'seed_memory_scale.json')))
for w, want in ((5, -0.113), (400, 0.203)):
    got = np.mean([r['w%d' % w] for r in ms])
    good = abs(got - want) < 0.004
    ok &= good
    print('sweep w=%-3d %+0.4f (want %+0.4f) %s' % (w, got, want, 'ok' if good else 'FAIL'))
for a, want in (('0.20', -0.105), ('0.01', 0.130)):
    got = np.mean([r['a%s' % a] for r in ms])
    good = abs(got - want) < 0.004
    ok &= good
    print('sweep a=%-4s %+0.4f (want %+0.4f) %s' % (a, got, want, 'ok' if good else 'FAIL'))
print()
print('S31 CHECK', 'PASS' if ok else 'FAIL')