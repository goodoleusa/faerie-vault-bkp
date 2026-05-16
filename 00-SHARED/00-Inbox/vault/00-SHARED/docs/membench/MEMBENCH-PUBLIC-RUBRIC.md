---
doc_id: MEMBENCH-PUBLIC-RUBRIC
version: "1.0"
created: "2026-04-24"
status: active
cites:
  - docs/bundle-evolution-system-design-2026-04-24.md
  - docs/SPAWN-BOILERPLATE.md
  - CLAUDE.md (faerie2)
supersedes: []
tags: [membench, evaluation, rubric, metrics, substrate]
---

# MEMBENCH Public Rubric — Memory System Evaluation

**Navigation:** [INDEX](./MEMBENCH-INDEX.md) | [Public Rubric](./MEMBENCH-PUBLIC-RUBRIC.md) | [Metrics Explanatory](./MEMBENCH-METRICS-EXPLANATORY.md) | [Quick Reference](./MEMBENCH-QUICK-REFERENCE.md) | [Visual Guide](./MEMBENCH-VISUAL-GUIDE.md) | [Strategy](./MEMBENCH-STRATEGY.md)

**Scorecard:** [2026-04-24](../forensics/scorecards/2026-04-24_FAERIE-SCORECARD.md)

---

## 1. What Membench Measures

Membench is the measurement substrate for the faerie2 memory system. It answers one core question:

> Does memory make agents more capable — and by how much?

The benchmark operates across two independent axes:

| Axis | What it scores | Measured how |
|------|---------------|--------------|
| **Substrate quality** | Is the memory corpus healthy, accurate, and usable? | 11 metrics run against HONEY, NECTAR, pollen, and droplets |
| **Agent efficiency** | Do agents with memory complete more work than agents without? | Task-completion rate with memory vs baseline without memory |

These axes are orthogonal. An agent can produce high-quality output (good substrate contributor) while still having a low efficiency ratio if the memory overhead is too expensive. Both must improve together for the platform to benefit from memory at all.

**Baseline (v0.2.0, 2026-04-16):**

```
Composite score: 78.4 / 100
Work efficiency: 15× tasks-per-token above baseline (M3 = 1.31)
Memory overhead: 2.8% of context per turn (net, after savings)
Confabulation:   0%
```

---

## 2. The 11 Metrics

### Core Five (always measured)

**M1 — Retention**

What fraction of facts written to memory are findable in a subsequent session?

- Baseline: 88%
- Measured by: seeded-fact retrieval test (100 representative facts inserted; query in fresh session; count hits)
- Failure signal: M1 < 70% means agents are writing to memory but the corpus is not retaining them

**M2 — Relevance**

What fraction of HONEY content is procedural and applicable to current work (vs historical, overly specific, or outdated)?

- Baseline: 84%
- Measured by: human + LLM audit of HONEY lines; each line scored relevant / neutral / dead weight
- Failure signal: M2 < 75% means HONEY is accumulating noise; crystallization is overdue

**M3 — Work Efficiency**

How many tasks does an agent with memory complete per 100K tokens vs an agent without memory?

- Baseline: 1.31× (31% more tasks completed with memory, per 100K tokens)
- Measured by: A/B task completion comparison across sessions; normalized by token budget
- This is the primary metric. If M3 < 1.0, memory overhead is not compensated; revert
- Target for experimental bundles: M3 ≥ 1.45

**M4 — Overhead**

What percent of total context does memory consume per turn, net of savings from reduced re-explanation?

- Baseline: 2.8% net
- Measured by: token budget consumed by memory reads (HONEY + NECTAR + pollen) minus tokens saved by not re-explaining prior context
- Failure signal: M4 > 10% net means memory is becoming a context drain

**M5 — Continuity**

When auto-compact fires mid-session, what fraction of in-flight tasks resume correctly from checkpoint?

- Baseline: 100%
- Measured by: piston-checkpoint.json recovery tests; wave state verification post-compact
- Failure signal: M5 < 90% means checkpoint recovery is broken; agents lose work at context boundary

### Extended Six (measured when infrastructure is available)

**M6 — Coordination**

What fraction of agent findings from session N are explicitly cited by agents in session N+1?

- Baseline: 34%
- Target (experimental bundle): 60%
- Measured by: `builds_on_refs` + `contradicts_refs` fields in manifests; compared against predecessor manifest outputs
- This is the stigmergic learning metric — do later agents actually benefit from earlier agents?

**M7 — Crystallization Density**

What fraction of HONEY lines are at maximum semantic density (no lossless compression possible)?

- Baseline: 82%
- Measured by: LLM-assisted audit; each line scored on information density vs length
- Failure signal: M7 < 70% means HONEY is verbose; crystallization needed

**M8 — Confabulation Rate**

What fraction of facts in the memory corpus are false or unverifiable?

- Baseline: 0%
- Measured by: adversarial fact-check audit; randomly sample 50 HONEY/NECTAR claims and verify against source
- This is a veto gate. If M8 > 5%, quarantine the memory variant immediately and trigger human review. Zero tolerance for anti-facts in forensic context.

**M9 — Ceiling-Hit Rate**

What fraction of metrics are at or near their practical ceiling (95%+)?

- Baseline: 40% (4–5 of 11 metrics near ceiling)
- Measured by: count of metrics scoring ≥ 95 of maximum
- This tracks whether measurement infrastructure is surfacing useful signal or is saturated

**M10 — Coverage**

What fraction of the 11 metric dimensions are populated with measured values (vs null / not-measured)?

- Baseline: 100%
- Measured by: presence check of all 11 metric fields in membench output
- Failure signal: M10 < 100% means measurement infrastructure has gaps; fix before drawing conclusions

**M11 — Bootstrap Success Rate**

What fraction of agents start successfully with memory loaded, without errors or hangs during startup?

- Baseline: 100%
- Measured by: agent startup logs; count initialization failures attributable to memory read errors
- This is a veto gate. If M11 < 70%, agents crash on memory load; revert the bundle immediately

---

## 3. Scoring Methodology

### Composite Score

The composite score weights the five core metrics:

```
Composite = (M1 × 0.25) + (M3 × 0.30) + (M4_inverted × 0.15) + (M5 × 0.20) + (M8_inverted × 0.10)

Where:
  M4_inverted = 1.0 - min(M4 / 0.20, 1.0)   # overhead near 0 = score 1.0; overhead at 20% = score 0
  M8_inverted = 1.0 - min(M8 / 0.10, 1.0)   # confab 0% = score 1.0; confab ≥ 10% = score 0
```

Scale: 0–100. Baseline 78.4 corresponds to healthy memory with room to optimize.

### Score Bands

| Band | Score | Interpretation |
|------|-------|---------------|
| Excellent | 90–100 | Memory system is a force multiplier; invest in scaling |
| Healthy | 75–90 | Operating well; optimize individual weak metrics |
| Marginal | 60–75 | Memory is breaking even; diagnose root cause |
| Failing | below 60 | Memory overhead outweighs benefit; pause and repair |

### Per-Metric Targets

| Metric | Baseline | Minimum acceptable | Veto threshold |
|--------|----------|-------------------|----------------|
| M1 Retention | 88% | 70% | — |
| M2 Relevance | 84% | 75% | — |
| M3 Efficiency | 1.31× | 1.0× | — |
| M4 Overhead | 2.8% | <10% net | — |
| M5 Continuity | 100% | 90% | — |
| M6 Coordination | 34% | — | — |
| M7 Density | 82% | 70% | — |
| M8 Confabulation | 0% | — | >5% immediate quarantine |
| M9 Ceiling | 40% | — | — |
| M10 Coverage | 100% | 100% | — |
| M11 Bootstrap | 100% | 70% | <70% immediate revert |

---

## 4. Mutation-Specific Metrics

When bundle variants are tested (conservative vs experimental), additional mutation metrics apply on top of the standard 11.

**MDR — Mutation Detection Rate**

How many mutation pairs (conflicting or emergent rule interactions) are detected per 100 instructions?

- Baseline T=0 (2026-04-23): 4.66 pairs per 100 instructions

**MC — Mutation Classification Distribution**

Breakdown of detected mutations into four categories:

| Category | Meaning | T=0 Baseline |
|----------|---------|-------------|
| Beneficial | Enables new capability; keep and promote | 36% |
| Neutral | No measurable effect; harmless | 18% |
| Harmful | Introduces errors or contradictions; fix after T+1 baseline wired | 36% |
| Uncertain | Mixed signals; measure longer before classifying | 9% |

**SR — Shadow Rate**

What fraction of rule citations in agent outputs refer to predecessor artifacts (pollen, manifests, droplets) vs appear to be invented?

- Baseline T=0: 10%
- Soft gate: SR ≥ 10% triggers citation-drift audit; agents may be hallucinating rule provenance

**PR — Preservation Rate**

What fraction of T=0 beneficial mutations survive into T+1 after repair wave?

- Target: ≥ 80%
- This metric cannot be measured until T+1 baseline is wired; never repair harmful mutations before this is measured

**EBI — Emergent Behavior Index**

Fraction of total mutations that produce unplanned multi-metric improvements (improvements beyond what the mutation hypothesis predicted).

- High EBI = the bundle unlocked a structural principle that was not anticipated

**FD — Flag Delay**

Time from first emergence signal in pollen/droplets to classification in the mutation ledger.

- Target: < 1 session (same-session classification)

**CCI — Capability Composition Index**

Fraction of multi-metric improvements attributable to agent interactions (not just individual agent improvement).

- High CCI = the system is producing emergent capability through coordination, not just better individual agents

### Mutation Gates

| Gate | Threshold | Action |
|------|-----------|--------|
| SUBSTRATE_WARN | Harmful% > 15% | Pause evolution; human review required |
| CITATION_DRIFT | SR ≥ 10% | Audit bundle clarity; agents may be confusing bundle rules with invented rules |
| M8_VETO | Confabulation > 5% | Immediate quarantine of bundle variant |
| M11_VETO | Bootstrap < 70% | Immediate revert of bundle variant |

---

## 5. Bundle Variants and Measurement

The bundle evolution framework tests two bundle formulas side-by-side:

**Conservative bundle (baseline):**
- Full HONEY + NECTAR tail-30 + pollen excerpt
- Approximately 4K tokens per agent
- Target: stable M1 = 0.88, M3 = 1.31×, composite = 78.4
- Used by: evidence-curator, report-writer, data-engineer, documentation-engineer

**Experimental bundle (hypothesis):**
- Scoped HONEY + NECTAR tail-50 (tag-filtered) + pollen with siblings + top-5 droplets
- Approximately 9.7K tokens per agent
- Hypothesis: M3 ≥ 1.45 (+11%), M6 ≥ 0.60 (+76%), M1 acceptable at 0.78 (−10%)
- Used by: knowledge-synthesizer, python-pro, memory-keeper, workflow-orchestrator

**Routing:** Conservative is the default and fallback. Experimental is capability-gated. Forensic agents (evidence-curator, security-auditor, coc-manager, membot) are locked to conservative regardless of caller argument.

### How to Compare Bundle Variants

After a session with both variants deployed:

```bash
# Run membench breakdown by bundle variant
python3 scripts/eval_membench.py --session {SID} --breakdown-by-bundle

# Measure mutation metrics specifically
python3 scripts/9x_mutation_analyzer.py --session {SID} \
  --output forensics/mutations/MUTATIONS-CLASSIFICATION-SESSION_{SID8}.jsonl

# Validate T=0 preservation before evolving to T+1
python3 scripts/9x_bundle_preservation_validator.py \
  --baseline T=0 \
  --session {SID} \
  --threshold 0.80 \
  --output forensics/mutations/preservation-report-{SID8}.jsonl
```

---

## 6. How Agents Contribute to the Substrate

Every agent run affects membench scores. The contribution mechanisms:

**M1 Retention (what you write to memory):**
- Write precise, citable MEM blocks to pollen during work
- Emit findings via `9x_memory_bridge.py --stream` — these feed NECTAR at /handoff
- Avoid overwriting; append-only writes preserve the full signal for retrieval

**M3 Efficiency (how you spend tokens):**
- Read memory before doing investigative work (prior findings prevent re-investigation)
- Reference NECTAR entries in your manifest (`nectar_references` field)
- Each re-solved problem is a waste of M3 budget

**M6 Coordination (how you cite predecessors):**
- Include `builds_on_refs` and `contradicts_refs` in every manifest
- Cite the predecessor manifest path or task_id explicitly
- Droplets from parallel agents are meant to be read at task boundaries — read them

**M8 Confabulation (what you claim):**
- Every finding must cite its source (file path, manifest, database, prior agent run)
- Do not speculate in streams without marking the observation as unverified hypothesis
- Clean corpus is forensically admissible; anti-facts destroy it

**M5 Continuity (how you checkpoint):**
- Write manifest progressively (status: in-progress → draft → final)
- Include `context_remaining` estimate in manifests when approaching limits
- This enables piston-checkpoint.json to recover accurately after auto-compact

**M11 Bootstrap (how you initialize):**
- If memory load fails at startup, emit a bootstrap_failure flag in your manifest
- Do not silently proceed without memory if bundle injection fails
- Failure visibility enables infrastructure repair before it becomes a trend

---

## 7. Measurement Schedule and Evolution Protocol

**Phase 1 (current):** Archive T=0 baselines; wire measurement infrastructure; run conservative bundle as ground truth.

**Phase 2:** Deploy both bundle variants; measure M3/M6 delta; classify mutations.

**Phase 3:** Calculate T+1 Preservation Rate; generate evolved bundles:
- conservative-v1.1 = conservative-v1.0 with harmful mutations pruned
- experimental-v1.1 = experimental-v1.0 with beneficial mutations integrated
- hybrid-v1.0 = conservative core + experimental methods (new variant)

**Phase 4+:** Quarterly evolution cycles; compound beneficial mutations; retire harmful mutations.

**Non-negotiable constraint:** Measure T=0 before repairing harmful mutations. The T+1 Preservation Rate cannot be computed if harmful mutations are fixed before the baseline is established. Audit → Measure → Pause → Fix → Measure again → Publish.

### Emergence Classification

When a bundle mutation produces improvements beyond what the hypothesis predicted:

| Signal | Classification | Action |
|--------|---------------|--------|
| M3 up + M1 up + M6 up | BENEFICIAL_EMERGENT | Adopt broadly; promote to conservative-v2.0 |
| M3 up + M1 stable | BENEFICIAL_FOCUSED | Keep for exploratory tasks; monitor M1 drift |
| M3 stable + no regression | NEUTRAL | Optional; no harm in keeping |
| M1 down more than 15% | HARMFUL | Quarantine; archive as lesson |
| M8 above 5% | HARMFUL_VETO | Immediate rollback; human review |
| M3 up + M1 down (trade-off) | UNCERTAIN | Measure longer; calculate true ROI |

**The heuristic for emergent benefit:** if a mutation improves metrics that were not in its hypothesis, ask what structural principle it unlocked. Name that principle; add it to HONEY. The unplanned benefit reveals a deeper pattern than the planned benefit.

---

## Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-04-24 | documentation-engineer (task-D1-rubric) | Initial authoring per plan v2 Sections 1–7 |

**Source documents:** bundle-evolution-system-design-2026-04-24.md (plan v2), SPAWN-BOILERPLATE.md (membench context section), CLAUDE.md baselines.

**Hash:** `doc_hash: sha256:pending`
