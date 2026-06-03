---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: bearing-trajectory-tracking
status: synthesis-log
canon_candidate: true
---

# Bearing trajectories — charting each agent's actual course, not just spawn intent

User asked (verbatim):

> "what frontmatter are we collecting in coc and mission graph
>  frontmatter that ensures we are tracking not just each agent's
>  initial bearing, but the vector path they navigated (charting
>  their course?) along the way"
> "where they ended up from initial bearing"

This is a real and currently-unmet gap. Today we capture an agent's
INITIAL bearing (sometimes) and their FINAL completion_choice. We
don't capture the path between those two points. An agent that
started N (unblock), discovered the unblock required E (parallel
setup), then pivoted S (ship the actual deliverable) leaves no
record of that pivot. The COC trail shows only the endpoints.

## Today's state (audit results)

**COC entries** (`forensics/coc.jsonl`):
```json
{
  "ts": "...",
  "event": "charter-created",
  "kind": "...",
  "mission": "...",
  "charter_id": "...",
  "entry_sha": "...",
  "coc_chain": {...},
  "content_sha256": "..."
}
```
No `bearing` field. No `vector`.

**Mission graph nodes** (`forensics/mission-graph.json`):
```json
{
  "created": "...",
  "status": "...",
  "tasks": [...]
}
```
No `agent_trajectories`. Per-agent paths invisible.

**Manifests**:
- `mission` field — yes
- `bearing` field — INCONSISTENTLY present (some manifests have it, most don't)
- `discovered_work[]` — has bearings per discovered item (the NEXT moves)
- `completion_choice` — final move only
- No `bearing_trajectory[]` ledger

So agents make trajectory-shaped moves but only their endpoints
get recorded. The middle of the journey is lost.

## What should be captured

### Manifest body — add `bearing_trajectory[]`

```json
{
  "manifest_id": "...",
  "agent_type": "maker",
  "mission": "doctrine.coverage.audit",

  "initial_bearing": "N",
  "initial_bearing_rationale": "audit blocks downstream four-layer enforcement",

  "bearing_trajectory": [
    {
      "ts": "2026-05-22T14:23:00Z",
      "bearing": "N",
      "reason": "spawn",
      "context": "user asked to retrofit four-layer pattern"
    },
    {
      "ts": "2026-05-22T14:31:00Z",
      "bearing": "W",
      "reason": "baseline-discovery",
      "context": "audit revealed grep heuristic too strict; redirected to fix detector first"
    },
    {
      "ts": "2026-05-22T14:48:00Z",
      "bearing": "S",
      "reason": "ship-after-baseline",
      "context": "honest baseline established, now shipping the 4 gap-fills"
    },
    {
      "ts": "2026-05-22T15:42:00Z",
      "bearing": "E",
      "reason": "parallel-emerged",
      "context": "discovered membench OSS could use same pattern; spawned parallel"
    }
  ],

  "final_bearing": "S",
  "final_bearing_at_close": "shipped 12/14 deliverables",

  "bearing_delta": {
    "initial": "N",
    "final": "S",
    "pivots": 3,
    "pivot_kind": "intentional-redirect | unexpected-block | discovery-driven"
  },

  "completion_choice": {...}
}
```

### COC entry — add `bearing` per event

```json
{
  "ts": "...",
  "event": "manifest-written",
  "bearing": "S",                  // ← NEW
  "bearing_was": "W",              // ← NEW (the bearing before this event)
  "bearing_pivot_reason": "...",   // ← NEW (only if bearing changed)
  ...existing fields
}
```

The COC chain becomes the ground-truth trajectory: walking it gives
you the precise sequence of bearings + the moment of every pivot
across every agent across every charter.

### Mission graph node — add `agent_trajectories[]`

```json
{
  "cluster_prefix": ["doctrine", "coverage", "audit"],
  "first_seen": "...",
  "manifest_count": 3,
  "status": "active",

  "agent_trajectories": [
    {
      "agent_type": "maker",
      "agent_pubkey": "ed25519:JrSObB...",
      "session_id": "abc12345",
      "initial_bearing": "N",
      "trajectory": ["N", "W", "S", "E"],  // compact form
      "pivot_count": 3,
      "final_bearing": "E",
      "final_choice": "discover"
    },
    {
      "agent_type": "navigator",
      "agent_pubkey": "ed25519:8kPLqR...",
      "trajectory": ["N", "N", "S"],
      "pivot_count": 1,
      "final_bearing": "S",
      "final_choice": "promote"
    }
  ]
}
```

The mission node becomes a graph of all agents that touched the
mission + the path each one navigated through it.

## Why this matters

### Reputation precision

Today's reputation scoring (`9x_reputation_tracker.py`) probably
uses outcome (completion_choice.kind) + signature counts. With
trajectory data, reputation gains nuance:

- Agents who PIVOT EARLY when their initial bearing was wrong = good
  (they reseat baseline quickly instead of grinding the wrong path)
- Agents who NEVER PIVOT despite mission-graph signals = poor
  navigators (path-dependent; can't read the frontier)
- Agents whose pivots are DISCOVERY-DRIVEN (W → revised
  understanding) = high quality
- Agents whose pivots are UNEXPECTED-BLOCK driven (frequent N
  reseats) = signal of upstream brittleness

### Pattern discovery

Mining the trajectory data across many agents reveals:

- **Mission shape signatures** — some missions consistently produce
  `[N, S]` paths (clean ship); others produce `[N, W, S]` (baseline
  pivot common); others produce `[N, E, E, S, W, S]` (high-thrash).
  The trajectory pattern IS a measurable property of the mission's
  difficulty + clarity.

- **Anti-patterns** — agents that pivot 10+ times on a single
  mission have probably scope-crept. The trajectory length itself
  is a signal.

- **Optimal paths** — agents whose trajectories are short + match
  the final completion_choice's bearing reveal which mission types
  benefit from which spawn-time bearing assignments.

### Forensic replay quality

Today, "what did agent X actually do" reconstruction requires
reading the manifest's `_evolution_log[]` prose. With
`bearing_trajectory[]`, the reconstruction is mechanical:

```
T+0:   spawn, bearing=N (unblock the four-layer audit)
T+8:   pivot to W (baseline shifted; detector heuristic wrong)
T+25:  pivot to S (baseline restored; ship the gap-fills)
T+79:  pivot to E (parallel work emerged; spawned sub-mission)
T+120: close with completion_choice=discover, final bearing=E
```

Five lines. The whole arc. No prose required.

## What needs to ship

### Cut 1 — Schema

Three schema additions:
- `forensics/schemas/shape/manifest.schema.json` — add
  `bearing_trajectory[]` with `{ts, bearing, reason, context}`
- `forensics/schemas/shape/coc-entry.schema.json` — add `bearing`,
  `bearing_was`, `bearing_pivot_reason` (optional, all)
- `forensics/schemas/shape/mission-graph-node.schema.json` — add
  `agent_trajectories[]`

### Cut 2 — Manifest writer

`scripts/0x_manifest_writer.py` accepts `bearing_trajectory[]` in
the input dict; rejects manifests where the trajectory's final
bearing doesn't match the completion_choice's downstream bearing
(consistency check).

### Cut 3 — COC append

`scripts/_charter_lib::append_coc_entry()` (or wherever COC entries
are built) — accepts optional `bearing` + `bearing_was` from the
caller. Doesn't require them (backward compatible) but encourages
their use via deprecation warning when missing.

### Cut 4 — Mission graph accretion

When a manifest with `bearing_trajectory[]` lands, the
mission-graph indexer extracts the trajectory + agent identity
and appends to that mission's `agent_trajectories[]`.

### Cut 5 — Skill alignment

`fast-evo/SKILL.md` Beat 4 (Crystallize) updated to require
agents record their bearing trajectory:

> Beat 4 — CRYSTALLIZE: Your manifest MUST include
> `bearing_trajectory[]` with entries at every bearing change.
> At minimum: one entry at spawn (initial_bearing) and one at
> close (final_bearing). Pivots between get their own entries.

### Cut 6 — Audit + shape

New shape: `bearing.trajectory.tracked` — fraction of recent
manifests that carry `bearing_trajectory[]`. Target_direction =
increasing. The audit records this as a positive template.

## Implementation note — four-layer enforcement

This work fits exactly into the four-layer pattern:

- **Structural** — schemas defining bearing_trajectory shape
- **Cognitive** — fast-evo SKILL.md updated; agents reminded to
  record pivots
- **Reactive** — manifest-writer rejects manifests where trajectory
  is missing OR inconsistent
- **Recovery** — audit + `bearing.trajectory.tracked` shape catches
  drift over time

The full doctrine arc 08-20 is now complete:
- 08 dynamics, 09 types, 10 naming, 11 emergence, 12 claim,
- 13 shape, 14 formulas, 15 F↔M alignment, 16 MaaS/MaA,
- 17 compression-vs-crystallization, 18 FFMx,
- 19 charter accretion, **20 bearing trajectories**

## Single-line summary

**Today we record an agent's initial bearing + final completion
choice; we don't record the PATH between them. The fix:
`bearing_trajectory[]` on the manifest, `bearing` per COC entry,
`agent_trajectories[]` on mission graph nodes. The full vector
path becomes structured data — replayable, mineable, reputable.
Pivot count + pivot kind become measurable shapes; agents that
reseat their baseline quickly when wrong gain reputation; agents
that thrash on a single mission surface as patterns.**

---

*Closes the 13-doctrine arc for 2026-05-22 (08-20). Implementation
needs a focused MAKER pass — schema + writer + accretion + skill +
audit. Should be the next major dispatch.*
