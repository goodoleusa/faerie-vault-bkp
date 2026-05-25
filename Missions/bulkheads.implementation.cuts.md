---
type: mission
status: open
mission_id: bulkheads.implementation.cuts
task_count: 3
last_ts: "2026-05-23T23:25:46"
bearing_summary: {"S": 3}
charter_ids: ["enterprise-patent-foundation"]
canonical_repo_path: "forensics/mission-graph.json"
tags: [mission, pseudosystem]
blueprint: "[[Mission.blueprint]]"
---

# Mission — bulkheads.implementation.cuts

> **Vault pseudosystem dossier** — canonical source: `forensics/mission-graph.json`
> Task count: **3** | Bearings: **S:3** | Last activity: **2026-05-23**

---

## Related Charters

- [[enterprise-patent-foundation]]

## Open Work

| Bearing | Task ID | Rationale |
|---------|---------|-----------|
| S | egress-allowlist-deny-by-default-flip | current matcher 'WebFetch|WebSearch' catches both, but operator may want a stric |
| S | audit-cron-scheduler-wire | cron-bulkhead-audit.py exists but is not yet scheduled; wire into session_end ho |
| E | egress-source-reputation-feed | egress-allowed/denied jsonl is the natural feed for Bulkhead 3's source-reputati |
| S | bulkhead-audit-promote-to-canonical | audit jsonl + report live in forensics/eval/ — confirm 5x_b2_realtime_uploader q |
| S | wire-sanitization-into-hooks-json | Hooks exist but .openhands/hooks.json may need updates so OH actually invokes th |

## Recent Manifests

- `perimeter-audit` — Bulkhead 1 PERIMETER + audit cron shipped; 2 hooks wired; egress filter live
- `bidirectional-sanitizer` — Bulkhead 2 PURIFICATION wired: sanitize_lib + 2 hooks + audit log + 2 shape move
- `detection-reputation-canary` — Bulkhead-3 wired: detector (4 sub-detectors) + reputation aggregator + canary re

## Narrative

Bulkhead 1 PERIMETER + audit cron shipped; 2 hooks wired; egress filter live Bulkhead 2 PURIFICATION wired: sanitize_lib + 2 hooks + audit log + 2 shape move Bulkhead-3 wired: detector (4 sub-detectors) + reputation aggregator + canary re

---

*Mission dossier derived from `forensics/mission-graph.json`. Schema version: ?. Corpus: 265 manifests.*
