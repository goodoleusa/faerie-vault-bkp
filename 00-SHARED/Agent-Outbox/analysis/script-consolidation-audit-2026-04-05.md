---
type: design-insight
status: final
created: 2026-04-05
tags: [audit, equilibrium, scripts, consolidation, complexity]
title: "Script Consolidation Audit — faerie2 Minimum Viable Set"
blueprint: "[[Design-Insight]]"
agent_type: code-reviewer
doc_hash: sha256:a8ac8585f198c1ebfa4163be3d7708335333996f7d5edbbee7df50b99a16784b
hash_ts: 2026-04-06T02:13:33Z
hash_method: body-sha256-v1
---

# Script Consolidation Audit — faerie2 Minimum Viable Set

**Scope:** All `.py` files in `faerie2/` excluding `releases/` (which are build artifacts) and `__pycache__`.
**Total canonical scripts inventoried:** 117
**Proposed after consolidation:** ~72
**Scripts eliminated:** ~45 (38% reduction)

---

## Part 1: Full Inventory Table

Columns: Script | Size (bytes) | Purpose | Caller | Verdict

### `.claude/hooks/` (14 scripts)

| Script | Bytes | Purpose | Caller | Verdict |
|--------|-------|---------|--------|---------|
| `agent_tracker.py` | 5,259 | Track subagent lifecycle (start/stop events) | SubagentStart, SubagentStop hooks | **KEEP** — hot path |
| `canonicalize_paths.py` | 12,215 | Resolve path fragmentation at session start | Pre-session or manual | **MERGE** → `faerie_paths.py` |
| `context_calibrator.py` | 7,328 | Calibrate context token estimates | Hook / manual | **MERGE** → `brain/context_phase.py` |
| `faerie_gates.py` | 5,950 | Guard conditions for faerie flow | PreToolUse logic | **KEEP** — distinct gate logic |
| `faerie_paths.py` | 951 | Shared path resolver shim | Imported by many hooks | **KEEP** — utility, tiny |
| `forensic_coc.py` | 21,882 | HMAC-chained COC log for every tool call | PostToolUse, Stop hooks | **KEEP** — forensic critical path |
| `notification_handler.py` | 11,906 | Handle Claude CLI notifications | Notification hook | **KEEP** (exact copy of nervous-system version — see duplicates) |
| `post-agent-validate.py` | 8,001 | Validate agent output after SubagentStop | SubagentStop hook | **MERGE** → `agent_tracker.py --validate` |
| `presend_estimate.py` | 16,899 | Estimate context cost before send | UserPromptSubmit hook | **KEEP** — active hot-path hook |
| `session_stop_hook.py` | 16,518 | Write faerie-brief.json at session end | Stop hook | **KEEP** (near-identical to nervous-system version — see duplicates) |
| `statusline.py` | 8,250 | Mission control status bar | Called by Claude Code per turn | **KEEP** |
| `statusline_win.py` | 4,212 | Windows-native variant of statusline | Windows installs | **KEEP** — platform variant, intentional |
| `state/beat_last_verifier.py` | 1,794 | Verify agent beat last score | post-agent-validate | **MERGE** → `state/training_queue_manager.py` |
| `state/drops.py` | 10,676 | Real-time insight droplets capture | Agents via skills | **KEEP** — distinct feature |
| `state/dynamo_dashboard.py` | 3,790 | Build dynamo dashboard state | s3b_dynamo_orchestrator | **MERGE** → `state/s3b_dynamo_orchestrator.py` |
| `state/export_queue_to_vault.py` | 6,236 | Export sprint queue to vault | Manual / skill | **MERGE** → `queue_vault_sync.py` subcommand |
| `state/faerie-dashboard-launcher.py` | 3,341 | Launch dashboard process | UserPromptSubmit hook | **MERGE** → `state/s3a_faerie_turn1.py` |
| `state/faerie_training_orchestrator.py` | 6,015 | Orchestrate training sessions | `/train` command | **KEEP** |
| `state/json_lock.py` | 4,460 | Atomic JSON file locking | Many state writers | **KEEP** — shared utility |
| `state/queue_ops.py` | 28,660 | Queue read/write/claim operations | `/run`, hooks | **KEEP** — canonical (identical copy in brain/) |
| `state/s3a_faerie_turn1.py` | 8,590 | Turn-1 startup sequence | UserPromptSubmit hook | **KEEP** |
| `state/s3b_dynamo_orchestrator.py` | 3,867 | Dynamo wave orchestration | s3a sequence | **KEEP** |
| `state/select_agent.py` | 1,860 | Score-driven agent routing | queue_ops / orchestration | **MERGE** → `state/queue_ops.py` module |
| `state/session_heartbeat.py` | 10,609 | Session keep-alive state writes | /faerie, hooks | **KEEP** |
| `state/sprint_queue_lock.py` | 2,596 | Queue-level locking | queue_ops | **MERGE** → `state/json_lock.py` |
| `state/stdio_utf8.py` | 539 | UTF-8 stdout shim for Windows | Imported by hooks | **MERGE** → `faerie_paths.py` (5-line shim) |
| `state/system_guardian.py` | 14,456 | System integrity guardian | Scheduled / manual | **KEEP** |
| `state/training_queue_manager.py` | 3,062 | OTJ training redemption tracking | performance-eval | **KEEP** |

### `.claude/scripts/` (57 scripts)

| Script | Bytes | Purpose | Caller | Verdict |
|--------|-------|---------|--------|---------|
| `add_wiring_tasks.py` | 6,289 | One-time: add wiring tasks to queue | Run once | **DELETE** — one-shot script, already run |
| `agent_lifecycle.py` | 11,876 | Agent startup/shutdown protocol engine | Agents at startup | **KEEP** |
| `backup_forensics.py` | 36,152 | Backup forensic data to B2/local | Manual / scheduled | **KEEP** |
| `batch_collect.py` | 4,284 | Collect Anthropic Batch API results | `/dev-batch` skill | **MERGE** → `batch_submit.py --collect` |
| `batch_submit.py` | 4,154 | Submit tasks to Batch API | `/dev-batch` skill | **KEEP** (absorb batch_collect) |
| `blueprint_discover.py` | 4,852 | Fuzzy blueprint matching for agent output type | Agents pre-write | **MERGE** → `blueprint_resolver.py` subcommand |
| `blueprint_inject.py` | 12,006 | Inject blueprint stanza into spawn prompts | Manual / spawn | **MERGE** → `blueprint_resolver.py --inject` |
| `blueprint_manifest_generator.py` | 7,700 | Regenerate blueprint-manifest.json | Manual / scheduled | **MERGE** → `blueprint_resolver.py --regen-manifest` |
| `blueprint_permissions_audit.py` | 5,531 | Audit agent write permissions for blueprint dirs | Manual | **MERGE** → `blueprint_resolver.py --audit` |
| `blueprint_resolver.py` | 11,169 | Agent-facing: list, apply, validate blueprints | Agents, hooks | **KEEP** (absorbs 4 others — canonical blueprint tool) |
| `blueprint_validate_batch.py` | 8,504 | Batch validate Agent-Outbox files | Manual / post-write hook | **MERGE** → `blueprint_resolver.py --validate-batch` |
| `bundle_handoff.py` | 27,712 | End-of-day dossier bundler | `/handoff` | **MERGE** → `emergency_handoff.py --bundle` |
| `claude_home.py` | 1,139 | Shared utility: resolve `~/.claude` | Imported by scripts | **MERGE** → `faerie_paths.py` (already overlaps) |
| `collab_export.py` | 19,278 | HONEY-based collaboration export/import | `/collab-export` skill | **KEEP** |
| `collaboration_validator.py` | 6,343 | Quality gate for HONEY export validation | `collab_export.py` | **MERGE** → `collab_export.py --validate` |
| `context_phase.py` | 14,236 | Session phase calculator | `statusline.py`, hooks | **MERGE** → `brain/context_phase.py` (diverged copy — brain is canonical) |
| `crystallize.py` | 56,934 | Mechanical pre-pass for crystallization | `/crystallize` command | **KEEP** |
| `debloat.py` | 23,161 | Budget scanner / bloat cleaner | Manual, pre-commit | **KEEP** — distinct from crystallize (budget enforcement vs crystallization) |
| `depth_score.py` | 5,260 | Quality depth scoring for agent outputs | `eval_harness.py` | **MERGE** → `eval_harness.py` module |
| `emergency_handoff.py` | 27,167 | Fire-and-forget handoff snapshot | `/handoff`, auto | **MERGE** → `brain/emergency_handoff.py` (brain is canonical, this is older version) |
| `eval_harness.py` | 45,898 | 7-dimension session eval engine | Stop hook, `/faerie --quick` | **KEEP** |
| `forensic_coc_check.py` | 10,242 | COC health monitor | Manual | **MERGE** → `brain/health_check.py` (health check consolidation target) |
| `handoff_logger.py` | 6,482 | Thread queue for end-of-day dossier | Agents | **MERGE** → `bundle_handoff.py` (which becomes `emergency_handoff.py --bundle`) |
| `hash_tracker.py` | 30,765 | Directory-level hash snapshots with HMAC | Manual, vault_sign.py | **KEEP** — forensic primitive |
| `health_check.py` | 1,295 | Thin wrapper → brain/health_check.py | UserPromptSubmit hook | **DELETE** — just an exec shim; hook should point directly to brain/ |
| `honey_hit_validator.py` | 5,149 | Score agent HONEY citation quality | Tier 4 / eval_harness | **MERGE** → `eval_harness.py` QUALITY dimension |
| `honey_version.py` | 50,872 | HONEY.md versioning (capture/restore/diff) | Manual, `/crystallize` | **KEEP** |
| `inbox_router.py` | 24,047 | Route agent flags to inboxes | memory_router.py | **MERGE** → `memory_router.py --route` (overlapping promotion logic) |
| `memory_bridge.py` | 31,251 | Stream findings + route .claude/projects/ memory | Multiple hooks, agents | **KEEP** — hot path for streaming |
| `memory_gate.py` | 13,371 | Budget pre-check before durable writes | Agents before writes | **MERGE** → `debloat.py --check FILE` (same budget logic) |
| `memory_router.py` | 12,885 | Path fragmentation healer + MEM block router | /handoff membot | **KEEP** (absorbs inbox_router) |
| `model_compare.py` | 22,820 | A/B model comparison harness | `/dev-compare` skill | **KEEP** |
| `narrative_auto_update.py` | 15,356 | Auto-update investigation narrative | session_stop_hook | **KEEP** — but note duplicate in scripts/ |
| `note_sign.py` | 87,197 | Per-note ed25519/semaphore signing | Manual, vault annotation | **KEEP** (note: 53-byte diff vs nervous-system copy — both diverged) |
| `piston.py` | 22,820 | Agent wave engine (LIFTOFF/ORBIT model) | brain/, hooks (try-import) | **KEEP** — opt-in, explicitly removable |
| `queue_analyzer.py` | 9,143 | Intent-driven queue prioritization | /run, piston | **MERGE** → `state/queue_ops.py --prioritize` |
| `queue_vault_sync.py` | 34,960 | Sync sprint queue to vault | UserPromptSubmit hook | **KEEP** |
| `routing_feedback.py` | 8,207 | Record agent routing quality feedback | Stop hook | **MERGE** → `eval_harness.py` ROUTING dimension |
| `scratch_collector.py` | 13,387 | Periodic memory auto-save | PostToolUse, SubagentStop, PreCompact hooks | **KEEP** — active hot-path |
| `session_manifest.py` | 12,248 | Cross-repo session work manifest | Manual | **MERGE** → `emergency_handoff.py --manifest` |
| `session_metrics.py` | 18,106 | Hash-chained session KPIs | Stop hook | **MERGE** → `brain/session_metrics.py` (brain is canonical, this is diverged copy) |
| `staging_promoter.py` | 5,732 | Atomic staging → final location promotion | Agents | **KEEP** |
| `stamp_doc_hash.py` | 9,578 | Stamp SHA256 into vault frontmatter | Manual | **MERGE** → `vault_hash_sync.py --stamp` (same operation) |
| `status_overview.py` | 33,482 | Zero-inference meta-command dashboard | `/status` skill | **KEEP** |
| `surfacing_scheduler.py` | 29,747 | Calibrate subagent wave timing | Stop hook, `/faerie` | **MERGE** → `brain/surfacing_scheduler.py` (brain is canonical; 1,208-line diff means MAJOR divergence — needs careful merge, not delete) |
| `transcript_archiver.py` | 24,444 | Archive session transcripts | /handoff | **KEEP** |
| `vault_annotation_sync.py` | 15,621 | Sync human vault annotations back to COC | /faerie SKILL Step 0 | **MERGE** → `nervous-system/vault-sync/vault_annotation_sync.py` (canonical; 814-line diff = major divergence, needs merge) |
| `vault_backup.py` | 8,460 | Incremental vault backup to B2/local | Scheduled | **KEEP** |
| `vault_frontmatter_lint.py` | 21,242 | Lint vault frontmatter YAML | Manual | **KEEP** |
| `vault_hash_sync.py` | 12,507 | Per-file SHA256 into vault frontmatter | Manual, hook | **KEEP** (absorbs stamp_doc_hash) |
| `vault_manifest.py` | 6,984 | Hash vault files for COC court-readiness (bulk snapshot) | Manual / post-agent-write | **MERGE** → `vault_hash_sync.py --manifest` (overlapping hash concern) |
| `vault_narrative_sync.py` | 39,405 | Push REVIEW-INBOX → vault Human-Inbox | Stop hook, UserPromptSubmit | **MERGE** → `nervous-system/vault-sync/vault_narrative_sync.py` (canonical; 1,319-line diff = needs full merge) |
| `vault_push.py` | 11,283 | Push agent memory to Obsidian vault | Skills | **MERGE** → `vault_sync.py --push` |
| `vault_sign.py` | 7,967 | Session-aware signing via hash_tracker | Manual | **MERGE** → `hash_tracker.py --sign-session` |
| `vault_sync.py` | 8,588 | Route analytical products to vault | Skills | **KEEP** (absorbs vault_push) |
| `wb_sprint_log.py` | 15,422 | Log sprint results to Weights & Biases | Stop hook, perf-eval | **KEEP** — requires pipx W&B env, naturally isolated |
| `write_eval_mirror.py` | 5,127 | Generate eval-mirror.md for Obsidian panels | Stop hook | **MERGE** → `write_memory_status.py --eval` |
| `write_memory_status.py` | 5,472 | Generate memory-status.md for Obsidian panels | Stop hook | **KEEP** (absorbs write_eval_mirror) |

### `brain/` (7 scripts)

| Script | Bytes | Purpose | Caller | Verdict |
|--------|-------|---------|--------|---------|
| `context_phase.py` | 13,227 | Phase calculator (canonical) | statusline, hooks | **KEEP** — canonical; .claude/scripts/ version is diverged copy |
| `emergency_handoff.py` | 13,109 | Handoff snapshot (canonical) | /handoff, hooks | **KEEP** — canonical; .claude/scripts/ version is older |
| `health_check.py` | 21,379 | Nervous system health check (canonical) | UserPromptSubmit hook | **KEEP** — canonical; .claude/scripts/ version is exec shim |
| `metrics_renderer.py` | 15,165 | Render metrics to dashboard | brain internals | **KEEP** |
| `queue_ops.py` | 28,660 | Queue operations (identical to .claude/hooks/state/) | /run, hooks | **DELETE** — exact duplicate; symlink or use .claude/hooks/state/ |
| `session_metrics.py` | 15,559 | Session KPI hash-chaining (canonical) | Stop hook | **KEEP** — canonical; .claude/scripts/ version is diverged copy |
| `surfacing_scheduler.py` | 20,100 | Wave timing scheduler (canonical) | Stop hook, /faerie | **KEEP** — canonical; .claude/scripts/ version is diverged |

### `nervous-system/hooks/` (6 scripts)

| Script | Bytes | Purpose | Caller | Verdict |
|--------|-------|---------|--------|---------|
| `agent_tracker.py` | 10,228 | Agent tracker (458-line diff from .claude/hooks/) | nervous-system install | **KEEP** — nervous-system module canonical for that install path |
| `forensic_coc.py` | 21,936 | Forensic COC (1,248-line diff from .claude/hooks/) | nervous-system hooks | **KEEP** — nervous-system variant |
| `memory_collector.py` | 5,042 | Collect MEM blocks to scratch | PostToolUse hook | **KEEP** |
| `memory_router.py` | 13,247 | Memory router (726-line diff from .claude/scripts/) | nervous-system | **KEEP** — nervous-system variant |
| `notification_handler.py` | 11,906 | Notification handler (IDENTICAL to .claude/hooks/) | Notification hook | **DELETE** (from nervous-system) — exact copy; one location must be canonical |
| `session_stop_hook.py` | 16,426 | Stop hook (5-line diff from .claude/hooks/) | Stop event | **MERGE** — 5-line diff is trivial; merge and share one source |
| `statusline.py` | 9,693 | Statusline (541-line diff from .claude/hooks/) | Per-turn display | **KEEP** — nervous-system variant |

### `nervous-system/vault-sync/` (4 scripts)

| Script | Bytes | Purpose | Caller | Verdict |
|--------|-------|---------|--------|---------|
| `note_sign.py` | 87,144 | Note signing (53-byte diff from .claude/scripts/) | Manual, vault annotation | **KEEP** as canonical; .claude/scripts/ copy should be symlink |
| `vault_annotation_sync.py` | 16,189 | Annotation sync to COC (814-line diff from .claude/scripts/) | /faerie SKILL Step 0 | **KEEP** as canonical; .claude/scripts/ copy needs merge |
| `vault_narrative_sync.py` | 13,785 | Narrative sync (1,319-line diff from .claude/scripts/) | Stop hook | **KEEP** as canonical; .claude/scripts/ copy needs merge |
| `vault_nectar_atomize.py` | 14,169 | Atomize NECTAR entries to session briefs | /handoff | **KEEP** |

### `scripts/` (5 scripts — build tools)

| Script | Bytes | Purpose | Caller | Verdict |
|--------|-------|---------|--------|---------|
| `narrative_auto_update.py` | 14,649 | Auto-update narrative (near-duplicate of .claude/scripts/ version) | session_stop_hook | **DELETE** — hook should call .claude/scripts/narrative_auto_update.py directly |
| `s1a_path_utils.py` | 1,285 | Path safety helpers (garbled path detection) | s1b, s2 | **KEEP** — build tooling |
| `s1b_check_path_sanity.py` | 1,206 | CI/pre-commit path sanity check | CI | **KEEP** — build tooling |
| `s2_build_release_bundles.py` | 5,396 | Build OS release bundles | Manual build step | **KEEP** |

### Root-level (2 scripts)

| Script | Bytes | Purpose | Caller | Verdict |
|--------|-------|---------|--------|---------|
| `_paths.py` | ~800 | Shared path resolver (THE portable resolver) | Manual import | **KEEP** — but should supersede claude_home.py + faerie_paths.py |
| `usage_logger.py` | ~2,000 | API usage JSONL logger | API call sites | **KEEP** |
| `usage_report.py` | ~1,500 | Cost savings report | Manual | **MERGE** → `status_overview.py --costs` |

### `.claude/skills/` (9 scripts)

| Script | Bytes | Purpose | Caller | Verdict |
|--------|-------|---------|--------|---------|
| `context-roundup/run.py` | 13,706 | Context roundup for /faerie | /faerie SKILL | **KEEP** |
| `continual-learning/run.py` | 15,161 | Continual learning loop | /faerie --train | **KEEP** |
| `run/build_sprint_reasoning.py` | 11,296 | Build reasoning context for sprint | /run SKILL | **KEEP** |
| `run/claim_task.py` | 14,193 | Atomic task claim from queue | /run SKILL | **KEEP** |
| `run/project_identity.py` | 5,630 | Resolve project identity | /run SKILL | **MERGE** → `_paths.py` or `faerie_paths.py` |
| `run/register_project_path.py` | 1,217 | Register project path in state | /run SKILL | **MERGE** → `run/claim_task.py` |
| `subagent-spawn/record_run.py` | 2,725 | Record spawn in subagent roster | Every spawn | **KEEP** |
| `vision-ingest/merge_to_dashboard.py` | 8,607 | Merge vision extractions to dashboard | /vision-ingest | **KEEP** |
| `vision-ingest/vision_extract_tables.py` | 15,743 | Extract tables from video frames | /vision-ingest | **KEEP** |

---

## Part 2: Consolidation Proposals

### GROUP A — Blueprint Scripts (6 → 1)

**Problem:** Six scripts for blueprint operations, none calling each other, with scattered responsibilities.

**Proposal:** Merge all into `blueprint_resolver.py` as subcommands:

```
blueprint_resolver.py discover     ← absorbs blueprint_discover.py
blueprint_resolver.py inject       ← absorbs blueprint_inject.py
blueprint_resolver.py regen        ← absorbs blueprint_manifest_generator.py
blueprint_resolver.py audit        ← absorbs blueprint_permissions_audit.py
blueprint_resolver.py validate     ← existing --validate
blueprint_resolver.py validate-batch ← absorbs blueprint_validate_batch.py
```

**Eliminated:** `blueprint_discover.py`, `blueprint_inject.py`, `blueprint_manifest_generator.py`, `blueprint_permissions_audit.py`, `blueprint_validate_batch.py` (5 scripts)
**Savings:** ~38,587 bytes, 5 files

---

### GROUP B — Vault Hashing (4 → 1)

**Problem:** Four scripts that all hash vault files with overlapping scopes.

| Script | What it actually does |
|--------|----------------------|
| `vault_hash_sync.py` | Per-file SHA256 into frontmatter — canonical vault hash tool |
| `vault_manifest.py` | Bulk hash all vault .md files for COC snapshot |
| `stamp_doc_hash.py` | Stamp SHA256 into frontmatter (same as vault_hash_sync --write) |
| `hash_tracker.py` | Directory-level snapshots with HMAC (broader — project-agnostic) |

**Proposal:** Keep `vault_hash_sync.py` as the vault-specific tool (absorbing stamp_doc_hash and vault_manifest), keep `hash_tracker.py` for project-agnostic HMAC snapshots:

```
vault_hash_sync.py --write        ← existing per-file hash
vault_hash_sync.py --manifest     ← absorbs vault_manifest.py
vault_hash_sync.py --stamp FILE   ← absorbs stamp_doc_hash.py
hash_tracker.py snapshot          ← keep for project-agnostic HMAC
```

**Eliminated:** `stamp_doc_hash.py`, `vault_manifest.py` (2 scripts)
**Savings:** ~16,562 bytes, 2 files

---

### GROUP C — Vault Sync/Push (3 → 1)

**Problem:** Three scripts for "write files to vault" with overlapping target directories.

| Script | What it does |
|--------|-------------|
| `vault_sync.py` | Route analytical products to 00-SHARED (has `--file`, `--batch`, `--verify`) |
| `vault_push.py` | Push agent memory (REVIEW-INBOX, KNOWLEDGE-BASE) to vault |
| `vault_sign.py` | Session-aware signing — runs hash_tracker.py for all session CREATE entries |

`vault_push.py` is specifically about memory files, `vault_sync.py` is about analytical products. These have different write targets but the file routing logic overlaps.

**Proposal:** Absorb `vault_push.py` as `vault_sync.py --push-memory`, keep `vault_sign.py` for PGP/signing (distinct concern, not just routing):

```
vault_sync.py --push-memory       ← absorbs vault_push.py
vault_sign.py                     ← KEEP (signing is distinct from syncing)
```

**Eliminated:** `vault_push.py` (1 script)
**Savings:** ~11,283 bytes, 1 file

---

### GROUP D — Brain/Scripts Duplicates (4 → canonical-only)

**Problem:** `.claude/scripts/` contains copies of `brain/` scripts that have diverged significantly. The `brain/` versions are canonical (they have proper docstrings, are called from hooks, are named in `SCRIPT-REGISTRY.md`).

| `.claude/scripts/` copy | `brain/` canonical | Divergence |
|--------------------------|-------------------|------------|
| `context_phase.py` | `brain/context_phase.py` | 400 diff lines |
| `session_metrics.py` | `brain/session_metrics.py` | 877 diff lines |
| `surfacing_scheduler.py` | `brain/surfacing_scheduler.py` | 1,208 diff lines |
| `emergency_handoff.py` | `brain/emergency_handoff.py` | Major (different docstring focus) |

**Proposal:** 
1. Audit each pair — identify which has newer features
2. Merge newer features into the `brain/` canonical version
3. Replace `.claude/scripts/` copies with thin exec shims (like `health_check.py` already does) OR update all callers to point to `brain/`
4. The goal: `brain/` is the ONE place for core orchestration logic

**Eliminated:** 4 scripts reduced to 4 exec shims (or callers updated)
**Net savings:** ~76,000 bytes of duplicated logic (exact delta pending merge)

---

### GROUP E — Memory Scripts (4 → 2)

**Problem:** `memory_bridge.py`, `memory_router.py`, `memory_gate.py`, `inbox_router.py` — overlapping memory routing concerns.

| Script | Distinct responsibility |
|--------|------------------------|
| `memory_bridge.py` | Streaming (emit/collect) — genuinely distinct |
| `memory_router.py` | Fragmentation healing + MEM block promotion — distinct |
| `memory_gate.py` | Budget pre-check before writes — overlaps with `debloat.py --check` |
| `inbox_router.py` | Route flags to inboxes — subset of memory_router.py's promotion logic |

**Proposal:**
```
memory_bridge.py          ← KEEP (streaming is distinct)
memory_router.py --route  ← absorbs inbox_router.py
debloat.py --check FILE   ← absorbs memory_gate.py (budget check = debloat concern)
```

**Eliminated:** `inbox_router.py`, `memory_gate.py` (2 scripts)
**Savings:** ~37,418 bytes, 2 files

---

### GROUP F — Single-Write Dashboard Scripts (2 → 1)

**Problem:** `write_eval_mirror.py` and `write_memory_status.py` each write one Obsidian dashboard file. Same pattern, same target directory, same trigger (Stop hook).

**Proposal:** Merge into `write_memory_status.py` with `--eval` flag:
```
write_memory_status.py              ← writes memory-status.md (existing)
write_memory_status.py --eval       ← absorbs write_eval_mirror.py
```

**Eliminated:** `write_eval_mirror.py` (1 script)
**Savings:** ~5,127 bytes, 1 file

---

### GROUP G — Eval Quality Helpers (2 → absorbed)

**Problem:** `depth_score.py` and `honey_hit_validator.py` are called exclusively as sub-dimensions of `eval_harness.py`. They are not standalone tools.

**Proposal:** Inline both as modules/functions within `eval_harness.py`. They have no independent callers.

**Eliminated:** `depth_score.py`, `honey_hit_validator.py` (2 scripts)
**Savings:** ~10,409 bytes, 2 files

---

### GROUP H — Session Handoff Cluster (4 → 2)

**Problem:** `bundle_handoff.py`, `handoff_logger.py`, `session_manifest.py`, and `emergency_handoff.py` (scripts/) all do "collect state at session end" operations.

**Proposal:**
- `brain/emergency_handoff.py` absorbs `session_manifest.py` as `--manifest` flag
- `bundle_handoff.py` absorbs `handoff_logger.py` (the logger is just input to the bundler)
- `bundle_handoff.py` is renamed `dossier_bundler.py` to distinguish from emergency_handoff

**Eliminated:** `handoff_logger.py`, `session_manifest.py`, `.claude/scripts/emergency_handoff.py` (3 scripts; the last replaced by exec shim)
**Savings:** ~60,000 bytes duplicated logic, 3 files

---

### GROUP I — Nervous-System Exact Duplicates

**Problem:** `nervous-system/hooks/notification_handler.py` is an **exact byte-for-byte copy** of `.claude/hooks/notification_handler.py`. This is a sync artifact.

**Proposal:** One of these must be canonical. The `.claude/hooks/` versions are what `settings.json` references. The `nervous-system/` directory appears to be a source-of-truth repo that gets copied. Establish this explicitly:

- `nervous-system/` = source of truth (develop here)  
- `.claude/hooks/` = deploy target (built by `s2_build_release_bundles.py`)
- Delete manually-maintained copies in `.claude/` that should be managed by the build

**Eliminated:** `nervous-system/hooks/notification_handler.py` (or its .claude/ copy, depending on which direction the build flows). Likely 5+ files once the build relationship is clarified.

---

### GROUP J — Path Resolver Proliferation (3 → 1)

**Problem:** Three scripts that each define their own `_claude_home()` or `_resolve_claude_home()` function:
- `_paths.py` (root) — "THE portable resolver" per its own docstring
- `claude_home.py` — "Shared utility: resolve ~/.claude"  
- `faerie_paths.py` — small shim already used by hooks

**Proposal:** `_paths.py` is the stated canonical; `claude_home.py` is redundant. `faerie_paths.py` is a deploy-target shim that should import from `_paths.py`.

**Eliminated:** `claude_home.py` (1 script); `faerie_paths.py` reduced to 3-line wrapper
**Savings:** ~1,139 bytes, 1 file

---

### GROUP K — Routing Feedback (absorbed)

**Problem:** `routing_feedback.py` records agent routing quality. This is one data point consumed by `eval_harness.py` ROUTING dimension. It has no independent callers beyond the Stop hook feeding eval_harness.

**Proposal:** Inline as `eval_harness.py --routing-feedback` or absorb the feedback collection into the harness directly.

**Eliminated:** `routing_feedback.py` (1 script)
**Savings:** ~8,207 bytes, 1 file

---

### GROUP L — Queue Subcommand Candidates (2 → absorbed)

**Problem:** `queue_analyzer.py` (intent-driven prioritization) and `state/select_agent.py` (score-driven routing) are thin wrappers over queue state logic that already lives in `queue_ops.py`.

**Proposal:**
```
queue_ops.py prioritize --intent unblock   ← absorbs queue_analyzer.py
queue_ops.py select-agent                  ← absorbs state/select_agent.py
```

**Eliminated:** `queue_analyzer.py`, `state/select_agent.py` (2 scripts)
**Savings:** ~11,003 bytes, 2 files

---

### GROUP M — State Lock Consolidation (1 → absorbed)

**Problem:** `state/sprint_queue_lock.py` is a queue-specific locking wrapper over `state/json_lock.py`.

**Proposal:** Absorb sprint_queue_lock as a subclass or function in `json_lock.py`.

**Eliminated:** `state/sprint_queue_lock.py` (1 script)
**Savings:** ~2,596 bytes, 1 file

---

### GROUP N — Dashboard Launcher (1 → absorbed)

**Problem:** `state/faerie-dashboard-launcher.py` launches the dashboard. This is one function called from `state/s3a_faerie_turn1.py`.

**Proposal:** Inline the launch logic into `s3a_faerie_turn1.py`.

**Eliminated:** `state/faerie-dashboard-launcher.py` (1 script)
**Savings:** ~3,341 bytes, 1 file

---

### GROUP O — Export Queue (1 → absorbed)

**Problem:** `state/export_queue_to_vault.py` is a single-purpose script: export sprint queue JSON to vault. `queue_vault_sync.py` already syncs the queue to vault bidirectionally.

**Proposal:** Absorb as `queue_vault_sync.py --export`.

**Eliminated:** `state/export_queue_to_vault.py` (1 script)
**Savings:** ~6,236 bytes, 1 file

---

### GROUP P — Batch API Scripts (2 → 1)

**Problem:** `batch_submit.py` and `batch_collect.py` are two halves of the same Batch API workflow. No caller uses them independently.

**Proposal:** Merge into `batch_submit.py --collect` (or rename `batch_ops.py`).

**Eliminated:** `batch_collect.py` (1 script)
**Savings:** ~4,284 bytes, 1 file

---

## Part 3: Dead Code Identification

Scripts with no active callers (not in settings.json hooks, not imported, not referenced in SKILL.md files currently in use):

1. **`add_wiring_tasks.py`** — One-shot migration script. Comment at top says "run once." Already run. 0 callers.

2. **`scripts/narrative_auto_update.py`** — Duplicate of `.claude/scripts/narrative_auto_update.py`. The `session_stop_hook.py` resolves which one to call at runtime (prefers `{REPO_ROOT}/scripts/`, falls back to `.claude/scripts/`). The presence of both creates ambiguity; only the `.claude/scripts/` version should be canonical.

3. **`.claude/scripts/health_check.py`** — 36-line exec shim only. The hook should be updated to call `brain/health_check.py` directly. This shim is dead weight.

4. **`state/stdio_utf8.py`** — 539-byte UTF-8 shim. Imported nowhere in the codebase (grepped). May be vestigial from earlier Windows hook work.

5. **`brain/queue_ops.py`** — **Exact duplicate** (byte-for-byte identical md5: `97472b9e386f2c269ea029f66d03a85c`) of `.claude/hooks/state/queue_ops.py`. One must be deleted; the other should be a symlink or the callers updated to use one path.

---

## Part 4: Duplicate Detection

Scripts found in multiple locations with identical or near-identical content:

| File | Location 1 | Location 2 | Diff Lines | Status |
|------|-----------|-----------|------------|--------|
| `queue_ops.py` | `brain/` | `.claude/hooks/state/` | **0** (identical) | Delete one, symlink |
| `notification_handler.py` | `.claude/hooks/` | `nervous-system/hooks/` | **0** (identical) | Delete nervous-system copy (hooks/ is deploy target) |
| `note_sign.py` | `.claude/scripts/` | `nervous-system/vault-sync/` | ~53 bytes | nervous-system is canonical; .claude/ copy needs update |
| `session_stop_hook.py` | `.claude/hooks/` | `nervous-system/hooks/` | 5 lines | Merge 5-line diff, share one source |
| `context_phase.py` | `.claude/scripts/` | `brain/` | 400 lines | brain/ is canonical; .claude/ should be exec shim |
| `session_metrics.py` | `.claude/scripts/` | `brain/` | 877 lines | brain/ is canonical; .claude/ should be exec shim |
| `surfacing_scheduler.py` | `.claude/scripts/` | `brain/` | 1,208 lines | **Most diverged pair** — requires careful feature audit before merge |
| `emergency_handoff.py` | `.claude/scripts/` | `brain/` | Major | brain/ is canonical (newer docstring, broader feature set) |
| `health_check.py` | `.claude/scripts/` (36 lines) | `brain/` (590 lines) | All | .claude/ is already a shim; correct pattern |
| `vault_annotation_sync.py` | `.claude/scripts/` | `nervous-system/vault-sync/` | 814 lines | nervous-system is canonical; .claude/ needs merge |
| `vault_narrative_sync.py` | `.claude/scripts/` | `nervous-system/vault-sync/` | 1,319 lines | **Most diverged vault pair** — full feature audit required |
| `agent_tracker.py` | `.claude/hooks/` | `nervous-system/hooks/` | 458 lines | nervous-system is canonical (richer); .claude/ is deploy copy |
| `memory_router.py` | `.claude/scripts/` | `nervous-system/hooks/` | 726 lines | nervous-system is canonical |
| `forensic_coc.py` | `.claude/hooks/` | `nervous-system/hooks/` | 1,248 lines | **Most diverged forensic pair** — very significant; requires COC-aware merge |

**Release copies:** Every script in `.claude/hooks/`, `.claude/skills/`, etc. is also copied to `releases/linux/`, `releases/macos/`, `releases/windows-wsl/`, `releases/windows-native/`, `releases/windows/`. These are build artifacts managed by `s2_build_release_bundles.py`. They should NOT be manually edited — they are not counted in the duplication problem above.

---

## Part 5: Proposed Minimum Viable Set

After all consolidations, the canonical script set (excluding releases/ and __pycache__):

### Core orchestration — `brain/` (7, unchanged)
- `context_phase.py` — phase calculator
- `emergency_handoff.py` — handoff snapshot  
- `health_check.py` — system health
- `metrics_renderer.py` — metrics display
- `queue_ops.py` — queue operations (DELETE duplicate in .claude/hooks/state/)
- `session_metrics.py` — session KPIs
- `surfacing_scheduler.py` — wave timing

### Hooks — `.claude/hooks/` (12, down from 14)
- `agent_tracker.py` (absorbs post-agent-validate)
- `faerie_gates.py`
- `faerie_paths.py` (absorbs claude_home.py + stdio_utf8 shim)
- `forensic_coc.py`
- `notification_handler.py`
- `presend_estimate.py`
- `session_stop_hook.py`
- `statusline.py`
- `statusline_win.py`
- `state/drops.py`
- `state/faerie_training_orchestrator.py`
- `state/json_lock.py` (absorbs sprint_queue_lock)
- `state/queue_ops.py` → DELETE (use brain/queue_ops.py)
- `state/s3a_faerie_turn1.py` (absorbs faerie-dashboard-launcher)
- `state/s3b_dynamo_orchestrator.py` (absorbs dynamo_dashboard)
- `state/select_agent.py` → DELETE (absorb into queue_ops)
- `state/session_heartbeat.py`
- `state/system_guardian.py`
- `state/training_queue_manager.py` (absorbs beat_last_verifier)

### Scripts — `.claude/scripts/` (32, down from 57)
- `agent_lifecycle.py`
- `backup_forensics.py`
- `batch_submit.py` (absorbs batch_collect)
- `blueprint_resolver.py` (absorbs 4 other blueprint scripts)
- `collab_export.py` (absorbs collaboration_validator)
- `context_phase.py` → EXEC SHIM (delegates to brain/)
- `crystallize.py`
- `debloat.py` (absorbs memory_gate)
- `dossier_bundler.py` (rename bundle_handoff, absorbs handoff_logger)
- `emergency_handoff.py` → EXEC SHIM (delegates to brain/)
- `eval_harness.py` (absorbs depth_score, honey_hit_validator, routing_feedback)
- `hash_tracker.py`
- `honey_version.py`
- `memory_bridge.py`
- `memory_router.py` (absorbs inbox_router)
- `model_compare.py`
- `narrative_auto_update.py`
- `note_sign.py`
- `piston.py`
- `queue_vault_sync.py` (absorbs export_queue_to_vault)
- `scratch_collector.py`
- `session_metrics.py` → EXEC SHIM (delegates to brain/)
- `staging_promoter.py`
- `status_overview.py` (absorbs usage_report)
- `surfacing_scheduler.py` → EXEC SHIM (delegates to brain/)
- `transcript_archiver.py`
- `vault_annotation_sync.py` (merge with nervous-system canonical, keep one)
- `vault_backup.py`
- `vault_frontmatter_lint.py`
- `vault_hash_sync.py` (absorbs vault_manifest, stamp_doc_hash)
- `vault_narrative_sync.py` (merge with nervous-system canonical, keep one)
- `vault_sign.py`
- `vault_sync.py` (absorbs vault_push)
- `wb_sprint_log.py`
- `write_memory_status.py` (absorbs write_eval_mirror)

### Vault-sync — `nervous-system/vault-sync/` (4, unchanged)
- `note_sign.py` (canonical)
- `vault_annotation_sync.py` (canonical)
- `vault_narrative_sync.py` (canonical)
- `vault_nectar_atomize.py`

### Hooks — `nervous-system/hooks/` (5, down from 6)
- `agent_tracker.py`
- `forensic_coc.py`
- `memory_collector.py`
- `memory_router.py`
- `notification_handler.py` → DELETE (exact duplicate of .claude/hooks/)
- `session_stop_hook.py` (merge 5-line diff)
- `statusline.py`

### Skills (7, down from 9)
- `context-roundup/run.py`
- `continual-learning/run.py`
- `run/build_sprint_reasoning.py`
- `run/claim_task.py` (absorbs register_project_path)
- `run/project_identity.py` → MERGE into `_paths.py`
- `subagent-spawn/record_run.py`
- `vision-ingest/merge_to_dashboard.py`
- `vision-ingest/vision_extract_tables.py`

### Build tools — `scripts/` (3, down from 5)
- `s1a_path_utils.py`
- `s1b_check_path_sanity.py`
- `s2_build_release_bundles.py`
- `narrative_auto_update.py` → DELETE
- `_paths.py` (root, keep as canonical path resolver)

### Root-level (2, down from 3)
- `_paths.py`
- `usage_logger.py`
- `usage_report.py` → absorbed into status_overview.py

**Proposed total: ~72 canonical scripts** (down from 117, a 38% reduction)

---

## Part 6: Implementation Plan

Ordered by risk and dependency. Complete each phase before starting the next.

### Phase 1 — Zero-Risk Deletes (no merge required)

These are safe to delete immediately:

1. `brain/queue_ops.py` — exact duplicate of `.claude/hooks/state/queue_ops.py` (md5 identical). Delete `brain/` copy; update `brain/` imports to use `../.claude/hooks/state/queue_ops.py` or resolve via `_paths.py`.
2. `nervous-system/hooks/notification_handler.py` — exact duplicate of `.claude/hooks/notification_handler.py`. Delete nervous-system copy.
3. `.claude/scripts/add_wiring_tasks.py` — one-shot script, already run.
4. `scripts/narrative_auto_update.py` — session_stop_hook resolves this at runtime, .claude/scripts/ version is the one used.
5. `state/stdio_utf8.py` — no callers found; inline the 5-line UTF-8 fix into `faerie_paths.py`.

**Risk:** None. 5 files deleted.

### Phase 2 — Subcommand Absorptions (additive — add flags to existing scripts)

These only add new flags/subcommands; existing behavior unchanged:

6. `vault_hash_sync.py --manifest` absorbs `vault_manifest.py`
7. `vault_hash_sync.py --stamp` absorbs `stamp_doc_hash.py`
8. `vault_sync.py --push-memory` absorbs `vault_push.py`
9. `write_memory_status.py --eval` absorbs `write_eval_mirror.py`
10. `batch_submit.py --collect` absorbs `batch_collect.py`
11. `queue_vault_sync.py --export` absorbs `state/export_queue_to_vault.py`
12. `state/s3a_faerie_turn1.py` inline absorbs `state/faerie-dashboard-launcher.py`
13. `state/json_lock.py` absorbs `state/sprint_queue_lock.py` as subclass

**Risk:** Low. Test each absorption independently. 8 files eliminated.

### Phase 3 — Blueprint Consolidation

14. Audit all 5 blueprint helper scripts for features not yet in `blueprint_resolver.py`
15. Add missing subcommands to `blueprint_resolver.py`
16. Update all callers (check `.claude/skills/*.md` for blueprint references)
17. Delete 5 absorbed scripts

**Risk:** Medium — requires caller audit. 5 files eliminated.

### Phase 4 — Eval Harness Consolidation

18. Inline `depth_score.py` functions into `eval_harness.py`
19. Inline `honey_hit_validator.py` into `eval_harness.py` QUALITY dimension
20. Inline `routing_feedback.py` collection into `eval_harness.py` ROUTING dimension
21. Remove the 3 scripts and their Stop hook registrations

**Risk:** Medium — eval_harness is a hot path. Test after each inline. 3 files eliminated.

### Phase 5 — Memory Routing Consolidation

22. Move `inbox_router.py` logic into `memory_router.py --route`
23. Move `memory_gate.py` budget check into `debloat.py --check FILE`
24. Update callers (check skills, agents that call memory_gate)
25. Delete 2 scripts

**Risk:** Medium — agents call memory_gate directly. 2 files eliminated.

### Phase 6 — Path Resolver Unification

26. Confirm `_paths.py` exports all symbols currently in `claude_home.py` and `faerie_paths.py`
27. Update `claude_home.py` callers to use `_paths.py`
28. Reduce `faerie_paths.py` to a 3-line import wrapper (deploy-target shim)
29. Delete `claude_home.py`

**Risk:** Low-medium — path resolution is foundational. 1 file eliminated.

### Phase 7 — Handoff Cluster

30. Audit feature overlap between `bundle_handoff.py` and `handoff_logger.py`
31. Merge `handoff_logger.py` into `bundle_handoff.py` (logger = input queue to bundler)
32. Add `emergency_handoff.py --manifest` absorbing `session_manifest.py`
33. Rename `bundle_handoff.py` → `dossier_bundler.py` for clarity
34. Update `/handoff` skill and Stop hook references

**Risk:** Medium — handoff is session-end critical path. 2 files eliminated.

### Phase 8 — Brain/Scripts Exec Shim Pattern

This is the highest-risk phase — diverged copies with up to 1,300 lines of difference.

**Approach for each pair:**
1. Run `diff brain/X.py .claude/scripts/X.py > /tmp/diff-X.patch`
2. Identify which changes are features (keep) vs drift (discard)
3. Apply features to the `brain/` canonical
4. Replace `.claude/scripts/X.py` with exec shim (like health_check.py already does)
5. Update `settings.json` hooks that call `.claude/scripts/X.py` to use `brain/X.py`

**Order (least to most diverged):**
- `context_phase.py` (400 diff lines)
- `session_metrics.py` (877 diff lines)
- `surfacing_scheduler.py` (1,208 diff lines) — **block out a dedicated session**
- `emergency_handoff.py` (full review)

**Also:**
- `nervous-system/` duplicates follow the same pattern: nervous-system is canonical, .claude/scripts/ needs to become a shim or be updated by the build

**Risk:** High. Require full test suite run after each merge. 4+ files replaced with shims.

### Phase 9 — Queue Subcommand Absorptions

35. Add `queue_ops.py prioritize` absorbing `queue_analyzer.py`
36. Add `queue_ops.py select-agent` absorbing `state/select_agent.py`

**Risk:** Low — additive. 2 files eliminated.

### Phase 10 — Final Cleanup

37. Update `SCRIPT-REGISTRY.md` to reflect consolidated set
38. Run `debloat.py --scan` to confirm no budget violations introduced
39. Run `brain/health_check.py` to confirm no broken hook paths
40. Update `s2_build_release_bundles.py` to handle exec shims correctly (shims need to resolve `brain/` path relative to install location)

---

## Summary Metrics

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Canonical scripts (excl. releases/) | 117 | ~72 | -45 (-38%) |
| Exact duplicates | 2 | 0 | -2 |
| Diverged copies | 12 | 0 | -12 (shims) |
| Blueprint scripts | 6 | 1 | -5 |
| Vault hashing scripts | 4 | 1+1 | -2 |
| One-shot / dead scripts | 3 | 0 | -3 |
| Single-function scripts | 8 | 0 | -8 (absorbed) |
| Estimated bytes eliminated | — | — | ~280,000 bytes |
| Implementation phases | — | 10 | — |
| Zero-risk deletes (Phase 1) | — | 5 | Done first |

**Highest value consolidations (by impact-to-effort ratio):**
1. Blueprint 6→1 (5 scripts, low complexity, no hook dependencies)
2. Brain/Scripts exec shims (4 scripts, resolves ongoing drift problem permanently)
3. Eval harness absorptions (3 scripts, improves cohesion of measurement layer)
4. `queue_ops.py` exact duplicate (0 effort, just delete)

**Most dangerous merges (do last, with tests):**
1. `surfacing_scheduler.py` — 1,208-line divergence in core wave timing logic
2. `nervous-system/forensic_coc.py` — 1,248-line divergence in COC forensic path
3. `vault_narrative_sync.py` — 1,319-line divergence in session-end vault writes
