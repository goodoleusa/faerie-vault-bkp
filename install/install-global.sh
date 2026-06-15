#!/bin/bash
# faerie2 global installation script
# Use this if you're starting fresh and want faerie2 as your global ~/.claude/

set -e

FAERIE_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
FAERIE_VAULT_DEFAULT="$(dirname "$FAERIE_REPO")/faerie-vault"

echo "==================================================================="
echo "faerie2 — Global Installation"
echo "==================================================================="
echo ""
echo "This will install faerie2 as your global ~/.claude/"
echo "  FAERIE_REPO:  $FAERIE_REPO"
echo "  CLAUDE_HOME:  $CLAUDE_HOME"
echo ""
echo "==================================================================="
echo "CONSENT DIALOG"
echo "==================================================================="
echo ""
echo "This installation will:"
echo "  1. Backup your existing ~/.claude/ (if present)"
echo "  2. Install faerie2 scripts, config, and agents globally"
echo "  3. Modify ~/.bashrc and ~/.zprofile to set FAERIE_* variables"
echo ""
echo "You can uninstall at any time by running:"
echo "  $FAERIE_REPO/uninstall.sh"
echo ""
echo "To proceed, type 'YES' (case-sensitive):"
read -r CONSENT_INPUT

if [ "$CONSENT_INPUT" != "YES" ]; then
  echo "Installation cancelled."
  exit 0
fi

# Step 1: Check for existing ~/.claude and plan merge
EXISTING_SETTINGS="$CLAUDE_HOME/settings.json"
EXISTING_SETTINGS_BACKUP=
if [ -d "$CLAUDE_HOME" ]; then
  BACKUP_DIR="$CLAUDE_HOME.backup-$(date +%Y%m%d-%H%M%S)"
  echo "⚠ Existing $CLAUDE_HOME found."
  echo "   Preserving existing settings and rules via merge..."
  echo "   Full backup saved to: $BACKUP_DIR"
  cp -r "$CLAUDE_HOME" "$BACKUP_DIR"
  EXISTING_SETTINGS_BACKUP="$BACKUP_DIR/settings.json"
  echo "   ✓ Backup complete"
fi

# Step 2: Install faerie2/.claude to ~/.claude
echo ""
echo "Installing faerie2 as global ~/.claude/"
mkdir -p "$CLAUDE_HOME"
cp -r "$FAERIE_REPO/.claude/"* "$CLAUDE_HOME/" || {
  echo "✗ Copy failed. Restore from backup and try again."
  exit 1
}
echo "✓ Files copied"

# Step 3: Merge settings.json (preserve user's rules)
if [ -f "$EXISTING_SETTINGS_BACKUP" ]; then
  echo ""
  echo "Merging settings.json (preserving existing allow/deny rules)..."
  python3 "$FAERIE_REPO/.claude/scripts/3x_settings_merge.py" \
    "$EXISTING_SETTINGS_BACKUP" \
    "$FAERIE_REPO/.claude/settings.json" \
    "$EXISTING_SETTINGS" || {
    echo "✗ Settings merge failed. Restore from backup:"
    echo "   cp -r $BACKUP_DIR/* $CLAUDE_HOME/"
    exit 1
  }
else
  echo "✓ No prior settings to merge (fresh install)"
fi

# Step 4: Configure faerie-vault path
echo ""
echo "Configuring vault path..."
if [ -d "$FAERIE_VAULT_DEFAULT" ]; then
  FAERIE_VAULT="$FAERIE_VAULT_DEFAULT"
  echo "  Found faerie-vault at: $FAERIE_VAULT"
else
  echo "  Enter path to faerie-vault (or press Enter to skip):"
  read -r FAERIE_VAULT_INPUT
  FAERIE_VAULT="${FAERIE_VAULT_INPUT:-$FAERIE_VAULT_DEFAULT}"
fi

# Step 5: Set environment variables
echo ""
echo "Setting environment variables..."
if [ -f "$HOME/.bashrc" ]; then
  if ! grep -q "FAERIE_REPO=" "$HOME/.bashrc"; then
    cat >> "$HOME/.bashrc" <<'EOF'

# faerie2 orchestration platform
export FAERIE_REPO="${FAERIE_REPO_PATH}"
export FAERIE_VAULT="${FAERIE_VAULT_PATH}"
EOF
    sed -i "s|\${FAERIE_REPO_PATH}|$FAERIE_REPO|g" "$HOME/.bashrc"
    sed -i "s|\${FAERIE_VAULT_PATH}|$FAERIE_VAULT|g" "$HOME/.bashrc"
    echo "✓ Added to ~/.bashrc"
  fi
fi

if [ -f "$HOME/.zprofile" ]; then
  if ! grep -q "FAERIE_REPO=" "$HOME/.zprofile"; then
    cat >> "$HOME/.zprofile" <<'EOF'

# faerie2 orchestration platform
export FAERIE_REPO="${FAERIE_REPO_PATH}"
export FAERIE_VAULT="${FAERIE_VAULT_PATH}"
EOF
    sed -i "s|\${FAERIE_REPO_PATH}|$FAERIE_REPO|g" "$HOME/.zprofile"
    sed -i "s|\${FAERIE_VAULT_PATH}|$FAERIE_VAULT|g" "$HOME/.zprofile"
    echo "✓ Added to ~/.zprofile"
  fi
fi

# Step 6: Validation
echo ""
echo "Validating installation..."
if [ -f "$CLAUDE_HOME/settings.json" ]; then
  echo "✓ settings.json found"
else
  echo "✗ settings.json not found. Installation may have failed."
  exit 1
fi

if [ -d "$CLAUDE_HOME/scripts" ]; then
  SCRIPT_COUNT=$(find "$CLAUDE_HOME/scripts" -name "*.py" | wc -l)
  echo "✓ Found $SCRIPT_COUNT scripts"
else
  echo "⚠ scripts/ directory not found"
fi

# Step 7: First run
echo ""
echo "==================================================================="
echo "✓ Installation complete!"
echo "==================================================================="
echo ""
echo "Next steps:"
echo "  1. Reload shell: source ~/.bashrc  (or restart terminal)"
echo "  2. Verify: python3 ~/.claude/scripts/0x_reputation_summary.py --json | head -3"
echo "  3. First run: cd /path/to/any/repo && claude && /faerie"
echo ""
echo "Documentation:"
echo "  - README.md: Overview and quick start"
echo "  - CLAUDE.md: Architecture and governance"
echo "  - docs/: Detailed guides"
echo ""
echo "To trial faerie2 in a specific project instead:"
echo "  cd faerie2 && claude  (uses project-scoped overlay)"
echo ""
