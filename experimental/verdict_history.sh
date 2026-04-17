#!/usr/bin/env bash
# Background helper: every minute, append one line per agent with the
# current cumulative verdict total to verdict_history.tsv. Later we can
# compute per-hour rate by diffing rows.

set -e
dir="agents"
history="verdict_history.tsv"

if [ ! -f "$history" ]; then
  echo -e "timestamp\tagent\tcumulative_verdicts" > "$history"
fi

while true; do
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  for agent_dir in "$dir"/*/; do
    name=$(basename "$agent_dir")
    log="$agent_dir/agent.log"
    [ -f "$log" ] || continue
    sum=$(grep -oE 'verdicts_this_session=[0-9]+' "$log" 2>/dev/null \
      | awk -F= '{s+=$2} END {print s+0}')
    printf '%s\t%s\t%s\n' "$ts" "$name" "$sum" >> "$history"
  done
  sleep 60
done
