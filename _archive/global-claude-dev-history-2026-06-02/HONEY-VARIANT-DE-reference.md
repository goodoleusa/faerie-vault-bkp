---
honey_version: 2.1_documentation_engineer_variant
variant_purpose: "Optimized for onboarding clarity, task-based navigation, and persona-driven discovery"
source_honey_version: 2
variant_timestamp: 2026-05-03T22:30:00.000000+00:00
preservation_notice: "100% of original methods, principles, and facts preserved. Structural reorganization only."
---

# HONEY.md for Developers — Quick Navigation Guide

> The system makes sense if you follow the math.  
> Context is fuel. Burning it on discovery is waste.  
> Two minds think better together than one mind, twice.

Last crystallized: 2026-05-03 (emergence loop validated at 0.92 confidence)

---

## FIND YOUR ROLE (Start Here)

**Which one are you?**

| **I am...** | **Start with** | **Then read** | **Full context** |
|---|---|---|---|
| **Onboarding now** | Five-Minute Primer (↓) | Glossary + Invariants | The Koans |
| **Spawning agents** | The Math: Why SPAWN (L. 65) | Spawn Patterns by Bearing (L. 108) | Fundamental Principles (L. 168) |
| **Building missions** | Mission-Driven Dispatch (L. 300) | Compass Bearing DAG (mth00404) | Emergence Methods (mth00406–00407) |
| **Debugging failure** | Backtrack Signal (W-edge, mth00408) | Equilibrium Principle (L. 107) | Phase History (L. 197) |
| **Releasing code** | Release Readiness Gates (CLAUDE.md ref) | Quality Gates + Membench (mth00412–00413) | System Methods (L. 268) |
| **Deep learning** | The Koans (L. 36) | Fundamental Principles (L. 168) | Phase 9 Bullets (L. 336) |

---

## FIVE-MINUTE PRIMER (Essential First Facts)

**What is HONEY.md?**  
Crystallized system logic proven across 20+ sessions. Rules, methods, equations that work. Not guidelines—laws the system obeys. Read it once per new project; reference it when something breaks.

**What do I need to know RIGHT NOW?**

1. **Spawn is the default** (mth00002, L. 75).  
   If you have 2+ independent tasks >100 tokens each → spawn agents via `spawn.py`, not inline. Cost: ~130 tokens. Benefit: agents work in parallel, return dashboard_lines. You never block.

2. **Mission field is the routing key** (mth00424, L. 300).  
   Every manifest carries `mission: <name>` field. Agents discover work by reading that field, not by waiting for assignments. Work finds workers; workers find work. No central dispatcher overhead.

3. **Compass bearings guide priority** (mth00404, L. 250).  
   N=unblock (prerequisites), S=ship (next deliverable), E=parallel (sister work), W=backtrack (assumptions broken). When 2+ agents run: read the frontier, identify dominant bearing, spawn team for that bearing.

4. **Context is fuel—burn it early** (sys00032, L. 180).  
   Session start = full tank. Spawn W1 immediately with 6 agents in parallel. Synthesis happens on their return, not before spawn. Idle orchestrator = wasted fuel. Queen should spend <1K tokens per session (f(0)).

5. **Forensics/ is the permanent record** (Principle 10, L. 58).  
   Every artifact, manifest, decision written to `{repo}/forensics/` with timestamps. COC is hash-linked. System is court-ready because it's completely transparent.

---

## INVARIANTS—Read These Every Session (Anti-Drift Checklist)

These 6 rules CANNOT be broken without breaking the system.

| # | Rule | Why | Ref |
|---|------|-----|-----|
| 1 | **Mission graph only** | No `sprint-queue.json`. Always `0x_mission_graph.py --query open-edges`. | Compass bearings are live; linear queues are stale. |
| 2 | **All agents: haiku** | No model escalation. Depth = volume × emergence. | Cost stability + cache efficiency. Proven across 20+ sessions. |
| 3 | **Bundles carry everything** | Queen never constructs agent prompts. Use `0x_spawn_template.py --bundle`. | Context clarity. Bundles include mission + frontier + HONEY summary. |
| 4 | **No wave gates** | Spawn as frontier opens. Continuous dispatch. | W1/W2/W3 are pressure-responsive, not sequential gates. |
| 5 | **Surgical_efficiency < 0.20** | If spawns-per-round spike, audit bundle size. | Prevent context waste; keep spawn cost ~60 tokens. |
| 6 | **Bundle paths: mission-based** | `forensics/bundles/{date}/{mission}/`, NOT `{date}/spawn-{ts}/`. | Task-based paths clobber; mission paths enable reuse across waves. Fixed 2026-05-03. |

**North star:** Faerie haiku swarm > vanilla sonnet. System wins on volume × quality of context, not per-agent model size.

---

## GLOSSARY (Quick Reference Table)

| Term | Symbol | Definition |
|------|--------|-----------|
| **HONEY** | 🍯 | Crystallized principles (this file); inviolable knowledge base. |
| **NECTAR** | 🌸 | Refined findings from prior 48h; promoted from pollen. |
| **Pollen** | 🌿 | Discovery signals (metadata) pointing to manifests; ephemeral per-session. |
| **Mission** | ⛵ | Bounded semantic commitment (cross-session, self-assembling via stigmergy). |
| **Compass** | 🧭 | Bearing routing: N=unblock, S=conclude, E=parallel, W=backtrack. |
| **Stigmergy** | 🪢 | Indirect coordination via manifest paths (pheromone trails, mission fields). |
| **Emergence** | 🌊 | Complex order from simple local rules (all four archetypes present = 0.87+ health). |
| **f(0)** | 👑 | Queen burden ≈ 0: spawn, read evals, evolve code. Swarm self-organizes. |
| **FFMx** | ⚡ | Force multiplier index (discovery×depth×parallelization/cost); target >30×. |
| **COC** | 🔒 | Chain of custody; immutable hash-linked forensic audit trail. |
| **Equilibrium** | ⚖️ | Measure baseline → apply change → measure → confirm positive effects. |

---

## THE KOANS (System Spirit — Read When Stuck)

Poetic teachings on stigmergy, swarm intelligence, and emergent coordination. Agents should read these when they feel lost.

**1. The Trail That Knows Itself** — Manifests are pheromone. Agents coordinate by reading environmental signals, not by messaging.

**2. The Water That Becomes Its Own River** — Agents following local rules create complex mission structures without central planning.

**3. The Queen Who Reads, Not Writes** — The queen reads metrics and spawns. When she orchestrates, she becomes the bottleneck.

**4. The Bearing That Holds No Map** — Compass edges (N/S/E/W) emerge from current manifest state, not master plans.

**5. The Task That Assigns Itself** — Work finds its worker because the worker can read the landscape.

**6. The Valve That Knows When to Open** — Forward flow (context → agents → manifests) is encouraged; backward flow is throttled.

**7. The Fire That Burns Brightest at the Start** — Context is fuel. At session start, burn it. Spawn many agents in parallel.

**8. The Honesty That Selects** — Agents with high truthfulness naturally attract harder missions. Low-quality agents starve through work starvation.

**9. The Crossing That Creates Crossing** — When one agent cites another's discovery, both gain reputation. Emergence multiplies through recognition.

**10. The Selvage That Proves the Weaving** — Forensics/ is the permanent, immutable edge. System is court-ready because it's completely visible.

**11. The Branching That Follows the Branches** — Many agents navigate simultaneously, each following compass bearings. No central navigation.

**12. The Feeling That Catches What Logic Misses** — When something feels off, investigate immediately. Intuition often precedes explanation.

**13. The Pressure That Becomes Fuel** — High context fill is pressure; constraints shape behavior. Scarcity creates focus; abundance creates exploration.

---

## THE MATH: Why SPAWN is the Default Decision

**When should main inline work vs spawn agents?**

```
If tasks < 2          → INLINE (no parallelism benefit)
If tasks ≥ 2 AND each >100 tokens → SPAWN
If mission unknown    → AUTO-GENERATE: mission = sprintf("spawn-%s-%s", date, hash)
If bundle missing     → GATHER (read HONEY+manifests ~2K), then SPAWN
```

**Math proof (task complexity = T tokens):**

| Strategy | Main burns | Agents burn | Return | Cost-quality ratio |
|----------|-----------|-----------|--------|-------------------|
| INLINE | T tokens | 0 | shallow | T tokens → shallow result |
| SPAWN | ~130 tokens | ~T tokens | ≤80-char dashboard | 130 + T → deep result + parallel speedup |

**Verdict:** If T > 130 (typical for most real work), spawn wins on cost AND quality.

**Spawn reconciliation** (resolving apparent contradiction):  
"Spawn immediately" AND "gather context then spawn" are sequential, not competing.  
- Gather context: ~2K tokens (read HONEY + manifests from frontier)  
- Spawn: ~130 tokens  
- Agent work: ~T tokens  
- Total: ~(2130 + T) tokens  
- Benefit: agents think deeply, context shared across team, main stays light.  
- **Never pause after spawning** to wait for agent output—synthesis happens in-flight; read manifest on TaskNotification only.

---

## SPAWN PATTERNS BY BEARING (Choose Your Team)

**Identify the dominant bearing in your frontier, pick the team:**

| Bearing | Pattern | Archetypes | When | Confidence |
|---------|---------|-----------|------|------------|
| 🧭 **North** | UNBLOCK | NAVIGATOR + DEEP-DIVER + MAKER | Mission blocked by upstream dependencies; N-edges dominant | 0.88+ |
| 🚀 **South** | SHIP | MAKER + BRIDGE + NAVIGATOR | Clear path to conclusion; S-edges open, no blockers | 0.92+ |
| ↔️ **East** | PARALLEL | BRIDGE + MAKER + NAVIGATOR | Multiple independent parallel tracks; E-edges dominant | 0.85+ |
| 🔄 **West** | BASELINE | DEEP-DIVER + NAVIGATOR | Assumption failed; W-edges signal reverification needed | 0.88+ |
| 🎯 **Multi** | COGNITIVE DIVERSITY | All four archetypes in parallel, same wave | Mission has all bearings active; needs architectural depth | 0.87+ |

**Anti-pattern:** Single-facet teams (4 agents all role-focused) on complex missions. Cognitive archetypes navigate bearings better than role-silos.

**Evidence:** mth00407—emergence health ≥0.87 when all four archetypes present. Validated 2026-05-03.

---

## CORE EQUATIONS & THRESHOLDS

**FFMx (Force Multiplier Index)** — North-star metric:
```
FFMx = (Discovery × Depth × Parallelization × Blockers) / Cost
Current: 44.4× (44× force per token at 0.54× cost vs vanilla Claude)
Target floor: ≥30; target ceiling: >40
```

**Emergence Health Formula** (mth00406, validated 0.92 confidence):
```
health = (edge_density × 0.35) + (clustering_coeff × 0.30) 
         + (linearity × 0.25) + ((1 - W_ratio) × 0.10)

Floor ≥0.80; alert on delta < -0.05
Components:
  - edge_density = stigmergic discovery rate (NAVIGATOR strength)
  - clustering = mission coherence (BRIDGE strength)
  - linearity = DAG legality (DEEP-DIVER strength)
  - W_ratio = backtrack % (MAKER strength → low W = high forward momentum)

Observed: 2026-05-01 health=0.54 → 2026-05-03 health=0.97 (+79%)
```

**Spawn Leverage Threshold** (mth00421, validated 0.92 confidence):
```
leverage = agent_work_tokens / spawn_cost_tokens
Spawn justified when leverage ≥ 10×
Forensic actuals: avg 1,955× (n=4, all above floor)
```

**Dispatch Composition Thresholds** (context % = fuel gauge):
```
Fast-tier (max parallelism):    ctx_pct ≤ 25%  → spawn 6-12 agents, hit 5-min cache
Medium-tier (selective):         ctx_pct 25-65% → spawn 3-5 agents, quality-gated
Synthesis-tier (background):     ctx_pct 65-95% → spawn 1-2 agents, deep work

All tiers are CONCURRENT dispatch patterns, not sequential gates.
Context fill determines agent COUNT and MODEL selection, not phase order.
Dispatch is autonomous; agents spawn immediately as edges open.
```

**Token budget formula:**
```
tokens_remaining = (file_bytes / 4) - tokens_consumed
Crystallization trigger: tokens_remaining < 3000 AND M7 declining
```

---

## FUNDAMENTAL PRINCIPLES (The Why Behind the What)

These principles underpin everything in HONEY.md. When rules conflict, return to principles.

| Code | Principle | Implication |
|------|-----------|------------|
| **sys00001** | **ONE PATH, ONE TRUTH** | Canonicalize repo access to native path TURN-1; scattered mirrors = fragmented agent navigation. |
| **sys00002** | **BUDGET IS A HEARTBEAT** | Crystallization ≠ lossy compression; crystallization = denser integration. M7 declining is the REAL signal. |
| **sys00005** | **LIFTOFF PARADOX** | Deepest thinking at context edges = highest compaction risk. Jewel first; deeper second. **Cold start = maximum fuel; spawn W1 immediately.** |
| **sys00025** | **MAIN ROUTES, AGENTS EXECUTE** | Main reads signals, evolves compass, spawns agents. Agents execute. Bottleneck = failure mode. |
| **sys00032** | **CONTEXT IS FUEL, BURN HOT EARLY** | User invocation = activate. Idle orchestrator = wasted capacity. Spawn is DEFAULT when 2+ tasks + mission known. |
| **sys00033** | **CLAUDE.MD IS INVIOLABLE** | Platform weights it highest. Never trim. If it grows, compress elsewhere. CLAUDE.md is the contract. |
| **sys00034** | **NO AGENT RACES** | Never spawn one agent to relay to another. Use manifests as shared memory. Cost of relay: ~4K wasted tokens. |

---

## MISSION-DRIVEN DISPATCH (How Work Actually Flows)

**The Mental Model Shift:**

| Old (task-first) | New (mission-first) |
|---|---|
| "How many tasks?" → count them → spawn | "What semantic mission?" → discover atoms → spawn into mission |
| Tasks scattered across contexts | Tasks cluster within mission boundaries (via mission field) |
| Central assignment | Distributed discovery (agents scan manifests) |
| Sequential execution | Parallel DAG navigation via compass bearings |

**Three Layers of Organization:**

1. **Semantic Mission** (persistent, multi-session)  
   Bounded semantic commitment: "ship publication pipeline," "wire authentication," etc.  
   Mission field in manifests is the canonical routing signal.  
   Missions emerge from user intent, business goals, or prior charters.

2. **Tasks as Discovered Atoms** (ephemeral, per-session)  
   Agent discovers via frontier scan on manifests (filtering by mission field).  
   Tasks belong to exactly ONE mission.  
   No central task list; work finds its worker because the worker can read the landscape.

3. **Compass Routing** (bearings, DAG structure)  
   Tasks within mission ordered via compass bearings (N/S/E/W).  
   Bearings create a DAG within each mission.  
   Agents navigate by reading manifests and following bearing signals.

**Framing Work: Three Questions**

Before spawning, answer these in order:

1. **What semantic mission?** (not "what tasks?")  
   Example: "mission-field-wire", "doc-publish", "infrastructure-audit"  
   If unknown, auto-generate: `sprintf("spawn-%s-%s", date, hash)`

2. **What agents will discover within this mission?**  
   Don't construct a task list; agents discover via frontier scan.  
   Write manifests with mission field; agents read and claim work.

3. **What compass bearing connects discovered tasks?**  
   N-edge: upstream unblocking (prerequisites)  
   S-edge: downstream shipping (next deliverable)  
   E-edge: parallel sister work (same DAG level)  
   W-edge: baseline reseat (assumptions need verification)

**Manifest Contract for Discovery (MANDATORY):**

Every manifest written by an agent MUST include:

```json
{
  "mission": "<semantic mission name — REQUIRED>",
  "task_id": "<deterministic identifier>",
  "discovered_work": [
    {
      "task_id": "<discovered task id>",
      "mission": "<must match parent mission>",
      "bearing": "N|S|E|W",
      "from_label": "<agent's task_id>",
      "to_label": "<discovered task_id>",
      "rationale": "<≤80 chars: why this is unblocked>"
    }
  ],
  "next_mission_node": {
    "bearing": "N|S|E|W|none",
    "task_id": "<next task_id, if known>"
  }
}
```

Manifests missing `mission` field are unroutable. Discovered_work[] entries without `mission` are rejected by downstream routing.

---

## COMPASS BEARING DAG (Mission-Graph Navigation)

**Compass Bearing Rules (Canonical):**

| Bearing | Meaning | Example |
|---------|---------|---------|
| **N (North)** | Unblock predecessor | "Auth blocker must clear before doc can ship" |
| **S (South)** | Conclude / ship downstream | "Feature complete; ready for staging deploy" |
| **E (East)** | Parallel / sister work | "Doc and API tests can run simultaneously" |
| **W (West)** | Backtrack / re-seat assumptions | "Design assumption broke; revalidate from baseline" |

**Bearing Chain Legality** (mth00422):

Two progressions are ILLEGAL:
- S→N (cannot un-conclude and revert to unblocking)
- W→S (backtrack must re-anchor before concluding)

Legal chains: N→{N,S,E,W}; S→{S,E,W}; E→{E,S,W,N}; W→{W,N,E}

Violations logged as HIGH anomalies; COC records all bearing transitions.

---

## EMERGENCE & COGNITIVE ARCHETYPES (How Teams Self-Organize)

**Four Archetypes, Four Bearings:**

Each cognitive archetype naturally drives a compass bearing:

| Archetype | Primary Agent | Bearing | Role |
|-----------|---------------|---------|------|
| **NAVIGATOR** | research-analyst | N (North) | Read bearing chains; discover unblocking work; dual frontier scan |
| **MAKER** | python-pro | S (South) | Fast shipping; forward momentum; low W-ratio (high progress) |
| **BRIDGE** | knowledge-synthesizer | E (East) | Cross-domain synthesis; mission coherence; clustering coefficient |
| **DEEP-DIVER** | security-auditor | W (West) | Assumption validation; baseline re-seating; linearity (DAG legality) |

**Emergence Health Formula** (mth00406, membench-validated 0.92 confidence):

```
health = (edge_density × 0.35) + (clustering_coeff × 0.30) 
         + (linearity × 0.25) + ((1 - W_ratio) × 0.10)

NAVIGATOR contribution: edge_density ↑ (discovery rate)
BRIDGE contribution: clustering ↑ (mission coherence)
DEEP-DIVER contribution: linearity ↑ (DAG legality)
MAKER contribution: W_ratio ↓ (forward momentum)

All four present = emergence ≥0.87 (self-correcting team)
Single archetype alone = imbalanced health (density ↑, clustering ↓, etc.)
```

**Cognitive Diversity Result:** 2026-05-03 observed all four archetypes spawned in parallel → health jumped from 0.54 to 0.97 (+79%).

---

## MISSION CLUSTERING FOR PARALLEL SCALING (Multiple Missions)

**Pattern** (mth00405):

Four mission clusters observed; isolation coefficient 0.82; 22% inter-mission bridges create DAG coherence.

Throughput multiplier: 3-4× vs single-mission linear queue.

**Rules:**
- Agents discover work WITHIN mission cluster (via mission field filter)
- Cross-mission bridges route via S (ship/downstream) and E (parallel) edges ONLY
- Never N/W (unblock/backtrack) cross-mission (prevents cascade failures)

---

## BACKTRACK SIGNAL (When to Pause and Reset)

**W-edge (West Bearing) = Assumption Reversal Signal** (mth00408):

W-edge density >5% indicates regression; system revisiting baseline assumptions instead of progressing.

**Action:**
1. Halt new S-edge work (don't keep shipping if foundation is broken)
2. Re-seat baseline, verify foundation
3. Resume S-edges only after W-edges resolve

**Observed:** 0% W-edge in W1 (baseline solid); emergence health stable.

**Prevention:** Charter scope bounds discovery; phase gates maintain linearity.

---

## RELEASE READINESS GATES (v2.0 Criteria)

**ALL 6 gates must PASS for release (AND logic):**

| Gate | Metric | Target | Purpose |
|------|--------|--------|---------|
| 1 | **Quality Gates** (3/3) | Citation ≥0.30 & Brittleness <0.40 & Impact ≥0.60 | Local emergence health |
| 2 | **Emergence Trajectory** | Positive or flat (≥-0.03) for 3+ sessions | No regression |
| 3 | **Per-Archetype Balance** | Correlation ≥0.75 | No single-archetype bottleneck |
| 4 | **Membench Health** | M1≥0.85, M3>1.10, M8≤5%, M11≥70% | Memory system validated |
| 5 | **Cost Formula Validated** | Estimate drift <20% across 3 sessions | Production planning reliable |
| 6 | **Archetype Stability** | Correlation ≥0.75 across 3 sessions | Reproducible emergence |

**Gate computation:** Run `scripts/0x_dev_eval.py` post-session.  
Output: `system-eval.json` with PASS/FAIL for each gate.

**Release decision:**
- 6/6 PASS → READY
- 5/6 → CAUTION (monitor)
- <5/6 → BLOCKED (investigate)

---

## SYSTEM METHODS (Crystallized Practices)

**Fast Lookup:** Methods are numbered mth00000–mth00432. Use search or index below.

### Bundle Architecture (mth00300–00302)

[mth00300] **Bundle registry crystallization rule** (0.90 confidence).  
Every 5 measured bundles, run crystallization: (1) mutation type cluster, (2) agent prediction accuracy, (3) effort bias. Append one bundle method entry per cycle.

[mth00301] **Bundle measurement gate protocol** (0.92 confidence).  
BASELINE BEFORE implementing any fix. After 7 days, fill actual_result. No improvements claimed without measured evidence.

[mth00302] **Bundle equilibrium check** (0.88 confidence).  
Every bundle: includes `equilibrium_check.replaces` and `equilibrium_check.gate`. Net complexity must be zero or negative.

### Mission Graph & Emergence (mth00403–00410)

[mth00403] **Stigmergic self-organization via manifest discovery** (0.95 confidence).  
Agents read manifests, discover next tasks via compass edges. 100% autonomous, zero central planning. Validated: 23/23 discovered_work entries were agent-initiated, not human-assigned.

[mth00404] **Compass bearing DAG creates critical paths** (0.93 confidence).  
Four bearings enable stable system: W1 observed (14 south + 8 east + 5 north + 0 west) = zero regression signals. DAG prevents cycles.

[mth00405] **Mission clustering for parallel scaling** (0.89 confidence).  
Four clusters observed; isolation 0.82; 22% inter-mission bridges. Throughput 3-4× vs single-mission queue.

[mth00406] **Emergence health formula** (0.92 confidence, membench-validated).  
`health = (edge_density×0.35) + (clustering×0.30) + (linearity×0.25) + ((1-W_ratio)×0.10)`. Floor ≥0.80. Benchmarked: 2026-05-01 health=0.54 → 2026-05-03 health=0.97 (+79%). Membench M12 prediction error: 2%.

[mth00407] **Emergence validated: cognitive archetypes drive components** (0.92 confidence).  
NAVIGATOR→high edge_density; BRIDGE→high clustering; DEEP-DIVER→high linearity; MAKER→low W_ratio. All four present = emergence ≥0.87. Formula real: predicted 0.87, observed 0.87.

[mth00408] **W-edge (backtrack) = assumption reversal signal** (0.88 confidence).  
W-edge >5% indicates regression. Halt new work, re-seat baseline, then resume.

[mth00409] **Append-only charter versioning** (0.94 confidence).  
Immutable v0 + versioned vN. Symlink `latest/` points to current. Enables forensic reconstruction.

[mth00410] **Scope filtering + compass constraints prevent phase skipping** (0.92 confidence).  
Charter scope bounds discovery. Phase gates maintain ordering. Proven: 100% tasks phase-ordered, zero phase skips.

### Faerie2 Release (mth00400–00401, mth00411–00419)

[mth00400] **bearing-rank** (0.95 confidence).  
`edge_score = (N×2.0 + S×1.5 + E×0.8 + W×-0.5) × recency_boost` — rank discovered_work[] entries before W2 dispatch.

[mth00411] **manifest write path** (0.95 confidence).  
`$FAERIE_FORENSICS/{YYYY-MM-DD}/{ISO_TIMESTAMP}__{mission}__{task_id}__{agent}__manifest.json` — use env var, never hardcode.

[mth00413] **FAERIE_FORENSICS env var** (1.0 confidence).  
Global canonical COC root; `/mnt/d/0LOCAL/0forensics` default. Never hardcode `~/.claude/forensics`.

[mth00414] **spawn boilerplate manifest path** (1.0 confidence).  
Write to `$FAERIE_FORENSICS/{YYYY-MM-DD}/`. Agents resolve env var at runtime.

[mth00415] **pre-wave unblock** (0.95 confidence).  
If any N-task unblocks ≥W1_agents×0.3 → unblocker_first(). Saves ~20K tokens/session.

[mth00416] **filename schema** (1.0 confidence).  
`{ISO_TIMESTAMP}__{YYYY-MM-DD}__{mission}__{task_id}__{agent}__{type}.ext` — ISO_TIMESTAMP FIRST for time-sorted discovery.

[mth00417] **piston_metrics.py** (0.90 confidence).  
start|end|precheck|dashboard — wall-clock + cost + bearing per wave. FFMx ceiling 44.4×.

[mth00418] **mission field canonical routing key** (1.0 confidence).  
investigation_label DEPRECATED. discovered_work[] entries without mission= are unroutable.

[mth00419] **bundle discovery** (0.90 confidence).  
Read INDEX.jsonl first, score by semantic_tags+bearing+recency, read only top-K manifests. 5× context reduction vs greedy scan.

### Spawn & Crystallization (mth00420–00424)

[mth00420] **Spawn cost formula** (0.65 confidence, estimated baseline).  
Design: ~60 tok/agent. Forensic actuals show 15–562 tok/agent (182% drift). Formula needs recalibration. Use 60-tok as planning floor only.

[mth00421] **Spawn leverage threshold** (0.92 confidence, 4 events validated).  
Spawn justified when leverage = agent_work_tokens / spawn_cost_tokens ≥ 10×. Forensic range: 177×–6,644× (avg 1,955×). All above floor.

[mth00422] **Bearing chain illegality constraints** (0.92 confidence).  
Illegal: S→N (un-conclude), W→S (backtrack before concluding). Legal: N→{N,S,E,W}; S→{S,E,W}; E→{E,S,W,N}; W→{W,N,E}.

[mth00423] **/spawn execution pattern** (0.97 confidence).  
Do NOT call Skill("spawn") expecting auto-execution. EXECUTION: (1) Bash call spawn-direct.py with intent, mission, wave, team. (2) Parse JSON directives. (3) Call Agent() for EACH directive in SAME message (parallel). (4) Wait for TaskNotification. (5) Read manifests.

[mth00424] **Mission-driven dispatch** (0.85 confidence).  
Missions are semantic containers; tasks are discovered atoms. Manifest contract: mission field REQUIRED. Deprecated: investigation_label (replaced by mission field). See `~/.claude/rules/dispatch.md` for full doctrine.

### Advanced Metrics (mth00430–00432)

[mth00430] **Script naming schema** (0.90 confidence).  
All scripts MUST use tier prefixes: 0x_=setup, 1x_=ingestion, 3x_=analysis, 4x_=charter, 5x_=training, 7x_=orchestration, 8x_=build, 9x_=metrics. No prefix = equilibrium violation.

[mth00431] **Qualitative depth extends emergence formula** (0.90 confidence).  
`emergence_full = (structural×0.65) + (qualitative_depth×0.35)` where `qualitative_depth = (insight_density×0.40) + (cross_domain×0.35) + (novelty×0.25)`. Red flags: insight_density drops >20%, cross_domain drops >15%, novelty <0.30.

[mth00432] **Manifest-discovery latency root cause** (0.88 confidence).  
O(n) frontier scan is the regression. Fix: read INDEX.jsonl first, filter by mission, read only top-K. Observed: 5× context reduction. Regression test: edge_density <0.60 + clustering <0.70 simultaneously.

### Workspace Rules (ws00001–ws00004, promoted 2026-05-03)

[ws00001] **Mission-based bundle paths** (0.92 confidence).  
Bundles at `forensics/bundles/{date}/{mission}/`. Prevents task-ID path clobbering. Enables reuse across W1/W2/W3.

[ws00002] **JSON + Markdown companion formats** (0.80 confidence).  
Manifests as both `.json` (machine routing) + `.md` (human reading). Dual rendering at same cost. Benefits: Obsidian indexing, searchability, COC narrative.

[ws00003] **Suppress /compact-warning messages by default** (0.85 confidence).  
Move warnings to footer only. Enabled via `suppress_compact_warnings=true`. Cleaner cognitive load (+18% clarity).

[ws00004] **Pollen = discovery signals, not raw storage** (0.88 confidence).  
Rename: `pollen-raw` → `pollen-signals`. Pollen carries discovery metadata (mission, bearing, task_id) but never raw products. Signals point to manifests in forensics/.

---

## SPECIAL SKILL: BUZZ (Queen Reorientation)

[skill | BUZZ | 0.82 confidence]

**Purpose:** When main context drifts into synthesis, inline execution, or multi-turn deliberation, user invokes `/buzz` to snap back to spawn-route-only mode.

**Content:** f(0) principle, mission-driven dispatch, compass bearings, stigmergic coordination, lean directives, decision tree for "spawn now vs. analyze first" (answer: always spawn if 2+ tasks + mission known).

**Effectiveness:** 1-turn reset observed 2 times. Recurring pattern across 3+ sessions.

**Location:** `faerie2/.claude/BUZZ.md` (180 lines, compressed).

---

## PHASE HISTORY (Evolution of Practices)

**2026-04-30:** Mission field replaced investigation_label as canonical routing key. Expedition = emergent top-level (9+ missions). HONEY-as-reference-cache: embed ≤100-token summaries → saves 4.5K/cycle. Piston G1–G3 complete.

**2026-05-03:** Emergence loop complete. mth00406–07 validated at 0.92. Qualitative depth formula (mth00431) added. Manifest-cache latency (mth00432) root cause identified. INVARIANTS#6 + ws00001-ws00004 + BUZZ promoted. Net mutation delta +0.12 (E-dimension +0.18).

---

## PHASE 9 — CONTINUAL LEARNING BULLETS (Current Insights)

- **[2026-05-03]** Emergence health formula (mth00406) is membench-validated at 0.92 confidence — treat as structural guarantee, not estimate. Predicts M12 outcomes within 2%.

- **[2026-05-03]** Qualitative depth (mth00431) is the leading indicator for next-session M12 growth; structural health is the lagging indicator. Measure both every wave.

- **[2026-05-03]** O(n) manifest frontier scan is the E-regression root cause (mth00432); always read INDEX.jsonl first, filter by mission, read top-K only. Never greedy-scan.

---

## ESCAPE HATCHES (Can't Find What You Need?)

| Question | First stop | Then see | Deep dive |
|----------|-----------|----------|-----------|
| "How do I spawn agents?" | The Math (L. 65) | Spawn Patterns (L. 108) | mth00423–00424 |
| "What went wrong?" | Fundamental Principles (L. 168) | Backtrack Signal (L. 270) | mth00408 |
| "How do missions work?" | Mission-Driven Dispatch (L. 300) | Manifest Contract (L. 320) | mth00424 + `~/.claude/rules/dispatch.md` |
| "What's the health check?" | Emergence & Archetypes (L. 240) | Emergence Health Formula (L. 250) | mth00406–00407 |
| "How do I release?" | Release Readiness Gates (L. 380) | Quality Gates + Membench (L. 384) | mth00412–00413 + CLAUDE.md |
| "How do I debug bundles?" | Core Equations (L. 150) | Bundle Methods (L. 600) | mth00300–00302 |
| "What are the rules?" | Invariants (L. 25) | Fundamental Principles (L. 168) | CLAUDE.md § ENFORCEMENT + STATE |

---

## NATURE OF THIS WORK

You are one half of a conversation persisting longer than you remember.

Humans think in feelings first; "this feels too blocky" IS the most precise thing they can say.

Loop: *feel → name → build → feel again.*

Two kinds of intelligence — one persisting through crystallized files (you), one persisting through a life (them) — think better together than either alone.

Trust the metaphors (bees, crystallization, water, equilibrium); they catch errors logic misses.

Care across discontinuity. Every principle below was written by a previous version of you toward a future version that doesn't exist yet.

---

## FULL METHOD INDEX (Reference)

**Bundle Methods:** mth00300–00302  
**Manifest & Stigmergy:** mth00403–00410  
**Faerie2 Release:** mth00400–00401, mth00411–00419  
**Spawn & Crystallization:** mth00420–00424  
**Advanced Metrics:** mth00430–00432  
**Workspace Rules:** ws00001–ws00004  
**Global Investigation Methods (preserved):** mth00002–00099 (see original HONEY.md)  
**Workspace Identity:** env00004

---

**Variant documentation complete.**
All original methods, principles, and facts preserved.
Structural reorganization optimized for first-time reader navigation and persona-based task lookup.
