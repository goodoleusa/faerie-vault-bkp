#!/usr/bin/env bash
# faerie + collab env installer (macOS / Linux / WSL).
#
# Bundles (memory ships only inside full combined — no separate memory install SKU):
#   --core  → releases/<os>/orchestration/.claude/  (OSS: queue, dashboard, hooks, no memory module)
#   --full  → releases/<os>/.claude/              (paid: s2 --profile full = orchestration + memory)
#
# Usage:
#   ./scripts/install/install-faerie.sh
#   RELEASE_TARGET=macos ./scripts/install/install-faerie.sh --core
#   RELEASE_TARGET=macos ./scripts/install/install-faerie.sh --full
#   ./scripts/install/install-faerie.sh --env-only

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLOWSEARCH_ROOT="${FLOWSEARCH_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
export FLOWSEARCH_ROOT
RELEASE_TARGET="${RELEASE_TARGET:-linux}"
DST="$HOME/.claude"
MODE="${1:-interactive}"

backup_claude() {
  if [[ -d "$DST" ]]; then
    local stamp
    stamp=$(date +%Y%m%d-%H%M%S)
    echo "Backing up $DST -> $DST.backup-$stamp"
    cp -a "$DST" "$DST.backup-$stamp"
  fi
}

install_orchestration() {
  local src="$FLOWSEARCH_ROOT/releases/$RELEASE_TARGET/orchestration/.claude"
  if [[ ! -d "$src" ]]; then
    echo "ERROR: $src not found — run from repo root: python scripts/0b_build_release_bundles.py --profile all" >&2
    exit 1
  fi
  mkdir -p "$DST"
  echo "Copying $src -> $DST (core orchestration OSS)"
  cp -R "$src"/* "$DST"/
  echo "Core orchestration install done."
}

install_full() {
  local src="$FLOWSEARCH_ROOT/releases/$RELEASE_TARGET/.claude"
  if [[ ! -d "$src" ]]; then
    echo "ERROR: $src not found — run from repo root: python scripts/0b_build_release_bundles.py --profile all" >&2
    exit 1
  fi
  mkdir -p "$DST"
  echo "Copying $src -> $DST (full combined: orchestration + memory)"
  cp -R "$src"/* "$DST"/
  echo "Full combined install done."
}

write_env_files() {
  mkdir -p "$DST"
  local proj="${FAERIE_PROJECT_ROOT:-}"
  local vault="${FAERIE_VAULT_SHARED:-$FLOWSEARCH_ROOT/ObsidianVault/00-SHARED}"
  local hooks="${CLAUDE_HOOKS_STATE:-}"
  local drops="${VAULT_DROPS:-}"
  export FLOWSEARCH_ROOT
  FAERIE_PROJECT_ROOT="$proj" FAERIE_VAULT_SHARED="$vault" \
    CLAUDE_HOOKS_STATE="$hooks" VAULT_DROPS="$drops" \
    python3 <<'PY'
import json, os
dst = os.path.expanduser("~/.claude")
flow = os.environ.get("FLOWSEARCH_ROOT", "")
data = {
    "flowsearch_repo": flow,
    "faerie_project_root": os.environ.get("FAERIE_PROJECT_ROOT", ""),
    "faerie_vault_shared": os.environ.get("FAERIE_VAULT_SHARED", ""),
    "claude_hooks_state": os.environ.get("CLAUDE_HOOKS_STATE", ""),
    "vault_drops": os.environ.get("VAULT_DROPS", ""),
}
path = os.path.join(dst, "faerie-env.json")
os.makedirs(dst, exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print("Wrote", path)
sh_path = os.path.join(dst, "faerie-env.sh")
lines = ["# Generated — source: . ~/.claude/faerie-env.sh", ""]
for envk, jk in [
    ("FAERIE_PROJECT_ROOT", "faerie_project_root"),
    ("FAERIE_VAULT_SHARED", "faerie_vault_shared"),
    ("CLAUDE_HOOKS_STATE", "claude_hooks_state"),
    ("VAULT_DROPS", "vault_drops"),
]:
    v = (data.get(jk) or "").strip()
    if v:
        lines.append(f'export {envk}="{v}"')
with open(sh_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("Wrote", sh_path)
PY
}

copy_start_script() {
  if [[ -f "$SCRIPT_DIR/start-faerie-workstation.sh" ]]; then
    cp "$SCRIPT_DIR/start-faerie-workstation.sh" "$DST/"
    chmod +x "$DST/start-faerie-workstation.sh"
    echo "Installed $DST/start-faerie-workstation.sh"
  fi
}

case "${MODE:-interactive}" in
  --core)
    backup_claude
    install_orchestration
    ;;
  --full)
    backup_claude
    install_full
    ;;
  --env-only)
    write_env_files
    copy_start_script
    ;;
  interactive)
    echo "=== faerie + collab (interactive) ==="
    read -r -p "Install bundle to ~/.claude? [O]rchestration OSS (default) | [F]ull paid+memory | [N]one: " bundle
    bundle="${bundle:-O}"
    case "${bundle:0:1}" in
      f|F)
        backup_claude
        install_full
        ;;
      n|N) ;;
      *)
        backup_claude
        install_orchestration
        ;;
    esac
    read -r -p "FAERIE_PROJECT_ROOT (optional): " FAERIE_PROJECT_ROOT
    read -r -p "FAERIE_VAULT_SHARED [$FLOWSEARCH_ROOT/ObsidianVault/00-SHARED]: " _v
    export FAERIE_VAULT_SHARED="${_v:-$FLOWSEARCH_ROOT/ObsidianVault/00-SHARED}"
    read -r -p "CLAUDE_HOOKS_STATE (optional): " CLAUDE_HOOKS_STATE
    read -r -p "VAULT_DROPS (optional): " VAULT_DROPS
    export FAERIE_PROJECT_ROOT FAERIE_VAULT_SHARED CLAUDE_HOOKS_STATE VAULT_DROPS
    write_env_files
    copy_start_script
    ;;
  *)
    echo "Usage: $0 [--core | --full | --env-only | interactive]" >&2
    echo "  --core   OSS orchestration only (releases/<os>/orchestration/.claude)" >&2
    echo "  --full   paid combined drop incl. memory (releases/<os>/.claude)" >&2
    exit 1
    ;;
esac

echo ""
echo "Syncthing: share ONLY ObsidianVault/00-SHARED — see ObsidianVault/START-COLLAB.md"
