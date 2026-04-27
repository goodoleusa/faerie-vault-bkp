---
type: index
tags: [index, human-inbox, daily-check]
parent:
  - "[[00-SHARED/00-SHARED|00-SHARED]]"
sibling:
  - "[[00-SHARED/Dashboards/_index|Dashboards]]"
  - "[[00-SHARED/Queue/_index|Queue]]"
  - "[[00-SHARED/Droplets/_index|Droplets]]"
  - "[[00-SHARED/Agent-Outbox/_index|Agent Outbox]]"
child:
  - "[[00-SHARED/Human-Inbox/flags/_index|Flags]]"
  - "[[00-SHARED/Human-Inbox/findings/_index|Findings]]"
doc_hash: sha256:53d5b3888ca4306a899a5e83e08ad89e7c65c048a2e8e4a61f33b10b6a5a37d4
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:35Z
hash_method: body-sha256-v1
---

> [!nav]
> [[00-SHARED/Dashboards/HOME|← HOME]] · **You are here: Inbox** · [[00-SHARED/Agent-Outbox/_index|Dig Into Raw →]] · [[00-SHARED/Queue/_index|Plan Work →]]
> [[00-SHARED/Human-Inbox/flags/_index|Flags]] · [[00-SHARED/Human-Inbox/findings/_index|Findings]] · [[00-SHARED/Dashboards/Annotation-Dash|Annotate →]]

# Human Inbox

Your daily check spot. Agents surface things here for your attention.

## How to Use

```
Human-Inbox/
  flags/           ← HIGH priority alerts — check these first
  findings/        ← Summaries needing your review or promotion to 30-Evidence/
```

Each item links to its **raw source** in [[00-SHARED/Agent-Outbox/|Agent-Outbox]]. Read the summary here; follow the link when you want the actual data, agent files, or full analysis.

## Quick Workflow

1. Open `flags/` — anything HIGH needs attention now
2. Open `findings/` — review, annotate, promote to [[30-Evidence/]] if confirmed
3. Want raw data? Follow the `Source:` link in any item → lands in Agent-Outbox
4. Decision flows back to repo COC via `vault_annotation_sync.py`

## Other Places You Check

| Folder | What's there | How often |
|--------|-------------|-----------|
| [[00-SHARED/Queue/sprint-queue|Queue/]] | Sprint tasks — edit priority, add notes, sync back | When planning |
| [[00-SHARED/Dashboards/|Dashboards/]] | FFFF views, session briefs, status | When orienting |
| `Droplets/` | Real-time insight capture (LIVE-*.md, BRIDGE-*.md) | When curious what was captured |
| [[00-SHARED/Agent-Outbox/|Agent-Outbox/]] | Raw agent work — reports, analysis, extractions | On-demand drill-down |

## What Goes Where (for agents)

- Agent writes draft → `Agent-Outbox/` (raw work product)
- Agent flags something → `REVIEW-INBOX.md` mirror → `flags/` (atomized by inbox_router.py)
- Agent confirms finding → `findings/` (human promotes to 30-Evidence/)

> [!chain]- Chain: #3 · agent-lint · 2026-03-28T16:05Z
> chain: `criticalexposure` · prev: `sha256:59c5db3de…` · this: `sha256:add9bad0a…`
> Verify: `python3 ~/.claude/scripts/note_sign.py verify <this-file>`
