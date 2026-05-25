---
type: dashboard
status: active
tags: [dashboard, queue, live, dataview]
parent: "[[00-SHARED/Dashboards/INDEX]]"
up: "[[INDEX]]"
created: 2026-04-25
updated: 2026-04-25
doc_hash: sha256:1cf4126029780237fc75499a8654d776bede412614857afda79e98d90e8d1228
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

> [up Parent](./INDEX.md) · [home Vault Index](../INDEX.md)

# Queue State — Live Dashboard

Data sourced from `_queue-index/` sidecar files (sprint-queue.json mirrored by `9x_queue_to_vault_index.py`). Refresh cadence: on every queue mutation (sidecar script wired to queue write hook). To force refresh: run `python3 /mnt/d/0local/gitrepos/faerie2/scripts/9x_queue_to_vault_index.py` from WSL.

---

## Flags — Blocked or Overdue Tasks

```dataviewjs
const tasks = dv.pages('"00-SHARED/Dashboards/_queue-index"')
  .where(p => p.queue_status === "blocked" || p.queue_status === "stalled");
if (tasks.length === 0) {
  dv.paragraph("No blocked or stalled tasks.");
} else {
  dv.table(
    ["Task ID", "Title", "Status", "Blocked By", "Priority"],
    tasks.sort(p => p.priority || "LOW", "asc").map(p => [
      p.task_id || "—",
      p.title || "—",
      p.queue_status || "—",
      p.blocked_by || "none",
      p.priority || "—"
    ])
  );
}
```

---

## Friction — Queue Depth by Priority

```dataviewjs
const tasks = dv.pages('"00-SHARED/Dashboards/_queue-index"')
  .where(p => p.queue_status === "pending" || p.queue_status === "queued");
const byPriority = { HIGH: 0, MED: 0, LOW: 0 };
for (const t of tasks) {
  const pri = (t.priority || "LOW").toUpperCase();
  if (byPriority[pri] !== undefined) byPriority[pri]++;
}
dv.paragraph(
  `Pending: **${tasks.length}** total — HIGH: ${byPriority.HIGH} | MED: ${byPriority.MED} | LOW: ${byPriority.LOW}`
);
```

---

## Flow — In Progress + Recently Completed

```dataviewjs
const inProgress = dv.pages('"00-SHARED/Dashboards/_queue-index"')
  .where(p => p.queue_status === "in_progress" || p.queue_status === "claimed");

dv.header(3, "In Progress");
if (inProgress.length === 0) {
  dv.paragraph("No tasks currently in progress.");
} else {
  dv.table(
    ["Task ID", "Title", "Agent", "Claimed At"],
    inProgress.map(p => [
      p.task_id || "—",
      p.title || "—",
      p.claimed_by || "unknown",
      p.claimed_at || "—"
    ])
  );
}

const cutoff = Date.now() - 86400000;
const recent = dv.pages('"00-SHARED/Dashboards/_queue-index"')
  .where(p => p.queue_status === "completed" && p.completed_at && new Date(p.completed_at).getTime() > cutoff)
  .sort(p => p.completed_at, "desc")
  .limit(10);

dv.header(3, "Completed (last 24h)");
if (recent.length === 0) {
  dv.paragraph("No completions in the last 24 hours.");
} else {
  dv.table(
    ["Task ID", "Title", "Completed At"],
    recent.map(p => [p.task_id || "—", p.title || "—", p.completed_at || "—"])
  );
}
```

---

## Focus — Full Pending Queue

```dataview
TABLE WITHOUT ID
  task_id as "Task ID",
  title as Title,
  priority as Priority,
  queue_status as Status,
  blocked_by as "Blocked By"
FROM "00-SHARED/Dashboards/_queue-index"
WHERE queue_status = "pending" OR queue_status = "queued"
SORT priority ASC, added_at DESC
```

---

*Live dashboard — data from `_queue-index/` sidecars | Sidecar script: `scripts/9x_queue_to_vault_index.py` | Hook: queue write PostToolUse*
