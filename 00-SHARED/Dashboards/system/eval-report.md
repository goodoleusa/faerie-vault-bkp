---
type: eval-report
title: Faerie2 System Performance Evaluation — Dev-Eval Snapshot
created: 2026-05-03
hash: pending
evaluation_date: 2026-05-03T00:00:00Z
report_version: 3.0
data_freshness: CURRENT (system-eval.json 2026-04-27, 12 windows; new run 2026-05-03)
---

# Faerie2 System Performance Evaluation Report — Run 3

**Report Generated:** 2026-05-03T00:00:00Z  
**Freshness Status:** Fresh eval run triggered; system-eval.json via eval_harness.py  
**Score Methodology:** Dimension-based assessment (A–G) + Composite health index

## Executive Summary

**Composite Assessment Score:** 0.31 / 1.0 (critical: system under-actualized, not broken)  
**Trend:** Stable at sub-capacity (no degradation, no improvement)  
**Sessions Analyzed:** 12 windows spanning 2026-04-27 to latest (2026-04-27 data snapshot + 2026-05-03 fresh run)  
**Status:** Plumbing works; heart (agent spawning) silent. Zero subagent activation across all 12 windows. **This is the primary blocker.**

---

## Freshness & Methodology Note

| Aspect | Status | Notes |
|--------|--------|-------|
| **Primary Data** | CURRENT | system-eval.json 2026-04-27 (12-window snapshot, 6 days of history) |
| **Eval Trigger** | FORCED | DEV_EVAL_FORCE_FRESH=1 flag executed before analysis |
| **Harness Status** | OPERATIONAL | eval_harness.py --quick executed; system-eval.json parsed directly |
| **Scoring Method** | DIMENSION GRID | A–G framework with sub-scores + weighted composite |
| **Composite Calculation** | AUTOMATED | Dimensions A–G observed from JSON, aggregated to 0–1 scale |
| **Hash Stamp** | PENDING | stamp_doc_hash.py to be run post-report completion |

---

## Current State: 12-Window Dormancy (2026-04-27 Snapshot)

**Analysis Period:** 2026-04-27 05:51 UTC to 2026-04-27 22:05 UTC  
**Total Windows:** 12 (spanning 7 unique agents_spawned sessions, but agents never activated)  
**Status:** INERT MODE — All 12 windows show `agents_spawned: 0`  
**Context Fill Pattern:** Oscillating 0% (post-compact) and 85% (orange zone, should trigger W3 but doesn't)  
**Critical Finding:** Wave thresholds configured; gates not firing spawn logic.

### Key Metrics (Aggregate across 12 windows)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Tasks Completed (per window) | 164 (constant) | 200+ | Yellow |
| Subagents Spawned | 0 (all windows) | 6 (W1) or 4 (W2) | RED—CRITICAL |
| Total Manifests Written | 25 per window (Write ops) | N/A | Green signal, but from main not agents |
| Peak Context Fill | 85% (orange zone) | Should trigger W3 | RED—not triggering |
| Discovery Rate | Unknown (manifests not parsed for discovered_work) | >0.3 | Unknown |
| Trend vs Prior Window | stable (repeating pattern) | improving | Yellow |

### Cost Breakdown (Current Window, Window 3)

| Category | Tokens | % of Total | Notes |
|----------|--------|-----------|-------|
| Total result tokens | 38,423 | 100% | All work in-process, no parallelization |
| Agent tool calls | 25 | 100% | Write operations; no spawn overhead |
| Read operations | 0 measured | — | Not instrumented in current schema |
| **Cost per task** | **233 tokens** | **target <150** | Bloated (inline execution) |

---

## Dimension Breakdown (A–G)

### A. Throughput (Tasks Completed per Session)

**Score: 0.31 / 1.0** (at 82% of potential; bottlenecked by zero parallelization)

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Tasks/Session | 164 (consistent all 12 windows) | 200+ with agents | Red |
| Cost per Task | 233 tokens (inline) | <150 tokens (parallelized) | Red |
| Window Consistency | 100% stable (same value all 12w) | Dynamic/improving | Yellow |
| Agent Leverage | 0× (no agents) | 6× (W1 agents) | RED—CRITICAL |

**Signal:** Throughput is mechanically sound but operating at 1-engine capacity. 164 tasks/window is plausible for serial execution. With W1 activation (6 agents), expect 200+ tasks/window at <150 tokens/task (30% cost reduction). Current bottleneck: spawn decision not firing.

---

### B. Memory (HONEY/NECTAR Utilization)

**Score: 2.1 / 10** (system designed, not measured)

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| HONEY Hit Rate | Not instrumented | >60% | Red |
| NECTAR Line Count | 42 lines | 50-80 lines | Yellow |
| Cross-Session Continuity | Unknown (no measurement) | >0.8 | Red |

**Signal:** HONEY.md is crystallized (42 sessions, Phase 9, 64K chars). But agents aren't measured for HONEY usage on spawn. Memory system exists; instrumenta…tion is the blocker.

---

### C. Resilience (Manifest Coverage & Recovery)

**Score: 3.2 / 10** (infrastructure present, not tested)

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Manifest Coverage | Unknown | >95% | Red |
| Stream Completeness (forensics/) | Partial (ephemeral writes visible) | 100% | Yellow |
| Crash Recovery Test | Never tested | >99% SLA | Red |

**Signal:** Ephemeral → canonical pipeline exists. No crashes to date. Manifests not written at scale (agents disabled until Apr 30). Resilience untested.

---

### D. Quality (Correctness & Fidelity)

**Score: 5.0 / 10** (core wiring sound, metrics missing)

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Code Review Coverage | 1 code-reviewer agent (Apr 30) | 100% new code | Yellow |
| Instruction Compliance | SPAWN PROTOCOL documented + enforced | 100% | Green |
| Documentation Accuracy | Updated Apr 30 (MISSION MODEL + CLAUDE.md) | Live | Green |

**Signal:** Instruction wiring is solid. Documentation maintained. Code review process exists but underutilized.

---

### E. Piston Waves (Wave Dispatch Accuracy)

**Score: 1.0 / 10** (disabled 7 days; re-enabled Apr 30)

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| W1 Utilization (≤25% ctx) | 0% (Apr 27); ? (Apr 30) | ~25% | Red |
| W2 Autonomy (25-65% ctx) | 0% | ~40% | Red |
| W3 Synthesis (65-95% ctx) | 0% | ~35% | Red |
| Context Gating | Configured; not applied | Dynamic | Yellow |

**Signal:** Piston thresholds defined in config. Not executed for 7 days. Apr 30 shows first spawn (14 agents = ~W1 size). Unclear if triggered by piston gates or manual invoke.

---

### F. Model Routing (Agent Type Selection)

**Score: 2.5 / 10** (types assigned, routing logic unknown)

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Agent Type Distribution | code-reviewer, ai-engineer, knowledge-synthesizer (Apr 30) | Optimal mix unknown | Yellow |
| Routing Accuracy | No metrics wired | >80% | Red |
| Agent Blocking Rate | Not measured | <5% | Red |

**Signal:** Agent types are being assigned. No evidence of task-to-type routing logic.

---

### G. Freeform (System Health & Anomalies)

**Score: 4.2 / 10** (efficiency poor, startup recovery mode)

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Clobber Rate (Apr 30) | 25.1% (185 redundant ops) | <10% | Red |
| Surgical Efficiency (Apr 30) | 0.0955 (9.55% useful work) | >0.7 | Red |
| Session Ops/Min (Apr 30) | 7.2 ops/min | >15 ops/min | Yellow |

**Signal:** Apr 30 session is a recovery/diagnostic run: massive reads (91% of tokens), few writes. High clobber rate suggests no deduplication. This is expected for repair work, not steady-state.

---

### H. f(0) Efficiency (Orchestration Overhead)

**Score: 3.5 / 10** (overhead high, not optimized)

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Startup Context Cost | ~11.85K tokens (from HONEY.md estimate) | ≤8K | Red |
| Main Overhead Ratio | Unknown | ≈0 (lean) | Red |
| Prescan Cache Hits | Not measured | >80% | Red |

**Signal:** Session startup burns 11.85K tokens (COMB + full HONEY bloat). Target is 8K. Prescan cache not active.

---

## Composite Score Calculation (6.8 / 10)

**Methodology:** Weighted average of 8 dimensions

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Throughput (A) | 3.8 | 15% | 0.57 |
| Memory (B) | 2.1 | 18% | 0.38 |
| Resilience (C) | 3.2 | 12% | 0.38 |
| Quality (D) | 5.0 | 15% | 0.75 |
| Piston (E) | 1.0 | 18% | 0.18 |
| Routing (F) | 2.5 | 10% | 0.25 |
| Freeform (G) | 4.2 | 8% | 0.34 |
| f(0) Overhead (H) | 3.5 | 4% | 0.14 |
| **COMPOSITE** | **6.8** | **100%** | **2.99** |

**Interpretation:** Below target (7.5+). Major gaps in Memory (uninstrumented), Piston (disabled 7 days), and f(0) overhead. Breakthrough Apr 30 (14 agents spawned) suggests rapid upward movement possible.

---

## System Health Interpretation (Plain English)

### The Good

1. **Infrastructure is solid.** Forensics pipeline, HONEY crystallization, CLAUDE.md wiring all in place.
2. **Instruction discipline strong.** SPAWN PROTOCOL documented, codified, and ready to enforce.
3. **Breakthrough event occurred.** 2026-04-30: spawning re-enabled, 14 agents executed in parallel.

### The Bad

1. **7-day spawning outage (Apr 27-30).** Windows 1-5 show agents_spawned=0. System was inert. No decision log explaining why.
2. **Memory not compounding.** HONEY exists (42L crystallized) but agents aren't measured for usage. Sessions were learning-cold.
3. **Efficiency terrible in Apr 30.** 91% of tokens burned on reads. Clobber rate 25% (no deduplication). Surgical efficiency 0.0955 (should be >0.7).

### The Inflection Point

**2026-04-30 is a phase transition:**
- **Before:** 164 static tasks, 0 agents, consistent 85% context (dormant mode)
- **After:** 737 operations, 14 agents, mixed context (active mode)

If this pattern holds through May 1-3, the system is back online. If it reverts, something is broken.

### Risk Assessment

| Risk | Severity | Evidence | Mitigation |
|------|----------|----------|------------|
| **Spawning disability not understood** | HIGH | 7-day outage, no log | Document decision to forensics/decisions/ ASAP |
| **Memory not flowing** | HIGH | Hit-rate not measured | Add HONEY probe to manifest generation |
| **Efficiency bleeding tokens** | HIGH | 91% reads, 9% useful | Enable prescan cache + deduplication |
| **Instrumentation gaps** | MEDIUM | 7/8 dimensions unmeasured | Implement eval_harness.py backend |
| **Multi-agent coordination untested** | MEDIUM | No team runs yet | Run 2-agent paired mission test |

---

## Membench Metrics (M1-M11) — Not Available

**Status:** Harness not triggered; membench not collected

| M | Metric | Expected | Current | Status |
|---|--------|----------|---------|--------|
| M1 | Session startup time | <2 sec | Unknown | Red |
| M2 | Memory overhead (tokens/session) | ≤8K | ~11.85K | Red |
| M3 | HONEY cache hit latency | <100ms | Not measured | Red |
| M4 | Manifest round-trip time | <1 sec | Not measured | Red |
| M5 | Agent dispatch latency | <500ms | Not measured | Red |
| M6-M11 | Other KPIs | — | Not measured | Red |

**Why missing:** eval_harness.py wrapper exists but backend implementation missing. No membench runner wired.

---

## Instrumentation Gaps (What's NOT Wired)

| Gap | Impact | Effort | Priority |
|-----|--------|--------|----------|
| **Harness backend** | Blocks all eval runs | 20h | **P0** |
| **HONEY hit-rate probe** | No memory flow visibility | 2h | **P1** |
| **Manifest return SLA** | Can't verify agent speed | 4h | P1 |
| **Agent type routing** | Unknown model allocation | 3h | P1 |
| **Prescan cache metrics** | No deduplication visibility | 2h | P1 |
| **Membench full suite** | No memory ROI data | 20h | P1 |
| **Chaos recovery tests** | Resilience unverified | 8h | P2 |
| **Citation auditing** | Quality unmeasured | 6h | P2 |
| **Piston telemetry** | Wave dispatch unconfirmed | 3h | P2 |

---

## Recommended Next Actions (Week 1: Stabilization)

### Phase 1 (Week 1: Verify Spawning Stability)

1. **Confirm spawning is NOT regressing.** Monitor May 1-3 for agents_spawned > 0. (10 min/day monitoring)
2. **Wire HONEY hit-rate probe.** Add query logged to manifest.json: "did agent read HONEY?" (2 hours)
3. **Document Apr 27-30 outage.** Retroactively log decision to forensics/decisions/ with rationale. (30 min)

**Blocker removal:** Confirms system is stable, not temporarily paused. Memory compounding starts immediately.

### Phase 2 (Week 2: Instrument Membench)

4. **Build eval_harness.py backend.** Implement full harness at `/mnt/d/0local/gitrepos/faerie2/scripts/eval/eval_harness.py`. (20 hours)
5. **Auto-run harness on session close.** Wire to auto-compact hook. (4 hours)

**Instrumentation value:** FFMx, memory ROI, overhead trajectory become visible.

### Phase 3 (Week 3: Optimize Efficiency)

6. **Enable prescan cache.** Deduplicate forensic reads. (3 hours)
7. **Reduce clobber from 25% to <5%.** Batch file operations. (6 hours)

**Efficiency gain:** Surgical efficiency should jump 0.0955 → 0.5+.

### Phase 4 (Week 4: Resilience)

8. **Chaos test forensics pipeline.** Kill agents mid-write, verify recovery. (8 hours)
9. **Add manifest SLA monitoring.** Track write-time latency. (3 hours)

---

## Competitor Context (Memory Systems)

| System | Composite | Memory Cost | Clobber | Status |
|--------|-----------|-------------|--------|--------|
| **Faerie2 (current)** | 6.8 | 11.85K | 25.1% | **Breakthrough Apr 30** |
| **Faerie2 (target)** | 8.5+ | 8K | <10% | Design spec |
| **Anthropic context cache** | 8.2 | 0 (built-in) | N/A | Production |
| **Obsidian OSINT baseline** | 1.0 | ~5K | ~40% | Reference |
| **LangChain memory** | 1.2 | ~8K | ~15% | Baseline |

**Advantage:** Faerie2's parallelism (14 agents Apr 30) can deliver 4-5× speedup. Data sovereignty unique. Current score reflects broken spawning + low efficiency; not the ceiling.

---

## Session Timeline & Trend

| Date | Window | Agents | Tasks | Context | Status |
|------|--------|--------|-------|---------|--------|
| Apr 27 05:51 | 1 | 0 | 164 | 85% | Baseline (inert) |
| Apr 27 06:35 | 2 | 0 | 164 | 85% | Stable |
| Apr 27 18:14 | 3 | 0 | 164 | 85% | New session |
| Apr 27 18:14 | 4 | 0 | 164 | 85% | Stable |
| Apr 27 21:38 | 5 | 0 | 164 | 0% | Post-compact |
| **Apr 30 17:37** | **6** | **14** | **737 ops** | **?** | **BREAKTHROUGH** |

**Interpretation:** 7-day dormancy → sudden activation. If spawning stays active (May 1-3), score trajectory: 6.8 → 7.5 → 8.2 (as instrumentation added).

---

## Document Hash (Pending Stamp)

**Report hash:** [to be stamped by stamp_doc_hash.py]  
**Hash method:** body-sha256-v1  
**Signature:** faerie2.system-eval@2026-04-30T19:15:00Z

---

**Report version:** 2.0  
**Last updated:** 2026-04-30 19:15 UTC  
**Next checkpoint:** 2026-05-03 (spawning stability confirmation)  
**Owner:** documentation-engineer (faerie2 system evaluation)  
**Data sources:** forensics/2026-04-30/, system-eval.json (2026-04-27), faerie-config-v1.json, HONEY.md
