# -*- coding: utf-8 -*-
"""
为 BCICIV-2b 建特征缓存
==========================
每个 T 会话 -> 一个 npz：
  X    (n, 3, T) float32   8-30 Hz 带通后的 cue 后 0.5-3.5 s
  y    (n,) int8           0=左(769) 1=右(770)
  date int32               自 2005-01-01 的天数（用于算间隔天数）
  subj str, sess int

另存 meta：每个会话的日期、试次数、剔除数
"""
import os, io, glob, re
import numpy as np
import mne
from scipy.signal import butter, filtfilt
mne.set_log_level("ERROR")

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
D = os.environ.get("BSPC_OUT", os.path.join(_ROOT, "results"))
DATA = os.environ.get("BSPC_DATA", r"E:\data")
CACHE = os.environ.get("BSPC_CACHE", os.path.join(_ROOT, "features", "cache_2b"))
ROOT = os.path.join(DATA, "BCICIV-2a-mat")
OUT = os.path.join(D, "_cache2b.txt")

if not os.path.isdir(CACHE):
    os.makedirs(CACHE)

SRC = os.path.join(DATA, "BCICIV-2b")
FS = 250
T0, T1 = 0.5, 3.5          # cue 后窗口（秒）
CH = ["EEG:C3", "EEG:Cz", "EEG:C4"]
EPOCH = np.datetime64("2005-01-01")

b, a = butter(4, [8.0 / (FS / 2), 30.0 / (FS / 2)], btype="band")

L = []


def say(s=""):
    L.append(s)
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L))


say("=" * 100)
say("BCICIV-2b -> cache_2b")
say("=" * 100)
say("")
say("  窗口：cue 后 %.1f-%.1f s（%.0f 采样点）" % (T0, T1, (T1 - T0) * FS))
say("  带通：8-30 Hz（4 阶 Butterworth，零相位）")
say("  通道：%s" % CH)
say("  剔除：标 1023 的 trial")
say("")

files = sorted(glob.glob(os.path.join(SRC, "*T.gdf")))
say("  %-13s %-10s %-6s %-6s %-6s %-6s %-6s" %
    ("file", "date", "n_768", "n_rej", "kept", "L", "R"))
meta = []
for p in files:
    bn = os.path.basename(p)
    m = re.match(r"B(\d{2})(\d{2})T\.gdf", bn, re.I)
    subj, sess = "S%s" % m.group(1), int(m.group(2))
    raw = mne.io.read_raw_gdf(p, preload=True, verbose="ERROR")
    md = raw.info["meas_date"]
    dint = int((np.datetime64(md.date()) - EPOCH).astype(int))
    raw.pick_channels(CH, ordered=True)
    X = raw.get_data().astype(np.float64)
    X = filtfilt(b, a, X, axis=1)

    ann = raw.annotations
    ons = ann.onset
    desc = np.array([str(x) for x in ann.description])
    rej_t = set(np.round(ons[desc == "1023"], 3).tolist())
    cues = [(o, 0) for o in ons[desc == "769"]] + [(o, 1) for o in ons[desc == "770"]]
    cues = sorted(cues, key=lambda t: t[0])

    # 768 起点，用来判断该 trial 是否被剔除
    st = np.round(ons[desc == "768"], 3)
    rej_trial_starts = set()
    for r in rej_t:
        # 1023 与 768 同刻或紧跟其后
        near = st[np.abs(st - r) < 0.01]
        if len(near):
            rej_trial_starts.update(near.tolist())
        else:
            rej_trial_starts.add(r)

    i0, i1 = int(T0 * FS), int(T1 * FS)
    segs, ys = [], []
    for o, lab in cues:
        # 该 cue 属于哪个 trial：往前找最近的 768
        prev = st[st <= o + 1e-6]
        if len(prev) and prev[-1] in rej_trial_starts:
            continue
        s = int(round(o * FS)) + i0
        e = int(round(o * FS)) + i1
        if e > X.shape[1] or s < 0:
            continue
        segs.append(X[:, s:e].astype(np.float32))
        ys.append(lab)
    if not segs:
        say("  %-13s 无有效试次" % bn)
        continue
    Xa = np.stack(segs, 0)
    ya = np.array(ys, np.int8)
    np.savez(os.path.join(CACHE, bn.replace(".gdf", ".npz")),
             X=Xa, y=ya, date=np.int32(dint), subj=subj, sess=np.int32(sess),
             ch=np.array(CH))
    meta.append(dict(file=bn, subj=subj, sess=sess, date=dint,
                     n768=int((desc == "768").sum()), nrej=len(rej_trial_starts),
                     n=len(ya), nl=int((ya == 0).sum()), nr=int((ya == 1).sum())))
    say("  %-13s %-10s %-6d %-6d %-6d %-6d %-6d" %
        (bn, str(md.date()), (desc == "768").sum(), len(rej_trial_starts),
         len(ya), int((ya == 0).sum()), int((ya == 1).sum())))
    del raw

say("")
say("  会话数 = %d，被试数 = %d" % (len(meta), len({m["subj"] for m in meta})))
tot = sum(m["n"] for m in meta)
say("  有效试次合计 = %d（平均 %.1f / 会话）" % (tot, tot / max(len(meta), 1)))
say("  平衡：左 %d，右 %d" % (sum(m["nl"] for m in meta), sum(m["nr"] for m in meta)))

say("")
say("  每被试的会话日期与间隔（天）：")
say("  %-6s %-34s %-28s" % ("subj", "dates", "相邻间隔"))
bysub = {}
for m in meta:
    bysub.setdefault(m["subj"], []).append(m)
gaps = []
for s in sorted(bysub):
    q = sorted(bysub[s], key=lambda x: x["date"])
    ds = [x["date"] for x in q]
    dstr = "  ".join("%d:%s" % (x["sess"], str(EPOCH + np.timedelta64(x["date"], "D")))
                     for x in q)
    g = [ds[i + 1] - ds[i] for i in range(len(ds) - 1)]
    gaps.extend(g)
    say("  %-6s %-34s %s" % (s, dstr, " ".join(str(x) for x in g)))
say("")
say("  相邻会话间隔：中位 %d 天，范围 %d-%d 天（n=%d）"
    % (int(np.median(gaps)), min(gaps), max(gaps), len(gaps)))

# 可配对数量
n_pair_ord = 0
for s in bysub:
    q = sorted(bysub[s], key=lambda x: x["date"])
    for i in range(len(q)):
        for j in range(i + 1, len(q)):
            n_pair_ord += 1
say("  按时间顺序（早->晚）的跨天配对数 = %d" % n_pair_ord)
say("")
say("DONE")
