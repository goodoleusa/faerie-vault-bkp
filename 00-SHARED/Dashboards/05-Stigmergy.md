---
type: dashboard
tier: stigmergy
title: "Stigmergy — discovered_work flow & cross-citation"
status: live
derived_from:
  - "CyberOps-UNIFIED/00-SHARED/Hive/05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK.md"
  - "CyberOps-UNIFIED/00-SHARED/ONBOARDING/CyberTemplate-Investigation/FFFF-Dashboard.md"
tags: [dashboard, stigmergy, compass]
---

# Stigmergy

`discovered_work[]` flow visualization: which agents cited which, cross-citation rate,
bearing distribution N/S/E/W.

---

## Bearing distribution (last 7d)

```dataview
TABLE WITHOUT ID
  bearing AS "Bearing",
  length(rows) AS "discovered_work entries"
FROM "forensics/manifests"
WHERE date(file.mtime) >= date(today) - dur(7 days) AND bearing
GROUP BY bearing
SORT length(rows) DESC
```

## Cross-citations: from_label → to_label (last 7d)

```dataview
TABLE WITHOUT ID
  from_label AS "From",
  to_label AS "To",
  bearing AS "→",
  rationale AS "Why"
FROM "forensics/manifests"
WHERE date(file.mtime) >= date(today) - dur(7 days) AND from_label AND to_label
SORT file.mtime DESC
LIMIT 40
```

## Agents by discovery activity (who finds work for whom)

```dataview
TABLE WITHOUT ID
  agent_type AS "Agent",
  length(rows) AS "Discoveries authored"
FROM "forensics/manifests"
WHERE agent_type AND from_label
GROUP BY agent_type
SORT length(rows) DESC
LIMIT 20
```

## North-bound unblockers (N-edges, prerequisite liberation)

```dataview
LIST from_label + " → " + to_label + " (" + default(rationale, "—") + ")"
FROM "forensics/manifests"
WHERE bearing = "N"
SORT file.mtime DESC
LIMIT 15
```

## Dynamic compass mermaid (last 24h)

```dataviewjs
const pages = dv.pages('"forensics/manifests"')
  .where(p => p.from_label && p.to_label && p.bearing)
  .where(p => p.file.mtime >= dv.date('today').minus({hours: 24}));
const FILL = { N:'#D4A843', S:'#93C572', E:'#4ECDC4', W:'#9b59b6' };
let mmd = '```mermaid\ngraph LR\n';
const seen = new Set();
for (const p of pages) {
  const key = `${p.from_label}->${p.to_label}`;
  if (seen.has(key)) continue;
  seen.add(key);
  const color = FILL[p.bearing] || '#aaa';
  mmd += `  ${p.from_label}["${p.from_label}"] -->|${p.bearing}| ${p.to_label}["${p.to_label}"]\n`;
  mmd += `  style ${p.from_label} fill:${color},color:#1a1a2e\n`;
}
mmd += '```';
dv.paragraph(mmd);
```
