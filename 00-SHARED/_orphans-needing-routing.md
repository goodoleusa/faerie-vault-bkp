---
type: audit
title: "Orphans needing routing — 00-SHARED/ loose markdown"
emoji: "🧹"
generated: 2026-05-19
tags: [audit, orphans, crystallization]
N: ['[Dashboards/00-Home](Dashboards/00-Home.md)']
S: ['[HELP/crystallization-workflow](HELP/crystallization-workflow.md)']
E: []
W: []
---

# 🧹 Orphans needing routing

Loose `.md` files at `00-SHARED/` root that pre-date the lifecycle ladder.
**Not deleted.** Flagged here for user review and intentional routing.

| File | Proposed destination | Notes |
|---|---|---|
| `00-SHARED.md` | keep (folder note for 00-SHARED itself) | folder-note convention |
| `agent-context-evolving.md` | `HELP/` or `Faerie-System-Internals/` | onboarding-adjacent |
| `DAE-Evolution-Narrative.md` | `Design-Narratives/` (already exists) | narrative artifact |
| `DEPRECATIONS.md` | `Faerie-System-Internals/` | system-meta |
| `ENVIRONMENT-SETUP.md` | `HELP/` | onboarding |
| `HOW-ANNOTATION-COC-WORKS.md` | `HELP/` | onboarding |
| `HOW-SYNC-WORKS.md` | `HELP/` | onboarding |
| `Human-Inbox.md` / `Human-Inbox 1.md` | merge → `Human/` folder-note | duplicate stub pair |
| `PIPELINE-DESIGN.md` | `Design-Narratives/` | narrative artifact |
| `PRIORITY.md` | `Dashboards/` | dashboard-adjacent |
| `QUICKSTART.md` | `HELP/` | onboarding |
| `VAULT-SCHEMA.md` | `Faerie-System-Internals/` | system-meta |
| `WRITE-ROUTING.md` | `Faerie-System-Internals/` | system-meta |
| `ZimaBoard-Remote-Access-Quickstart.md` | `HELP/` | onboarding |

## Resolution

User: open each row, decide. The crystallization pass (`10-crystallize.py`)
will not touch these until they have proper frontmatter + canonical location.
Until then they are read-only legacy notes — still queryable via search, just
outside the lifecycle ladder.
