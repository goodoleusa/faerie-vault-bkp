---
type: folder-index
status: active
created: 2026-04-20
tags: [index, membench]
parent: "[[HOME.md]]"
up: "[[HOME.md]]"
child: ["[[00-Metrics/_INDEX]]", "[[01-Literature/_INDEX]]", "[[02-Dashboards/_INDEX]]", "[[03-Baselines/_INDEX]]", "[[04-Methods/_INDEX]]"]
doc_hash: sha256:6873b1a9038ea39d33ca036ad2a3161df655049996d4ce8744a43cd6b3dadc19
hash_ts: 2026-04-20T21:59:43Z
hash_method: body-sha256-v1
---

> [⌂ Home](HOME.md)

# membench Vault — Full Index

| Path | Description |
|------|-------------|
| [[HOME.md]] | Entry point — reading path, quick links, why membench exists |
| **00-Metrics/** | Metric definitions, formulas, collection methods |
| [[00-Metrics/_INDEX]] | Metrics folder index |
| [[00-Metrics/SBI-Switchboard-Index]] | SBI composite overview (9 metrics) |
| [[00-Metrics/SI-Stigmergy-Index]] | SI composite overview (10 metrics) |
| [[00-Metrics/MBI-Membench-Index]] | MBI = 0.5·SBI + 0.5·SI |
| [[00-Metrics/sbi/IRR-Inline-Reasoning-Ratio]] | IRR — inline deliberation before spawn |
| [[00-Metrics/sbi/STL-Spawn-Turn-Latency]] | STL — turns to first Agent call |
| [[00-Metrics/sbi/MTC-Main-Token-Cost]] | MTC — main tokens per agent return |
| [[00-Metrics/sbi/ARD-Agent-Return-Density]] | ARD — returns per session hour |
| [[00-Metrics/sbi/CTD-Context-Token-Debt]] | CTD — tokens since last spawn |
| [[00-Metrics/sbi/WCR-Wave-Completion-Rate]] | WCR — manifests / agents spawned |
| [[00-Metrics/sbi/SPX-Switchboard-Purity-Index]] | SPX — weighted spawn-turn fraction |
| [[00-Metrics/sbi/TDR-Token-Delegation-Ratio]] | TDR — subagent / total tokens |
| [[00-Metrics/sbi/RAL-Return-to-Action-Latency]] | RAL — tokens notification → next action |
| [[00-Metrics/si/OMR-Orphaned-Manifest-Rate]] | OMR — manifests written but never read |
| [[00-Metrics/si/MPL-Manifest-Pickup-Latency]] | MPL — turns to manifest citation |
| [[00-Metrics/si/SDR-Stigmergic-Discovery-Rate]] | SDR — self-discovery vs told |
| [[00-Metrics/si/CMR-Coordination-Message-Ratio]] | CMR — SendMessage vs manifest-triggered |
| [[00-Metrics/si/CSS-Cross-Session-Signal-Survival]] | CSS — REVIEW-QUEUE pickup next session |
| [[00-Metrics/si/BPR-Broadcast-Propagation-Rate]] | BPR — shared droplets reaching siblings |
| [[00-Metrics/si/CD-Cascade-Depth]] | CD — autonomous agent chain length |
| [[00-Metrics/si/PCR-Path-Collision-Rate]] | PCR — overlapping agent writes |
| [[00-Metrics/si/SFE-Spec-File-Effectiveness]] | SFE — spec-file first-attempt success |
| [[00-Metrics/si/SHL-Signal-Half-Life]] | SHL — manifest age at pickup |
| [[00-Metrics/ISR-Insight-Surfacing-Rate]] | ISR — validated insights per session hour (MaA) |
| [[00-Metrics/FPR-Flow-Preservation-Rate]] | FPR — sessions without human stall (MaA) |
| [[00-Metrics/COC-WORM-AR-Auto-Route-Rate]] | COC-WORM-AR — forensic WORM auto-upload rate (MaA) |
| [[00-Metrics/CPI-Cost-Per-Insight]] | CPI — tokens per validated insight (MaaS) |
| **01-Literature/** | Background concepts and theoretical foundations |
| [[01-Literature/Stigmergy-Origins-Grasse]] | Grassé 1959, termites, stigmergic coordination |
| [[01-Literature/Stigmergy-in-Software-Systems]] | Theraulaz & Bonabeau, multi-agent software |
| [[01-Literature/Switchboard-Principle]] | Faerie core: main = switchboard, not worker |
| [[01-Literature/Piston-Wave-Model]] | W1/W2/W3 wave architecture |
| [[01-Literature/Anti-Gaming-Bundle-Model]] | Sub never reads own card — anti-anchoring |
| [[01-Literature/Equilibrium-Principle]] | Crystallization vs compression |
| [[01-Literature/MaaS-vs-MaA-Framework]] | Two composites, two optimization targets |
| **02-Dashboards/** | Dataview queries for live metric monitoring |
| [[02-Dashboards/Session-Health]] | Latest SBI/SI/MBI per session |
| [[02-Dashboards/Metric-Trends]] | Per-metric trend tables |
| [[02-Dashboards/Flag-Table]] | Metrics in flag zone |
| **03-Baselines/** | Measured session snapshots |
| [[03-Baselines/baseline-2026-04-20]] | First baseline placeholder |
| **04-Methods/** | Collection procedures and schema documentation |
| [[04-Methods/Collection-Procedure]] | How each metric is collected |
| [[04-Methods/Manifest-Schema-v2]] | triggered_by + files_read field spec |
