---
type: blueprint
blueprint_id: blueprint_dashboard
name: Dashboard
version: "1.1"
created: 2026-03-29
updated: 2026-03-29
status: active
---

# Blueprint: Dashboard

Live Dataview-powered status views. Agent-written markdown that Obsidian renders as
interactive dashboards. Combines static agent-written summaries with dynamic Dataview
queries for real-time queue and metric panels.

## Metadata

| Field | Value |
|-------|-------|
| ID | blueprint_dashboard |
| Output dir | 00-SHARED/Dashboards/ |
| Agent types | fullstack-developer, admin-sync, token-optimizer, multi-agent-coordinator |
| Promotion target | None — live views, not promoted |
| Human annotation | Humans may edit directly (exception to one-writer rule for dashboards) |

## Required Frontmatter

```yaml
---
type: dashboard
blueprint: blueprint_dashboard
agent_type: {agent_type}
session_id: {session_id}
title: "{descriptive title}"
status: live | archived
generated: YYYY-MM-DD
updated: YYYY-MM-DD
doc_hash: sha256:pending
---
```

## Optional Frontmatter

```yaml
tags: [dashboard]
refresh_cadence: per-session | on-demand | manual
dataview_queries: true
cssclasses: [wide-page, dashboard-home]
```

## Required Sections

### Status
Current state of whatever this dashboard monitors. Agent writes static snapshot here.
One table or 3-5 bullet points. Updated each session by the owning agent type.

### Queue / Active
What is in flight or pending. May be Dataview (dynamic) or agent-written table (static).

## DataviewJS Patterns

### Task queue by priority
```dataviewjs
dv.table(
  ["Task", "Priority", "Status", "Age"],
  dv.pages('"00-SHARED/Queue"')
    .where(p => p.status !== "completed" && p.status !== "archived")
    .sort(p => p.priority, "desc")
    .map(p => [p.file.link, p.priority, p.status,
               Math.floor((Date.now() - p.file.ctime) / 86400000) + "d"])
)
```

### Session metrics rolling window
```dataviewjs
const sessions = dv.pages('"00-SHARED/Dashboards/session-briefs"')
  .where(p => p.type === "session-manifest")
  .sort(p => p.date, "desc")
  .limit(10);
dv.table(
  ["Session", "Date", "Agents", "Findings", "Queue Added"],
  sessions.map(s => [s.file.link, s.date, s.agents_spawned,
                     s.findings_produced, s.queue_items_added])
)
```

### Agent evolution leaderboard
```dataviewjs
dv.table(
  ["Agent", "Score", "Deployment", "Tier"],
  dv.pages('"00-SHARED/Agent-Outbox/agent-evolution"')
    .where(p => p.type === "agent-evolution")
    .sort(p => p.latest_deployment_score || p.latest_score, "desc")
    .map(p => [p.file.link, p.latest_score, p.latest_deployment_score, p.tier])
)
```

## Structure Rules

- `updated` field must be set each time an agent writes (not left stale)
- `agent_type` reflects last agent to update (not the creator)
- Static sections: agent-written tables or bullet lists (updated per session)
- Dynamic sections: Dataview/DataviewJS queries (render live in Obsidian)
- No case data in frontmatter fields
- dashboards use cssclasses `wide-page` for readability in Obsidian

## Validation Rules

- `updated` field must be set and not empty
- Sections Status and Queue / Active must be present
- No case data in frontmatter fields
- `status: archived` when dashboard is superseded (do not delete)

## Example Output

See `00-SHARED/Agent-Outbox/dashboards/example-dashboard.md`
