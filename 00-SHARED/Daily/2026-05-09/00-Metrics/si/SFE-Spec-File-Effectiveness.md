---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, sfe]
metric_id: SFE
suite: SI
target: "≥ 0.90"
flag_threshold: "< 0.65"
weight_in_composite: null
parent: ["[[../SI-Stigmergy-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[SDR-Stigmergic-Discovery-Rate]]", "[[CMR-Coordination-Message-Ratio]]"]
child: []
doc_hash: sha256:bbbc06042d81342320f3b8b3cbae25b7802f426b0fb1fab71e74386c24643a78
hash_ts: 2026-04-20T22:04:21Z
hash_method: body-sha256-v1
---

> [↑ SI](../SI-Stigmergy-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# SFE — Spec File Effectiveness

## Definition

First-attempt success rate for agent runs that used a spec file (`STUDIO-SPEC.md` or equivalent) to receive their instructions rather than inline spawn prompt text.

## Formula

```
SFE = spec_file_first_attempt_successes / spec_file_agent_runs
```

## Target

- **Target:** ≥ 0.90 (spec files reliably guide agents on first attempt)
- **Flag threshold:** < 0.65 (spec files are failing — agents not reading them or spec content is poor)
- **Composite weight:** null (informational; not included in SI composite — sample size too small in early sessions)

## Why It Matters

The spec file pattern (`NO AGENT RACES` rule: write spec file → spawn one agent that reads it once → agent executes) is the stigmergic alternative to racing multiple agents or sending SendMessage updates mid-flight. SFE measures whether this pattern actually works when used. Low SFE suggests either the spec format is unclear, agents aren't reading the file at startup, or the task complexity exceeds what a static spec can capture.

This metric is informational because spec file usage is opt-in and sessions may have zero spec-file-guided agents, making the denominator undefined.

## Collection

**Data source:** Spawn prompt analysis (does prompt reference a spec file?) + WCR-style completion check.
**Sampling:** Per agent run that uses spec file pattern.

## Failure Modes

- **Undefined sessions:** Sessions with no spec-file-guided agents: SFE = null, not 0. Do not flag.
- **Environment failure vs spec failure:** Agent failed due to missing dependency, not spec content. Technically counts against SFE but shouldn't — adds noise. Note `failure_cause: environment` separately.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "SFE"
SORT created DESC
LIMIT 10
```

## Related

- [[SDR-Stigmergic-Discovery-Rate]]
- [[CMR-Coordination-Message-Ratio]]
- [[../SI-Stigmergy-Index]]
