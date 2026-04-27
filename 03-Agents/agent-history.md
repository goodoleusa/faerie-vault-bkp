---
type: system-design
status: active
created: 2026-03-27
updated: 2026-03-27
tags: [agents, evolution, meta, system-design]
parent:
  - "[[HOME]]"
sibling: []
child: []
memory_lane: inbox
promotion_state: capture
chain_id: ""
agent_hash: ""
ann_hash: ""
ann_ts: ""
doc_hash: sha256:339d2803e13aab4d4e63fa33eeada20dfba578bfb87fa396e8ec64c264aa5538
hash_ts: 2026-03-29T16:10:51Z
hash_method: body-sha256-v1
---

# Agent Evolution Dashboard

*Tracks how the agent roster evolved through autolearn, deployment, and investigation needs.*

---

## Current Roster (Live)

```dataview
TABLE WITHOUT ID
  file.link AS "Agent",
  file.mtime AS "Last Modified"
FROM "03-Agents/evolution"
WHERE file.name != "agent-history"
SORT file.name ASC
```

## Training Events (Recent)

```dataview
TABLE WITHOUT ID
  file.link AS "Brief",
  agent_author AS "Agent",
  ts AS "When",
  brief_type AS "Type"
FROM "00-SHARED/Session-Briefs"
WHERE type = "brief" AND contains(tags, "training")
SORT ts DESC
LIMIT 10
```

---

## Evolution Map

| Category | Count | Detail |
|----------|-------|--------|
| Survivors (original + still active) | 16 | Core investigation team |
| Retired (merged/removed) | 25 | Consolidated into specialists |
| Born new (post-evolution) | 7 | Emerged from investigation needs |

### Active Agents (16 survivors + 7 new = 23)

**Survivors**: context-manager, data-engineer, data-scientist, error-coordinator, evidence-curator, fullstack-developer, knowledge-synthesizer, memory-keeper, python-pro, research-analyst, security-auditor, task-distributor, team-builder, token-optimizer, vision-ingest, workflow-orchestrator

**Born new**: admin-sync, coc-manager, evidence-analyst, ipfs-publisher, membot, performance-eval, report-writer

### Retired (25)

Snapshots in `03-Agents/evolution/`. Key absorptions:
- statistical-analysis-subagent → data-scientist (2026-03-12)
- ml-engineer, machine-learning-engineer → data-scientist
- code-reviewer → security-auditor
- prompt-engineer → context-manager
- documentation-engineer → report-writer (new)

---

## Your Annotations

<!-- Evolution observations, training decisions, roster changes -->

