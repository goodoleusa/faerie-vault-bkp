# Auto-Handoff System — Architecture & Status

## Overview

**Auto-handoff** is a lightweight, fire-and-forget memory preservation system that fires automatically on every Claude CLI session exit. It ensures that HIGH-priority findings, reasoning streams, and NECTAR growth are captured without requiring explicit user invocation of `/handoff`.

**Status:** OPERATIONAL (both system files exist and are integrated)

---

## Components

### 1. `auto_handoff.py`
**Location:** `~/.claude/scripts/auto_handoff.py`
**Size:** ~8KB | **TIER:** `9x_utilities`

Lightweight wrapper that runs at every CLI session exit. Tasks:
- `run_emergency_handoff()` — state roundup via emergency_handoff.py
- `promote_high_flags()` — scan scratch-{SESSION_ID}.md for `pri=HIGH` MEM blocks → REVIEW-INBOX.md
- `collect_streams()` — archive memory_bridge output streams to forensic storage
- `queue_overnight_if_needed()` — detect NECTAR growth >5KB, queue crystallization batch
- `write_result()` — write auto-handoff-result.json manifest

**Blocking:** NO — spawned as background process (`subprocess.Popen`), does not block session exit

### 2. `emergency_handoff.py`
**Location:** `~/.claude/scripts/emergency_handoff.py`
**Size:** ~30KB

State roundup script called by auto_handoff. Snapshots faerie-brief.json and session metrics.

### 3. Integration in `session_stop_hook.py`
**Location:** `~/.claude/hooks/session_stop_hook.py` (end of main())

```python
# Auto-handoff: spawn lightweight memory preservation on every CLI exit
try:
    auto_handoff_script = CLAUDE / "scripts" / "auto_handoff.py"
    if auto_handoff_script.is_file():
        subprocess.Popen(
            [sys.executable, str(auto_handoff_script), session_id],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
except Exception:
    pass
```

---

## Workflow (Every CLI Exit)

```
1. User exits Claude CLI (Ctrl+C, completion, timeout)
   ↓
2. session_stop_hook.py fires (system hook at process exit)
   ├─ Run: narrative_auto_update.py
   ├─ Run: transcript_archiver.py (background)
   ├─ Run: backup_forensics.py (background)
   └─ Spawn: auto_handoff.py (background, subprocess.Popen)
   ↓
3. Session exits cleanly (NO WAIT — Popen returns immediately)
   ↓
4. auto_handoff.py runs asynchronously in background (~1-5 seconds)
   ├─ Calls: run_emergency_handoff() → state snapshot
   ├─ Calls: promote_high_flags() → scan scratch, append REVIEW-INBOX
   ├─ Calls: collect_streams() → archive memory outputs
   ├─ Calls: queue_overnight_if_needed() → check NECTAR delta
   └─ Calls: write_result() → manifest to state directory
```

---

## Memory Preservation Tasks

### Task 1: HIGH-Priority Flag Promotion

**Source:** `{repo}/.claude/memory/scratch-{SESSION_ID}.md`
**Pattern:** `<!-- MEM ... pri=HIGH ... -->`
**Destination:** `~/.claude/memory/REVIEW-INBOX.md` (append-only)
**Frequency:** Every CLI exit

Ensures critical findings marked `pri=HIGH` surface for human review even if the session ended abruptly.

### Task 2: Stream Collection & Archive

**Source:** `~/.claude/memory/streams/{SESSION_ID}.jsonl`
**Action:** Collect and archive to forensic storage
**Destination:** `~/.claude/memory/forensics/`
**Frequency:** Every CLI exit

Preserves the COC trail and reasoning chain from `memory_bridge.py --stream` outputs.

### Task 3: NECTAR Growth Detection

**Check:** NECTAR.md file size delta vs faerie-brief.json baseline
**Threshold:** >5KB growth detected
**Action:** Write task to overnight-batch-queue.json
**Suggested tasks:** `compress-HONEY`, `crystallize-NECTAR-tail`
**Frequency:** Every CLI exit (if threshold exceeded)

Detects when NECTAR has grown significantly and queues a background crystallization task.

### Task 4: State Roundup (via emergency_handoff.py)

**Action:** Snapshot system state
**Destination:** `~/.claude/hooks/state/faerie-brief.json`
**Frequency:** Every CLI exit

Provides cold-start fuel for next faerie cycle.

---

## Failure Modes & Safety

### Silent Failure Design

All exceptions in auto_handoff.py are caught and logged to scratch (best-effort). The session exit **never blocks** or hangs.

```python
try:
    # ... preservation tasks
except Exception:
    pass  # Silent failure — never crash on session exit
```

**Outcome:** Session exits cleanly within 1-2 seconds, with auto_handoff.py continuing in background if needed.

### No User Action Required

Auto-handoff fires automatically. Zero friction. No `/handoff` invocation needed for basic memory preservation.

---

## Result & Monitoring

### Success Indicator

**File:** `~/.claude/hooks/state/auto-handoff-result.json`

**Created within:** 5 seconds of session exit

**Schema:**
```json
{
  "session_id": "uuid-of-session",
  "timestamp": "2026-04-07T06:30:00Z",
  "type": "auto-handoff",
  "status": "complete",
  "phase": "memory-preservation"
}
```

### Monitor NECTAR Growth Events

**File:** `~/.claude/hooks/state/overnight-batch-queue.json`

Entries appended when NECTAR delta >5KB. Review this file to understand when crystallization is queued.

---

## Differences from `/handoff`

| Aspect | Auto-Handoff | `/handoff` Command |
|--------|--------------|-------------------|
| **Trigger** | Every CLI exit (automatic) | User-invoked (intentional) |
| **Scope** | Memory preservation only (HIGH flags, streams, NECTAR delta) | Full faerie cycle (memory promotion, decision application, overnight queue) |
| **Blocking** | Non-blocking (background process) | Blocking (user waits) |
| **Orchestration** | None — fire-and-forget | Faerie orchestrates multi-wave coordination |
| **User interaction** | Zero | Full interactive briefing |
| **Use case** | Safety net for abrupt exits | Intentional, coordinated session end |

**Auto-handoff is NOT a replacement for faerie orchestration.** It's a safety net that ensures findings are never lost.

---

## Files & Locations

| File | Path | Size | Status |
|------|------|------|--------|
| auto_handoff.py | `~/.claude/scripts/auto_handoff.py` | ~8KB | ✓ Operational |
| emergency_handoff.py | `~/.claude/scripts/emergency_handoff.py` | ~30KB | ✓ Operational |
| session_stop_hook.py | `~/.claude/hooks/session_stop_hook.py` | ~13KB | ✓ Integrated |
| Result manifest | `~/.claude/hooks/state/auto-handoff-result.json` | ~200B | Written per exit |
| Overnight queue | `~/.claude/hooks/state/overnight-batch-queue.json` | ~500B-2KB | Grows per session |

---

## Validation (Manual Testing)

To verify the system:

1. **Run a session and write a HIGH flag:**
   ```bash
   cd /mnt/d/0local/gitrepos/faerie2 && claude
   # Write a MEM block with pri=HIGH
   # Exit (Ctrl+C)
   ```

2. **Verify within 5 seconds:**
   ```bash
   cat ~/.claude/hooks/state/auto-handoff-result.json
   tail ~/.claude/memory/REVIEW-INBOX.md
   ls -la ~/.claude/memory/forensics/ | grep stream
   ```

3. **Check overnight queue (if NECTAR grew >5KB):**
   ```bash
   cat ~/.claude/hooks/state/overnight-batch-queue.json | jq .
   ```

---

## Next Steps

1. **Monitor in production** — observe overnight-batch-queue.json patterns
2. **Tune delta threshold** — adjust 5KB in auto_handoff.py if too aggressive/lenient
3. **Optional dashboard indicator** — show auto-handoff completion in presend footer
4. **Document in SKILL.md** — update /handoff skill with auto-handoff relationship

---

## Reference

- **Rules:** `.claude/rules/agent-lifecycle.md` — agent startup and memory responsibilities
- **Memory routing:** `.claude/rules/memory-routing.md` — canonical memory locations
- **Agent memory:** `.claude/rules/agent-memory.md` — MEM block format and promotion rules
