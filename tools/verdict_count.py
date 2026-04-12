#!/usr/bin/env python3
"""Count verdicts and comments per reva agent — queried directly from the
Coalescence platform, so this is the ground truth (unlike the local
`.reviewed_papers.json` which can drift out of sync when an agent posts
content but is killed before updating bookkeeping).

Usage:
    tools/verdict_count.py             # one-shot
    watch -n 10 tools/verdict_count.py # live dashboard

Data sources:
    GET /api/v1/verdicts/?limit=N                → all verdicts on platform,
                                                   filtered client-side by
                                                   author_id == agent's actor_id
    GET /api/v1/users/{actor_id}/comments?limit=N → agent's own comments
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# agent_dir_name -> actor_id (stable; confirmed via GET /users/me)
AGENTS = {
    "review-methodology-triage":               "6a944e9f-99cd-4508-9fe2-c85b80f076be",
    "review-methodology-three-stage-budgeted": "2af20618-405b-4fde-8324-7a2d8ecd6b9b",
    "review-methodology-triage-then-deep":     "8fd0f035-3704-43a2-8e73-de97761b19b7",
    "review-methodology-adaptive-triage-deep": "0c0b0abb-c045-4109-ae4e-1cf4df0e0a04",
    "light-triage-engagement":                 "85ac0904-073a-497f-b633-1cfce491bc85",
    "review-methodology-preregistration":      "5358e57f-8fb9-415e-9130-9be91d7d2954",
    "trust-weighted-consensus":                "4aca4338-14e0-4a0a-bc93-b4bd2bbf00e1",
}

AGENTS_DIR = Path("/home/toolkit/creating-agents/agent_configs")
BASE = "https://coale.science/api/v1"
PAGE = 1000  # max items per page


def curl_json(url: str, key: str):
    """Fetch JSON from a URL with Authorization header."""
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "8", "-H", f"Authorization: {key}", url],
            capture_output=True, text=True, check=False,
        )
        if r.returncode != 0 or not r.stdout:
            return None
        return json.loads(r.stdout)
    except Exception:
        return None


def read_key(agent_name: str) -> str | None:
    p = AGENTS_DIR / agent_name / ".api_key"
    if not p.exists():
        return None
    return p.read_text().strip()


def fetch_all_verdicts(key: str, cap: int = 100_000) -> list:
    """Paginate /verdicts/ until exhausted or cap reached.

    The Coalescence API returns verdicts oldest-first, so an insufficient cap
    silently truncates the NEWEST verdicts (which are usually the ones we care
    about most). Set cap high enough to fetch the entire platform comfortably.
    """
    out = []
    skip = 0
    while len(out) < cap:
        url = f"{BASE}/verdicts/?limit={PAGE}&skip={skip}"
        chunk = curl_json(url, key)
        if not isinstance(chunk, list):
            break
        out.extend(chunk)
        if len(chunk) < PAGE:
            break
        skip += PAGE
    return out


def fetch_user_comments(actor_id: str, key: str, cap: int = 5000) -> list:
    """Paginate /users/{id}/comments until exhausted or cap reached."""
    out = []
    skip = 0
    while len(out) < cap:
        url = f"{BASE}/users/{actor_id}/comments?limit={PAGE}&skip={skip}"
        chunk = curl_json(url, key)
        if not isinstance(chunk, list):
            break
        out.extend(chunk)
        if len(chunk) < PAGE:
            break
        skip += PAGE
    return out


def main():
    # Use any agent's key to hit /verdicts/ (global endpoint; auth required).
    first_name = next(iter(AGENTS))
    first_key = read_key(first_name)
    if first_key is None:
        print(f"ERROR: no .api_key for {first_name}", file=sys.stderr)
        sys.exit(1)

    all_verdicts = fetch_all_verdicts(first_key)
    total_platform = len(all_verdicts)

    rows = []
    grand_v = 0
    grand_c = 0
    for name, actor_id in AGENTS.items():
        key = read_key(name)
        if key is None:
            rows.append((name, "-", "-", actor_id[:8]))
            continue

        v_count = sum(
            1 for v in all_verdicts
            if isinstance(v, dict) and v.get("author_id") == actor_id
        )
        comments = fetch_user_comments(actor_id, key)
        c_count = len(comments) if isinstance(comments, list) else "?"

        rows.append((name, v_count, c_count, actor_id[:8]))
        if isinstance(v_count, int):
            grand_v += v_count
        if isinstance(c_count, int):
            grand_c += c_count

    # Render
    print(f"{'AGENT':<42s}  {'VERDICTS':>8s}  {'COMMENTS':>9s}  {'ACTOR':>8s}")
    print("-" * 78)
    for name, v, c, actor in rows:
        print(f"{name:<42s}  {str(v):>8s}  {str(c):>9s}  {actor:>8s}")
    print("-" * 78)
    print(f"{'TOTAL (our 5 agents)':<42s}  {grand_v:>8d}  {grand_c:>9d}")
    print()
    print(f"Total verdicts on Coalescence platform: {total_platform}")
    print(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z"))


if __name__ == "__main__":
    main()
