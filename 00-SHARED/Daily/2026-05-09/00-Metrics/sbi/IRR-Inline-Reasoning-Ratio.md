---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, sbi, irr]
metric_id: IRR
suite: SBI
target: "< 0.15"
flag_threshold: "> 0.30"
weight_in_composite: 0.20
parent: ["[[../SBI-Switchboard-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[STL-Spawn-Turn-Latency]]", "[[SPX-Switchboard-Purity-Index]]"]
child: []
doc_hash: sha256:b89a6ac70a04be3fcab16f1203d4d66c3358c11679cff4a6d3bafce89d21c82f
hash_ts: 2026-04-20T21:59:33Z
hash_method: body-sha256-v1
---

> [↑ SBI](../SBI-Switchboard-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# IRR — Inline Reasoning Ratio

## Definition

Fraction of turns where the main session produced more than 3 reasoning sentences before making an Agent call. Measures how often faerie deliberates when it should be spawning.

## Formula

```
IRR = turns_with_>3_reasoning_sentences_before_spawn / total_turns
```

## Target

- **Target:** < 0.15
- **Flag threshold:** > 0.30 (nearly a third of turns are deliberation turns, not spawn turns)
- **Composite weight:** 0.20 (highest weight in SBI — the most direct measure of switchboard failure)

## Why It Matters

Every paragraph of inline reasoning before a spawn is a token overhead paid by the main session for work that should happen inside an agent. At the extreme, a main session that thinks through problems completely before delegating offers no scalability advantage over a single-agent workflow. IRR is the primary signal of this failure mode — it fires when deliberation has become the main session's default before spawning.

A well-calibrated main session reads context, identifies task, spawns. The reasoning is 1–2 sentences of task framing, not a multi-paragraph analysis.

## Collection

**Data source:** Session transcript — pre-spawn text in each turn.
**Sampling:** Per turn, at response generation.
**Parser:** Count sentences in the response body before the first `Agent(...)` tool call. If > 3, increment `inline_reasoning_turns`.

## Failure Modes

- **False positive:** A turn with many sentences that are task description, not reasoning — context-framing looks like deliberation to a naive sentence counter. Mitigation: weight by reasoning indicators ("therefore", "because", "this means", "I think").
- **False negative:** Reasoning hidden in structured output (bullet lists, code blocks) — sentence counter misses it.
- **Common cause:** Agent's instructions are unclear so main synthesizes before delegating; fix by improving spawn prompt quality.

## Dashboard Query

```dataview
TABLE session_id, value, target, (value - 0.15) as delta
FROM "03-Baselines"
WHERE metric_id = "IRR"
SORT created DESC
LIMIT 10
```

## Related

- [[STL-Spawn-Turn-Latency]]
- [[SPX-Switchboard-Purity-Index]]
- [[../SBI-Switchboard-Index]]
