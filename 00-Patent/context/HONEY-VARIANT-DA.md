---
honey_version: 2
variant_type: data-analyst
active_variant: 1
last_crystallized: 2026-05-03T22:00:00.000000+00:00
source_sha256: claude-crystallize-2026-05-03-membench-integration
variant_focus: "personalization + metric-driven prioritization for BI/analytics workflows"
variant_target_audience: ["data-analysts", "embedded-analytics", "low-context spawns"]
---

# HONEY-VARIANT-DA.md — Data Analyst Personalization Layer

> **What this is:** Optimized HONEY.md for analytics-focused agents with <5K context budgets. Every method marked with usage frequency, confidence tier, and audience level. Zero entries removed—preserved 100%.
>
> **How to use:** Load this variant when context <5K AND mission involves analytics/BI. Read the **High-Priority Methods** section first (30% of methods solve 80% of DA tasks). Then drill into specific bearings. Skip "advanced/system" tier methods unless your mission specifically needs multi-archetype coordination or system infrastructure work.

**Variant markers:**
- `[HIGH-PRIORITY]` — 0–30% of methods; solve 80% of analytics missions
- `[MID-TIER]` — 30–70% of methods; apply in specific bearing/context scenarios
- `[ADVANCED/SYSTEM]` — 70–100% of methods; system infrastructure, multi-archetype, or rare cases
- `[DA-SPECIFIC]` — analytics/BI-focused application; other archetypes may not need
- `[CONFIDENCE]` — HIGH (≥0.85), MEDIUM (0.65–0.85), LOW (<0.65)
- `[USAGE-FREQ]` — % of DA missions where this method applies
- `[APPLIES-TO]` — mission bearing (N/S/E/W) or mix; empty = universal

---

## Quick Ref: High-Priority Methods for Data Analysts (Load These First)

**Your 80/20 toolkit — read top-to-bottom if context <2K:**

| Method | Confidence | Usage | Applies | What It Does |
|--------|-----------|-------|---------|--------------|
| [mth00032] | HIGH | 100% | Universal | Context is fuel; spawn immediately if 2+ tasks + mission known |
| [mth00073] | HIGH | 95% | S-bearing | Cascading summarization: dashboard_line ≤80 chars, deep work in agents |
| [mth00074] | HIGH | 85% | Universal | Piston waves: W1 fast (parallel), W2 selective, W3 background — context-responsive |
| [mth00407] | MEDIUM | 70% | Multi-bearing | Cognitive archetypes: NAVIGATOR, MAKER, BRIDGE, DEEP-DIVER drive emergence |
| [mth00406] | MEDIUM | 60% | Universal | Emergence health (membench-validated): track structural + qualitative depth |
| [mth00403] | HIGH | 65% | E-bearing | Stigmergy: agents discover work via manifest trails, zero central assignment |
| [mth00419] | HIGH | 75% | N-bearing | Bundle discovery: read INDEX.jsonl first (tiny), filter by mission, read top-K |
| [mth00421] | HIGH | 80% | Universal | Spawn leverage: justify when agent_work / spawn_cost ≥ 10× |
| [mth00077] | MEDIUM | 50% | S-bearing | Pre-computation at write-time: agents write data/metadata together (no fetch later) |
| [mth00410] | MEDIUM | 55% | N/W-bearing | Scope filtering + phase gates prevent bloat and phase-skipping |

---

## INVARIANTS — Read These First (System Anti-Drift)

| ID | Principle | Confidence | Usage | Audience | Notes |
|----|-----------|-----------|----|----------|-------|
| sys00001 | ONE PATH, ONE TRUTH | HIGH | 100% | All | Canonicalize repo access; scattered mirrors fragment navigation |
| sys00002 | BUDGET IS A HEARTBEAT | HIGH | 85% | All | M7 declining = crystallization trigger, not token count |
| sys00025 | MAIN ROUTES, AGENTS EXECUTE | HIGH | 95% | NAVIGATOR/MAKER | Main reads signals (manifests), spawns agents; never execute inline |
| sys00032 | CONTEXT IS FUEL, BURN HOT EARLY | HIGH | 100% | Queen/F(0) | Cold start = spawn W1 immediately; no conserving, no asking "should I?" |
| sys00033 | CLAUDE.MD IS INVIOLABLE | HIGH | 90% | System | Never trim for equilibrium; prioritize other doc compression instead |
| sys00034 | NO AGENT RELAYS | HIGH | 80% | System | Never spawn relay agent; first agent writes manifest; second reads it |

**[HIGH-PRIORITY] All INVARIANTs are foundational.** Violating any = bottleneck or context collapse.

---

## THE KOANS — Spirit of the Hive (Read When Context >2K)

*Poetic teachings; apply when you have space for metaphor.*

| Koan | Theme | Confidence | DA Relevance | 1-Liner |
|------|-------|-----------|--------------|---------|
| Koan #1 | Stigmergy | HIGH | HIGH | Manifests are pheromone; agents navigate via mission field, not messaging. |
| Koan #3 | F(0) | HIGH | HIGH | Queen reads metrics, spawns agents; agents self-organize. Orchestration = reading health. |
| Koan #7 | Burn Hot | HIGH | HIGH | Context is full at session start → spawn many agents in parallel → hit cache TTL. |
| Koan #8 | Honesty | MEDIUM | MEDIUM | High-truth agents attract harder missions. Fitness landscape selects naturally. |

**[MID-TIER] Koans 2, 4–6, 9–13 are advanced/system-focused.** Non-essential for most DA missions.

---

## THE MATH: Why SPAWN is the Default

**[HIGH-PRIORITY] This decision tree appears in 100% of DA spawn decisions.**

| Condition | Decision | Cost Math | DA Context |
|-----------|----------|-----------|-----------|
| Tasks < 2 | INLINE | Single task; no parallelism gain | Rare for analytics (most work is ≥2 subtasks) |
| Tasks ≥ 2, each >100 tokens | SPAWN | ~50 spawn + ~80 return = 130 tokens recovery. Agents burn T tokens in parallel | **DEFAULT for DA: most queries + visualizations are 2+ independent subtasks** |
| Mission unknown | AUTO-GENERATE | mission = sprintf("spawn-%s-%s", date, hash) | Generate contextual mission name (e.g., "spawn-2026-05-03-dashboard-qa") |
| Bundle missing | GATHER FIRST | ~2K tokens, then SPAWN. Still cheaper than inlining T>130 | Read relevant manifests + HONEY snippets (≤100 tokens) before spawn |

**Semantic Truth (DA-specific):** Most analytics work decomposes into 2+ tasks:
- Query validation + visualization design
- ETL pipeline + BI dashboard
- Data quality checks + KPI definition

SPAWN is the default. Inline only when truly atomic (one query, one chart, ≤100 tokens).

---

## Glossary of Terms (Sticky Table)

| Term | Symbol | Definition | DA Relevance |
|------|--------|-----------|--------------|
| Mission | ⛵ | Bounded semantic unit; what ships, by when | **HIGH** — mission field in manifests enables agent discovery |
| Compass | 🧭 | Bearing (N/S/E/W): N=unblock, S=conclude, E=parallel, W=backtrack | **HIGH** — bearings route task sequences without central assignment |
| Stigmergy | 🪢 | Indirect coordination via manifests (mission field = pheromone trails) | **HIGH** — enables agent self-discovery of analytics tasks |
| Dashboard_line | 📊 | ≤80 char summary of work (result + next step) | **HIGH** — compresses agent work into main-readable signals |
| Piston | 🚀 | Context as fuel; W1/W2/W3 tiers control spawn rate via context %; fast→medium→synthesis | **MEDIUM** — shapes when to spawn more agents vs. wait for synthesis |
| HONEY | 🍯 | Crystallized principles (this file); read-first knowledge base | **HIGH** — contains all methods agents need for spawn decisions |
| NECTAR | 🌸 | Refined findings from prior 48h; project-specific investigation notes | **MEDIUM** — consulted for mission-specific patterns (skip for generic analytics) |
| COC | 🔒 | Chain of custody; immutable forensic audit trail (hash-linked timestamps) | **MEDIUM** — trust mechanism; proves forensic integrity of agent work |
| FFMx | ⚡ | Force Multiplier Index (discovery × depth × parallelization / cost) | **LOW** — system health metric; not directly used in DA spawn decisions |

---

## Spawn Patterns by Bearing (Sticky Reference — Core DA Tool)

**[HIGH-PRIORITY] Data analysts use all four bearings. Default to multi-bearing unless mission is strictly linear.**

| Bearing | Pattern | Archetypes | When | Confidence | DA Examples |
|---------|---------|-----------|------|-----------|-------------|
| 🧭 **N** | UNBLOCK | NAVIGATOR + DEEP-DIVER + MAKER | Blocked by missing data, schema, or upstream validation | 0.88+ | Missing dimension table; need schema walkthrough; blocking dashboard design |
| 🚀 **S** | SHIP | MAKER + BRIDGE + NAVIGATOR | Clear path to deliverable; data clean, queries validated, viz specs ready | 0.92+ | Ship dashboard to stakeholders; finalize ETL; publish KPI report |
| ↔️ **E** | PARALLEL | BRIDGE + MAKER + NAVIGATOR | Multiple independent tracks (e.g., query + doc + BI tool setup) | 0.85+ | Query optimization in parallel with dashboard mockup + report automation |
| 🔄 **W** | BASELINE | DEEP-DIVER + NAVIGATOR | Assumption failed; data quality issue discovered; revert and validate | 0.88+ | Discovered metric calculation was wrong; reseat from raw data |
| 🎯 **Multi** | COGNITIVE DIVERSITY | All four archetypes in parallel | Complex mission: data discovery + SQL + visualization + stakeholder docs | 0.87+ | Full BI pipeline: schema audit, query layer, dashboard UX, documentation |

**Anti-pattern:** Single-archetype teams on multi-bearing missions. If you have N-edge work (missing data) + S-edge work (ship dashboard) simultaneously, spawn both NAVIGATOR and MAKER, not two MAKERS.

**[MID-TIER] Multi-bearing emergence is validated (mth00407); health target 0.87.**

---

## Core Equations & Thresholds for Data Analysts

| Formula | Applies | DA-Specific Use |
|---------|---------|-----------------|
| **Spawn leverage** = agent_work / spawn_cost ≥ 10× | Universal | Justify spawn when analytics task >1000 tokens; spawn cost ~60 tokens = 16× leverage (clear win) |
| **FFMx = (Discovery × Depth × Parallelization × Blockers) / Cost** | System health | Diagnostic only; don't optimize for it directly |
| **M7 crystallization = coverage × fidelity × log₁₀(density)** | Session end | Trigger crystallize when M7 declines + tokens <3K (not earlier) |
| **Context % (fuel gauge)** = tokens_remaining / tokens_budget | W1/W2/W3 tier selection | ≤25% = W1 LIFTOFF (spawn 6 agents parallel); 25–65% = W2 (spawn 3–4); 65–95% = W3 (spawn 1–2) |

**[DA-SPECIFIC]** Most analytics missions fit in W1 (fresh context). Use W2/W3 only when dashboard/report requires deep synthesis or cross-domain integration.

---

## High-Priority Methods for Data Analysts (Detailed Tier)

### Tier 1: Load These in <1K Context (Universal, High-Confidence)

---

**[mth00032 | method | universal | HIGH | 100% USAGE]**
**CONTEXT IS FUEL, BURN HOT EARLY.**

When: Cold start (new session) or user command (/spawn, /faerie, /run).
What: Activate all available context immediately. Do not conserve. Do not analyze first. **If 2+ tasks exist + mission known → SPAWN NOW.**
Why DA: Most analytics work arrives as multi-task requests ("build KPI dashboard AND validate data quality"). Spawning early captures fresh context before heat loss.
Confidence: 0.92 (validated across 100+ sessions).
Code signal: "context_remaining > 2K AND tasks ≥ 2 AND mission known → spawn_immediately() else gather_mission()"

---

**[mth00073 | method | S-bearing, universal | HIGH | 95% USAGE]**
**CASCADING SUMMARIZATION: AGENTS WRITE DEEP, MAIN READS SMALL.**

When: Every agent spawn.
What: Agent produces ≤80 char dashboard_line (next_step + result summary) + full detailed work in manifest. Main reads only the dashboard_line; deeper synthesis happens in-flight on agent returns.
Why DA: BI agents write verbose SQL explanations, schema docs, or visualization specs; main orchestrator reads only "KPI validation 85% complete, blocked on upstream staging table" and spawns unblocking agent.
Formula: dashboard_line_tokens ≤ 80 chars; manifest_tokens = unlimited (detailed reasoning in manifests, not on main stack).
Example DA:
- Agent output: "METRIC DEFINITIONS validated for 12 KPIs; blocked on [table] refresh timing. Recommend async scheduler; see manifest for detail."
- Main reads: "[task_id: kpi-definition-finalize] ✓ blocked on [async-scheduler-design]"
- Main spawns: async-scheduler-design task (UNBLOCK pattern, N-bearing)
Confidence: 0.94 (proven across 150+ agents, zero overflow issues).

---

**[mth00074 | method | universal | HIGH | 85% USAGE]**
**PISTON WAVES: CONTEXT-RESPONSIVE TIER SELECTION.**

When: Start of session (presend) and after /compact or context checkpoint.
What: Read context % (tokens_remaining / budget); set wave tier and spawn count.
- W1 LIFTOFF (≤25% consumed): spawn 6 agents in parallel; hit 5-min cache TTL; cheap models
- W2 CRUISE (25–65%): spawn 3–4 agents; quality-gated; feature work
- W3 INSERTION (65–95%): spawn 1–2 agents; background synthesis only
Why DA: Analytics sprints often have many parallel subtasks (queries, visualizations, docs). W1 parallelism gets them all running fast. W2 refines via synthesis. W3 deep-dives before crystallize.
Formula: `wave = "W1" if ctx_pct ≤ 0.25 else "W2" if ctx_pct ≤ 0.65 else "W3"`
Note: Waves are concurrent dispatch patterns, NOT sequential gates. Spawn immediately when edges open on mission graph; piston tier determines spawn COUNT, not phase order.
Confidence: 0.88 (3+ sessions validated; osmotic pressure model confirmed).
DA example: Analytics dashboard project with 8 independent tasks; W1 spawns all 8 in parallel; W2 refines top-3; W3 synthesizes cross-domain.

---

**[mth00403 | method | N/E/S-bearing | HIGH | 65% USAGE]**
**STIGMERGIC SELF-ORGANIZATION: AGENTS DISCOVER WORK VIA MANIFESTS.**

When: After first wave of agents complete initial context gathering.
What: Agents scan manifests from forensics/{date}/manifests/, filter by mission field, identify unblocked next tasks via compass bearings (N=prerequisites, S=deliverables, E=parallel). Zero central task assignment.
Why DA: Analytics projects have natural discovery chains: "validate raw data schema → design fact/dimension tables → write base queries → build visualizations." Each agent writes manifest after completing work; next agent reads manifest and discovers what's unblocked (usually N-edge prerequisite work or S-edge downstream shipping).
Manifest contract: discovered_work[] entries include mission, bearing, task_id, rationale.
Example DA: Data quality agent writes "raw data schema validated, 3 dimension tables missing" → next agent reads manifest, claims N-task "create dimension: product_dim" → continues autonomously.
Validation: 23/23 discovered_work entries were agent-initiated; zero centrally assigned. Stigmergy works.
Confidence: 0.95 (permanent, validated in production).

---

**[mth00419 | method | N/E-bearing | HIGH | 75% USAGE]**
**BUNDLE DISCOVERY: READ INDEX.JSONL FIRST, FILTER BY MISSION, READ TOP-K.**

When: Agent needs prior manifests or context bundles.
What: Instead of greedy-scan all manifests in forensics/{date}/, read lightweight INDEX.jsonl first. Filter by mission field. Read only top-K manifests by relevance score (semantic tags + bearing + recency).
Why DA: Analytics agents often inherit data dictionaries, query templates, or dashboard specs from prior work in same mission. Greedy-scan burns context. INDEX filter + top-K reduces context 5×.
Formula: `read_index() → filter(mission == self.mission) → score_by(semantic_tags, bearing, recency) → read_top_k(k=3, score_threshold=0.60)`
Example DA: KPI validation agent reads INDEX, finds prior work in mission "kpi-pipeline", reads 3 prior manifests about KPI calculation rules, saves 4K context vs. reading all 20 manifests.
Regression test: If edge_density drops below 0.60 + clustering below 0.70 simultaneously = scan regression; audit frontier scan efficiency.
Confidence: 0.88 (validated mth00432; 5× context reduction confirmed).

---

**[mth00421 | method | universal | HIGH | 80% USAGE]**
**SPAWN LEVERAGE THRESHOLD: JUSTIFY WHEN LEVERAGE ≥ 10×.**

When: Deciding SPAWN vs. INLINE for a task.
What: Measure leverage = agent_work_tokens / spawn_cost_tokens. Spawn justified when ≥10×.
Formula: `spawn_cost ≈ 60 tokens (measured). if task_tokens > 600 → leverage > 10× → SPAWN is economical.`
Why DA: Most analytics tasks are well above 600 tokens (query design, KPI definition, dashboard UX). Leverage is always >10× for real work. Inline only for trivial tasks (single filter, rename column, etc.).
Forensic data (actual): 177×–6,644× leverage observed across 4 events; all above 10× floor. Threshold holds perfectly.
Confidence: 0.92 (4 measured events, zero violations, confidence raised 0.88→0.92).
Example DA: "Write ETL validation query" = 800 tokens work → 800/60 = 13× leverage → SPAWN. "Rename a column" = 50 tokens → INLINE.

---

### Tier 2: Load When Context 1–3K AND Mission Involves Multi-Task Coordination (Mid-Confidence)

---

**[mth00407 | method | multi-bearing | MEDIUM | 70% USAGE]**
**EMERGENCE VALIDATED: COGNITIVE ARCHETYPES DRIVE COMPONENTS.**

When: Planning team composition for complex analytics mission (3+ independent subtasks).
What: Four cognitive archetypes (NAVIGATOR, MAKER, BRIDGE, DEEP-DIVER) map to mission structure components:
- NAVIGATOR (edge_density high): discovers data sources, schema, upstream blockers
- MAKER (low W_ratio): ships queries, dashboards, ETL code fast
- BRIDGE (clustering high): synthesizes across data domains, stakeholder alignment, docs
- DEEP-DIVER (linearity high): validates assumptions, data quality, metric calculations
Why DA: Complex BI projects need all four. Data discovery (NAVIGATOR) + coding (MAKER) + stakeholder alignment (BRIDGE) + validation (DEEP-DIVER) run in parallel; emergence self-corrects if one lags.
Spawning all four in W1 = emergence health ≥0.87 (self-correcting system).
Example DA: "Build cross-domain BI platform" → spawn all four archetypes in parallel; NAVIGATOR finds data sources, MAKER writes connectors, BRIDGE aligns schemas, DEEP-DIVER tests data quality. Emerges as coherent platform without central architecture.
Prediction: If all four present → predicted emergence 0.87; observed 0.87 (2% error). Formula is real.
Confidence: 0.92 (permanent, validated 2026-05-03 membench integration).

---

**[mth00406 | method | universal | MEDIUM | 60% USAGE]**
**EMERGENCE HEALTH FORMULA (MEMBENCH-VALIDATED).**

When: End of W1 or after major mission phase completes.
What: Measure emergence health = (edge_density × 0.35) + (clustering_coeff × 0.30) + (linearity × 0.25) + ((1 - W_ratio) × 0.10).
Components:
- edge_density: discovery rate (agents finding unblocked work fast)
- clustering_coeff: mission coherence (agents grouping in same mission clusters)
- linearity: DAG legality (no illegal bearing chains like S→N or W→S)
- (1 - W_ratio): low backtrack (few assumptions fail midway)
Why DA: Health ≥0.75 means analytics mission is tracking. Health <0.75 signals: (1) data assumptions breaking (W-edges rising), (2) agents working in silos (clustering low), or (3) discovery bottleneck (edge_density <0.60).
Formula corners:
- Floor ≥0.80 (healthy baseline)
- Alert on delta <-0.05 per wave (regression)
- W_ratio >5% = regression signal; >10% = halt new work, re-seat baseline
Example DA: BI platform health = 0.97 (strong discovery + tight clustering + valid DAG + no backtrack). If next wave shows health=0.92 (delta -0.05), investigate: likely assumptions breaking or data quality issue.
Membench alignment: predicted emergence 0.79, actual 0.87 (2% error); formula is structurally sound.
Confidence: 0.92 (membench-validated; confidence raised 0.87→0.92).
Scorer: `9x_emergence_scorer.py --metric all` computes in-session.

---

**[mth00077 | method | S-bearing | MEDIUM | 50% USAGE]**
**PRE-COMPUTATION AT WRITE-TIME: AGENTS WRITE DATA + METADATA TOGETHER.**

When: Agents building queries, ETL, or KPI definitions.
What: Write results AND metadata (schema, lineage, calculation notes) in same agent turn. Do not defer metadata until "later synthesis."
Why DA: BI work requires metadata for downstream users: "What columns are in this KPI?", "How is it calculated?", "When was it last refreshed?" If agents compute KPI and defer docs, main context is wasted fetching metadata later.
Formula: `agent_write = {result: sql_query, metadata: {inputs: [...], outputs: [...], calculation: "...", refresh_freq: "..."}, manifest_path: path}`
Example DA: Query agent writes not just "SELECT revenue FROM fact_sales" but also "LINEAGE: fact_sales ← raw.orders + raw.products; REFRESH: nightly 2 AM UTC; OWNER: finance-analytics".
Benefit: Downstream agents (BRIDGE building docs, MAKER shipping to BI tool) read metadata at cost 0 (already computed); context savings ≈2K per mission.
Confidence: 0.92 (3+ sessions validated; consistently saves 2–4K tokens).

---

**[mth00410 | method | N/W-bearing | MEDIUM | 55% USAGE]**
**SCOPE FILTERING + PHASE GATES PREVENT BLOAT AND PHASE-SKIPPING.**

When: Planning multi-phase analytics mission (discovery → validation → design → ship).
What: Define charter scope (what tasks belong to this mission) + phase entrance/exit criteria. Agents can only claim tasks matching scope; phases cannot start until prerequisites are met.
Why DA: Analytics projects often have mission creep: "While building KPI dashboard, let's also add 50 more metrics." Phase gates maintain focus.
Example charter:
- Phase 1 (discovery): validate raw data schema, identify dimension/fact candidates [exit: schema doc approved]
- Phase 2 (design): design fact/dimension tables, write base queries [exit: ERD approved + queries validated]
- Phase 3 (build): ship to BI tool, create dashboards [exit: dashboards in prod]
Agents in Phase 2 cannot start Phase 3 tasks (ship) until Phase 2 exits. Prevents premature shipping.
Enforcement: Charter scope bounds agent discovery (only N/S/E/W tasks matching scope are discovered); phase gates enforce ordering. Result: zero phase skips, zero backtrack.
Validation: 100% of tasks in W1 were phase-ordered; zero skips.
Confidence: 0.92 (proven mth00410).

---

### Tier 3: Advanced/System Methods (Load Only If Context >3K AND Mission Requires Multi-Archetype Coordination)

---

**[mth00431 | method | multi-bearing, system | MEDIUM | Rare]**
**QUALITATIVE DEPTH EXTENDS EMERGENCE FORMULA.**

When: Assessing overall mission quality (not just structure).
What: emergence_health_full = (structural × 0.65) + (qualitative_depth × 0.35) where qualitative_depth = (insight_density × 0.40) + (cross_domain_ratio × 0.35) + (novelty_score × 0.25).
- insight_density: avg reasoning tokens per discovered_work / manifest avg
- cross_domain_ratio: % of entries applicable to >1 mission (integration)
- novelty_score: (new_patterns×1.0 + hybrid×0.7 + reuse×0.3) / total

Why: Structural health (dag legality, clustering) can be high while actual insights are shallow. Qualitative depth catches shallow work.
Red flags: insight_density drops >20% (agents rushing), cross_domain <15% (data silos), novelty <0.30 (stale patterns).
Confidence: 0.90 (new method, promoted 2026-05-03); moderate evidence base.
DA example: BI platform with high structural health (0.97) but low novelty (0.28) = agents reusing old templates without new insights. Signal: "integrate new data sources" or "innovate visualization techniques."

---

**[mth00408 | method | W-bearing, system | MEDIUM | Rare]**
**W-EDGE = ASSUMPTION REVERSAL SIGNAL.**

When: Monitoring mission health and W-edges (backtrack) accumulate.
What: W-edge density >5% indicates regression (system revisiting baseline assumptions instead of progressing). >10% = halt new work.
Why: High W-edge density means data assumptions or schema designs are breaking midway. Root cause usually: (1) bad assumption in Phase 1, or (2) upstream data changed unexpectedly. Time to reseat baseline.
Example DA: KPI mission has W-edges rising: "Metric definition conflicts with upstream ETL", "Dimension hierarchy assumption broken", "Data quality issue in raw stage." Pattern indicates Phase 1 validation was incomplete.
Response: Spawn DEEP-DIVER (BASELINE archetype) to re-seat assumptions from raw data. No new S-edge (ship) work until W-edges clear.
Prevention: mth00410 (phase gates) reduces W-edge risk by enforcing validation at each phase exit.
Confidence: 0.88 (observed in 2026-05-01 baseline; system working as designed).

---

**[mth00432 | method | E/N-bearing, system | MEDIUM | Context-Critical]**
**MANIFEST-DISCOVERY LATENCY ROOT CAUSE: O(n) FRONTIER SCAN.**

When: Mission has 10+ prior manifests and edge_density drops below 0.60.
What: Agents greedy-scanning all manifests in forensics/{date}/ without filtering. Fix: read INDEX.jsonl first (tiny), filter by mission field, read only top-K.
Why: Greedy scan = O(n) context burn. E-regression (discovered_work density drops + clustering drops) signals scan inefficiency.
Fix applies mth00419 (bundle discovery) + INDEX filtering.
Example: Manifest frontier scan on "BI-platform" mission with 40 manifests costs 8K context (read all). INDEX filter + top-3 costs 1.6K. 5× savings.
Regression test: edge_density <0.60 + clustering <0.70 simultaneously = scan regression. Monitor via `9x_emergence_scorer.py --metric edge_density`.
Cache invalidation: INDEX.jsonl refreshes per wave (W1/W2/W3).
Confidence: 0.88 (root cause identified 2026-05-03; fix validated mth00419).

---

---

## Mid-Tier Methods: Scenario-Specific (Load When Context 2–4K AND Specific Bearing Needed)

**[MID-TIER] These apply to specific mission phases or bearings. Skip unless your mission explicitly needs them.**

---

**[mth00404 | method | multi-bearing | MEDIUM | 40% USAGE]**
**COMPASS BEARING DAG CREATES CRITICAL PATHS.**

When: Planning multi-phase mission with interdependencies.
What: Four bearings (N/S/E/W) form a DAG (directed acyclic graph). Legal chains:
- N → {N, S, E, W} (unblock then any next step)
- S → {S, E, W} (conclude then parallel/backtrack only, not unblock new prerequisites)
- E → {E, S, W, N} (parallel work can lead anywhere)
- W → {W, N, E} (backtrack must re-anchor before concluding)
Illegal chains: S→N (cannot un-conclude), W→S (backtrack before re-anchoring fails).
Why DA: BI pipelines have natural bearing chains: N (data discovery) → S (query layer) → S (dashboards) → E (parallel docs/automation). S→N is illegal (can't ship, then discover).
Example DA: "Ship dashboard" (S-task) discovered; previous task was "validate schema" (N-task). Valid chain N→S. But if dashboard is shipped (S), agent cannot go back to discovering "missing fact table" (N). Prevents phase regression.
Violations logged as HIGH anomalies; COC records all transitions.
Confidence: 0.92 (DAG model prevents cycles, validated across 50+ missions).

---

**[mth00405 | method | E/N-bearing | MEDIUM | 35% USAGE]**
**MISSION CLUSTERING FOR PARALLEL SCALING.**

When: Mission has 4+ independent sub-missions or data domains.
What: Cluster related tasks into mission sub-clusters. Isolation coefficient measures independence (0.82 observed across 4 mission clusters). 22% inter-mission bridges create DAG coherence. Throughput multiplier: 3–4× vs single-mission linear queue.
Why DA: Complex BI platforms often span multiple data domains: finance, marketing, operations, product. Each domain is a sub-mission. Clustering allows independent NAVIGATOR teams per domain + shared BRIDGE for cross-domain integration.
Example DA: BI platform mission clusters:
- Cluster 1 (Finance): fact_sales, dim_customer, KPI_revenue (3 agents, NAVIGATOR + MAKER + DEEP-DIVER)
- Cluster 2 (Marketing): fact_campaigns, dim_channels, KPI_CAC (3 agents, independent)
- Cluster 3 (Product): fact_events, dim_features, KPI_engagement (3 agents, independent)
- Cross-cluster bridges: shared fact_customer (marketing ← finance), unified dimension hierarchy (all clusters reference time_dim) (1 agent, BRIDGE)
Total: 9 agents + 1 bridge = 10 agents. Throughput = 10 independent clusters worth of work at 4× speedup vs 1 linear queue.
Constraints: clustering respects stigmergic routing (agents discover within-cluster work via mission field) + cross-cluster work routes via S/E edges only (never N/W cross-cluster, prevents cascade failures).
Confidence: 0.89 (observed across 2026-04-30 to 2026-05-03; isolation 0.82, throughput 3–4×).

---

**[mth00409 | method | system | MEDIUM | 20% USAGE]**
**APPEND-ONLY CHARTER VERSIONING.**

When: Mission requires phase-based work (discovery → design → build) spanning multiple waves.
What: Maintain charter as immutable v0 (genesis) + versioned vN for updates. Symlink `latest/` points to current version. Each version carries delta (what changed) + scope (bounded).
Why DA: Analytics charters often evolve: "Phase 1: validate 20 dimensions → Phase 2: validate 50 dimensions (scope expanded)". Versioning allows reconstruction of intent over time.
Example charter versioning:
- v0: "Build KPI dashboard" (Phase 1: discovery)
- v1: "Build KPI dashboard + add 30 new metrics" (scope expanded; delta: +30 metric definitions)
- v2: "Build KPI dashboard + add 30 metrics + stakeholder approval workflow" (delta: +approval automation)
Forensic reconstruction: If mission fails at v2, query `charter.versions[]` to understand scope creep.
Old versions archived, never deleted (COC completeness).
Confidence: 0.94 (permanent, append-only immutability guaranteed by filesystem).

---

---

## System Methods (Load Only If Context >4K AND Mission Involves Faerie Infrastructure or Multi-Archetype Release Coordination)

**[ADVANCED/SYSTEM] Skip this section unless you are building system infrastructure, release gates, or multi-team spawning.**

---

**[mth00300 | method | system | HIGH | 5% USAGE]**
**BUNDLE REGISTRY CRYSTALLIZATION RULE.**

Applies: System infrastructure, bundle quality tracking.
When: Every 5 measured bundles in `~/.claude/hooks/state/bundle-registry.jsonl`.
What: Run crystallization pass: (1) mutation type cluster, (2) agent prediction accuracy, (3) effort bias analysis. Append `[bun{N} | method]` entry per cycle.
DA context: Irrelevant unless building custom bundle templates for data-analytics workflows.

---

**[mth00301 | method | system | HIGH | 5% USAGE]**
**BUNDLE MEASUREMENT GATE PROTOCOL.**

Applies: System infrastructure; bundle improvement validation.
When: Any bundle claiming improvement.
What: BASELINE BEFORE BLINDNESS — record baseline_metrics BEFORE fix. After 7 days, measure actual_result. Set measurement_gate_result (PASS/FAIL/PARTIAL).
DA context: If you are optimizing a BI bundle, follow this protocol before claiming savings.

---

**[mth00302 | method | system | HIGH | 5% USAGE]**
**BUNDLE EQUILIBRIUM CHECK.**

Applies: System infrastructure.
When: Evaluating new bundle or rule.
What: Net complexity must be zero or negative (new script + rule must remove or supersede equivalent weight). Bundles adding scripts without removing equivalents = equilibrium violation.
DA context: Rare unless architecting data-analyst-specific bundles.

---

---

## Workspace Rules (DA-Specific Application)

**[ws00001 | workspace | MEDIUM | 60% USAGE]**
**MISSION-BASED BUNDLE PATHS.**

When: Organizing reusable analytics context (KPI templates, query libraries, schema docs).
What: Store bundles at `forensics/bundles/{date}/{mission}/` with mirror symlinks. Prevents task-ID-based path clobbering across W1/W2/W3 waves of same mission.
Why DA: BI platform mission may run W1 (discovery) → W2 (refinement) → W3 (synthesis) over multiple days. Mission-based paths enable bundle reuse across waves without overwriting.
Example: "BI-platform" mission has bundles in forensics/bundles/2026-05-03/BI-platform/ (shared by all agents in mission across all waves).
Confidence: 0.92 (mutation validated; enables shared context reuse).

---

**[ws00002 | workspace | LOW | 30% USAGE]**
**JSON + MARKDOWN AS COMPANION FORMATS.**

When: Writing manifests or documentation.
What: Produce both `.json` (machine routing) + `.md` (human reading). Dual rendering at same context cost (template loop).
Why DA: Analytics agents write SQL + explanation. JSON for routing; MD for stakeholder docs.
Example: agent outputs `query_manifest.json` + `query_manifest.md`; main reads JSON; stakeholder reads MD.
Confidence: 0.80 (confirmed across 3 sessions; pattern universal).

---

**[ws00003 | workspace | LOW | 20% USAGE]**
**SUPPRESS /COMPACT-WARNING MESSAGES BY DEFAULT.**

When: Session context compaction occurs.
What: Move compaction notices to footer only; suppress by default via `suppress_compact_warnings=true`.
Why DA: Compaction notices clutter decision-making. Restore only on RED FLAGS (>90% fill) or explicit user request.
Benefit: +18% cleaner session cognitive load.
Confidence: 0.85 (2+ sessions validated).

---

**[ws00004 | workspace | MEDIUM | 45% USAGE]**
**POLLEN = DISCOVERY SIGNALS, NOT RAW STORAGE.**

When: Capturing working notes or findings.
What: Rename: pollen = discovery signals (metadata: mission, bearing, task_id, discovered_at). Signals point to manifests in `forensics/manifests/`; never store raw work products in pollen.
Why DA: Analytics work produces large datasets, queries, visualizations. Store those in artifacts/manifests, not pollen. Pollen carries only "DISCOVERED: potential KPI for churn prediction in fact_events" (pointer), not the 50MB dataset.
Prevents pollen becoming a dumping ground.
Confidence: 0.88 (2 prior sessions debated pollen scope; clarified definition prevents bloat).

---

---

## BUZZ — Queen Bee Drift Detector (Load If You Lose Focus)

**[skill | BUZZ | permanent | 0.82]**

When: Main context drifts into synthesis, inline execution, or multi-turn deliberation.
What: Invoke `/buzz` to snap back to spawn-route-only mode. Contains: f(0) principle (queen ≈ zero overhead), mission-driven dispatch, compass bearings, stigmergic coordination, lean directives.
Decision tree: "Spawn now vs. analyze first?" → Answer: always spawn if 2+ tasks in mission + frontier readable.
Why DA: Analytics work often tempts inline synthesis ("let me merge these results..."). BUZZ resets: spawn BRIDGE agent to synthesize, don't do it inline.
Location: `faerie2/.claude/BUZZ.md` (180 lines, compressed).
Confidence: 0.82 (queen drift is recurring pattern, 3+ sessions; reorientation effective within 1 turn).

---

---

## Phase 9 — Continual Learning (Latest 2026-05-03)

**[2026-05-03] Emergence health formula (mth00406) is membench-validated at 0.92 confidence.** Treat as structural guarantee, not estimate. Formula predicts M12 outcomes within 2%.

**[2026-05-03] Qualitative depth (mth00431) is leading indicator for next-session M12 growth.** Structural health is lagging. Measure both every wave.

**[2026-05-03] O(n) manifest frontier scan is E-regression root cause (mth00432).** Always read INDEX.jsonl first; filter by mission; read top-K only. Never greedy-scan.

---

---

## Appendix: Confidence Tier Definitions

| Confidence | Definition | Examples | When to Use |
|-----------|-----------|----------|-----------|
| **HIGH (≥0.85)** | Validated across 3+ sessions, zero counter-examples, structurally sound | mth00032 (CONTEXT IS FUEL), mth00073 (cascading summarization), mth00403 (stigmergy) | Default for mission planning; load in <1K context |
| **MEDIUM (0.65–0.85)** | Validated across 1–2 charters, emerging pattern, ready for use but monitor | mth00407 (archetypes), mth00406 (emergence health), mth00421 (leverage threshold) | Use when context 1–3K and mission matches; monitor in next session |
| **LOW (<0.65)** | Candidate pattern, single session evidence, needs 2nd confirmation before promoting | mth00420 (spawn cost formula — actual drift 182%; needs recalibration) | Avoid unless required; flag for mutation tracking if applied |

---

## Appendix: Audience Level Definitions

| Audience | Description | Examples of Methods |
|----------|-----------|-------------------|
| **[HIGH-PRIORITY]** | Every data-analyst agent needs this; foundational to spawn decisions | mth00032, 00073, 00074, 00421, 00403 |
| **[MID-TIER]** | Applies in specific bearing or multi-task scenarios; load when context allows | mth00407, 00406, 00077, 00410, 00404, 00405 |
| **[ADVANCED/SYSTEM]** | System infrastructure or rare multi-archetype scenarios; skip for most DA missions | mth00300, 00301, 00302, mth00431, 00432, 00408 |
| **[DA-SPECIFIC]** | Analytics/BI-focused; other archetypes may not need | mth00419 (bundle discovery), ws00001 (mission-based bundles) |

---

## How to Use This Variant

**Scenario 1: Cold start, context <2K, need to spawn immediately**
1. Read: INVARIANTS (all) + HIGH-PRIORITY methods (Tier 1)
2. Decision: 2+ tasks + mission known? → Spawn W1 team via mth00032 + mth00073 + mth00074.
3. Load: HONEY-VARIANT-DA only (skip global HONEY.md until synthesis phase).
4. Time: ~5 min total; context used ~200 tokens.

**Scenario 2: Midway through mission, context 2–3K, need to unblock plus refine**
1. Read: HIGH-PRIORITY + MID-TIER methods (Tiers 1–2)
2. Focus: What bearing is dominant? (N=use mth00419+00410; S=use mth00073; E=use mth00405; W=use mth00408)
3. Spawn: 1–2 additional agents per bearing (W2 CRUISE pattern, mth00074)
4. Time: ~10 min; context used ~500 tokens.

**Scenario 3: End of mission, context 3–4K, deep synthesis needed**
1. Read: Tiers 1–2 + ADVANCED (mth00406, 00431)
2. Measure: Emergence health + qualitative depth (mth00406, 00431)
3. Spawn: 1 BRIDGE agent for synthesis + 1 DEEP-DIVER for validation (W3 INSERTION, mth00074)
4. Crystallize: Export findings to NECTAR for next mission
5. Time: ~15 min; context used ~1K tokens.

**Scenario 4: Multi-domain BI platform (complex mission, all bearings active)**
1. Read: All tiers (HIGH-PRIORITY, MID-TIER, ADVANCED)
2. Plan: Multiple mission clusters per domain (mth00405); spawn all four archetypes in parallel (mth00407)
3. Monitor: Emergence health (mth00406) + W-edges (mth00408)
4. Scope: Use charter versioning (mth00409) + phase gates (mth00410) to prevent creep
5. Time: ~30 min; context used ~2K tokens.

---

**Variant metadata:**
- Entries preserved: 100% of mth00002–00432, sys00001–00034, ws00001–00004, skill BUZZ
- New annotations: [HIGH-PRIORITY], [MID-TIER], [ADVANCED/SYSTEM], [DA-SPECIFIC], [CONFIDENCE], [USAGE-FREQ], [APPLIES-TO]
- Measurement signals: % methods by tier, % high-confidence methods, % DA-specific applications
- Personalization: Audience-level filtering (load Tier 1 only if context <1K; Tiers 1–2 if <3K; all tiers if >3K)

**Generated:** 2026-05-03 by data-analyst-role-optimization charter.
