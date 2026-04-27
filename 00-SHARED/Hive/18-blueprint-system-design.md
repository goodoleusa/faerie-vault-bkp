---
type: design-narrative
blueprint: blueprint_design_insight
title: "Blueprint System for Agent Output Types"
agent_type: fullstack-developer
session_id: 2026-03-29-a3f8c1
generated: 2026-03-29
status: active
impact: HIGH
doc_hash: sha256:pending
promotion_state: raw
coc_ref: ~/.claude/memory/forensics/
tags: [design, adr, blueprints, vault-schema]
related:
  - "[[VAULT-SCHEMA]]"
  - "[[System-Architecture]]"
---

# 18 — Blueprint System for Agent Output Types

## Context

Audit of the vault on 2026-03-29 (see [[00-SHARED/Agent-Outbox/blueprint-audit-2026-03-29]])
revealed that 50 blueprints were nominally defined in VAULT-SCHEMA.md but only 7 were actively
referenced by agents (86% unused). Agent output files had inconsistent frontmatter — missing
`agent_type`, `session_id`, `promotion_state`, and `blueprint` reference fields.

The root cause: blueprints were defined as schema snippets inside a large monolithic document,
not as standalone agent-readable template files. Agents writing via the CLI had no practical
way to consult a 260-line schema doc mid-task. Without an authoritative template, each agent
improvised — leading to fragmented schemas that Dataview queries couldn't reliably use.

## Decision

We will create per-type blueprint files in `Hive/blueprints/` as standalone markdown documents,
covering the 5 most active output types: Agent-Evolution, Droplet, Dashboard, Session-Manifest,
and Design-Insight. Each blueprint file contains: required frontmatter spec, optional fields,
section requirements, structure rules, validation rules, and a link to an example output.

Blueprint files are referenced from agent output frontmatter via `blueprint: blueprint_{type}`.
Spawn prompts for agents that produce these types will include the blueprint path so agents
can check the schema at write time.

## Alternatives Considered

- **Single VAULT-SCHEMA.md mega-document:** Already exists and demonstrably unused in practice.
  Splitting by type makes each schema digestible and directly linkable from spawn prompts.
- **Enforce via Python validation script:** Useful downstream but doesn't help agents know what
  to write. Script catches errors after the fact; a blueprint prevents them at write time.
- **Obsidian template injection:** Obsidian templates work for human-authored notes but agents
  write directly via CLI — they never open the Obsidian template picker. Agent-readable markdown
  files solve the CLI path that human templates don't cover.
- **Inline in agent cards:** Agent cards are per-type (800-token budget), not per-output-type.
  One agent type may produce multiple output types. Blueprints separate the concerns cleanly.

## Trade-offs

| Trade-off | Description |
|-----------|-------------|
| Gains | Per-type schema clarity; agents can reference single authoritative file at write time |
| Gains | Dataview queries on `promotion_state`, `agent_type`, `blueprint` become reliable |
| Gains | Blueprint is evolvable independently of VAULT-SCHEMA.md |
| Costs | 5 new files to maintain; drift risk if blueprint is updated but old outputs are not |
| Costs | Agents must be explicitly pointed to blueprint path in spawn prompt (not automatic) |
| Risks | Schema fragmentation — blueprint and VAULT-SCHEMA.md may diverge over time |
| Deferred | Automated validation at write time (would require a write hook — separate task) |
| Deferred | Backfilling `blueprint` field on existing agent outputs (separate maintenance task) |

## Impact

- `Hive/blueprints/` now contains 8 blueprint files (3 pre-existing + 5 new)
- Example outputs created in Agent-Outbox/ for each new blueprint
- System-Architecture.md updated with Blueprint Registry section linking all blueprints
- Future spawn prompts for fullstack-developer, memory-keeper, research-analyst will include
  the relevant blueprint path
- Dataview coverage dashboard (see example at Agent-Outbox/dashboards/example-dashboard.md)
  now shows live blueprint adoption rate
- VAULT-SCHEMA.md remains canonical for the universal frontmatter definition; per-type
  blueprints are the write-time reference layer on top of it
