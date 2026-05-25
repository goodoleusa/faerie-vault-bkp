---
type: guide
status: active
tags: [onboarding, skills, commands, tour]
parent: Onboarding/INDEX
up: Onboarding/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:989b3e38463eb406b55f5332f6a37e674391e0dde54c041f2f3f673432ed9e52
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Onboarding](INDEX.md) · [⌂ Home](../../HOME.md)

# 02 — Skills Tour

Every skill command explained. Use this as a map before diving into the quick-refs.

---

## The Seven Core Skills

| Skill | Role | When to use |
|-------|------|-------------|
| `/faerie` | Session orchestrator | Start of every session |
| `/run` | Queue consumer | Execute tasks from the queue |
| `/metrics` | System health | Check quality scores and gaps |
| `/dev-eval` | Eval detail | Deep eval breakdown, gap analysis |
| `/handoff` | Session closer | End of every session |
| `/crystallize` | Memory integrator | Promote pollen → NECTAR → HONEY |
| `/queue` | Queue manager | View, add, reprioritize tasks |
| `/droplet` | Insight capture | Write an insight to the droplets vault |

---

## /faerie — The Orchestrator

`/faerie` is the session start command. It:
- Reads the current piston state (wave, context %, agents in flight)
- Reads the sprint queue (pending tasks)
- Runs Wave 1 (fast triage agents, inline)
- Runs Wave 2 (research agents, inline)
- Responds with a dashboard
- Fires Wave 3 in background after response

**Modes:**

| Invocation | Behavior |
|---|---|
| `/faerie` | Standard session start |
| `/faerie focus on X` | Prioritize tasks related to X |
| `/faerie --explain` | Show what /faerie WOULD do (dry run) |
| `/faerie --queue` | Queue manager mode only |
| `/faerie --review` | Red-team top findings, no tasks launched |

---

## /run — The Queue Consumer

`/run` claims and executes tasks. It:
- Batch-claims HIGH priority tasks
- Groups them by wave (W1/W2/W3)
- Spawns agents for W1 inline, W2 inline, W3 background
- Runs performance-eval after completion

**Filters:**

```
/run blockers        → run only blocker tasks
/run critical        → run critical-path tasks
/run --once          → run exactly one task then stop
/run --dry-run       → show what would be claimed
```

---

## /metrics and /dev-eval — Health Checks

`/metrics` shows current system health: eval scores, queue depth, memory status.

`/dev-eval` gives the detailed breakdown: per-dimension scores, gap analysis,
improvement suggestions for each dimension.

Use `/metrics` daily. Use `/dev-eval` when a score drops unexpectedly.

---

## /handoff — Session Closer

`/handoff` closes the faerie cycle. It:
- Promotes pollen (session notes) → NECTAR (validated findings)
- Syncs vault with agent outputs
- Updates the piston checkpoint for next session
- Spawns membot to crystallize findings

Always run `/handoff` before closing Claude Code. Without it, session
observations stay in pollen and are lost at next session start.

---

## /crystallize — Memory Integrator

`/crystallize` is for deliberate memory integration. It:
- Scans NECTAR for patterns that recur across ≥3 sessions
- Proposes HONEY candidates (requires human approval)
- Integrates validated findings into crystallized knowledge

**Note:** Crystallization requires human choice. Agents never queue it.
It runs when you decide the session's findings are worth integrating.

---

## /queue — Queue Manager

`/queue` shapes the sprint queue without executing tasks. Operations:

```
/queue               → show full queue
/queue add           → add a new task
/queue drop 3        → remove task #3
/queue bump 5 HIGH   → raise task #5 to HIGH priority
/queue focus 2       → move task #2 to critical path front
```

Queue changes are immediately respected by the next `/run` invocation.

---

## /droplet — Insight Capture

`/droplet` writes an insight to the droplets vault. Use it when:
- A cross-domain connection clicks
- Something surprising emerges during analysis
- You want to preserve a thought before context compresses it

Droplets are discovered by future agents at task boundaries.
High-priority droplets are promoted to NECTAR at `/handoff`.

---

## Next Steps

- [[03-spawn-your-first-agent]] — hands-on agent spawning
- [[../Skills-Reference/INDEX]] — full quick-refs for every skill
- [[05-using-the-queue]] — queue management in depth

---

## Related

- [[../Hive/piston-rocket-physics]] — why the wave model is shaped this way
- [[../Glossary/terms]] — all terms used here defined
