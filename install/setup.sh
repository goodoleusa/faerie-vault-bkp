#!/bin/bash
# faerie2 unified setup script (v1.7)
# Detects your environment and offers installation options
# v1.7 includes: vault crystallization pipeline, bundle consolidation,
# global script standardization, unified mission dashboard, piston observation layers

set -e

FAERIE_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"

echo "==================================================================="
echo "faerie2 v1.7 — Setup Assistant"
echo "==================================================================="
echo ""
echo "Core deliverables:"
echo "  • Vault crystallization pipeline (0x_vault_sync_crystallize.py)"
echo "  • Bundle consolidation with mission-graph teaching (0x_bundle.py)"
echo "  • Global script standardization (11 canonical, 63% reduction)"
echo "  • Unified mission dashboard (9x_mission_state_generator.py)"
echo "  • Piston observation infrastructure (pressure-aware spawn)"
echo ""

# Detect existing ~/.claude
if [ -d "$CLAUDE_HOME" ]; then
  echo "✓ Existing ~/.claude/ detected"
  echo ""
  echo "Choose installation path:"
  echo ""
  echo "  [1] Trial in this repo (project scope)"
  echo "      - Clone and cd into faerie2"
  echo "      - Your global ~/.claude/ stays unchanged"
  echo "      - Use when: testing faerie, have existing Claude config"
  echo ""
  echo "  [2] Merge into global ~/.claude/ (upgrade)"
  echo "      - Backs up existing ~/.claude/"
  echo "      - Adds faerie2 agents, hooks, scripts"
  echo "      - Merges faerie2 settings intelligently"
  echo "      - Use when: ready to adopt faerie globally"
  echo ""
  read -p "Enter [1] or [2]: " CHOICE

  case "$CHOICE" in
    1)
      bash "$FAERIE_REPO/install-trial.sh"
      ;;
    2)
      bash "$FAERIE_REPO/install-global.sh"
      ;;
    *)
      echo "Invalid choice. Exiting."
      exit 1
      ;;
  esac
else
  echo "No existing ~/.claude/ detected (fresh machine)"
  echo ""
  echo "Installing faerie2 as your global ~/.claude/"
  echo ""
  bash "$FAERIE_REPO/install-global.sh"
fi
