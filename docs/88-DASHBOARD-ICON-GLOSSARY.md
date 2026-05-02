# Dashboard Icon Glossary — Semantic Compression Layer

**Purpose:** Compress system state, work type, and health metrics into icons (<2 chars per component). Used across dashboard_lines, statusline, membench metrics, and agent bundles.

**Principle:** Emoji are memory anchors. Icon → glossary lookup → metric → data. Stickier than numbers.

---

## System Components (Health States)

Each component can be in one of 4 health states. Icon + suffix = component status.

### 🧠 Memory (HONEY/NECTAR)

**What it measures:** Knowledge retention, NECTAR hit-rate, observation→pollen→HIGH promotion flow.

**Health states:**
- `🧠✓` — NECTAR hit-rate >60%, pollen observations flowing, HIGH promotions happening
- `🧠⚠️` — Hit-rate 30-60%, some promotion stalls, NECTAR growing but not read
- `🧠💤` — Hit-rate <30%, observations piling up without promotion
- `🧠❌` — Memory corrupted (duplicate entries, citation backlinks missing)

**Membench dimension:** B (Memory)
**Key metric:** `NECTAR_hit_rate` + `pollen_observation_count` + `promotion_latency`
**See also:** membench/MEMBENCH-PUBLIC-RUBRIC.md § Memory Dimension

---

### 🔄 Piston (Wave Orchestration)

**What it measures:** Agent dispatch rhythm, W1/W2/W3 burn rate, spawn latency, inter-agent coordination.

**Health states:**
- `🔄⚡` — W1 LIFTOFF active, agents spawning in parallel, high burn rate
- `🔄🔥` — W2+ running, sequential dispatches, cooling down
- `🔄💤` — W3 or idle, no new spawns, waiting for queue claims
- `🔄❌` — Piston stalled (queue backlog, spawn failures)

**Membench dimension:** E (Piston Orchestration)
**Key metric:** `agents_in_flight` + `spawn_latency_p50` + `wave_burn_rate` + `interagent_coordination_score`
**See also:** membench/MEMBENCH-PUBLIC-RUBRIC.md § Piston Dimension

---

### 🗂️ Forensics (COC Integrity)

**What it measures:** Artifact naming compliance, COC chain completeness, manifest integrity, recovery readiness.

**Health states:**
- `🗂️✓` — All artifacts named correctly, COC chain complete, manifests hashable
- `🗂️⚠️` — Minor naming gaps (<5% violations), COC chain mostly valid
- `🗂️🔥` — Forensics hot (rapid artifact generation, risk of clobbering)
- `🗂️❌` — COC chain broken, orphaned artifacts, recovery impossible

**Membench dimension:** Forensic Integrity (G submetric)
**Key metric:** `artifact_naming_compliance` + `coc_chain_completeness` + `recovery_success_rate`
**See also:** forensics/FORENSIC-INTEGRITY.md + membench/MEMBENCH-PUBLIC-RUBRIC.md § Completeness

---

### ⛓️ Spawn Contract (Enforcement)

**What it measures:** TEMPLATE-SIGNED validation, scout-protocol injection, bundle immutability, enforcer mode.

**Health states:**
- `⛓️✓` — Contract enforced (BLOCK mode), all spawns signed, scouts routed correctly
- `⛓️⚠️` — Contract in WARN mode, violations logged, not blocking
- `⛓️💤` — Enforcer inactive (permissive mode during debug)
- `⛓️❌` — Contract violations found (unsigned spawns, bad scout injection)

**Membench dimension:** F (Model Routing) + Forensic Integrity
**Key metric:** `spawn_contract_violations_count` + `enforcer_mode` + `template_signature_validity`
**See also:** hooks/8x_spawn_contract_enforcer.py + docs/SPAWN-CARD-PROTOCOL.md

---

### 🧭 Compass (Navigation Graph)

**What it measures:** Task dependency graph (N/S/E/W edges), dangling references, cold threads, mutation boundaries.

**Health states:**
- `🧭✓` — Compass edges valid, no orphans, agents can self-navigate, mission braiding working
- `🧭⚠️` — Some dangling edges, cold threads detected (in_progress >24h), resurrectable
- `🧭🔥` — Many contradictions (West edges), unresolved tensions, mutation opportunities
- `🧭❌` — Compass broken (cycles, dead ends), agents lost, no navigation

**Membench dimension:** Emergence (mutation testing dimension)
**Key metric:** `dangling_edges_count` + `cold_threads_5day` + `compass_traversability_score` + `contradiction_count`
**See also:** docs/IDEA-COMPASS-ARCHITECTURE.md + mutation/mutation-baseline.json

---

### 🎯 Queue (Tasks & Missions)

**What it measures:** Pending task count, critical path blockage, mission claim rate, task staleness.

**Health states:**
- `🎯✓` — Queue <10 items, critical path clear, mission claim rate >50%
- `🎯⚠️` — Queue 10-30 items, some blockers, claim rate 20-50%
- `🎯🔥` — Queue >30 items, hot (critical path active), high burn
- `🎯💤` — Queue empty or stalled, no claims, waiting for human queue add

**Membench dimension:** A (Throughput)
**Key metric:** `queue_length` + `critical_path_blockage` + `mission_claim_rate` + `task_staleness_p99`
**See also:** scripts/7x_queue_ops.py + docs/QUEUE-DEPRECATION-NOTICE.md (Compass edges replace linear queue)

---

### 🤖 Agents (Return Rate & Reliability)

**What it measures:** Agent spawn count, return rate, avg completion time, failure rate, reputation drift.

**Health states:**
- `🤖✓` — Return rate >80%, low failure, reputation stable/improving
- `🤖⚠️` — Return rate 50-80%, some failures, reputation oscillating
- `🤖💤` — Return rate <50%, slow agents, waiting for work
- `🤖❌` — Agent failures, timeouts, negative reputation drift

**Membench dimension:** C (Resilience) + A (Throughput)
**Key metric:** `agent_return_rate` + `agent_completion_time_p50` + `agent_failure_rate` + `reputation_drift_per_agent`
**See also:** scripts/7x_queue_ops.py + ~/.claude/agents/*.md (Last Training scores)

---

### 🧬 Mutation (Adaptive Changes)

**What it measures:** Rate of system changes (new scripts, hooks, bundle enrichment), cost/benefit ratio, stability impact.

**Health states:**
- `🧬✓` — Mutation beneficial (metrics improved post-change), cost <10%, stability maintained
- `🧬⚠️` — Mutation risky (mixed signals, >10% cost), baseline underway
- `🧬🔥` — High mutation rate (many changes in flight), experiment phase
- `🧬💤` — No mutations (stable, all baselines measured), production lockdown

**Membench dimension:** Mutation Testing (full dimension)
**Key metric:** `mutation_rate` + `change_cost_ratio` + `stability_impact` + `beneficial_vs_harmful_ratio`
**See also:** mutation/mutation-baseline.json + docs/EMERGENCE-AND-MUTATION-GLOSSARY.md

---

### ⚡ Context Efficiency (Tokens-Per-Finding)

**What it measures:** Token consumption relative to real findings, memory overhead, bundle size, model routing optimality.

**Health states:**
- `⚡✓` — <100 tokens per finding, bundle compression working, routing optimal
- `⚡⚠️` — 100-200 tokens per finding, some overhead, check memory churn
- `⚡🔥` — >200 tokens per finding, bloated bundles, context drift happening
- `⚡💤` — No findings recorded (query phase only), efficiency unmeasurable

**Membench dimension:** A (Throughput) + Memory (efficiency submetric)
**Key metric:** `tokens_per_finding_median` + `tokens_per_finding_p95` + `bundle_size_bytes` + `model_routing_optimality`
**See also:** membench/MEMBENCH-PUBLIC-RUBRIC.md § Throughput + scripts/9x_session_metrics.py

---

## Work Type Icons (What agent is doing)

Prefix the health state to indicate work category.

| Icon | Work Type | Example |
|------|-----------|---------|
| `🔧` | Infrastructure / System changes | `🔧✓ Spawn contract wired` |
| `📊` | Analysis / Metrics / Eval | `📊⚡ Membench run (42 tok/finding)` |
| `🔍` | Investigation / Discovery | `🔍✓ Cold threads identified` |
| `💾` | Storage / Forensics / Archival | `💾✓ Eval archival wired` |
| `🚀` | Deployment / Activation | `🚀⚡ Bundle enrichment deployed` |
| `🧠` | Memory / Learning / Training | `🧠⚠️ NECTAR promotion stalling` |
| `📝` | Documentation / Guides | `📝✓ Icon glossary created` |
| `🎯` | Queue / Task claiming | `🎯🔥 Mission claiming (50% rate)` |

---

## Status Suffixes (Outcome)

Append to component or work-type icon.

| Suffix | Meaning | Context |
|--------|---------|---------|
| `✓` | Success / Healthy / Optimal | Used for all components in good state |
| `⚠️` | Warning / Degraded / Watch | Needs attention but not failure |
| `🔥` | Hot / Critical / High-activity | Could mean good (agents busy) or bad (overload) — context matters |
| `💤` | Idle / Stalled / Waiting | No activity, waiting for input |
| `❌` | Failure / Violation / Broken | Unrecoverable error, action needed |

---

## Trend Indicators (Direction of Change)

Append to status suffix to show trajectory.

| Arrow | Meaning | Example | Interpretation |
|-------|---------|---------|---|
| `↑` | Improving | `🧠✓↑` | Memory healthy AND getting better (hit-rate rising) |
| `↓` | Degrading | `⚡42↓` | Efficiency cost increasing (tokens-per-finding climbing) |
| `↔` | Flat / Stable | `🧬8%↔` | Mutation cost unchanged (stable phase) |
| `~` | Oscillating | `🤖~` | Agent return rate bouncing (unstable, watch variance) |

**Baseline reference (in parentheses) — choose based on feedback loop:**

| Baseline | Window | Use when | Example |
|----------|--------|----------|---------|
| `(vs T-1)` | 1 manifest (~3-5 min) | Real-time adjustment visible? | Changed spawn behavior; want immediate ↑/↓ signal |
| `(vs T-3)` | 3 manifests (~10-15 min) | In-session tuning feedback | Reduced bundle bloat; want to see efficiency ↑ before session end |
| `(vs session)` | From session start (~1 hour+) | Drift detection within session | Are we accumulating context/token debt this session? |
| `(vs genesis)` | T=0 baseline (2026-04-23) | Long-term trajectory | Is system fundamentally better/worse than launch? |
| `(vs w/avg)` | 7-day rolling mean | Noise filtering | Is this a real trend or normal variance? |

**Rules:**
- **Real-time behaviors** (spawn rate, bundle size, agent return rate) → compare vs T-1 or T-3
- **In-session tuning** (efficiency tweaks, queue claim changes) → compare vs session start
- **Acceptance/anomaly detection** → compare vs w/avg (filter out daily noise)
- **Long-term health** → compare vs genesis (trajectory matters more than T-1 noise)

**Examples with realistic baselines:**

### Real-time adjustment (manifests 5 min apart):
```
⚡42↓ 🔧✓ Reduced bundle NECTAR to 5 lines (vs T-1)
└─ Efficiency improved: tokens-per-finding was 78, now 62
└─ Real-time feedback: can see 16-token gain in 5 minutes
```
→ You reduced NECTAR bloat. T-1 baseline shows immediate impact. Keep or revert?

### In-session tuning (since session start):
```
🧠✓↑ 🎯✓↑ (vs session) Mission claiming: 8→12 (vs session start 30m ago)
└─ Memory hit-rate stabilized, queue claim rate doubled in 30 min
```
→ Your queue shaping worked within a session window you can act on.

### Anomaly detection (vs week average):
```
🔄💤↓ (vs w/avg) Spawn latency: 0.8s vs 2.1s avg (unusual)
└─ Agents spawning 2.6x faster than normal — investigate
```
→ Deviation from w/avg highlights anomalies without daily noise.

### Strategic (long-term):
```
🤖85%↑ 🧬✓↑ (vs genesis) Agent return rate: 62%→85%, mutation cost stable (vs T=0)
└─ Agent reliability fundamentally improved since 2026-04-23 baseline
```
→ Genesis baseline shows this is real improvement, not just good luck this week.
```

---

## Dashboard Line Format

**General structure:**
```
{system_health_icons_with_trends} {work_type} {description} (baseline) [{hidden_force_metrics}]
```

**Icon syntax:**
- Component health: `{icon}{status}{trend}` → e.g., `🧠✓↑` (healthy, improving)
- Hidden force: `{icon}{value}{unit}` → e.g., `⚡42` (42 tokens-per-finding)

**Complete Examples (with real numbers):**

### Clean success with improvement:
```
🧠✓↑ 🔄⚡↑ ⛓️✓↔ 🔧✓ Phase-1c: consolidated (vs T-1) [⚡42 🤖7]
└─ Memory hit-rate improving
    └─ Piston agents rising (7 in flight, hottest yet)
         └─ Contract stable, work succeeded
              └─ Efficiency at 42 tokens/finding (good baseline)
```

### Degraded state with hidden forces:
```
🧠⚠️↓ 🔄💤↔ 🧭⚠️↑ 📊 Membench run (vs w/avg) [⚡156↑ 🧠23%↓ ❄️5]
└─ Memory hit-rate 23% (was 45% week avg) — degrading
    └─ Piston idle (no agents), cost stable
         └─ Compass issues rising (new contradictions), cold threads found
              └─ Efficiency bloated: 156 tokens/finding (worse than baseline)
                   └─ 5 tasks stalled >24h — braiding opportunity
```

### Hot phase with full metrics:
```
🧬🔥↑ 🤖⚠️↓ 🧠💤↔ 🚀⚡ W1: 8 agents parallel (vs session) [❌12% ⏱️3.2s 🧬8%]
└─ Mutation rate hot & climbing (experiment phase)
    └─ Agent reliability 85%→73% (declining, watch failures)
         └─ Memory not promoting (pollen building up)
              └─ Deployment hot, spawn issues emerging
                   └─ Failure rate: 12% (up from 8%), latency 3.2s (was 0.8s), mutation overhead 8%
```

**Metric value placement:** Hidden forces appear in square brackets as suffix. Always include unit (%, s, K, none) for clarity.

---

## Hidden Forces Metrics (Emergent Properties)

**Format:** `{icon}{numeric_value}{unit}` — emoji as memory anchor, number for precision.

These are "invisible" system properties revealed by membench + mutation tests. Surface them as metric suffix in dashboard_line.

| Hidden Force | Icon + Format | Example | What it means | See |
|--------------|----------------|---------|---|-----|
| Token efficiency | `⚡{N}` | `⚡42` | 42 tokens-per-finding | membench/A |
| Agent coalescence | `🤖{N}` | `🤖3` | 3 agents solving same problem | mutation/coalescence |
| Context drift | `📏{N}K` | `📏156K` | 156K tokens accumulated | membench/memory |
| Memory hit-rate | `🧠{%}` | `🧠23%` | 23% NECTAR read (low = poisoning) | membench/B |
| Spawn latency | `⏱️{N}s` | `⏱️2.3s` | 2.3s median spawn→return | membench/C |
| Cold threads | `❄️{N}` | `❄️5` | 5 in_progress >24h tasks | compass |
| Failure rate | `❌{%}` | `❌12%` | 12% agent failure rate | membench/C |
| Mutation cost | `🧬{%}` | `🧬8%` | 8% overhead from changes | mutation-baseline |

---

## Membench Crosswalk (Icon → Metric → Dimension)

| Icon | Metric | Dimension | Link |
|------|--------|-----------|------|
| `🧠` | NECTAR_hit_rate, pollen_count | B (Memory) | membench/MEMBENCH-PUBLIC-RUBRIC.md§B |
| `🔄` | agents_in_flight, spawn_latency | E (Piston) | membench/MEMBENCH-PUBLIC-RUBRIC.md§E |
| `🗂️` | artifact_naming_compliance, coc_completeness | G (Completeness) | membench/MEMBENCH-PUBLIC-RUBRIC.md§G |
| `⛓️` | spawn_violations, enforcer_mode | F (Model Routing) | membench/MEMBENCH-PUBLIC-RUBRIC.md§F |
| `🧭` | dangling_edges, compass_traversability | Mutation (Emergence) | mutation/mutation-baseline.json |
| `🎯` | queue_length, task_claim_rate | A (Throughput) | membench/MEMBENCH-PUBLIC-RUBRIC.md§A |
| `🤖` | agent_return_rate, failure_rate | C (Resilience) | membench/MEMBENCH-PUBLIC-RUBRIC.md§C |
| `🧬` | mutation_rate, change_cost | Mutation (Full) | mutation/mutation-baseline.json |
| `⚡` | tokens_per_finding | A (Throughput) + Memory efficiency | membench/MEMBENCH-PUBLIC-RUBRIC.md§A |

---

## Implementation Notes

**For agents writing manifests:**
- `icon_class` field (optional): `"infrastructure"`, `"analysis"`, `"investigation"`, etc.
- `system_health` field (optional): map of component → state, e.g., `{"memory": "warning", "piston": "hot"}`
- Template enricher will format dashboard_line with icons

**For statusline (9x_lean_query.py):**
- Display hidden force metrics with icons: `🧠23 🔄⚡ ⚡42 🧬8% 🤖85%`
- Update every manifest or every session (config TBD)

**For human operators:**
- Scan dashboard_line left-to-right: system health → work type → status → description
- Unknown icon? Grep this glossary
- Want detail? Follow the icon to membench dimension

**For bundle injection:**
- Bundle includes this glossary as `bundle.icon_glossary`
- Agents can reference icons in observations: "🧠⚠️ NECTAR hit-rate low, promoting more observations"

---

**Version:** 1.0 (2026-04-26)  
**Replaces:** None (new)  
**Cross-repo:** See `membench/docs/ICON-METRICS-CROSSWALK.md` for membench dimension mapping
