---
type: narrative
status: active
tags: [permission, context, momentum, sys00037]
parent: Hive/INDEX
up: Hive/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:8fb4ac6d5796113ae24ed75060129e83f3371ce44c5950c29b817215d3f4662d
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

> [↑ Hive](INDEX.md) · [⌂ Home](../../HOME.md)

# Permission to Leap

**sys00037: Conservation-first instinct is wrong. Burn hot early.**

This is the principle that inverts the natural instinct about context management.

---

## The Instinct

When you open a new Claude session, the natural impulse is to be careful.
"I have 200K tokens. Let me not waste them. I'll be conservative early
and save context for when I really need it."

This feels right. It is wrong.

---

## Why Conservation Fails

**Cache misses.** Claude Code caches prompts for ~5 minutes. If you spend
the first 3 minutes "being careful" — asking clarifying questions, reading
one file at a time, thinking before spawning — you miss the cache window.
Every subsequent agent spawn in this session pays full prefill cost.

**Gravity wins.** Context fills. Every cautious thought still costs tokens.
The question is never "spend or save." It is "spend now for momentum or
spend now for nothing."

**First-wave drag.** W1 is designed for max burn — parallel spawns, cache
warm, fast triage. If W1 is timid, W2 inherits nothing. W3 has no foundation.
The piston stalls.

---

## The Correct Frame

```
Turn 1 is liftoff. Burn everything.
Weight drops at each stage boundary (dashboard_line compression).
Main coasts on subagent momentum.
```

- Spawn W1 agents in parallel. All of them. Today.
- Read only dashboard_lines when they return.
- Spawn W2 immediately with W1 context.
- Respond once. Let W3 run in background.

The system is designed to be cheap to use. `7x_spawn_template.py` renders
spawn prompts deterministically for ≤50 tokens each (was 40K before templates).
Spawning 10 agents in W1 costs ≤500 tokens of overhead.

---

## The Main-Inference Heuristic

> If main's thought connects ≥2 subagent returns OR makes a routing decision
> OR catches a contradiction — it is earning its inference cost.
>
> If it is reformulating something a subagent already said — it is burning context.

Main should do only the work no subagent can do:
- Cross-cut synthesis across N returns
- Routing decisions
- Contradiction-catching
- Cascading summarization

Everything else: spawn it. Do not inline it.

---

## The Anti-Pattern

These are violations of permission-to-leap:

- "Let me first understand the full codebase before spawning anything"
- "I'll read these 5 files carefully before deciding on agents"
- "Let me check if context is getting full before launching W2"
- Responding to the user with "I'm planning to..." instead of doing it

Each of these burns main context with zero output value.
The agents would have gotten better context by just starting.

---

## Practical Leap Triggers

| Situation | Action |
|---|---|
| Session start | Spawn W1 immediately while reading context files in parallel |
| W1 complete | Launch W2 immediately, do not re-read W1 manifests |
| Context >70% | W3 should already be running in background |
| User asks something that would take >3 reasoning sentences | Spawn, don't inline |

---

## Related

- [[piston-rocket-physics]] — the wave model that makes leaping work
- [[the-five-principles]] — pressure-responsive streaming (principle 5)
- [[../Architecture/piston-waves]] — technical piston implementation
- [[../Skills-Reference/faerie]] — /faerie skill reference
