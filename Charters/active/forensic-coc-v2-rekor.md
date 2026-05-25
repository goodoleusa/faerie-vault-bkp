---
type: charter
status: active
charter_id: forensic-coc-v2-rekor
semantic_mission: merkle.rekor.anchor
cluster_prefix: []
phase: "phase_1_kickoff"
author: goodoleusa
created: 2026-05-24
canonical_repo_path: "forensics/charters/active/2026-05-24Z__charter__forensic-coc-v2-rekor__goodoleusa.json"
filename_base: "2026-05-24Z__charter__forensic-coc-v2-rekor__goodoleusa"
tags: [charter, pseudosystem]
blueprint: "[[Charter.blueprint]]"
---

# Charter — forensic-coc-v2-rekor

> **Vault pseudosystem mirror** — canonical source: `forensics/charters/active/2026-05-24Z__charter__forensic-coc-v2-rekor__goodoleusa.json`
> Status: **active** | Phase: **phase_1_kickoff** | Mission: `[[merkle.rekor.anchor]]`

---

## Thesis

(see canonical JSON)

## Phases

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| phase_1_kickoff | Shadow writing — observe-only, zero risk |  | active |
| phase_2_merkle_batching | Cutover — v2 becomes authoritative for new events |  | blocked_on_phase_1 |
| phase_3_rekor_anchor | v2 genesis block + Sigstore Rekor hourly anchoring |  | blocked_on_phase_2 |
| phase_4_legacy_archival | Legacy chain pinned + new audits use v2 exclusively |  | blocked_on_phase_3 |
| phase_5_hardening | Long-lived notary key + cold storage + compaction policy |  | blocked_on_phase_4 |

## Operator Pain Points

- (none)

## Non-Goals

- (none)

## Related Charters

- (none)

---

*To jump to canonical JSON: open `forensics/charters/active/2026-05-24Z__charter__forensic-coc-v2-rekor__goodoleusa.json` in repo. Vault note is navigation-only — do not edit to change charter state.*
