---
type: index
status: active
tags: [index, dashboards, metrics, health]
parent: 00-SHARED/INDEX
up: 00-SHARED/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:ed3e22af288d8efd4a7335f1da70ef8ba84e819560a220b2dac0c212c16d92bb
hash_ts: 2026-04-25T01:10:51Z
hash_method: body-sha256-v1
---

> [↑ 00-SHARED](../INDEX.md) · [⌂ Home](../../HOME.md)

# Dashboards — System State Narratives

Narrative versions of system health and state metrics.
These are read-only interpretations — not live data.
For live queries: `python3 ~/.claude/scripts/9x_lean_query.py --get-all`

---

## Dashboards

| Dashboard | What it shows |
|-----------|--------------|
| [[system-health]] | Composite system health — eval scores, queue, memory |
| [[piston-state]] | Current wave + queue depth + agents in flight |
| [[eval-snapshot]] | Quality scores by dimension + gap analysis |
| [[stigmergy-state]] | Autonomy %, discovery chains, droplet counts, emergence |

---

## Related

- [[../Skills-Reference/metrics]] — /metrics skill quick-ref
- [[../Skills-Reference/dev-eval]] — /dev-eval skill quick-ref
- [[../Glossary/terms]] — eval dimensions defined
