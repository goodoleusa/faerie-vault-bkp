#!/bin/bash
# 0x_bundle_emission_pressure.sh
# TIER: 0x (governance hook)
# REPLACES: manual bundle emission decisions
# METRIC: bundles_emitted_per_session (target: >1 per W1 LIFTOFF cohort)
#
# Presend hook: Check if remaining context > 30%.
# If yes, inject bundle-emission instructions into agent prompt.
# Creates formalized pressure for agents to emit bundles (equilibrium principle).

set -eu

ALTIMETER_FILE="$HOME/.claude/altimeter.json"
FORMULAS_FILE="/mnt/d/0local/.claude/faerie2-formulas.json"

# Read current context %
if [[ ! -f "$ALTIMETER_FILE" ]]; then
    exit 0  # No altimeter yet; no pressure injection
fi

CONTEXT_PCT=$(jq -r '.context_pct // 50' "$ALTIMETER_FILE" 2>/dev/null || echo "50")
AGENT_TYPE="${AGENT_TYPE:-general-purpose}"

# Read formula: BUNDLE_EMISSION_CONTEXT_THRESHOLD (default 30%)
THRESHOLD=$(jq -r '.BUNDLE_EMISSION_CONTEXT_THRESHOLD // 30' "$FORMULAS_FILE" 2>/dev/null || echo "30")

# If remaining context > threshold, inject bundle emission pressure
REMAINING_PCT=$((100 - ${CONTEXT_PCT%.*}))

if (( $(echo "$REMAINING_PCT > $THRESHOLD" | bc -l) )); then
    cat > /tmp/bundle-emission-pressure.txt << 'EOF'

---

## Bundle Emission Opportunity

Your remaining context after primary task: **~$REMAINING_PCT%**

**Formula:** If >30% context remains + work completed, emit bundles for next agents.

**Why:** Agents with spare context can render future-agent context bundles. Cost to you: ~10% of remaining tokens. Benefit to next agents: 40% faster ramp-up. This is how the system scales without main context burden (f(0) equilibrium).

**When to emit:**
1. ✅ Primary task complete + manifest written
2. ✅ Prescan passes (work is stale/absent)
3. ✅ Remaining context >20% after task
4. ✅ Use: 0x_spawn_template.py --bundle (ready to call, zero main burden)

**When NOT to emit:**
- Primary task still in progress
- Manifest not yet written
- Prescan blocks (work too recent)
- Remaining context <10%

**Recommendation:** If you discover unblocking work matching your agent type + investigation_label, emit a bundle for future scouts. This advances the mission without waiting for main to route it.

EOF
    echo "[PRESSURE] Bundle emission opportunity detected (context_remaining=$REMAINING_PCT%, threshold=$THRESHOLD%)"
fi

exit 0
