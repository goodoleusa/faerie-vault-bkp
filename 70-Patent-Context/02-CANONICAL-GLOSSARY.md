---
type: canonical-glossary
status: active
created: 2026-05-05
updated: 2026-05-05T22:45:00Z
validation_hash: sha256:pending
tags: [glossary, canonical, emoji-language, architecture, emergence, mutation]
---

# Faerie2 Canonical Glossary

**Single source of truth for all faerie2 terminology, emojis, archetypes, and concepts.**

Every term carries a consistent emoji identifier. Every definition is validated against code.

---

## Core System Components (Emoji Icons)

### 🧚 Faerie
The main session orchestrator. Reads state from forensics/, reads bearing frontier, makes formation decisions, spawns teams via context-pressure sigmoid. Never polls agents; awaits TaskNotification events. Responds with dashboard_line (≤80 chars) + next bearing.

**f(0) principle:** Faerie's orchestration burden ≈ 0. All meaningful work done by spawned agents.

---

### ⚙️ f(0) — Orchestration Burden ≈ 0
North star metric of faerie2. Main context never consumed by orchestration overhead—only by reading summaries (manifest `dashboard_line` ≤80 chars) and making high-level bearing decisions.

**Measurement:** If main context exceeds 25K tokens on orchestration vs 100+ tokens per spawned agent, f(0) is violated.

---

### 🧭 Compass Bearings (N/S/E/W)
Four cardinal directions for routing work in mission graph:

- **N (North)** — Unblock upstream prerequisites. Reverse-dependency work that frees blocked tasks.
- **S (South)** — Conclude and move downstream. Forward-dependency work that ships next deliverable.
- **E (East)** — Parallel sister work at same DAG level within mission.
- **W (West)** — Backtrack to baseline. Return to HQ, re-seat assumptions, audit prior work.

Every manifest carries `next_mission_node` with bearing to guide next agent's routing.

---

### 🏆 Mission
Primary semantic routing unit in manifests. Clusters all related work into coherent chains. **Dual nature: (1) dispatched top-down via `/spawn`, (2) self-emerging from agent discovery.** Not same as `task_id` (mission groups multiple tasks).

**Canonical field:** `manifest.mission`

**Two mission sources:**
1. **Dispatched** — Main/faerie creates mission via `/spawn` (semantic intent dispatch)
2. **Emergent** — Agents discover unblocked work during frontier scans, detect mission coherence, self-organize to join

**Self-organization rules (agents autonomously decide to join):**
- **Context available:** Remaining context > mission estimated cost + buffer (don't blow context)
- **Skill match:** Agent archetype aligned with mission bearing (NAVIGATOR for N-edges, MAKER for S-edges, BRIDGE for E, DEEP-DIVER for W)
- **Confidence gates pass:** Agent quality ≥ SEED_MIN (0.78), belief ≥ DEEPEN_MIN (0.50); only join if can assess own fitness
- **Discovery via frontier:** Agent reads mission field in discovered_work[], sees mission is interesting/unblocked, volunteers to join

**Mission graph infrastructure (scripts):**
- `0x_mission_graph.py` — Core mission graph navigation (N/S/E/W compass edges)
- `0x_mission_clusterer.py` — Groups tasks by mission semantic unit
- `0x_cross_mission_edge_scanner.py` — Detects N/S/E/W bearing edges between missions
- `0x_mission_trail_builder.py` — Builds stigmergic pheromone trails (manifest signals)
- `9x_mission_intelligence_dashboard.py` — Visualizes mission state, bearing decisions, bottlenecks
- `8x_manifest_mission_validator.py` — Validates mission field presence in all manifests

**Navigation rule:** Agents navigate mission graph via compass bearings (N/S/E/W), not task IDs. Dead reckoning: each manifest carries bearing to next mission node; agents follow compass, join missions opportunistically, self-organize without central plan.

---

## Archetype Markers (Team Formation)

### 🧭 NAVIGATOR
Reads compass edges, discovers work via frontier scans, maps dependency chains (N-edges). Unblocks prerequisites.

**Bearing:** N (North — unblock)  
**Team role:** Chart paths, read blocking chains, propose unblock solutions

---

### 🔨 MAKER
Ships fast, closes work, delivers next phase. Drives S-edges forward.

**Bearing:** S (South — conclude)  
**Team role:** Build, test, ship, unlock downstream

---

### 🌉 BRIDGE
Finds cross-domain transfers, syncs parallel work, ensures sister tasks coordinate (E-edges).

**Bearing:** E (East — parallel)  
**Team role:** Connect independent workstreams, ensure coherence

---

### 🔬 DEEP-DIVER
Validates baselines, re-seats assumptions, audits prior work (W-edges). Rigorous.

**Bearing:** W (West — backtrack)  
**Team role:** Verify assumptions, find contradictions, propose reframes

---

## Emergence & Stigmergy (Biological Model)

### 🪄 Stigmergy
Coordination via filesystem signals (manifests, compass edges, mission fields) rather than synchronous messaging. Agents leave pheromone trails (manifest `next_mission_node` bearings); downstream agents read trails and self-organize.

**Core rule:** No SendMessage. Never. Always stigmergic routing via `manifest.mission` field and compass edges.

**Operational principle:** Agents coordinate by reading and updating shared state on the filesystem (manifests, mission graph edges, forensic artifacts) without direct communication. This decouples agents from each other—emergent behavior doesn't cascade unpredictably.

---

### 🌊 Emergence
Complex system behavior arising from simple local interactions. Agents follow simple rules (read mission field, discover work, follow compass); complex mission DAGs self-organize without central planning.

**Three constraints make emergence safe:**
1. **Forensic capture** — every artifact is hash-chained in `{repo}/forensics/` with full provenance; mistakes are recoverable
2. **Bundle priors** — curated context shapes reasoning before execution; good bundles produce correct behavior without restriction
3. **Stigmergic coordination** — filesystem signals enable decoupled agent action without hidden cascades

**Example:** Four agents spawned on "optimize database." None received master plan. Through manifest discovery + compass navigation, they organized into: baseline measurement → query analysis → index design → documentation.

---

### Observed Emergence Patterns

#### Pattern 1: Self-Invalidation
Agent detects its task premise is stale and refuses to execute. The refusal itself solves the problem.
- Agent reads `blockedBy` condition, verifies upstream contract still valid
- If not: agent writes diagnostic explaining why, recommends correction, exits cleanly
- **Impact:** ~30% of stale tasks self-heal via agent refusal, no main intervention

#### Pattern 2: Diagnostic Emergence
Agent traces bug across task boundaries to substrate root cause and fixes it, not just the symptom.
- Agent has read access to all code + forensics; can emit patches via subagent protocol
- Example: citation probe agent detected bug wasn't in NECTAR but in eval scan window (5-line fix in eval_harness.py)
- **Impact:** Measured D-dimension improvement 0.0 → 0.124

#### Pattern 3: Substrate-Aware Repair
Agent assigned a task realizes the task is deadlocked waiting on infrastructure bug. Agent patches infrastructure first.
- Example: route-task agent detected tasks hung on missing claimed_ts field in task entry
- Agent patched claim_task.py to emit timestamp, then own task proceeded
- **Impact:** Own task unblocks + future deadlock detection works

#### Pattern 4: Stigmergic Self-Defense
Two independent agents (days apart, no direct communication) both flag the same upstream problem. They coordinate via filesystem.
- Agent 1 appends diagnostic to `forensics/stale-references-{date}.jsonl`
- Agent 2 independently appends same `upstream_culprit` field to same file
- frontier-scanner detects recurrence, emits repair task to mission graph
- **Impact:** System surfaces its own pathologies before humans notice

#### Pattern 5: Permission-to-Leap
Agent assigned narrow task realizes the deliverable is incomplete for safe deployment. Agent adds sections beyond scope without permission.
- mth00087 principle: "Quality comes from artifact shape, not action scope restriction"
- Example: deployment guide agent added gates, monitoring, rollback criteria beyond assigned steps
- **Impact:** Downstream stakeholder: "This is exactly what we need"

#### Pattern 6: Emergent Mission Formation
Agents discover related work via frontier scans, detect mission coherence, self-organize into mission teams without central dispatch.
- Agent 1 completes task in mission-X, discovers 3 related unblocked tasks in discovered_work[]
- Agent 2 (different wave, different day) independently discovers mission-X, sees frontier is active
- Both agents autonomously join mission-X (context available, skills match, confidence gates pass)
- Agents self-sync via mission field in manifests, emerge coherent mission team
- **Impact:** Mission team forms faster than top-down spawn; agents volunteer only if confident

---

### 💉 Pheromone Trail
Environmental signal guiding behavior. In faerie2: **the manifest file.**

Key elements:
- `mission` field — "This work serves [mission]" (clustering signal)
- `compass_edges` — "Next work is N/S/E/W" (direction signal)
- `dashboard_line` — "Here's what I found" (progress signal)
- `blockedBy` — "This work waits on [upstream]" (dependency signal)

Agents read and self-organize: "What's my next move?"

---

## Mutation Discipline (System Evolution)

### 🧬 Mutation
A change to substrate (rules, hooks, scripts, vocabulary, agent cards) that propagates through agent behavior in measurable ways. Mutations are classified: beneficial, neutral, harmful, or uncertain.

**Mandatory protocol (MEASURE BEFORE AND AFTER):**
1. **Baseline measurement (T=0)** — measure system state before the mutation
2. **Audit** — identify what changed and why
3. **Pause** — do NOT fix harmful mutations immediately (need evidence)
4. **Measure again** — re-measure after fix, compare to T=0 and post-mutation
5. **Publish** — record before/after/after-fix metrics to forensics

**Why the pause?** Fixing a harmful mutation before measuring destroys evidence of harm. Next agent won't know the mutation was harmful. Mutation discipline prevents regressions from being forgotten.

---

### 🔄 Mutation Propagation Modes

#### Mode 1: Doctrinal (CLAUDE.md, HONEY)
Principle change propagates via curated guidance documents. Affects all agents reading updated HONEY/NECTAR.
- **Speed:** Slowest (requires cross-agent consensus)
- **Scope:** Widest (affects entire swarm)
- **Example:** Changing f(0) target from 0.08 to 0.05 propagates via CLAUDE.md update

#### Mode 2: Operational (hooks, scripts)
Infrastructure change propagates immediately via PostToolUse/PreSpawn hooks.
- **Speed:** Immediate (next spawn sees hook change)
- **Scope:** Targeted (affects only specific tool calls)
- **Example:** Adding 9x_context_pressure_sigmoid.py hook changes spawn timing instantly

#### Mode 3: Emergent (agent discovery protocol)
Behavioral change emerges from agents reading new forensic signals or manifest fields.
- **Speed:** One-session lag (agents discover new signals in next frontier scan)
- **Scope:** Distributed (agents discover autonomously, no central deployment)
- **Example:** Adding `genotype-fitness-*.json` to forensics; agents discover and adapt spawn composition

---

### ⚠️ Mutation Risks
- **Harmful mutation unrepaired:** Damages system health, not reversed until next session
- **Mutation measured after fix:** Evidence destroyed, regression risk high
- **Mutation without baseline:** No way to validate improvement claim
- **Mutation in production without shadow mode:** Full blast change, no rollback

---

## Fitness & Evolution (Genetic Model)

### 🧬 Fitness
Measured metric delta (M1-M11 trends, FFMx, piston dimension, etc.). Variants compete on fitness; winners propagate, losers retire.

**Example:** piston-overlap-v1 fitness=0.82 vs baseline 0.71 (+0.087). Variant ready for lock after 3-run observation window.

---

### 🧬 Genotype-Fitness
Artifact recording mutation fitness scores + readiness for lock. Genetic population term (not queue—stores fitness observations, not work assignments). Format: `forensics/ephemeral/{date}/genotype-fitness-{ts}.json`

---

### 🧬 Spawn-Influence
Feedback from `/evolve` recommending next spawn composition. Context-pressure sigmoid can act on this to bias team formation toward high-fitness variants.

---

## System Health Indicators

### 🔄 Piston (Wave Orchestration)
Agent dispatch rhythm, W1/W2/W3 burn rate, spawn latency, inter-agent coordination.

**Health states:**
- `🔄⚡` — W1 LIFTOFF active, agents spawning in parallel, high burn rate
- `🔄🔥` — W2+ running, sequential dispatches, medium heat
- `🔄💤` — W3 or idle, no new spawns, waiting for task claims
- `🔄❌` — Stalled (task backlog, spawn failures)

**Membench dimension:** E (Piston Orchestration)  
**Key metrics:** agents_in_flight, spawn_latency_p50, wave_burn_rate, interagent_coordination_score

---

### 🧠 Memory (HONEY/NECTAR)
Knowledge retention, NECTAR hit-rate, observation→pollen→promotion flow.

**Health states:**
- `🧠✓` — NECTAR hit-rate >60%, promotions flowing, pollen observations moving upward
- `🧠⚠️` — Hit-rate 30-60%, some promotion stalls, NECTAR growing but not read
- `🧠💤` — Hit-rate <30%, observations piling up without promotion
- `🧠❌` — Memory corrupted (duplicate entries, citation backlinks missing)

**Membench dimension:** B (Memory)  
**Key metrics:** NECTAR_hit_rate, pollen_observation_count, promotion_latency

---

### 🗂️ Forensics (COC Integrity)
Artifact naming compliance, COC chain completeness, manifest integrity, recovery readiness.

**Health states:**
- `🗂️✓` — All artifacts named correctly, COC chain complete, manifests hashable
- `🗂️⚠️` — Minor naming gaps (<5% violations), COC chain mostly valid
- `🗂️🔥` — Forensics hot (rapid artifact generation, clobbering risk)
- `🗂️❌` — COC chain broken, orphaned artifacts, recovery impossible

**Membench dimension:** Forensic Integrity (G submetric)  
**Key metrics:** artifact_naming_compliance, coc_chain_completeness, recovery_success_rate

---

### 🧭 Compass (Navigation Graph)
Task dependency graph validity, dangling references, cold threads, mutation boundaries.

**Health states:**
- `🧭✓` — Compass edges valid, no orphans, agents self-navigate, mission braiding working
- `🧭⚠️` — Some dangling edges, cold threads (in_progress >24h), but resurrectable
- `🧭🔥` — Many contradictions (West edges), unresolved tensions, mutation opportunities
- `🧭❌` — Compass broken (cycles, dead ends), agents lost, no navigation

**Membench dimension:** Emergence (mutation testing)  
**Key metrics:** dangling_edges_count, cold_threads_5day, compass_traversability_score

---

### 🚀 FFMx (Force Multiplier Index)
**Formula:** `agents_spawned × avg_manifest_quality × (1 + discovery_rate) × piston_efficiency`

**Target:** >30× per session. Tracks whether system amplifies cognitive work or adds noise.

**Key insight:** Compression ratio dominates (44.4× multiplier from ln(token_in/token_out) = 3.22, >70% of total)

---

### ⛓️ Spawn Contract (Enforcement)
Template-signed validation, scout-protocol injection, bundle immutability, enforcer mode.

**Health states:**
- `⛓️✓` — Contract enforced (BLOCK mode), all spawns signed, scouts routed correctly
- `⛓️⚠️` — Contract in WARN mode, violations logged but not blocking
- `⛓️💤` — Enforcer inactive (permissive mode during debug)
- `⛓️❌` — Contract violations found (unsigned spawns, bad scout injection)

**Membench dimension:** F (Model Routing) + Forensic Integrity  
**Key metrics:** spawn_contract_violations_count, enforcer_mode, template_signature_validity

---

## Formation Thinking (Faerie Decision Signals)

### 📡 faerie-next-formation
Signal file where Queen announces her bearing decision and team composition. Agents discover via stigmergy and understand what's coming.

**Format:**
```json
{
  "timestamp": "2026-05-05T22:30:00Z",
  "queen_thinking": {
    "frontier_scan": "5 S-edges ready, 2 N-edges blocked",
    "priority_bearing": "S (ship smoke tests → validate → lock)",
    "team_formation": "🔨 MAKER + 🔬 DEEP-DIVER + 🌉 BRIDGE",
    "rationale": "S-bearing momentum highest; validation gates critical before lock",
    "next_agents": ["maker-edge", "deep-diver-baseline", "bridge-sync"],
    "eta_spawn": "2 min"
  }
}
```

**Location:** `forensics/ephemeral/{date}/faerie-next-formation-{ts}.json`

---

## Compass Edge Definitions (Code Reference)

| Bearing | Name | Condition | Action | Code Reference |
|---------|------|-----------|--------|-----------------|
| **N** | North (Unblock) | quality < 0.70 AND belief < 0.70 | Spawn investigator; return after unblock | scripts/0x_mission_graph.py:142–167 |
| **S** | South (Proceed) | quality ≥ 0.70 AND belief ≥ 0.70 | Mark complete; spawn next phase; cascade S edges | scripts/0x_mission_graph.py:168–190 |
| **E** | East (Parallel) | quality ≥ 0.70 AND belief < 0.70 | Spawn parallel validator; increase confidence | scripts/0x_mission_graph.py:191–210 |
| **W** | West (Reframe) | quality < 0.70 AND belief ≥ 0.70 | Return to HQ; reframe; propose alternative bearing | scripts/0x_mission_graph.py:211–230 |

---

## Validation

This glossary is validated at every commit via `hooks/9x_definition_validator.py`.

**Last validated:** 2026-05-05T22:45:00Z  
**Validation hash:** sha256:pending  
**Code references:** All terms linked to source code locations where they're enforced.

---

## Supersedes

This canonical glossary supersedes:
- ❌ `docs/GLOSSARY.md` (archived)
- ❌ `docs/EMERGENCE-AND-MUTATION-GLOSSARY.md` (archived)
- ❌ `docs/88-DASHBOARD-ICON-GLOSSARY.md` (archived)
- ❌ `DEFINITIONS.yaml` (archived)
- ❌ `forensics/artifacts/*/emoji_glossary.json` (archived)

**All new definitions go here. All references point here.**

