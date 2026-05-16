---
type: home
status: active
created: 2026-04-20
tags: [home, membench, metrics, faerie]
doc_hash: sha256:f758bfc4a89474aee990fc0ffe4c029ddfe404704dba7f5a696e4a903fe55034
hash_ts: 2026-04-20T21:59:29Z
hash_method: body-sha256-v1
---

> [⌂ INDEX](INDEX.md) · [📊 Dashboards](02-Dashboards/_INDEX.md) · [📚 Literature](01-Literature/_INDEX.md) · [📐 Metrics](00-Metrics/_INDEX.md)

# membench — Multi-Agent Session Benchmark

Measures the operational health of the faerie multi-agent system across two axes:

1. **[[00-Metrics/SBI-Switchboard-Index|SBI — Switchboard Index]]** — how well the main session stays lean and delegates
2. **[[00-Metrics/SI-Stigmergy-Index|SI — Stigmergy Index]]** — how well agents coordinate through the filesystem

Composite: **[[00-Metrics/MBI-Membench-Index|MBI]]** = 0.5·SBI + 0.5·SI

---

## Why This Exists

The faerie system depends on two disciplines holding simultaneously. First: the main session must stay lean — it is a switchboard, not a worker. When it starts reasoning at length before spawning, or synthesizing what agents should synthesize, it accumulates context debt and session throughput collapses. Second: agents must coordinate through the filesystem without being told where to look. A manifest at the expected path is the message. When agents self-discover their inputs and trigger downstream chains autonomously, the system scales. When they wait for inline instructions, they're just remote procedures with extra overhead.

SBI measures the first discipline. SI measures the second. When both hold, session throughput is high and the human gets leverage. When either fails, the session stalls — either main becomes a bottleneck (low SBI) or agents work in isolation and the human has to broker every handoff (low SI). Measuring makes both visible so they can be corrected.

---

## Quick Links

- [[02-Dashboards/Session-Health|Latest session health]]
- [[02-Dashboards/Flag-Table|Current flags]]
- [[04-Methods/Collection-Procedure|How metrics are collected]]
- [[01-Literature/Stigmergy-Origins-Grasse|What is stigmergy?]]
- [[01-Literature/Switchboard-Principle|The switchboard principle]]

---

## Reading Path

**First-time visitor:**

1. [[01-Literature/Switchboard-Principle|The switchboard principle]] — why main stays lean
2. [[01-Literature/Stigmergy-Origins-Grasse|Stigmergy origins]] — why agents coordinate via files
3. [[00-Metrics/SBI-Switchboard-Index|SBI metrics suite]] — 9 delegation metrics
4. [[00-Metrics/SI-Stigmergy-Index|SI metrics suite]] — 10 coordination metrics
5. [[02-Dashboards/Session-Health|Live dashboard]] — current readings

**Metric deep-dive:**

- SBI metrics: [[00-Metrics/sbi/IRR-Inline-Reasoning-Ratio|IRR]] · [[00-Metrics/sbi/STL-Spawn-Turn-Latency|STL]] · [[00-Metrics/sbi/TDR-Token-Delegation-Ratio|TDR]] · [[00-Metrics/sbi/WCR-Wave-Completion-Rate|WCR]] · [[00-Metrics/sbi/SPX-Switchboard-Purity-Index|SPX]]
- SI metrics: [[00-Metrics/si/OMR-Orphaned-Manifest-Rate|OMR]] · [[00-Metrics/si/SDR-Stigmergic-Discovery-Rate|SDR]] · [[00-Metrics/si/CD-Cascade-Depth|CD]] · [[00-Metrics/si/CSS-Cross-Session-Signal-Survival|CSS]] · [[00-Metrics/si/PCR-Path-Collision-Rate|PCR]]

**Context:**

- [[01-Literature/Piston-Wave-Model|The piston wave model]] — W1/W2/W3 wave architecture
- [[01-Literature/Anti-Gaming-Bundle-Model|Anti-gaming bundle model]] — why subs never read their own cards
- [[01-Literature/Equilibrium-Principle|Equilibrium principle]] — crystallization vs compression

---

## MaaS vs MaA — Two Composites

membench measures the same telemetry against two different optimization targets. See [[01-Literature/MaaS-vs-MaA-Framework]] for the full framework.

- **[[00-Metrics/MBI-Membench-Index|MBI]]** — the MaA health composite (SBI + SI). Primary indicator for faerie sessions.
- **MaA_Score** — extends MBI with ISR, FPR, COC-WORM-AR for deep-investigation operators.
- **MaaS_Score** — cost-efficiency composite (TDR, MTC, CTD, CPI) for API-service operators.

Faerie is a MaA system. MBI is the correct primary indicator. Applying MaaS scoring would penalize the deep-synthesis and coordination behaviors that make faerie valuable.

---

## Current Baseline Status

First measurements pending. Run `/membench baseline` to capture from `session_metrics.py` history.

See [[03-Baselines/baseline-2026-04-20|Baseline placeholder (2026-04-20)]] for schema.
