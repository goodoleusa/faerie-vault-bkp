---
type: charter
status: active
charter_id: mcp-dispatcher-only-migration
semantic_mission: mcp.surface.unify
cluster_prefix: ["mcp", "surface", "unify"]
phase: ""
author: goodoleusa
created: 2026-05-23
canonical_repo_path: "forensics/charters/active/2026-05-23Z__charter__mcp-dispatcher-only-migration__goodoleusa.json"
filename_base: "2026-05-23Z__charter__mcp-dispatcher-only-migration__goodoleusa"
tags: [charter, pseudosystem]
blueprint: "[[Charter.blueprint]]"
---

# Charter — mcp-dispatcher-only-migration

> **Vault pseudosystem mirror** — canonical source: `forensics/charters/active/2026-05-23Z__charter__mcp-dispatcher-only-migration__goodoleusa.json`
> Status: **active** | Phase: **** | Mission: `[[mcp.surface.unify]]`

---

## Thesis

The MCP server currently exposes ~41 flat tools AND ~10 verb dispatchers, with a Category-A/B
distinction on inner helpers that the lint stack has to special-case. Operator chose Option B
(dispatcher-only) as the right shape for an MCP-first world: the LLM is the primary caller; forcing
it to wade through 41 flat tools is worse UX than asking the frontend to spell `{verb: "list"}`.
Migration: drop the flat tools, keep the dispatchers, eliminate the Category A/B distinction
entirely.

## Phases

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| phase_1_pilot_charter | Pilot family — charter (smallest, well-understood) | 4 | queued |
| phase_2_manifest | manifest family | 6 | queued |
| phase_3_mission_and_shape | mission + shape families (smaller scope, fast pass) | 4 | queued |
| phase_4_remaining_families | vault, chat, consolidate, sign, spawn, coc | 6 | queued |
| phase_5_lint_simplification | Drop the Category A/B distinction from the linter | 2 | queued |

## Operator Pain Points

- (none)

## Non-Goals

- (none)

## Related Charters

- (none)

---

*To jump to canonical JSON: open `forensics/charters/active/2026-05-23Z__charter__mcp-dispatcher-only-migration__goodoleusa.json` in repo. Vault note is navigation-only — do not edit to change charter state.*
