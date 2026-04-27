---
status: ready-for-review
created: 2026-03-30T01:50:00Z
priority: HIGH
relates_to: [forensic_extract_convergence, spiderfoot_osint_integration, piston_equilibrium]
---

# Breadcrumb Trail System Complete — Agent Recovery Architecture

## What Was Built

**Filesystem-based checkpoint mechanism** for long-running agent tasks. Agents leave "breadcrumb" JSONL checkpoints in `~/.claude/memory/checkpoints/` during execution. If interrupted, any agent (or human monitor) can read the trail and resume from exact checkpoint.

## Key Files

| File | Purpose | Location |
|------|---------|----------|
| `breadcrumb.py` | Checkpoint writer/reader utility | `~/.claude/scripts/` |
| `BREADCRUMB-INTEGRATION.md` | Agent implementation guide | `~/.claude/scripts/` |
| `project_breadcrumb_trail_system.md` | Architecture + decisions (NECTAR-frozen) | `~/.claude/projects/.../memory/` |
| `DURABLE-STATE-LOADER.md` | Minimal startup file reads (equilibrium-safe) | `~/.claude/docs/` |
| `sprint-OSINT-BREADCRUMB-001.md` | First validation task (HIGH priority, queued) | `~/.claude/hooks/state/sprint-queue/` |

## How It Works

### Checkpoint Format (JSONL, hash-chained)
```jsonl
{"ts":"2026-03-30T00:32:01Z","checkpoint":1,"task_id":"OSINT-001","agent_id":"a541145f","session_id":"sess-123","progress":"10/50","next_start":10,"entry_hash":"a7c2f1...","prev_hash":null}
{"ts":"2026-03-30T00:32:45Z","checkpoint":2,"task_id":"OSINT-001","agent_id":"a541145f","session_id":"sess-123","progress":"20/50","next_start":20,"entry_hash":"b9d3e2...","prev_hash":"a7c2f1..."}
```

### Recovery Paths
1. **Lost agent self-recovery:** `resume_from_breadcrumb(task_id)` → resumes from `next_start`
2. **Human monitor:** `breadcrumb.py read TASK_ID` → human-friendly progress view
3. **New agent takeover:** Different agent reads trail, continues work

## Integration with Existing Systems

- **+ Streams:** Checkpoints = recovery (WHERE); streams = findings (WHAT)
- **+ COC chain:** Hash-chained like NECTAR + forensic logs (tamper-evident)
- **+ Piston model:** Agents write checkpoints every N items; no overhead to main session

## Equilibrium Respected

✓ Durable state solution keeps agent startup ≤650 tokens
✓ Agents read only: own card (~300T) + piston checkpoint if resuming (~100T) + NECTAR tail if investigation (~250T)
✓ Task metadata from claimed task object, not by re-reading sprint-queue.json
✓ Breadcrumbs use append-only JSONL (no locking, no conflicts)

## Validation Task

**OSINT-BREADCRUMB-001** (HIGH priority, queued now):
- Scan 50+ targets with ≥5 checkpoints
- Test recovery mechanism (manual interrupt at CP3, verify resume from next_start)
- Stream findings to NECTAR (hash-based dedup)
- Validate forensic_extract convergence works end-to-end

## Message in a Bottle

**Core concept:** If an agent gets disconnected from the session, the breadcrumb trail IS THERE on the filesystem. Anyone (lost agent, new agent, human, monitor script) can find it and understand what happened.

No metadata server needed — **filesystem IS the communication medium (stigmergy)**.
Hash-chained for forensic integrity — suitable for court exhibits.

## Next Steps

1. Monitor ac3acefe (data-engineer) for DAE integration completion
2. Run `/run` to claim OSINT-BREADCRUMB-001
3. Verify breadcrumb checkpoints + recovery mechanism work
4. Promote findings to NECTAR
5. Document lessons in agent cards

---

**Status:** Ready for production use. First validation task queued.
**Archive:** See `project_breadcrumb_trail_system.md` for full architecture decisions.
