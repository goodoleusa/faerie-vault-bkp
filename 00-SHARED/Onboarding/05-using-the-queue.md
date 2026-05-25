---
type: guide
status: active
tags: [onboarding, queue, tasks, sprint]
parent: Onboarding/INDEX
up: Onboarding/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:cbe7df62c1fb1cc885548793c97a860fe5c81181e9cb4df6229bb162ad3c34cc
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Onboarding](INDEX.md) · [⌂ Home](../../HOME.md)

# 05 — Using the Queue

The sprint queue is the task backlog that faerie drains. Understanding
how to read, shape, and manage it is essential for directing work.

---

## Queue Concepts

| Term | Definition |
|------|-----------|
| **Sprint queue** | The ordered list of pending tasks (`sprint-queue.json`) |
| **Claim** | An agent atomically takes ownership of a task |
| **Blockers** | Tasks that must complete before a blocked task can be claimed |
| **Priority** | HIGH / MED / LOW — affects wave assignment and claim order |
| **Wave target** | W1 / W2 / W3 — which wave should execute this task |

---

## Viewing the Queue

```bash
# In Claude Code:
/queue

# Or directly:
python3 ~/.claude/scripts/9x_lean_query.py --get-queue
```

Output:
```
QUEUE: pending:12 queued:8 in-flight:2 complete:47
  [HIGH] task-078 | data-engineer | ingest logs from S3
  [HIGH] task-079 | python-pro    | fix null pointer in pipeline
  [MED]  task-080 | research-analyst | analyze log patterns
  ...
```

---

## Shaping the Queue

`/queue` shapes tasks without executing them. `/run` executes them.

```bash
/queue drop 3        # Remove task #3
/queue bump 5 HIGH   # Raise priority of task #5 to HIGH
/queue focus 2       # Move task #2 to front of critical path
/queue add           # Add a new task (interactive)
```

After shaping, the next `/run` invocation picks up the shaped queue.

---

## Adding Tasks

Tasks need a context bundle to be executable:

```json
{
  "id": "task-081",
  "title": "Document the faerie wave model",
  "category": "publishing",
  "priority": "MED",
  "context_bundle": {
    "highest_value": "developer understands W1/W2/W3 and why",
    "done_looks_like": "clear narrative doc; wave table; examples",
    "source_files": ["docs/SPAWN-BOILERPLATE.md", "skills/faerie/BODY.md"]
  }
}
```

`faerie_turn1.py` auto-patches missing context bundles at each `/faerie` launch.

---

## Blocking and Unblocking

Tasks can depend on other tasks:

```json
{
  "id": "task-082",
  "blockedBy": ["task-081"]
}
```

Task 082 will not be claimable until task 081 reaches `status: final`.
When an agent writes `next_task_queued` in its manifest, the PostToolUse
hook creates this relationship automatically.

---

## Queue Health Check

```bash
python3 ~/.claude/scripts/9x_lean_query.py --get-all
```

Shows:
- Pending / queued / in-flight / complete counts
- Current wave state
- Context fill %
- Top 3 tasks by priority

---

## Related

- [[../Skills-Reference/queue]] — /queue command quick-ref
- [[04-reading-manifests]] — how manifests create next_task_queued
- [[06-when-things-drift]] — what to do when queue stops draining
- [[../Glossary/terms]] — sprint queue, blocker, wave target defined
