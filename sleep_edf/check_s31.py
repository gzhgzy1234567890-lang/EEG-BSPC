# -*- coding: utf-8 -*-
"""Assert the values reported in S31: block-wise decomposition, memory sweep, composition analyses."""
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

al = json.load(open(os.path.join(RES, 'sleep_blocks_all.json')))
ba_rows = json.load(open(os.path.join(RES, 'sleep_block_composition.json')))
dropped = sum(1 for r in al if r['ncls_block'] < 2 or r['ncls_hist'] < 2)
for name, got, want in (('blocks', len(al), 14949), ('retained', len(ba_rows), 6648), ('dropped', dropped, 8301)):
    good = got == want
    ok &= good
    print('%-10s %6d (want %6d) %s' % (name, got, want, 'ok' if good else 'FAIL'))

subs = {}
for r in al:
    subs.setdefault(r['subj'], []).append(r)
rates = []
for s, rs in subs.items():
    lo = [r for r in rs if r['maxfrac'] < 0.6]
    hi = [r for r in rs if r['maxfrac'] >= 0.8]
    if lo and hi:
        f = lambda xs: np.sum([x['err1'] - x['err0'] for x in xs]) / np.sum([x['n'] for x in xs])
        rates.append(f(hi) - f(lo))
rates = np.array(rates)
for name, got, want in (('paired n', len(rates), 32), ('paired mean', round(float(rates.mean()), 3), 0.084), ('positive', int((rates > 0).sum()), 29)):
    good = abs(got - want) < 0.002 if name == 'paired mean' else got == want
    ok &= good
    print('%-10s %s (want %s) %s' % (name, got, want, 'ok' if good else 'FAIL'))
print()
print('S31 CHECK', 'PASS' if ok else 'FAIL')