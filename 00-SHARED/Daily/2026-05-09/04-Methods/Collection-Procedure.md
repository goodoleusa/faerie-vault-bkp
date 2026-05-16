---
type: methodology
status: active
created: 2026-04-20
tags: [methods, collection, metrics]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Manifest-Schema-v2]]"]
child: []
doc_hash: sha256:40f68918c1212b8dae2207b65ebc4a9bd53d8834bd587d212aec4227eeacafd0
hash_ts: 2026-04-20T21:59:42Z
hash_method: body-sha256-v1
---

> [↑ Methods Index](_INDEX.md) · [→ Schema](Manifest-Schema-v2.md) · [⌂ Home](../HOME.md)

# Collection Procedure

How each membench metric is measured. This document mirrors `COLLECTION.md` at the membench repo root — consult that file for the authoritative technical detail. This vault page surfaces the key decisions and edge cases for human reference.

**Source file:** `/mnt/d/0LOCAL/gitrepos/membench/COLLECTION.md`

---

## SBI Metrics — Quick Reference

All SBI metrics are sourced from `session_metrics.py` output or session transcript analysis. The full integration spec is in `BENCHMARKS.md §Integration with session_metrics.py`.

| Metric | Source | Edge Case |
|--------|--------|-----------|
| IRR | Pre-spawn text token count | Session start context load inflates; discount turn-0 |
| STL | Turn index delta | No Agent call in session → record ∞ |
| MTC | session_metrics.py main token delta | Exclude turn-0 initialization |
| ARD | task_notification count / session hours | W3 background agents counted at collection time |
| CTD | Token counter since last Agent call | Legitimate high CTD at session start |
| WCR | manifests_found / agents_spawned | W3 checked at 24h window |
| SPX | Weighted spawn-turn fraction | Context-load turns are not spawn turns; flag separately |
| TDR | subagent_tokens / total_tokens | W3 Opus agents correctly inflate sub-agent fraction |
| RAL | Token delta: TaskNotification → next action | W3 returns get looser threshold (< 2K) |

---

## SI Metrics — Key Decisions

### SDR — Prompt-Path Proxy

The hardest metric to measure accurately. The proxy compares paths in spawn prompts vs paths in `manifest.files_read`. Two important edge cases:

1. **Directory hint vs file path:** If spawn prompt mentions `/mnt/d/.../wave1/` and agent reads files under that directory, count as "told" (the directory hint directed discovery).
2. **Schema v1 sessions:** If `files_read` is absent from manifest, skip the task entirely. Do not impute SDR = 0.

Requires manifest schema v2. See [[Manifest-Schema-v2]].

### CD — Chain-Walk Algorithm

CD requires `triggered_by` field in every manifest. The chain-walk starts from root manifests (those with `triggered_by = "user"` or `"faerie-turn-0"`) and follows the chain. Multi-branch chains take the deepest branch.

Defend against cycles with a visited set. Cycles should not occur architecturally but can appear during debugging.

### OMR — Citation Detection Proxy

Citation = manifest path appears as a string in a later spawn prompt. Limitation: a path mentioned but not acted on counts as "read." This is an acceptable proxy — the alternative (verifying the agent acted on the data) requires reading the agent's decision process.

---

## New Metrics (MaA Suite) — Collection Notes

### ISR — Insight Surfacing Rate

No direct measurement signal in most sessions. Use the following proxy:

1. Count droplets promoted to NECTAR by memory-keeper at /handoff (these were validated as worth promoting).
2. Count vault doc linkages created from pollen MEM blocks.
3. If explicit `cat=VALIDATED` flag is present in pollen, count directly.

Target: ≥ 2/hour. This will be low (possibly < 1) in early sessions before the validation pattern is established.

### FPR — Stall Detection

A stall = 60s elapsed with no agent return, no user output from faerie, while human is in active session. Requires session telemetry timestamps. Proxy: if `session_metrics.py` reports session duration but the agent return timestamps show 60s+ gaps, flag as potential stall.

### COC-WORM-AR — B2 Upload Matching

Match `forensic/coc.jsonl` entries to B2 upload logs. The B2 backup tool at `~/tools/b2-backup/` should log uploads with timestamps. COC events without a matching B2 entry within 24h of write = not auto-routed.

---

## Collector Scripts

| Metric | Script |
|--------|--------|
| SI composite | `collectors/si_calculator.py` |
| OMR | `collectors/omr_collector.py` |
| SDR | `collectors/sdr_collector.py` |
| CD | `collectors/cd_collector.py` |
| MBI | `collectors/mbi_calculator.py` |
| SBI | `collectors/sbi_calculator.py` |

All scripts accept `--session-id` and `--since` args; output JSON to stdout.
