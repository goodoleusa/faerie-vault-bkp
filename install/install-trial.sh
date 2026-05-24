#!/bin/bash
# faerie2 trial installation script
# Use this to trial faerie2 in your project without affecting global ~/.claude/

set -e

FAERIE_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAERIE_VAULT_DEFAULT="$(dirname "$FAERIE_REPO")/faerie-vault"

echo "==================================================================="
echo "faerie2 — Trial Installation (Project Scope)"
echo "==================================================================="
echo ""
echo "This will trial faerie2 WITHIN this repo only."
echo "Your global ~/.claude/ will NOT be modified."
echo ""
echo "  FAERIE_REPO:  $FAERIE_REPO"
echo ""

# Step 1: Check for faerie-vault
echo "Checking for faerie-vault..."
if [ -d "$FAERIE_VAULT_DEFAULT" ]; then
  FAERIE_VAULT="$FAERIE_VAULT_DEFAULT"
  echo "✓ Found faerie-vault at: $FAERIE_VAULT"
else
  echo "⚠ faerie-vault not found. Enter path to faerie-vault (or press Enter to skip):"
  read -r FAERIE_VAULT_INPUT
  FAERIE_VAULT="${FAERIE_VAULT_INPUT:-}"
  if [ -z "$FAERIE_VAULT" ]; then
    echo "⚠ Vault not configured. Dataview queries will not update live metrics."
  else
    echo "✓ Vault path set: $FAERIE_VAULT"
  fi
fi

# Step 2: Configure .claude/settings.json to use overlay
echo ""
echo "Configuring project-scoped settings..."
if [ ! -f "$FAERIE_REPO/.claude/settings.json" ]; then
  echo "ℹ Using settings-overlay.json as settings.json"
  cp "$FAERIE_REPO/.claude/settings-overlay.json" "$FAERIE_REPO/.claude/settings.json"
  echo "✓ settings.json configured"
fi

# Step 3: Set environment variables (local shell only)
echo ""
echo "Environment variables (add to ~/.bashrc to persist):"
echo ""
echo "  export FAERIE_REPO='$FAERIE_REPO'"
if [ -n "$FAERIE_VAULT" ]; then
  echo "  export FAERIE_VAULT='$FAERIE_VAULT'"
fi
echo ""
echo "For this session only, run:"
echo "  source <(echo 'export FAERIE_REPO=\"$FAERIE_REPO\"')"
if [ -n "$FAERIE_VAULT" ]; then
  echo "  source <(echo 'export FAERIE_VAULT=\"$FAERIE_VAULT\"')"
fi
echo ""

# Step 4: Validation
echo "Validating trial setup..."
if [ -f "$FAERIE_REPO/.claude/settings.json" ]; then
  echo "✓ settings.json found"
else
  echo "✗ settings.json not found"
  exit 1
fi

# Step 5: First run
echo ""
echo "==================================================================="
echo "✓ Trial setup complete!"
echo "==================================================================="
echo ""
echo "Next steps:"
echo "  1. Export variables: source <(echo 'export FAERIE_REPO=\"$FAERIE_REPO\"')"
echo "  2. Run: cd $FAERIE_REPO && claude"
echo "  3. Try: /faerie (should load dashboard)"
echo ""
echo "Your global ~/.claude/ is unchanged. Trial is isolated to this repo."
echo ""
echo "To make this the global installation:"
echo "  bash install-global.sh"
echo ""
