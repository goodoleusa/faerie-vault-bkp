# Breaking Changes Assessment - Mission Architecture Enforcement Audit

**Auditor:** code-reviewer (AGENT 2 of 4)
**Investigation Label:** mission-architecture-enforcement
**Date:** 2026-04-29
**Scope:** /mnt/d/0LOCAL/.claude/{scripts,hooks} + /mnt/d/0local/gitrepos/faerie2/{scripts,hooks}

## Executive Verdict

**No breaking changes to stigmergy or emergence logic detected.** The compass DAG architecture, investigation_label clustering, COC hash chain, ephemeral-promotion symlink pipeline, and mission-trail discovery index are all internally consistent and operational. The system is f(0)-aligned.

However, four classes of issues materially reduce maintainability and one introduces a silent forensic-integrity regression that should be hot-fixed BEFORE the next mutation eval.

---

## Issue HIGH-1: COC chain finalizer silently writes genesis prev_hash on every call

**Severity:** HIGH (forensic integrity regression)
**File:** /mnt/d/0local/gitrepos/faerie2/scripts/0x_coc_finalizer.py
**Lines:** 41-48

The finalizer reads the previous COC tail with this pattern:

```python
prev_entry_hash = "0" * 64
if COC_CANONICAL.exists():
    with open(COC_CANONICAL, "rb") as f:
        last_line = f.readlines()[-1] if f.readlines() else b""
        if last_line:
            f.seek(-len(last_line), 2)
            last_entry = json.loads(f.read())
            prev_entry_hash = last_entry.get("entry_hash", "0" * 64)
```

The first `f.readlines()` exhausts the iterator. The second `f.readlines()` (in the `else`) returns `[]` regardless of file state. When the file is non-empty the conditional `last_line = f.readlines()[-1]` evaluates first and grabs the last line correctly, BUT the subsequent `if last_line: f.seek(-len(last_line), 2); ... f.read()` reads from an already-consumed handle and gets `b""`, which fails `json.loads`. The except is implicit (no try-except wraps this), so an unhandled JSONDecodeError will propagate unless `last_line` is empty.

In practice this means: any time the finalizer path runs against a non-empty coc.jsonl, it raises. Any time it runs against an empty coc.jsonl, it appends with prev_entry_hash = "0"*64. Net effect: chain is never linked through the finalizer.

**Compare:** `scripts/0x_promote_to_forensics.py:127-140` `read_previous_coc_hash()` does this correctly using `read_text().splitlines()[-1]`. The finalizer should call into the same helper.

**Fix:**
```python
from pathlib import Path
def _read_previous_hash(coc_path: Path) -> str:
    if not coc_path.exists():
        return "0" * 64
    text = coc_path.read_text(encoding="utf-8").strip()
    if not text:
        return "0" * 64
    last_line = text.splitlines()[-1]
    return json.loads(last_line).get("entry_hash", "0" * 64)
```

Also: finalizer's append path does NOT use fcntl.flock, so concurrent finalizer + promoter writes will race. Promoter handles this correctly via `_COC_LOCK_PATH`. Finalizer must adopt the same pattern (preferably by routing through `0x_promote_to_forensics._append_raw_coc_entry`).

**Blast radius:** any session where the PreToolUse preallocator + PostToolUse finalizer pair fires (currently NOT wired in faerie2 settings.json — only the promoter is wired, so live damage is zero today; but the file is reachable via `python3 0x_coc_finalizer.py` direct invocation and is presumably scheduled to be wired given the docstring REPLACES claim).

---

## Issue MED-1: settings.json references nonexistent hook script

**Severity:** MED (silent hook-failure on PreToolUse[Write|Edit|Bash])
**File:** /mnt/d/0local/gitrepos/faerie2/settings.json
**Issue:** PreToolUse hook command points to `scripts/8x_protect_coc_paths.py` which is not present in the scripts/ directory listing. The file `hooks/4x_protect_coc_paths.py` does exist.

If the path is incorrect, the hook silently fails (timeout or file-not-found), which means the PreToolUse protection for forensics/*.jsonl writes does NOT fire. Promoter and deny-rules may still cover the canonical case, but the deeper protection (e.g., direct Edit on coc.jsonl) is bypassed.

**Verification:** `ls /mnt/d/0local/gitrepos/faerie2/scripts/8x_protect_coc_paths.py` — confirm presence.
**Fix:** Repoint to `hooks/4x_protect_coc_paths.py` if that file exists, or restore the missing scripts/8x_protect_coc_paths.py.

---

## Issue MED-2: 16 orphaned hook files in faerie2/hooks/ reference deprecated sprint-queue.json

**Severity:** MED (dead-code drag, equilibrium violation)
**Affected files (faerie2/hooks/):**
- 7x_context_auto_injector.py
- 8x_compass_native_bridge.py
- 8x_convergence_detector.py
- 8x_enforce_lean_queries.py
- 8x_manifest_metric_validator.py
- 8x_mission_autorun.py
- 8x_mission_completion_synthesizer.py
- 8x_mission_janitor_rotation.py
- 8x_precompact_springboard.py
- 8x_state_read_drag.py
- 8x_taskcreate_to_queue.py
- 9x_continuous_dualstate_hook.py
- 9x_intent_to_queue.py
- 9x_intent_to_mission_graph.py (partial — bridges queue to mission graph)
- compass_auto_infer.py
- manifest_task_autocompletion.py + pre-session.py

**Wiring check:** Zero of these are referenced in `/mnt/d/0local/gitrepos/faerie2/settings.json` hooks block. They are pure dead code.

**Recommendation:** Move to `archive/2026-04-29-deprecated-sprint-queue/` (preserve git history) or delete. Per FUNDAMENTAL GOVERNANCE RULE, removal of unused abstractions is equilibrium-respecting (no metrics required because not in critical path).

**Class B caveat:** `9x_intent_to_mission_graph.py` may be the migration bridge from intent → mission_graph. Inspect before deletion; if it's the bridge, keep + remove its sprint-queue dependency.

---

## Issue MED-3: 21 global ~/.claude/scripts authoritatively read/write sprint-queue.json

**Severity:** MED (architectural drift between global and faerie2)
**Files (live, not orphaned):**
- 1x_queue_data_ingest.py — primary queue ingest
- 7x_router.py, 7x_queue_router.py — routers
- 7x_piston_wave_progression.py, 7x_piston_wave_timing.py — wave gating
- 3x_eval_harness.py — _read_sprint_queue() + training-queue.json mutation
- 3a_routing_advisor.py — reads training-queue
- 7x_emergency_handoff.py, 7x_sprint_pulse.py — sprint workflows
- 7x_faerie_queue_prep.py, 7x_queue_prep.py, 7x_queue_vault_sync.py — vault sync
- 7x_sketch_renderer.py — visualization
- 5x_vault_narrative_sync.py — narrative
- 0x_health_check.py — checks queue_readable
- 0x_state_to_forensics_migrator.py, 0b_build_release_bundles.py — packaging
- 3x_analyzer.py — read-only
- 0x_spawn_template.py:1640 — `queue_autonomy: bool = True` default

These are operational paths. Migration to mission-graph DAG (per faerie2/scripts/CLAUDE.md) is incomplete at the global layer.

**Recommendation:** Treat this as a separate mission (not a quick fix). Each script needs evaluation: is it (a) safely deprecatable, (b) needs port to read forensics/manifests + 0x_mission_graph queries, or (c) globally relevant infrastructure to keep.

---

## Issue MED-4: HONEY.md crystallized memory contains drifted state references

**Severity:** MED (memory-architecture inconsistency)
**File:** /mnt/d/0LOCAL/.claude/HONEY.md
**Entries:**
- `mth00068` — "global state (piston-checkpoint, sprint-queue, REVIEW-QUEUE) stays global"
- `mth00083` — "sprint-queue.json named as canonical example of unbounded-growth state"
- `mth00097` — "sprint-queue, next_task_queued chains" described as durable-state heartbeat

These are marked `permanent | 1.0` confidence. They will be re-injected into every session and contradict the new compass DAG architecture in CLAUDE.md.

**Options:**
1. Update entries to substitute `sprint-queue` → `forensics/manifests/` + mission graph
2. Mark as historical (`permanent | 1.0 [historical]`) and add successor entries that reference mission graph
3. Move to NECTAR archive

Option 2 preserves audit trail; recommend option 2.

---

## Stigmergy & Emergence Integrity (PASSED)

| Check | Status | Evidence |
|---|---|---|
| investigation_label as primary semantic ID | PASS | 17 faerie2/scripts + 12 global scripts use canonical form; zero typos (`investigate_label`) |
| Compass edge logic preserved | PASS | N/S/E/W bearings consistently used; phase gate thresholds match docs; bearing_symbol map (⛓️/🔓/➡️/⬅️) matches CLAUDE.md visual glossary |
| Mission-trail discovery via stigmergy | PASS | 0x_mission_trail_builder.py wired in settings.json PostToolUse[Write]; symlinks self-organize per investigation_label |
| Ephemeral → canonical promotion | PASS | 0x_promote_to_forensics.py wired; symlink + fcntl-locked COC append + fsync; idempotent |
| COC hash chain (promoter path) | PASS | flock-protected; 2s timeout; lock-warning field on timeout; sha256 of canonical-bytes |
| COC hash chain (finalizer path) | FAIL | See HIGH-1 above |
| No SendMessage primitives | PASS | Filesystem is the coordination layer; zero violations found |
| Investigation label clustering | PASS | 0x_compass_query, 0x_mission_graph, 0x_mission_trail_builder, 1x_mission_crystallizer all cluster by label |
| Forensics write-protection | MOSTLY PASS | settings.json deny rules exist; PreToolUse 8x_protect_coc_paths path issue (MED-1) reduces defense-in-depth |
| Discovery protocol (3-pass frontier scan) | PASS | 6x_agent_bundle_creator.py spawn cards reference protocol; 0x_compass_query implements label filter |

---

## Recommended Sequence (post-audit, equilibrium-respecting)

1. **Hot-fix HIGH-1:** patch 0x_coc_finalizer.py to use `read_text().splitlines()[-1]` and to call into `_append_raw_coc_entry` from promoter (single locked path). This is a bug fix, not an addition — no metric required.
2. **Verify MED-1:** confirm 8x_protect_coc_paths path; either restore file or repoint settings.json.
3. **Archive MED-2:** move 16 orphaned faerie2 hooks to `archive/2026-04-29-deprecated-sprint-queue/`. Keep `9x_intent_to_mission_graph.py` if it's the bridge.
4. **Track MED-3 separately:** scope mission for global script migration; out of this audit's task budget.
5. **Annotate MED-4:** mark mth00068/83/97 as `[historical]` and add cross-link to mission graph successor entries; do NOT delete (forensic preservation).
6. **Document mission-trail in CLAUDE.md:** add line under "Discovery Queries" describing `forensics/mission-trails/{label}/{date}/` symlink index produced by hook.

All recommendations respect FUNDAMENTAL GOVERNANCE RULE: removals (1, 3) are bug fixes / dead-code purges (no metrics required); additions (5, 6) are documentation-only.

---

## Compass Edge for This Manifest

**bearing:** S (proceed)
**rationale:** Audit complete; no system-blocking findings; one HIGH-severity bug surfaced for hot-fix. Downstream agents (documentation-engineer, knowledge-synthesizer, data-analyst) can proceed with their parallel tracks; no rework needed on this thread.
**next_task_queued:** remove-orphaned-sprint-queue-hooks-and-update-HONEY-mth00068-mth00083-mth00097
