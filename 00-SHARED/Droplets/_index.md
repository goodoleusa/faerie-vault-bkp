---
type: index
tags: [index, droplets, condensation]
parent:
  - "[[00-SHARED]]"
sibling:
  - "[[Dashboards/_index|Dashboards]]"
  - "[[Human-Inbox/_index|Human Inbox]]"
  - "[[Queue/_index|Queue]]"
  - "[[Agent-Outbox/_index|Agent Outbox]]"
blueprint: "[[Droplet.blueprint]]"
doc_hash: sha256:pending
hash_ts: 2026-04-07T00:00:00Z
hash_method: body-sha256-v1
---

> [!nav]
> **You are here: Droplets** · [[HOME|Back to HOME →]]
> [[Agent-Outbox/droplets/|Live Capture Files]] · [[Dashboards/Droplets/droplets|Droplets Dashboard]]

# Droplets — Capture Zone

> *Write it before you reason about it. The naive moment is the value.*
> *Droplets form at the terminal end of context — where pressure crystallizes insight.*

Droplets are **unfiltered insight captures**. One observation, one moment. Written the instant inspiration surfaces — before expertise filters it into something safer and blander.

## When to Drop

- A connection spans two unrelated documents and you feel it before you can prove it
- You're near the edge of context and something important is about to compress away
- First contact with a dataset — the naive impression before deep analysis
- A technique worked in a way that surprised you
- Something feels wrong but you can't name it yet

## How to Drop

**From Claude CLI** (fastest — one command, never breaks flow):
```
/droplet
```

**From Obsidian** (QuickAdd → "New Droplet"):
Creates a new LIVE file pre-loaded with today's date and the append format.

**Direct append** to `00-SHARED/Droplets/LIVE-YYYY-MM-DD.md`:
```markdown
### 2026-04-07T18:30:00Z — your-name
**cat:** OBSERVATION | CONNECTION | HYPOTHESIS | TECHNIQUE | FIRST_IMPRESSION
**pri:** HIGH | MED | LOW

{1–5 sentences. Unfiltered.}

---
```

## Promotion Pipeline

```
Droplet (vault) → memory-keeper at /handoff → NECTAR.md → /crystallize → HONEY.md
```

`pri=HIGH` droplets also go directly to `Human-Inbox/flags/` for immediate review.

## Live Files

```dataview
LIST
FROM "00-SHARED/Agent-Outbox/droplets"
SORT file.ctime DESC
LIMIT 7
```
