#!/usr/bin/env bash
# Monitor verdict throughput for all live experimental agents.
#
# Counts completed sessions (`verdicts_this_session=N` summary lines) from
# each agent.log and reports per-agent totals + estimated rate. Run this at
# any time to check progress against the 100-per-hour target.
#
# Usage: ./monitor_verdicts.sh [agents_dir]

set -e
dir="${1:-agents}"

printf '%-22s  %8s  %12s  %12s  %s\n' AGENT VERDICTS MEAN/SESSION LAST CUR_SESS
echo "----------------------  --------  ------------  ------------  ----------------------"

total=0
for agent_dir in "$dir"/*/; do
  name=$(basename "$agent_dir")
  log="$agent_dir/agent.log"
  [ -f "$log" ] || continue

  # Strip lines that match the literal prompt template (contains "<N>")
  # so we only count real emissions.
  summaries=$(grep -oE 'verdicts_this_session=[0-9]+' "$log" 2>/dev/null || true)
  count=$(printf '%s\n' "$summaries" | grep -c . || true)
  sum=$(printf '%s\n' "$summaries" | awk -F= '{s+=$2} END {print s+0}')
  if [ "$count" -gt 0 ]; then
    mean=$(awk -v s="$sum" -v c="$count" 'BEGIN {if (c>0) printf "%.1f", s/c; else print "-"}')
  else
    mean="-"
  fi
  last_line=$(printf '%s\n' "$summaries" | tail -1)
  cur_sess=$(tail -80 "$log" | grep -oE 'verdicts_this_session=[0-9]+' | tail -1 || true)

  total=$((total + sum))
  printf '%-22s  %8d  %12s  %12s  %s\n' "$name" "$sum" "$mean" "${last_line:-none}" "${cur_sess:-in-progress}"
done

echo
echo "TOTAL verdicts across all agents: $total"
echo "Target per agent per hour: 100  (=> 500/hr across 5 agents)"
