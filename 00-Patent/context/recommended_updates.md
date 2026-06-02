# Recommended Updates — Mission Architecture Enforcement

**task_id:** mission-architecture-enforcement
**investigation_label:** mission-architecture-enforcement
**bearing:** N (north — unblock infrastructure prerequisites first), then E (parallel field rollout), then S (proceed to charter implementation)

This list is ordered to **respect the FUNDAMENTAL GOVERNANCE RULE**: rename/wire-fix work first (no abstractions added, equilibrium preserved), then schema-extension work that requires mutation discipline (baseline → fix → measure).

---

## Tier A — Hygiene Fixes (No New Abstractions, Safe to Apply)

These align references to scripts that already exist; no behavioral mutation, no measurement required because nothing currently runs.

### A1. Replace broken `5x_b2_realtime_uploader.py` reference

**File:** `/mnt/d/0local/gitrepos/faerie2/.claude/settings.json:79`
**Current:**
```json
"command": "python3 /mnt/d/0local/gitrepos/faerie2/hooks/5x_b2_realtime_uploader.py --async 2>/dev/null || true"
```
**Fix:**
```json
"command": "python3 /mnt/d/0local/gitrepos/faerie2/hooks/0x_b2_realtime_uploader.py --async 2>/dev/null || true"
```

**File:** `/mnt/d/0LOCAL/.claude/settings.json:81`
**Current:**
```json
"command": "python3 /mnt/d/0local/gitrepos/faerie2/hooks/5x_b2_realtime_uploader.py --verify-queued 2>/dev/null || true"
```
**Fix:**
```json
"command": "python3 /mnt/d/0local/gitrepos/faerie2/hooks/0x_b2_realtime_uploader.py --verify-queued 2>/dev/null || true"
```

**Verification before fix:** confirm `0x_b2_realtime_uploader.py` actually accepts `--async` and `--verify-queued` (read its argparse). If it does not, leave the wires removed and add an issue.

### A2. Remove broken `9x_forensic_signer.py` wire

**File:** `/mnt/d/0LOCAL/.claude/settings.json:128`

Either:
- (a) **Delete** the entire hook block (lines 124-133) since the signer does not exist; OR
- (b) **Replace** with the actual Ed25519 signer if a real one exists (search needed; not found in this audit).

Recommendation: **option (a)** — remove the wire, file an issue for re-implementing `9x_forensic_signer.py` if signing is still required by the contract.

### A3. Remove broken `5x_b2_manifest_uploader.py` wire

**File:** `/mnt/d/0LOCAL/.claude/settings.json:182-191`

The hook references `5x_b2_manifest_uploader.py --realtime`. The actual realtime path goes through `0x_b2_realtime_uploader.py`. Either:
- (a) Remove this PreToolUse block (manifests are already promoted via PostToolUse `0x_promote_to_forensics.py` + B2 queue); OR
- (b) Point at `0x_b2_realtime_uploader.py` if its CLI supports the manifest-only path.

### A4. Remove dangling symlink

```bash
rm /mnt/d/0LOCAL/.claude/scripts/7x_queue_ops.py
```
(Confirms the deletion intended in commit `eee3d83`.)

### A5. Update header comments referring to deleted scripts

These hooks document `7x_queue_ops.py` / `7x_mission_graph_ops.py` / `9x_queue_janitor_scout.py` as collaborators but the targets are gone. Since the hooks are not currently wired in settings.json, the references are stale comments only. Recommended: add a `# DEPRECATED 2026-04-26` banner in the docstring of each:

- `/mnt/d/0local/gitrepos/faerie2/hooks/8x_taskcreate_to_queue.py` (line 11, 30, 60, 95, 118)
- `/mnt/d/0local/gitrepos/faerie2/hooks/8x_compass_native_bridge.py` (line 23, 44)
- `/mnt/d/0local/gitrepos/faerie2/hooks/9x_intent_to_mission_graph.py` (line 14, 35, 177)
- `/mnt/d/0local/gitrepos/faerie2/hooks/8x_mission_janitor_rotation.py` (line 15, 59)
- `/mnt/d/0local/gitrepos/faerie2/hooks/manifest_task_autocompletion.py` (line 40, 62)
- `/mnt/d/0LOCAL/.claude/hooks/4x_manifest_task_autocompletion.py` (line 40, 62)
- `/mnt/d/0LOCAL/.claude/hooks/8x_taskcreate_to_queue.py` (line 11, 30, 60, 95, 118)

### A6. Fix `0x_compass_query.py` relative-path bug

**File:** `/mnt/d/0local/gitrepos/faerie2/scripts/0x_compass_query.py:27`

**Current:**
```python
manifests_dir = Path("forensics/manifests")
```
**Fix:** anchor to repo root and accept date-stratified subdirs (which is the actual layout per CLAUDE.md):
```python
REPO_ROOT = Path(__file__).resolve().parents[1]
manifests_dir = REPO_ROOT / "forensics" / "manifests"
```
**Also:** loop over date subdirs is correct on line 32-35; the bug is only the relative-path resolution. Live test on 2026-04-29 returned `total_tasks: 0` because of this.

---

## Tier B — Schema Bridges (Dual-Write, No Reader Breakage)

These are non-breaking field-additions: write both the legacy field and the canonical field, allow consumers to migrate independently. Per FUNDAMENTAL GOVERNANCE RULE, baseline mutation discipline applies — measure before/after via `mutation_verification_pass_rate`.

### B1. Introduce `next_mission_node` dict alongside `next_task_queued` string

**Producers to update:** every spawn-template path that emits a manifest skeleton.

**Schema (canonical model 44):**
```json
{
  "next_mission_node": {
    "bearing": "S",
    "task_id": "docs-consolidation-phase-2",
    "from_label": "faerie2-shipping",
    "to_label": "docs-consolidation"
  },
  "next_task_queued": "docs-consolidation-phase-2",
  "compass_edge": "S",
  "investigation_label": "faerie2-shipping"
}
```

**Migration discipline:**
- Phase 1: write both fields (dual-write); readers continue to read string fields.
- Phase 2: introduce optional reads of `next_mission_node` in consumers (`0x_mission_graph.py --query open-edges`, `0x_compass_query.py`, `1x_mission_crystallizer.py`).
- Phase 3: when 100% of producers emit dict form for ≥7 days with verification metric ≥ 0.95, deprecate string field.

**Baseline measurement required:** before Phase 1, capture current count of manifests with `next_task_queued != null` per day. After Phase 1, capture count with `next_mission_node != null AND next_task_queued != null`. Pass criterion: 100% dual-write rate.

### B2. Add `from_label` to manifest schema

`investigation_label` answers "which mission am I currently in." For dead-reckoning, agents also need `from_label` (the mission they came FROM, e.g., the previous manifest's `to_label`) and `to_label` (the mission `next_task_queued` targets).

**Producer:** `0x_spawn_template.py` injects `from_label` from spawn-time bundle (the parent manifest's `investigation_label`). `to_label` is computed at manifest-write time when the agent commits a `next_task_queued`.

---

## Tier C — Charter Layer Implementation (Requires Baseline Measurement)

Before adding any of the following, a baseline must be measured per FUNDAMENTAL GOVERNANCE RULE:
- N = manifests written per session, current
- M = manifest count per investigation_label cluster, current
- Q = avg quality_score per cluster, current

After charter is added, re-measure same metrics. Charter is beneficial only if Q increases or N stabilizes around an explicit deadline-bounded count.

### C1. Create `genesis_manifests/{YYYY-MM-DD}/{charter_id}.json`

Schema per doc 44:
```json
{
  "charter_id": "faerie2-v1.0-shipping",
  "investigation_labels": ["faerie2-shipping", "docs-consolidation", "vault-setup"],
  "scope": "Ship faerie2 v1.0 to production",
  "deadline": "2026-04-29",
  "map_boundary": "All missions reachable from faerie2-shipping via south edges",
  "deliverables": [
    {"task_id": "ship-releases-build", "must_complete": true},
    {"task_id": "ship-install-safety-audit", "must_complete": true}
  ],
  "success_criteria": {
    "manifest_count_min": 10,
    "avg_quality_score_min": 0.75,
    "blocking_issues": 0
  }
}
```

### C2. Implement `--charter` flag in `0x_spawn.py`

```python
parser.add_argument("--charter", help="Path to genesis_manifest.json or charter_id")
```

Loads charter, sets `charter_boundary = charter.investigation_labels`, restricts bundle discovery to that set.

### C3. Implement `1x_mission_crystallizer.py --charter-close`

When all charter `deliverables` are met, write `crystallization_metrics.json` snapshot of MAP at charter close. Do NOT delete missions from MAP — charter close is a snapshot, MAP continues evolving.

---

## Tier D — Consider Wiring Currently-Unwired Stigmergy Hooks (Per-Hook Mutation Discipline)

These hooks exist with proper headers and TIER markers but are not wired. **Each requires its own baseline + post-fix measurement before wiring** per FUNDAMENTAL GOVERNANCE RULE.

| Hook | Purpose | Suggested Trigger |
|------|---------|-------------------|
| `8x_manifest_first_guardian.py` | Validates manifest contains `dashboard_line`, `compass_edge` | PreToolUse `Write` matcher on manifest paths |
| `9x_droplet_live_sync.py` | Maintains droplet investigation_label index | PostToolUse `Write` on `*droplet*` filenames |
| `8x_vault_mutation_tracker.py` | Hash-tracks vault doc mutations per CLAUDE.md mandate | PostToolUse `Write` on `vault/**` |
| `8x_convergence_detector.py` | Auto-queues synthesizer when compass_w siblings complete | SubagentStop |
| `8x_mission_completion_synthesizer.py` | Closes mission cluster, writes synthesis | SubagentStop conditional |
| `9x_intent_to_mission_graph.py` | Auto-adds mission node when user prompt is concrete | UserPromptSubmit (already designed for it; disabled per docstring line 20-21) |

For each, the canonical sequence is:
1. Measure baseline (1 session, current behavior).
2. Wire the hook in settings.json.
3. Measure 3 sessions with hook on.
4. Compute delta per FUNDAMENTAL GOVERNANCE RULE.
5. Keep wire if delta is positive; remove and document if neutral or harmful.

---

## Order of Operations (Suggested)

1. **Now (no risk):** Tier A1, A4, A5, A6 (rename and remove dangling references).
2. **Next session (low risk):** A2, A3 (remove or replace broken hook wires).
3. **After 1-week baseline:** Tier B1+B2 (dual-write `next_mission_node`).
4. **After charter consensus + 1-week baseline:** Tier C (charter layer).
5. **Ongoing per-hook:** Tier D (wire stigmergy hooks one at a time with measurement).

## Asks for User

- Confirm whether `9x_forensic_signer.py` should be re-implemented (Implementation Rule #4 requires Ed25519 signing) or struck from the contract.
- Confirm `5x_b2_*` family naming intent: did the B2 lifecycle rename leave `0x_b2_realtime_uploader.py` as the canonical name?
- Confirm whether the CHARTER layer is Q2 work (after v1.0 ship) or pre-ship.
