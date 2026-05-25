---
type: reference
status: active
tags: [skill, queue, tasks, sprint, management]
parent: Skills-Reference/INDEX
up: Skills-Reference/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:15e3acf7cf92ca3806b9893909546e6f938f853e652f3d3929fc32b5ad8f433f
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Skills-Reference](INDEX.md) · [⌂ Home](../../HOME.md)

# /queue — Queue Manager

View, add, and shape the sprint queue. Queue shaping is separate from execution.
`/queue` shapes. `/run` executes.

---

## Invocation

| Command | Action |
|---------|--------|
| `/queue` | Show full queue with priorities |
| `/queue add` | Add a new task (interactive) |
| `/queue drop 3` | Remove task #3 |
| `/queue bump 5 HIGH` | Raise task #5 to HIGH priority |
| `/queue focus 2` | Move task #2 to critical path front |
| `/queue drop 3` | Remove task #3 from queue |

---

## Queue Display

```
QUEUE — 2026-04-24T15:00Z
================================================================
BLOCKERS (run first):
  [B1] 🔴HIGH | task-078 | python-pro     | fix null pointer
  [B2] 🔴HIGH | task-079 | data-engineer  | fix ingest pipeline

CRITICAL PATH:
  [C1] 🔴HIGH | task-080 | research-analyst | analyze log patterns

BREADTH:
  [D1] 🟡MED  | task-081 | documentation-engineer | document spawn contract
  [D2] 🟢LOW  | task-082 | membot          | promote W3 findings

TOTAL: 12 pending | 2 in-flight | 127 complete
================================================================
```

---

## Task Structure

Required fields for a queueable task:

```json
{
  "id": "task-081",
  "title": "Document the spawn contract",
  "category": "publishing",
  "priority": "MED",
  "wave_target": "W2",
  "context_bundle": {
    "highest_value": "developer understands the spawn contract",
    "done_looks_like": "spawn-contract.md written; examples included",
    "source_files": ["docs/SPAWN-BOILERPLATE.md"]
  }
}
```

`faerie_turn1.py` auto-patches missing `context_bundle` at each `/faerie` launch.

---

## Priority Effects

| Priority | Claim order | Wave |
|----------|------------|------|
| HIGH | First (batch claim up to 4) | W1 or W2 based on complexity |
| MED | After HIGH exhausted | W2 default |
| LOW | After MED exhausted | W2 or W3 |

---

## Related

- [[run]] — /run executes the shaped queue
- [[../Onboarding/05-using-the-queue]] — queue usage in depth
- [[../Glossary/terms]] — sprint queue, blocker, priority defined
