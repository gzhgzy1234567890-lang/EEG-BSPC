# -*- coding: utf-8 -*-
"""Recompute the sleep-EDF headline numbers from the archived result files, and assert them."""
import json, os, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get('BSPC_RESULTS', os.path.join(HERE, 'results'))


def load(name):
    p = os.path.join(RES, name)
    if not os.path.exists(p):
        return None
    data = json.load(open(p))
    if isinstance(data, dict):
        for k in ('cells', 'rows'):
            if k in data:
                return data[k]
        return None
    return data


def subj_means(rows, key, night_key='night', subj_key='subj'):
    subs = {}
    for r in rows:
        subs.setdefault(r[subj_key], {}).setdefault(r[night_key], []).append(r[key])
    return np.array([np.mean([np.mean(v) for v in n.values()]) for n in subs.values()])


def boot_ci(vals, seed=20261031):
    rng = np.random.default_rng(seed)
    b = [rng.choice(vals, len(vals), replace=True).mean() for _ in range(5000)]
    return np.percentile(b, [2.5, 97.5])


def main_result():
    rows = load('sleep_edf_frozen_cells.json')
    if rows is None:
        return None
    d = subj_means(rows, 'delta')
    lo, hi = boot_ci(d)
    return {'cells': len(rows), 'mean': d.mean(), 'ci': (lo, hi), 'neg': int((d < 0).sum()), 'n': len(d)}


def estimator_matrix():
    rows = load('sleep_edf_estimator_matrix.json')
    if rows is None:
        return None
    out = {}
    for e in ('cumulative', 'block', 'window50', 'exponential', 'varratio'):
        d = subj_means(rows, '%s|1.00' % e) - subj_means(rows, '%s|0.00' % e)
        out[e] = (d.mean(), int((d < 0).sum()))
    return out


def decomposition():
    rows = load('sleep_decomposition.json')
    if rows is None:
        return None
    base = subj_means(rows, 'none')
    out = {'none': base.mean()}
    for k in ('full', 'prior', 'cond'):
        d = subj_means(rows, k) - base
        out[k] = (d.mean(), int((d < 0).sum()))
    err = max(r['recon_err'] for r in rows)
    same = [r for r in rows if r['n_only_a'] == 0 and r['n_only_b'] == 0]
    b2 = subj_means(same, 'none')
    out['same'] = {k: (subj_means(same, k) - b2).mean() for k in ('full', 'prior', 'cond')}
    out['recon_err_max'] = err
    out['n_same'] = len(same)
    return out


def gate():
    rows = load('sleep_gate_online.json')
    if rows is None:
        return None
    base = subj_means(rows, 'none')
    return {'all': (subj_means(rows, 'all') - base).mean(),
            'gate': (subj_means(rows, 'gate') - base).mean(),
            'frac': float(np.mean([r['frac_corrected'] for r in rows]))}


def telemetry():
    rows = load('sleep_telemetry_cells.json')
    if rows is None:
        return None
    d = subj_means(rows, 'delta')
    lo, hi = boot_ci(d)
    return {'cells': len(rows), 'mean': d.mean(), 'ci': (lo, hi), 'neg': int((d < 0).sum()), 'n': len(d)}


def models():
    rows = load('sleep_models.json')
    if rows is None:
        return None
    return {k: subj_means(rows, k).mean() for k in ('lda', 'svm', 'mlp')}



GAL = os.environ.get('BSPC_GAL_RESULTS', os.path.join(HERE, '..', 'grasp_and_lift_order', 'results'))


def gal():
    p = os.path.join(GAL, 'gal_order_curves.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    out = {}
    for key in ('published', 'sorted_control', 'time'):
        cells = d[key]['cells']
        per_subj = {}
        for row in cells:
            subj, lam0, lam1 = row[0], row[3], row[-1]
            per_subj.setdefault(subj, []).append(lam1 - lam0)
        v = np.array([np.mean(x) for x in per_subj.values()])
        out[key] = (v.mean(), int((v < 0).sum()), len(v))
    return out


def seed_film():
    p = os.path.join(GAL, 'seed_film_disjoint_rot.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    v = np.array(d['per_subject'])
    return v.mean(), int((v > 0).sum()), len(v)


EXPECT = {
    'main': (-0.1023, 0.010),
    'cumulative': (-0.107, 0.006),
    'block': (-0.102, 0.006),
    'window50': (-0.108, 0.006),
    'exponential': (-0.052, 0.006),
    'varratio': (-0.082, 0.006),
    'full': (-0.098, 0.006),
    'prior': (-0.120, 0.008),
    'cond': (0.034, 0.008),
    'gate': (0.000, 0.004),
    'telemetry': (-0.048, 0.006),
    'svm': (-0.064, 0.008),
    'mlp': (-0.061, 0.008),
    'published': (-0.1075, 0.008),
    'sorted_control': (-0.090, 0.008),
    'time': (0.0014, 0.006),
    'seed_rot': (0.200, 0.010),
}


def report():
    ok = True
    m = main_result()
    if m:
        print('main          %+0.4f [%+0.4f, %+0.4f]  %d/%d negative  %d cells' % (m['mean'], m['ci'][0], m['ci'][1], m['neg'], m['n'], m['cells']))
        ok &= abs(m['mean'] - EXPECT['main'][0]) < EXPECT['main'][1]
    em = estimator_matrix()
    if em:
        for k, (v, n) in em.items():
            print('%-13s %+0.4f  %d/32 negative' % (k, v, n))
            ok &= abs(v - EXPECT[k][0]) < EXPECT[k][1]
    dc = decomposition()
    if dc:
        print('decomposition: none %.4f  full %+0.4f  prior %+0.4f  cond %+0.4f' % (dc['none'], dc['full'][0], dc['prior'][0], dc['cond'][0]))
        for k in ('full', 'prior', 'cond'):
            ok &= abs(dc[k][0] - EXPECT[k][0]) < EXPECT[k][1]
        print('identical class sets (%d cells): full %+0.4f  prior %+0.4f  cond %+0.4f' % (dc['n_same'], dc['same']['full'], dc['same']['prior'], dc['same']['cond']))
    g = gate()
    if g:
        print('gate: always %+0.4f  online %+0.4f  (%.0f%% of blocks corrected)' % (g['all'], g['gate'], 100 * g['frac']))
        ok &= abs(g['gate'] - EXPECT['gate'][0]) < EXPECT['gate'][1]
    t = telemetry()
    if t:
        print('telemetry     %+0.4f [%+0.4f, %+0.4f]  %d/%d negative  %d cells' % (t['mean'], t['ci'][0], t['ci'][1], t['neg'], t['n'], t['cells']))
        ok &= abs(t['mean'] - EXPECT['telemetry'][0]) < EXPECT['telemetry'][1]
    md = models()
    if md:
        print('models: lda %+0.4f  svm %+0.4f  mlp %+0.4f' % (md['lda'], md['svm'], md['mlp']))
        ok &= abs(md['svm'] - EXPECT['svm'][0]) < EXPECT['svm'][1]
        ok &= abs(md['mlp'] - EXPECT['mlp'][0]) < EXPECT['mlp'][1]
    g = gal()
    if g:
        for k, (v, n, m) in g.items():
            print('%-14s %+0.4f  %d/%d negative' % (k, v, n, m))
            ok &= abs(v - EXPECT[k][0]) < EXPECT[k][1]
    sf = seed_film()
    if sf:
        print('SEED film-disjoint (3 rotations) %+0.4f  %d/%d positive' % sf)
        ok &= abs(sf[0] - EXPECT['seed_rot'][0]) < EXPECT['seed_rot'][1]
    print()
    print('CHECK', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(report())