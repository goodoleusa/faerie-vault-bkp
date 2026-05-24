---
type: research-outline
status: active
created: 2026-04-27
updated: 2026-04-27T21:43:00Z
tags: [research, publication, arxiv, emergence, stigmergy, orchestration]
parent: ../README.md
doc_hash: sha256:pending
hash_ts: pending
hash_method: body-sha256-v1
---

> **Breadcrumb:** faerie2 > docs > 4x-RESEARCH-PAPER-OUTLINE

# faerie2 Publication Research: arXiv Landscape & Novel Contributions

## Eval Baseline (from forensic evals, 2026-04-25)

| Dimension | Score | Confidence | Key Metric |
|-----------|-------|------------|------------|
| composite | 0.742 | stable | up from 0.554 baseline (+0.188) |
| quality | 0.891 | stable | citation_accuracy 1.0, cross_session_recall 0.94 |
| resilience | 0.824 | stable | crash_recovery 0.96, manifest_coverage 1.0 |
| throughput | 0.500 | stable | 18 tasks/session median; cost_per_finding = NULL |
| piston | 1.000 | establishing | bootstrap_mode=true; wave metrics not yet wired |
| memory | 0.667 | stable | bootstrap_mode=true; nectar_relevance = 0.0 |
| model_routing | 0.667 | stable | haiku_w1_rate 1.0; w2 wiring = NULL |

**Competitor deltas (self-reported via eval harness, not externally validated):** +149% vs vanilla Claude, +108% vs ChatGPT memory, +91% vs mem0. These are from the frozen_rubric eval framework — not peer-reviewed benchmarks. Any paper must characterize these as internal eval scores.

---

## Part 1 — arXiv Literature Survey (8 Papers)

### Paper 1: Emergent Collective Memory in Decentralized Multi-Agent AI Systems
**arXiv:** [2512.10166](https://arxiv.org/abs/2512.10166) | December 2025 | Khushiyant et al.

**Problem:** How does collective memory emerge from individual agent memory + environmental trace deposits, without centralized control?

**Key Results:** Individual memory alone: +68.7% over no-memory baseline. At high density (ρ > 0.20), stigmergic traces outperform individual memory by 36–41%.

**faerie2 comparison:** Validates faerie2's stigmergy-as-coordination approach. Novel extension in faerie2: typed traces (manifests, investigation_labels, compass edges) with semantic bearing semantics (N/S/E/W) rather than undirected pheromone gradients. faerie2 also chains traces to forensic COC.

---

### Paper 2: Emergent Coordination in Multi-Agent Systems via Pressure Fields
**arXiv:** [2601.08129](https://arxiv.org/abs/2601.08129) | January 2026

**Problem:** Replace role-based MAS coordination with role-free stigmergic approach using quality signals.

**Key Results:** 48.5% solve rate (vs 12.6% conversation-based, 1.5% hierarchical). Removing temporal decay causes -10 percentage points.

**faerie2 comparison:** **CLOSEST PRIOR ART for piston waves.** Both use pressure as coordination metaphor. CRITICAL DIFFERENCES: (1) Paper uses quality-signal pressure on shared artifact; faerie2 uses context-fill pressure on ORCHESTRATOR; (2) Paper has no forensic trace chain; (3) faerie2's W1/W2/W3 staging is asymmetric/irreversible (rocket physics), not continuous gradient; (4) faerie2 adds reputation-aware dispatch (agent scores gate assignment).

---

### Paper 3: Right to History: A Sovereignty Kernel for Verifiable AI Agent Execution
**arXiv:** [2602.20214](https://arxiv.org/abs/2602.20214) | February 2026 | Jing Zhang

**Problem:** No existing system provides tamper-evident, independently verifiable records of AI agent actions on personal hardware.

**Key Results:** Proposes sovereignty kernel extending Floridi's informational rights framework. Focuses on personal hardware deployment.

**faerie2 comparison:** Strong conceptual alignment on forensic integrity. Key DIFFERENTIATOR: faerie2 integrates forensic integrity as byproduct of coordination (manifest writes ARE the forensic record), not as separate auditing layer. faerie2's COC entries produced by agents as part of normal work, not surveillance overlay. Architectural distinction worth articulating.

---

### Paper 4: Adaptive Orchestration: Scalable Self-Evolving Multi-Agent Systems
**arXiv:** [2601.09742](https://arxiv.org/abs/2601.09742) | January 2026 | Sathish Sampath, Anuradha Baskaran

**Problem:** Monolithic agents suffer context pollution. Static swarms have latency/resource overhead.

**Methodology:** Dynamic Mixture of Experts — "hires" specialized sub-agents based on real-time conversation analysis.

**faerie2 comparison:** Shares dynamic sub-agent spawning. faerie2 diverges: (1) Spawning triggered by stigmergy (investigation_label density, compass edge bearing), not conversation-analysis; (2) Reputation-weighted dispatch; (3) Spawn contract enforced by script (0x_spawn_template.py), not LLM judgment; (4) Mutation discipline (measure-before-fix) adds governance.

---

### Paper 5: Emergent Coordination in Multi-Agent Language Models
**arXiv:** [2510.05174](https://arxiv.org/abs/2510.05174) | October 2025

**Problem:** Is genuine higher-order emergent structure in LLM multi-agent systems real, or spurious temporal coupling?

**Methodology:** Information-theoretic framework measuring dynamical emergence vs spurious synergy.

**faerie2 comparison:** This paper measures whether emergence is real in LLM systems — natural evaluation framework for faerie2's stigmergic emergence claims. faerie2 currently lacks this measurement (piston dimension in bootstrap_mode). Paper submission should apply 2510.05174 framework or explicitly acknowledge gap.

---

### Paper 6: Self-Healing Machine Learning: A Framework for Autonomous Adaptation
**arXiv:** [2411.00186](https://arxiv.org/abs/2411.00186) | November 2024 | Paulius Rauba et al.

**Problem:** ML systems degrade in deployment; self-healing = autonomous diagnosis + corrective action.

**faerie2 comparison:** Addresses model-level self-healing. faerie2's mutation discipline targets orchestration substrate health (manifest validator, wave_gate retirement, empty_probe_validator), not model weights. Distinct contribution: substrate self-healing for orchestration infrastructure, not ML model health.

---

### Paper 7: AdaptOrch: Task-Adaptive Multi-Agent Orchestration
**arXiv:** [2602.16873](https://arxiv.org/abs/2602.16873) | February 2026

**Problem:** As LLM capabilities converge, topology selection (parallel/sequential/hierarchical/hybrid) becomes key performance driver.

**Methodology:** Formalizes topology selection; dynamically selects among 4 canonical topologies based on task dependency graphs.

**faerie2 comparison:** faerie2 does not use topology selection — uses compass graph navigation (stigmergy-first, bearing-following). Topology emerges from compass edges rather than being selected by router. Fundamental architectural difference: explicit topology vs emergent topology from local bearing signals.

---

### Paper 8: AOI: Context-Aware Multi-Agent Operations via Dynamic Scheduling
**arXiv:** [2512.13956](https://arxiv.org/abs/2512.13956) | December 2025

**Problem:** Context management and dynamic task prioritization across multiple agents.

**Methodology:** LLM-based Context Compressor + dynamic scheduling + three-layer memory architecture.

**faerie2 comparison:** faerie2's cascading summarization (HONEY/NECTAR/pollen) has structural similarity to AOI's three-layer memory. Key differentiator: crystallization is NOT compression — it is integration (denser + richer, not lossy). faerie2 also routes memory via stigmergic traces, not central LLM compressor.

---

## Part 2 — faerie2's Five Novel Contributions

### Contribution 1: Forensic Coordination — COC as Byproduct

**Claim:** faerie2 is first system making forensic chain-of-custody a natural byproduct of coordination rather than surveillance layer.

**Evidence:** Every manifest write produces forensic record. Manifest IS the COC entry — same artifact, dual purpose. Agents produce own signed, hash-chained manifests as part of task completion.

**Measurable:** resilience=0.824, manifest_coverage=1.0 (24/24 sessions), crash_recovery=0.96 (from system-eval.json, 2026-04-25).

---

### Contribution 2: Piston Model — Context-Pressure-Responsive Waves

**Claim:** faerie2 triggers agent spawning based on context fill (pressure gradient), not elapsed time or task completion. W1/W2/W3 waves are physically realized through altimeter gating.

**Evidence:** Documented in CLAUDE.md; operational since 2026-04-23. W1=LIFTOFF (parallel), W2=CRUISE (selective), W3=INSERTION (background).

**Closest prior art:** 2601.08129 uses pressure on shared artifact; faerie2 uses pressure on ORCHESTRATOR'S context — different locus. No surveyed paper uses internal context fill as dispatch signal.

**Gap:** piston score=1.0 but bootstrap_mode=true; wave_history_sessions=0. Metric exists, not yet measured. Paper must acknowledge explicitly.

---

### Contribution 3: Reputation-Aware Stigmergic Dispatch

**Claim:** faerie2 combines agent reputation scoring (composite_score, manifest_truthfulness, belief_index) with stigmergic routing. Agents ≥0.5 receive HIGH/CRITICAL; <0.5 constrained to MED/LOW retraining. Natural selection without central control.

**Evidence:** Reputation schema at config/reputation-schema.json. Agent cards with Last Training scores. Dispatch honors routing_weight in spawn selection. 241 agents in roster as of 2026-04-27.

**Novel combination:** No surveyed paper combines reputation scoring with stigmergic compass navigation as single dispatch mechanism.

**Gap:** model_routing score=0.667; sonnet_w2_rate=NULL. Reputation dispatch implemented but not quantitatively evaluated for impact.

---

### Contribution 4: Typed Compass Bearing Navigation

**Claim:** faerie2 encodes directed investigation structure as typed compass edges (N/S/E/W) on manifest DAG. Agents self-navigate complex multi-phase investigations without central planner. Filesystem IS coordination layer.

**Evidence:** Compass architecture in CLAUDE.md and 3x-EMERGENCE.md. N=unblock prerequisites, S=proceed/conclude, E=parallel validation, W=retreat/reframe. Each bearing carries quality_score + belief_index thresholds as phase gates.

**Novel element:** No surveyed paper uses typed compass bearing semantics. AdaptOrch selects topologies centrally; faerie2 emergent topology arises from agents following local bearing signals. Dead reckoning analogy (position → bearing → movement → observed position → next bearing) not in any surveyed paper.

---

### Contribution 5: Mutation Discipline for Orchestration Substrate

**Claim:** faerie2 applies evolutionary mutation discipline (baseline → mutate → measure → publish) to orchestration substrate, not model weights. Prevents harmful changes and creates compounding system health.

**Evidence:** T=0 baseline locked at forensics/mutation-baselines/ (2026-04-23). Four substrate fixes documented: citation_wiring (0.124→0.891), manifest_metric_validator, empty_probe_validator, wave_gate_retirement (+47% resilience), m6_ignition (coordination_rate 0.0617→0.2159).

**Novel element:** Self-healing ML papers target model adaptation, not orchestration substrate. faerie2 heals coordination primitives themselves.

---

## Part 3 — Suggested Paper Outline

**Proposed Title:** *faerie2: Stigmergic Orchestration with Forensic Coordination — Emergent Multi-Agent Intelligence via Typed Compass Navigation and Context-Pressure-Responsive Dispatch*

**Target Venue:** arXiv cs.MA (Multi-Agent Systems) + AAMAS 2027 or NeurIPS 2026 Agent Workshop

**Abstract (draft):**
Modern LLM agent orchestration concentrates coordination logic in central context, creating a bottleneck. We present faerie2, achieving near-zero main-context overhead (f(0) principle) through: (1) stigmergic compass navigation (agents read/write typed manifest traces without messaging); (2) context-pressure-responsive wave dispatch (piston model — spawning triggered by orchestrator context fill); (3) forensic coordination (COC records emerge as byproduct of manifests). We demonstrate measured improvements from 0.554→0.742 composite score across 24 sessions (356 eval runs), with quality recovering to 0.891 following structured mutation-discipline interventions. We compare against eight recent arXiv papers (2024–2026) and identify five novel contributions.

**Section Outline:**
1. Introduction — Orchestration bottleneck; f(0) as design target
2. Related Work — 8 papers surveyed with clear differentiation per contribution
3. Architecture (3.1–3.5)
   - Stigmergic manifest layer (typed compass, investigation_labels)
   - Piston wave model (W1/W2/W3, context-pressure, altimeter gating)
   - Reputation-aware dispatch (composite_score, manifest_truthfulness, belief_index)
   - Forensic coordination (COC as byproduct, hash-chaining, three-store)
   - Mutation discipline (measure-before-fix, T=0 baseline, substrate fixes)
4. Evaluation (4.1–4.4)
   - Eval framework (6 dimensions, frozen_rubric, 356 runs)
   - Substrate fix results with measurable deltas
   - Honest null disclosures (piston bootstrap_mode, memory=0.0, cost_per_finding=NULL)
   - Limitations (internal eval harness, competitor deltas not externally validated)
5. Novel Contribution Analysis — Per contribution vs closest prior art
6. Risks and Gaps
7. Conclusion + Future Work

---

## Part 4 — Publication Risks and Mitigations

| Risk | Level | Mitigation |
|------|-------|-----------|
| 2601.08129 (Pressure Fields) misinterpreted as prior art | High | Clearly distinguish locus (shared artifact vs orchestrator context); add unique chain (pressure → wave staging → irreversible commit → forensic trace) |
| 2512.10166 validates stigmergy broadly; faerie2 as instance | Medium | Emphasize typed/semantic compass edges vs undirected pheromone trails |
| 2602.20214 (Sovereignty Kernel) concurrent forensics work | Medium | faerie2's structural integration (forensics-as-byproduct) vs bolt-on kernel is clear architectural distinction |
| Internal eval harness not externally benchmarked | High | Explicitly characterize competitor deltas as self-reported; commit to external benchmark protocol for publication submission |
| Piston dimension completely unmeasured (wave_history=0) | High | Either apply measurement protocol before submission, or remove piston from novel contributions and focus on 4 others |

---

## Part 5 — Honest Null Disclosures

These dimensions are unmeasured or have null metrics (as of 2026-04-25 system-eval.json):
- `tasks_per_100k_median` = NULL
- `cost_per_finding_median` = NULL
- `time_to_first_finding_sec_median` = NULL
- `honey_hit_rate` = "establishing" (not a number)
- `nectar_relevance_score` = 0.0 (bootstrap mode, not evidence of failure)
- `wave_history_sessions` = 0 (piston dimension completely unmeasured)
- `sonnet_w2_rate` = NULL
- `competitor_deltas` — self-reported, not externally benchmarked

**Any paper submission MUST include these as explicit limitations.**

---

## Next Actions for Publication

1. **Apply 2510.05174 framework** to faerie2 to measure whether emergence is statistically real (not spurious)
2. **Wire piston dimension** — measure wave_history_sessions, context_pressure_correlation, latency gains per wave
3. **External benchmark protocol** — compare against ChatGPT Memory, Mem0, equivalent tools with same task suite
4. **High-risk paper review** — 2601.08129 most likely reviewer; prepare detailed distinction document
5. **Submit to cs.MA track with agent workshop track** — position as emerging field contribution

---

**Manifest:**
```json
{
  "task_id": "research-faerie2-arxiv-publications",
  "agent": "research-analyst",
  "generated_at": "2026-04-27T21:43:00Z",
  "dashboard_line": "8 papers surveyed; 5 novel contributions identified; 1 high prior-art risk; publication-ready path charted",
  "compass_edge": "S",
  "quality_score": 0.85,
  "belief_index": 0.88,
  "next_task_queued": "Apply 2510.05174 emergence-measurement framework to faerie2 data; wire piston dimension metrics"
}
```

---

**Related docs:**
- [3x-EMERGENCE.md](3x-EMERGENCE.md) — Formal emergence framework with timeline and tipping point hypothesis
- [EMERGENCE-AND-STIGMERGY.md (vault reference)](../../0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED/Hive/EMERGENCE-AND-STIGMERGY.md) — Central CT_VAULT hub linking to this framework

---

**Document Status:** Active | Ready for external benchmark planning
**Last Updated:** 2026-04-27  
**Hash:** sha256:pending
