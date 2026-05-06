---
date: 2026-05-03
title: "Faerie2 Pseudo-System Design — Phase C Update"
author: knowledge-synthesizer
type: system-design
status: final
mission: mission-system-infrastructure-phase-c
tags: [architecture, dispatch, springboard, charter-sync, ffmx, release-gates]
vault_path: "00-SHARED/Hive/faerie2-pseudo-system-design-20260503.md"
supersedes: "emergence-quality-metrics-system-20260503.md"
---

# Faerie2 Pseudo-System Design — Phase C Update

**Date:** 2026-05-03 | **Status:** Final | **Confidence:** 0.87

This document extends the emergence quality metrics system design with Phase C additions: living FFMx formula, agent card injection cost validation, springboard recovery mechanics, charter-faerie sync, compass bearing DAG routing, and full 6-gate release readiness. It is the human-readable companion to `docs/ARCHITECTURE.md`.

---

## Part 1: System Philosophy

Faerie2 is modeled on biophysical fluid dynamics and stigmergic coordination. The queen's burden approaches zero. Agents coordinate via filesystem signals, not messages. Context is fuel; idle orchestrator is waste.

**Design equation:**
```
f(0) = queen_overhead ≈ 0
swarm_value = N_agents × Q_manifests × (1 + D_discovery) × P_piston
net = swarm_value - queen_overhead ≈ swarm_value
```

Every architectural component is justified by its contribution to f(0).

---

## Part 2: Mission-Driven Dispatch (Canonical)

### Semantic Mission as Routing Unit

Missions are the canonical routing signal. Tasks are discovered atoms. The `mission` field in every manifest is what routes work to workers — not `investigation_label` (deprecated).

**Agent discovery protocol:**
1. Agent completes primary task, writes manifest first (always).
2. Scans `forensics/{date}/manifests/` for prior work with matching `mission` field.
3. Identifies north-edge tasks (blockers just resolved), east-edge work (now runnable in parallel).
4. Appends discovered work to `discovered_work[]` with bearing + rationale.
5. Sets `next_mission_node.bearing` to guide next agent.

**No central dispatcher.** Work finds workers because workers read the landscape.

### Compass Bearing DAG

```
N (north) = unblock predecessor
  "This prerequisite must resolve before downstream work."
  Legal chains from N: N→{N,S,E,W}

S (south) = ship downstream  
  "After completing this, the next logical step is..."
  Legal chains from S: S→{S,E,W}  [S→N ILLEGAL]

E (east) = parallel sister work
  "This can run concurrently at same DAG level."
  Legal chains from E: E→{E,S,W,N}

W (west) = backtrack to baseline
  "An assumption failed; must reseat before continuing."
  Legal chains from W: W→{W,N,E}  [W→S ILLEGAL]
```

W-ratio >5% signals regression. W-ratio >10% triggers mission pause and baseline re-seating.

---

## Part 3: Living FFMx Formula

### Formula

```
FFMx = N_completed × Q × (1 + D) × P
```

| Factor | Definition |
|--------|-----------|
| N_completed | Agents returning valid manifest (has output_path + dashboard_line) |
| Q | Avg manifest quality 0–1 (0.25 per field: output_path, dashboard_line, files_written, next_mission_node) |
| D | Discovery rate = discovered_work_items / max(N_completed, 1) |
| P | Piston efficiency: 1.0 base, -0.3 if W1→W2 gap >60s, +0.2 if adaptive sizing used |

**Current:** 44.4× | **Floor:** ≥30 | **Ceiling target:** >40

### Self-Calibration Loop (5-Session Trajectory)

FFMx is not a static target. The system monitors rolling trajectory and adjusts:

| Condition | Response |
|-----------|----------|
| FFMx <30 for 2 sessions | Spawn bundle-consumption-audit (W-bearing) |
| FFMx >40 sustained | System scaling well; no action unless cost drift >20% |
| Trajectory slope <-0.03 over 5 sessions | Regression investigation required |
| P-factor anomaly (W1→W2 gap >60s) | Audit piston dispatch hooks |
| D-factor drop >20% | Check bundle path clobbering (INVARIANT#6) + INDEX.jsonl |

**Trajectory monitoring:** After each session, `9x_piston_metrics.py end` computes FFMx and appends to `forensics/main-metrics.jsonl`. The 5-session rolling slope is available via `9x_spawn_metrics_query.py --period 5 --ffmx-trend`.

---

## Part 4: Agent Card Injection (810 Tokens/Agent — Validated)

### What Agent Cards Contain

Each agent at spawn time receives an agent card as part of its bundle context. The card includes:

1. Archetype role and bearing constraints (legal/illegal chains)
2. Primary and secondary agents for this archetype
3. Mission field and frontier manifests (task-specific context)
4. HONEY.md reference (Agent 0: full 8.5K tokens; Agent 1+: 5-token reference excerpt)
5. COMB.md (role clarity, immutable per-session)

### Measured Cost

**Design estimate:** 60 tokens per agent (spawn boilerplate only).
**Measured reality:** ~810 tokens per agent when full bundle + card injection is included.

This is the validated figure from Phase C instrumentation. The 60-token figure in `faerie-config-v1.json` covers spawn boilerplate only. Total per-agent bundle cost is 810 tokens.

**Implication for 6-agent W1:** ~4,860 tokens total injection cost. At FFMx 44.4×, return value is approximately 215,000 tokens equivalent of work. ROI remains >40× even at measured cost.

### Bundle Architecture

```
AGENT BUNDLE = COMB.md (role clarity, immutable)
             + HONEY.md (Agent 0: full 8.5K; Agent 1+: 5-token excerpt)
             + mission context (charter scope + frontier manifests)
             + agent card (archetype constraints + bearing rules)
             + task directive (what to do)
```

Bundles are stored at `forensics/bundles/{date}/{mission}/` (mission-based paths, INVARIANT#6). Task-based paths cause clobbering across W1/W2/W3 waves.

---

## Part 5: Springboard Recovery Mechanics

### Problem

Without session recovery infrastructure, a daemon restart or context compact requires the queen to manually reconstruct context — violating f(0). Every minute of manual reconstruction is waste.

### Design

Two hooks, zero user overhead.

**PreCompact Hook** — fires before every context compact:

```
State file → forensics/{date}/state-snapshot
~/.claude/hooks/state/faerie-brief.json       → state-snapshot_faerie-brief_faerie_{session_id}.json
~/.claude/hooks/state/piston-checkpoint.json  → state-snapshot_piston-checkpoint_faerie_{session_id}.json
~/.claude/hooks/state/sprint-queue.json       → state-snapshot_sprint-queue_faerie_{session_id}.json
~/.claude/hooks/state/session_heartbeat.json  → state-snapshot_session-heartbeat_faerie_{session_id}.json
```

Each promotion appends a COC entry to `forensics/coc.jsonl`. Files are immutable after promotion.

**SessionStart Hook** — fires at every session start:

```
1. Load faerie-brief.json snapshot     → reconstruct mission + bearing + charter
2. Load piston-checkpoint.json         → restore wave tier + context %
3. Load sprint-queue.json              → restore task atoms (if interrupted)
4. Load session_heartbeat.json         → detect clean vs interrupted exit
5. If interruption: emit N-bearing manifest (unblock interrupted work) before spawning
```

### Recovery Validation

Target: under 30 seconds from SessionStart hook invocation to first agent spawned.

Validation method: `9x_piston_metrics.py precheck` logs hook-to-spawn latency. If >30s, audit: hook failing? State files missing? INDEX.jsonl stale?

### Why This Satisfies f(0)

Queen reads brief (1 turn) → spawns (1 action) → done. The Springboard infrastructure makes reconstruction ambient. Queen cost: ~1K tokens. Swarm cost: 810 tokens × 6 agents. f(0) preserved.

---

## Part 6: Charter-Faerie Sync

### Charter as Schedule + Constraint Layer

Active charters define:
- Semantic mission (routing signal)
- Pre-registered mutations (pre-approved task atoms)
- Falsifiable claims (what must be measured)
- Phase gates (ordered phases with allowed_bearings per phase)

Charters are the schedule. Presend validation checks every spawn decision against active charter scope.

### Pre-Registration Auto-Population

When a charter activates:
1. `4x_charter_loader.py` reads `charter.preRegisteredChanges[]`
2. Writes task atoms to sprint queue + bundle context for the charter's mission
3. Agents spawned on the mission arrive pre-loaded with charter context

This eliminates the "blank start" problem on charter-driven missions. Agents discover pre-registered tasks at high confidence (they know the work was intentional).

### Phase Gate + Bearing Enforcement

Charter phases define bearing constraints:

```json
{
  "phases": [
    {
      "name": "Phase 1 — Foundation",
      "allowed_bearings": ["N", "E"],
      "blocked_bearings": ["S", "W"],
      "exit_criteria": "All N-edge blockers resolved"
    }
  ]
}
```

`presend_estimate.py` validates spawn bearing against `phases[current].allowed_bearings`. Violations surface as charter/phase/bearing mismatch flags. User must explicitly override. Silent violations are not allowed.

### Crystallization Pathway

```
Charter complete
  → charter_archiver.py archives + updates template success_rate
  → Extract pattern candidates (appear in 2+ charters?)
  → YES: append to NECTAR.md as method candidate (confidence 0.70)
  → After 2nd charter confirmation: promote to HONEY.md (confidence 0.70→0.80)
  → 3rd confirmation + zero failures: confidence 0.80→0.88
```

Charter-derived methods start at 0.70, not 1.0 (per crystallization rules in `~/.claude/rules/charter-crystallization.md`).

---

## Part 7: Release Readiness Gates (All 6)

### Gate Overview

```
RELEASE_READY = gate1 AND gate2 AND gate3 AND gate4 AND gate5 AND gate6
```

All gates must PASS. 5/6 = CAUTION. <5/6 = BLOCKED.

### Gate 1: Quality Gates (3/3)

Local session health. Three sub-gates all must PASS.

| Sub-gate | Formula | Threshold |
|----------|---------|-----------|
| Citation density | manifests_with_cross_citations / total_manifests | ≥0.30 |
| Brittleness | (W_ratio×0.60) + (test_gap×0.25) + (evidence_delta×0.15) | <0.40 |
| Downstream impact | N_edges_resolved / total_N_edges | ≥0.60 |

**Meaning:** Agents are learning from each other (citation), assumptions are solid (brittleness), and shipping actually unblocks downstream work (impact).

### Gate 2: Emergence Trajectory

No regression. `delta ≥ -0.03` for 3 consecutive sessions.

**Why flat is OK:** Equilibrium (not growth) is a healthy state for a mature system. Only sustained decline triggers investigation.

### Gate 3: Per-Archetype Balance

No single-archetype bottleneck. Pearson correlation of 4 archetype scores ≥ 0.75.

**What it detects:** If MAKER is 0.92 but NAVIGATOR is 0.45, the system is shipping without adequate discovery — a fragility signal.

### Gate 4: Membench Health

Memory system correctness. Four metrics, all must pass:

- **M1 ≥0.85:** HONEY facts recalled correctly (retention)
- **M3 >1.10:** Memory ROI is positive (efficiency)
- **M8 ≤5%:** Veto gate — confabulation rate (hallucinated recalls)
- **M11 ≥70%:** Veto gate — agent bootstrap success rate

M8 and M11 are hard veto gates. Any failure blocks release regardless of all other scores.

### Gate 5: Cost Formula Validated

Spawn cost estimate drift <20% from actual, averaged across 3 sessions.

**Current status: FAIL.** mth00420 (spawn cost formula) is LOW confidence (RED FLAG). Average drift 182%. This gate will not pass until forensic actuals stabilize and `faerie-config-v1.json` is recalibrated.

**Path to PASS:** Run 3 sessions, collect actuals via `9x_spawn_cost_tracker.py`, compute mean drift. If <20%: update config estimate. Gate 5 passes.

### Gate 6: Archetype Stability

Per-archetype balance correlation ≥0.75 across 3 consecutive sessions. Confirms emergence is reproducible.

**Current status: PENDING.** Requires 3-session history post-wiring.

### Current Release Readiness

| Gate | Status |
|------|--------|
| 1 Quality Gates | PENDING (first session post-wiring) |
| 2 Emergence Trajectory | PENDING (3 sessions needed) |
| 3 Per-Archetype Balance | CAUTION (1 session; Phase C = 0.78) |
| 4 Membench Health | PASS (Phase C: M1=0.88, M3=1.31, M8=0.01, M11=1.0) |
| 5 Cost Formula | FAIL (182% drift; recalibration required) |
| 6 Archetype Stability | PENDING (3 sessions needed) |

**v2.0 release: BLOCKED.** Primary blocker: Gate 5 (cost formula). Secondary: Gates 2, 6 need 3-session history.

---

## Part 8: Architecture Audit Index

See `docs/architecture-audit-20260503.md` for full component status. Summary:

**Implemented:** Mission-driven dispatch, compass bearing DAG, stigmergic manifest routing, piston waves (W1/W2/W3), bundle architecture (COMB + HONEY), anchor agent coordination pattern, per-archetype emergence scoring design, quality gate formulas, membench M1-M11 harness, COC hash chain, write-protection architecture.

**Pending:** Springboard PreCompact + SessionStart hooks wired, charter pre-registration auto-population, spawn cost formula recalibration (Gate 5), `0x_dev_eval.py` aggregator wired end-to-end, 3-session history for Gates 2 + 6.

**Experimental:** M12-M15 membench metrics (validated Phase C; needs 2 more sessions to promote from MEDIUM to HIGH confidence), living FFMx trajectory auto-recalibration.

---

## References

- Full narrative architecture: `docs/ARCHITECTURE.md`
- Mission navigation model: `docs/MISSION-NAVIGATION-MODEL.md`
- Spawn cost accountability: `docs/SPAWN-COST-ACCOUNTABILITY.md`
- Membench bridge: `docs/membench-emergence-bridge.md`
- Dev-eval signal flow: `docs/dev-eval-signal-flow.md`
- Emergence metrics system: `00-SHARED/Hive/emergence-quality-metrics-system-20260503.md`
- Config source of truth: `config/faerie-config-v1.json`
- HONEY.md methods: mth00400–mth00432

---

**Document version:** 1.0 (Phase C) | **Date:** 2026-05-03 | **Next review:** After 3-session post-wiring run
