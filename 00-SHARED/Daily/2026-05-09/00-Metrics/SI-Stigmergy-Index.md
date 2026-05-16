---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, composite]
metric_id: SI
suite: SI
target: "≥ 0.80"
flag_threshold: "< 0.55"
weight_in_composite: 0.5
parent: ["[[../MBI-Membench-Index]]"]
up: "[[../_INDEX.md]]"
child: ["[[si/OMR-Orphaned-Manifest-Rate]]", "[[si/SDR-Stigmergic-Discovery-Rate]]", "[[si/CD-Cascade-Depth]]"]
doc_hash: sha256:42fbea1f915304be9d7857039bd1f50d5f7cf576c054f2d2917bb98a0413e0de
hash_ts: 2026-04-20T21:59:35Z
hash_method: body-sha256-v1
---

> [↑ MBI](MBI-Membench-Index.md) · [⌂ Metrics Index](_INDEX.md) · [📊 Dashboard](../02-Dashboards/Session-Health.md)

# SI — Stigmergy Index

## Definition

Measures how well agents coordinate through the filesystem as shared state, without direct messaging. A manifest at the expected path is the message. SI measures whether that principle is actually operating at runtime.

## Formula

```
SI = (1 - OMR)       * 0.20
   + (1 - norm_MPL)  * 0.15
   + SDR             * 0.20
   + (1 - CMR)       * 0.15
   + CSS             * 0.10
   + BPR             * 0.10
   + min(CD/3, 1.0)  * 0.05
   + (1 - PCR)       * 0.05

norm_MPL = min(MPL_turns / 4.0, 1.0)
```

SFE and SHL are tracked informational but not included in the composite (insufficient sample size in early sessions; will be added when baselines establish).

## Target

- **Target:** ≥ 0.80
- **Flag threshold:** < 0.55 (stigmergy is decorative — agents being micromanaged by inline context)
- **Composite weight:** 0.5 (in MBI)

## Sub-Metrics

| ID | Name | Weight | What it catches |
|----|------|--------|-----------------|
| [[si/OMR-Orphaned-Manifest-Rate\|OMR]] | Orphaned Manifest Rate | 0.20 | Manifests emitted but no agent reads them |
| [[si/MPL-Manifest-Pickup-Latency\|MPL]] | Manifest Pickup Latency | 0.15 | Slow downstream response to manifests |
| [[si/SDR-Stigmergic-Discovery-Rate\|SDR]] | Stigmergic Discovery Rate | 0.20 | Agents told where to look vs self-discovering |
| [[si/CMR-Coordination-Message-Ratio\|CMR]] | Coordination Message Ratio | 0.15 | Chat vs manifest-triggered coordination |
| [[si/CSS-Cross-Session-Signal-Survival\|CSS]] | Cross-Session Signal Survival | 0.10 | Signals not picked up next session |
| [[si/BPR-Broadcast-Propagation-Rate\|BPR]] | Broadcast Propagation Rate | 0.10 | Shared droplets not reaching siblings |
| [[si/CD-Cascade-Depth\|CD]] | Cascade Depth | 0.05 | No autonomous trigger chains |
| [[si/PCR-Path-Collision-Rate\|PCR]] | Path Collision Rate | 0.05 | Agent write conflicts |
| [[si/SFE-Spec-File-Effectiveness\|SFE]] | Spec File Effectiveness | — | Informational |
| [[si/SHL-Signal-Half-Life\|SHL]] | Signal Half-Life | — | Informational |

## Why It Matters

Low SI is the failure mode that looks like success. Many agents get spawned (SBI looks good), but they work in isolation — each run starts from inline instructions, manifests go unread, no autonomous chains form. The human ends up brokering every handoff manually. Throughput is capped by the human's attention, not the system's capacity.

High SI means the filesystem is alive: agents find each other's outputs, build on them, and the main session observes rather than coordinates.

## Relationship to SBI

See [[SBI-Switchboard-Index]] and [[MBI-Membench-Index]] for the full relationship model. The short version: high SBI + low SI is the dangerous failure mode. Appears productive, isn't scaling.

## Collection

**Source:** `~/.claude/hooks/state/wave*-result.json`, `broadcast.jsonl`, REVIEW-QUEUE.json, session transcript.
**Sampling:** Per session, at session end.
**Parser:** `collectors/si_calculator.py`

## Dashboard Query

```dataview
TABLE session_id, SI, status
FROM "03-Baselines"
WHERE type = "baseline"
SORT created DESC
LIMIT 10
```

## Related

- [[MBI-Membench-Index]]
- [[SBI-Switchboard-Index]]
- [[../01-Literature/Stigmergy-Origins-Grasse]]
- [[../01-Literature/Stigmergy-in-Software-Systems]]
- [[../04-Methods/Collection-Procedure]]
