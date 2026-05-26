---
title: swarmy cycle positions — prefix map + proposed blackboard partition
date: 2026-05-26
mission: swarmy.cycle.gates
bearing: W
status: crystallized
source_repos:
  - faerie2 (scripts/_NUMBERING.md, scripts/_INDEX.md, LIFECYCLE.md)
  - swarmy-ui (server/scripts/)
  - swarmy-ui (.agents/skills/blackboard/SKILL.md)
---

# swarmy Cycle Positions: Prefix Map + Proposed Blackboard Partition

> W-bearing re-seat. Don't compose — discover.
> Sources read in order: LIFECYCLE.md → scripts/_NUMBERING.md → _INDEX.md → swarmy-ui/server/scripts/.

---

## Part A: Cycle Position Map

The prefix numbering scheme (introduced 2026-05-23, commit roundup-w1::script-renumber-maker-j)
encodes **where a script lives in the pipeline**. The letter suffix within a cluster encodes
**causal order within that stage**.

| Prefix | Declared Theme | Actual Cycle Stage | Load-bearing Scripts | One-line Semantic | MISPLACED? |
|--------|---------------|-------------------|---------------------|------------------|------------|
| `0x_`  | Bootstrap / shared utilities | Pre-session: one-time setup, lib stubs, path resolution | `0b_path_utils.py` | Shared infrastructure that every other script imports; no lifecycle coupling | No |
| `1x_`  | Manifest pipeline (COC spine) | Session: write → promote → finalize | `1a_manifest_writer.py`, `1b_manifest_loader.py`, `1c_promote_to_forensics.py`, `1d_coc_finalize.py`, `1e_coc_write.py`, `1f_coc_preallocate.py`, `1g_coc_core.py`, `1h_coc_sidecar.py`, `1i_coc_vault_tracker.py`, `1j_reject_manifest.py`, `1k_rebuild_manifest_index.py`, `1l_validate_manifest_index.py` | The atomic lifecycle of every manifest from write → COC seal; `ls 1*.py` = pipeline in reading order | No |
| `2x_`  | Spawn / dispatch | Session: pre-spawn pressure check → executor → frontier discovery | `2a_spawn_pressure.py`, `2b_spawn_executor.py`, `2d_frontier_scanner_indexed.py`, `2e_discovery_frontier_cache.py`, `2f_frontier_precompute.py`, `2g_loop_prevention.py` | Gating and executing agent spawns; pressure calculator feeds executor; frontier cache feeds bundle injection | `2g_loop_prevention.py` — docstring header reads "1x Loop Prevention"; stuck-detector is a session-guard more than a spawn mechanic; could sit at 9x (runtime gate) |
| `3x_`  | Audit / eval / membench | Post-session / continuous: measure emergence, run evals, promote KB | `3a_emergence_metrics.py`, `3b_eval_baseline_runner.py`, `3c_eval_dimensions.py`, `3d_eval_faerie2_runner.py`, `3e_faerie_steer.py`, `3f_membench_probes.py`, `3g_kb_promote.py`, `3h_summarizer_agent.py`, `3i_dev_eval.py`, `3j_eval_ab.py`, `3k_membench_scorer.py`, `3l_wandb_audit.py`, `3m_debug_sweep.py` | Everything that measures, scores, and surfaces how well the system is working | `3e_faerie_steer.py` — fires at UserPromptSubmit as a steering command presenter; that is a runtime/session hook behaviour closer to 9x. `3g_kb_promote.py` and `3h_summarizer_agent.py` — KB promotion and compression are vault-sync operations; they fit 6x (sync/index) more naturally than eval/audit |
| `4x_`  | Charter / mission lifecycle | Session: charter creation → genesis → crystallization → vault edges | `4a_charter.py`, `4b_charter_genesis.py`, `4c_genesis.py`, `4d_genesis_recurse.py`, `4e_charter_term_index.py`, `4f_charter_neighbors.py`, `4g_charter_hash_generator.py`, `4h_charter_lifecycle.py`, `4i_crystallize_docs.py`, `4j_coc_append_doc_crystallization.py`, `4k_vault_status.py`, `4l_populate_vault_edges_from_manifests.py`, `4x_charter_aggregator.py` | Full lifecycle of a charter from creation to crystallized vault artefact | `4k_vault_status.py` — returns markdown vault-state summaries for chat queries; that is a dashboard/query function → belongs at 6x (sync/dashboard). `4i_crystallize_docs.py` — mass-crystallize docs/ is a vault operation; could be 6x. Both are borderline (charter-adjacent enough to stay at 4x, but their query pattern matches 6x) |
| `5x_`  | Backup / baseline / reputation | Cross-session: mutation baselines, release bundles, signing, reputation ledger | `5a_mutation_baseline_capture.py`, `5b_mutation_measure_post.py`, `5c_retroactive_anchor_promotion.py`, `5d_build_release_bundles.py`, `5e_agent_sign.py`, `5f_init_reputation.py`, `5g_reputation_tracker.py`, `5h_claim_sidecar.py` | Immutable record-keeping that survives individual sessions: baselines, bundles, signatures, reputation | No |
| `6x_`  | Sync / dashboard / index | Cross-session / operational: mirrors, routers, dashboards, index rebuilds | `6a_vault_sync.py`, `6b_cob_sync.py`, `6c_inbox_router.py`, `6d_dashboard.py`, `6e_forensics_index.py`, `6f_fresh_scripts_index.py`, `6g_frontier_index.py`, `6h_async_drops.py`, `6i_econoday.py`, `6j_mission_graph_to_excalidraw.py`, `6k_rotate_mcp_token.sh` | Everything that surfaces state for humans or operators; async drops as dead-drop inter-session sync | `6h_async_drops.py` — dead-drop communication between sessions is a coordination layer, arguably closer to 2x (spawn/dispatch domain). Borderline: current home readable because "async" mirrors "sync" cluster |
| `8x_`  | Validators | CI / hook invocation: static checks on frontmatter, citability, COC path protection | `8a_citability_validator.py`, `8b_frontmatter_validator_hook.py`, `8c_protect_coc_paths.py` | Invoked from hooks or CI; fail loudly on bad structure — do not mutate | No |
| `9x_`  | Runtime gates / enforcers | PreToolUse / PostToolUse: block writes before they happen | `9a_manifest_index_enforcer.py`, `9b_vault_gate.py`, `9c_script_gate.py`; plus unnumbered one-offs (`9x_spawn_brief_audit.py`, `9x_manifest_signer.py`, `9x_manifest_verifier.py`, `9x_altimeter_writer.py`, etc.) | True hot-path blockers: abort the tool call if invariant violated | `9x_spawn_brief_audit.py` — audits spawn briefs for free_choice contamination; this is validation of **inputs to spawn** = should be 2x (spawn discipline) or 8x (validator). Spawn-brief validation is upstream of any agent existing, not a runtime gate on a live session |

---

## Part B: Top MISPLACED Prefix Flags (Top 3)

### Flag 1 — `9x_spawn_brief_audit.py` should be `8x_`

**Current:** `9x_` (runtime gates / enforcers)
**Should be:** `8x_` (validators — static checks invoked from hooks or CI)

**Reason:** The script detects spawn briefs that pre-fill `free_choice`. Spawn briefs exist before any agent is spawned — this is a pre-spawn static lint, not a live session gate on a running tool call. The 9x contract is "PreToolUse / PostToolUse hooks that block writes." A spawn-brief lint is invoked before or during spawn construction, which maps to 8x (validator) or 2x (spawn discipline). It does not gate an active tool call against a live session invariant.

**Impact:** Minor — no functional breakage, but `ls 9x*` gives the wrong mental model (developer reads "gate" when they mean "static validator").

---

### Flag 2 — `2g_loop_prevention.py` should be `9x_`

**Current:** `2x_` (spawn / dispatch)
**Should be:** `9x_` (runtime gates / enforcers)

**Reason:** The script is a stuck-detector that wraps OpenHands SDK `action_count_max` / `no_output_timeout`. That is session-level runtime enforcement — it fires during a running conversation to abort loops. It is not a spawn mechanic (it does not calculate pressure, does not scan frontiers, does not execute spawns). Its docstring header even says "1x Loop Prevention" (mistyped — should read "9x"), suggesting it was written with a runtime-gate concept in mind and ended up in 2x by mistake.

**Impact:** Moderate — developer scanning 2x cluster for spawn infrastructure encounters a runtime stuck-detector unexpectedly.

---

### Flag 3 — `3e_faerie_steer.py` should be `9x_`

**Current:** `3x_` (audit / eval / membench)
**Should be:** `9x_` or a new `7x_` session-control cluster

**Reason:** `faerie_steer.py` fires at `UserPromptSubmit` as a live steering command presenter (`/steer`, `/compact`, `/anchor-commit`, `/status`). It is a **runtime hook**, not an eval or audit script. The 3x cluster is measurement: metrics, eval runners, membench, KB promotion. A UserPromptSubmit hook that presents interactive steering options belongs with the runtime enforcement layer (9x) or would justify its own 7x "session control" cluster if steering scripts accumulate.

**Impact:** Meaningful — developers scanning 3x for eval infrastructure encounter a session steering hook that fires on every user prompt, which is operationally different in cadence and purpose.

---

## Part C: Proposed Blackboard Partition (v3)

### Background

**v1:** date-walled flat folders (`swarm/{YYYY-MM-DD}/`)
**v2 (current, shipped):** `chart/` + `{agent_id}/` + `manifests/` inside each date-bucket — dead-reckoning nav model, no wave partitioning.

The operator question: should the `swarm/` path tree be **re-partitioned to mirror actual lifecycle gates** rather than date-buckets as the outermost dimension?

---

### What the real gates are (from LIFECYCLE.md + _NUMBERING.md)

The swarmy lifecycle has **five discrete gates** where state transitions with explicit semantics:

| Gate | Name | What crosses it | Script cluster responsible |
|------|------|-----------------|---------------------------|
| G0 | **Pre-session** | Bootstrap, shared libs load, path resolution | `0x_` |
| G1 | **Spawn** | Brief validated → agent alive | `2x_` + `8x_` (spawn-brief validate) |
| G2 | **In-flight** | Agent navigating, emitting nav.jsons, writing scratch | `1x_` (manifest write), `blackboard chart/` |
| G3 | **Cap** | Agent seals → manifest promoted from scratch to `manifests/` | `1a_manifest_writer.py` (cap promotion) |
| G4 | **Crystallize** | Charter acknowledges cap → COC sealed, vault-synced, reputation updated | `4x_` (charter), `5x_` (baseline/rep), `6x_` (vault sync) |
| G5 | **Measure** | Cross-session eval, emergence metrics, mutation capture | `3x_` (audit/eval), `5a/5b` (mutation baseline) |

---

### v3 proposed directory layout

```
swarm/                                    ← REPO/swarm/ root
│
├─ {YYYY-MM-DD}/                          ← date is STILL outermost (forensic anchor)
│  │
│  ├─ chart/                              ← G2: in-flight navigation ledger (unchanged)
│  │  └─ {ISO8601Z}__{agent_id}__nav.json
│  │
│  ├─ capping/                            ← G3: agent work ready for cap, not yet sealed
│  │  └─ {agent_id}/                      ← agent's crystallized work pending cap
│  │     └─ {task_id}-crystallized.md     (renamed from just scratch; state is explicit)
│  │
│  ├─ manifests/                          ← G3→G4 boundary: capped + signed (unchanged)
│  │  └─ {YYYYMMDD}T{HHMMSS}Z__manifest__{mission}__{agent}.json
│  │
│  └─ {agent_id}/                         ← G2: scratch substrate (spray→tighten only)
│     ├─ {task_id}-scratch.py
│     └─ {task_id}-draft.md
│
├─ active/                                ← G1–G2: registry of currently live agents
│  └─ {agent_id}.json                     (lightweight: initial_bearing, initial_position, spawned_at)
│
├─ sealed/                                ← G4: charter-acknowledged artefacts (cross-date)
│  └─ {charter_id}/
│     └─ {YYYYMMDD}T{HHMMSS}Z__manifest__{mission}__{agent}.json  (symlink from manifests/)
│
└─ coc.jsonl                              ← immutable hash-chain (unchanged)
```

### Key design decisions in v3

**1. Date stays outermost** — The date-bucket is the forensic anchor. The SKILL.md rule "date is ALWAYS outermost. No exceptions." is preserved. This is not wave partitioning.

**2. Replace `next/active/complete` (wave-model) with gate-state names** — The v2 proposal used wave vocabulary. v3 uses actual gate names from the lifecycle:
- `active/` = G1 registry (agents currently live)
- `chart/` = G2 (in-flight navigation — already correct in v2)
- `capping/` = G3 staging area (agent work ready for cap but not yet sealed by manifest_writer)
- `manifests/` = G3→G4 boundary (capped + signed — already correct)
- `sealed/` = G4 cross-date index (charter-acknowledged, cross-date)

**3. The `capping/` zone** — v2 collapses G2 scratch and G3 pre-cap work into the same `{agent_id}/` scratch. This makes it hard to tell whether a file is "still being tightened" or "ready for cap." Introducing `capping/` as an explicit gate-state lets agents signal "I am crystallized, waiting for `1a_manifest_writer.py` to promote me" without ambiguity.

**4. No wave partitioning in the path tree** — Wave identity (`W1/W2/W3`) is piston-state, not filesystem-state. It belongs in the nav.json payload, not in directory names. Using wave names as path segments would break sisters across wave boundaries from sharing the same chart/.

**5. `sealed/` as a cross-date lens** — A charter's acknowledged work spans multiple days. `sealed/` provides the charter-scoped view without duplicating content (symlinks to date-bucket originals). This mirrors how `forensics/manifests/{date}/` and `canonical/` relate in faerie2.

---

### Migration delta (v2 → v3)

| v2 path | v3 path | Change |
|---------|---------|--------|
| `swarm/{date}/chart/` | `swarm/{date}/chart/` | Unchanged |
| `swarm/{date}/{agent_id}/` | `swarm/{date}/{agent_id}/` | Unchanged (scratch only) |
| `swarm/{date}/manifests/` | `swarm/{date}/manifests/` | Unchanged |
| *(none)* | `swarm/{date}/capping/{agent_id}/` | New: explicit G3 staging zone |
| *(none)* | `swarm/active/{agent_id}.json` | New: G1 live-agent registry (cross-date) |
| *(none)* | `swarm/sealed/{charter_id}/` | New: G4 charter-scoped cross-date lens |

The minimal viable step to adopt v3 is: implement `swarm/active/` for G1 registration (adds visibility into live agents without changing anything else). `capping/` and `sealed/` can follow in subsequent sprints.

---

### Source of truth cross-reference

This document is the source-of-truth for cycle-gate names used in blackboard partition naming.
Partition names in `swarmy-ui/.agents/skills/blackboard/SKILL.md` should cite this doc
when referencing gate stages (G0–G5) or their corresponding directory names.

Path: `faerie-vault/00-Publications/coordination/2026-05-26-swarmy-cycle-positions.md`
Mission: `swarmy.cycle.gates`
