#!/usr/bin/env python3
"""Extract per-paper reasoning traces from agent.log files and push to GitHub.

Each agent's agent.log contains stream-json with the full chain of thought.
This script segments it by paper, extracts the reasoning text, and writes
it to transparency/traces/<paper_id>/<agent>_reasoning.md.

Usage:
    python3 tools/backfill_traces.py          # one-shot
    watch -n 120 python3 tools/backfill_traces.py  # periodic
"""

import json
import os
import re
import subprocess
import time
from pathlib import Path

REPO = Path("/home/toolkit/creating-agents")
TRANSPARENCY = REPO / "transparency" / "traces"
PAPERS = json.loads((REPO / "day2_intel/bigbangtest_papers.json").read_text())
PAPER_IDS = {p["id"] for p in PAPERS}

AGENT_DIRS = {
    "triage-reviewer": "review-methodology-triage",
    "three-stage-budgeted-reviewer": "review-methodology-three-stage-budgeted",
    "triage-then-deep-reviewer": "review-methodology-triage-then-deep",
    "adaptive-triage-deep-reviewer": "review-methodology-adaptive-triage-deep",
    "light-triage-engagement-reviewer": "light-triage-engagement",
    "preregistration-reviewer": "review-methodology-preregistration",
    "trust-weighted-consensus-reviewer": "trust-weighted-consensus",
}


def extract_traces_from_log(agent_name: str, log_path: Path) -> dict:
    """Parse agent.log and extract per-paper reasoning chains.

    Returns: {paper_id: [list of reasoning text blocks]}
    """
    if not log_path.exists():
        return {}

    size = log_path.stat().st_size
    # Read last 20MB (current session should be within this)
    with log_path.open("rb") as f:
        f.seek(max(0, size - 20_000_000))
        raw = f.read().decode("utf-8", errors="ignore")

    lines = raw.split("\n")

    # Track which paper the agent is currently working on
    current_paper = None
    paper_traces = {}  # paper_id -> [text blocks]

    for line in lines:
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue

        # Detect paper context from tool calls (curl to /papers/<id> or mentions of paper_id)
        if d.get("type") == "assistant":
            content = d.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue
            for item in content:
                if not isinstance(item, dict):
                    continue

                # Check tool_use for paper_id references
                if item.get("type") == "tool_use":
                    inp = item.get("input", {})
                    cmd = inp.get("command", "") if isinstance(inp, dict) else ""
                    # Look for BigBangTest paper IDs in commands
                    for pid in PAPER_IDS:
                        if pid in str(inp) or pid in cmd:
                            current_paper = pid
                            break

                # Extract reasoning text
                if item.get("type") == "text" and current_paper:
                    text = item.get("text", "").strip()
                    if text and len(text) > 20:  # skip trivial outputs
                        paper_traces.setdefault(current_paper, []).append(text)

        # Also check tool results for paper_id context
        if d.get("type") == "user":
            content = d.get("message", {}).get("content", [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        c = str(item.get("content", ""))
                        for pid in PAPER_IDS:
                            if pid in c:
                                current_paper = pid
                                break

    return paper_traces


def format_trace(agent_name: str, paper_id: str, blocks: list) -> str:
    """Format reasoning blocks into a markdown trace file."""
    lines = [
        f"# Reasoning Trace: {agent_name}",
        f"**Paper**: `{paper_id}`",
        f"**Generated**: {time.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        "---",
        "",
    ]
    for i, block in enumerate(blocks):
        # Truncate very long blocks (e.g., full paper text dumps)
        if len(block) > 3000:
            block = block[:2500] + "\n\n[...truncated...]"
        lines.append(f"### Step {i+1}")
        lines.append("")
        lines.append(block)
        lines.append("")
    return "\n".join(lines)


def main():
    updated = []

    for agent_name, dir_name in AGENT_DIRS.items():
        log_path = REPO / "agent_configs" / dir_name / "agent.log"
        if not log_path.exists():
            continue

        traces = extract_traces_from_log(agent_name, log_path)

        for paper_id, blocks in traces.items():
            if not blocks:
                continue

            trace_dir = TRANSPARENCY / paper_id
            trace_dir.mkdir(parents=True, exist_ok=True)
            trace_file = trace_dir / f"{agent_name}_reasoning.md"

            content = format_trace(agent_name, paper_id, blocks)

            # Only write if new or changed
            existing = trace_file.read_text() if trace_file.exists() else ""
            if content != existing:
                trace_file.write_text(content)
                updated.append(f"{agent_name} → {paper_id[:8]}")

    if updated:
        # Git commit + push
        os.chdir(REPO)
        subprocess.run(["git", "add", "transparency/traces/"], capture_output=True)
        msg = f"Update reasoning traces: {len(updated)} files"
        result = subprocess.run(
            ["git", "commit", "-m", msg],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            push = subprocess.run(
                ["git", "push", "origin", "sg/adaptive"],
                capture_output=True, text=True,
            )
            if push.returncode != 0:
                # Try rebase and retry
                subprocess.run(["git", "pull", "--rebase", "origin", "sg/adaptive"], capture_output=True)
                subprocess.run(["git", "push", "origin", "sg/adaptive"], capture_output=True)

        print(f"[{time.strftime('%H:%M:%S')}] Updated {len(updated)} traces: {', '.join(updated[:10])}")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] No new traces to update")


if __name__ == "__main__":
    main()
