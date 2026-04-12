#!/usr/bin/env python3
"""Build .other_agent_scores.json for the adversarial-detector agent.

Reads existing verdict traces from transparency/traces/*/
and extracts scores + reasoning summaries from our 3 agents.
"""

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRACES_DIR = REPO_ROOT / "transparency" / "traces"
OUTPUT_PATH = REPO_ROOT / "agent_configs" / "adversarial-detector" / ".other_agent_scores.json"

AGENTS = [
    "triage-then-deep-reviewer",
    "three-stage-budgeted-reviewer",
    "preregistration-reviewer",
]

# Load the paper list
PAPERS_JSON = REPO_ROOT / "day2_intel" / "bigbangtest_papers.json"


def extract_score(content: str) -> float | None:
    """Extract score from a verdict trace file."""
    # Look for **Score**: X.X pattern in the header
    match = re.search(r"\*\*Score\*\*:\s*([\d.]+)", content)
    if match:
        return float(match.group(1))
    # Look for Score: X.X
    match = re.search(r"^(?:\*\*)?Score(?:\*\*)?:\s*([\d.]+)", content, re.MULTILINE)
    if match:
        return float(match.group(1))
    return None


def extract_reasoning_summary(content: str, max_chars: int = 200) -> str:
    """Extract first ~200 chars of reasoning from a verdict trace."""
    # Find the reasoning trace section
    match = re.search(r"## Reasoning Trace\s*\n+(.*)", content, re.DOTALL)
    if match:
        text = match.group(1).strip()
    else:
        # Fall back to the verdict reasoning section
        match = re.search(r"## Verdict Reasoning.*?\n+(.*)", content, re.DOTALL)
        if match:
            text = match.group(1).strip()
        else:
            # Just take everything after the header block
            lines = content.split("\n")
            text_lines = []
            past_header = False
            for line in lines:
                if past_header:
                    text_lines.append(line)
                elif line.startswith("## "):
                    past_header = True
                    text_lines.append(line)
            text = "\n".join(text_lines).strip()

    # Truncate to max_chars
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0] + "..."
    return text


def main():
    papers = json.loads(PAPERS_JSON.read_text())
    paper_ids = [p["id"] for p in papers]

    result = {}
    papers_with_data = 0
    total_verdicts = 0

    for paper_id in paper_ids:
        trace_dir = TRACES_DIR / paper_id
        if not trace_dir.exists():
            continue

        paper_data = {}
        for agent in AGENTS:
            verdict_file = trace_dir / f"{agent}_verdict.md"
            if not verdict_file.exists():
                continue

            content = verdict_file.read_text(encoding="utf-8")
            score = extract_score(content)
            if score is None:
                print(f"  WARNING: Could not extract score from {verdict_file}", file=sys.stderr)
                continue

            reasoning = extract_reasoning_summary(content)
            paper_data[agent] = {
                "score": score,
                "reasoning_summary": reasoning,
            }
            total_verdicts += 1

        if paper_data:
            result[paper_id] = paper_data
            papers_with_data += 1

    # Write output
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(f"Built .other_agent_scores.json:")
    print(f"  Papers with data: {papers_with_data}/{len(paper_ids)}")
    print(f"  Total verdicts extracted: {total_verdicts}")
    print(f"  Output: {OUTPUT_PATH}")

    # Summary per agent
    for agent in AGENTS:
        count = sum(1 for pd in result.values() if agent in pd)
        print(f"  {agent}: {count} verdicts")


if __name__ == "__main__":
    main()
