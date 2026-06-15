#!/bin/bash
# faerie2 uninstall script
# Removes faerie2 global installation and restores backup if available

set -e

CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"

echo "==================================================================="
echo "faerie2 — Global Uninstallation"
echo "==================================================================="
echo ""

# Check if ~/.claude is present
if [ ! -d "$CLAUDE_HOME" ]; then
  echo "✓ $CLAUDE_HOME not found. Nothing to uninstall."
  exit 0
fi

echo "This will uninstall faerie2 from your system:"
echo "  CLAUDE_HOME: $CLAUDE_HOME"
echo ""
echo "The most recent backup (if available) will be restored."
echo ""
echo "To proceed, type 'YES' (case-sensitive):"
read -r CONSENT_INPUT

if [ "$CONSENT_INPUT" != "YES" ]; then
  echo "Uninstallation cancelled."
  exit 0
fi

# Step 1: Remove ~/.claude
echo ""
echo "Removing $CLAUDE_HOME..."
rm -rf "$CLAUDE_HOME"
echo "✓ Removed"

# Step 2: Find and restore most recent backup
echo ""
echo "Looking for backups..."
BACKUP_DIR=$(find "$HOME" -maxdepth 1 -name ".claude.backup-*" -type d 2>/dev/null | sort -V | tail -1)

if [ -n "$BACKUP_DIR" ]; then
  echo "Found backup: $BACKUP_DIR"
  echo "Restoring from backup..."
  # Use cp -a to preserve all attributes and properly handle directory contents
  cp -a "$BACKUP_DIR/." "$CLAUDE_HOME/" || {
    echo "✗ Restore failed. Creating empty $CLAUDE_HOME."
    mkdir -p "$CLAUDE_HOME"
  }
  echo "✓ Backup restored"
else
  echo "⚠ No backup found. Creating empty $CLAUDE_HOME."
  mkdir -p "$CLAUDE_HOME"
fi

# Step 3: Clean shell rc files
echo ""
echo "Cleaning shell rc files..."

# Clean ~/.bashrc
if [ -f "$HOME/.bashrc" ]; then
  if grep -q "# faerie2 orchestration platform" "$HOME/.bashrc"; then
    # Remove the faerie2 section (comment + export lines)
    sed -i '/# faerie2 orchestration platform/,+2d' "$HOME/.bashrc"
    echo "✓ Cleaned ~/.bashrc"
  fi
fi

# Clean ~/.zprofile
if [ -f "$HOME/.zprofile" ]; then
  if grep -q "# faerie2 orchestration platform" "$HOME/.zprofile"; then
    # Remove the faerie2 section (comment + export lines)
    sed -i '/# faerie2 orchestration platform/,+2d' "$HOME/.zprofile"
    echo "✓ Cleaned ~/.zprofile"
  fi
fi

# Step 4: Validation
echo ""
echo "Validating uninstallation..."

if [ ! -d "$CLAUDE_HOME" ] || [ -z "$(ls -A "$CLAUDE_HOME" 2>/dev/null)" ]; then
  echo "✓ $CLAUDE_HOME successfully removed/emptied"
else
  echo "✓ $CLAUDE_HOME restored from backup"
fi

# Final message
echo ""
echo "==================================================================="
echo "✓ Uninstallation complete!"
echo "==================================================================="
echo ""
echo "Next steps:"
echo "  1. Reload shell: source ~/.bashrc  (or restart terminal)"
echo "  2. Verify uninstallation: echo \$FAERIE_REPO (should be empty)"
echo ""
echo "To reinstall faerie2:"
echo "  cd /path/to/faerie2 && bash install-global.sh"
echo ""
