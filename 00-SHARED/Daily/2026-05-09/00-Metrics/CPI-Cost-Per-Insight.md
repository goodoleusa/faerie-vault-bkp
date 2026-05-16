---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, maas, cpi]
metric_id: CPI
suite: MaaS
target: "lower is better"
flag_threshold: "context-dependent"
weight_in_composite: 0.10
parent: ["[[MBI-Membench-Index]]"]
up: "[[_INDEX.md]]"
sibling: ["[[../sbi/TDR-Token-Delegation-Ratio]]", "[[../sbi/MTC-Main-Token-Cost]]"]
child: []
doc_hash: sha256:35acd07697904619d84c113b0b1572052e1654e6cccdc7ba3dad78392d24da78
hash_ts: 2026-04-20T21:59:32Z
hash_method: body-sha256-v1
---

> [↑ MBI](MBI-Membench-Index.md) · [⌂ Metrics Index](_INDEX.md) · [📊 Dashboard](../02-Dashboards/Session-Health.md)

# CPI — Cost Per Insight

## Definition

Total session tokens divided by novel findings validated by the human. The economic efficiency metric: how much does it cost to produce one accepted insight?

## Formula

```
CPI = total_tokens_session / novel_findings_validated
```

## Target

- **Target:** lower is better (no universal threshold — compare session to session for the same task type)
- **Flag threshold:** context-dependent (2× median for similar sessions is a reasonable flag trigger)
- **Composite weight:** 0.10 (in MaaS composite only — not in MaA composite)

## Why It Matters

CPI is the MaaS operator's primary metric. It answers: "is the system getting cheaper over time at producing value?" A system that gets better at routing to Haiku, caching repeated context, and avoiding redundant agent spawns should show declining CPI over sessions of similar complexity.

CPI is explicitly NOT a MaA metric. MaA accepts higher per-session token costs in exchange for deeper context, longer chains, and compounding cross-session memory. A session with CPI = 50K tokens/insight might be deeply valuable if the insight is a breakthrough finding that reshapes the investigation. CPI would penalize it. The MaA view: cost-per-insight is the wrong denominator when the system is building compounding value.

This distinction is why MaaS and MaA need separate composites. See [[../01-Literature/MaaS-vs-MaA-Framework]].

## Collection

**Data source:** `session_metrics.py` total token count; validated findings count from ISR collection.
**Sampling:** Per session where findings were validated.
**Note:** CPI is only meaningful when ISR is also being tracked. If ISR denominator is imprecise, CPI inherits that imprecision.

## Failure Modes

- **Zero validated findings:** CPI = undefined (divide by zero). Flag session as `insight_count: 0`.
- **Session type mismatch:** CPI for a deep research session (naturally high token cost) vs a triage session is not comparable. Always compare within session type.
- **Caching effects:** Prompt caching (cache HIT) reduces effective token cost without changing token count in some metrics. Ensure CPI uses actual billed tokens, not raw context tokens.

## Dashboard Query

```dataview
TABLE session_id, value, total_tokens, findings_count
FROM "03-Baselines"
WHERE metric_id = "CPI"
SORT created DESC
LIMIT 10
```

## Related

- [[../sbi/TDR-Token-Delegation-Ratio]]
- [[../sbi/MTC-Main-Token-Cost]]
- [[ISR-Insight-Surfacing-Rate]]
- [[../01-Literature/MaaS-vs-MaA-Framework]]
