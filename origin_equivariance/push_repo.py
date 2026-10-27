# -*- coding: utf-8 -*-
"""Push the v16 analysis, results, figures and manuscript to the public archive."""
import base64
import io
import json
import os
import time
import urllib.error
import urllib.request
import ssl
try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    CTX = ssl._create_unverified_context()

D = r"G:\Work_work\math\EEG\paper_v8"
OWNER, NAME, PREFIX = "gzhgzy1234567890-lang", "EEG-BSPC", "origin_equivariance/"
TOKEN = os.environ.get("GH_TOKEN", "")
API = "https://api.github.com"


def req(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(API + path, data=data, method=method)
    r.add_header("Authorization", "token " + TOKEN)
    r.add_header("Accept", "application/vnd.github+json")
    r.add_header("User-Agent", "dsh")
    if data is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=60, context=CTX) as f:
            return json.loads(f.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError("%s %s -> %s" % (method, path, e.code))


def put(path, blob):
    payload = {"message": "Update " + path, "content": base64.b64encode(blob).decode(),
               "branch": "main"}
    try:
        cur = req("GET", "/repos/%s/%s/contents/%s" % (OWNER, NAME, path))
        if isinstance(cur, dict) and "sha" in cur:
            payload["sha"] = cur["sha"]
    except RuntimeError:
        pass
    return req("PUT", "/repos/%s/%s/contents/%s" % (OWNER, NAME, path), payload)


def main():
    if not TOKEN:
        raise SystemExit("no token")
    files = []
    for f in sorted(os.listdir(D)):
        if f.endswith(".py") or f.endswith(".md"):
            files.append((f, os.path.join(D, f)))
    for sub in ("results", "figs"):
        for f in sorted(os.listdir(os.path.join(D, sub))):
            if f.endswith((".txt", ".npz", ".pdf", ".png")):
                files.append((sub + "/" + f, os.path.join(D, sub, f)))
    ok = 0
    for rel, full in files:
        if os.path.getsize(full) > 20 * 1024 * 1024:
            continue
        blob = io.open(full, "rb").read()
        try:
            put(PREFIX + rel, blob)
            ok += 1
        except RuntimeError as e:
            print("FAIL", rel, str(e)[:80])
        time.sleep(0.12)
    print("uploaded", ok, "of", len(files))


if __name__ == "__main__":
    main()
