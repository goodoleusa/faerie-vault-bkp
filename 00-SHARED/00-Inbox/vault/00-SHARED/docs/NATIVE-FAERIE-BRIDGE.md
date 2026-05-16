---
type: architecture
status: design-proposal
created: 2026-04-23
task_id: native-faerie-bridge-20260423
tags: [bridge, task-tool, stigmergy, queue, hooks, f0]
parent: "[[ARCHITECTURE]]"
up: "[[ARCHITECTURE]]"
sibling: ["[[INVISIBLE-QUEUE-INTEGRATION]]", "[[QUEUE-CLAIMING-ARCHITECTURE]]", "[[DAILY-HOOKS-SCRIPTS-WIRING]]"]
same: ["[[INVISIBLE-QUEUE-INTEGRATION]]"]
child: []
down: []
doc_hash: sha256:pending
hash_ts: 2026-04-23
hash_method: body-sha256-v1
---

> [↑ Parent](./ARCHITECTURE.md) · [← Prev](./INVISIBLE-QUEUE-INTEGRATION.md) · [→ Next](./QUEUE-CLAIMING-ARCHITECTURE.md) · [⌂ Index](./README.md)

# Native-Faerie Bridge — Task Tool ↔ sprint-queue.json

**Task_id:** `native-faerie-bridge-20260423`
**Status:** Design (existing partial implementation identified; consolidation needed)
**Supersedes (in part):** `docs/INVISIBLE-QUEUE-INTEGRATION.md` (design), `docs/archive/faerie-task-sync-bridge-design.md` (2026-04-07 proposal). Does **not** supersede `docs/QUEUE-CLAIMING-ARCHITECTURE.md` (claim semantics still authoritative).

---

## 1. Problem Statement

Two parallel task systems exist. Neither knows the other exists.

| System | Owner | Persistence | Scope | Visibility |
|---|---|---|---|---|
| Native Task (TaskCreate/TaskUpdate/TaskList) | Claude Code CLI | session-scoped (`/tmp/claude-{uid}/{project}/{session_id}/tasks/`) | main session | IDE pane |
| Faerie sprint-queue | faerie + `queue_ops.py` | persistent (`~/.claude/hooks/state/sprint-queue.json`) | cross-CLI | agent-facing |

**Consequence:** TaskCreate on main never enters the faerie queue; `queue_ops.py complete` never flips native Task status; after `/compact` or session end, faerie loses visibility of native work. Sprint velocity undercounted, tasks duplicated, manual reconciliation burned at every faerie startup.

This is the canonical "two rooms, no wire" problem laid out in `docs/archive/faerie-task-sync-bridge-design.md` (2026-04-07).

---

## 2. Current State — What Already Exists

### 2.1 Native Task persistence (investigated)

Claude Code writes native task output streams to:

```
/tmp/claude-{uid}/{project-slug}/{session_id}/tasks/{task_run_id}.output
```

Each `.output` file is either:
- A symlink to `~/.claude/projects/{project}/{session_id}/subagents/agent-{hash}.jsonl` (for Agent-tool spawns), or
- A plain file containing TaskUpdate output for main-session TodoWrite-style tasks.

**No JSON task-state object** is written in `/tmp/claude-{uid}/**/tasks/` — only `.output` streams. The structured task state (id, subject, status, priority) is held by the Claude Code process in memory and surfaced via the `TaskList` tool. **Scripts cannot read the native task registry from the filesystem directly.**

This invalidates the approach taken by `scripts/sync_queue_from_tasks.py` and `scripts/task_bridge.py`, both of which assume `~/.claude/tasks/` holds structured per-task JSON. That assumption is wrong on this platform (Claude Code on WSL, session_id 6175d565..., 2026-04-23). Those scripts are harmless no-ops today.

### 2.2 Bridge scripts already on disk (partial implementations)

| Path | Status | Purpose | Fitness |
|---|---|---|---|
| `/mnt/d/0LOCAL/.claude/hooks/8x_taskcreate_to_queue.py` | present | PostToolUse on `TaskCreate` → append to `sprint-queue.json` | **viable** — correctly gated on `tool=='TaskCreate'` + `manifest.status=='final'`; dedup by id |
| `/mnt/d/0LOCAL/.claude/hooks/manifest_task_autocompletion.py` | present | PostToolUse on `Agent` → `queue_ops.py complete` + `queue_sync.py --sync-complete` | **wired** — referenced in logic but settings.json does not yet register it |
| `/mnt/d/0LOCAL/.claude/hooks/populate_queue_from_tasklist.py` | stub | No-op; can't read TaskList from disk | obsolete |
| `scripts/task_bridge.py` | stub | Reads `~/.claude/tasks/` (doesn't exist) | obsolete |
| `scripts/sync_queue_from_tasks.py` | stub | Same — reads non-existent dir | obsolete |
| `scripts/queue_sync_bridge.py` | stub | Calls `task_bridge.get_all_tasks()` which returns `[]` | obsolete |
| `scripts/queue_sync.py` | partial | `QueueSyncBridge` class; `sync_complete_to_tasklist` writes to `task-list-cache.json` (file that is never produced) | **partial** — completion half works; pending-sync half is broken |

### 2.3 What's wired in `settings.json`

**Currently wired PostToolUse hooks** (`/mnt/d/0LOCAL/.claude/settings.json`, lines 147–224):
- `forensic_coc.py posttool` on `Read|Write|Edit|Bash|Agent`
- `8x_roster_update.py` on `Agent`
- `memory_collector.py` on `Write|Edit`
- `8x_vault_write_gate.py` on `Write|Edit`
- `5x_post_vault_write_stamp.py` on `Write`
- `8x_dashboard_generator.py` on `Agent`
- `9x_forensic_signer.py` on `Write|Edit`

**Not wired:**
- `8x_taskcreate_to_queue.py` (no matcher registered for `TaskCreate`)
- `manifest_task_autocompletion.py` (logic exists but settings.json does not call it — it is referenced in `INVISIBLE-QUEUE-INTEGRATION.md` implementation checklist as "pending")
- Anything on `TaskUpdate` / `TaskList`

### 2.4 Prior docs

- `docs/INVISIBLE-QUEUE-INTEGRATION.md` — 2026-04 design doc for the invisible-queue pattern. This doc's "Implementation Checklist" (lines 186–202) is still all unchecked. **Partially superseded by this doc's consolidated hook design.**
- `docs/archive/faerie-task-sync-bridge-design.md` — 2026-04-07 design narrative for `task-sync-bridge.py`. Conceptually sound but depended on a `~/.claude/tasks/` filesystem view that does not exist. **Superseded.**
- `docs/QUEUE-CLAIMING-ARCHITECTURE.md` — claim-state machine. **Still authoritative for queue semantics.**
- `docs/task-droplet-architecture.md` — task-linked droplets for stigmergic discovery. **Orthogonal to bridge — keep.**
- `docs/ARCHITECTURE_QUEUE_CLAIMING.md` — implementation doc for queue claiming. **Still authoritative.**

### 2.5 Memory-collector hook — Task event handling

`memory_collector.py` (PostToolUse on `Write|Edit`) fires only on file-path writes in `.claude/projects/*/memory/`. It does **not** hook Task events. No pollen MEM block is currently produced on TaskCreate / TaskUpdate.

---

## 3. Design — Single Hook, Two Directions

### 3.1 Name & tier

**New script:** `scripts/8x_task_bridge_hook.py`
**Tier:** `8x_` (PostToolUse hook)
**LOAD:** `core` (queue integrity depends on it)
**REPLACES:** `scripts/task_bridge.py`, `scripts/sync_queue_from_tasks.py`, `scripts/queue_sync_bridge.py` (all three are stubs built on the wrong filesystem assumption); consolidates the `TaskCreate` branch of `/mnt/d/0LOCAL/.claude/hooks/8x_taskcreate_to_queue.py` and the TaskList-sync branch of `scripts/queue_sync.py` into one handler.
**METRIC:** 100% of `TaskCreate|TaskUpdate` PostToolUse events result in a corresponding mutation to `sprint-queue.json` within 200 ms, and 100% of `TaskUpdate status=completed` events result in a `DECISION` or `HANDOFF` MEM block in `pollen-{SID}.md`.

### 3.2 Event wiring

Add to `/mnt/d/0LOCAL/.claude/settings.json` under `hooks.PostToolUse`:

```jsonc
{
  "matcher": "TaskCreate|TaskUpdate|TaskList",
  "hooks": [
    {
      "type": "command",
      "command": "python3 /mnt/d/0local/gitrepos/faerie2/scripts/8x_task_bridge_hook.py",
      "timeout": 3,
      "statusMessage": "Bridging task to faerie queue..."
    }
  ]
}
```

The existing `manifest_task_autocompletion.py` (on PostToolUse `Agent`) stays as-is — it handles the **agent-return → queue completion** direction. The new hook handles the **main-session TaskCreate/TaskUpdate → queue** direction. Together they cover both principals.

### 3.3 Event handlers

The hook reads PostToolUse JSON from stdin (`{tool, tool_input, tool_response, ...}`) and dispatches on `tool`:

**On `TaskCreate`:**
- Extract `task_id`, `subject`, `description`, `priority` (default MED), `blockedBy` (default [])
- Dedup by `id` in `sprint-queue.json`
- Append entry:
  ```json
  {
    "id": "<native_task_id>",
    "title": "<subject>",
    "description": "<description>",
    "status": "queued",
    "claim_state": "unclaimed",
    "priority": "MED",
    "blockedBy": [],
    "source": "native-claude-task",
    "source_session_id": "<CLAUDE_SESSION_ID>",
    "created_at": "<ISO8601>"
  }
  ```
- Append to `forensics/native-bridge-coc.jsonl`: `{ts, event:"create", task_id, dashboard_line}`

**On `TaskUpdate` (status transition):**
- Resolve `task_id` from `tool_input.taskId`, resolve new status from `tool_input.status` (or `tool_response`)
- Match map: `pending`→no-op, `in_progress`→claim, `completed`→complete, `cancelled`→release
- Delegate to `~/.claude/hooks/state/queue_ops.py`:
  - `in_progress`: subprocess `queue_ops.py claim_specific --task-id <id> --session <CLAUDE_SESSION_ID> --owner main-session` (requires minor extension to queue_ops — see §4.1)
  - `completed`: subprocess `queue_ops.py complete <id>`
  - `cancelled`: subprocess `queue_ops.py release <id>`
- On `completed`: also emit MEM block to `{repo}/.claude/memory/pollen-{SID}.md`:
  ```
  <!-- MEM agent=main ts={ISO8601} session={SID} cat=DECISION pri=MED av=baseline -->
  **[DECISION]** Native Task #{id} completed: {subject}

  Source: TaskUpdate status=completed (main session)
  Bridged: faerie queue_ops.py complete {id}
  Manifest: {manifest_path if present else "none"}

  Files: none | Next: none
  <!-- /MEM -->
  ```

**On `TaskList` (read):**
- **Read-only, no mutation**. Optional helper: write a snapshot of current native list to `~/.claude/hooks/state/task-list-cache.json` so diagnostic commands (`queue_sync.py --status`) have a live view. This is the cache-file the partial `scripts/queue_sync.py` implementation was already looking for but nothing wrote. Hook populates it; `queue_sync.py` can finally function for humans running `--status`.

### 3.4 Failure behavior

- Non-JSON stdin → `sys.exit(0)` silently (like `8x_taskcreate_to_queue.py`)
- `queue_ops.py` subprocess failure → log to `forensics/native-bridge-coc.jsonl` with `level=warn`; do **not** exit nonzero (PostToolUse hook failures must not block the main session — aligns with "sauce must degrade silently")
- Missing `task_id` → silent exit
- Simultaneous TaskCreate + queue write from faerie / `/task`: dedup by `id` (if caller supplies one) or by `(source_session_id, subject[:80])` fallback

### 3.5 Stigmergy-only compliance check

- No `SendMessage` anywhere in the flow.
- All coordination via: `sprint-queue.json` (state), `pollen-{SID}.md` (MEM blocks), `forensics/native-bridge-coc.jsonl` (audit), `task-list-cache.json` (observable snapshot).
- Faerie discovers queue changes by reading `sprint-queue.json` at next wave plan — no event bus.
- Complies with f(0) Principle 1 (stigmergy-only), Principle 2 (artifacts in forensics), Principle 3 (task_id in COC filenames).

---

## 4. Implementation Plan

### Phase 0 — Ship-prep validation (this session, read-only)

- [x] Verify `/tmp/claude-{uid}/**/tasks/` contains only `.output` streams (no structured JSON)
- [x] Enumerate existing bridge scripts + their fitness
- [x] Confirm `settings.json` does NOT wire any Task* hook today
- [x] Confirm `manifest_task_autocompletion.py` logic handles agent-return side but is not currently called from settings.json

### Phase 1 — Consolidation (next session, one PR)

1. Write `scripts/8x_task_bridge_hook.py` per spec (§3).
2. Add PostToolUse matcher `TaskCreate|TaskUpdate|TaskList` to `settings.json`.
3. Register `manifest_task_autocompletion.py` under PostToolUse `Agent` in `settings.json` (currently orphaned).
4. Archive obsolete stubs to `docs/DEPRECATED-CONFIGS/` (with COC deletion entry):
   - `scripts/task_bridge.py`
   - `scripts/sync_queue_from_tasks.py`
   - `scripts/queue_sync_bridge.py`
   - `/mnt/d/0LOCAL/.claude/hooks/populate_queue_from_tasklist.py`
   - `/mnt/d/0LOCAL/.claude/hooks/8x_taskcreate_to_queue.py` (subsumed by new hook)
5. Extend `~/.claude/hooks/state/queue_ops.py` with `claim_specific --task-id ID --session SID --owner ROLE` (minor — the existing `claim` uses priority ordering; this variant claims a known id by source).

### Phase 2 — Verify

- [ ] `TaskCreate "test-bridge"` from main → appears in `sprint-queue.json` within 1 s with `source:"native-claude-task"`
- [ ] `TaskUpdate taskId=X status=in_progress` → queue entry flips to `claim_state:"claimed", claimed_by_session:"main-{SID}"`
- [ ] `TaskUpdate taskId=X status=completed` → queue entry flips to `status:"completed"` AND `pollen-{SID}.md` gains DECISION MEM block
- [ ] Agent completes task via Agent tool → `manifest_task_autocompletion.py` runs → queue completion + TaskList reverse-sync still works (regression check)
- [ ] `forensics/native-bridge-coc.jsonl` has hash-chained entries for each bridge event
- [ ] Remove all three stub scripts + orphaned hook; confirm nothing breaks (f(0) debt reduction)

### Phase 3 — Observability

- Add `scripts/9x_bridge_health.py` (sauce): reads `native-bridge-coc.jsonl` + `sprint-queue.json`, reports delta, stale claims, unbridged TaskCreate events (if any slipped past the hook).
- Surface in `/status` and `/dev-health` dashboards.

---

## 5. Deliverables of this investigation

1. **This document** (`docs/NATIVE-FAERIE-BRIDGE.md`) — current state + design + plan.
2. **Hook spec** (§3 above + inline `scripts/8x_task_bridge_hook.py` spec stub — next section).
3. **Settings-json diff spec** (§3.2).
4. **Deprecation list** (§4.1 step 4).

---

## 6. Open questions

- Does Claude Code's PostToolUse event for `TaskCreate` actually deliver `task_id` in the payload? (`8x_taskcreate_to_queue.py` assumes `manifest.task_id`; this needs an empirical probe in Phase 1.)
- Does `TaskList` PostToolUse fire at all, or only on mutations? (If only mutations, §3.3 TaskList handler becomes a no-op and the cache file is populated from TaskCreate/TaskUpdate deltas instead.)
- What is Claude Code's native task id format — integer, UUID, or free-form string? Affects dedup strategy.

Answers come from a 10-minute Phase 1 probe: wire the hook with a stdin-dump to `/tmp/task-bridge-probe.jsonl`, trigger each Task* tool once, read the JSON shape, refine the hook.

---

**References:**
- `docs/INVISIBLE-QUEUE-INTEGRATION.md` (partial design — this doc supersedes its implementation section)
- `docs/archive/faerie-task-sync-bridge-design.md` (2026-04-07 narrative — superseded by this doc)
- `docs/QUEUE-CLAIMING-ARCHITECTURE.md` (claim semantics — authoritative)
- `docs/DAILY-HOOKS-SCRIPTS-WIRING.md` (hook wiring index — update to reference new bridge hook)
- `~/.claude/hooks/state/queue_ops.py` (queue state machine — extends with `claim_specific`)

**Last-agent rule (vault sync):** This document is a repo artifact, not a vault artifact. A short summary is written to `$CT_VAULT/00-SHARED/ONBOARDING/2026-04-23-ship-prep-audit/NATIVE-FAERIE-BRIDGE-SUMMARY.md`.
