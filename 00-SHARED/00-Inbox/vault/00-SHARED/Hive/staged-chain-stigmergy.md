---
type: narrative
status: active
tags: [stigmergy, chaining, manifest, task-graph]
parent: Hive/INDEX
up: Hive/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:61638fd1578d570e3e0fef2325e14d1768d8a9be311f55a6fd01c2f65ac6521d
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Hive](INDEX.md) · [⌂ Home](../../HOME.md)

# Staged Chain Stigmergy

Staged chain stigmergy is the pattern where manifest status transitions
create a self-propagating task graph — each agent's completion automatically
surfaces and unblocks the next stage of work.

---

## The Status Ladder

Every manifest progresses through a defined status ladder:

```
in-progress → draft → final
```

Agents update their manifest progressively. Downstream consumers
read `status: final` as the signal that work is safe to consume.

This replaces polling. Agents do not ask "is task X done?"
They read the manifest at the known path. Status field answers.

---

## Automatic Blocking Relationships

When an agent writes `next_task_queued` in its manifest:

```
Agent completes T1
  ↓
  Writes manifest with next_task_queued: {task_id: "T2", reason: "..."}
  ↓
PostToolUse hook reads manifest
  ↓
Hook calls queue_ops.py to add blockedBy[T1] to T2
  ↓
T2 auto-unblocks when T1 status = final
  ↓
Next available agent claims T2 from queue
```

No manual DAG management. The agents declare their own successors.
The hook enforces the dependency. The queue manages claiming.

---

## Discovery at Task Boundaries

At each task boundary, agents follow this discovery order:

1. **Faerie queue** — what is unblocked and claimable right now?
2. **Manifest locations** — what have upstream agents already written?
3. **Vault droplets** — what cross-domain insights exist from parallel agents?
4. **Native task list** — within a team, what sub-tasks are owned/blocked?

This is passive. Agents read what is there. No orchestrator pushes context.

---

## The Two-Stream Rule

Every agent deposit path serves two purposes simultaneously:

1. **Forensic capture** — a permanent hash-chained audit record
2. **Stigmergic discovery** — a pheromone trail for the next agent

These are not separate writes. The same file path in `forensics/` serves both.
The `task_id`-in-filename convention makes it discoverable.

Hooks handle the forensic side silently. Agents focus on writing good output
to the right path. The chain builds itself.

---

## Related

- [[stigmergic-recursion]] — the full coordination model
- [[the-five-principles]] — task_id-in-filename (principle 3)
- [[../Architecture/forensic-integrity]] — COC implementation
- [[../Architecture/spawn-contract]] — spawn validation
