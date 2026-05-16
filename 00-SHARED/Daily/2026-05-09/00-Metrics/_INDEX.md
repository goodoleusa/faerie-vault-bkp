---
type: folder-index
status: active
created: 2026-04-20
tags: [index, metrics]
parent: "[[../INDEX.md]]"
up: "[[../INDEX.md]]"
child: ["[[SBI-Switchboard-Index]]", "[[SI-Stigmergy-Index]]", "[[MBI-Membench-Index]]"]
doc_hash: sha256:8c1cc2ea10d79f17a3154da5bd849a5a5cecd3df441595004cfdd8ef54d2491d
hash_ts: 2026-04-20T21:59:36Z
hash_method: body-sha256-v1
---

> [↑ Vault Index](../INDEX.md) · [⌂ Home](../HOME.md)

# 00-Metrics — All Metric Definitions

## Composite Scores

| File | Description |
|------|-------------|
| [[SBI-Switchboard-Index]] | 9-metric delegation quality index |
| [[SI-Stigmergy-Index]] | 10-metric coordination quality index |
| [[MBI-Membench-Index]] | Combined session health index |

## SBI Metrics (Switchboard Index)

| ID | File | Target | Flag |
|----|------|--------|------|
| IRR | [[sbi/IRR-Inline-Reasoning-Ratio]] | < 0.15 | > 0.30 |
| STL | [[sbi/STL-Spawn-Turn-Latency]] | 0 | ≥ 2 |
| MTC | [[sbi/MTC-Main-Token-Cost]] | < 2K | > 8K |
| ARD | [[sbi/ARD-Agent-Return-Density]] | ≥ 3/hr | < 1/hr |
| CTD | [[sbi/CTD-Context-Token-Debt]] | < 8K | > 20K |
| WCR | [[sbi/WCR-Wave-Completion-Rate]] | ≥ 0.90 | < 0.70 |
| SPX | [[sbi/SPX-Switchboard-Purity-Index]] | ≥ 0.80 | < 0.50 |
| TDR | [[sbi/TDR-Token-Delegation-Ratio]] | ≥ 0.85 | < 0.60 |
| RAL | [[sbi/RAL-Return-to-Action-Latency]] | < 500 | > 2K |

## SI Metrics (Stigmergy Index)

| ID | File | Target | Flag |
|----|------|--------|------|
| OMR | [[si/OMR-Orphaned-Manifest-Rate]] | < 0.10 | > 0.30 |
| MPL | [[si/MPL-Manifest-Pickup-Latency]] | < 1 turn | > 3 turns |
| SDR | [[si/SDR-Stigmergic-Discovery-Rate]] | ≥ 0.80 | < 0.50 |
| CMR | [[si/CMR-Coordination-Message-Ratio]] | < 0.20 | > 0.60 |
| CSS | [[si/CSS-Cross-Session-Signal-Survival]] | ≥ 0.85 | < 0.50 |
| BPR | [[si/BPR-Broadcast-Propagation-Rate]] | ≥ 0.70 | < 0.30 |
| CD | [[si/CD-Cascade-Depth]] | ≥ 2 | 0 |
| PCR | [[si/PCR-Path-Collision-Rate]] | 0 | > 0.05 |
| SFE | [[si/SFE-Spec-File-Effectiveness]] | ≥ 0.90 | < 0.65 |
| SHL | [[si/SHL-Signal-Half-Life]] | < 2h | > 12h |

## MaA / MaaS Extended Metrics

| ID | File | Suite | Target | Flag |
|----|------|-------|--------|------|
| ISR | [[ISR-Insight-Surfacing-Rate]] | MaA | ≥ 2/hr | < 0.5/hr |
| FPR | [[FPR-Flow-Preservation-Rate]] | MaA | ≥ 0.90 | < 0.70 |
| COC-WORM-AR | [[COC-WORM-AR-Auto-Route-Rate]] | MaA | 1.0 | < 0.80 |
| CPI | [[CPI-Cost-Per-Insight]] | MaaS | lower is better | 2× median |
