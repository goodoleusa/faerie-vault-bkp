---
type: dashboard
status: active
tags: [dashboard, phase, progress, live, dataview]
parent: "[[00-SHARED/Dashboards/INDEX]]"
up: "[[INDEX]]"
created: 2026-04-25
updated: 2026-04-25
doc_hash: sha256:7d6c9c5db45bc9cdc0d294813ee9aeedd7d8f0dd879deb754909f0b266f7bf05
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

> [up Parent](./INDEX.md) · [home Vault Index](../INDEX.md)

# Phase Progress — Live Dashboard

Data sourced from `_phase-index/` sidecar files (forensics/phases/ mirrored by `9x_manifests_to_vault_index.py --mode phases`). Tracks sprint phases, milestones, and task completion toward next gate.

---

## Flags — Gates at Risk

```dataviewjs
const phases = dv.pages('"00-SHARED/Dashboards/_phase-index"')
  .where(p => p.phase_status === "at-risk" || p.phase_status === "blocked");
if (phases.length === 0) {
  dv.paragraph("No phases at risk.");
} else {
  dv.table(
    ["Phase", "Gate", "Status", "Blocker"],
    phases.map(p => [
      p.phase_name || "—",
      p.gate || "—",
      p.phase_status || "—",
      p.blocker || "none"
    ])
  );
}
```

---

## Friction — Incomplete Tasks by Phase

```dataviewjs
const phases = dv.pages('"00-SHARED/Dashboards/_phase-index"')
  .where(p => p.phase_status === "in-progress");
if (phases.length === 0) {
  dv.paragraph("No active phases.");
} else {
  for (const phase of phases) {
    const total = phase.task_count || 0;
    const done = phase.tasks_done || 0;
    const pct = total > 0 ? Math.round((done / total) * 100) : 0;
    const bar = "█".repeat(Math.floor(pct / 10)) + "░".repeat(10 - Math.floor(pct / 10));
    dv.paragraph(`**${phase.phase_name}** [${bar}] ${pct}% (${done}/${total} tasks)`);
  }
}
```

---

## Flow — Completed Phases

```dataview
TABLE WITHOUT ID
  phase_name as Phase,
  gate as Gate,
  completed_at as "Completed",
  task_count as "Tasks",
  outcome as Outcome
FROM "00-SHARED/Dashboards/_phase-index"
WHERE phase_status = "completed"
SORT completed_at DESC
```

---

## Focus — Active Phase Detail

```dataviewjs
const active = dv.pages('"00-SHARED/Dashboards/_phase-index"')
  .where(p => p.phase_status === "in-progress")
  .sort(p => p.phase_order || 99, "asc")
  .first();
if (!active) {
  dv.paragraph("No active phase found.");
} else {
  dv.header(3, active.phase_name || "Active Phase");
  dv.paragraph(`**Gate:** ${active.gate || "—"} | **Sprint:** ${active.sprint || "—"}`);
  dv.paragraph(`**Started:** ${active.started_at || "—"} | **Target:** ${active.target_date || "—"}`);
  if (active.open_threads) {
    dv.header(4, "Open Threads");
    const threads = Array.isArray(active.open_threads) ? active.open_threads : [active.open_threads];
    dv.list(threads);
  }
}
```

---

*Live dashboard — data from `_phase-index/` sidecars | Sidecar script: `scripts/9x_manifests_to_vault_index.py --mode phases` | Updated at session boundaries*
