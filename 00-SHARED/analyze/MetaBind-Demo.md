---
type: dashboard
status: active
created: 2026-05-17
tags: [dashboard, demo, meta-bind]
intent_mode: analyze
---

> [← 00-SHARED/analyze](00-SHARED/analyze.md)

# MetaBind Dashboard Examples

Reference for using MetaBind with dataview dashboards.

---

## Intent Mode Selector

```
INPUT[toggle:intent_mode|learn-explore|📚 Explore]
INPUT[toggle:intent_mode|analyze|🔬 Analyze]
INPUT[toggle:intent_mode|review|✏️ Review]
INPUT[toggle:intent_mode|finalize|🎯 Finalize]
```

**Renders as:** Clickable toggles for each intent mode

---

## Status Buttons

```
INPUT[choice:status|active|Active] 
INPUT[choice:status|archived|Archived]
INPUT[choice:status|superseded|Superseded]
```

**Renders as:** Radio-style buttons

---

## Quick Actions

```
BUTTON[go to learn-explore]
BUTTON[go to analyze]
BUTTON[go to review] 
BUTTON[go to finalize]
```

**Note:** Replace with actual page links

---

## Search Query Input

```
INPUT[text:search_query|Search vault...]
```

---

## Dataview + MetaBind Combo

```dataview
TABLE WITHOUT ID
  choice AS "Update Status",
  status AS "Current"
FROM "00-SHARED"
WHERE type = "index"
SORT file.name
```

Use INPUT in dataview output cells for inline editing.

---

## More Examples

See: [[COMPASS-FRONTMATTER-TEMPLATE]] for frontmatter field specs