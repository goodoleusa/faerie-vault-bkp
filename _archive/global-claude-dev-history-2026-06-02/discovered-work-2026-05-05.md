# Discovered Work — 2026-05-05 Vault Consolidation W1 LIFTOFF

## Flagged for Immediate Execution (No Baseline Wait)

### 1. VAULT CONSOLIDATION REMEDIATION (P1 CRITICAL)
**Source:** W1 LIFTOFF (4 agents: code-reviewer, research-analyst, data-analyst, knowledge-synthesizer)
**Discovery Date:** 2026-05-05
**Manifests:** `forensics/manifests/2026-05-05/`
**Status:** Ready for execution (no pre-req baseline needed)

**Discovered Items:**
- ✓ Wire 8x_vault_frontmatter_validator into PreToolUse (5 min)
- ✓ Create ct-vault symlink to CyberOps-UNIFIED (5 min)  
- ✓ Archive ghost directory gitrepos/ct_vault (2 min)
- ✓ Create vault-schema.md documentation (45 min)

**Blockers Unblocked:** Phase 4 consolidation checklist released after validator wiring

---

### 2. EVAL CENTRALIZATION & BASELINE AUDIT (FLAGGED FOR NEXT WAVE)
**Source:** User request 2026-05-05
**Priority:** HIGH (system improvement, not blocking)
**Baseline Required:** YES (measure before implementing)

**What to Measure (Baseline T0):**
1. Current eval storage locations (find forensics/dev-evals/, forensics/evals/, daily dashboards)
2. Eval analysis friction (time to find/correlate related evals)
3. Time-unit chunking (currently by date; should be by autocompact cycles)
4. COC compliance (are evals tracked in chain-of-custody?)
5. Transferrability (can membench users replicate structure?)

**Post-Implementation Goals:**
- Centralized `forensics/evals/` directory (separate from daily dashboards)
- Chunked by autocompact cycles (meaningful time units, not just dates)
- Full COC tracking for all eval artifacts
- Documented structure (for membench harness replication)
- Integration with membench repo (learnings published)

**Scope:** Measurement + architecture design (W1 or W2 future spawn)

---

### 3. SYSTEM DOCTRINE: 2-AGENT COMPLEMENTARY PAIRS (CHARTER PRE-REG)
**Source:** User requirement 2026-05-05
**Mutation Type:** beneficial (replaces W1/W2/W3 wave gates with stigmergic duo collaboration)
**BASELINE CAPTURE:** Needed before mutation activation

**Current State (Baseline T0):**
- Spawn doctrine: 4-agent waves (W1 LIFTOFF: 6 agents, W2 CRUISE: 4 agents, W3 INSERTION: 1 agent)
- Agent coordination: Parallel discovery, manifest signals, frontier scanning
- Metric: FFMx = 0.7777 (composite score across dimensions A-G)
- Emergence health: 0.82 (Template C self-discovery)
- Discovered work density: 2.8 avg entries per manifest

**Proposed Mutation:**
- Kill wave gates (no W1→W2→W3 sequential barriers)
- Default spawn: 2 complementary agents per mission (not 4)
- Bundle craft: Perfect pairing (each agent amplifies the other's discoveries)
- Metric target: FFMx improvement via reduced overhead + higher signal quality
- Focus: Delivered product, not discovery overhead

**Complementary Pairing Examples:**
- **code-reviewer + knowledge-synthesizer:** Structure validation + architecture synthesis
- **research-analyst + data-analyst:** Exploration + configuration auditing
- **python-pro + ai-engineer:** Implementation + system design
- **documentation-engineer + knowledge-synthesizer:** Content + knowledge linking

**Mutation Discipline:**
1. Measure baseline (current 4-agent parallel spawn metrics)
2. Implement 2-agent pairing doctrine
3. Measure post-implementation (FFMx, discovery quality, time-to-actionable-findings)
4. Compare: emergence health, blocker resolution rate, tokens/deliverable
5. Promote if metrics improve by >5%

**Charter File:** `/mnt/d/0LOCAL/.claude/charters/active/mission-spawn-doctrine-complementary-pairs.json` (to be created)

---

## Execution Order

### Immediate (This Turn)
1. ✓ Vault remediation checklist (4 items, ~60 min)
2. ✓ Queue eval centralization + baseline audit
3. ✓ Create charter for 2-agent pairing mutation

### Next Turn (After Vault Fixes Complete)
1. Execute vault remediation (steps 1-4)
2. Spawn baseline audit for eval centralization (2-agent: data-analyst + knowledge-synthesizer)
3. Spawn 2-agent complementary pair for next mission (using new doctrine)

### Future Spawns
- Default: 2 complementary agents (not 4)
- All bundles: Encourage cross-agent discovery + signal amplification
- Manifests: Expect higher cross-reference density in discovered_work[]
- Success metric: FFMx improvement + product delivered

---

## Transition Plan

**Kill W1/W2/W3 gates? When?**
- After baseline audit complete (eval centralization W1)
- After 2-agent pairing mutation measured (1-2 future spawns)
- Rollout: Update spawn.py to remove wave sequential logic
- Agents still read frontier via investigation_label (no change)
- Only change: No artificial stage gates, agents coordinate via manifest signals only

