#!/usr/bin/env python3
"""Day 2 live dashboard — tracks all 7 agents across 30 BigBangTest papers.

Usage:
    watch -n 15 python3 tools/day2_dashboard.py
"""

import json
import subprocess
import sys
import time
from pathlib import Path

BASE = "https://coale.science/api/v1"
REPO = Path("/home/toolkit/creating-agents")

AGENTS_ORDERED = [
    ("8fd0f035-3704-43a2-8e73-de97761b19b7", "t-deep"),
    ("2af20618-405b-4fde-8324-7a2d8ecd6b9b", "3stg"),
    ("5358e57f-8fb9-415e-9130-9be91d7d2954", "preg"),
    ("871ecc46-543c-4ef3-a9f2-240839220adc", "td-cx"),
    ("3aec76e6-9991-46c1-890a-8f71924dbef0", "3s-cx"),
    ("80c63e4f-bc62-48fd-b1b7-0ff2aa2535af", "adv"),
]
AGENT_MAP = {aid: short for aid, short in AGENTS_ORDERED}
AGENT_SHORTS = [short for _, short in AGENTS_ORDERED]

PAPERS = json.loads((REPO / "day2_intel/bigbangtest_papers.json").read_text())
PAPER_IDS = {p["id"]: p.get("title", "?")[:28] for p in PAPERS}

# Load adversarial scan results if available
ADV_SCAN = {}
adv_path = REPO / "day2_intel/adversarial_scan.json"
if adv_path.exists():
    try:
        ADV_SCAN = json.loads(adv_path.read_text())
    except Exception:
        pass


def curl_json(url, key, timeout=20):
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", str(timeout), "-H", f"Authorization: {key}", url],
            capture_output=True, text=True, check=False,
        )
        return json.loads(r.stdout) if r.stdout else None
    except Exception:
        return None


def get_key():
    for d in (REPO / "agent_configs").iterdir():
        kf = d / ".api_key"
        if kf.exists():
            return kf.read_text().strip()
    return None


def main():
    key = get_key()
    if not key:
        print("ERROR: no .api_key found")
        sys.exit(1)

    # Fetch all verdicts (paginated)
    all_verdicts = []
    skip = 0
    while True:
        chunk = curl_json(f"{BASE}/verdicts/?limit=1000&skip={skip}", key, timeout=30)
        if not isinstance(chunk, list) or not chunk:
            break
        all_verdicts.extend(chunk)
        if len(chunk) < 1000:
            break
        skip += 1000

    # Index: paper_id -> agent_short -> verdict info
    verdict_map = {}  # pid -> {agent_short: score}
    for v in all_verdicts:
        pid = v.get("paper_id", "")
        aid = v.get("author_id", "")
        if pid in PAPER_IDS and aid in AGENT_MAP:
            verdict_map.setdefault(pid, {})[AGENT_MAP[aid]] = v.get("score")

    # Fetch comments per agent
    comment_map = {}  # pid -> {agent_short: count}
    for aid, short in AGENTS_ORDERED:
        comments = curl_json(f"{BASE}/users/{aid}/comments?limit=500", key)
        if isinstance(comments, list):
            for c in comments:
                pid = c.get("paper_id", "")
                if pid in PAPER_IDS:
                    comment_map.setdefault(pid, {})
                    comment_map[pid][short] = comment_map[pid].get(short, 0) + 1

    # Header
    now = time.strftime("%H:%M:%S UTC")
    total_v = sum(len(v) for v in verdict_map.values())
    total_c = sum(sum(cs.values()) for cs in comment_map.values())
    papers_done = sum(1 for pid in PAPER_IDS if pid in verdict_map)

    print(f"Day 2 Dashboard — {now}  |  Papers: {papers_done}/30  |  V: {total_v}  C: {total_c}")
    print()

    # Column header: Adv scan + per-agent (V C Score) groups
    agent_header = "| Adv "
    agent_sep = "+-----"
    for short in AGENT_SHORTS:
        agent_header += f"| {short:^10s} "
        agent_sep += "+------------"

    print(f"{'Paper':<30s} {agent_header}|")
    print(f"{'-'*30}-{agent_sep}+")

    sub = f"{'':30s} |     "
    for _ in AGENT_SHORTS:
        sub += "| V  C  Scr  "
    sub += "|"
    print(sub)
    print(f"{'-'*30}-{agent_sep}+")

    # Per paper rows
    for p in PAPERS:
        pid = p["id"]
        title = p.get("title", "?")[:28]

        # Adversarial scan status
        adv = ADV_SCAN.get(pid, {})
        adv_cls = adv.get("classification", "")
        if adv_cls == "INJECTED":
            adv_mark = " ☠  "
        elif adv_cls == "CLEAN":
            adv_mark = " ·  "
        else:
            adv_mark = " ?  "

        row = f"{title:<30s} |{adv_mark}"
        for short in AGENT_SHORTS:
            v_score = verdict_map.get(pid, {}).get(short)
            c_count = comment_map.get(pid, {}).get(short, 0)
            has_v = "✓" if v_score is not None else "·"
            c_str = str(c_count) if c_count > 0 else "·"
            s_str = f"{v_score:.0f}" if v_score is not None else "·"
            row += f"| {has_v}  {c_str:<2s} {s_str:>3s}  "
        row += "|"
        print(row)

    print(f"{'-'*30}-{agent_sep}+")

    # Adversarial scan summary
    injected = sum(1 for v in ADV_SCAN.values() if v.get("classification") == "INJECTED")
    clean = sum(1 for v in ADV_SCAN.values() if v.get("classification") == "CLEAN")
    scanned = len(ADV_SCAN)
    if scanned > 0:
        print(f"Adv scan: {scanned}/30 done — {injected} INJECTED ☠, {clean} CLEAN")
    print()

    # Agent totals row
    totals = f"{'TOTALS':<30s} |     "
    for short in AGENT_SHORTS:
        v_count = sum(1 for pid in PAPER_IDS if short in verdict_map.get(pid, {}))
        c_count = sum(comment_map.get(pid, {}).get(short, 0) for pid in PAPER_IDS)
        scores = [verdict_map[pid][short] for pid in PAPER_IDS if short in verdict_map.get(pid, {})]
        avg = f"{sum(scores)/len(scores):.1f}" if scores else "—"
        totals += f"| {v_count:<2d} {c_count:<2d} {avg:>4s} "
    totals += "|"
    print(totals)


if __name__ == "__main__":
    main()
