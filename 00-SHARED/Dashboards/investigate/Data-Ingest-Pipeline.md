---
type: dashboard
stage: investigate
tags: [dashboard, data-ingest, pipeline, runs]
cssclass: wide-page
parent:
  - "[[HOME]]"
sibling:
  - "[[Phase1-AgentSync]]"
  - "[[Hypothesis-Tracker]]"
  - "[[Pipeline-Gates]]"
doc_hash: sha256:4fe253dd942c4f55ccf96a679f375fc30b038067526364f9b5b480adc459d44f
hash_ts: 2026-03-29T16:10:00Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|← HOME]] · [[Phase1-AgentSync|← Command Center]] · [[Pipeline-Gates|← Gates]] · **Data-Ingest Pipeline**

# Data-Ingest Pipeline — Run Tracker

> *Full view from raw data → curated evidence. One row per pipeline run.*
> *Phase-Narrative notes drive this dashboard — apply [[Phase-Narrative.blueprint]] at each run start.*
> *Between runs: annotate gaps, set blockers, queue next run directly from here.*

---

## ⚡ Active / In-Progress Runs

```dataview
TABLE pipeline_run AS "Run", phase_ingest AS "Ingest", phase_clean AS "Clean",
      phase_curate AS "Curate", phase_analyze AS "Analyze", phase_publish AS "Publish",
      tier1_count AS "T1", tier2_count AS "T2", files_processed AS "Files"
FROM ""
WHERE type = "phase-narrative" AND (status = "in-progress" OR status = "partial")
SORT file.mtime DESC
```

---

## ✅ Completed Runs

```dataview
TABLE pipeline_run AS "Run", file.ctime AS "Date",
      tier1_count AS "T1", tier2_count AS "T2", tier3_count AS "T3",
      files_processed AS "Files", entities_extracted AS "Entities",
      ipfs_cid AS "IPFS", promotion_state AS "State"
FROM ""
WHERE type = "phase-narrative" AND status = "complete"
SORT file.ctime DESC
```

---

## 🔴 Blocked — Needs Action Before Next Run

```dataview
TABLE pipeline_run AS "Run", file.mtime AS "Last Updated"
FROM ""
WHERE type = "phase-narrative" AND status = "blocked"
SORT file.mtime DESC
```

---

## 📊 Pipeline Progress — All Runs Combined

```dataview
TABLE WITHOUT ID
  rows.phase_ingest AS "Phase",
  length(filter(rows, (r) => r.phase_ingest = "complete")) AS "✅ Done",
  length(filter(rows, (r) => r.phase_ingest = "in-progress")) AS "⚡ Running",
  length(filter(rows, (r) => r.phase_ingest = "pending")) AS "⏳ Pending",
  length(filter(rows, (r) => r.phase_ingest = "failed")) AS "❌ Failed"
FROM ""
WHERE type = "phase-narrative"
GROUP BY "Ingest"
LIMIT 1
```

---

## 🧱 Open Gaps / Blockers (across all runs)

```dataview
LIST file.link + " — " + pipeline_run
FROM ""
WHERE type = "phase-narrative"
  AND (phase_ingest = "failed" OR phase_curate = "failed"
       OR phase_analyze = "failed" OR phase_publish = "pending")
  AND status != "complete"
SORT file.mtime DESC
```

---

## 📦 Evidence Inventory (by tier, all runs)

```dataview
TABLE WITHOUT ID
  rows.tier AS "Tier",
  length(rows) AS "Total",
  length(filter(rows, (r) => r.ann_hash != null AND r.ann_hash != "")) AS "Annotated",
  length(filter(rows, (r) => r.promotion_state = "crystallized")) AS "→ HONEY"
FROM "30-Evidence" OR "00-SHARED/Agent-Outbox"
WHERE type = "evidence" OR type = "phase-narrative"
GROUP BY tier
SORT tier ASC
```

---

## 🔎 Evidence Ready for Final Analysis

```dataview
TABLE evidence_id AS "ID", tier AS "Tier", confidence_level AS "Conf",
      hypothesis_support AS "Hypotheses", pipeline_run AS "Run",
      date_analyzed AS "Analyzed"
FROM "30-Evidence"
WHERE tier <= 2 AND ann_hash != null AND ann_hash != ""
SORT tier ASC, confidence_level DESC
LIMIT 20
```

---

## 📬 Agent Deliveries Awaiting Review (Agent-Outbox)

```dataview
TABLE evidence_id AS "ID", pipeline_run AS "Run", confidence_level AS "Conf",
      tier AS "Tier", source_type AS "Source", file.ctime AS "Delivered"
FROM "00-SHARED/Agent-Outbox"
WHERE status = "awaiting-human"
SORT file.ctime DESC
LIMIT 15
```

*Review → promote: move file from `Agent-Outbox/` to `30-Evidence/`, apply [[Evidence-Item.blueprint]].*

---

## 🗂 NECTAR Entries by Run

```dataview
TABLE date_found AS "Found", sprint_id AS "Sprint",
      hypothesis_support AS "Hypotheses", confidence_delta AS "Δ",
      promotion_state AS "State"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry"
SORT pipeline_run DESC, date_found DESC
```

---

## 📋 Run Completion Checklist

*For a run to be "done" and ready for final analysis, all boxes must be checked:*

```dataview
TABLE pipeline_run AS "Run",
  choice(phase_ingest = "complete", "✅", "⬜") AS "Ingest",
  choice(phase_clean = "complete", "✅", "⬜") AS "Clean",
  choice(phase_curate = "complete", "✅", "⬜") AS "Curate",
  choice(phase_analyze = "complete", "✅", "⬜") AS "Analyze",
  choice(phase_publish = "complete", "✅", "⬜") AS "Publish",
  choice(ipfs_cid != null AND ipfs_cid != "", "✅", "⬜") AS "IPFS",
  tier1_count AS "T1"
FROM ""
WHERE type = "phase-narrative"
SORT file.ctime DESC
```

---

## 🔢 How Many Runs Remain?

```dataview
TABLE WITHOUT ID
  length(filter(rows, (r) => r.status = "complete")) AS "Runs Complete",
  length(filter(rows, (r) => r.status = "in-progress")) AS "Runs Active",
  length(filter(rows, (r) => r.status = "pending" OR r.status = "blocked")) AS "Runs Queued",
  sum(map(filter(rows, (r) => r.status = "complete"), (r) => r.tier1_count)) AS "T1 Total"
FROM ""
WHERE type = "phase-narrative"
GROUP BY "summary"
```

*Tag a Phase-Narrative with `status: pending` to pre-register planned runs.*
*When a run is queued in sprint-queue.json, create the Phase-Narrative note immediately so it shows here.*
