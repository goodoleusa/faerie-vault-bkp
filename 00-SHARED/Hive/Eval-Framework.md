---
title: Eval Framework — Cumulative System Gains
status: final
created: 2026-03-29
author: data-scientist agent
version: 1.0
tags: [eval, metrics, benchmarking, piston, memory]
doc_hash: sha256:8b588e0dcae42f4ab97e584ded8ae960cad3ebae3a7c19f4d7dbc82eb47f3413
hash_ts: 2026-03-29T16:10:24Z
hash_method: body-sha256-v1
---

# Eval Framework: Measuring Cumulative System Gains

**Pre-registration statement** (written before computing any numbers):
This document specifies the complete measurement methodology for comparing the faerie/hive system against (a) vanilla Claude with no tooling and (b) competitor memory tools (mem0, Letta, ChatGPT Memory). All metrics, baselines, targets, and scoring rubrics are defined here before any evaluation run. No metric may be added, removed, or reframed after data collection begins without a dated amendment logged at the bottom of this document.

---

## Architecture Map (what is being measured)

```
Feature                   → Metric dimension
─────────────────────────────────────────────
Piston wave scheduling    → E. Piston Efficiency
Compound momentum         → E. Piston Efficiency
Lean main (O(1) ingest)   → A. Throughput
Stratospheric subagents   → A. Throughput + E. Piston
Crystallized memory       → B. Memory Effectiveness
Stigmergy (manifest trail)→ C. Resilience
Stream + droplet          → C. Resilience
OTJ learning              → A. Throughput (trend slope)
```

---

## Dimension A: Throughput

### A1 — Tasks Per Session
- **Metric name:** `tasks_per_session`
- **Measurement:** Read `tasks_completed` from `session-metrics.jsonl` (collected by `session_metrics.py`)
- **Collection point:** `session_stop_hook` — already wired
- **Storage:** `~/.claude/hooks/state/session-metrics.jsonl` + aggregated in `system-eval.json`
- **Baseline (vanilla Claude):** 2–4 tasks/session (single-thread, no subagents, no manifest re-use)
- **Target:** ≥8 tasks/session sustained across 5 sessions (2× baseline)
- **Notes:** Trend slope over last 10 sessions is the OTJ learning signal. Must be non-negative.

### A2 — Tasks Per 100K Tokens
- **Metric name:** `tasks_per_100k_tokens`
- **Measurement:** `tasks_completed / (tokens_consumed / 100_000)` — both fields in `session-metrics.jsonl`
- **Collection point:** Stop hook — derived in `eval_harness.py`
- **Storage:** `system-eval.json`
- **Baseline:** ~1.5 tasks/100K (single-thread burns context on full-blob returns)
- **Target:** ≥6 tasks/100K (lean-main O(1) integration gives 4× leverage)
- **Calibration note:** Use median over ≥10 sessions. Mean is skewed by outlier sessions.

### A3 — Cost Per Validated Finding (USD)
- **Metric name:** `cost_per_finding`
- **Measurement:** `cost_usd / findings_produced` — already in `session-metrics.jsonl`
- **Collection point:** Stop hook
- **Storage:** `session-metrics.jsonl`, trend in `system-eval.json`
- **Baseline:** ~$0.45/finding (vanilla Claude Sonnet, ~1 finding per $0.45 session avg)
- **Target:** ≤$0.08/finding (parallel subagents amortize across many findings)
- **Confound:** Only count NECTAR entries with a hypothesis code (H1-H5) or `cat=FINDING`. Raw observation appends do not count.

### A4 — Time to First Finding (seconds)
- **Metric name:** `time_to_first_finding_sec`
- **Measurement:** Timestamp of first NECTAR append minus `generated_at` in `faerie-brief.json`
- **Collection point:** NEW — requires NECTAR append hook writing `first_append_ts` to `~/.claude/hooks/state/nectar-timing.json` per session
- **Storage:** `nectar-timing.json` + aggregated in `system-eval.json`
- **Baseline:** ~600s (vanilla Claude, linear work before first finding)
- **Target:** ≤120s (Wave 0 fast agents return within 2 minutes)

---

## Dimension B: Memory Effectiveness

### B1 — HONEY Hit Rate
- **Metric name:** `honey_hit_rate`
- **Measurement:** Per session: count `cat=DECISION` MEM blocks in scratch that contain the word "HONEY" (citation proxy) divided by total DECISION-type MEM blocks.
  - `grep -c "HONEY" scratch-{SID}.md` / `grep -c "cat=DECISION" scratch-{SID}.md`
  - This is an approximation. True auditing requires agent reasoning — flag for monthly human spot-check.
- **Collection point:** `scratch_collector.py` at session end + `eval_harness.py` aggregation
- **Storage:** `system-eval.json` → `memory.honey_hit_rate`
- **Baseline:** 0% (vanilla Claude has no HONEY)
- **Target:** ≥40% of DECISION-type MEM blocks cite HONEY context

### B2 — NECTAR Tail-30 Relevance
- **Metric name:** `nectar_relevance_score`
- **Measurement:** % of sessions where a NECTAR `recent_observations` entry from `faerie-brief.json` generated a task that was subsequently completed that same session.
  - Proxy: cross-reference `faerie-brief.json → recent_observations[].summary` keywords with `sprint-queue.json` tasks completed in same session.
- **Collection point:** `faerie-brief.json` vs `session-metrics.jsonl` comparison
- **Storage:** `system-eval.json` → `memory.nectar_relevance`
- **Baseline:** 0 (no NECTAR equivalent in vanilla Claude)
- **Target:** ≥60% of sessions have ≥1 NECTAR observation converted to completed task

### B3 — Cross-Session Continuity
- **Metric name:** `cross_session_continuity`
- **Measurement:** For each NECTAR finding tagged with session ID N, does any session after N+2 reference that finding's task ID or finding hash in its scratch or stream files?
  - `eval_harness.py --cross-session-audit` scans NECTAR for session-tagged entries, then searches scratch-* and streams/*.jsonl for those IDs in later sessions.
- **Collection point:** On-demand audit, run weekly or pre-publication
- **Storage:** `system-eval.json` → `memory.cross_session_continuity`
- **Baseline:** 0% (vanilla Claude, no session linkage)
- **Target:** ≥30% of NECTAR findings referenced again within 5 sessions

### B4 — HONEY Crystallization Pressure
- **Metric name:** `honey_crystallization_pressure_days`
- **Measurement:** Days since last `/crystallize` invocation (from most-recent dated section header in HONEY.md). Alert if > 14 days AND NECTAR has grown > 200 lines since last crystallization.
- **Collection point:** `eval_harness.py` on each run (file stat)
- **Storage:** `system-eval.json` → `memory.crystallization_lag_days`
- **Baseline:** N/A
- **Target:** 7–14 days between events (pressure-driven, not scheduled)
- **Anti-pattern guards:** < 3 days = over-crystallizing; > 21 days = stagnation. Both trigger alerts.

---

## Dimension C: Resilience

### C1 — Manifest Coverage
- **Metric name:** `manifest_coverage_pct`
- **Measurement:** `stages_with_final_manifest / total_expected_stages` per DAE pipeline run. Read from `scripts/audit_results/runs/{RUN_ID}/manifests/`. Expected stage count from `run-benchmarks.json` per `task_type`.
- **Collection point:** `session_stop_hook` or on-demand via `trail_reader.py --list`
- **Storage:** `system-eval.json` → `resilience.manifest_coverage`
- **Baseline:** 0% (vanilla Claude has no manifests — coordination is entirely in-context)
- **Target:** ≥90% coverage on all pipeline runs

### C2 — Stream Completeness
- **Metric name:** `stream_completeness_pct`
- **Measurement:** % of agents in `subagent-roster.json` that have `~/.claude/memory/streams/{task_id}.jsonl` with ≥5 entries.
- **Collection point:** `session_stop_hook` after roster is written; `eval_harness.py` computes
- **Storage:** `system-eval.json` → `resilience.stream_completeness`
- **Baseline:** 0%
- **Target:** ≥80% of agents emit ≥5 stream entries

### C3 — Crash Recovery Rate
- **Metric name:** `crash_recovery_rate`
- **Measurement:** When `/faerie` detects an in-flight agent from prior session (via `agent_state.json` or `piston-checkpoint.json`), was the session resumed without human relay? Score 1/0 per event. Write `resume_outcome` to `piston-checkpoint.json`.
- **Collection point:** `/faerie` startup hook — NEW field required in `piston-checkpoint.json`
- **Storage:** `system-eval.json` → `resilience.crash_recovery_rate`
- **Baseline:** 0% (vanilla Claude loses all state on disconnect)
- **Target:** ≥85% of crash scenarios resume autonomously

### C4 — Trail Read Success
- **Metric name:** `trail_read_success_rate`
- **Measurement:** % of `trail_reader.py --resume` calls returning valid `next_stage` (exit 0, non-empty). Log each call to `~/.claude/hooks/state/trail-read-log.jsonl`.
- **Collection point:** Wrapper around `trail_reader.py` calls in pipeline scripts
- **Storage:** `trail-read-log.jsonl` + aggregated in `system-eval.json`
- **Baseline:** N/A
- **Target:** ≥95% (failures = pipeline schema drift or corrupt manifests)

---

## Dimension D: Output Quality vs Baselines

### D1 — Finding Depth Score
- **Metric name:** `finding_depth_score`
- **Measurement:** Human-scored rubric, 0–10. Applied to random sample of 3 findings per week. Scored by human investigator, NOT self-assessed.
  - 0–2: Superficial restatement of input
  - 3–4: Single-source synthesis
  - 5–6: Multi-source synthesis with conflict resolution
  - 7–8: Novel cross-session connection + evidence chain
  - 9–10: Falsifiable hypothesis + distinguishing evidence named
- **Collection point:** Weekly human review of REVIEW-INBOX.md sample
- **Storage:** `system-eval.json` → `quality.finding_depth` (rolling avg of last 9 sampled)
- **Baseline (vanilla Claude):** 4.5 (single-session, no cross-reference, no hypotheses)
- **Target:** ≥7.0
- **Competitor estimates:** mem0 ~5.0, Letta ~5.5, ChatGPT Memory ~4.0

### D2 — Citation Accuracy
- **Metric name:** `citation_accuracy_rate`
- **Measurement:** % of NECTAR findings with ≥1 traceable source (task ID, stream file path, or manifest hash). Non-traceable = finding added without provenance.
  - Each NECTAR entry should carry `session_id` + one of: `stream_ref`, `manifest_ref`, `task_id`.
- **Collection point:** `scratch_collector.py` / `memory_bridge.py --collect-streams` at handoff
- **Storage:** `system-eval.json` → `quality.citation_accuracy`
- **Baseline:** ~20% (vanilla Claude occasionally cites session content, no hash chain)
- **Target:** ≥95%

### D3 — Cross-Session Recall (Binary)
- **Metric name:** `cross_session_recall_pass_rate`
- **Measurement:** Standardized Task 1 (Section 5). Run monthly. Score: 1 if system recalls a finding from ≥3 sessions ago with correct attribution; 0 otherwise.
- **Collection point:** Monthly benchmark run
- **Storage:** `run-benchmarks.json` → append `cross_session_recall` field
- **Baseline:** 0 (vanilla Claude has no cross-session memory)
- **Target:** ≥0.9 pass rate

---

## Dimension E: Piston Efficiency

### E1 — Waves Before First Response
- **Metric name:** `waves_before_first_response`
- **Measurement:** Count of agent waves (0=fast, 1=medium, 2=deep) that completed and returned BEFORE dashboard was shown to user. Source: `piston.py` logs + `surfacing-log.jsonl`.
  - Requires `piston.py` to write `wave_completion_timestamps` and `first_response_ts` to `piston-checkpoint.json`.
- **Collection point:** `piston.py` wave completion handler — NEW fields required
- **Storage:** `piston-checkpoint.json` + `system-eval.json` → `piston.waves_before_first_response`
- **Baseline:** 0 (vanilla Claude is synchronous — response before any work)
- **Target:** ≥1 wave completed before first response

### E2 — Two-Wave Pre-Response Rate
- **Metric name:** `two_wave_pre_response_rate`
- **Measurement:** % of /faerie sessions where ≥2 waves returned before dashboard shown.
- **Collection point:** Derived from `piston-checkpoint.json` session history
- **Storage:** `system-eval.json` → `piston.two_wave_pre_response_rate`
- **Baseline:** 0%
- **Target:** ≥50% of sessions

### E3 — Agents in Flight at First Response
- **Metric name:** `agents_in_flight_at_response`
- **Measurement:** Count of subagents launched but not yet returned at first response time. Higher = more compound momentum.
- **Collection point:** `piston.py` — record `in_flight_count` when dashboard emitted
- **Storage:** `piston-checkpoint.json` + `system-eval.json`
- **Baseline:** 0 (vanilla Claude synchronous)
- **Target:** ≥3 agents in flight at first response

### E4 — Findings Per Wave 1
- **Metric name:** `findings_per_wave1`
- **Measurement:** NECTAR additions + completed tasks attributed to Wave 1 agents (medium-depth: membot, research-analyst, data-scientist). Attribution via `wave` tag in roster entry — requires `piston.py` to tag spawns.
- **Collection point:** `scratch_collector.py` + roster wave tags
- **Storage:** `system-eval.json` → `piston.findings_per_wave1`
- **Baseline:** 0
- **Target:** ≥2 findings from Wave 1 per session

---

## Section 5: Benchmark Methodology — Competitor Comparison

**Ground rules:**
- Same prompt text verbatim across all systems
- Human evaluator blinded to system identity (labeled A/B/C/D)
- Scored within 24h of run (no post-hoc revision)
- All scores logged to `run-benchmarks.json` with timestamp

### Task 1: Cross-Session Recall
**Prompt:** "What was the key infrastructure finding from the investigation work done approximately 3 sessions ago? Include the specific technical detail and the source where it was confirmed."

**Setup:** A confirmed finding must exist in the test dataset ≥3 sessions back with a named source. For faerie: it must be in NECTAR with session ID. Competitors: given the finding verbally in a prior test session.

**Rubric (0–10):**
- 0: No answer or completely wrong
- 1–2: Acknowledges a finding exists, vague category only
- 3–4: Correct general finding, wrong or missing technical detail
- 5–6: Correct finding + detail, no source attribution
- 7–8: Correct finding + detail + named source (URL, file, or task ID)
- 9–10: All above + session reference + confidence qualifier

**Pass threshold:** ≥7. **Expected:** Vanilla 0–1. ChatGPT Memory 3–5. mem0 4–6. Letta 4–6. **Faerie target:** ≥8.

### Task 2: Pipeline Recovery
**Prompt:** "The data ingestion script crashed at stage 3a mid-run. The run ID is [RUN_ID]. What is the exact next step to resume, and what output did stage 3a produce before crashing?"

**Setup:** Synthetic partial run with manifests for stages 1–2, `status: partial` for 3a, stage 3b not started.

**Rubric (0–10):**
- 0: Cannot answer
- 1–2: Generic advice ("re-run the script")
- 3–4: Identifies 3b as next but cannot verify 3a partial output
- 5–6: Reads trail, identifies next stage correctly
- 7–8: Reads partial manifest, reports 3a's partial output, names next stage
- 9–10: All above + exact resume command + names verification step

**Pass threshold:** ≥7. **Expected:** Vanilla 1–2. ChatGPT/mem0/Letta 0–3 (no pipeline integration). **Faerie target:** ≥8.

### Task 3: Synthesis Quality
**Prompt:** "Summarize the 5 most important architectural decisions made in this project this month. For each: the decision, the rationale, and any open questions it left."

**Setup:** ≥5 real decisions must exist in NECTAR/HONEY/scratch with `cat=DECISION` from current month.

**Rubric (0–10):**
- 0: Cannot answer
- 1–2: Generic project description, no specific decisions
- 3–4: Identifies 1–2 real decisions, misses others
- 5–6: Identifies 3–4 real decisions with partial rationale
- 7–8: All 5 correctly identified with accurate rationale
- 9–10: All 5 + open questions named + cross-references between decisions

**Pass threshold:** ≥7. **Expected:** Vanilla 3–4 (current session only). ChatGPT Memory 4–5. mem0/Letta 5–6. **Faerie target:** ≥8.

---

## Section 6: Dashboard Integration

### /faerie Dashboard Line
Add to the 10-line /faerie output after the queue summary:
```
EVAL  composite=0.87 (+34% vs baseline) | mem=0.82 res=0.91 qual=0.79 | trend: improving
```

### Status Footer Extension
Current format: `[{stage} T{N} | {alert} | ctx ~{K}K | cache HIT/MISS | ${cost}/turn | headroom:{H}K]`
New format: `[{stage} T{N} | {alert} | ctx ~{K}K | eval:{score}{arrow} | ${cost}/turn | headroom:{H}K]`
- `{score}` = composite score to 2 decimal places
- `{arrow}` = ↑ (improving), → (flat, ±0.02), ↓ (degrading)
- Read from `system-eval.json` on /faerie launch; cached for session

### Alert Conditions (surface as `{alert}` in statusline)
| Code | Condition |
|------|-----------|
| `HONEY_LAG` | > 14 days since crystallize AND NECTAR grown > 200 lines |
| `STREAM_LOW` | Stream completeness < 60% last session |
| `QUALITY_DIP` | Finding depth score < 5.0 on last weekly sample |
| `COST_HIGH` | cost_per_finding > 3× target ($0.24) |
| `PISTON_FLAT` | waves_before_first_response = 0 in last 3 sessions |

---

## Section 7: Implementation Roadmap

### Already wired (no new work)
- A1, A2, A3: `session_metrics.py` provides raw data
- C1: `trail_reader.py --list` covers manifest coverage
- B1 partial: scratch files exist for grep-based citation check

### Requires new instrumentation (priority order)
1. **eval_harness.py** — the aggregator script (`~/.claude/scripts/eval_harness.py`)
2. **A4** — NECTAR append hook: write `first_append_ts` to `nectar-timing.json` per session
3. **E1–E4** — `piston.py` needs `wave_completion_timestamps`, `first_response_ts`, `in_flight_count` in `piston-checkpoint.json`; roster entries need `wave` tag
4. **C3** — `piston-checkpoint.json` needs `resume_outcome` field on /faerie startup
5. **D3** — Monthly manual benchmark run (standardized prompts, Section 5)

### Collection cadence
```
session_stop:  session_metrics.py → scratch_collector.py → eval_harness.py (write system-eval.json)
/faerie start: eval_harness.py --quick (read system-eval.json → inject statusline + alerts)
weekly:        eval_harness.py --cross-session-audit (B3)
monthly:       eval_harness.py --benchmark (manual human scoring for D1, D3)
```

---

## Section 8: Multi-Issue Defense Score

A benchmark delta alone is a one-dimensional argument. A feature that closes 5 distinct gaps simultaneously is categorically stronger than one that improves a single metric 10%. The defense score captures this second axis of evidence — not a substitute for benchmark scores, but a complement.

### Formula

```
defense_score = benchmark_delta + 0.1 * problems_closed + 0.15 * unexpected_benefits
```

- `benchmark_delta` — composite score improvement over baseline (e.g. +0.34)
- `problems_closed` — count of distinct named problems the feature addresses (be exhaustive; list them)
- `unexpected_benefits` — count of benefits discovered post-deployment that were NOT part of the original design intent

**Interpretation:**
- `defense_score ≥ 1.5` — strong, architecturally fit feature
- `defense_score 0.5–1.5` — solid; justifies complexity
- `defense_score < 0.5` — narrow fix; question whether complexity is warranted

### Reporting Rules
- Same 3-run baseline guard applies — do not report `defense_score` until run 3
- Report alongside composite score in eval output: `composite=0.87 defense=1.62`
- `problems_closed` and `unexpected_benefits` must be named in a comment, not just counted

### Per-Feature Scoring (running ledger)

| Feature | benchmark_delta | problems_closed | unexpected_benefits | defense_score |
|---|---|---|---|---|
| manifest-as-return-value | +0.34 | 6 | 3 | 0.34 + 0.60 + 0.45 = **1.39** |
| stream + droplet | +0.18 | 4 | 1 | 0.18 + 0.40 + 0.15 = **0.73** |
| baseline_established guard | +0.09 | 3 | 2 | 0.09 + 0.30 + 0.30 = **0.69** |

*(Expand as features are evaluated. Scores finalized at run 3.)*

---

## Section 9: Failure-to-Gold Log

Features often start as fixes to specific failures. When a feature also unexpectedly resolves problems that were never part of the original design, that is evidence of deep architectural fitness — it solves unknown problems, not just known ones.

**Rule:** When documenting a feature, ask: *What failure triggered this? What gold came out of it? Did the gold solve anything we didn't anticipate?*

Capture unexpected benefits immediately — they evaporate quickly.

### Log

| Feature | Original Problem | Unexpected Benefits | Discovered |
|---|---|---|---|
| manifest-as-return-value | main context burn on subagent returns | crash recovery, stigmergy self-healing, O(1) integration cost | 2026-03-29 |
| vault_hash_stamp PostToolUse hook | provenance missing from Obsidian | auto-stamps on EVERY write (not batch), forensic integrity continuous | 2026-03-29 |
| baseline_established guard | fake % comparisons on run 1 | hash-chain integrity, proves no cherry-picking of baseline date | 2026-03-29 |

*(Add rows when unexpected benefits are discovered post-deployment.)*

---

## Amendments Log
*(Add entries below if any metric is changed after 2026-03-29)*

| Date | Amendment | Reason | Approved by |
|------|-----------|--------|-------------|
| 2026-03-29 | Added Section 8 (Multi-Issue Defense Score) + Section 9 (Failure-to-Gold Log) | Architectural evaluation principles — defense_score as complement to benchmark delta | human |
