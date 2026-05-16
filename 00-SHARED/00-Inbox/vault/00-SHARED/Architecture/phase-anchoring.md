---
type: reference
status: active
tags: [architecture, phase, anchoring, continuity]
parent: Architecture/INDEX
up: Architecture/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:9e14c7f3a93b236b990c4b4d38437ee51c0aeeddc23284065aa2445e874f8a81
hash_ts: 2026-04-25T01:10:50Z
hash_method: body-sha256-v1
---

> [↑ Architecture](INDEX.md) · [⌂ Home](../../HOME.md)

# Phase Anchoring

Session continuity across faerie cycles. How faerie knows where it is
in a long-running investigation or sprint.

---

## The Problem

A faerie cycle is one `/faerie` → waves → `/handoff` unit. An investigation
may span 10+ faerie cycles across multiple days. Without anchoring, each
session re-orients from scratch — burning 5-20K tokens of context just
to remember what was already learned.

---

## Phase State

Phase state is stored in `piston-checkpoint.json`:

```json
{
  "context_pct": 42,
  "wave_state": "W2",
  "agents_in_flight": 2,
  "phase": {
    "id": "phase-003",
    "milestone": "spawn-contract-stabilized",
    "started": "2026-04-20T09:00:00Z",
    "tasks_complete": 47,
    "tasks_pending": 12
  }
}
```

---

## Phase Transitions

Phase transitions happen when a milestone is reached:

```
phase-001: Initial setup complete → phase-002
phase-002: Core eval infrastructure → phase-003
phase-003: Spawn contract stable + bundle evolution → phase-004
```

Transition triggers are declared in `ARCHITECTURE.md` for each project.
When a trigger condition is met, faerie writes the new phase to the checkpoint.

---

## Cold Start vs Warm Start

**Cold start (>8h since last session):**
- Read `handoff-snapshot-summary.json` (lightweight, avoids 256KB limit)
- Run `7x_emergency_handoff.py` if summary is missing
- Cross-project registry scan for all active projects

**Warm start (<8h, same day):**
- Read `piston-checkpoint.json` only (phase, wave, context %)
- Skip faerie-brief.json (gated by `8x_faerie_brief_gatekeeper.py`)
- Skip NECTAR re-read (already in context from this session)

**SEAMLESS RULE:** Do not speak to user post-compact until you have
an agent return, a dashboard refresh, or a blocking question.

---

## Handoff Snapshot

`/handoff` writes a snapshot that survives across CLI sessions:

```
~/.claude/hooks/state/handoff-snapshot-summary.json  ← lightweight (≤200 bytes)
~/.claude/hooks/state/handoff-snapshot.json          ← full (may be 1MB)
```

faerie reads the summary first. Full snapshot only if summary is missing
or a conditional deep read is triggered.

---

## Related

- [[piston-waves]] — piston checkpoint structure
- [[memory-topology]] — how NECTAR preserves phase context across sessions
- [[../Skills-Reference/handoff]] — /handoff writes the snapshot
- [[../Glossary/terms]] — phase, cold start, warm start defined
