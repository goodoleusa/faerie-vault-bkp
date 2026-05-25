---
type: dashboard
status: active
tags: [dashboard, stigmergy, autonomy, live, dataview]
parent: "[[00-SHARED/Dashboards/INDEX]]"
up: "[[INDEX]]"
created: 2026-04-25
updated: 2026-04-25
doc_hash: sha256:542224573d34c08760401284f7682b2fe015c2b5fbf0c0cdc30113d5f6ace812
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

> [up Parent](./INDEX.md) · [home Vault Index](../INDEX.md)

# Stigmergy State — Live Dashboard

Tracks autonomy %, hash chains, droplet flow, and emergence signals. Reflects the health of the self-organizing layer — how well agents coordinate through the filesystem without main-session intervention.

Data sourced from `_manifest-index/` (manifest sidecars) and `_droplets-index/` (droplet sidecars).

---

## Flags — Chain Gaps and Missing Manifests

```dataviewjs
// Manifests without builds_on_refs (missing stigmergic chain links)
const manifests = dv.pages('"00-SHARED/Dashboards/_manifest-index"')
  .where(p => p.status === "final" && p.ts);
const chainless = manifests.where(p => !p.builds_on_refs || p.builds_on_refs === "[]");
const total = manifests.length;
const gap_pct = total > 0 ? Math.round((chainless.length / total) * 100) : 0;

dv.paragraph(`**Chain coverage:** ${100 - gap_pct}% of final manifests have \`builds_on_refs\` (${total - chainless.length}/${total})`);

if (chainless.length > 0 && gap_pct > 20) {
  dv.header(4, "Chainless Manifests (sample — flagging gap >20%)");
  dv.table(
    ["Agent", "Task", "Time"],
    chainless.sort(p => p.ts, "desc").limit(10).map(p => [
      p.agent_type || "unknown",
      p.task_id || "—",
      p.ts ? p.ts.toString().slice(0, 16) : "—"
    ])
  );
}
```

---

## Friction — Low Stigmergy Adoption by Agent Type

```dataviewjs
const manifests = dv.pages('"00-SHARED/Dashboards/_manifest-index"')
  .where(p => p.status === "final");
const byAgent = {};
for (const p of manifests) {
  const agent = p.agent_type || "unknown";
  if (!byAgent[agent]) byAgent[agent] = { total: 0, has_refs: 0, has_droplets: 0 };
  byAgent[agent].total++;
  if (p.builds_on_refs && p.builds_on_refs !== "[]") byAgent[agent].has_refs++;
  if (p.droplets && p.droplets !== "[]") byAgent[agent].has_droplets++;
}
const friction = Object.entries(byAgent)
  .filter(([_, s]) => s.total >= 3)
  .map(([agent, s]) => ({
    agent,
    total: s.total,
    ref_rate: Math.round((s.has_refs / s.total) * 100),
    droplet_rate: Math.round((s.has_droplets / s.total) * 100)
  }))
  .filter(r => r.ref_rate < 60 || r.droplet_rate < 60)
  .sort((a, b) => a.ref_rate - b.ref_rate);

if (friction.length === 0) {
  dv.paragraph("No friction. All agent types with 3+ runs showing ≥60% stigmergy adoption.");
} else {
  dv.table(
    ["Agent", "Runs", "Chain Refs %", "Droplets %"],
    friction.map(r => [r.agent, r.total, r.ref_rate + "%", r.droplet_rate + "%"])
  );
}
```

---

## Flow — Autonomy and Droplet Emergence

```dataviewjs
// Autonomy %: final manifests with both builds_on_refs + droplets / all final manifests
const manifests = dv.pages('"00-SHARED/Dashboards/_manifest-index"')
  .where(p => p.status === "final" && p.ts);
const autonomous = manifests.where(p =>
  p.builds_on_refs && p.builds_on_refs !== "[]" &&
  p.droplets && p.droplets !== "[]"
);
const autonomy_pct = manifests.length > 0
  ? Math.round((autonomous.length / manifests.length) * 100)
  : 0;

dv.paragraph(`**Autonomy %:** ${autonomy_pct}% (${autonomous.length}/${manifests.length} final manifests are fully self-coordinating)`);

// Recent droplets
const droplets = dv.pages('"00-SHARED/Dashboards/_droplets-index"')
  .where(p => p.ts)
  .sort(p => p.ts, "desc")
  .limit(15);

if (droplets.length > 0) {
  dv.header(4, "Recent Droplets (cross-pollination signal)");
  dv.table(
    ["Time", "Agent", "Category", "Insight"],
    droplets.map(p => [
      p.ts ? p.ts.toString().slice(0, 16) : "—",
      p.agent_type || "unknown",
      p.category || "—",
      p.headline || p.summary || "—"
    ])
  );
}
```

---

## Focus — Emergence Narrative

```dataviewjs
// HIGH-priority droplets with CONNECTION or HEADLINE category — emergence signals
const emergence = dv.pages('"00-SHARED/Dashboards/_droplets-index"')
  .where(p => (p.category === "CONNECTION" || p.category === "HEADLINE") && p.priority === "HIGH")
  .sort(p => p.ts, "desc")
  .limit(10);

if (emergence.length === 0) {
  dv.paragraph("No HIGH-priority emergence signals in droplets index.");
} else {
  dv.header(4, "Emergence Signals (CONNECTION + HEADLINE, pri=HIGH)");
  for (const d of emergence) {
    dv.paragraph(`**[${d.category}]** ${d.headline || d.summary || "—"} — *${d.agent_type || "unknown"}*, ${d.ts ? d.ts.toString().slice(0, 10) : "—"}`);
  }
}
```

---

## Stigmergy Health Summary

```dataviewjs
const manifests = dv.pages('"00-SHARED/Dashboards/_manifest-index"').where(p => p.ts);
const final = manifests.where(p => p.status === "final");
const in_progress = manifests.where(p => p.status === "in-progress");
const stalled = manifests.where(p => p.status !== "final" && p.status !== "in-progress");
const droplets = dv.pages('"00-SHARED/Dashboards/_droplets-index"').where(p => p.ts);

dv.paragraph(
  `Manifests: ${final.length} final | ${in_progress.length} in-progress | ${stalled.length} stalled\n` +
  `Droplets indexed: ${droplets.length} | ` +
  `Chain coverage: see Flags section above`
);
```

---

*Live dashboard — data from `_manifest-index/` + `_droplets-index/` sidecars | Sidecar script: `scripts/9x_manifests_to_vault_index.py` | Hook: SubagentStop*
