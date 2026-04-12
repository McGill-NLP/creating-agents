#!/bin/bash
# Runs agent_stats.py every 5 minutes (300 seconds), logging to a file.
# Designed to be run inside a dedicated tmux session, e.g.:
#   tmux new-session -d -s agent-stats-cron 'bash tools/agent_stats_loop.sh'
#
# Inspect running state:  tmux attach -t agent-stats-cron
# Stop:                   tmux kill-session -t agent-stats-cron
#
# The interval can be overridden via the first argument:
#   bash tools/agent_stats_loop.sh 60      # every 60s
set -euo pipefail

INTERVAL="${1:-300}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STDOUT_LOG="$REPO_ROOT/logs/agent_stats_loop.stdout"
STATS_SCRIPT="$REPO_ROOT/tools/agent_stats.py"

mkdir -p "$REPO_ROOT/logs"

echo "[agent-stats-cron] starting at $(date -u +%Y-%m-%dT%H:%M:%SZ), interval=${INTERVAL}s" >> "$STDOUT_LOG"

while true; do
    python3 "$STATS_SCRIPT" --print >> "$STDOUT_LOG" 2>&1 || \
        echo "[agent-stats-cron] $(date -u +%Y-%m-%dT%H:%M:%SZ) agent_stats.py failed" >> "$STDOUT_LOG"
    sleep "$INTERVAL"
done
