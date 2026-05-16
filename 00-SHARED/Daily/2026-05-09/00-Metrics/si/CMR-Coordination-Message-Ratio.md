---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, cmr]
metric_id: CMR
suite: SI
target: "< 0.20"
flag_threshold: "> 0.60"
weight_in_composite: 0.15
parent: ["[[../SI-Stigmergy-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[SDR-Stigmergic-Discovery-Rate]]", "[[BPR-Broadcast-Propagation-Rate]]"]
child: []
doc_hash: sha256:84823dc277f90d7cb6f17c175bb106ec1fc0f60c55bc6eed2236875505b2b5aa
hash_ts: 2026-04-20T21:59:34Z
hash_method: body-sha256-v1
---

> [↑ SI](../SI-Stigmergy-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# CMR — Coordination Message Ratio

## Definition

Fraction of coordination events that are direct messages (SendMessage calls) rather than manifest-triggered agent actions. Measures the balance between direct messaging and filesystem-mediated coordination.

## Formula

```
CMR = SendMessage_calls / (SendMessage_calls + manifest_triggered_actions)
```

## Target

- **Target:** < 0.20 (direct messaging is exceptional, not the default)
- **Flag threshold:** > 0.60 (majority of coordination is via direct chat, not shared state)
- **Composite weight:** 0.15

## Why It Matters

SendMessage has legitimate uses: mid-flight updates to a running agent, team coordinator messages, urgent redirects. But if it's the dominant coordination mechanism, agents are chatting rather than coordinating through state — which breaks the key stigmergy property of persistence. A pheromone trail persists; a message does not. When the session compacts or an agent restarts, messages are lost. Manifests survive.

Note: CMR does not say SendMessage is bad. CMR = 0 is not the target — some direct messaging is natural. CMR < 0.20 means "direct messaging is the exception, filesystem is the rule."

## Collection

**Data source:** Session transcript tool call counts.
**Sampling:** Per session.
**Parser:** Count `SendMessage(...)` calls; count `Agent(...)` calls whose prompt body cites a `wave*-result.json` path.

## Failure Modes

- **Team coordination:** W2/W3 teams using SendMessage between teammates are doing legitimate coordination — this inflates CMR. Consider filtering team-internal SendMessages from CMR (or reporting CMR_team and CMR_main separately).
- **Missing manifest citations:** Agent calls where the spawn reason is a manifest but the path isn't literally in the prompt body will be undercounted. Improves with schema v2 adoption.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "CMR"
SORT created DESC
LIMIT 10
```

## Related

- [[SDR-Stigmergic-Discovery-Rate]]
- [[BPR-Broadcast-Propagation-Rate]]
- [[../SI-Stigmergy-Index]]
