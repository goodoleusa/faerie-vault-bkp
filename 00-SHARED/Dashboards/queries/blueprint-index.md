---
title: Blueprint Index — All Agent Outputs
type: query-dashboard
updated: 2026-03-29
---

# Blueprint Index

## All Agent Outputs by Type

```dataview
TABLE
  type AS "Type",
  status AS "Status",
  file.mtime AS "Modified",
  agent AS "Agent"
FROM "00-SHARED/Agent-Outbox"
WHERE type != null
SORT file.mtime DESC
LIMIT 50
```

## In-Progress Outputs

```dataview
TABLE
  type AS "Type",
  file.mtime AS "Modified",
  agent AS "Agent"
FROM "00-SHARED/Agent-Outbox"
WHERE status = "in-progress"
SORT file.mtime DESC
```

## High / Critical Findings

```dataview
TABLE
  file.link AS "Finding",
  priority AS "Priority",
  file.mtime AS "Date"
FROM "00-SHARED/Agent-Outbox"
WHERE (priority = "HIGH" OR priority = "CRITICAL") AND type = "finding"
SORT file.mtime DESC
```

## Recent Droplets

```dataview
TABLE
  file.link AS "Droplet",
  tags AS "Tags",
  file.mtime AS "Date"
FROM "00-SHARED/Agent-Outbox/droplets"
SORT file.mtime DESC
LIMIT 20
```

## Blueprint Templates Available

```dataview
TABLE
  file.name AS "Template",
  file.mtime AS "Last Modified"
FROM "00-SHARED/Hive/blueprints"
WHERE file.name != "_write_test"
SORT file.name ASC
```

## Session Manifests (last 10)

```dataview
TABLE
  session_id AS "Session",
  agent_count AS "Agents",
  file.mtime AS "Date"
FROM "00-SHARED/Agent-Outbox/session-briefs" OR "00-SHARED/Dashboards/session-briefs"
SORT file.mtime DESC
LIMIT 10
```
