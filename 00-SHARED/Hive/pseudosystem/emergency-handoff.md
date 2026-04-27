---
type: system-component
component_type: process
status: active
created: 2026-03-27
tags: [system, pseudosystem, emergency-handoff]
parent:
  - "[[session-lifecycle]]"
sibling:
  - "[[handoff-end]]"
child: []
inputs:
  - "[[brief-atoms]]"
  - "[[scratch-working]]"
outputs:
  - "[[handoff-snapshot]]"
  - "[[brief-atoms]]"
color: gold
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:91b1790abf069a3b7018bdc36a119d359baea9e22ceeada66661f888ac36a2b8
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Emergency Handoff

The circuit breaker. When context reaches 1% remaining, a PostToolUse hook fires a Python script — no LLM, no token spend, 1.5 seconds flat. It snapshots the current brief atoms and active scratch into a minimal handoff file, then exits. This prevents catastrophic state loss when a session hits the context wall unexpectedly. It is the system's fail-safe: dumb, fast, and reliable.

## Flow

**In:** Current brief atoms (accumulated checkpoints), any open scratch content
**Out:** Minimal handoff snapshot, appended brief atom marking the emergency stop

## Relationships

- [[handoff-end]] — the graceful version; emergency-handoff is the fallback
- [[brief-atoms]] — the pre-accumulated checkpoints that make emergency handoff possible
- [[handoff-snapshot]] — what gets written; minimal but sufficient
- [[faerie-start]] — will read this snapshot and recover gracefully

## Natural Metaphor

An aircraft black box: passive, always recording, triggers automatically on impact. The pilot doesn't have to do anything — the box saves what it can.
