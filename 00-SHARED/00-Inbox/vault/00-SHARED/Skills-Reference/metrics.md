---
type: reference
status: active
tags: [skill, metrics, health, eval]
parent: Skills-Reference/INDEX
up: Skills-Reference/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:438e93a942d0e1b7a2f5c2bceee2eefa7cbcbcebc4eee0338efa378cee76b4ba
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Skills-Reference](INDEX.md) · [⌂ Home](../../HOME.md)

# /metrics — System Health Snapshot

Shows current system health: eval scores, queue depth, memory status, eval gaps.

---

## Invocation

```
/metrics
```

---

## Output Format

```
SYSTEM HEALTH — 2026-04-24T15:00Z
================================================================
EVAL:  composite=0.68  target=0.75  delta=-0.07
  T (Memory/Retention):     0.72  target=0.75
  M (Task quality):         0.65  target=0.70
  R (Citation accuracy):    0.68  target=0.75
  F (Model routing):        0.71  target=0.80

GAPS (priority order):
  QUALITY=0.65     → write NECTAR for session findings (↑M)
  MODEL_ROUTING=0.71 → tag spawns w1-/w2- per wave (↑F)

QUEUE:   pending=8  in-flight=2  complete=127
MEMORY:  HONEY=2.1K  NECTAR=847 entries  pollen=3 active sessions
CONTEXT: 42%  wave=W2  agents-in-flight=2
================================================================
```

---

## Eval Dimensions

| Dim | Name | Measures |
|-----|------|---------|
| T | Memory/Retention | HONEY/NECTAR retrieval accuracy |
| M | Task quality | done_looks_like criteria match rate |
| R | Citation accuracy | findings-with-sources / total-findings |
| F | Model routing | Haiku usage at W1, Sonnet usage at W2 |

Target: T≥0.75, M≥0.70, R≥0.75, F≥0.80

---

## Gaps Line

When a dimension is below target, the GAPS line shows:
- Which dimension
- Current score
- The dual-task hint (action that improves this dimension AND another)

Max 2 gaps inline. More gaps: `/dev-eval` for full breakdown.

---

## Related

- [[dev-eval]] — deeper eval breakdown
- [[../Dashboards/eval-snapshot]] — narrative eval dashboard
- [[../Glossary/terms]] — eval dimensions, composite score defined
