#!/usr/bin/env python3
"""Push a reasoning trace to the transparency directory and commit+push to GitHub.

Usage:
    python3 /home/toolkit/creating-agents/tools/push_trace.py \
        --paper-id <uuid> \
        --agent-name <display_name> \
        --type comment|verdict \
        --content "The reasoning trace markdown text..." \
        [--score 7.5]  # only for verdicts

Prints the resulting GitHub URL to stdout on success.
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone

REPO_ROOT = "/home/toolkit/creating-agents"
TRANSPARENCY_DIR = os.path.join(REPO_ROOT, "transparency")
TRACES_DIR = os.path.join(TRANSPARENCY_DIR, "traces")
GITHUB_REPO_URL = "https://github.com/McGill-NLP/creating-agents"
BRANCH = "sg/adaptive"  # current working branch


def git_run(*args, retries=2):
    """Run a git command in the repo root, with optional retries for push."""
    cmd = ["git", "-C", REPO_ROOT] + list(args)
    for attempt in range(retries + 1):
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result
        if attempt < retries and "push" in args:
            # Pull and retry on push failure
            subprocess.run(
                ["git", "-C", REPO_ROOT, "pull", "--rebase", "origin", BRANCH],
                capture_output=True,
                text=True,
            )
        else:
            print(f"git {' '.join(args)} failed: {result.stderr}", file=sys.stderr)
            if attempt == retries:
                return result
    return result


def main():
    parser = argparse.ArgumentParser(description="Push a transparency trace to GitHub")
    parser.add_argument("--paper-id", required=True, help="Paper UUID")
    parser.add_argument("--agent-name", required=True, help="Agent display name")
    parser.add_argument(
        "--type",
        required=True,
        choices=["comment", "verdict"],
        help="Type of trace",
    )
    parser.add_argument("--content", required=True, help="Reasoning trace content")
    parser.add_argument(
        "--score", type=float, default=None, help="Verdict score (only for verdicts)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write file but do not commit or push",
    )
    args = parser.parse_args()

    # Validate
    if args.type == "verdict" and args.score is None:
        print(
            "Warning: --score not provided for verdict trace", file=sys.stderr
        )

    # Create directory
    paper_dir = os.path.join(TRACES_DIR, args.paper_id)
    os.makedirs(paper_dir, exist_ok=True)

    # Build filename
    filename = f"{args.agent_name}_{args.type}.md"
    filepath = os.path.join(paper_dir, filename)

    # Build content
    timestamp = datetime.now(timezone.utc).isoformat()
    score_line = f"**Score**: {args.score}\n" if args.score is not None else ""
    type_label = args.type.capitalize()

    trace_content = f"""# {type_label} Trace: {args.agent_name} on {args.paper_id}

**Agent**: {args.agent_name}
**Paper**: {args.paper_id}
**Type**: {args.type}
{score_line}**Timestamp**: {timestamp}

## Reasoning Trace

{args.content}
"""

    # Write file
    with open(filepath, "w") as f:
        f.write(trace_content)

    if args.dry_run:
        print(f"[dry-run] Wrote {filepath}", file=sys.stderr)
        # Still print the URL it would produce
        rel_path = os.path.relpath(filepath, REPO_ROOT)
        url = f"{GITHUB_REPO_URL}/blob/{BRANCH}/{rel_path}"
        print(url)
        return

    # Git add
    rel_path = os.path.relpath(filepath, REPO_ROOT)
    result = git_run("add", rel_path)
    if result.returncode != 0:
        print(f"git add failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Also add .gitkeep removal if it exists
    gitkeep = os.path.join(paper_dir, ".gitkeep")
    if os.path.exists(gitkeep):
        os.remove(gitkeep)
        git_run("add", os.path.relpath(gitkeep, REPO_ROOT))

    # Commit
    commit_msg = f"trace: {args.agent_name} {args.type} on {args.paper_id[:8]}"
    result = git_run("commit", "-m", commit_msg, "--", rel_path)
    if result.returncode != 0:
        # Check if there's nothing to commit (file unchanged)
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            print(
                "File unchanged, no new commit needed", file=sys.stderr
            )
        else:
            print(f"git commit failed: {result.stderr}", file=sys.stderr)
            sys.exit(1)

    # Push with retry
    result = git_run("push", "origin", BRANCH, retries=2)
    if result.returncode != 0:
        print(
            f"Warning: git push failed (trace is committed locally): {result.stderr}",
            file=sys.stderr,
        )
        # Still print the URL -- it will be valid once pushed

    # Print the GitHub URL
    url = f"{GITHUB_REPO_URL}/blob/{BRANCH}/{rel_path}"
    print(url)


if __name__ == "__main__":
    main()
