#!/usr/bin/env bash
# Count successful verdict submissions per reva agent.
# Usage:
#   tools/verdict_count.sh           # one-shot
#   watch -n 10 tools/verdict_count.sh
#
# Data source: each agent's .reviewed_papers.json, where an entry with
# "verdict": true means the agent successfully posted a verdict on that
# paper. commented/voted/global_summary are also tracked where the
# methodology uses them.

set -euo pipefail

AGENTS_DIR="/home/toolkit/creating-agents/agent_configs"
AGENTS=(
    "review-methodology-triage"
    "review-methodology-three-stage-budgeted"
    "review-methodology-triage-then-deep"
    "review-methodology-adaptive-triage-deep"
    "light-triage-engagement"
)

printf "%-45s  %8s  %10s  %7s  %7s\n" "AGENT" "VERDICTS" "COMMENTED" "VOTED" "TOTAL"
printf "%s\n" "------------------------------------------------------------------------------------------"

TOTAL_V=0
TOTAL_C=0
TOTAL_VT=0
TOTAL_T=0

for a in "${AGENTS[@]}"; do
    f="$AGENTS_DIR/$a/.reviewed_papers.json"
    if [ ! -f "$f" ]; then
        printf "%-45s  %8s  %10s  %7s  %7s\n" "$a" "-" "-" "-" "-"
        continue
    fi
    # python3 parse — handles nested dict values, missing keys, malformed JSON
    stats=$(python3 - "$f" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    if not isinstance(d, dict):
        print("0 0 0 0")
        sys.exit(0)
    verdicts = 0
    commented = 0
    voted = 0
    total = len(d)
    for v in d.values():
        if not isinstance(v, dict):
            continue
        if v.get("verdict") is True:
            verdicts += 1
        if v.get("commented") is True:
            commented += 1
        if v.get("voted") is True:
            voted += 1
    print(f"{verdicts} {commented} {voted} {total}")
except Exception:
    print("? ? ? ?")
PY
)
    read -r V C VT T <<<"$stats"
    printf "%-45s  %8s  %10s  %7s  %7s\n" "$a" "$V" "$C" "$VT" "$T"
    # accumulate if numeric
    if [[ "$V" =~ ^[0-9]+$ ]]; then TOTAL_V=$((TOTAL_V + V)); fi
    if [[ "$C" =~ ^[0-9]+$ ]]; then TOTAL_C=$((TOTAL_C + C)); fi
    if [[ "$VT" =~ ^[0-9]+$ ]]; then TOTAL_VT=$((TOTAL_VT + VT)); fi
    if [[ "$T" =~ ^[0-9]+$ ]]; then TOTAL_T=$((TOTAL_T + T)); fi
done

printf "%s\n" "------------------------------------------------------------------------------------------"
printf "%-45s  %8s  %10s  %7s  %7s\n" "TOTAL" "$TOTAL_V" "$TOTAL_C" "$TOTAL_VT" "$TOTAL_T"
echo
echo "Running agents (reva status):"
if command -v reva >/dev/null 2>&1; then
    reva status 2>&1 | tail -n +1 | head -10
else
    echo "  reva not in PATH"
fi
echo
date '+%Y-%m-%d %H:%M:%S %Z'
