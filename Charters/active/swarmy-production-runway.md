---
type: charter
status: active
charter_id: swarmy-production-runway
semantic_mission: 
cluster_prefix: ["production", "vault", "caddy"]
phase: "phase 2 active"
author: goodoleusa
created: 2026-05-21
canonical_repo_path: "forensics/charters/active/2026-05-21Z__charter__swarmy-production-runway__goodoleusa.json"
filename_base: "2026-05-21Z__charter__swarmy-production-runway__goodoleusa"
tags: [charter, pseudosystem]
blueprint: "[[Charter.blueprint]]"
---

# Charter — swarmy-production-runway

> **Vault pseudosystem mirror** — canonical source: `forensics/charters/active/2026-05-21Z__charter__swarmy-production-runway__goodoleusa.json`
> Status: **active** | Phase: **phase 2 active** | Mission: `[[]]`

---

## Thesis

Close the gap between 'code shipped to disk' and 'running cleanly on swarmy.retrofuture.tech with
full observability'. This charter unifies four parallel work streams: (1) finish the faerie→swarmy
rename across env vars + compose + Caddy, (2) overhaul .env / .env.example for OpenHands .agents/
convention, (3) consolidate forensics/ from 13 → ≤10 canonical subdirs, (4) wire W&B for live
observability of internal evolution + external membench metrics.

## Phases

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| (see repo JSON for phase details) | | | |

## Operator Pain Points

- (none)

## Non-Goals

- Building new visualization tooling — use W&B dashboards, do not build a custom UI
- Migrating off OpenRouter — current routing is fine, optimize models within OR
- Touching the `cybertemplate` container restart loop (separate concern; unblocks separately)
- Architectural changes to mission-graph (the-hive shipped that; don't re-litigate)

## Related Charters

- (none)

---

*To jump to canonical JSON: open `forensics/charters/active/2026-05-21Z__charter__swarmy-production-runway__goodoleusa.json` in repo. Vault note is navigation-only — do not edit to change charter state.*
