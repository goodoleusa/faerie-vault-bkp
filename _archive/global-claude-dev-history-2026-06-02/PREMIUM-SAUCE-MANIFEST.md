---
type: manifest
status: final
created: 2026-04-20
tags: [equilibrium, ship-readiness, premium-tier, script-audit]
parent: /mnt/d/0LOCAL/.claude/CLAUDE.md
up: /mnt/c/Users/amand/.claude/rules/core.md
child: [script-equilibrium-audit-2026-04-20.json, script-rename-plan-2026-04-20.json]
down: [script-equilibrium-audit-2026-04-20.json]
same: [/mnt/d/0LOCAL/.claude/hooks/state/script-equilibrium-audit-2026-04-20.json]
doc_hash: sha256:pending
hash_ts: 2026-04-20T22:01:33Z
hash_method: body-sha256-v1
---

> [up Parent CLAUDE.md](/mnt/d/0LOCAL/CLAUDE.md) - [same Audit JSON](/mnt/d/0LOCAL/.claude/hooks/state/script-equilibrium-audit-2026-04-20.json) - [same Rename Plan](/mnt/d/0LOCAL/.claude/hooks/state/script-rename-plan-2026-04-20.json) - [home Rules core.md](/mnt/c/Users/amand/.claude/rules/core.md)

# Premium Sauce Manifest — Paid Tier Feature Edge

**Audit run:** 2026-04-20T22:01:33Z  
**Scripts scanned:** 525  
**Compliance:** 40 compliant (8%) / 220 warn (42%) / 265 violation (50%)  
**Ship blocker:** 1 script load-misclassified (see Violations below)

## Executive Summary

The Claude system is architected as **core + sauce**. Core = system-critical (free tier, fully functional). Sauce = enhancement (premium tier, graceful degradation when absent). This manifest enumerates the paid-tier feature edge across **7 feature bundles** and specifies the graceful-degradation contract.

Key finding: free tier is already viable. Every spawned agent, memory promotion, forensic COC write, and session lifecycle event works on the core set alone. Sauce adds intelligence, observability, and domain depth — but never gates the fundamental loop.

## 1. Free Tier — What You Get With Core Alone

**37 core scripts** keep the system operating: agents spawn, memory flows pollen -> NECTAR -> HONEY, forensic COC writes on every tool use, session lifecycle hooks fire cleanly.

| Script | Role |
|---|---|
| `agent_tracker.py` | Tracks in-flight agents + lifecycle state for faerie orchestrator. |
| `auto_handoff.py` | Automatic handoff flow when session approaches compaction or end. |
| `budget_check.py` | Enforces token budget limits on writes to HONEY / rules / cards. |
| `canonicalize_paths.py` | Resolves WSL vs Windows paths to single canonical repo path — anti-ghost. |
| `coc_bridge.py` | Bridges hook events to forensic chain-of-custody ledger. |
| `emergency_handoff.py` | Salvage pollen + hashes when compaction fires unexpectedly. |
| `enforce_budget.py` | Hard block on overbudget writes; routes to crystallize instead. |
| `faerie_gates.py` | Gates that block unsafe faerie operations. |
| `forensic_coc.py` | PostToolUse hook that writes hash-chained COC entries on every write. |
| `forensic_coc_check.py` | Verify COC chain integrity before commits. |
| `handoff_logger.py` | Append-only handoff ledger (who handed what to whom, when). |
| `hash_tracker.py` | Snapshots directory hashes before/after operations for forensic deltas. |
| `hook_runner.py` | Unified hook dispatcher — one entry point for all settings.json hooks. |
| `inbox_router.py` | Routes inbox/queue messages to correct destination. |
| `memory_bridge.py` | Streams agent output; routes pollen -> NECTAR -> HONEY pipeline. |
| `memory_collector.py` | PostToolUse hook that mirrors native auto-memory writes to pollen. |
| `memory_gate.py` | Validates memory writes (schema, budget, routing correctness). |
| `memory_router.py` | Routes MEM blocks to correct file based on category + priority. |
| `native_claude_memory_router.py` | Handles native Claude auto-memory (feedback/project/user/reference). |
| `notification_handler.py` | Processes TaskNotification events from async agent returns. |
| `post_tool_use.py` | Master PostToolUse hook — delegates to all downstream hooks. |
| `post_vault_write_stamp.py` | Stamps SHA-256 on every vault doc after write (COC link). |
| `pre_write_forensics_guard.py` | Blocks writes that would corrupt forensic COC chain. |
| `pre_write_memory_guard.py` | Blocks writes to memory files that violate append-only / budget rules. |
| `presend_estimate.py` | Estimates spawn-prompt token cost + scans for polling language. |
| `prevent-staging-local-settings.py` | Prevents accidentally staging machine-specific settings.json. |
| `protect-coc-paths.py` | Read-only guard on evidence_manifest.json, hash_manifest*.json, coc_*.json. |
| `scratch_collector.py` | Collects session scratch/pollen for memory-keeper promotion. |
| `session_stop_hook.py` | Fires on CLI run end — drains pollen, logs final session state. |
| `shared_file_cache.py` | LRU cache for hot-path file reads across 24 hooks (-60% hook latency). |
| `state_serializer.py` | Atomic JSON state writes with fcntl.flock — prevents corruption. |
| `statusline.py` | Renders the turn-N status footer (stage, alert, ctx, cost). |
| `task_completion_router.py` | Routes task completion events to queue / eval / memory subsystems. |
| `validate_state_files.py` | Schema-validate ~/.claude/hooks/state/*.json on startup. |
| `vault-mutation-tracker.py` | Watches vault for agent/human writes; logs to forensic COC. |
| `vault_guardian.py` | Prevents writes to 01-PROTECTED/, 30-Evidence/, 00-SHARED/Inbox/. |
| `vault_hash_stamp.py` | Computes + writes doc_hash on vault documents. |

**Free tier guarantee:** removing any sauce bundle leaves the system running — slower, blinder, less automated, but running. Core scripts have no soft-import pattern because they are required; their absence IS a system failure and must be diagnosed.

## 2. Paid Tier — Feature Bundles

### Evaluation Suite (10 scripts)

Closed-loop agent improvement — baseline scoring, A/B comparison, KPI tracking, training queue, redemption logging. Without this, agents run but never learn.

| Script | Tier | Premium? | Role |
|---|---|---|---|
| `9x_ab_auto_run.sh` | 9x | yes | Evaluation/benchmarking |
| `9x_ab_score.py` | 9x | yes | Evaluation/benchmarking |
| `auto_eval_hook.py` | 3x | yes | Evaluation/benchmarking |
| `beat_last_verifier.py` | 3x | yes | Evaluation/benchmarking |
| `eval_harness.py` | 3x | yes | Evaluation/benchmarking |
| `eval_membench.py` | 3x | yes | Evaluation/benchmarking |
| `free_eval_harness_extension.py` | 3x | yes | Evaluation/benchmarking |
| `model_compare.py` | 3x | yes | Evaluation/benchmarking |
| `piston_eval_multi_session.py` | 3x | yes | Orchestration |
| `write_eval_mirror.py` | 3x | yes | Evaluation/benchmarking |

### Forensic Premium (8 scripts)

Beyond basic COC — B2 WORM orchestration, PGP signing automation, hash chain dashboard, forensic memory analyzer. Without this, forensic COC still hash-chains locally, but off-site WORM backup is manual.

| Script | Tier | Premium? | Role |
|---|---|---|---|
| `7x_forensic_memory_analyzer.py` | 7x | standard | Analysis |
| `b2_backup_hook.py` | 8x | standard | Archive/backup |
| `backup_forensics.py` | 4x | standard | Evidence/COC |
| `forensics_b2_sync.py` | 4x | standard | Evidence/COC |
| `hash_guardian_RUN008.py` | 4x | standard | Evidence/COC |
| `hash_guardian_run006.py` | 4x | standard | Evidence/COC |
| `hash_viz_RUN011.py` | 9x | standard | Unclassified — needs human review |
| `note_sign.py` | 4x | standard | Unclassified — needs human review |

### Performance Optimization (7 scripts)

Spend less per insight — token-optimizer reports, cache hit tracking, dev-health dashboards, context calibration, compact-risk detection, debloat scans. Without this, the system runs; it just costs more.

| Script | Tier | Premium? | Role |
|---|---|---|---|
| `compact-risk-detector.py` | 3x | standard | Unclassified — needs human review |
| `context_calibrator.py` | 9x | yes | Cost/context optimization |
| `context_phase.py` | 9x | standard | Cost/context optimization |
| `cost_display.py` | 9x | yes | Cost/context optimization |
| `cost_extractor.py` | 9x | yes | Cost/context optimization |
| `debloat.py` | 9x | yes | Knowledge surfacing |
| `dev_health_audit.py` | 3x | yes | Dashboard/visibility |

### Dashboards & Visibility (12 scripts)

Human interface surface — mission control dashboard, metrics renderer, dashboard launcher, viz index builders. Without this, the system is CLI-only with no graphical overview.

| Script | Tier | Premium? | Role |
|---|---|---|---|
| `build_dashboard.py` | 9x | yes | Dashboard/visibility |
| `build_pipeline_ip_crossref.py` | 9x | standard | Unclassified — needs human review |
| `build_viz_feeds_RUN008.py` | 9x | standard | Unclassified — needs human review |
| `build_viz_index.py` | 9x | standard | Unclassified — needs human review |
| `dae_dashboard.py` | 9x | yes | Dashboard/visibility |
| `dae_dashboard_launcher.py` | 9x | yes | Dashboard/visibility |
| `dashboard_launcher.py` | 9x | yes | Dashboard/visibility |
| `dashboard_presend.py` | 9x | yes | Dashboard/visibility |
| `merge_to_dashboard.py` | 9x | yes | Dashboard/visibility |
| `metrics_renderer.py` | 9x | yes | Dashboard/visibility |
| `session_dashboard.py` | 8x | yes | Dashboard/visibility |
| `status_dashboard.py` | 3x | yes | Dashboard/visibility |

### Investigation Accelerators (10 scripts)

Domain-specific depth — OSINT / SpiderFoot, vision-ingest deep extractors, PDF rendering, Obsidian automations. Without this, investigations proceed via manual extraction.

| Script | Tier | Premium? | Role |
|---|---|---|---|
| `5x_obsidian_to_pdf.sh` | 5x | yes | Publish/distribute |
| `9x_pdf_aspect_sizer.py` | 9x | yes | Investigation accelerator |
| `b2_provision_user.py` | 0x | yes | Setup/genesis helper |
| `gemini_extract_tables.py` | 1x | standard | Ingest/extraction |
| `osint-spiderfoot.py` | 1x | yes | Investigation accelerator |
| `osint_pipeline_task20260330.py` | 1x | yes | Investigation accelerator |
| `pdf-mermaid-prerender.py` | 9x | yes | Investigation accelerator |
| `spiderfoot_osint.py` | 9x | yes | Investigation accelerator |
| `sync_obsidian_vault.py` | 9x | yes | Investigation accelerator |
| `vision_extract_tables.py` | 1x | yes | Ingest/extraction |

### Stigmergy Observatory (9 scripts)

Visibility into agent coordination — piston state, DAG view, flight deck, stigmergy trail tracker, sprint pulse. Without this, agents coordinate (file-stigmergy still works) but you cannot see it.

| Script | Tier | Premium? | Role |
|---|---|---|---|
| `7x_sprint_pulse.py` | 7x | yes | Dashboard/visibility |
| `9c_stigmergy_tracker.py` | 9x | yes | Knowledge surfacing |
| `agent_flight_status.py` | 3x | yes | Unclassified — needs human review |
| `agent_lifecycle.py` | 9x | standard | Unclassified — needs human review |
| `agent_staleness_detector.py` | 9x | standard | Unclassified — needs human review |
| `dag_view.py` | 9x | yes | Dashboard/visibility |
| `flight_deck.py` | 9x | yes | Dashboard/visibility |
| `piston-analyzer.py` | 3x | yes | Analysis |
| `piston-profiler.py` | 3x | yes | Orchestration |

### Knowledge Surfacing (15 scripts)

Insights surface without being asked — broadcast scan, memory retrieve, narrative auto-update, droplet promotion, crystallize helpers. Without this, memory still promotes on /handoff, but active retrieval requires manual grep.

| Script | Tier | Premium? | Role |
|---|---|---|---|
| `4a_narrative_auto_update.py` | 9x | yes | Evidence/COC |
| `8x_broadcast_hook.py` | 8x | standard | Hook enhancement |
| `8x_droplet_register.py` | 8x | standard | Hook enhancement |
| `9e_honey_filter.py` | 9x | standard | Knowledge surfacing |
| `9x_broadcast_scan.py` | 9x | yes | Knowledge surfacing |
| `9x_memory_retrieve.py` | 9x | yes | Knowledge surfacing |
| `apply_crystallize_2026_04_06.py` | 9x | standard | Knowledge surfacing |
| `crystallize.py` | 9x | standard | Knowledge surfacing |
| `honey_hit_validator.py` | 9x | standard | Knowledge surfacing |
| `honey_repo_sync.py` | 9x | standard | Knowledge surfacing |
| `honey_scope_filter.py` | 9x | standard | Knowledge surfacing |
| `honey_version.py` | 7x | standard | Knowledge surfacing |
| `memory-lite-gen.py` | 9x | standard | Unclassified — needs human review |
| `narrative_auto_update.py` | 9x | yes | Publish/distribute |
| `vault_nectar_atomize.py` | 7x | standard | Knowledge surfacing |

## 3. Graceful Degradation Contract

If a paid bundle is disabled (uninstalled, license lapsed, import fails), the system must continue. This table specifies the exact degradation path per bundle.

| Bundle | What Stops | What Still Works |
|---|---|---|
| Evaluation Suite | Score tracking, A/B comparison, training queue auto-updates | Agents spawn + return manifests; user can evaluate manually via /eval; training-log.jsonl still exists as append-only ledger |
| Stigmergy Observatory | Visual piston/DAG state, sprint pulse dashboard, stigmergy stall detection | File-stigmergy itself (agents coordinate via manifest paths); stall detection falls back to manual agent-state.json inspection |
| Knowledge Surfacing | broadcast_scan checkpoints, memory_retrieve ranked search, narrative auto-update on session-stop | Pollen -> NECTAR promotion at /handoff still runs (core); manual grep of HONEY.md + NECTAR.md tail still works |
| Forensic Premium | B2 WORM backup, PGP signing automation, hash-chain visualization | Core COC hash-chain still writes on every PostToolUse; manual `hash_tracker snapshot` still works; repo/forensics/ tree stays git-tracked |
| Performance Optimization | Token-cost rollups, cache-hit dashboards, compact-risk early warnings, debloat scans | Sessions still run within context; budget_check hook still blocks overbudget writes (core); /compact still available |
| Investigation Accelerators | OSINT/SpiderFoot enrichment, vision-ingest pipelines, PDF render, Obsidian automations | Raw data still ingests via basic 2x clean scripts; manual extraction possible |
| Dashboards & Visibility | Mission-control UI, metrics HTML, flight deck | statusline in footer still works (core); manual `cat hooks/state/*.json` still works |

## 4. Violation Report — Ship Blockers

**Core-to-sauce unwrapped imports (hard blockers):** 1

These are imports from a **core** script to a **sauce** script without try/except protection. On the free tier (sauce absent) these would crash the system.

- `/mnt/d/0LOCAL/.claude/hooks/shared_file_cache.py` line 13: `from shared_file_cache import FileCache`
  - Note: self-referential (script's own module name); not a real production risk, but verify.

**LOAD misclassifications:** 1

- `/mnt/d/0LOCAL/.claude/scripts/shared_file_cache.py` — LOAD misclassified: marked "sauce" but duplicates hooks/shared_file_cache.py which is core
  - **Fix:** change LOAD header from `sauce` to `core` and reconcile with the true core file at `/mnt/d/0LOCAL/.claude/hooks/shared_file_cache.py`.

**Sauce-to-sauce unwrapped imports (lower priority):** 29

These are cross-sauce dependencies. Not ship blockers (both scripts in same tier), but best practice is to wrap them so partial-sauce installs degrade cleanly. See audit JSON `callers_audited` field for full list.

**Fix recipe (per unwrapped import):**

```python
# BEFORE:
from eval_harness import score_run

# AFTER:
try:
    from eval_harness import score_run
    EVAL_AVAILABLE = True
except ImportError:
    EVAL_AVAILABLE = False
    def score_run(*args, **kwargs):  # no-op shim
        return None
```

## 5. Compliance Stats

**Total scripts scanned:** 525

### By status

| Status | Count | Percent |
|---|---|---|
| Compliant (4 headers + tier prefix) | 40 | 8% |
| Missing headers (needs TIER/REPLACES/METRIC/LOAD) | 264 | 50% |
| Missing filename prefix | 220 | 42% |
| LOAD misclassified | 1 | 0% |

### By tier (recommended)

| Tier | Count | Role class |
|---|---|---|
| 0x | 28 | setup |
| 1x | 41 | ingest |
| 2x | 32 | clean |
| 3x | 47 | analysis |
| 4x | 48 | evidence/COC |
| 5x | 36 | publish |
| 6x | 10 | archive |
| 7x | 42 | orchestration |
| 8x | 9 | hooks |
| 9x | 230 | utilities |
| unnumbered | 2 | (needs tier assigned) |

### By load

- **core:** 40 (free tier must-haves)
- **sauce:** 485 (paid tier enhancement)
- **unclassified:** 0 (needs human review)

### By directory

| Directory | Compliant | Total | % |
|---|---|---|---|
| .claude/scripts | 17 | 160 | 11% |
| cybertemplate | 1 | 158 | 1% |
| data-analysis-engine | 14 | 112 | 12% |
| .claude/hooks | 0 | 46 | 0% |
| faerie2 | 8 | 44 | 18% |
| membench | 0 | 5 | 0% |

## 6. Existing Auditor Integration (Deliverable 5)

`9b_equilibrium_audit.py` already scans for TIER/REPLACES/METRIC headers. To produce the schema of `script-equilibrium-audit-2026-04-20.json`, the following additions are needed (patch, not applied):

```diff
+ # Extract LOAD header in addition to TIER/REPLACES/METRIC
+ LOAD_RE = re.compile(r"LOAD\s*[:=]\s*([^\n#]+)", re.I)
+ load_match = LOAD_RE.search(header_block)
+ record["load"] = load_match.group(1).strip() if load_match else None
+ record["load_misclassified"] = check_load_vs_role(record)
+
+ # Cross-caller import audit — for each sauce script, grep callers
+ record["callers_audited"] = scan_sauce_callers(script_path, sauce_stems)
+
+ # Premium-tier classification
+ record["premium_sauce_tier"] = classify_premium(script_name)
+ record["removal_blast_radius"] = compute_blast_radius(record)
```

Caller for follow-up session: `/run` the task "patch 9b_equilibrium_audit.py per PREMIUM-SAUCE-MANIFEST.md section 6". Then subsequent `python3 ~/.claude/scripts/9b_equilibrium_audit.py --check-scripts --json-report` will produce this same audit automatically.

## 7. Next Actions for Researcher

1. **Review rename plan** (436 unprefixed scripts) — follow-up session executes `git mv` + import updates with user approval.
2. **Fix 1 load misclassification** — `/mnt/d/0LOCAL/.claude/scripts/shared_file_cache.py` should be promoted from `sauce` to `core` (duplicates correct core file in hooks/).
3. **Wrap 29 sauce-to-sauce unwrapped imports** (non-blocker but best practice) — follow-up session applies try/except wrapping per fix recipe.
4. **Add LOAD header extraction to `9b_equilibrium_audit.py`** (patch in section 6) so future audits run automatically.
5. **Confirm the 7 bundle definitions** — they map directly to paid-tier SKUs. Any reorg affects billing/feature-gate logic.

---

**Audit files:**

- Full machine-readable audit: `/mnt/d/0LOCAL/.claude/hooks/state/script-equilibrium-audit-2026-04-20.json`
- Rename plan: `/mnt/d/0LOCAL/.claude/hooks/state/script-rename-plan-2026-04-20.json`
- Source rule: `/mnt/c/Users/amand/.claude/rules/core.md` (Script Equilibrium + Core vs Sauce)
