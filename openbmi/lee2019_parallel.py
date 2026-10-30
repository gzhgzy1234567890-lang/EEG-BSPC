# -*- coding: utf-8 -*-
"""Parallel Lee2019-MI runner: concurrent downloads, process-pool analysis.

Downloads are I/O bound (8 threads), feature computation is CPU bound (4 processes,
each holding one 609 MB MAT pair, so the pool is capped by the 15.4 GB of RAM).
Everything is resumable: a subject already in results/openbmi_all.json is skipped.
"""
import json
import os
import sys
import urllib.request
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

ROOT = r"D:\data\mne_data\MNE-lee2019-mi-data\gigadb\pub\10.5524\100001_101000\100542"
BASE = "https://s3.ap-northeast-1.wasabisys.com/gigadb-datasets/live/pub/10.5524/100001_101000/100542"
OUT = os.path.join(HERE, "results", "openbmi_all.json")
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"
SUBJECTS = list(range(1, 55))


def path_of(subject, session):
    return os.path.join(ROOT, "session%d" % session, "s%d" % subject,
                        "sess0%d_subj%02d_EEG_MI.mat" % (session, subject))


def present(subject, session):
    p = path_of(subject, session)
    return os.path.exists(p) and os.path.getsize(p) > 1e8


def download_one(args):
    subject, session = args
    dst = path_of(subject, session)
    if present(subject, session):
        return (subject, session, "cached")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    url = "%s/session%d/s%d/sess0%d_subj%02d_EEG_MI.mat" % (BASE, session, subject, session, subject)
    tmp = dst + ".part"
    try:
        with urllib.request.urlopen(url, timeout=1800) as r, open(tmp, "wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
        if os.path.getsize(tmp) < 1e8:
            raise RuntimeError("short file")
        os.replace(tmp, dst)
        return (subject, session, "downloaded")
    except Exception as exc:
        if os.path.exists(tmp):
            os.remove(tmp)
        return (subject, session, "failed: %r" % (exc,))


def evaluate(subject):
    import lee2019_direct as L
    a, b = path_of(subject, 1), path_of(subject, 2)
    try:
        res = L.run(a, b, "subj%02d" % subject)
        return {"subject": subject, "ba": {str(k): float(v) for k, v in res.items()},
                "delta": float(res[1.0] - res[0.0])}
    except Exception as exc:
        return {"subject": subject, "error": repr(exc)[:200]}


def main():
    todo = [(s, k) for s in SUBJECTS for k in (1, 2) if not present(s, k)]
    print("missing files:", len(todo), flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(download_one, t) for t in todo]
        done = 0
        for f in as_completed(futs):
            s, k, st = f.result()
            done += 1
            if done % 10 == 0 or st.startswith("failed"):
                print("download %d/%d subject %d session %d %s" % (done, len(todo), s, k, st), flush=True)

    ready = [s for s in SUBJECTS if present(s, 1) and present(s, 2)]
    print("subjects ready:", len(ready), flush=True)

    rows = []
    if os.path.exists(OUT):
        try:
            rows = json.load(open(OUT))["rows"]
        except Exception:
            rows = []
    have = {r["subject"] for r in rows if "delta" in r}
    pend = [s for s in ready if s not in have]
    print("to evaluate:", len(pend), flush=True)

    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(evaluate, pend):
            rows.append(r)
            tag = ("delta %+.4f" % r["delta"]) if "delta" in r else r.get("error", "")
            print("subject %2d %s" % (r["subject"], tag), flush=True)
            json.dump({"rows": rows}, open(OUT, "w"), indent=1)

    ok = [r for r in rows if "delta" in r]
    json.dump({"rows": rows}, open(OUT, "w"), indent=1)
    print("done, n =", len(ok), flush=True)


if __name__ == "__main__":
    main()
