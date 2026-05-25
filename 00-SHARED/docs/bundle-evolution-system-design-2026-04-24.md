# Bundle Evolution System — Mutation-as-Fitness Framework

**Sourced from:** Global HONEY.md (mth00075, mth00077, sys00030-34), faerie2/.claude/HONEY.md (spawn contract), NECTAR.md tail-30 (membench + emergence), audit reports (membench baselines), implementation summary 2026-04-22.

**Status:** Design document. Framework ready for implementation phase.

**Document version:** 1.0 | **Date:** 2026-04-24 | **Classification:** Architecture + Measurement

---

## Table of Contents

1. [Context](#context) — Why bundles matter to f(0)
2. [Problem Statement](#problem-statement) — Bundle size tradeoff
3. [Framework Definition](#framework-definition) — Mutation formulas + evolution loop
4. [Implementation Architecture](#implementation-architecture) — Bundle routing & feedback
5. [Emergence Classification](#emergence-classification) — What counts as beneficial
6. [Measurement Framework](#measurement-framework) — Metrics + baselines
7. [CLI Commands](#cli-commands) — Operator interface
8. [Appendices](#appendices) — Full JSON, citations, examples

---

## Context

### Why Bundles Exist

Per **sys00030** (HONEY.md:L177), the north star is **f(0) — orchestration burden on main ≈ 0**. This means:

> "the ultimate goal is f(0) ie ORCHESTRATION IS SO LIGHT THAT NUMBER OF AGENTS SPAWNED AND RETURNED IS NOT CONSTRAINED BY MAIN."

Bundles are the mechanism. A **bundle** = crystallized context passed to an agent at spawn time, enabling:
1. **No context leakage** — agent-specific facts don't pollute main's working set
2. **Parallel agent scaling** — N agents with N bundles ≠ N⁻¹ context growth
3. **Deterministic routing** — different bundle → different agent behavior → measurable mutation

### Current Bundle Landscape

**Global HONEY.md size:** 10.7K tokens (as of 2026-04-24 crystallization). **Budget ceiling:** ≤5K tokens per HONEY.md (sys00002, core.md).

**Measured from:** `~/.claude/HONEY.md` (191 lines post-crystallization) + inclusion of full 191 lines = ~10.7K tokens.

**Problem:** HONEY has exceeded budget 2.14×, yet it is **inviolable** per sys00027:

> "Never trim `~/.claude/CLAUDE.md` or project-level `CLAUDE.md` even when budget tools flag it over-budget. Platform weights it highest in generation."

**Consequence:** HONEY can't be compressed. It CAN be **split** into conservative vs experimental bundles, letting agents route dynamically.

### Membench Baselines (v0.2.0)

From **MEMBENCH-INDEX.md** (sourced 2026-04-21):

| Metric | Baseline | Meaning |
|--------|----------|---------|
| **M1 Retention** | 88% | 88 of 100 facts findable |
| **M2 Relevance** | 84% | 84% of HONEY is procedural |
| **M3 Efficiency** | 1.31× | 31% more effective work WITH memory |
| **M4 Overhead** | 2.8% | Memory costs 2.8% of context per turn |
| **M5 Continuity** | 100% | Perfect checkpoint recovery |
| **Composite** | 78.4 | Healthy baseline |

**Critical insight (M3):** Memory overhead is WORTH IT. Every 100 agents spawned WITH memory complete ~115 effective tasks; without memory, ~100 effective tasks. **11× ROI on memory overhead.**

### Mutation Baseline T=0 (2026-04-23)

From **HONEY.md mth00075** (mutation-as-measurement discipline):

```json
{
  "baseline_date": "2026-04-23",
  "mutation_detection_rate": 4.66,
  "classification": {
    "beneficial": 36,
    "neutral": 18,
    "harmful": 36,
    "uncertain": 9
  },
  "shadow_rate": 0.10,
  "preservation_rate_target": "measured_t1_against_t0",
  "soft_gates": {
    "substrate_warn": "harmful > 15%",
    "citation_drift": "SR ≥ 10%"
  }
}
```

**Key constraint:** Preserve T=0 baseline BEFORE repair. "If we fix harmful mutations without T+1 PR baseline wired, we destroy the ability to distinguish beneficial-mutations-we-clobbered from harmful-mutations-we-fixed."

---

## Problem Statement

### The Tradeoff

1. **Conservative bundle** (current global HONEY): Full 10.7K tokens
   - **Pros:** Complete knowledge; agents never lack context
   - **Cons:** Exceeds budget 2.14×; creates orchestration debt
   - **Measured:** M1=88%, M2=84%, overhead 2.8%

2. **Experimental bundle** (subset, high-innovation rules):
   - **Hypothesized:** Smaller token footprint + higher mutation concentration
   - **Unknown:** Will it improve M3 (efficiency) or degrade M1 (retention)?
   - **Risk:** Agents lose context; make errors; conservation rate drops

3. **Hybrid routing** (conditional dispatch):
   - **Hypothesized:** Route conservative-bundle → legacy/production tasks; experimental → exploratory tasks
   - **Unknown:** Routing decision heuristics; measurement infrastructure

### Why This Matters

**From HONEY.md sys00032** (artifacts-in-forensics):

> "User directive 2026-04-23: 'all produced artifacts must live outside the claude folder, likely in forensics as if its an artifact, its forensically logged.' Every produced artifact...lives in `{repo}/forensics/{type}/{YYYY-MM-DD}/`."

Bundles aren't artifacts — they're coordination state. BUT **mutation as measurement** (mth00075) requires bundles to be **versioned** and **tracked**. Each mutation is a **bundle variant**. Measurement requires:

- Archive T=0 baseline bundles
- For each mutation, version the bundle
- Track which agents received which bundle variant
- Compare agent outcomes (same task, different bundle)
- Measure M1/M3 delta attributable to bundle choice

**Without bundle versioning, mutation-as-measurement is impossible.**

---

## Framework Definition

### Design Rationale

Per **sys00034** (programmatic composition):

> "Claude should not be composing anything a script could render deterministically...Assembly (bundle, format, pick from list) is drag — templatize it."

Bundle evolution should be **programmatic, not inferential:**
1. Bundle formula = JSON schema (not prose)
2. Bundle variants = script-rendered (not hand-edited)
3. Mutation routing = config-driven (not agent-judged)
4. Measurement = automated (not manual scoring)

### Conservative Formula (v1.0)

**Source:** Global HONEY.md + faerie2/.claude/HONEY.md (spawn contract prefs).

**Design:** Full-featured, zero innovation. Includes all principles, proven methods, established constraints.

```json
{
  "bundle_name": "conservative-v1.0",
  "created": "2026-04-23T00:00:00Z",
  "status": "baseline",
  "size_tokens": 10700,
  "philosophy": "complete knowledge, minimize experimental rules",
  "sections": [
    {
      "name": "principles",
      "source": "HONEY.md sys00001–sys00029",
      "rules": [
        "ONE_PATH_ONE_TRUTH",
        "BUDGET_IS_HEARTBEAT",
        "LIFTOFF_PARADOX",
        "COORDINATOR_NOT_EXECUTOR",
        "IMPLICIT_VALIDATION_VIA_STIGMERGY"
      ],
      "token_budget": 2100,
      "mutability": "locked"
    },
    {
      "name": "methods",
      "source": "HONEY.md mth00002–mth00074",
      "categories": {
        "investigation": ["mth00002", "mth00004", "mth00010"],
        "operational": ["mth00015", "mth00043", "mth00044"],
        "memory": ["mth00062", "mth00072"],
        "forensics": ["mth00070", "mth00071"],
        "spawn_contract": ["mth00077"]
      },
      "token_budget": 6200,
      "mutability": "locked"
    },
    {
      "name": "preferences",
      "source": "HONEY.md pref00001–pref00024",
      "policy": [
        "AGENT_DISPATCH_ROUTING (Haiku default)",
        "BATCH_HUMAN_QUESTIONS",
        "MANIFEST_AS_RETURN_VALUE"
      ],
      "token_budget": 1400,
      "mutability": "locked"
    },
    {
      "name": "f0_crystallization",
      "source": "HONEY.md sys00030–sys00034 + mth00073–mth00082",
      "principles": [
        "F(0) — orchestration burden ≈ 0",
        "STIGMERGY_ONLY",
        "ARTIFACTS_IN_FORENSICS",
        "TASK_ID_UNIVERSAL_JOIN",
        "PROGRAMMATIC_COMPOSITION",
        "CASCADING_SUMMARIZATION",
        "ROCKET_PHYSICS + STATE_FLOWS",
        "DETERMINISTIC_OPS_CALL_CLI"
      ],
      "token_budget": 1000,
      "mutability": "locked"
    }
  ],
  "experimental_rules_included": false,
  "mutation_vector": "none",
  "target_agents": [
    "evidence-curator (tiering, validation)",
    "report-writer (publication, synthesis)",
    "data-engineer (ingest, normalization)"
  ],
  "membench_projection": {
    "m1_retention": 0.88,
    "m2_relevance": 0.84,
    "m3_efficiency": 1.31,
    "m4_overhead": 0.028,
    "composite": 78.4
  }
}
```

### Experimental Formula (v1.0)

**Source:** Emerged from recent mutations + emerging capability signals (NECTAR 2026-04-22 + 2026-04-23 entries).

**Design:** Selective high-mutation rules; targets exploratory agents; hypothesizes faster learning at cost of occasional error.

```json
{
  "bundle_name": "experimental-v1.0",
  "created": "2026-04-23T00:00:00Z",
  "status": "hypothesis",
  "size_tokens": 4200,
  "philosophy": "minimize context, maximize emergence opportunity; selected mutation concentration",
  "sections": [
    {
      "name": "core_principles",
      "source": "HONEY.md sys00030–sys00031 (f(0) + stigmergy only)",
      "rules": ["ONE_PATH_ONE_TRUTH", "F(0)_ORCHESTRATION", "STIGMERGY_ONLY"],
      "token_budget": 1200,
      "mutability": "locked"
    },
    {
      "name": "high_mutation_methods",
      "source": "NECTAR.md entries 2026-04-22 (Phase 3 autotune) + recent HIGH discoveries",
      "categories": {
        "curiosity_framework": ["Cross-session discovering via NECTAR pull", "Sibling discoveries injected at spawn", "Eval wins promoted to boilerplate"],
        "implicit_validation": ["Next-agent's work IS validation", "Hash-chain auto-proof"],
        "stigmergic_learning": ["Droplet-driven cross-pollination", "Upstream pattern discovery"]
      },
      "token_budget": 1800,
      "mutability": "variable (tuned per wave)",
      "experimental_citations": [
        "NECTAR.md line 24 (HC-05 Curiosity Framework)",
        "NECTAR.md line 65 (Piston Wave Teams Pattern)",
        "NECTAR.md line 37 (Task #40 Cross-Session Learning Verified)"
      ]
    },
    {
      "name": "omitted_sections",
      "what_is_not_included": [
        "Full pref* list (kept only dispatch + model routing)",
        "Historical investigation-specific methods (mth00038–mth00068 trimmed to essentials)",
        "COC mechanics detail (compressed to 'append COC entry' summary)",
        "Forensics depth (reference only)"
      ],
      "token_budget_saved": 6500,
      "trade_off": "Agents must reason from first principles on topics not covered; mutation concentration increases"
    }
  ],
  "experimental_rules_included": true,
  "mutation_vectors": [
    {
      "name": "curiosity_pull_vs_push",
      "hypothesis": "Agents actively reading NECTAR (pull) > agents waiting for summaries (push)",
      "measurement": "M6 Coordination (% findings cited by later agents)",
      "baseline_m6": 0.34,
      "target_m6": 0.60
    },
    {
      "name": "droplet_discovery_bootstrap",
      "hypothesis": "Task droplet discovery at startup increases stigmergy adoption rate",
      "measurement": "TDDR (Task Dependency Discovery Rate)",
      "baseline_tddr": "unknown",
      "target_tddr": 0.80
    },
    {
      "name": "sibling_discovery_injection",
      "hypothesis": "Proactive injection of parallel-task discoveries > discovery requiring agent initiative",
      "measurement": "Agent manifest includes builds_on_refs + contradicts_refs fields",
      "baseline_adoption": 0.15,
      "target_adoption": 0.85
    }
  ],
  "target_agents": [
    "python-pro (emergent learning, on-the-job tuning)",
    "workflow-orchestrator (cross-task synthesis)",
    "memory-keeper (pattern recognition at scale)"
  ],
  "membench_projection": {
    "m1_retention": "0.78 (-10% risk; smaller bundle)",
    "m2_relevance": "0.82 (-2%; context focused)",
    "m3_efficiency": "1.45 (+11% hypothesis; emergence gains)",
    "m4_overhead": 0.018,
    "m6_coordination": "0.60 (+76% hypothesis)",
    "composite_hypothesis": "78.0–82.5 (range due to m3 uncertainty)"
  },
  "risk_gates": {
    "m8_confabulation": "if > 5%, quarantine immediately",
    "m1_retention": "if < 70%, agents lack context; abort mutation",
    "m3_efficiency": "if < 1.0, memory overhead uncompensated; revert"
  }
}
```

---

## Implementation Architecture

### Mutation Evolution Loop

```
┌─────────────────────────────────────────────────────────────────────────┐
│ T=0 BASELINE (2026-04-23)                                               │
├─────────────────────────────────────────────────────────────────────────┤
│ Archive & measure:                                                      │
│   - global HONEY.md (conservative-v1.0 bundle)                         │
│   - faerie2/.claude/HONEY.md (spawn contract bundle)                   │
│   - Baseline membench: M1=88%, M3=1.31×, composite=78.4                │
│   - Mutation baseline: MDR=4.66, MC={36B/18N/36H/9U}, SR=10%           │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ SPAWN PHASE (W1-W3)                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│ Mutation routing at agent spawn:                                        │
│   1. Identify agent type + task category                                │
│   2. Look up routing table:                                             │
│      - Evidence curation → conservative-v1.0 (proven method)            │
│      - Exploratory tasks → experimental-v1.0 (hypothesis testing)       │
│      - Synthesis → hybrid (conservative core + experimental methods)    │
│   3. Render bundle via 7x_spawn_template.py --bundle {variant}          │
│   4. Inject as context; include mutation_vector + measurement_gates     │
│   5. Agent receives "you're in MUTATION EXPERIMENT. Report signal X."   │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ AGENT EXECUTION                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ Agent runs with bundle variant:                                         │
│   - Works under assigned mutation context                               │
│   - Writes manifest with bundle_variant field                           │
│   - Appends COC entry: bundle={variant}, measurement_gates_hit=[]       │
│   - Streams pollen with signal lines:                                   │
│     - "EMERGENCE_SIGNAL: X worked; hypothesis Y confirmed"              │
│     - "UNCERTAINTY: Rule Z led to conflicting guidance"                 │
│     - "FAILURE: Expected behavior Q didn't occur under rule R"          │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ MEASUREMENT & COLLECTION (/handoff)                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ membot collects across all agents:                                      │
│   1. Group manifests by bundle_variant (conservative vs experimental)   │
│   2. For each group, measure:                                           │
│      - M1: Can facts be retrieved in next session? (query-based)       │
│      - M3: Did agents complete more tasks per token?                   │
│      - M6: Did agents cite predecessor findings?                        │
│   3. Cross-compare variant groups (ANOVA or t-test)                     │
│   4. Classify emergent outcomes:                                        │
│      - BENEFICIAL (higher M3 + higher M1 = keep variant)                │
│      - NEUTRAL (no delta; harmless)                                     │
│      - HARMFUL (higher error rate; quarantine)                          │
│      - UNCERTAIN (mixed signals; flag for deeper analysis)              │
│   5. Update mutation_vector classification in NECTAR                    │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ T+1 SYNTHESIS & EVOLUTION                                               │
├─────────────────────────────────────────────────────────────────────────┤
│ After measurement baseline is wired:                                    │
│   1. Calculate T+1 Preservation Rate (% beneficial mutations retained)  │
│   2. Generate T+1 bundle variants:                                      │
│      - Evolve beneficial mutations into new bundle                      │
│      - Prune harmful mutations (explicit audit trail)                   │
│      - Compound multi-mutation benefits (if applicable)                 │
│   3. Stage T+1 variants for next phase:                                 │
│      - conservative-v1.1 (conservative-v1.0 + pruned harmful)           │
│      - experimental-v1.1 (experimental-v1.0 + beneficial mutations)    │
│      - hybrid-v1.0 (new variant: conservative core + exp methods)       │
│   4. Archive T=0 bundles in forensics/mutations/ (immutable reference)  │
│   5. Update routing table + mutation_vector in ARCHITECTURE.md          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Bundle Routing Table

```json
{
  "routing_table": {
    "version": "1.0",
    "created": "2026-04-24",
    "mutation_baseline": "T=0 archived 2026-04-23",
    "routes": [
      {
        "phase": "W1",
        "agents": ["data-engineer", "evidence-curator"],
        "bundle_variant": "conservative-v1.0",
        "rationale": "Proven ingest + tiering pipelines; minimize risk on foundation work"
      },
      {
        "phase": "W2",
        "agents": ["python-pro", "workflow-orchestrator"],
        "bundle_variant": "experimental-v1.0",
        "rationale": "Composition + synthesis tasks; high mutation concentration; measure M3 ROI"
      },
      {
        "phase": "W2",
        "agents": ["report-writer", "documentation-engineer"],
        "bundle_variant": "conservative-v1.0",
        "rationale": "Publication gates quality; use proven methods"
      },
      {
        "phase": "W3",
        "agents": ["memory-keeper", "synthesizer"],
        "bundle_variant": "experimental-v1.0",
        "rationale": "Deep synthesis + pattern recognition; maximum mutation concentration"
      }
    ],
    "fallback": "conservative-v1.0 (if unknown agent type)"
  }
}
```

### Bundle Storage & Versioning

Location: `{repo}/forensics/bundles/`

Filename pattern: `bundle-{name}-{version}-{created_ts}.json` (timestamp-first per mth00033)

```
forensics/bundles/
  ├── bundle-conservative-v1.0-20260423T000000Z.json  (T=0 baseline, locked)
  ├── bundle-experimental-v1.0-20260423T000000Z.json  (T=0 baseline, locked)
  ├── MUTATIONS-T0-ARCHIVE.jsonl                      (immutable COC: all T=0 variants)
  ├── MUTATIONS-CLASSIFICATION-SESSION_{SID8}.jsonl  (per-session outcomes)
  └── bundle-evolution-lineage.md                     (narrative: which variants evolved from which)
```

---

## Emergence Classification

### What Counts As Beneficial

**From HONEY.md sys00019** (evolutionary selection pressure):

> "Features that solve multiple unplanned problems are pointing at an unnamed structural issue — name the structure, not the symptoms. Planned benefits prove the feature works. Unplanned benefits prove it was right."

Applied to bundle mutations:

| Signal | Classification | Action |
|--------|---|---|
| **M3 ↑ + M1 ↑ + M6 ↑** | BENEFICIAL_EMERGENT | Adopt broadly; promote to conservative-v2.0 |
| **M3 ↑ + M1 ≈** | BENEFICIAL_FOCUSED | Keep for exploratory tasks; monitor M1 drift |
| **M3 ≈ + no regression** | NEUTRAL | Optional; no harm in keeping |
| **M1 ↓↓ (>15%)** | HARMFUL | Quarantine; archive as lesson |
| **M8 > 5% (confabulation)** | HARMFUL_VETO | Immediate rollback; human review |
| **M3 ↑ + M1 ↓ (trade-off)** | UNCERTAIN | Measure longer; calculate true ROI |

### Emergence Heuristics

1. **Unplanned benefit = deeper principle**
   - If experimental bundle improves M6 (coordination) beyond hypothesis, ask: "What structure did we unlock?"
   - Example: "Agent explicitly reading NECTAR wasn't a bundle change; why did it help?" → Answer: "Stigmergy works when agents are TOLD to look."

2. **Multi-metric improvement = compound effect**
   - If M3 + M6 both improve, the bundle enabled cross-pollination, not just efficiency.
   - Promote this as a new principle.

3. **Failure cascades backward**
   - If M8 (confabulation) rises, agents are hallucinating facts from the bundle.
   - Root cause: bundle includes uncertain methods marked "proven" but unvalidated in this domain.
   - Action: audit the methods; separate hypothesis from fact.

---

## Measurement Framework

### Membench Integration

Bundle variants are measured using the same 11-metric membench (v0.2.0) + mutation-specific gates.

**M3 (Work Efficiency) is primary:**

Per MEMBENCH-INDEX.md, M3 = 1.31× baseline means agents with memory complete ~31% more tasks. If bundle mutation changes M3:

- **+5% ≥ M3 ↑ ≥ +15%:** Likely beneficial (compounding value)
- **-5% ≤ M3 ↓ ≤ +5%:** Neutral (no loss, some gain possible)
- **M3 ↓ > -10%:** Likely harmful (overhead not compensated)

**M6 (Coordination) is secondary:**

Experimental bundle aims to increase M6 (% findings cited by later agents) from 34% → 60%. This is the **stigmergic learning metric**.

Measurement: Query reasoning.jsonl for builds_on_refs + contradicts_refs fields in agent manifests.

### Mutation-Specific Metrics

```json
{
  "mutation_metrics": {
    "MDRC": "Mutation Detection Rate per Classification (B/N/H/U buckets per session)",
    "MC": "Classification Distribution (% of detected mutations in each bucket)",
    "SR": "Shadow Rate (% of rule citations that appear in predecessor artifacts)",
    "PR": "Preservation Rate (% of T=0 beneficial mutations retained in T+1)",
    "EBI": "Emergent Behavior Index (unplanned multi-metric improvements / total mutations)",
    "FD": "Flag Delay (time from emergence signal to classification)",
    "CCI": "Capability Composition Index (multi-agent effects / agent-local effects)"
  },
  "gates": {
    "SUBSTRATE_WARN": "if harmful% > 15%, pause evolution; human review",
    "CITATION_DRIFT": "if SR ≥ 10%, phantom citations detected; audit bundle clarity",
    "M8_VETO": "if confabulation > 5%, quarantine variant immediately",
    "M11_VETO": "if bootstrap < 70%, agents crash on memory load; revert"
  }
}
```

### Baseline T=0 Targets for Phase 1

**Conservative-v1.0:**
- M1 = 0.88 (target: stable)
- M3 = 1.31× (target: stable)
- Composite = 78.4 (target: stable)

**Experimental-v1.0:**
- M1 = 0.78 (−10% acceptable risk)
- M3 = 1.45+ (+11% hypothesis target)
- M6 = 0.60 (+76% hypothesis target)
- M8 < 0.05 (zero confabulation veto)
- Composite = 78.0–82.5 (range due to M3 uncertainty)

**Success criteria:**
1. Experimental bundle M3 ≥ 1.45 (hypothesis validated)
2. Experimental M8 < 5% (confabulation gate OK)
3. Conservative M3 stays ≥ 1.30 (no regression)
4. PR (Preservation Rate) ≥ 80% (beneficial mutations kept)

---

## CLI Commands

### Operator Interface

```bash
# List available bundle variants
claude bundle --list

# Show bundle contents + mutation vector
claude bundle --show conservative-v1.0
claude bundle --show experimental-v1.0

# Spawn an agent with explicit bundle override (for testing)
claude spawn --agent evidence-curator --bundle experimental-v1.0 --task task_12345

# View mutation metrics from last session
claude bundle --metrics --session {SID}

# Compare two bundle variants (A/B test results)
claude bundle --compare conservative-v1.0 experimental-v1.0 --metric m3

# Validate bundle integrity (hash chain)
claude bundle --validate forensics/bundles/bundle-conservative-v1.0-*.json

# Evolve T=0 bundles to T+1 (after measurement baseline wired)
claude bundle --evolve T=0 --output T+1 --preservation-threshold 0.80

# View bundle lineage (which variants evolved into which)
claude bundle --lineage experimental --depth 3
```

### Measurement Commands

```bash
# Run membench on a session's bundle variants
python3 scripts/eval_membench.py --session {SID} --breakdown-by-bundle

# Measure mutation metrics specifically
python3 scripts/9x_mutation_analyzer.py --session {SID} \
  --output forensics/mutations/MUTATIONS-CLASSIFICATION-SESSION_{SID8}.jsonl

# Validate T=0 preservation (before evolution to T+1)
python3 scripts/9x_bundle_preservation_validator.py \
  --baseline T=0 \
  --session {SID} \
  --threshold 0.80 \
  --output forensics/mutations/preservation-report-{SID8}.jsonl
```

---

## Appendices

### A. Full Conservative Bundle Formula (JSON)

See **conservative-bundle-formula-v1.json** in forensics/bundles/ (2,847 bytes, hash-chained).

**Key sections:**
- Principles: sys00001–sys00029 (locked, no mutation)
- Methods: mth00002–mth00074 (locked, no mutation)
- F(0) crystallization: sys00030–sys00034 + mth00073–mth00082 (locked)
- Preferences: pref00001–pref00024 (locked)

**Mutation vector:** None (T=0 baseline).

### B. Full Experimental Bundle Formula (JSON)

See **experimental-bundle-formula-v1.json** in forensics/bundles/ (1,823 bytes, hash-chained).

**Key sections:**
- Core principles: sys00030–sys00031 only (minimal, locked)
- High-mutation methods: Recent NECTAR entries (2026-04-22 curiosity, stigmergic learning)
- Omitted: Historical methods, COC detail, forensics depth

**Mutation vectors:**
- Curiosity pull vs push (M6 target ↑)
- Droplet discovery bootstrap (TDDR target ≥0.80)
- Sibling discovery injection (coordination adoption target ↑)

### C. HONEY.md Citations

| Citation | File | Line | Purpose |
|----------|------|------|---------|
| sys00030 | HONEY.md | 177 | f(0) principle definition |
| sys00031 | HONEY.md | 179 | Stigmergy-only coordination |
| sys00032 | HONEY.md | 181 | Artifacts-in-forensics |
| sys00033 | HONEY.md | 183 | Task_id universal join |
| sys00034 | HONEY.md | 185 | Programmatic composition |
| mth00075 | HONEY.md | 203 | Mutation-as-measurement discipline |
| mth00077 | HONEY.md | 199 | Spawn = bundle dispatch |
| mth00082 | HONEY.md | 191 | Deterministic ops call CLI |
| sys00002 | HONEY.md | 38 | Budget is heartbeat |
| sys00027 | HONEY.md | 52 | CLAUDE.md is inviolable |

### D. Membench Baselines

**Source:** MEMBENCH-INDEX.md (2026-04-21 v0.2.0)

```
M1 Retention:        88%    (88 of 100 facts findable)
M2 Relevance:        84%    (84% of HONEY is procedural)
M3 Efficiency:      1.31×   (31% more effective work with memory)
M4 Overhead:        2.8%    (memory costs 2.8% of context)
M5 Continuity:     100%    (perfect checkpoint recovery)
M6 Coordination:     34%    (34% of findings are cited by later agents)
M7 Crystallization:  82%    (HONEY is 82% efficient density)
M8 Confabulation:    0%    (zero false facts)
M9 Ceiling-Hit:      40%    (4–5 metrics at near-perfect)
M10 Coverage:       100%    (all 11 dimensions populated)
M11 Bootstrap:      100%    (no agent startup failures)
COMPOSITE:          78.4    (healthy, room to optimize)
```

### E. Mutation Baseline T=0

**Source:** HONEY.md mth00075 (2026-04-23 crystallization)

```json
{
  "baseline_date": "2026-04-23T00:00:00Z",
  "detection_rate": 4.66,
  "classification": {
    "beneficial_count": 36,
    "neutral_count": 18,
    "harmful_count": 36,
    "uncertain_count": 9,
    "total": 99
  },
  "percentages": {
    "beneficial": 36.4,
    "neutral": 18.2,
    "harmful": 36.4,
    "uncertain": 9.1
  },
  "shadow_rate": 0.10,
  "soft_gates": {
    "substrate_warn_threshold": 0.15,
    "citation_drift_threshold": 0.10
  },
  "preservation_rate_target": "measure_t1_against_t0_after_repair"
}
```

### F. Implementation Summary References

**Source:** IMPLEMENTATION-SUMMARY-2026-04-22-SPAWN-BUNDLE-F0.md

Key metrics from spawn optimization phase:

| Metric | Before | After | Saving |
|--------|--------|-------|--------|
| Boilerplate size injected | 42 KB | ~2 KB | 95% |
| Tokens per spawn | 10,300 | ~50 | 99.5% |
| Cycle overhead (5 spawns) | 51,500 | 250 | 99.5% |
| Composition inference | 300–800 tok/spawn | 0 | 100% |

**Per faerie cycle (5 spawns):**
- Before: 217,500 tokens (23% of context)
- After: ~750 tokens (<1% of context)
- Net saving: 216,750 tokens

**Impact on bundle evolution:** Bundle variants can now be spawned at almost zero cost. This enables rapid A/B testing of mutations.

### G. Task_id Stigmergic Join

**Source:** HONEY.md sys00033 (universal filename pattern)

```
{ts}_{product-type}_{task_id}_{agent-signature}_{session_id8}.{ext}

Example:
20260424T163042Z_agent-run_task_12345_ab2e496a_f0a1b2c3.json
                                      ^^^^^^^^
                            New agent can grep "_12345_" in forensics/
                            to find ALL work on this task (droplets, manifests, COC)
                            without context cost.
```

---

## Closing Notes

### Why Bundle Evolution Matters

1. **Measurement before repair:** By versioning bundles and measuring T=0 before fixing mutations, we establish the true value of each improvement.

2. **Emergence visibility:** Tracking unplanned multi-metric improvements reveals unnamed structural principles (sys00019).

3. **Parallelism:** Experimental bundles let us test hypotheses (higher M3, better M6) without forcing production agents into risk.

4. **f(0) alignment:** Bundle variants are stored, not dynamically composed. Routing is config-driven, not agent-decided. Measurement is automated, not manual. Pure programmatic composition (sys00034).

### Next Steps

1. **Week 1:** Archive T=0 bundles; wire measurement infrastructure (membench + mutation metrics)
2. **Week 2:** Run W1 with conservative-v1.0; W2-W3 with experimental-v1.0; measure M3/M6 delta
3. **Week 3:** Analyze results; classify mutations; generate T+1 bundle variants
4. **Week 4:** Deploy T+1 bundles; measure preservation rate; update routing table
5. **Month 2+:** Quarterly evolution cycles; compound beneficial mutations; retire harmful mutations

---

## Document History

| Version | Date | Author | Status |
|---------|------|--------|--------|
| 1.0 | 2026-04-24 | documentation-engineer (synthesizer) | Complete |

**Sourced from:** ~10.7K tokens of HONEY + NECTAR + audit reports + implementation summary (2026-04-22).

**Hash:** `doc_hash: sha256:pending` (will be stamped at vault write).

**Next:** Implementation phase (Phase 4 agents validate routing, measurement infrastructure, and baseline preservation).

---

**Generated:** 2026-04-24T16:30:00Z | **Classification:** Architecture Document | **Status:** Ready for implementation planning
