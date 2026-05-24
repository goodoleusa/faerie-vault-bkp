#!/usr/bin/env bash
# =============================================================================
# CyberOps-UNIFIED Vault — One-Click Installer (Bash)
# Supports: Linux, macOS, WSL2 on Windows
#
# Usage:
#   bash install.sh /path/to/install/dir
#   bash install.sh    # installs to ./CyberOps-UNIFIED in current dir
#
# What this installs:
#   - Folder structure (00-SHARED, 10-Investigations, 20-Entities, etc.)
#   - Obsidian config (.obsidian folder with plugins, themes, snippets)
#   - QuickAdd macro library (quickadd-macros.js + plugin data)
#   - Blueprint templates (all .blueprint files)
#   - Note templates (Templates/ folder)
#   - Theme CSS snippets (agent-formatting.css + others)
#   - Onboarding content (ONBOARDING/ start-here guide)
#   - Placeholder files for agent write paths
# =============================================================================

set -euo pipefail

# ── Colours ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'
BOLD='\033[1m'; RESET='\033[0m'
info()    { echo -e "${CYAN}[info]${RESET}  $*"; }
ok()      { echo -e "${GREEN}[ok]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[warn]${RESET}  $*"; }
die()     { echo -e "${RED}[error]${RESET} $*" >&2; exit 1; }

# ── Arg handling ──────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="${1:-${PWD}/CyberOps-UNIFIED}"
VAULT_ROOT="$(realpath -m "$VAULT_ROOT")"   # resolve without requiring existence

echo ""
echo -e "${BOLD}CyberOps-UNIFIED Vault Installer${RESET}"
echo "────────────────────────────────────────────────────────"
info "Source: $SCRIPT_DIR"
info "Target: $VAULT_ROOT"
echo ""

# Safety: refuse to clobber non-empty non-vault dir
if [[ -d "$VAULT_ROOT" ]] && [[ -n "$(ls -A "$VAULT_ROOT" 2>/dev/null)" ]]; then
    if [[ ! -d "$VAULT_ROOT/.obsidian" ]] && [[ ! -f "$VAULT_ROOT/VAULT-RULES.md" ]]; then
        die "Target exists and is not an Obsidian vault. Aborting to prevent data loss.\nPick a new path or pass an existing vault dir."
    fi
    warn "Target exists — will merge/overwrite config files only."
fi

# ── Step 1: Folder structure ──────────────────────────────────────────────────
info "Creating folder structure..."

declare -a FOLDERS=(
    "00-Inbox"
    "00-SHARED/Agent-Outbox"
    "00-SHARED/Human-Inbox/findings"
    "00-SHARED/Human-Inbox/flags"
    "00-SHARED/Human-Inbox/connections"
    "00-SHARED/Human-Inbox/narratives"
    "00-SHARED/Human-Inbox/devdocs"
    "00-SHARED/Human-Inbox/collab"
    "00-SHARED/Droplets"
    "00-SHARED/Hive"
    "00-SHARED/Dashboards/scripts"
    "00-SHARED/ONBOARDING"
    "00-SHARED/Queue"
    "10-Investigations"
    "20-Entities/People"
    "20-Entities/IPs"
    "20-Entities/Domains"
    "20-Entities/Organizations"
    "25-Networks"
    "30-Evidence/tier-T1"
    "30-Evidence/tier-T2"
    "30-Evidence/tier-T3"
    "30-Evidence/tier-T4"
    "40-Intelligence"
    "50-Financial"
    "60-Chronology"
    "70-Sources"
    "99-Archives"
    "01-Memories/shared"
    "01-Memories/agents"
    "01-PROTECTED"
    "Blueprints"
    "Templates"
    "Workbench"
    "Dashboards"
    "Excalidraw"
    "Tags"
)

for folder in "${FOLDERS[@]}"; do
    mkdir -p "$VAULT_ROOT/$folder"
done
ok "Folder structure created (${#FOLDERS[@]} directories)"

# ── Step 2: .obsidian config ──────────────────────────────────────────────────
info "Copying Obsidian config..."

SRC_OBSIDIAN="$SCRIPT_DIR/vault-template/.obsidian"
if [[ -d "$SRC_OBSIDIAN" ]]; then
    cp -r "$SRC_OBSIDIAN/." "$VAULT_ROOT/.obsidian/"
    # Remove sync-conflict files (personal machine artifacts)
    find "$VAULT_ROOT/.obsidian" -name "*.sync-conflict*" -delete 2>/dev/null || true
    ok ".obsidian config copied"
else
    warn ".obsidian source not found at $SRC_OBSIDIAN — skipping plugin config"
    warn "You will need to manually install and configure plugins (see SETUP.md)"
    mkdir -p "$VAULT_ROOT/.obsidian/plugins"
    mkdir -p "$VAULT_ROOT/.obsidian/snippets"
    mkdir -p "$VAULT_ROOT/.obsidian/themes"
fi

# ── Step 3: Blueprints ────────────────────────────────────────────────────────
info "Copying blueprint templates..."

SRC_BLUEPRINTS="$SCRIPT_DIR/vault-template/Blueprints"
if [[ -d "$SRC_BLUEPRINTS" ]]; then
    cp "$SRC_BLUEPRINTS"/*.blueprint "$VAULT_ROOT/Blueprints/" 2>/dev/null || true
    cp "$SRC_BLUEPRINTS"/*.md "$VAULT_ROOT/Blueprints/" 2>/dev/null || true
    BLUEPRINT_COUNT=$(ls "$VAULT_ROOT/Blueprints/" 2>/dev/null | wc -l)
    ok "Blueprints installed ($BLUEPRINT_COUNT files)"
else
    warn "Blueprints source not found — skipping"
fi

# ── Step 4: Templates ─────────────────────────────────────────────────────────
info "Copying note templates..."

SRC_TEMPLATES="$SCRIPT_DIR/vault-template/Templates"
if [[ -d "$SRC_TEMPLATES" ]]; then
    # Copy .md templates (skip hidden .space folder)
    cp "$SRC_TEMPLATES"/*.md "$VAULT_ROOT/Templates/" 2>/dev/null || true
    TEMPLATE_COUNT=$(ls "$VAULT_ROOT/Templates/"*.md 2>/dev/null | wc -l)
    ok "Templates installed ($TEMPLATE_COUNT files)"
else
    warn "Templates source not found — skipping"
fi

# ── Step 5: QuickAdd macro JS ─────────────────────────────────────────────────
info "Installing QuickAdd macro library..."

SRC_MACROS="$SCRIPT_DIR/vault-template/00-SHARED/Dashboards/scripts/quickadd-macros.js"
if [[ -f "$SRC_MACROS" ]]; then
    mkdir -p "$VAULT_ROOT/00-SHARED/Dashboards/scripts"
    cp "$SRC_MACROS" "$VAULT_ROOT/00-SHARED/Dashboards/scripts/"
    ok "QuickAdd macro library installed"
else
    warn "quickadd-macros.js not found — skipping"
fi

# ── Step 6: ONBOARDING content ────────────────────────────────────────────────
info "Installing onboarding guide..."

SRC_ONBOARDING="$SCRIPT_DIR/vault-template/00-SHARED/ONBOARDING"
if [[ -d "$SRC_ONBOARDING" ]]; then
    cp "$SRC_ONBOARDING/00-START-HERE.md" "$VAULT_ROOT/00-SHARED/ONBOARDING/" 2>/dev/null || true
    ok "Onboarding guide installed"
else
    # Create minimal start-here from embedded template
    cat > "$VAULT_ROOT/00-SHARED/ONBOARDING/00-START-HERE.md" << 'ONBOARDING_EOF'
---
type: onboarding
status: active
tags: [setup, faerie2]
title: Vault Quick Start
---

# Quick Start

## Where Things Live

| Folder | Purpose |
|--------|---------|
| `00-SHARED/Agent-Outbox/` | Agents write here — pick up outputs |
| `00-SHARED/Human-Inbox/` | Routed findings for human review |
| `10-Investigations/` | Active investigation notes |
| `30-Evidence/tier-T1/` | Highest-confidence evidence |
| `Blueprints/` | Formatting templates for agent output |
| `Templates/` | QuickAdd note templates |

## First Steps

1. Enable community plugins (Settings → Community Plugins → Disable Safe Mode)
2. Install: QuickAdd, Dataview, Blueprint
3. Read `SETUP.md` for configuration details
4. Test by creating a file in `00-SHARED/Agent-Outbox/`

ONBOARDING_EOF
    ok "Minimal onboarding guide created"
fi

# ── Step 7: Root vault files ──────────────────────────────────────────────────
info "Installing vault index files..."

SRC_ROOT_FILES=(
    "VAULT-RULES.md"
    "VAULT-INDEX.md"
    "HOME.md"
    "README.md"
)
for f in "${SRC_ROOT_FILES[@]}"; do
    SRC="$SCRIPT_DIR/vault-template/$f"
    if [[ -f "$SRC" ]]; then
        cp "$SRC" "$VAULT_ROOT/$f"
    fi
done

# Always install SETUP.md from installer dir
if [[ -f "$SCRIPT_DIR/SETUP.md" ]]; then
    cp "$SCRIPT_DIR/SETUP.md" "$VAULT_ROOT/SETUP.md"
fi
ok "Vault root files installed"

# ── Step 8: Placeholder / init files ─────────────────────────────────────────
info "Initializing write-path placeholders..."

# Agent write paths need to exist for autopoke to scan
touch "$VAULT_ROOT/00-SHARED/Agent-Outbox/.gitkeep"
touch "$VAULT_ROOT/00-SHARED/Droplets/.gitkeep"
touch "$VAULT_ROOT/00-SHARED/Human-Inbox/findings/.gitkeep"
touch "$VAULT_ROOT/00-SHARED/Human-Inbox/flags/.gitkeep"

# Log files for autopoke
touch "$VAULT_ROOT/00-SHARED/Dashboards/scripts/autopoke-log.jsonl"
touch "$VAULT_ROOT/00-SHARED/Dashboards/scripts/autopoke-errors.jsonl"

ok "Write-path placeholders created"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}Vault installed successfully!${RESET}"
echo "────────────────────────────────────────────────────────"
echo ""
echo -e "${BOLD}Next steps:${RESET}"
echo "  1. Open vault in Obsidian:  File → Open Vault → $VAULT_ROOT"
echo "  2. Enable community plugins: Settings → Community Plugins → Disable Safe Mode"
echo "  3. Install plugins (see SETUP.md): QuickAdd, Blueprint, Dataview"
echo "  4. Import QuickAdd config:  Settings → QuickAdd → Manage Macros → load quickadd-macros.js"
echo "  5. Read SETUP.md in vault root for full configuration"
echo ""
echo -e "  Vault root: ${CYAN}$VAULT_ROOT${RESET}"
echo ""
