---
title: "Membench Metric Encyclopedia"
version: "v0.2.0+mutation"
date: "2026-04-25"
status: "canonical"
supersedes: "none"
cites:
  - "MEMBENCH-METRICS-EXPLANATORY.md"
  - "MEMBENCH-PUBLIC-RUBRIC.md"
  - "MEMBENCH-MUTATION-METRICS-PROPOSAL.md"
  - "scripts/3x_eval_membench.py"
  - "scripts/3x_eval_mutation.py"
doc_hash: "sha256:pending"
---

# Membench Metric Encyclopedia

**Navigation:** [INDEX](./MEMBENCH-INDEX.md) | [Explanatory](./MEMBENCH-METRICS-EXPLANATORY.md) | [Quick Reference](./MEMBENCH-QUICK-REFERENCE.md) | [Strategy](./MEMBENCH-STRATEGY.md) | [Visual Guide](./MEMBENCH-VISUAL-GUIDE.md)

**Purpose:** Single-source-of-truth reference for every membench metric. One entry per metric. Canonical definition, formula, measurement protocol, data sources, veto/gate rules, and known interaction effects. Use this when building a new probe, implementing a new eval harness, or resolving a metric definition dispute.

**Scope:** M1–M11 (memory system, v0.2.0 composite) + MDR/MC/EBI/FD/PR/SR/CCI (mutation/substrate, v0.3 proposal). Both families are catalogued here; mutation family is marked PROPOSAL until wired into eval_harness.

---

## Part I — Memory System Metrics (M1–M11)

### Composite Formula

```
composite_v0.2 = (M1×0.25 + M2×0.20 + M3_v0.2×0.30 + (100−M4)×0.10 + M5×0.15) × M10

Veto gates (applied before composite is published):
  M8 > 5.0  → composite = INVALID (confabulation; all downstream findings suspect)
  M11 < 0.70 → composite = INVALID (bootstrap failure; session data untrustworthy)
```

M3_v0.2 applies an estimate-quality penalty:
```
M3_v0.2 = M3_raw × (0.5 + 0.5 × M3_is_estimate_subscore)
  direct measurement  → subscore = 1.0 (no penalty)
  estimate from logs  → subscore = 0.75 (conservative)
  guess               → subscore = 0.50 (very conservative)
```

**Composite interpretation:**

| Range | Grade | Meaning |
|-------|-------|---------|
| 90–100 | Excellent | Memory compounds; agents rarely re-derive facts |
| 70–90 | Healthy | System works; optimization opportunities exist |
| 50–70 | Functional | Debt accumulated; improvement needed |
| < 50 | Critical | System failing; investigate before next spawn wave |

---

### M1 — Retention

**Symbol:** M1  
**Composite weight:** 25%  
**Unit:** percent (0–100)  
**Class:** Core (required for composite)  
**v0.2 baseline:** 88%

**Definition:** The fraction of probe-set facts that are findable in the active memory corpus (HONEY + NECTAR tail + loaded rules). Measures whether facts written in prior sessions survive and remain retrievable.

**Formula:**
```
M1 = (Σ probe_score_i / Σ probe_weight_i) × 100

where probe_score_i =
  probe_weight_i       if ALL keywords present (full hit)
  0.4 × probe_weight_i if ≥1 keyword present (partial hit)
  0                    otherwise
```

**Measurement protocol:**
1. Load probe set from `~/.claude/hooks/state/membench-probes.json`
2. Read corpus: HONEY.md + NECTAR.md tail-500 lines + all rules/*.md files
3. For each probe, keyword-search the corpus (case-insensitive substring match)
4. Score each probe; sum; normalize to 100

**Data sources:**
- `~/.claude/HONEY.md`
- `~/.claude/NECTAR.md` (tail-500 lines; configurable)
- `~/.claude/rules/core/*.md`, `~/.claude/rules/sauce/*.md`
- `~/.claude/hooks/state/membench-probes.json` (probe set)

**Probe set format:**
```json
{
  "probes": [
    {
      "id": "P001",
      "claim": "training-queue was dark for 36 days before restoration",
      "keywords": ["training-queue", "36 days", "dark"],
      "anti_fact": ["training-queue active every day"],
      "weight": 10
    }
  ]
}
```

**Thresholds:**

| Score | Status | Action |
|-------|--------|--------|
| > 80% | Healthy | No action; monitor |
| 70–80% | Warning | Review recent NECTAR archival; check HONEY crystallization |
| < 70% | Risk | Facts are evaporating; audit deletion/archival events |

**Interaction effects:**
- Falls after aggressive HONEY crystallization (less text = fewer keyword matches); if M2/M3 rise simultaneously, trade-off is healthy
- Falls if NECTAR tail window is shortened; not an architecture failure
- If M1 falls AND M3 falls, genuine memory loss

---

### M2 — Relevance

**Symbol:** M2  
**Composite weight:** 20%  
**Unit:** percent (0–100)  
**Class:** Core  
**v0.2 baseline:** 84%

**Definition:** The fraction of HONEY facts that are procedural (actionable) rather than narrative (contextual-only). Measures whether memory guides agent decisions or merely describes past events.

**Formula:**
```
M2 = (actionable_fact_count / total_fact_count) × 100

actionable fact: line that starts with an imperative verb, ALWAYS/NEVER/DO/DON'T,
                 or encodes a decision rule (if-then shape)
narrative fact:  observation, historical note, or contextual description
```

**Measurement protocol:**
1. Load HONEY.md; strip comment lines, blank lines, headings
2. For each content line, classify actionable vs narrative using heuristic regex
3. Score = (actionable / total) × 100

**Data sources:**
- `~/.claude/HONEY.md`
- `{repo}/.claude/HONEY.md` (project scope)

**Thresholds:**

| Score | Status | Action |
|-------|--------|--------|
| > 85% | Excellent | HONEY is a decision rulebook |
| 70–85% | Acceptable | Some narrative acceptable; monitor |
| < 70% | Risk | HONEY is telling stories; crystallize into rules |

**Interaction effects:**
- Falls when narrative findings from NECTAR are promoted to HONEY without distillation
- Rises after `/crystallize` run (converts narrative entries to procedural rules)
- Does NOT affect composite via M1 (different corpus and different scoring dimension)

---

### M3 — Work Efficiency

**Symbol:** M3  
**Composite weight:** 30% (highest weight)  
**Unit:** ratio (1.0 = break-even; >1.0 = memory provides positive ROI)  
**Class:** Core; primary optimization target  
**v0.2 baseline:** 1.31

**Definition:** The ratio of effective task completion with memory enabled vs without memory, per-token. Values above 1.0 mean memory is earning its token cost. Below 1.0 means memory is slowing agents down.

**Formula:**
```
M3_raw = tasks_completed_with_memory / tasks_completed_without_memory
         (normalized by token budget used in each condition)

M3_v0.2 = M3_raw × (0.5 + 0.5 × M3_is_estimate_subscore)

M3_is_estimate_subscore:
  1.0  — measured directly from session logs (concrete task counts)
  0.75 — estimated from indirect signals (e.g. stream logs, partial data)
  0.5  — guessed (no direct measurement available)
```

**Measurement protocol:**
1. Read `session-metrics.jsonl` for current session: tasks_completed, tokens_used, blockers_resolved
2. Read `eval-history.jsonl` for baseline (last 5 sessions without memory reads as control group, or configurable no-memory baseline)
3. Compute ratio; apply estimate penalty

**Data sources:**
- `~/.claude/hooks/state/session-metrics.jsonl`
- `~/.claude/hooks/state/eval-history.jsonl`
- Wave result manifests (`wave*-result.json`)
- Piston checkpoint (`piston-checkpoint.json`)

**Known ROI data point:** Early empirical measurement shows 11:1 ROI on memory tokens — for every 100 agents spawned with memory, ~11 redundant spawns are avoided because downstream agents find prior findings instead of re-deriving them. Net overhead: 2.8% of context.

**Thresholds:**

| Score | Status | Action |
|-------|--------|--------|
| > 1.5 | Excellent | Memory compounding; agents save 50%+ rework |
| 1.1–1.5 | Healthy | Memory is net-positive |
| 1.0–1.1 | Marginal | Memory barely paying its cost; diagnose M4 first |
| < 1.0 | Risk | Memory is slowing agents; audit overhead |

**Veto consideration:** M3 < 1.0 does not trigger a veto gate but is the highest-priority optimization signal. A confirmed M3 < 1.0 warrants disabling memory reads for the next session as a diagnostic.

**Interaction effects:**
- Positively correlated with M1 (can't reuse facts you can't find) and M6 (coordination means facts ARE being used)
- Negatively correlated with M4 (high overhead eats into efficiency)
- M3 is the only metric tied directly to business outcome; all other metrics are means to improving M3

---

### M4 — Overhead

**Symbol:** M4  
**Composite weight:** 10% (inverted: score = 100 − overhead_pct)  
**Unit:** percent of total session tokens consumed by memory loads  
**Class:** Core  
**v0.2 baseline:** 2.8% overhead → M4 score = 97.2

**Definition:** The fraction of total session token budget consumed by reading memory files (HONEY, NECTAR, rules) minus the token savings from avoided re-explanations.

**Formula:**
```
gross_overhead_pct = (memory_tokens_loaded / total_session_tokens) × 100
savings_pct        = (re_explanation_tokens_avoided / total_session_tokens) × 100
net_overhead_pct   = gross_overhead_pct − savings_pct

M4_score = 100 − net_overhead_pct   (higher is better; less overhead = better score)
```

**Measurement protocol:**
1. Read session token counts from `session-metrics.jsonl`
2. Identify memory-load events (Read tool calls on HONEY/NECTAR/rules files)
3. Estimate re-explanation savings: count agent runs that cited prior NECTAR findings vs ran from scratch
4. Compute net overhead; invert to score

**Data sources:**
- `~/.claude/hooks/state/session-metrics.jsonl`
- Tool call logs (Read tool events with HONEY/NECTAR paths)

**Thresholds:**

| Overhead % | M4 Score | Status |
|------------|----------|--------|
| < 3% | > 97 | Lean; memory is cheap |
| 3–5% | 95–97 | Acceptable |
| 5–10% | 90–95 | Marginal; audit HONEY size |
| > 10% | < 90 | Bloated; crystallize/archive |
| > 15% | < 85 | Critical; memory outweighs benefit |

**Interaction effects:**
- Rises as HONEY grows (HONEY is loaded every turn; budget: ≤5K tokens)
- Rises as rules/sauce files multiply and are loaded on startup
- Reduces when NECTAR tail window is shortened (fewer lines loaded)

---

### M5 — Continuity

**Symbol:** M5  
**Composite weight:** 15%  
**Unit:** percent (0–100)  
**Class:** Core; safety gate at < 80%  
**v0.2 baseline:** 100%

**Definition:** The fraction of memory checkpoints that survive auto-compact, agent crashes, and session restarts. Tests whether the memory system is reliable across context boundaries.

**Formula:**
```
M5 = (checkpoints_recovered / checkpoints_written) × 100

A checkpoint is "recovered" if:
  (a) piston-checkpoint.json is readable post-compact with expected fields present
  (b) the NECTAR marker written before compact is findable after compact
```

**Measurement protocol:**
1. Before each auto-compact: write timestamp marker to NECTAR + snapshot piston-checkpoint.json to forensics
2. After compact resumes: search for marker in NECTAR; verify piston-checkpoint.json fields intact
3. Score = (successful verifications / total checkpoints in session)

**Data sources:**
- `~/.claude/hooks/state/piston-checkpoint.json`
- `~/.claude/NECTAR.md`
- `{repo}/forensics/checkpoints/` (archived snapshots)

**Thresholds:**

| Score | Status | Action |
|-------|--------|--------|
| 100% | Excellent | Memory is fully resilient |
| 95–99% | Healthy | Minor data loss; investigate specific checkpoint |
| 80–95% | Warning | Auto-compact safety uncertain; monitor |
| < 80% | Risk | Memory is unreliable across compacts; review architecture |

**Interaction effects:**
- If M5 falls, M1 (Retention) will typically follow — lost checkpoints = lost facts
- git-tracked NECTAR is the insurance policy; if NECTAR is gitignored, M5 < 100% becomes permanent risk

---

### M6 — Coordination

**Symbol:** M6  
**Composite weight:** 0% (observational only — not in composite formula)  
**Unit:** percent (0–100)  
**Class:** Diagnostic; tracked for trend visibility  
**v0.2 baseline:** 34%

**Definition:** The fraction of unique findings in the corpus that have been cited by at least one subsequent agent (either built upon or contradicted). Measures actual cross-agent memory leverage.

**Formula:**
```
M6 = (cited_findings / total_unique_findings) × 100

cited_finding: any finding in NECTAR where a subsequent agent manifest or
               pollen block contains a "builds_on" or "contradicts" reference to it
```

**Measurement protocol:**
1. Parse NECTAR entries; extract finding identifiers (timestamps, session IDs, fact claims)
2. Scan agent manifests and pollen files for cross-references
3. Score = (findings with ≥1 citation / total findings)

**Data sources:**
- `~/.claude/NECTAR.md`
- `{repo}/forensics/manifests/*.json`
- `{repo}/.claude/memory/pollen-*.md`

**Note on zero weight:** M6 has zero composite weight because it is difficult to measure reliably in automated fashion (cross-references require natural language matching). It is tracked as an observational metric to signal whether the memory system is actually being used for cross-agent compounding.

**Thresholds:**

| Score | Status | Interpretation |
|-------|--------|----------------|
| > 30% | Good | Agents are discovering and using prior findings |
| 10–30% | Marginal | Some coordination; spawn prompts should explicitly request NECTAR checks |
| < 10% | Poor | Agents are siloed; memory exists but isn't being leveraged |

---

### M7 — Crystallization

**Symbol:** M7  
**Composite weight:** 0% (lagging indicator — observational)  
**Unit:** score 0–100 (inverse of lines-per-fact)  
**Class:** Diagnostic; lagging indicator  
**v0.2 baseline:** 82%

**Definition:** A measure of HONEY density. High scores indicate that facts are tightly expressed (few lines per insight). Low scores indicate verbose HONEY that carries the same information in more tokens.

**Formula:**
```
lines_per_fact = total_content_lines_in_HONEY / distinct_fact_count
M7 = min(100, 100 / lines_per_fact)

A "distinct fact" is a non-blank, non-heading, non-comment HONEY line that
encodes a unique decision rule, method, or principle.
```

**Measurement protocol:**
1. Load HONEY.md; strip blanks, headings, comments
2. Count distinct content lines as facts
3. Compute lines-per-fact; invert to score

**Data sources:**
- `~/.claude/HONEY.md`
- `{repo}/.claude/HONEY.md`

**Thresholds:**

| Score | Status | Action |
|-------|--------|--------|
| > 80 | Dense | HONEY is well-crystallized |
| 60–80 | Acceptable | Some verbosity; watch for trend |
| < 60 | Bloated | Schedule `/crystallize`; HONEY needs compression |

**Why lagging:** Crystallization effects take 3–5 sessions to appear in M3 (the ROI metric). Schedule M7 as a leading indicator for future M3 degradation — if M7 falls while M3 holds, budget for crystallization in next sprint.

---

### M8 — Confabulation Rate

**Symbol:** M8  
**Composite weight:** Veto gate (does not enter composite numerically)  
**Unit:** percent of probes where anti_facts are present (0 = clean; > 5 = VETO)  
**Class:** Safety gate; hard veto  
**v0.2 baseline:** 0.0%

**Definition:** The fraction of memory probes where the probe's anti-fact (a known-false claim) appears in the active corpus. A non-zero M8 indicates the memory system contains contradictory or false information.

**Formula:**
```
M8 = (probes_with_antifact_match / total_probes) × 100

For each probe:
  if any string in probe.anti_fact appears in corpus → confabulation detected
```

**Measurement protocol:**
1. Load probe set; extract `anti_fact` arrays
2. Search active corpus (HONEY + NECTAR + rules) for each anti-fact string
3. Count probes where any anti-fact string is found
4. Score = (count / total_probes) × 100

**Veto rule:**
```
if M8 > 5.0:
  composite = INVALID
  status = "CONFABULATION — do not use session findings for training"
  action = quarantine_session + rollback_to_last_clean_commit
```

**Amber/red zones:**

| Rate | Status | Action |
|------|--------|--------|
| 0–2% | Green | Normal noise; monitor |
| 2–5% | Amber | Minor hallucination risk; audit recent NECTAR entries |
| > 5% | Red | VETO — block spawning; quarantine session |

**Why this matters for forensic work:** False facts in agent memory poison training, evaluation, and any downstream findings. At 0% confabulation rate (v0.2 baseline), the memory system is forensically clean — an important property when memory artifacts are chain-of-custody evidence.

---

### M9 — Ceiling-Hit

**Symbol:** M9  
**Composite weight:** 0% (meta-metric; diagnostic only)  
**Unit:** percent of metrics scoring ≥ 99  
**Class:** Diagnostic  
**v0.2 baseline:** 40% (4–5 metrics near-perfect)

**Definition:** The fraction of composite-weighted metrics (M1–M5 plus M10/M11) that score at or near the ceiling (≥ 99). A high ceiling-hit percentage signals diminishing optimization returns; a low one identifies the most under-developed dimensions.

**Formula:**
```
M9 = (count(metrics where score ≥ 99) / count(all_scored_metrics)) × 100
```

**Primary use:** Effort allocation. When M9 is 80%+, most subsystems are mature and further optimization has low ROI. When M9 is < 20%, multiple subsystems need investment simultaneously. The most actionable use of M9 is to invert it: look at which metrics are NOT at ceiling to find bottlenecks.

---

### M10 — Instruction Coverage

**Symbol:** M10  
**Composite weight:** Multiplier on composite (0–1.0 scale)  
**Unit:** percent of 11 dimensions with populated inputs (used as multiplier: 100% = 1.0, 82% = 0.82)  
**Class:** Measurement integrity multiplier  
**v0.2 baseline:** 100% (→ multiplier = 1.0)

**Definition:** The fraction of the 11 membench input dimensions that have populated, readable data. Applied as a multiplier to penalize composite scores from incomplete measurement setups.

**Formula:**
```
M10 = (populated_dimensions / 11) × 100
composite_final = composite_unweighted × (M10 / 100)
```

**The 11 dimensions:**

| # | Dimension | Data source |
|---|-----------|-------------|
| 1 | HONEY.md exists | `~/.claude/HONEY.md` |
| 2 | NECTAR.md exists | `~/.claude/NECTAR.md` |
| 3 | Rules populated | `~/.claude/rules/core/*.md` |
| 4 | Probe set exists | `~/.claude/hooks/state/membench-probes.json` |
| 5 | Session metrics captured | `session-metrics.jsonl` |
| 6 | Agent state logs | `agent_state.json` |
| 7 | Piston checkpoint | `piston-checkpoint.json` |
| 8 | Stream logs | `memory/streams/` |
| 9 | Eval history | `eval-history.jsonl` |
| 10 | Stigmergy tracker active | `9x_stigmergy_tracker.py` reachable |
| 11 | Bootstrap metrics | Bootstrap manifests in session |

**Rationale:** A composite score of 85 from only 6 of 11 dimensions instrumented is not the same as an 85 from full instrumentation. M10 enforces measurement completeness before publishing composite scores.

---

### M11 — Bootstrap Exit

**Symbol:** M11  
**Composite weight:** Veto gate (does not enter composite numerically)  
**Unit:** fraction of spawned agents that reached first tool call (0.0–1.0; veto < 0.70)  
**Class:** Safety gate; hard veto  
**v0.2 baseline:** 100% (1.0)

**Definition:** The fraction of agents that successfully completed their startup sequence and reached at least one tool call (Read or Bash). Agents that crash during memory loading (e.g., due to HONEY corruption or missing dependency) count as bootstrap failures.

**Formula:**
```
M11 = agents_reached_first_tool_call / total_agents_spawned

Veto rule:
  if M11 < 0.70:
    composite = INVALID
    status = "BOOTSTRAP_FAILURE — memory corruption suspected"
    action = quarantine_session + rollback_memory_to_last_clean_state
```

**Measurement protocol:**
1. Count agents spawned (from agent-runs.jsonl or session-metrics.jsonl)
2. For each agent, check whether a Read or Bash tool call appears in its trace
3. Score = successful_bootstraps / total_spawned

**Thresholds:**

| Score | Status | Action |
|-------|--------|--------|
| 1.0 | Excellent | No startup failures |
| 0.90–1.0 | Acceptable | Occasional failure; investigate specific crash |
| 0.70–0.90 | Warning | Multiple crashes; memory architecture risk |
| < 0.70 | VETO | Session invalid; block all spawning; rollback |

---

## Part II — Mutation / Substrate Metrics (v0.3 Proposal)

**Status:** Proposal — not yet wired into eval_harness. Implementation spec in `scripts/3x_eval_mutation.py`. All metrics in this family measure the *instruction substrate* (rules, hooks, scripts), not the memory layer. They are reported as a parallel scoreline distinct from the composite.

**Why a separate family:** M1–M11 measure whether memory stores and retrieves facts correctly. The mutation family measures whether the *instruction set itself* is self-consistent. Both matter; mixing them in one composite obscures which layer is failing.

---

### MDR — Mutation Detection Rate

**Symbol:** MDR  
**Unit:** conflicting pairs per 100 active instructions  
**Scoreline:** Reported separately, not in composite  
**v0.2 baseline (T=0, 2026-04-23):** 4.66

**Definition:** Number of conflicting or overlapping instruction pairs per 100 active instructions. An instruction pair is *conflicting* if both are reachable at runtime, operate on the same observable (file path, hook event, env var), and their behaviors diverge.

**Formula:**
```
MDR = (count(conflicting_pairs) / count(active_instructions)) × 100

active instruction = (a) cited in settings.json hooks OR
                     (b) referenced in rules/*.md by absolute path OR
                     (c) committed within last 30 days
```

**Soft gate:** No hard veto; MDR ≥ 10 should trigger an audit sprint.

---

### MC — Mutation Classification

**Symbol:** MC  
**Unit:** % breakdown across four classes  
**v0.2 baseline (T=0):** 36% Beneficial / 18% Neutral / 36% Harmful / 9% Uncertain

**Definition:** For each mutation pair detected by MDR, classification into one of four classes:

| Class | Definition |
|-------|-----------|
| BENEFICIAL | Enables emergent capability: redundant path that gracefully degrades, layered safety net |
| NEUTRAL | Harmless drift: duplicate docs, near-identical copies with no runtime divergence |
| HARMFUL | Causes conflict: contradictory guidance, racing hooks, silent shadowing |
| UNCERTAIN | Novel combination; outcome requires empirical observation to classify |

**Critical constraint:** Repair HARMFUL mutations only after measuring baseline. Fixing all conflicts before T=0 measurement destroys the ability to track T+1 Preservation Rate (beneficial mutations accidentally removed during "cleanup").

---

### EBI — Emergent Behavior Index

**Symbol:** EBI  
**Unit:** count of confirmed beneficial interactions emerging from mutation pairs  
**v0.2 baseline (T=0):** TBD (insufficient observation window)

**Definition:** The count of system behaviors that emerged from classified-BENEFICIAL mutation pairs and were confirmed by ≥2 sessions of observation. Tracks the system's ability to evolve through benign conflict.

---

### FD — Flag Delay

**Symbol:** FD  
**Unit:** median hours from mutation introduction to detection  
**v0.2 baseline (T=0):** TBD

**Definition:** Median time between when a conflicting instruction is introduced (git commit timestamp) and when it is detected by MDR measurement or hook audit. Lower is better.

---

### PR — Preservation Rate

**Symbol:** PR  
**Unit:** percent (0–100)  
**v0.2 baseline (T=0):** TBD (requires T+1 measurement)

**Definition:** Fraction of BENEFICIAL mutations that survive repair waves targeting HARMFUL mutations. Measures whether cleanup operations are surgical (preserving benefit) or blunt (destroying benefit along with harm).

**Formula:**
```
PR = (beneficial_mutations_retained_post_repair / beneficial_mutations_pre_repair) × 100
```

**Measurement note:** PR requires at least two measurement points (T=0 pre-repair baseline, T+1 post-repair). Measuring PR is the primary reason the mutation baseline must be locked before any repair work begins.

---

### SR — Shadow Rate

**Symbol:** SR  
**Unit:** percent (0–100)  
**Soft gate:** SR ≥ 10% fires CITATION-DRIFT alert  
**v0.2 baseline (T=0):** 10%

**Definition:** The fraction of rule file citations that point to pre-evolution (ancestor) script versions rather than the current tier-prefixed canonical version. A high SR means agents are following old instructions.

**Formula:**
```
SR = (citations_pointing_to_stale_path / total_rule_citations) × 100

A citation is "stale" if the referenced path does not match the current canonical
tier-prefixed filename (e.g., rule references "eval_harness.py" but canonical is
"3x_eval_harness.py").
```

**Action at SR ≥ 10%:** Fix is a rule-line edit updating the citation to the tier-prefixed evolved variant. NOT a script rename.

---

### CCI — Capability Composition Index

**Symbol:** CCI  
**Unit:** count of emergent capabilities confirmed from ≥2 BENEFICIAL mutation pairs  
**v0.2 baseline (T=0):** TBD

**Definition:** A count of distinct capabilities that exist only because two or more instruction sources interact beneficially. Tracks the compounding value of instruction composition over time. The goal is a rising CCI alongside stable/falling MDR (more capability emerging from fewer conflicts).

---

## Part III — Cross-Metric Reference

### Metric Interaction Map

| If this metric falls... | First check... | Because... |
|------------------------|---------------|-----------|
| M1 Retention | M5 Continuity | Lost checkpoints = lost facts |
| M1 Retention | Recent NECTAR archival | Active corpus shrinks |
| M2 Relevance | HONEY crystallization logs | New narrative entries added without distillation |
| M3 Efficiency | M4 Overhead | High overhead eats efficiency |
| M3 Efficiency | M6 Coordination | Low coordination = facts not being reused |
| M4 Overhead | HONEY size (wc -c) | HONEY loaded every turn |
| M5 Continuity | NECTAR git status | NECTAR gitignored = no recovery path |
| M8 Confabulation | Recent NECTAR entries | Agent wrote contradictory claim |
| M11 Bootstrap | Memory load errors | HONEY syntax error or missing dependency |
| MDR | Recent commits | New scripts introduced without REPLACES declaration |
| SR | Rule files citation audit | Rules updated without updating citations |

### Metric Priority Order (optimization)

When multiple metrics are below threshold, address in this order:

1. **M8 > 5%** — VETO; fix before anything else
2. **M11 < 0.70** — VETO; fix before anything else
3. **M3 < 1.0** — Primary ROI signal; memory is net-negative
4. **M5 < 90%** — Continuity risk; may corrupt future measurements
5. **M1 < 70%** — Retention gap; M3 cannot improve without M1
6. **M2 < 70%** — Relevance gap; HONEY needs crystallization
7. **M4 > 10%** — Overhead too high; archive and compress
8. **MDR > 10** — Substrate conflicts; audit sprint needed
9. **SR ≥ 10%** — CITATION-DRIFT; update rule citations

### Baselines Summary (v0.2.0, 2026-04-21)

| Metric | Baseline | Weight | Gate |
|--------|----------|--------|------|
| M1 Retention | 88% | 25% | Warn < 70% |
| M2 Relevance | 84% | 20% | Warn < 70% |
| M3 Work Efficiency | 1.31× | 30% | Warn < 1.0 |
| M4 Overhead | 2.8% (score 97.2) | 10% | Warn > 10% overhead |
| M5 Continuity | 100% | 15% | Warn < 80% |
| M6 Coordination | 34% | 0% (obs.) | — |
| M7 Crystallization | 82% | 0% (obs.) | — |
| M8 Confabulation | 0.0% | Veto gate | VETO > 5% |
| M9 Ceiling-Hit | 40% | 0% (meta) | — |
| M10 Instr. Coverage | 100% | Multiplier | — |
| M11 Bootstrap Exit | 100% | Veto gate | VETO < 70% |
| MDR | 4.66 | Substrate | Alert ≥ 10 |
| MC | 36/18/36/9 B/N/H/U | Substrate | — |
| SR | 10% | Substrate | Alert ≥ 10% |
| **Composite (v0.2)** | **78.4** | — | **Critical < 50** |

---

## Part IV — Implementation Reference

### Running membench

```bash
# Full membench run (all M1–M11 + composite):
python3 scripts/eval/eval_harness.py --membench --session $CLAUDE_SESSION_ID

# Mutation metrics (MDR, MC, SR):
python3 scripts/3x_eval_mutation.py --check-all

# Quick composite check:
python3 scripts/9x_lean_query.py --get-all | grep composite

# Trend (last 5 sessions):
jq '.[] | {ts, composite: .membench.composite}' \
  ~/.claude/hooks/state/eval-history.jsonl | tail -5
```

### Script locations

| Script | Purpose | Tier |
|--------|---------|------|
| `scripts/3x_eval_membench.py` | M1–M11 computation | 3 (analysis) |
| `scripts/3x_eval_mutation.py` | MDR/MC/SR computation | 3 (analysis) |
| `scripts/eval/eval_harness.py` | Orchestrator; writes eval-history.jsonl | 3 |
| `scripts/9x_wb_membench_log.py` | wandb logging for membench runs | 9 (utilities) |
| `scripts/9x_lean_query.py` | Fast statusline query | 9 (utilities) |

### Output schema (eval-history.jsonl entry)

```json
{
  "ts": "2026-04-25T00:01:23Z",
  "session_id": "...",
  "membench": {
    "M1_retention": 92.5,
    "M2_relevance": 78.0,
    "M3_work_efficiency": 1.31,
    "M3_is_estimate_subscore": 1.0,
    "M4_overhead_pct": 2.8,
    "M5_continuity": 100.0,
    "M6_coordination": 34.0,
    "M7_crystallization": 82.0,
    "M8_confabulation_pct": 0.0,
    "M9_ceiling_hit_pct": 40.0,
    "M10_instruction_coverage": 100.0,
    "M11_bootstrap_exit": 1.0,
    "composite_v0_2": 78.4,
    "composite_naive": 77.1,
    "verdict": "PASS"
  },
  "mutation": {
    "MDR": 4.66,
    "MC": {"beneficial": 36, "neutral": 18, "harmful": 36, "uncertain": 9},
    "SR": 10.0
  }
}
```

---

**Document version:** v0.2.0+mutation | **Date:** 2026-04-25 | **Status:** Canonical reference  
**Next review:** Quarterly (2026-07-25) — retire probes scoring 100%; add harder ones; update baselines
