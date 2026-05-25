---
type: dashboard
status: active
tags: [dashboard, health, eval, queue, memory]
parent: Dashboards/INDEX
up: Dashboards/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:2a7529b19b4a3b8424e76398177d023257a77f7d2c82fcdbd2fd23eee1f8847f
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

> [↑ Dashboards](INDEX.md) · [⌂ Home](../../HOME.md)

# System Health

Narrative interpretation of the /metrics output structure.
For live data: `python3 ~/.claude/scripts/9x_lean_query.py --get-all`

---

## How to Read the Health Dashboard

When you run `/metrics`, faerie produces output like this:

```
SYSTEM HEALTH — 2026-04-24T15:00Z
================================================================
EVAL:  composite=0.68  target=0.75  delta=-0.07
  T (Memory/Retention):     0.72  target=0.75
  M (Task quality):         0.65  target=0.70
  R (Citation accuracy):    0.68  target=0.75
  F (Model routing):        0.71  target=0.80

GAPS:
  QUALITY=0.65     → write NECTAR for session findings (↑M)
  MODEL_ROUTING=0.71 → tag spawns w1-/w2- per wave (↑F)

QUEUE:   pending=8  in-flight=2  complete=127
MEMORY:  HONEY=2.1K  NECTAR=847 entries  pollen=3 active sessions
CONTEXT: 42%  wave=W2  agents-in-flight=2
================================================================
```

---

## EVAL Line Interpretation

| Reading | Interpretation | Action |
|---------|---------------|--------|
| composite ≥ 0.75 | Healthy | Continue current practices |
| composite 0.65-0.74 | Acceptable | Address highest-gap dimension |
| composite < 0.65 | Needs attention | Run /dev-eval, address gaps |

The composite score is a weighted average of all active dimensions.
The delta shows movement from last session.

---

## GAPS Line

Gaps are dimensions below their target. The system shows at most 2 gaps
inline, with dual-task hints (actions that improve 2+ dimensions).

If GAPS line is absent: all dimensions at target. No action needed.

---

## QUEUE Interpretation

| Reading | Interpretation |
|---------|---------------|
| pending high, in-flight low | Ready to run — `/run` to execute |
| in-flight high | Agents running — wait or check manifests |
| pending = 0 | Queue empty — add tasks or check /dev-eval |

---

## MEMORY Interpretation

| Reading | Interpretation |
|---------|---------------|
| HONEY < 2K | Healthy (plenty of headroom) |
| HONEY 4-5K | Near budget — /crystallize upcoming |
| HONEY > 5K | Over budget — /crystallize needed |
| NECTAR entry count growing | Normal — append-only by design |
| pollen = 0 | No active sessions or /handoff just ran |

---

## CONTEXT Interpretation

| Reading | Interpretation |
|---------|---------------|
| < 70% | Normal — all waves available |
| 70-85% | W3 should be running in background |
| > 85% | Compact queued — W3 synthesis window closing |

---

## Related

- [[eval-snapshot]] — per-dimension breakdown
- [[piston-state]] — wave and context detail
- [[../Skills-Reference/metrics]] — /metrics quick-ref
- [[../Skills-Reference/dev-eval]] — deeper analysis
