#!/usr/bin/env bash
# 9x_honey_sync_schedule.sh — Scheduled HONEY sync runner
#
# TIER: 9x_ (utilities)
# REPLACES: manual sync invocations
# METRIC: honey_sync_coc_entries (target: 1 per run, 24+/day)
# LOAD: light
#
# Runs 9x_honey_sync_to_vault.py for today's date with audience=all.
# Writes a COC entry to forensics/{date}/coc-entries/ for every run.
# On sync failure (exit code non-zero), emits compass_edge=W manifest.
#
# Cron example (hourly):
#   0 * * * * /bin/bash /path/to/faerie-vault/scripts/9x_honey_sync_schedule.sh >> /tmp/honey-sync.log 2>&1
#
# On-demand:
#   bash scripts/9x_honey_sync_schedule.sh
#   bash scripts/9x_honey_sync_schedule.sh --date 2026-04-28 --audience economist

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve repo root (script lives at {repo}/scripts/9x_honey_sync_schedule.sh)
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SCRIPTS_DIR="${REPO_ROOT}/scripts"
FORENSICS_ROOT="${REPO_ROOT}/forensics"

# Defaults
DATE="$(date -u +%Y-%m-%d)"
AUDIENCE="all"

# Parse flags
while [[ $# -gt 0 ]]; do
    case "$1" in
        --date)     DATE="$2";     shift 2 ;;
        --audience) AUDIENCE="$2"; shift 2 ;;
        *)          shift ;;
    esac
done

TIMESTAMP="$(date -u +%H-%M-%SZ)"
TS_ISO="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
COC_DIR="${FORENSICS_ROOT}/${DATE}/coc-entries"
mkdir -p "${COC_DIR}"

# Counter: avoid collision if run multiple times in same second
COUNTER=1
COC_FILE="${COC_DIR}/${TIMESTAMP}_coc-entry_honey-sync-schedule_honey-sync_$(printf '%03d' ${COUNTER}).jsonl"
while [[ -f "${COC_FILE}" ]]; do
    COUNTER=$((COUNTER + 1))
    COC_FILE="${COC_DIR}/${TIMESTAMP}_coc-entry_honey-sync-schedule_honey-sync_$(printf '%03d' ${COUNTER}).jsonl"
done

echo "[honey-sync-schedule] ${TS_ISO} date=${DATE} audience=${AUDIENCE}"

# ---------------------------------------------------------------------------
# Run the sync script
# ---------------------------------------------------------------------------
EXIT_CODE=0
python3 "${SCRIPTS_DIR}/9x_honey_sync_to_vault.py" \
    --date "${DATE}" \
    --audience "${AUDIENCE}" \
    2>&1 || EXIT_CODE=$?

SYNC_RESULT="success"
COMPASS_EDGE="S"
if [[ "${EXIT_CODE}" -ne 0 ]]; then
    SYNC_RESULT="failed"
    COMPASS_EDGE="W"
    echo "[honey-sync-schedule] WARN: sync exited ${EXIT_CODE} — compass W, needs manual review"
fi

# ---------------------------------------------------------------------------
# Write COC entry (JSONL append, one object per line)
# ---------------------------------------------------------------------------
printf '{"timestamp_utc":"%s","operation":"honey-sync-schedule","tool":"9x_honey_sync_to_vault.py","date":"%s","audience":"%s","exit_code":%d,"sync_result":"%s","compass_edge":"%s","agent":"honey-sync-schedule"}\n' \
    "${TS_ISO}" "${DATE}" "${AUDIENCE}" "${EXIT_CODE}" "${SYNC_RESULT}" "${COMPASS_EDGE}" \
    >> "${COC_FILE}"

echo "[honey-sync-schedule] COC entry written: ${COC_FILE}"

# ---------------------------------------------------------------------------
# On error: ensure a West manifest exists for manual review routing
# (prescan gate: skip if manifest already written by 9x_honey_sync_to_vault.py)
# ---------------------------------------------------------------------------
if [[ "${COMPASS_EDGE}" == "W" ]]; then
    MANIFESTS_DIR="${FORENSICS_ROOT}/manifests/${DATE}"
    mkdir -p "${MANIFESTS_DIR}"

    # Prescan: look for an existing West manifest from this session
    EXISTING_W=$(find "${MANIFESTS_DIR}" -name "*honey-sync*" -newer "${MANIFESTS_DIR}" -maxdepth 1 2>/dev/null | head -1 || true)
    if [[ -n "${EXISTING_W}" ]]; then
        echo "[honey-sync-schedule] prescan: West manifest already exists (${EXISTING_W}), skip duplicate write"
    else
        MANIFEST_COUNTER=1
        MANIFEST_FILE="${MANIFESTS_DIR}/${TIMESTAMP}_manifest_honey-sync-${DATE}_honey-sync_$(printf '%03d' ${MANIFEST_COUNTER}).json"
        while [[ -f "${MANIFEST_FILE}" ]]; do
            MANIFEST_COUNTER=$((MANIFEST_COUNTER + 1))
            MANIFEST_FILE="${MANIFESTS_DIR}/${TIMESTAMP}_manifest_honey-sync-${DATE}_honey-sync_$(printf '%03d' ${MANIFEST_COUNTER}).json"
        done

        printf '{
  "task_id": "honey-sync-%s",
  "agent_type": "honey-sync",
  "investigation_label": "honey-version-sync",
  "timestamp_utc": "%s",
  "dashboard_line": "honey-sync FAILED date=%s aud=%s exit=%d — compass W",
  "compass_edge": "W",
  "quality_score": 0.0,
  "belief_index": 0.90,
  "next_task_queued": "honey-sync-manual-review",
  "prescan_decision": "passed — schedule run triggered sync failure",
  "sync_result": "%s",
  "exit_code": %d,
  "audience_filter": "%s"
}\n' \
            "${DATE}" "${TS_ISO}" "${DATE}" "${AUDIENCE}" "${EXIT_CODE}" \
            "${SYNC_RESULT}" "${EXIT_CODE}" "${AUDIENCE}" \
            > "${MANIFEST_FILE}"

        echo "[honey-sync-schedule] West manifest written: ${MANIFEST_FILE}"
    fi

    exit 1
fi

echo "[honey-sync-schedule] done — compass S"
exit 0
