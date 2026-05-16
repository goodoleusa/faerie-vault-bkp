---
type: narrative
status: active
tags: [intro, faerie, overview, newcomer]
parent: Hive/INDEX
up: Hive/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:79de9d75932e9c62d2b7468369b74dff17dcafe9447fb5dfc4e77a78028e38c9
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Hive](INDEX.md) · [⌂ Home](../../HOME.md)

# What is faerie?

faerie2 is an agent orchestration platform built around one idea:

> **f(0) — orchestration burden on main context should approach zero.**

What this means in practice: you can spawn as many agents as needed without worrying
about running out of context in the session that launched them. Each agent carries its
own context window. Main stays lean.

---

## The Problem faerie Solves

Vanilla Claude sessions hit context limits quickly when doing complex multi-step work.
Every thought, every tool call, every agent return fills the window. Eventually you
have to start over, losing continuity.

faerie inverts this. The main session is a *dispatcher*, not a worker. It reads only
`dashboard_line` summaries (≤80 chars each). Deep work happens in subagent context
windows that are separate, parallel, and expendable.

---

## The Three-Wave Model

faerie organizes work into **piston waves**:

| Wave | Name | Time Budget | Mode |
|------|------|-------------|------|
| W1 | Liftoff | 45 seconds | Fast triage, validation, state reads |
| W2 | Cruise | 180 seconds | Feature work, research, analysis |
| W3 | Insertion | 600 seconds | Deep synthesis, background |

Waves fire in sequence. W1 and W2 are inline (main waits). W3 fires in background
after the session responds — you see output from W1+W2 immediately, W3 completes
asynchronously.

---

## How Agents Coordinate

Agents do **not** message each other. Instead, they write to the filesystem and
other agents read what they find. This is called **stigmergy** — coordination through
environmental marks, not direct communication.

An agent completing a task writes a **manifest** to a known path. The next agent
discovers it by reading that path or by grepping for its `task_id` in `forensics/`.
No orchestrator needed. No polling. No messaging overhead.

---

## The Memory Stack

faerie uses a layered memory system:

- **HONEY.md** — crystallized knowledge, dense, ≤5K tokens. Rarely changes.
- **NECTAR.md** — validated findings, append-only forever. Grows across sessions.
- **pollen** — ephemeral session notes. Cleared after each faerie cycle.
- **forensics/** — immutable artifacts. Hash-chained, git-tracked, never deleted.

Each layer has a different lifespan and promotion threshold. Pollen observations
that prove valuable get promoted to NECTAR. NECTAR patterns that persist become HONEY.

---

## What You Do

You invoke skills. The platform does the rest.

```
/faerie       → start a session (orient, run waves, dashboard)
/run          → claim and execute tasks from the queue
/handoff      → close session (promote memory, sync vault)
/metrics      → check system health and eval scores
/queue        → view, shape, and manage the task queue
```

That is the full interface. Everything else happens in agent context.

---

## Related

![[../Diagrams/five-principles-compass.excalidraw]]

- [[the-five-principles]] — the design reasoning in depth
- [[piston-rocket-physics]] — the wave model explained
- [[../Onboarding/01-first-session]] — your first concrete steps
- [[../Glossary/terms]] — definitions for every term used here
