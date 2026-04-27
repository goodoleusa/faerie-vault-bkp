---
type: dashboard
stage: investigate
tags: [dashboard, hypotheses, evidence-tracking]
parent:
  - "[[HOME]]"
sibling:
  - "[[Phase1-AgentSync]]"
  - "[[Pipeline-Gates]]"
  - "[[Data-Ingest-Pipeline]]"
doc_hash: sha256:a9b0828766a7287a136dafd75d30d023aa6161fa467453c5a1777f3b39578327
hash_ts: 2026-03-29T16:10:00Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|← HOME]] · [[Phase1-AgentSync|← Agent Command]] · **Hypothesis Tracker** · [[Pipeline-Gates|Gates →]] · [[Annotation-Dash|Annotate →]]

# Hypothesis Tracker

## Live Confidence — Latest Brief

![[session-briefs/LATEST-brief#Hypothesis Health]]

---

## H1 — The Insider
*DOGE insider access enabled by credential misuse*

```dataview
TABLE WITHOUT ID
  file.link AS "Finding",
  cat AS "Cat",
  priority AS "Pri",
  confidence_level AS "Conf",
  dateformat(date(ts), "MM-dd") AS "Date"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Agent-Outbox"
WHERE contains(string(hypothesis_support), "H1") OR contains(string(tags), "H1")
SORT priority ASC, ts DESC
LIMIT 10
```

## H2 — The Pipeline
*Packetware/Prometheus as data exfiltration pipeline*

```dataview
TABLE WITHOUT ID
  file.link AS "Finding",
  cat AS "Cat",
  priority AS "Pri",
  confidence_level AS "Conf",
  dateformat(date(ts), "MM-dd") AS "Date"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Agent-Outbox"
WHERE contains(string(hypothesis_support), "H2") OR contains(string(tags), "H2")
SORT priority ASC, ts DESC
LIMIT 10
```

## H3 — The Breach
*Treasury/federal systems breached via known vulnerabilities*

```dataview
TABLE WITHOUT ID
  file.link AS "Finding",
  cat AS "Cat",
  priority AS "Pri",
  confidence_level AS "Conf",
  dateformat(date(ts), "MM-dd") AS "Date"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Agent-Outbox"
WHERE contains(string(hypothesis_support), "H3") OR contains(string(tags), "H3")
SORT priority ASC, ts DESC
LIMIT 10
```

## H4 — The Handoff
*Data handoff to foreign actors (Russia/China)*

```dataview
TABLE WITHOUT ID
  file.link AS "Finding",
  cat AS "Cat",
  priority AS "Pri",
  confidence_level AS "Conf",
  dateformat(date(ts), "MM-dd") AS "Date"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Agent-Outbox"
WHERE contains(string(hypothesis_support), "H4") OR contains(string(tags), "H4")
SORT priority ASC, ts DESC
LIMIT 10
```

## H5 — The Coverup (DEAD)
*Published as null result — contextual material preserved as timeline context only.*

```dataview
TABLE WITHOUT ID
  file.link AS "Finding",
  cat AS "Cat",
  priority AS "Pri",
  dateformat(date(ts), "MM-dd") AS "Date"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Agent-Outbox"
WHERE contains(string(hypothesis_support), "H5") OR contains(string(tags), "H5")
SORT ts DESC
LIMIT 5
```

---

## Confidence Over Time

```dataview
TABLE WITHOUT ID
  file.link AS "Brief",
  h_conf_H1_doge_insider_access AS "H1",
  h_conf_H2_pipeline_compromise AS "H2",
  h_conf_H3_active_breach AS "H3",
  h_conf_H4_foreign_handoff_apt AS "H4",
  dateformat(date(date), "MM-dd") AS "Date"
FROM "00-SHARED/Dashboards/session-briefs"
WHERE type = "session-brief" AND h_conf_H1_doge_insider_access != null
SORT date DESC
LIMIT 15
```

---

## Evidence Distribution

```dataview
TABLE WITHOUT ID
  rows.cat AS "Category",
  length(rows) AS "Count"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Agent-Outbox"
WHERE hypothesis_support != null
GROUP BY cat
SORT length(rows) DESC
```

---

*[[HOME|← HOME]] · [[Phase1-AgentSync|Command Center]] · [[Annotation-Dash|Annotate]] · [[Pipeline-Gates|Gates]]*
