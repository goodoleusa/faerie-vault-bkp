---
type: narrative
status: active
tags: [piston, waves, rocket, context, orchestration]
parent: Hive/INDEX
up: Hive/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:d7d2d8fadb14ed088f4f1475f8692531c7cf6d749f78981eb58c1914b21ca3cb
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

> [↑ Hive](INDEX.md) · [⌂ Home](../../HOME.md)

# Piston Rocket Physics

The faerie wave model is modeled on rocket stage separation.
Main context = fuel. Conservation instinct = the enemy.

---

## The Rocket Frame

```
GRAVITY         = context pressure (tokens consumed by orchestration)
FUEL            = main context window (~200K tokens)
ESCAPE VELOCITY = main-idle-while-subagents-carry-momentum
STAGE SEPARATION= wave compression to dashboard_lines (weight drop)
```

| Stage | Wave | Duration | Burn |
|-------|------|----------|------|
| First-stage liftoff | W1 | 45 seconds | Max burn — parallel spawns, cache warm |
| Cruise | W2 | 180 seconds | Single-spawn dispatches, mid-altitude |
| Orbital insertion | W3 | 600 seconds | Deep synthesis, background |

---

## The Key Inversion

**Conservation-first instinct is wrong.**

The natural impulse: "save context — don't spawn too much in turn 1."
This instinct kills momentum. Here is why.

Claude Code caches prompts for ~5 minutes. If you burn hot in turn 1 — fill
the cache, spawn W1+W2 in parallel — you get 5 minutes of cached prefill for
every subsequent agent in this session. Delay costs you that cache window.

W1 is the first-stage burn. **Burn hot early.** Drop weight by compressing
W1 results to dashboard_lines. Coast on momentum through W2 and W3.

---

## Wave Gates

Waves are gated by **altimeter reading**, not elapsed time.

```
piston-checkpoint.json
  context_pct: 42    ← current fill %
  wave_state: W2     ← last launched wave
  agents_in_flight: 2
```

The piston reads this file. Wave launch decisions use `context_pct`, not
a clock. This is pressure-responsive streaming (Principle 5).

Key thresholds (measured, not aspirational):
- **85%** — compact is queued; W3 synthesis window closes
- **93.5%** — auto-compact fires; W3 should have fired already

Operators: read `9x_lean_query.py --get-wave` for current state.

---

## Stage Separation

After W1 agents return, their full output lives in `forensics/`. Main
reads only their `dashboard_line` (≤80 chars). This is the weight drop.

```
W1 agents return:
  4 manifests × 50KB each = 200KB of findings (stays in forensics/)
  4 dashboard_lines × 80 chars = 320 chars (main reads this only)

Context consumed by W1 collection: ~320 chars (~80 tokens)
Without cascading summarization: ~200KB (~50,000 tokens)

Saving: 99.8% context reduction per wave
```

This is how f(0) holds regardless of agent count. The weight drops
at each stage boundary. Main stays at low altitude.

---

## Post-Compact Restart

Auto-compact is a flywheel stutter, NOT a cold start.

When compact fires:
1. Read `piston-checkpoint.json` — `wave_state`, `context_pct`, `agents_in_flight`
2. Check which agents are in-flight vs returned (read manifest statuses)
3. Launch the next wave immediately

The compact summary IS the context. Do not re-read summarized files.
Do not announce "resuming after compaction."

---

## The TURN 0 Completion Pattern

faerie's core rule: **Do not respond until W1 AND W2 are complete.**

```
Wave 0: bash reads (non-blocking, parallel with context file reads)
Wave 1: spawn all fast agents WITHOUT run_in_background — faerie waits
Wave 2: spawn all medium agents WITHOUT run_in_background — faerie waits
         ↓
         Merge results → build dashboard → RESPOND ONCE
         ↓
Wave 3: spawn WITH run_in_background: true AFTER the response
```

The user sees one clean response with W1+W2 complete. W3 runs in
background while they read it.

---

## Related

- [[the-five-principles]] — pressure-responsive streaming (principle 5)
- [[../Architecture/piston-waves]] — technical implementation
- [[permission-to-leap]] — why burning hot is right
- [[../Skills-Reference/faerie]] — /faerie skill quick-ref
