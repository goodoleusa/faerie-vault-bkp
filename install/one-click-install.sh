#!/usr/bin/env bash
# =============================================================================
# faerie2 + faerie-vault + ct-vault — One-Click Install Script
# Version: 1.0.0  |  Mission: vault-infrastructure-overhaul
#
# Usage:
#   bash one-click-install.sh                    # interactive, defaults to ~/Obsidian
#   bash one-click-install.sh /path/to/install   # non-interactive install dir
#   VAULT_DIR=~/MyVaults bash one-click-install.sh
#
# What this installs:
#   1. faerie2         — orchestration engine (Claude Code)
#   2. faerie-vault    — portable publication vault (Obsidian)
#   3. ct-vault        — investigation vault (Obsidian)
#   4. Obsidian plugin configs (.obsidian folder wired for all required plugins)
#   5. faerie-env.json — environment variable glue
#   6. Symlinks        — canonical vault path resolution
#
# Supports: Linux, macOS, WSL2/Windows
# Target runtime: <2 minutes on a typical broadband connection
# =============================================================================

set -euo pipefail

# ── Colours ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}[info]${RESET}  $*"; }
ok()      { echo -e "${GREEN}[ok]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[warn]${RESET}  $*"; }
die()     { echo -e "${RED}[error]${RESET} $*" >&2; exit 1; }
step()    { echo -e "\n${BOLD}── $* ──${RESET}"; }

INSTALL_START=$(date +%s)

# ── OS Detection ──────────────────────────────────────────────────────────────
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif grep -qi microsoft /proc/version 2>/dev/null; then
        OS="wsl"
    elif [[ "$OSTYPE" == "linux"* ]]; then
        OS="linux"
    else
        OS="unknown"
    fi
    info "Detected OS: $OS"
}

# ── Obsidian Detection ────────────────────────────────────────────────────────
check_obsidian() {
    local found=0

    if command -v obsidian &>/dev/null; then
        found=1
    elif [[ "$OS" == "macos" ]] && [[ -d "/Applications/Obsidian.app" ]]; then
        found=1
    elif [[ "$OS" == "wsl" ]]; then
        # Check common Windows install locations via /mnt/c
        if ls /mnt/c/Users/*/AppData/Local/Obsidian/Obsidian.exe 2>/dev/null | head -1 | grep -q Obsidian; then
            found=1
        fi
    elif [[ "$OS" == "linux" ]]; then
        if ls ~/.local/share/applications/obsidian*.desktop 2>/dev/null | grep -q obsidian || \
           ls /opt/Obsidian* 2>/dev/null | grep -q Obsidian || \
           ls ~/Applications/Obsidian* 2>/dev/null | grep -q Obsidian; then
            found=1
        fi
    fi

    if [[ $found -eq 1 ]]; then
        ok "Obsidian installation found"
    else
        warn "Obsidian not detected. Install from https://obsidian.md/download before opening vaults."
        warn "Installation will continue — vault files will be ready when you install Obsidian."
    fi
}

# ── Dependency Check ──────────────────────────────────────────────────────────
check_deps() {
    local missing=()

    command -v git &>/dev/null      || missing+=("git")
    command -v python3 &>/dev/null  || missing+=("python3")

    if [[ ${#missing[@]} -gt 0 ]]; then
        die "Missing required tools: ${missing[*]}\nInstall them then re-run this script."
    fi
    ok "Dependencies satisfied (git, python3)"
}

# ── Repo URLs (edit these for your fork) ─────────────────────────────────────
FAERIE2_URL="${FAERIE2_URL:-https://github.com/goodoleusa/faerie2.git}"
FAERIE_VAULT_URL="${FAERIE_VAULT_URL:-https://github.com/goodoleusa/faerie-vault.git}"
CT_VAULT_URL="${CT_VAULT_URL:-https://github.com/goodoleusa/ct-vault.git}"

# ── Vault Storage Location ────────────────────────────────────────────────────
resolve_install_dir() {
    if [[ -n "${1:-}" ]]; then
        INSTALL_DIR="$(realpath -m "$1")"
        info "Install directory (arg): $INSTALL_DIR"
        return
    fi

    if [[ -n "${VAULT_DIR:-}" ]]; then
        INSTALL_DIR="$(realpath -m "$VAULT_DIR")"
        info "Install directory (env): $INSTALL_DIR"
        return
    fi

    # Interactive prompt
    local default_dir="$HOME/Obsidian"
    echo ""
    echo -e "${BOLD}Where would you like to install the faerie vaults?${RESET}"
    echo -e "  Default: ${CYAN}$default_dir${RESET}"
    read -r -p "  Install path [press Enter for default]: " user_path
    INSTALL_DIR="${user_path:-$default_dir}"
    INSTALL_DIR="$(realpath -m "$INSTALL_DIR")"
    info "Install directory: $INSTALL_DIR"
}

# ── Clone Repos ───────────────────────────────────────────────────────────────
clone_repos() {
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"

    local repos=(
        "faerie2:$FAERIE2_URL"
        "faerie-vault:$FAERIE_VAULT_URL"
        "ct-vault:$CT_VAULT_URL"
    )

    for entry in "${repos[@]}"; do
        local name="${entry%%:*}"
        local url="${entry##*:}"

        if [[ -d "$name/.git" ]]; then
            info "$name already cloned — pulling latest..."
            git -C "$name" pull --ff-only 2>/dev/null || warn "Pull failed for $name (may have local changes)"
        else
            info "Cloning $name..."
            if git clone --depth=1 "$url" "$name" 2>/dev/null; then
                ok "Cloned $name"
            else
                warn "Could not clone $name from $url"
                warn "Check URL or network. You can manually clone later."
                mkdir -p "$name"
            fi
        fi
    done
}

# ── Obsidian Plugin Config ────────────────────────────────────────────────────
install_plugin_configs() {
    local vault_dir="$INSTALL_DIR/faerie-vault"

    # Install plugin configs from vault-install template if present
    local template_obsidian="$INSTALL_DIR/faerie2/vault-install/vault-template/.obsidian"
    if [[ -d "$template_obsidian" ]]; then
        info "Installing Obsidian plugin configs from vault-install template..."
        mkdir -p "$vault_dir/.obsidian"
        cp -r "$template_obsidian/." "$vault_dir/.obsidian/"
        find "$vault_dir/.obsidian" -name "*.sync-conflict*" -delete 2>/dev/null || true
        ok "Plugin configs installed from template"
    else
        info "Generating minimal Obsidian plugin configs..."
        install_minimal_plugin_configs "$vault_dir"
    fi

    # Also apply to ct-vault if it exists as a real vault
    local ct_vault_dir="$INSTALL_DIR/ct-vault"
    if [[ -d "$ct_vault_dir" ]]; then
        mkdir -p "$ct_vault_dir/.obsidian"
        # ct-vault gets its own minimal config (investigation data vault)
        install_minimal_plugin_configs "$ct_vault_dir"
        ok "Plugin configs also applied to ct-vault"
    fi
}

install_minimal_plugin_configs() {
    local vault_dir="$1"
    mkdir -p "$vault_dir/.obsidian/plugins"
    mkdir -p "$vault_dir/.obsidian/snippets"
    mkdir -p "$vault_dir/.obsidian/themes"

    # app.json — core vault settings
    cat > "$vault_dir/.obsidian/app.json" << 'APP_EOF'
{
  "useMarkdownLinks": false,
  "newLinkFormat": "relative",
  "attachmentFolderPath": "Assets",
  "showUnsupportedFiles": false,
  "defaultViewMode": "preview",
  "vimMode": false,
  "foldHeading": false,
  "foldIndent": true,
  "showLineNumber": false,
  "readableLineLength": true,
  "strictLineBreaks": false,
  "showFrontmatter": false,
  "livePreview": true
}
APP_EOF

    # community-plugins.json — required plugin list
    cat > "$vault_dir/.obsidian/community-plugins.json" << 'PLUGINS_EOF'
[
  "dataview",
  "breadcrumbs",
  "quickadd",
  "obsidian-meta-bind-plugin",
  "obsidian-excalidraw-plugin",
  "mrj-text-expand",
  "obsidian-blueprints"
]
PLUGINS_EOF

    # core-plugins.json
    cat > "$vault_dir/.obsidian/core-plugins.json" << 'CORE_EOF'
{
  "file-explorer": true,
  "global-search": true,
  "switcher": true,
  "graph": true,
  "backlink": true,
  "outgoing-link": true,
  "tag-pane": true,
  "page-preview": true,
  "daily-notes": true,
  "templates": true,
  "note-composer": true,
  "command-palette": true,
  "open-with-default-app": true,
  "outline": true,
  "word-count": true
}
CORE_EOF

    # Dataview plugin config
    mkdir -p "$vault_dir/.obsidian/plugins/dataview"
    cat > "$vault_dir/.obsidian/plugins/dataview/data.json" << 'DV_EOF'
{
  "enableDataviewJs": false,
  "enableInlineDataview": true,
  "enableInlineDataviewJs": false,
  "prettyRenderInlineFields": true,
  "tableIdColumnName": "File",
  "tableGroupColumnName": "Group",
  "refreshInterval": 2500,
  "maxRecursiveRenderDepth": 4,
  "defaultDateFormat": "MMMM dd, yyyy",
  "defaultDateTimeFormat": "h:mm a - MMMM dd, yyyy",
  "dataviewJsKeyword": "dataviewjs",
  "inlineQueryPrefix": "=",
  "inlineJsQueryPrefix": "$=",
  "allowHtml": true
}
DV_EOF

    # Breadcrumbs plugin config — compass-aware hierarchy
    mkdir -p "$vault_dir/.obsidian/plugins/breadcrumbs"
    cat > "$vault_dir/.obsidian/plugins/breadcrumbs/data.json" << 'BC_EOF'
{
  "userHiers": [
    {
      "up": ["north", "parent"],
      "same": ["east", "west"],
      "down": ["south", "child"],
      "next": ["south"],
      "prev": ["north"]
    }
  ],
  "impliedRelations": {
    "siblingIdentity": false,
    "parentOfSibling": false,
    "siblingOfParent": false
  },
  "showBCs": true,
  "showBCsInEditLPMode": true,
  "showTrail": true,
  "showGrid": false,
  "showPrevNext": true,
  "showRefreshButton": false,
  "noPathMessage": "No path found",
  "trailSeperator": "  >  ",
  "respectReadableLineLength": true,
  "hideTrailIfNoPath": false,
  "fieldSuggestor": true,
  "openMatrixOnLoad": true,
  "openStatsOnLoad": false,
  "showAll": false,
  "debugMode": false,
  "superDebugMode": false
}
BC_EOF

    # QuickAdd plugin config — auto-routing
    mkdir -p "$vault_dir/.obsidian/plugins/quickadd"
    cat > "$vault_dir/.obsidian/plugins/quickadd/data.json" << 'QA_EOF'
{
  "choices": [
    {
      "id": "faerie-daily-note",
      "name": "Daily Note",
      "type": "Template",
      "command": true,
      "templatePath": "Templates/daily-note-template.md",
      "fileNameFormat": {
        "enabled": true,
        "format": "{{DATE:YYYY-MM-DD}}-daily"
      },
      "folder": {
        "enabled": true,
        "folder": "00-Inbox",
        "chooseWhenCreatingNote": false
      },
      "appendLink": false,
      "openFile": true,
      "openFileInNewTab": {
        "enabled": false,
        "direction": "vertical",
        "focus": true
      },
      "fileExistsMode": "Append to bottom of file"
    },
    {
      "id": "faerie-mission-note",
      "name": "Mission Note",
      "type": "Template",
      "command": true,
      "templatePath": "Templates/mission-note-template.md",
      "fileNameFormat": {
        "enabled": true,
        "format": "{{DATE:YYYYMMDD}}-{{VALUE:Note name}}"
      },
      "folder": {
        "enabled": true,
        "folder": "10-Investigations",
        "chooseWhenCreatingNote": false
      },
      "appendLink": false,
      "openFile": true,
      "openFileInNewTab": {
        "enabled": false,
        "direction": "vertical",
        "focus": true
      },
      "fileExistsMode": "Increment the file name"
    }
  ],
  "macros": [],
  "templateFolderPath": "Templates",
  "devMode": false,
  "templateEngine": "Eta",
  "announceUpdates": false
}
QA_EOF

    # compass-graph-colors.css snippet — N=blue S=green E=yellow W=red
    cat > "$vault_dir/.obsidian/snippets/compass-graph-colors.css" << 'CSS_EOF'
/* faerie2 Compass Graph Colors — mission bearing visualization */
/* North (predecessor/unblock) = blue */
.graph-view.color-arrow[data-edge-field="north"],
.graph-view.color-arrow[data-edge-field="parent"] {
  color: #4a90e2;
}
/* South (downstream/ship) = green */
.graph-view.color-arrow[data-edge-field="south"],
.graph-view.color-arrow[data-edge-field="child"] {
  color: #2ecc71;
}
/* East (parallel sister work) = yellow */
.graph-view.color-arrow[data-edge-field="east"],
.graph-view.color-arrow[data-edge-field="same"] {
  color: #f1c40f;
}
/* West (return to genesis) = red */
.graph-view.color-arrow[data-edge-field="west"] {
  color: #e74c3c;
}
/* Discovery (opportunistic in-flight) = purple dashed */
.graph-view.color-arrow[data-edge-field="discovery"] {
  color: #9b59b6;
  stroke-dasharray: 4,4;
}

/* Node quality coloring */
.graph-view.color-fill[data-quality="high"]    { color: #27ae60; }
.graph-view.color-fill[data-quality="medium"]  { color: #f39c12; }
.graph-view.color-fill[data-quality="low"]     { color: #c0392b; }
.graph-view.color-fill[data-quality="unknown"] { color: #8e44ad; }
CSS_EOF

    # snippets config — enable compass snippet
    cat > "$vault_dir/.obsidian/snippets.json" << 'SNIP_EOF'
{
  "compass-graph-colors": true
}
SNIP_EOF

    ok "Minimal plugin configs written to $vault_dir/.obsidian/"
}

# ── Vault Settings Configuration ──────────────────────────────────────────────
configure_vault_settings() {
    local vault_dir="$INSTALL_DIR/faerie-vault"

    # Write workspace.json — initial pane layout
    cat > "$vault_dir/.obsidian/workspace.json" << 'WS_EOF'
{
  "main": {
    "id": "main",
    "type": "split",
    "children": [
      {
        "id": "center",
        "type": "leaf",
        "state": {
          "type": "markdown",
          "state": {
            "file": "00-SHARED/ONBOARDING/00-START-HERE.md",
            "mode": "preview"
          }
        }
      }
    ],
    "direction": "vertical"
  },
  "left": {
    "id": "left",
    "type": "split",
    "children": [
      {
        "id": "file-explorer",
        "type": "leaf",
        "state": { "type": "file-explorer" }
      }
    ],
    "direction": "horizontal",
    "width": 280
  },
  "right": {
    "id": "right",
    "type": "split",
    "children": [
      {
        "id": "backlink",
        "type": "leaf",
        "state": { "type": "backlink" }
      }
    ],
    "direction": "horizontal",
    "width": 300
  },
  "active": "center"
}
WS_EOF

    ok "Vault workspace configured (opens to onboarding doc)"
}

# ── Environment Config ────────────────────────────────────────────────────────
write_env_config() {
    local env_file="$INSTALL_DIR/faerie-env.json"
    local env_sh="$INSTALL_DIR/faerie-env.sh"

    cat > "$env_file" << ENV_EOF
{
  "faerie2_root": "$INSTALL_DIR/faerie2",
  "faerie_vault": "$INSTALL_DIR/faerie-vault",
  "ct_vault": "$INSTALL_DIR/ct-vault",
  "claude_home": "$HOME/.claude",
  "install_dir": "$INSTALL_DIR",
  "os": "$OS",
  "installed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
ENV_EOF

    cat > "$env_sh" << ENV_SH_EOF
# faerie2 environment — source this in your shell profile
# Generated by one-click-install.sh on $(date -u +%Y-%m-%dT%H:%M:%SZ)
# Add to ~/.bashrc or ~/.zshrc:  source $env_sh

export FAERIE2_ROOT="$INSTALL_DIR/faerie2"
export FAERIE_VAULT="$INSTALL_DIR/faerie-vault"
export CT_VAULT="$INSTALL_DIR/ct-vault"
export CT_VAULT_PRIMARY="$INSTALL_DIR/ct-vault"
export FAERIE_VAULT_PORTABLE="$INSTALL_DIR/faerie-vault"
export FORENSIC_REPO_PATH="$INSTALL_DIR/faerie2"

echo "faerie2 environment loaded (FAERIE2_ROOT=\$FAERIE2_ROOT)"
ENV_SH_EOF

    chmod +x "$env_sh"
    ok "Environment config written: $env_file"
    ok "Shell env written: $env_sh"
}

# ── Canonical Symlinks ────────────────────────────────────────────────────────
create_symlinks() {
    # Resolve competing vault path variants to canonical location
    local canonical_ct="$INSTALL_DIR/ct-vault"

    local variants=(
        "$HOME/ct_vault"
        "$HOME/CT_VAULT"
        "$HOME/ct-vault"
    )

    for link in "${variants[@]}"; do
        if [[ ! -e "$link" ]] && [[ ! -L "$link" ]]; then
            ln -s "$canonical_ct" "$link" 2>/dev/null && \
                info "Symlink: $link -> $canonical_ct" || true
        fi
    done

    ok "Canonical symlinks resolved"
}

# ── Verify Connectivity ───────────────────────────────────────────────────────
verify_connectivity() {
    local faerie2_dir="$INSTALL_DIR/faerie2"

    # Check faerie2 vault sync script exists
    if [[ -f "$faerie2_dir/scripts/0x_vault_sync_test.py" ]]; then
        info "Running vault sync test..."
        python3 "$faerie2_dir/scripts/0x_vault_sync_test.py" \
            --vault "$INSTALL_DIR/faerie-vault" \
            --faerie2 "$faerie2_dir" 2>/dev/null && \
            ok "Vault sync test passed" || \
            warn "Vault sync test returned non-zero (may need manual check)"
    else
        info "Vault sync test script not found — skipping (manual check: open vault in Obsidian)"
    fi
}

# ── Wikilink Validation ───────────────────────────────────────────────────────
validate_wikilinks() {
    local vault_dir="$INSTALL_DIR/faerie-vault"
    local broken=0

    info "Checking wikilinks in faerie-vault..."

    # Simple check: find [[...]] references and verify the target files exist
    while IFS= read -r md_file; do
        while IFS= read -r link; do
            # Strip the [[...]] wrapper and any pipe aliases
            local target="${link//\[\[/}"
            target="${target//\]\]/}"
            target="${target%%|*}"   # strip alias
            target="${target%.md}"   # strip .md if present

            # Search for matching file in vault
            if ! find "$vault_dir" -name "${target}.md" -not -path "*/.obsidian/*" 2>/dev/null | grep -q .; then
                # Tolerate missing optional docs — warn only
                warn "Unresolved wikilink: [[$target]] in $(basename "$md_file")"
                ((broken++)) || true
            fi
        done < <(grep -oP '\[\[.*?\]\]' "$md_file" 2>/dev/null || true)
    done < <(find "$vault_dir" -name "*.md" -not -path "*/.obsidian/*" 2>/dev/null | head -50)

    if [[ $broken -eq 0 ]]; then
        ok "Wikilinks: all resolved"
    else
        warn "$broken unresolved wikilinks (may be placeholders — verify in Obsidian)"
    fi
}

# ── Templates ─────────────────────────────────────────────────────────────────
install_templates() {
    local vault_dir="$INSTALL_DIR/faerie-vault"
    mkdir -p "$vault_dir/Templates"

    # Daily note template with mission_choice frontmatter
    cat > "$vault_dir/Templates/daily-note-template.md" << 'DAILY_EOF'
---
type: hub
status: active
tags: [daily, faerie2]
created: {{DATE:YYYY-MM-DDThh:mm:ssZ}}
updated: {{DATE:YYYY-MM-DDThh:mm:ssZ}}
mission_choice: ""
doc_hash: ""
---

# {{DATE:YYYY-MM-DD}} Daily

## Mission Choice

> Fill in `mission_choice` frontmatter above — which mission are you steering today?

## Agent Outputs

> Check `00-SHARED/Agent-Outbox/` for new agent outputs.
> Check `00-SHARED/Human-Inbox/` for routed findings.

## Notes

DAILY_EOF

    # Mission note template
    cat > "$vault_dir/Templates/mission-note-template.md" << 'MISSION_EOF'
---
type: narrative
status: active
tags: [mission, faerie2]
mission: "{{VALUE:Mission name}}"
bearing: ""
created: {{DATE:YYYY-MM-DDThh:mm:ssZ}}
updated: {{DATE:YYYY-MM-DDThh:mm:ssZ}}
north: ""
south: ""
east: ""
west: ""
doc_hash: ""
---

# {{VALUE:Note name}}

## Context

## Findings

## Next Steps

MISSION_EOF

    ok "Templates installed (daily-note, mission-note)"
}

# ── Onboarding Docs ───────────────────────────────────────────────────────────
install_onboarding() {
    local vault_dir="$INSTALL_DIR/faerie-vault"
    mkdir -p "$vault_dir/00-SHARED/ONBOARDING"

    cat > "$vault_dir/00-SHARED/ONBOARDING/00-START-HERE.md" << 'ONBOARD_EOF'
---
type: hub
status: active
tags: [onboarding, faerie2, setup]
created: 2026-05-06T00:00:00Z
updated: 2026-05-06T00:00:00Z
doc_hash: ""
---

# Welcome to faerie2 + Vault

This vault is your window into the faerie2 orchestration system. Agents write here; you read and guide.

## What Is faerie2?

faerie2 is a multi-agent AI orchestration system powered by Claude. Agents work in parallel, each writing findings as manifest files in `forensics/`. A sync hook converts those manifests into vault notes automatically.

**You** are the queen: you spawn agents and read their outputs. The swarm does the work.

## Where to Find Agent Outputs

| Location | What Is Here |
|----------|-------------|
| `00-SHARED/Agent-Outbox/` | Raw agent writes — fresh findings |
| `00-SHARED/Human-Inbox/findings/` | Routed findings for your review |
| `00-SHARED/Human-Inbox/flags/` | Items flagged as needing attention |
| `00-SHARED/Droplets/` | Crystallized memory drops from agents |
| `10-Investigations/` | Active investigation notes |

> The "outbox" is named from the agent's perspective. It is your **inbox**.

## How to Capture Mission Choice

Each day, open your daily note and fill in the `mission_choice` frontmatter field.

Example:
```yaml
mission_choice: "vault-infrastructure-overhaul"
```

Agents check this field to cluster their work under the correct mission. No `mission_choice` = agents default to their last known mission.

## How to Make Edits

- Use `[[wikilinks]]` to link between notes — never `[markdown](links.md)`.
- Relative wikilinks only (Obsidian setting already configured).
- All vault notes must have frontmatter: `type`, `status`, `tags`, `created`, `updated`.
- Run the frontmatter validator before committing: agents do this automatically via hooks.

## How to Sync

Sync is automatic via PostToolUse hooks in faerie2. When agents write a final manifest, `0x_manifest_to_vault_sync.py` renders it as a vault note.

Manual sync:
```bash
cd ~/Obsidian/faerie2   # or your install dir
python3 scripts/0x_vault_sync_test.py --vault ../faerie-vault --faerie2 .
```

## Troubleshooting

### Broken wikilinks
- Obsidian shows broken links in orange.
- Common cause: file was moved or renamed.
- Fix: use Obsidian's built-in "Rename file" (updates all links automatically).
- Or run: `grep -r "\[\[" vault/ | grep -v ".obsidian"` to find raw broken refs.

### Sync stuck / not updating
- Check that hooks are active: `ls ~/.claude/hooks/`
- Restart Claude Code to reinitialize hooks.
- Manual trigger: `python3 scripts/0x_manifest_to_vault_sync.py`

### Plugin not loading
- Settings → Community Plugins → verify plugin is enabled (toggle ON).
- Check Obsidian version: minimum 1.12.0 required.
- Disable and re-enable the plugin to reload its config.
- Check Obsidian developer console (Ctrl+Shift+I) for error messages.

### Dataview queries show no results
- Ensure `enableInlineDataview: true` in Dataview plugin settings.
- Frontmatter fields must match query exactly (case-sensitive).
- Wait up to 5 seconds for Dataview index to rebuild after vault open.

### QuickAdd template not triggering
- Open QuickAdd settings and verify template path matches `Templates/` folder.
- Template filename must end in `.md`.
- Trigger via command palette: `QuickAdd: <template name>`.

---
*Generated by one-click-install.sh — vault-infrastructure-overhaul mission*
ONBOARD_EOF

    ok "Onboarding docs installed: 00-START-HERE.md"
}

# ── Final Output ──────────────────────────────────────────────────────────────
print_summary() {
    local elapsed=$(( $(date +%s) - INSTALL_START ))

    echo ""
    echo -e "${BOLD}${GREEN}Setup complete in ${elapsed}s${RESET}"
    echo "────────────────────────────────────────────────────────────────"
    echo ""
    echo -e "${BOLD}Installed:${RESET}"
    echo "  faerie2       $INSTALL_DIR/faerie2"
    echo "  faerie-vault  $INSTALL_DIR/faerie-vault"
    echo "  ct-vault      $INSTALL_DIR/ct-vault"
    echo ""
    echo -e "${BOLD}Next steps:${RESET}"
    echo "  1. Source env vars:"
    echo -e "       ${CYAN}source $INSTALL_DIR/faerie-env.sh${RESET}"
    echo "     (Add this line to ~/.bashrc or ~/.zshrc for persistence)"
    echo ""
    echo "  2. Open vault in Obsidian:"
    echo "       File → Open Vault → $INSTALL_DIR/faerie-vault"
    echo ""
    echo "  3. Enable community plugins in Obsidian:"
    echo "       Settings → Community Plugins → Disable Safe Mode → Enable All"
    echo ""
    echo "  4. Open today's daily note and set mission_choice frontmatter"
    echo ""
    echo "  5. Start faerie2 (in faerie2 dir, run Claude Code):"
    echo -e "       ${CYAN}cd $INSTALL_DIR/faerie2 && claude${RESET}"
    echo ""
    echo -e "  Onboarding guide: ${CYAN}$INSTALL_DIR/faerie-vault/00-SHARED/ONBOARDING/00-START-HERE.md${RESET}"
    echo ""
}

# ── Main ──────────────────────────────────────────────────────────────────────
main() {
    echo ""
    echo -e "${BOLD}faerie2 + Vault — One-Click Install${RESET}"
    echo "════════════════════════════════════════════════════════════════"
    echo ""

    detect_os
    check_deps
    check_obsidian
    resolve_install_dir "${1:-}"

    step "1 of 7 — Cloning repositories"
    clone_repos

    step "2 of 7 — Installing Obsidian plugin configs"
    install_plugin_configs

    step "3 of 7 — Configuring vault settings"
    configure_vault_settings

    step "4 of 7 — Installing templates"
    install_templates

    step "5 of 7 — Installing onboarding docs"
    install_onboarding

    step "6 of 7 — Writing environment config"
    write_env_config
    create_symlinks

    step "7 of 7 — Validation"
    verify_connectivity
    validate_wikilinks

    print_summary
}

main "$@"
