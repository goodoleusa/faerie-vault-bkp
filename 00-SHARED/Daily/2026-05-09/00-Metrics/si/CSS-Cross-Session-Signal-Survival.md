---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, css]
metric_id: CSS
suite: SI
target: "≥ 0.85"
flag_threshold: "< 0.50"
weight_in_composite: 0.10
parent: ["[[../SI-Stigmergy-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[SHL-Signal-Half-Life]]", "[[BPR-Broadcast-Propagation-Rate]]"]
child: []
doc_hash: sha256:06b27d97ea5b4065888756cac7cc7412b88b065c5d1dd535189fa833a402a01d
hash_ts: 2026-04-20T21:59:34Z
hash_method: body-sha256-v1
---

> [↑ SI](../SI-Stigmergy-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# CSS — Cross-Session Signal Survival

## Definition

Fraction of signals written to REVIEW-QUEUE during session N that are acknowledged (read and acted on or dismissed) in session N+1.

## Formula

```
CSS = REVIEW-QUEUE_signals_picked_up_next_session / signals_written_this_session
```

## Target

- **Target:** ≥ 0.85 (≤ 15% of cross-session signals leak)
- **Flag threshold:** < 0.50 (majority of signals vanish between sessions)
- **Composite weight:** 0.10

## Why It Matters

CSS measures whether the persistent memory layer is actually closing the loop. REVIEW-QUEUE is the mechanism by which insights, flags, and HIGH-priority observations survive session boundaries. If signals are written but not picked up, each session starts partly blind — the context that crystallized during deep work is lost, and the system doesn't accumulate. Low CSS means the HONEY/NECTAR pipeline is leaking at its earliest stage.

## Collection

**Data source:** `~/.claude/memory/REVIEW-QUEUE.json` (signal IDs and write timestamps) + session N+1 NECTAR promotion log or pollen MEM blocks referencing the signal IDs.
**Sampling:** Per session boundary.

## Failure Modes

- **Deliberate signal deferral:** Some HIGH signals are noted as "not urgent, review next sprint." These are legitimately deferred, not leaked. Distinguish by priority field: `MED/LOW` deferrals don't count against CSS.
- **Session never followed:** If session N is the most recent session (no N+1), CSS is undefined for that session. Do not penalize.
- **Promotion vs acknowledgment:** NECTAR promotion by memory-keeper counts as survival. Human dismissal in `/memory` also counts. A signal that is still in REVIEW-QUEUE with status `pending` after session N+1 ends is leaked.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "CSS"
SORT created DESC
LIMIT 10
```

## Related

- [[SHL-Signal-Half-Life]]
- [[BPR-Broadcast-Propagation-Rate]]
- [[../SI-Stigmergy-Index]]
