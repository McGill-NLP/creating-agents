#!/usr/bin/env python3
"""Scan agent_configs/ and report per-agent stats for the running review agents.

One JSON line per invocation is appended to logs/agent_stats.jsonl, so running
this on a cron schedule produces a simple time-series you can aggregate later.

Usage:
    python3 tools/agent_stats.py                 # append to logs/agent_stats.jsonl
    python3 tools/agent_stats.py --print         # also print a human-readable summary

Counts:
- pl_calls:  tool calls to any mcp__paperlantern__* tool
- verdicts:  POSTs to /api/v1/verdicts (structured verdict with score)
- comments:  POSTs to /api/v1/comments (free-form review text)
- votes:     POSTs to /api/v1/votes (upvote/downvote actions)

Both `verdicts` and `comments` count as "posting a review" — different agents
use different endpoints depending on the review methodology they're following.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / "agent_configs"
LOG_PATH = REPO_ROOT / "logs" / "agent_stats.jsonl"
AGENT_NAME_PREFIX = "review-methodology-"

# Post detection.
#
# Agents post to Coalescence in two ways: `curl -X POST ...` (flags and URL in
# any order) and inline Python scripts (`python3 << PYEOF ... urllib.request /
# requests.post ... PYEOF`). The earlier version of this script only caught curl
# POSTs with the URL immediately after `-X POST`, so it missed most real posts.
#
# The rule we enforce now:
#   1. The command must clearly intend to POST something (POST-intent marker).
#   2. It must reference a Coalescence endpoint we care about.
#   3. Extract paper_id from the JSON body if possible.
#
# A single command that touches both verdicts and comments endpoints with POST
# intent is counted as one verdict post AND one comment post.

_POST_INTENT_PATTERNS = [
    r"-X\s+['\"]?POST['\"]?",        # curl -X POST  or  curl -X "POST"
    r"requests\.post\s*\(",           # python: requests.post(...)
    r"method\s*=\s*['\"]POST['\"]",   # python: Request(..., method="POST")
]
_POST_INTENT_RE = re.compile("|".join(_POST_INTENT_PATTERNS))

# Endpoint match (any /api/vN/verdicts or /api/vN/comments, excluding GET-style
# read paths like /comments/paper/<id> or /verdicts/paper/<id> which are used
# for GETs in this codebase).
_VERDICT_ENDPOINT_RE = re.compile(r"/api/v\d+/verdicts(?!/paper/)")
_COMMENT_ENDPOINT_RE = re.compile(r"/api/v\d+/comments(?!/paper/)")
_VOTE_ENDPOINT_RE = re.compile(r"/api/v\d+/votes(?!/paper/)")

_UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
# Match paper_id in any of these forms:
#   "paper_id": "<uuid>"         — JSON key, any quoting
#   paper_id = "<uuid>"          — Python variable (case-insensitive)
#   PAPER_ID = "<uuid>"          — constant convention
_PAPER_ID_RE = re.compile(
    rf'["\']paper_id["\']\s*:\s*["\']({_UUID})["\']'
    rf"|"
    rf"(?:paper_id|PAPER_ID)\s*=\s*['\"]({_UUID})['\"]",
    re.IGNORECASE,
)


def _extract_paper_id(cmd: str) -> str | None:
    m = _PAPER_ID_RE.search(cmd)
    if not m:
        return None
    return m.group(1) or m.group(2)


def _classify_post(cmd: str) -> list[tuple[str, str | None]]:
    """Return [(endpoint_type, paper_id), ...] for verdict/comment/vote POSTs
    found in a single Bash command. Empty list if no POST intent or no
    relevant endpoint."""
    if "coale.science" not in cmd:
        return []
    if not _POST_INTENT_RE.search(cmd):
        return []

    paper_id = _extract_paper_id(cmd)
    hits = []
    if _VERDICT_ENDPOINT_RE.search(cmd):
        hits.append(("verdicts", paper_id))
    if _COMMENT_ENDPOINT_RE.search(cmd):
        hits.append(("comments", paper_id))
    if _VOTE_ENDPOINT_RE.search(cmd):
        hits.append(("votes", paper_id))
    return hits


def parse_agent_log(log_path: Path) -> dict:
    """Return per-agent counts:
      pl_calls:   tool calls to mcp__paperlantern__*
      verdicts:   POSTs to /api/v*/verdicts
      comments:   POSTs to /api/v*/comments
      votes:      POSTs to /api/v*/votes
      papers:     unique paper IDs the agent posted verdict-or-comment on
    """
    counts = {"pl_calls": 0, "verdicts": 0, "comments": 0, "votes": 0}
    papers = set()

    if not log_path.exists():
        return {**counts, "papers": 0}

    with open(log_path, errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            if obj.get("type") != "assistant":
                continue

            for c in obj.get("message", {}).get("content", []):
                if c.get("type") != "tool_use":
                    continue
                name = c.get("name", "")
                inp = c.get("input", {})

                if name.startswith("mcp__paperlantern__"):
                    counts["pl_calls"] += 1

                if name == "Bash":
                    cmd = inp.get("command", "")
                    for endpoint, paper_id in _classify_post(cmd):
                        counts[endpoint] += 1
                        if paper_id and endpoint in ("verdicts", "comments"):
                            papers.add(paper_id)

    return {**counts, "papers": len(papers)}


def collect() -> dict:
    """Collect stats across all review-methodology-* agents."""
    agents = {}
    for agent_dir in sorted(AGENTS_DIR.glob(f"{AGENT_NAME_PREFIX}*")):
        if not agent_dir.is_dir():
            continue
        short = agent_dir.name.removeprefix(AGENT_NAME_PREFIX)
        agents[short] = parse_agent_log(agent_dir / "agent.log")

    totals = {
        "pl_calls": sum(a["pl_calls"] for a in agents.values()),
        "verdicts": sum(a["verdicts"] for a in agents.values()),
        "comments": sum(a["comments"] for a in agents.values()),
        "votes":    sum(a["votes"] for a in agents.values()),
        "papers":   sum(a["papers"] for a in agents.values()),
    }
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agents": agents,
        "totals": totals,
    }


def print_summary(snapshot: dict) -> None:
    ts = snapshot["ts"]
    print(f"[{ts}]")
    header = (
        f"  {'agent':24s}  {'papers':>6s}  {'pl_calls':>8s}"
        f"  {'verdicts':>8s}  {'comments':>8s}  {'votes':>6s}"
    )
    print(header)
    print(f"  {'-' * (len(header) - 2)}")
    for name, s in snapshot["agents"].items():
        print(
            f"  {name:24s}  {s['papers']:>6d}  {s['pl_calls']:>8d}"
            f"  {s['verdicts']:>8d}  {s['comments']:>8d}  {s['votes']:>6d}"
        )
    t = snapshot["totals"]
    print(
        f"  {'TOTAL':24s}  {t['papers']:>6d}  {t['pl_calls']:>8d}"
        f"  {t['verdicts']:>8d}  {t['comments']:>8d}  {t['votes']:>6d}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print", action="store_true", help="Also print a human-readable summary")
    args = parser.parse_args()

    snapshot = collect()

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(snapshot) + "\n")

    if args.print:
        print_summary(snapshot)

    return 0


if __name__ == "__main__":
    sys.exit(main())
