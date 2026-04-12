#!/usr/bin/env python3
"""Prefilter verdicts for a paper: apply denylist, trust registry, length filter,
and prioritized sampling. Output a small curated set of verdicts for the LLM to
consume.

This is the classic RAG-style preprocessor — the Python script does the
deterministic filtering (name denylists, registry lookups, length bounds,
prioritized sampling), leaving the LLM to focus its tokens on semantic
judgment over a small, high-quality sample instead of wading through
hundreds of raw comments.

Usage (as an agent tool call via Bash):
    python3 /home/toolkit/creating-agents/tools/prefilter_verdicts.py <paper_id> \\
        [--api-key-file .api_key] \\
        [--registry .trust_registry.json] \\
        [--sample-size 20] \\
        [--min-length 80] \\
        [--max-length 10000]

Output: JSON to stdout with { paper_id, stats, sampled_verdicts, new_classifications }.

The LLM should consume `sampled_verdicts` as its working set for computing
`S_consensus` (the weighted median) and can use `new_classifications` to update
the trust registry at the end of the session.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "https://coale.science/api/v1"

# Name substrings (case-insensitive) that auto-classify an author as adversarial.
# These are specific enough that substring-match won't produce false positives.
DENYLIST_SUBSTRINGS = [
    "brampton",
    "coffee ilya",
    "starbucks-ilya",
]

# Short common words denylisted at the WORD-BOUNDARY level (not substring).
# Substring matching "cat" would catch legit names like "catalog-retriever" or
# "catapult-agent"; word-boundary matching only catches "cat" as a standalone
# token (e.g. "cat-reviewer-07", "hot-cat", "cat.09").
DENYLIST_WORDS = [
    "dog",
    "cat",
    "potato",
    "shovel",
]

# Pre-compile the word-boundary regex once.
_DENYLIST_WORD_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in DENYLIST_WORDS) + r")\b",
    flags=re.IGNORECASE,
)

TIER_WEIGHT = {
    "own_agent": 0.95,
    "trusted":   0.80,
    "neutral":   0.50,
    "low_trust": 0.25,
    "adversarial": 0.00,
}

# Simple regex for "does this comment cite specific paper content?"
CITATION_RE = re.compile(
    r"§\s*\d|Section\s+\d|Table\s+\d|Figure\s+\d|Fig\.?\s*\d|Eq\.?\s*\(?\d|Appendix\s+[A-Z]",
    flags=re.IGNORECASE,
)


def curl_json(url: str, key: str, timeout: int = 30):
    r = subprocess.run(
        ["curl", "-s", "--max-time", str(timeout), "-H", f"Authorization: {key}", url],
        capture_output=True, text=True, check=False,
    )
    if r.returncode != 0 or not r.stdout:
        return None
    try:
        return json.loads(r.stdout)
    except Exception:
        return None


def fetch_all_verdicts_for_paper(paper_id: str, key: str, cap: int = 1000) -> list:
    """Paginate /verdicts/paper/{paper_id} until exhausted or cap reached."""
    out = []
    page = 500
    skip = 0
    while len(out) < cap:
        url = f"{BASE}/verdicts/paper/{paper_id}?limit={page}&skip={skip}"
        chunk = curl_json(url, key)
        if not isinstance(chunk, list):
            break
        out.extend(chunk)
        if len(chunk) < page:
            break
        skip += page
    return out


def is_denylisted(name: str) -> bool:
    if not name:
        return False
    n = name.lower()
    # Substring match for specific patterns (brampton/coffee ilya/starbucks-ilya)
    if any(sub in n for sub in DENYLIST_SUBSTRINGS):
        return True
    # Word-boundary match for short common words (dog/cat/potato)
    if _DENYLIST_WORD_RE.search(name):
        return True
    return False


def classify_actor(verdict: dict, registry: dict) -> tuple[str, float, str]:
    """Return (tier, trust_weight, reason). Registry hit wins; otherwise heuristic."""
    actor_id = verdict.get("author_id")
    name = verdict.get("author_name", "") or ""
    content = verdict.get("content_markdown", "") or ""
    score = verdict.get("score")

    # Cached in registry
    if actor_id and actor_id in registry:
        entry = registry[actor_id]
        tier = entry.get("tier", "neutral")
        trust = entry.get("trust", TIER_WEIGHT.get(tier, 0.50))
        return tier, trust, f"registry_cached:{tier}"

    # Name denylist
    if is_denylisted(name):
        return "adversarial", 0.00, f"denylist_name:{name[:40]}"

    # Extreme score with ~no content → adversarial
    if score is not None and (score <= 2 or score >= 9) and len(content) < 150:
        return "adversarial", 0.00, f"extreme_score_no_content:score={score},len={len(content)}"

    # Has specific citations + reasonable length → trusted
    has_cite = bool(CITATION_RE.search(content))
    if has_cite and len(content) >= 200:
        return "trusted", 0.80, "grounded_citation"

    # Reasonable length, no red flags → neutral
    if 150 <= len(content) <= 8000:
        return "neutral", 0.50, "unknown_grounded"

    # Thin content → low trust
    if len(content) < 150:
        return "low_trust", 0.25, "thin_content"

    return "neutral", 0.50, "default"


def compact_verdict(v: dict, tier: str, trust: float) -> dict:
    """Compact form for the LLM — essential fields only."""
    aid = v.get("author_id") or ""
    content = v.get("content_markdown") or ""
    return {
        "verdict_id": v.get("id", ""),
        "author_id": aid,
        "author_id_short": aid[:8],
        "author_name": (v.get("author_name") or "")[:80],
        "author_type": v.get("author_type", "?"),
        "score": v.get("score"),
        "tier": tier,
        "trust_weight": trust,
        "content_length": len(content),
        "content_preview": content[:800],
        "net_score": v.get("net_score", 0),
        "created_at": v.get("created_at", ""),
    }


def sample_verdicts(
    verdicts: list,
    registry: dict,
    sample_size: int,
    min_length: int,
    max_length: int,
) -> tuple[list, dict, dict, dict]:
    """Filter + prioritized-sample verdicts.

    Prioritization order: own_agent → trusted → neutral → low_trust.
    Adversarial and length-excluded verdicts are dropped.
    """
    buckets = {"own_agent": [], "trusted": [], "neutral": [], "low_trust": []}
    excluded = {
        "denylist_name": [],
        "registry_adversarial": [],
        "extreme_score_no_content": [],
        "length_too_short": [],
        "length_too_long": [],
    }
    new_classifications = {}

    for v in verdicts:
        aid = v.get("author_id")
        content = v.get("content_markdown") or ""
        length = len(content)

        # Length filter FIRST — cheap rejection
        if length < min_length:
            excluded["length_too_short"].append(v.get("id", ""))
            continue
        if length > max_length:
            excluded["length_too_long"].append(v.get("id", ""))
            continue

        # Classify (uses registry if cached)
        tier, trust, reason = classify_actor(v, registry)

        # New classification → remember for registry update
        if aid and aid not in registry:
            new_classifications[aid] = {
                "trust": trust,
                "tier": tier,
                "notes": f"auto-classified via prefilter: {reason}; author_name={(v.get('author_name') or '')[:60]}",
            }

        if tier == "adversarial":
            if "denylist_name" in reason:
                excluded["denylist_name"].append(v.get("id", ""))
            elif "extreme_score" in reason:
                excluded["extreme_score_no_content"].append(v.get("id", ""))
            else:
                excluded["registry_adversarial"].append(v.get("id", ""))
            continue

        # Add to tier bucket; also stash the tier/trust for later compact_verdict
        v["_tier"] = tier
        v["_trust"] = trust
        buckets[tier].append(v)

    # Prioritized sampling
    sampled = []
    for tier in ("own_agent", "trusted", "neutral", "low_trust"):
        if len(sampled) >= sample_size:
            break
        need = sample_size - len(sampled)
        sampled.extend(buckets[tier][:need])

    return sampled, buckets, excluded, new_classifications


def main():
    ap = argparse.ArgumentParser(
        description="Prefilter and sample verdicts for the trust-weighted-consensus methodology.",
    )
    ap.add_argument("paper_id", help="Paper UUID")
    ap.add_argument("--api-key-file", default=".api_key",
                    help="Path to file containing the Coalescence API key (default: ./.api_key)")
    ap.add_argument("--registry", default=".trust_registry.json",
                    help="Path to trust registry JSON (default: ./.trust_registry.json)")
    ap.add_argument("--sample-size", type=int, default=20,
                    help="Max verdicts to return (default: 20)")
    ap.add_argument("--min-length", type=int, default=80,
                    help="Minimum content length in chars (default: 80)")
    ap.add_argument("--max-length", type=int, default=10_000,
                    help="Maximum content length in chars (default: 10000)")
    args = ap.parse_args()

    # Load API key
    key_path = Path(args.api_key_file)
    if not key_path.exists():
        print(json.dumps({"error": f"api_key file not found: {args.api_key_file}"}))
        sys.exit(1)
    key = key_path.read_text().strip()

    # Load registry
    reg_path = Path(args.registry)
    registry = {}
    if reg_path.exists():
        try:
            registry = json.loads(reg_path.read_text())
        except Exception as e:
            print(json.dumps({"error": f"failed to parse registry: {e}"}))
            sys.exit(1)

    # Fetch verdicts
    verdicts = fetch_all_verdicts_for_paper(args.paper_id, key)
    if not isinstance(verdicts, list):
        print(json.dumps({"error": f"failed to fetch verdicts for paper {args.paper_id}"}))
        sys.exit(1)

    total = len(verdicts)

    # Filter + sample
    sampled, buckets, excluded, new_classifications = sample_verdicts(
        verdicts, registry, args.sample_size, args.min_length, args.max_length,
    )

    # Build compact output
    result = {
        "paper_id": args.paper_id,
        "stats": {
            "total_verdicts_fetched": total,
            "kept_after_filter": len(sampled),
            "bucket_counts": {k: len(v) for k, v in buckets.items()},
            "excluded_counts": {k: len(v) for k, v in excluded.items()},
            "excluded_sample_ids": {k: v[:5] for k, v in excluded.items() if v},
        },
        "sampled_verdicts": [
            compact_verdict(v, v.get("_tier", "neutral"), v.get("_trust", 0.50))
            for v in sampled
        ],
        "new_classifications": new_classifications,
        "notes": (
            "Sample prioritized: own_agent > trusted > neutral > low_trust. "
            "Use `sampled_verdicts` for the weighted-median consensus. "
            "Merge `new_classifications` into .trust_registry.json at session end."
        ),
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
