---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, maa, coc-worm-ar]
metric_id: COC-WORM-AR
suite: MaA
target: "1.0"
flag_threshold: "< 0.80"
weight_in_composite: 0.05
parent: ["[[MBI-Membench-Index]]"]
up: "[[_INDEX.md]]"
sibling: ["[[FPR-Flow-Preservation-Rate]]", "[[../sbi/WCR-Wave-Completion-Rate]]"]
child: []
doc_hash: sha256:ec2d740bf61dfc335aedb703322c1b614df0eda85f493f434c316bf08819168d
hash_ts: 2026-04-20T21:59:32Z
hash_method: body-sha256-v1
---

> [↑ MBI](MBI-Membench-Index.md) · [⌂ Metrics Index](_INDEX.md) · [📊 Dashboard](../02-Dashboards/Session-Health.md)

# COC-WORM-AR — Chain-of-Custody WORM Auto-Route Rate

## Definition

Fraction of forensic events (hash chain entries, COC log appends, evidence manifest writes) that are automatically uploaded to WORM storage (B2/S3) without human intervention.

## Formula

```
COC-WORM-AR = forensic_events_uploaded_to_WORM_without_human / total_forensic_events
```

## Target

- **Target:** 1.0 (every forensic event reaches WORM automatically)
- **Flag threshold:** < 0.80 (more than 20% of COC events require human action to persist)
- **Composite weight:** 0.05 (in MaA composite)

## Why It Matters

The three-store architecture (repo/forensics/ → vault → WORM) is only as strong as its automatic propagation. If forensic events require human intervention to reach WORM, the chain of custody is fragile — a missed upload, a session that ends without handoff, a context compact that fires at the wrong moment — and evidence that should be immutable is at risk. COC-WORM-AR = 1.0 means the system handles its own forensic hygiene. Anything less means the human is a required step in the COC, which contradicts the MaA goal of autonomous forensic integrity.

This metric has no MaaS equivalent — MaaS systems don't maintain a forensic chain of custody.

## Collection

**Data source:** `{repo}/forensic/coc.jsonl` (write timestamps) vs B2 backup logs (upload timestamps).
**Sampling:** Per session, at /handoff.
**Parser:** Match COC entries to B2 upload manifest. Events present in COC but absent from B2 log = not auto-routed.

## Failure Modes

- **B2 throttle:** B2 API rate limits can delay uploads without permanent failure. Distinguish transient delay from missed upload by checking next-session upload logs.
- **Offline sessions:** If the WSL instance had no internet during the session, WORM upload is physically impossible. Flag `offline_session: true`; do not penalize COC-WORM-AR.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "COC-WORM-AR"
SORT created DESC
LIMIT 10
```

## Related

- [[FPR-Flow-Preservation-Rate]]
- [[../sbi/WCR-Wave-Completion-Rate]]
- [[../01-Literature/MaaS-vs-MaA-Framework]]
