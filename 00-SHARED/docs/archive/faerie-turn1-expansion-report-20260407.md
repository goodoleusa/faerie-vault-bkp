# /faerie Turn-1 Roundup Expansion — Audit Report
**Date:** 2026-04-07 | **Task:** task-20260325-235934-d743 | **Agent:** context-manager

---

## Current Turn-0 Read Sequence (as-implemented)

Step 0 runs all of these in parallel via bash before any Agent spawn:

| Source | Type | Purpose |
|---|---|---|
| `faerie_turn1.py` | Python script | Queue state, brief freshness, stale-claim reset, bundle patch, wave pre-assignment, stigmergy sweep, parallel launch hint, free-model routing |
| `health_check.py` | Python script | System health (6 checks, <1s canary) |
| `session_heartbeat.py read` | Python script | Session presence / stale detection |
| `batch_collect.py` | Python script | Overnight Opus batch results |
| `vault_annotation_sync.py --apply --limit 50` | Python script | Apply pending human vault annotations |
| `faerie-brief.json` / `faerie-brief-sth.json` | JSON | Session brief (membot/handoff vs stop-hook — faerie_turn1 picks fresher) |
| `handoff-snapshot.json` | JSON | Full roundup: project memories, queue snapshot, hypothesis confidence, flags, observations |
| `overnight-synthesis-results.json` | JSON | Opus batch output (silent skip if absent) |
| `eval_harness.py --quick` | Python script | Composite eval score quick check |
| `annotation-sync-state.json` | JSON | pending/applied annotation counts for dashboard |
| `emergency_handoff.py` | Python script | Conditional: runs if brief age > 8h |
| `session_heartbeat.py write` | Python script | Mark session presence after reads |

Context read priority (after bash): handoff-snapshot.json (age<12h) → faerie-brief.json (age<12h) → emergency_handoff output.

---

## Manifest Source Audit

### handoff-snapshot.json
- **Path:** `~/.claude/hooks/state/handoff-snapshot.json`
- **Age (audit time):** Generated 2026-04-07T13:56Z — same day, ~6h before this audit
- **Generator:** `emergency_handoff.py`
- **Size:** 1009KB — **exceeds the Read tool's 256KB limit**
- **Content:** 116 project memory entries, 5841 lines, queue snapshot, hypothesis confidence (H1=0.95, H2=0.78, H3=0.78, H4=0.55, H5=0.0), top_flags (5), recent_observations (2), memory_drain stats
- **GAP:** faerie cannot read this file fully via the Read tool. Only the first ~60 lines are accessible. SKILL.md treats it as a single canonical source ("one file = all project state") but that assumption breaks at this file size. No truncation guard or summary companion exists.

### faerie-brief.json
- **Path:** `~/.claude/hooks/state/faerie-brief.json`
- **Age:** Generated 2026-04-07T14:06Z (fresh)
- **Generator:** `session_stop_hook`
- **Content:** queue counts (20 HIGH, 8 MED, 1 LOW), hypothesis confidence, top_flags (5), blockers (none), recent_observations (2), memory_drain
- **GAP:** The `top_flags` entries in this brief lack `id` fields — they only have `cat` and `summary`. `faerie_turn1.py:_merge_brief_top_flags()` requires a non-empty `id` field to merge a flag into the queue. Result: ALL 5 brief flags are silently dropped every session. The merge is a no-op. This has likely been broken since the brief format was standardized.

### REVIEW-HOT.md
- **Path:** `~/.claude/memory/REVIEW-HOT.md`
- **Age:** Regenerated 2026-04-06T04:32Z — **25h old, stale by 12h policy**
- **Content:** 51 active items: 0 CRITICAL, 41 HIGH, 10 MED
- **GAP:** REVIEW-HOT.md is **not in the faerie Turn-0 read sequence**. The lifecycle rule says agents read it at startup (replacing the 26K REVIEW-INBOX with a ~3K distilled version), but faerie itself does not read it in Step 0. Faerie surfaces flags only through faerie-brief.json top_flags (5 items max), missing 46 active HIGH/MED items. This includes: FLAG-CRITICAL (GitHub PAT in mcp.json), publication blockers, COC chain break, eval composite degrading to 0.33, instrumentation wiring gap.

### REVIEW-INBOX.md
- **Path:** `~/.claude/memory/REVIEW-INBOX.md`
- **Age of most recent meaningful entries:** 2026-03-29 (9 days)
- **Content:** FLAG-CRITICAL: GitHub PAT exposed in mcp.json; 7 FLAG-HIGH items (H1 confidence conflict, T1 evidence unverified, publication blockers, COC chain break)
- **Note:** REVIEW-INBOX is not directly read in Turn-0. It surfaces via faerie-brief.json top_flags only (and that path is currently broken — see above).

### annotation-sync-state.json
- **Path:** `~/.claude/hooks/state/annotation-sync-state.json`
- **Age:** 2026-04-06T22:42Z (~21h)
- **Content:** pending_found: 0, applied: 0 — clean
- **Assessment:** Handled correctly. No gap.

### piston-checkpoint.json
- **Path:** `~/.claude/hooks/state/piston-checkpoint.json`
- **Age:** 2026-04-07T14:03Z (fresh, same day)
- **Content:** last_wave_launched: 0, no agents in flight, queue: 20 HIGH / 9 MED / 1 LOW, resume_instruction: "Launch Wave 1 immediately"
- **GAP:** piston-checkpoint.json is **not in the Turn-0 standard read list** in SKILL.md Step 0. It is only referenced in the Post-Compact Piston Restart section. For a normal cold start (no compaction), faerie has no piston state context. Without this, faerie cannot distinguish a clean cold start from a mid-wave interruption where agents were in flight.

### overnight-synthesis-results.json
- **Status:** FILE DOES NOT EXIST
- **GAP:** SKILL.md reads this in Step 0 bash with `2>/dev/null` — silent skip when absent. Faerie has no way to distinguish "overnight batch never queued" from "batch queued but failed to write results." No dashboard alert when absent after a known overnight queue.

### sprint-progress.json
- **Path:** `~/.claude/hooks/state/sprint-progress.json`
- **Age:** Last updated 2026-03-21 (17 days stale)
- **Content:** Sprint: "Faerie Slim", 64% done, phases P2a/P5/P10 pending, next: P2a faerie_core.py
- **GAP:** sprint-progress.json is not read in Turn-0. Faerie gets task counts but not sprint-level progress percentage or phase name. Phase context would improve wave assignment — sprint-critical tasks should bias toward W2 regardless of category.

### context-calibration.json
- **Path:** `~/.claude/hooks/state/context-calibration.json`
- **Age:** Last updated 2026-03-17 (21 days stale)
- **Content:** correction_factor: 1.1712, 3 observations (all showing 13-40% underestimate)
- **GAP:** context-calibration.json is not in the Turn-0 read list. Without it, faerie uses uncorrected context estimates in the footer from Turn-1 onward. The rule says "memory-keeper reads this before any context estimate" but memory-keeper has not run at Turn-0. Faerie systematically underestimates context by ~17% on heavy sessions.

---

## Gate State Audit (as of 2026-04-07)

### Human Review Gate
- **Active items:** 51 (41 HIGH, 10 MED, 0 CRITICAL)
- **REVIEW-HOT age:** 25h (stale — should be regenerated by membot)
- **Oldest unresolved:** 2026-03-13 (headline re: foreign IPs — 25 days)
- **Status:** STALE + BACKLOGGED

### Publication Gate
Blockers from REVIEW-INBOX (oldest from 2026-03-22):
1. FLAG-CRITICAL: GitHub PAT exposed in `faerie2/mcp.json` — rotate immediately
2. FLAG-HIGH: 18 T1 evidence items, 0 sha256-verified — publication BLOCKED
3. FLAG-HIGH: report.html cert language requires human legal review
4. FLAG-HIGH: COC chain break at master-coc.jsonl entries 742-746
- **Status:** BLOCKED

### Piston Gate
- last_wave_launched: 0, no agents in flight
- **Status:** READY — no stall, launch W1 immediately

### Sprint Gate
- Sprint: "Faerie Slim", 64% complete
- Pending: P2a (faerie_core.py), P5 (Skill consolidation), P10 (HONEY split)
- **Status:** IN PROGRESS

### Annotation Gate
- pending_found: 0, applied: 0
- **Status:** CLEAN

---

## Active Plan Assessment

**Queue:** 20 HIGH / 9 MED / 1 LOW | 0 running | 3 done

**Critical path (top 3 HIGH tasks):**
1. `task-20260407-pat-rotation` — GitHub PAT rotation (OVERDUE since 2026-03-28, blocks publication push)
2. `task-20260407-publish-commit` — Final commit + push H1+H3 narratives to GitHub
3. `task-20260402-opt-a-d-parallel` — OPT-A+D parallel W1+W2 + circuit breaker (30s/cycle savings)

**This task** (`task-20260325-235934-d743`) is assigned W2 via wave pre-assignment in faerie_turn1.py.

**No active blockers** in piston-checkpoint (stalled agents: none).

**Hypothesis confidence:** H1=0.95, H2=0.78, H3=0.78, H4=0.55, H5=0.0

---

## Expansion Recommendations

### REC-1 (HIGH): Add piston-checkpoint.json to Turn-0 standard reads

**Gap closed:** faerie cannot distinguish clean cold start from mid-wave interruption.

**Implementation:** Add to Step 0 bash:
```bash
cat ~/.claude/hooks/state/piston-checkpoint.json 2>/dev/null
```
Add to context read priority: after handoff-snapshot.json, before brief fallback. Include `resume_instruction` and `agents_in_flight` in dashboard if wave was interrupted.

---

### REC-2 (HIGH): Add REVIEW-HOT.md to faerie Step 0 reads

**Gap closed:** 46 active HIGH/MED review items invisible to faerie at session start.

**Implementation option A (simpler):** Add to Step 0 bash:
```bash
cat ~/.claude/memory/REVIEW-HOT.md 2>/dev/null
```
Check age — if >12h, faerie_turn1.py should include `review_hot_stale: true` in its output, triggering a membot regeneration task.

**Implementation option B (lower token cost):** faerie_turn1.py reads REVIEW-HOT.md and includes top-5 HIGH items in its JSON output, so faerie only sees a 200-token summary rather than the full 3K file.

---

### REC-3 (HIGH): Fix top_flags id field in faerie-brief.json

**Gap closed:** _merge_brief_top_flags() is silently a no-op every session.

**Root cause:** `session_stop_hook` writes `top_flags` entries without an `id` field. `faerie_turn1.py` requires `id` to prevent duplicate flag tasks.

**Implementation:**
- In `session_stop_hook.py` (or wherever top_flags are written): derive `id` from `f"{cat}-{ts_hash8}"` pattern.
- OR: relax `_merge_brief_top_flags()` to use `f"{flag['cat']}-{hash(flag['summary'])}"` as id when `id` is absent.

The second option is a one-line fix in faerie_turn1.py with no dependency on brief format changes.

---

### REC-4 (MED): Embed context-calibration correction_factor in faerie_turn1.py output

**Gap closed:** faerie underestimates context by ~17% on heavy sessions from Turn-1.

**Implementation:** In `faerie_turn1.py main()`, read context-calibration.json and include:
```json
"context_calibration": {
  "correction_factor": 1.1712,
  "last_updated": "2026-03-17",
  "note": "apply: corrected_pct = raw_pct * correction_factor"
}
```
faerie applies it to headroom calculation in the status footer.

---

### REC-5 (MED): Add sprint-progress.json to faerie_turn1.py reads

**Gap closed:** faerie wave assignment is blind to sprint critical path.

**Implementation:** faerie_turn1.py reads `~/.claude/hooks/state/sprint-progress.json`, includes `sprint_name`, `progress_pct`, `next_phase` in its JSON output. faerie displays in dashboard and can bias wave assignment: if a task's goal matches `next_phase`, promote to W2.

---

### REC-6 (LOW): Add handoff-snapshot.json summary companion file

**Gap closed:** 1009KB file exceeds Read tool limit; faerie can only see first ~60 lines.

**Implementation:** `emergency_handoff.py` writes a companion `handoff-snapshot-summary.json` (<50KB) containing only:
- queue counts + top 3 HIGH tasks
- hypothesis_confidence
- top_flags (5 items with id, cat, summary)
- recent_observations (3 items)
- blockers
- memory_drain summary

SKILL.md reads summary file at Step 0; full snapshot available for agent deep-dive on demand.

---

### REC-7 (LOW): Overnight synthesis missing-file alert

**Gap closed:** silent skip when overnight batch results are absent after a known batch was queued.

**Implementation:** `batch_collect.py` should output a status field indicating whether a batch was queued overnight. `faerie_turn1.py` checks: if batch was queued AND results file absent → include `overnight_batch_alert: "results missing"` in output.

---

## Performance Bottleneck Assessment

| Bottleneck | Severity | Notes |
|---|---|---|
| handoff-snapshot.json at 1009KB | HIGH | Exceeds read tool limit; faerie reads ~6% of file |
| REVIEW-HOT not in Turn-0 sequence | HIGH | 46 active items invisible at session start |
| top_flags id bug — merge is no-op | HIGH | Brief flags never enter queue |
| piston-checkpoint not in Step 0 | MED | Resumption context missing on cold starts |
| context-calibration not applied at T0 | MED | 17% systematic underestimate on heavy sessions |
| sprint-progress not read | LOW | Phase context missing from wave assignment |

---

## Files Referenced

- `/mnt/d/0local/gitrepos/faerie2/.claude/skills/faerie/SKILL.md` — Turn-0 execution flow
- `/mnt/c/Users/amand/.claude/hooks/state/faerie_turn1.py` — State machine (694 lines)
- `/mnt/c/Users/amand/.claude/hooks/state/faerie-brief.json` — Session brief (fresh)
- `/mnt/c/Users/amand/.claude/hooks/state/handoff-snapshot.json` — Full roundup (1009KB)
- `/mnt/c/Users/amand/.claude/hooks/state/piston-checkpoint.json` — Wave state
- `/mnt/c/Users/amand/.claude/hooks/state/annotation-sync-state.json` — Annotation gate
- `/mnt/c/Users/amand/.claude/hooks/state/sprint-progress.json` — Sprint phase state
- `/mnt/c/Users/amand/.claude/hooks/state/context-calibration.json` — Context correction factor
- `/mnt/c/Users/amand/.claude/memory/REVIEW-HOT.md` — Distilled active review items (51)
- `/mnt/c/Users/amand/.claude/memory/REVIEW-INBOX.md` — Full review inbox (publication blockers)
- `/mnt/c/Users/amand/.claude/hooks/state/sprint-queue.json` — Task queue (20 HIGH / 9 MED / 1 LOW)

---

*Generated by context-manager agent | task-20260325-235934-d743 | 2026-04-07*
