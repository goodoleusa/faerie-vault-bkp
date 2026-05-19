---
type: audit
title: "Orphan routing — RESOLVED 2026-05-19"
emoji: "✅"
generated: 2026-05-19
status: resolved
tags: [audit, orphans, crystallization]
N: ['[Dashboards/00-Home](Dashboards/00-Home.md)']
S: ['[HELP/crystallization-workflow](HELP/crystallization-workflow.md)']
---

# ✅ Orphan routing — resolved

Loose `.md` files that pre-dated the lifecycle ladder have been routed
via `git mv` (history preserved). Snapshot of the routing actually applied:

| Original | Routed to |
|---|---|
| `agent-context-evolving.md` | `HELP/` |
| `DAE-Evolution-Narrative.md` | `Design-Narratives/` |
| `DEPRECATIONS.md` | `Faerie-System-Internals/` |
| `ENVIRONMENT-SETUP.md` | `HELP/` |
| `HOW-ANNOTATION-COC-WORKS.md` | `HELP/` |
| `HOW-SYNC-WORKS.md` | `HELP/` |
| `Human-Inbox.md` / `Human-Inbox 1.md` | deleted (empty stubs); new `Human/_index.md` is the folder note |
| `PIPELINE-DESIGN.md` | `Design-Narratives/` |
| `PRIORITY.md` | `Dashboards/` |
| `QUICKSTART.md` | `HELP/` |
| `VAULT-SCHEMA.md` | `Faerie-System-Internals/` |
| `WRITE-ROUTING.md` | `Faerie-System-Internals/` |
| `ZimaBoard-Remote-Access-Quickstart.md` | `HELP/` |

`00-SHARED.md` retained as the folder note for `00-SHARED/` itself.

## Remaining loose root files (intentional)

- `00-SHARED.md` — folder note for `00-SHARED/` (Obsidian folder-note convention)
- `_orphans-needing-routing.md` — this audit (kept as record)

The lifecycle ladder is the canonical surface now. New notes should land
in `Ephemeral/{date}/{task_id}/` (agents) or `Human/{date}/` (you) and be
promoted from there.
