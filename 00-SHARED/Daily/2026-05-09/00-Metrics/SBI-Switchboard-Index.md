---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, sbi, composite]
metric_id: SBI
suite: SBI
target: "≥ 0.80"
flag_threshold: "< 0.60"
weight_in_composite: 0.5
parent: ["[[../MBI-Membench-Index]]"]
up: "[[../_INDEX.md]]"
child: ["[[sbi/IRR-Inline-Reasoning-Ratio]]", "[[sbi/STL-Spawn-Turn-Latency]]", "[[sbi/TDR-Token-Delegation-Ratio]]"]
doc_hash: sha256:314394df3027b1a3a36e82c6ed9ace2b157b12d423611536b3771692c1a00186
hash_ts: 2026-04-20T21:59:34Z
hash_method: body-sha256-v1
---

> [↑ MBI](MBI-Membench-Index.md) · [⌂ Metrics Index](_INDEX.md) · [📊 Dashboard](../02-Dashboards/Session-Health.md)

# SBI — Switchboard Index

## Definition

Measures how well the main session operates as a pure switchboard — spawning agents quickly, staying lean, and not doing inline work that belongs in subagents.

## Formula

```
SBI = (1 - IRR) * 0.20
    + (1 - normalized_STL) * 0.10
    + (1 - normalized_MTC) * 0.10
    + normalized_ARD * 0.15
    + (1 - normalized_CTD) * 0.10
    + WCR * 0.10
    + SPX * 0.15
    + TDR * 0.10
    + (1 - normalized_RAL) * 0.10
```

## Target

- **Target:** ≥ 0.80
- **Flag threshold:** < 0.60 (piston is stalled)
- **Composite weight:** 0.5 (in MBI)

## Sub-Metrics

| ID | Name | Weight | What it catches |
|----|------|--------|-----------------|
| [[sbi/IRR-Inline-Reasoning-Ratio\|IRR]] | Inline Reasoning Ratio | 0.20 | Deliberating before spawning |
| [[sbi/STL-Spawn-Turn-Latency\|STL]] | Spawn Turn Latency | 0.10 | Slow first spawn after user message |
| [[sbi/MTC-Main-Token-Cost\|MTC]] | Main Token Cost/Return | 0.10 | Expensive main-session inference |
| [[sbi/ARD-Agent-Return-Density\|ARD]] | Agent Return Density | 0.15 | Low throughput |
| [[sbi/CTD-Context-Token-Debt\|CTD]] | Context Token Debt | 0.10 | Growing main context |
| [[sbi/WCR-Wave-Completion-Rate\|WCR]] | Wave Completion Rate | 0.10 | Agents not finishing |
| [[sbi/SPX-Switchboard-Purity-Index\|SPX]] | Switchboard Purity Index | 0.15 | Turns not being spawn events |
| [[sbi/TDR-Token-Delegation-Ratio\|TDR]] | Token Delegation Ratio | 0.10 | Work happening in main, not agents |
| [[sbi/RAL-Return-to-Action-Latency\|RAL]] | Return-to-Action Latency | 0.10 | Slow action on agent returns |

## Why It Matters

A high SBI means faerie is operating as designed: the main session handles orchestration overhead only, subagents do the actual work, and the human's attention is leveraged rather than consumed. A low SBI is a throughput ceiling — every inline reasoning paragraph is tokens burned on coordination that should be in an agent.

## Relationship to SI

SBI and SI are complementary. SBI measures "are we spawning well?" SI measures "are spawned agents coordinating well?" Both must be ≥ 0.80. See [[MBI-Membench-Index]] for the combined picture and [[../01-Literature/Switchboard-Principle|Switchboard Principle]] for the theoretical basis.

## Collection

**Source:** `session_metrics.py` output + session transcript analysis.
**Sampling:** Per session, at session end or on demand.
**Parser:** `collectors/sbi_calculator.py`

## Dashboard Query

```dataview
TABLE session_id, SBI, status
FROM "03-Baselines"
WHERE type = "baseline"
SORT created DESC
LIMIT 10
```

## Related

- [[MBI-Membench-Index]]
- [[SI-Stigmergy-Index]]
- [[../01-Literature/Switchboard-Principle]]
- [[../04-Methods/Collection-Procedure]]
