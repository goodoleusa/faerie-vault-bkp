---
type: dashboard
status: active
tags: [dashboard, eval, live, dataview]
parent: "[[00-SHARED/Dashboards/INDEX]]"
up: "[[INDEX]]"
created: 2026-04-25
updated: 2026-04-25
doc_hash: sha256:b24c3a305de6654782cfe8b4db7246e8afe5351ec2cd517c1491cce0d95179e0
hash_ts: 2026-04-25T01:10:52Z
hash_method: body-sha256-v1
---

> [up Parent](./INDEX.md) · [home Vault Index](../INDEX.md)

# Agent Eval — Live Dashboard

Data sourced from `_manifest-index/` sidecar files (JSON manifests converted by `9x_manifests_to_vault_index.py`). Refresh cadence: on every agent return (SubagentStop hook wires sidecar rebuild). To force refresh: run `python3 /mnt/d/0local/gitrepos/faerie2/scripts/9x_manifests_to_vault_index.py` from WSL.

---

## Flags — What Needs Attention Now

```dataviewjs
const cards = dv.pages('"00-SHARED/Dashboards/_manifest-index"')
  .where(p => p.status === "failed" || p.status === "stalled" || p.status === "in-progress");
if (cards.length === 0) {
  dv.paragraph("No flags. All recent manifests reached final status.");
} else {
  dv.table(
    ["Agent", "Task", "Status", "Time"],
    cards.sort(p => p.ts, "desc").limit(10).map(p => [
      p.agent_type || "unknown",
      p.task_id || "—",
      p.status || "—",
      p.ts || "—"
    ])
  );
}
```

---

## Friction — Where the System is Grinding

```dataviewjs
// Agents with repeated non-final status across recent runs
const all = dv.pages('"00-SHARED/Dashboards/_manifest-index"')
  .where(p => p.ts);
const byAgent = {};
for (const p of all) {
  const agent = p.agent_type || "unknown";
  if (!byAgent[agent]) byAgent[agent] = { total: 0, final: 0 };
  byAgent[agent].total++;
  if (p.status === "final") byAgent[agent].final++;
}
const friction = Object.entries(byAgent)
  .map(([agent, stats]) => ({
    agent,
    total: stats.total,
    final: stats.final,
    success_rate: stats.total > 0 ? Math.round((stats.final / stats.total) * 100) : 0
  }))
  .filter(r => r.total >= 2 && r.success_rate < 80)
  .sort((a, b) => a.success_rate - b.success_rate);
if (friction.length === 0) {
  dv.paragraph("No friction detected. All agents with 2+ runs at ≥80% success.");
} else {
  dv.table(
    ["Agent", "Total Runs", "Final", "Success %"],
    friction.map(r => [r.agent, r.total, r.final, r.success_rate + "%"])
  );
}
```

---

## Flow — What's Working

```dataviewjs
// Recent successful manifests (last 48h)
const cutoff = Date.now() - 86400000 * 2;
const recent = dv.pages('"00-SHARED/Dashboards/_manifest-index"')
  .where(p => p.status === "final" && p.ts && new Date(p.ts).getTime() > cutoff)
  .sort(p => p.ts, "desc")
  .limit(20);
if (recent.length === 0) {
  dv.paragraph("No final manifests in the last 48 hours.");
} else {
  dv.table(
    ["Time", "Agent", "Task", "Dashboard Line"],
    recent.map(p => [
      p.ts ? p.ts.toString().slice(0, 16) : "—",
      p.agent_type || "unknown",
      p.task_id || "—",
      p.dashboard_line || "—"
    ])
  );
}
```

---

## Focus — Agent Baseline Scores

```dataview
TABLE WITHOUT ID
  file.link as Agent,
  baseline_score as "Baseline",
  current_score as "Current",
  trend as Trend,
  last_run as "Last Run"
FROM "00-SHARED/Dashboards/_eval-cards"
WHERE type = "eval-card"
SORT current_score DESC
```

*Note: `_eval-cards/` is populated by `9x_manifests_to_vault_index.py --mode eval-cards`. If empty, run the sidecar script.*

---

## Recent Manifests — Full Index

```dataviewjs
const all = dv.pages('"00-SHARED/Dashboards/_manifest-index"')
  .where(p => p.ts)
  .sort(p => p.ts, "desc")
  .limit(50);
dv.table(
  ["Time", "Agent", "Task ID", "Status", "Dashboard Line"],
  all.map(p => [
    p.ts ? p.ts.toString().slice(0, 19) : "—",
    p.agent_type || "unknown",
    p.task_id || "—",
    p.status || "—",
    p.dashboard_line || "—"
  ])
);
```

---

*Live dashboard — data from `_manifest-index/` sidecars | Sidecar script: `scripts/9x_manifests_to_vault_index.py` | Hook: SubagentStop*
