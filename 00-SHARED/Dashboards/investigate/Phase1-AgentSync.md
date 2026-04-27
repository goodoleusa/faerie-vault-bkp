---
type: dashboard
stage: investigate
tags: [dashboard, investigation, agent-sync, live]
description: Phase 1 investigation command center — agent activity, findings review, queue status
parent:
  - "[[HOME]]"
sibling:
  - "[[Hypothesis-Tracker]]"
  - "[[Pipeline-Gates]]"
  - "[[Data-Ingest-Pipeline]]"
child:
  - "[[Annotation-Dash]]"
doc_hash: sha256:ac9d38ff7a83dc3356c68402cc7ff18b805ede6d18780e29513a75f43676c1a7
hash_ts: 2026-03-29T16:10:00Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|← HOME]] · **Phase 1 — Investigation** · [[Hypothesis-Tracker|Hypotheses →]] · [[Pipeline-Gates|Gates →]]
> [[Annotation-Dash|Annotate findings]] · [[Phase2-Publication|Phase 2 →]]

# Phase 1 — Investigation Command Center

> **Mode:** Agent-driven. You review, annotate, redirect.
> **When to shift to Phase 2:** When the Waves are all in "Review" status and Tier 1 evidence covers all 4 active hypotheses.

---

## Latest Session

![[session-briefs/LATEST-brief#Agent Queue]]

---

## Agent Findings — Needs Your Review

> *HIGH flags from agents. Accept → annotate in Obsidian. Reject → annotate why.*

```dataview
TABLE WITHOUT ID
  file.link AS "Item",
  cat AS "Cat",
  priority AS "Pri",
  agent AS "Agent",
  dateformat(date(ts), "MM-dd") AS "Date"
FROM "00-SHARED/Human-Inbox/findings" OR "00-SHARED/Human-Inbox/flags"
WHERE review_status = "unreviewed"
SORT choice(priority = "HIGH", 0, choice(priority = "MED", 1, 2)) ASC, ts DESC
LIMIT 25
```

---

## Agent Deliveries — Outbox

```dataview
TABLE WITHOUT ID
  file.link AS "Draft",
  type AS "Type",
  agent_author AS "Agent",
  confidence_level AS "Conf",
  tier AS "Tier",
  dateformat(file.ctime, "MM-dd") AS "Delivered"
FROM "00-SHARED/Agent-Outbox"
SORT file.ctime DESC
LIMIT 15
```

---

## Hypothesis Status

![[session-briefs/LATEST-brief#Hypothesis Health]]

---

## Open Investigation Gaps

> From `gap_priority_order.json` — auto-updated by evidence-curator.

**Critical (block Tier 1 promotion):**
- [ ] LLNL cert type on 45.130.147.179 (controlbanding.llnl.gov) — needed to complete nuclear triple
- [ ] AS45102 link for cdn181.awsdns-531.com — 5 sibling domains not checked
- [ ] BlurbStudio.cr WHOIS — potential pivot from ORNL finding
- [ ] userId a458bkg9pb95tgb8 identity — Levenshtein=1 from known DOGE account

**Open threads (supporting evidence):**
- [ ] `SUCKMYCHOCOLATESALTYBALLS.DOGE.GOV` — WHOIS/DNS history, active status
- [ ] `ahmn.co` — current operator of 172.93.110.120 (was Packetware container registry)
- [ ] `400yaahc.gov` — unusual .gov on Russian AEZA IP; attribution missing
- [ ] Russian Starlink INNs 231533996303 + 232524834996 — shared directorships with Aeza/Baxet

---

## Cross-Session Connections (Last 7 Days)

```dataview
TABLE WITHOUT ID
  file.link AS "Finding",
  hypothesis_support AS "H",
  confidence_level AS "Conf",
  promotion_state AS "State",
  dateformat(file.mtime, "MM-dd") AS "Found"
FROM "00-SHARED"
WHERE (type = "evidence" OR type = "agent-review-item" OR type = "agent-draft")
  AND file.mtime >= date(today) - dur(7 days)
SORT confidence_level DESC
LIMIT 15
```

---

## Recently Updated Investigations

```dataview
TABLE WITHOUT ID
  file.link AS "Investigation",
  type AS "Type",
  dateformat(file.mtime, "MM-dd HH:mm") AS "Updated"
FROM "10-Investigations"
SORT file.mtime DESC
LIMIT 10
```

---

## Quick Actions

| Action | How |
|--------|-----|
| New Evidence | QuickAdd → **New Evidence Item** → `30-Evidence/` |
| New Entity | QuickAdd → **New Entity Stub** → `20-Entities/` |
| New Task | QuickAdd → **New Task** → `00-SHARED/Queue/` |
| Research Log | QuickAdd → **Today's Research Log** → `01-Memories/` |

---

*[[HOME|← HOME]] · [[Hypothesis-Tracker|Hypotheses]] · [[Pipeline-Gates|Gates]] · [[Annotation-Dash|Annotate]] · [[Phase2-Publication|Phase 2 →]]*
