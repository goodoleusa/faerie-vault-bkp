---
type: dashboard
stage: system
tags: [dashboard, nectar, memory, findings]
cssclass: wide-page
parent:
  - "[[HOME]]"
sibling:
  - "[[Session-Manifests]]"
  - "[[System-Architecture]]"
doc_hash: sha256:f4c309306eca1105731518c86af9b66a9d01ffb829d698c6b31a6c1d49df2c09
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|← HOME]] · **NECTAR Explorer** · [[Session-Manifests|Sessions →]] · [[System-Architecture|Architecture →]]

# NECTAR — Finding Explorer

> *Atomized NECTAR.md entries as sortable, annotatable vault notes.*
> *Source: `vault_nectar_atomize.py` → `00-SHARED/Agent-Outbox/*/nectar-entries/`*
> *To promote a finding to HONEY: open the note, set `promotion_state: crystallized`.*

---

## 🔴 Needs Your Annotation

```dataview
TABLE date_found AS "Found", sprint_id AS "Sprint", pipeline_run AS "Run",
      confidence_level AS "Conf", confidence_delta AS "Δ",
      hypothesis_support AS "Hypotheses", source_agent AS "Agent"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry" AND (ann_hash = null OR ann_hash = "")
  AND (promotion_state = "capture" OR promotion_state = "inbox")
SORT date_found DESC
LIMIT 15
```

---

## ⬆️ Ready to Promote → HONEY

```dataview
TABLE date_found AS "Found", sprint_id AS "Sprint", confidence_level AS "Conf",
      hypothesis_support AS "Hypotheses", promotion_state AS "State"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry" AND promotion_state = "crystallized"
SORT confidence_level DESC
LIMIT 10
```

*These have `promotion_state: crystallized` — membot will distill them to HONEY.md at next session end.*

---

## 📊 By Hypothesis

### H1 — Insider
```dataview
TABLE date_found AS "Found", confidence_level AS "Conf", confidence_delta AS "Δ",
      sprint_id AS "Sprint", pipeline_run AS "Run", promotion_state AS "State"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry" AND contains(hypothesis_support, "H1")
SORT date_found DESC
```

### H2 — Pipeline
```dataview
TABLE date_found AS "Found", confidence_level AS "Conf", confidence_delta AS "Δ",
      sprint_id AS "Sprint", pipeline_run AS "Run", promotion_state AS "State"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry" AND contains(hypothesis_support, "H2")
SORT date_found DESC
```

### H3 — Breach
```dataview
TABLE date_found AS "Found", confidence_level AS "Conf", confidence_delta AS "Δ",
      sprint_id AS "Sprint", pipeline_run AS "Run", promotion_state AS "State"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry" AND contains(hypothesis_support, "H3")
SORT date_found DESC
```

### H4 — Handoff
```dataview
TABLE date_found AS "Found", confidence_level AS "Conf", confidence_delta AS "Δ",
      sprint_id AS "Sprint", pipeline_run AS "Run", promotion_state AS "State"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry" AND contains(hypothesis_support, "H4")
SORT date_found DESC
```

### H5 — Payoff
```dataview
TABLE date_found AS "Found", confidence_level AS "Conf", confidence_delta AS "Δ",
      sprint_id AS "Sprint", pipeline_run AS "Run", promotion_state AS "State"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry" AND contains(hypothesis_support, "H5")
SORT date_found DESC
```

---

## 📅 All Findings — Chronological

```dataview
TABLE date_found AS "Found", sprint_id AS "Sprint", pipeline_run AS "Run",
      confidence_level AS "Conf", confidence_delta AS "Δ",
      hypothesis_support AS "Hypotheses", category AS "Type",
      source_agent AS "Agent", promotion_state AS "State"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry"
SORT date_found DESC
```

---

## 🔗 Connections (cross-entity links)

```dataview
TABLE date_found AS "Found", sprint_id AS "Sprint",
      hypothesis_support AS "Hypotheses", confidence_level AS "Conf"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry" AND category = "connection"
SORT confidence_level DESC
```

---

## 📈 Confidence Movers (high delta)

```dataview
TABLE date_found AS "Found", sprint_id AS "Sprint",
      hypothesis_support AS "Hypotheses", confidence_delta AS "Δ",
      confidence_level AS "New Conf"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry" AND confidence_delta > 0.05
SORT confidence_delta DESC
LIMIT 10
```

---

## 🔧 Promotion Pipeline

```dataview
TABLE WITHOUT ID
  rows.promotion_state AS "State",
  length(rows) AS "Count"
FROM "00-SHARED" OR "30-Evidence"
WHERE type = "nectar-entry"
GROUP BY promotion_state
SORT rows.promotion_state ASC
```

> **Promote workflow:**
> 1. Open finding note
> 2. Write your annotation in `## Your Annotations`
> 3. Set `promotion_state: crystallized` in frontmatter
> 4. Run `Ctrl+Alt+C` to sign (optional but recommended)
> 5. Membot picks up at next `/faerie --crystallize` or `/handoff`
