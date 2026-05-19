---
type: routing
updated: 2026-03-28
tags: [meta, routing, agents, coc]
description: Where agents write in the vault, and how humans find what they wrote
doc_hash: sha256:f0376b04ee4a9ffe41521ff6690c357f843be9a4670edad9a1fb664f401c6f6d
hash_ts: 2026-03-29T16:10:51Z
hash_method: body-sha256-v1
---

# Agent Write Routing — 00-SHARED

## Where Agents Write

| Content Type | Write To | Format |
|---|---|---|
| Finding drafts | `Agent-Outbox/criticalexposure/` | FINDING-template.md |
| Analysis reports | `Agent-Outbox/analysis/` | free-form .md |
| Evidence extractions | `Agent-Outbox/extractions/` | free-form .md |
| Viz/charts | `Agent-Outbox/viz/` | .md + .png |
| HIGH flags | `Human-Inbox/flags/REVIEW-INBOX.md` | append only |
| Findings for review | `Human-Inbox/findings/` | summary + link to Agent-Outbox source |
| Session briefs | `Dashboards/session-briefs/` | LATEST-brief.md |
| Droplets | `Droplets/LIVE-{date}.md` | append, real-time |
| Bridge-promoted | `Droplets/BRIDGE-{date}.md` | auto-promoted from memory_bridge |
| Design narratives | `00-META/` | `NN-TITLE.md` (sequential numbering) |
| HONEY dev edits | `Hive/honey-dev/dev/` | HONEY-*.md |
| Agent context | `Agent-Context/` | read-mostly snapshots |
| Sprint queue | `Queue/sprint-queue.md` | bidirectional sync |
| Templates | `templates/` | .md |

## Where Humans Check

```
DAILY:         Human-Inbox/  → flags/ (urgent) + findings/ (review)
PLANNING:      Queue/        → edit sprint-queue.md, syncs back to session
CURIOUS:       Droplets/     → LIVE-*.md (what was captured today?)
ORIENTING:     Dashboards/   → FFFF views, session briefs

ON-DEMAND:     Agent-Outbox/ → raw data behind any Human-Inbox summary
               Agent-Context/→ onboarding + collaboration bundle
```

## Flow: Summary → Raw Data

Every Human-Inbox item links to its source in Agent-Outbox. You read the 3-line summary; follow the link for full analysis, raw data, agent working files. Two clicks from flag to raw.

## Ownership Rule (no collisions)

Every file has exactly ONE writer. The other side reads only.

**Agent-owned** (agents write, humans read):
- `Agent-Outbox/*` — raw work products
- `Agent-Context/*` — memory snapshots
- `Dashboards/*` — FFFF views, session briefs
- `Droplets/*` — real-time captures (LIVE-*.md, BRIDGE-*.md)
- `Human-Inbox/flags/*` — REVIEW-INBOX mirror (append-only)
- `Human-Inbox/findings/*` — summaries agents generate

**Human-owned** (humans write, agents read via explicit sync):
- `Queue/sprint-queue.md` — edit tasks, reorder, add `> annotations`
- `Inbox/*` — QuickAdd, brainstorms, organic notes
- `30-Evidence/*` — promoted findings (agents never see)
- `00-PROTECTED/*` — dead zone

**Human annotations on agent files** — use `.ann.md` sibling files:
- Agent writes `findings/FIND-001.md` → human creates `findings/FIND-001.ann.md`
- Sync scripts never touch `.ann.md` files
- `vault_annotation_sync.py` reads `.ann.md` → routes decision back to repo COC

## Collaboration

HONEY is designed to be shareable. `Agent-Context/README.md` has the onboarding protocol.
