#!/usr/bin/env bash
# Second window: source env, refresh vault queue mirror, Mission Control (live JSON).
set -euo pipefail
if [[ -f "$HOME/.claude/faerie-env.sh" ]]; then
  # shellcheck disable=SC1090
  . "$HOME/.claude/faerie-env.sh"
fi
PY="$(command -v python3 || command -v python)"
export_script="$HOME/.claude/hooks/state/export_queue_to_vault.py"
if [[ -f "$export_script" ]]; then
  echo "Refreshing vault queue mirror..."
  "$PY" "$export_script"
fi
db="$HOME/.claude/dashboard.py"
if [[ ! -f "$db" ]]; then
  echo "ERROR: $db missing — run install-faerie.sh (core) first." >&2
  exit 1
fi
echo "Starting Mission Control..."
exec "$PY" "$db" --watch
