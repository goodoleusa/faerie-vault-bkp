---
type: system-design
status: active
created: 2026-03-27
updated: 2026-03-27
tags: [agents, performance, dashboard, FFFF]
parent:
  - "[[HOME]]"
  - "[[agent-history]]"
sibling: []
child: []
memory_lane: inbox
promotion_state: capture
chain_id: ""
agent_hash: ""
ann_hash: ""
ann_ts: ""
doc_hash: sha256:1d833bdeb76f550efa8cd702b092510a1b89376329c7d81bd63aeef967ef20b8
hash_ts: 2026-03-29T16:10:51Z
hash_method: body-sha256-v1
---

# Agent Performance Dashboard

*FINDINGS FLAGS FRICTION FLOW at every zoom level.*
*Sync: `python3 scripts/vault_agent_evolution_sync.py` (run at session end or on-demand)*

---

## ZOOM OUT: Team Overview

### FINDINGS — What the team discovered

```dataview
TABLE WITHOUT ID
  agent_author AS "Agent",
  count(rows) AS "Briefs",
  min(rows.confidence_delta) AS "Min Delta",
  max(rows.confidence_delta) AS "Max Delta"
FROM "00-SHARED/Session-Briefs"
WHERE type = "brief"
GROUP BY agent_author
SORT count(rows) DESC
```

### FLAGS — Blockers and warnings raised

```dataview
TABLE WITHOUT ID
  file.link AS "Flag",
  agent_author AS "Agent",
  blockers AS "Blocker",
  created AS "When"
FROM "00-SHARED/Session-Briefs"
WHERE type = "brief" AND length(blockers) > 0
SORT created DESC
LIMIT 10
```

### FRICTION — Where agents struggled

```dataview
TABLE WITHOUT ID
  agent_name AS "Agent",
  training_type AS "Type",
  score_delta AS "Delta",
  created AS "When"
FROM "03-Agents/training-events"
WHERE score_delta < 0
SORT created DESC
LIMIT 10
```

### FLOW — What went smoothly

```dataview
TABLE WITHOUT ID
  agent_name AS "Agent",
  training_type AS "Type",
  new_score AS "Score",
  score_delta AS "Delta"
FROM "03-Agents/training-events"
WHERE score_delta > 0
SORT score_delta DESC
LIMIT 10
```

---

## ZOOM MID: Sprint / Pipeline Phase

### Current Sprint Performance

```dataview
TABLE WITHOUT ID
  agent_name AS "Agent",
  current_score AS "Score",
  deployment_score AS "Deploy",
  score_delta AS "Delta"
FROM "03-Agents/snapshots"
WHERE type = "agent-snapshot"
SORT current_score DESC
```

### Pipeline Phase Heatmap

| Phase | Strong Agents | Weak Agents | Notes |
|-------|--------------|-------------|-------|
| SEED | data-engineer, evidence-analyst | | Ingest + baseline |
| DEEPEN | data-scientist, research-analyst | | Statistical analysis |
| EXTEND | security-auditor, evidence-curator | | Verification + curation |
| FULL | report-writer, fullstack-developer | | Publication |

### Session-Level: Recent Spawns

```dataview
TABLE WITHOUT ID
  file.link AS "Event",
  agent_name AS "Agent",
  training_type AS "Type",
  new_score AS "Score",
  created AS "Date"
FROM "03-Agents/training-events"
SORT created DESC
LIMIT 15
```

---

## ZOOM IN: Individual Agent Drill-Down

> Click any agent snapshot below to see their full history, spawn log, score trends, and techniques learned.

```dataview
TABLE WITHOUT ID
  file.link AS "Agent",
  current_score AS "Training",
  deployment_score AS "Deployment",
  score_delta AS "Delta",
  score_context AS "Context"
FROM "03-Agents/snapshots"
WHERE type = "agent-snapshot"
SORT current_score DESC
```

### Agent Score Chart

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#93C572',
  'primaryTextColor': '#1a1a2e',
  'primaryBorderColor': '#D4A843',
  'lineColor': '#4ECDC4',
  'secondaryColor': '#4ECDC4',
  'tertiaryColor': '#2d2d44',
  'background': '#1a1a2e',
  'fontFamily': 'Inter, system-ui'
}}}%%
xychart-beta
    title "Agent Scores (Training vs Deployment)"
    x-axis ["data-sci", "evidence-cur", "data-eng", "research-an", "security-aud", "memory-kpr", "python-pro", "fullstack"]
    y-axis "Score" 0 --> 1.0
    bar [0.95, 0.91, 0.90, 0.88, 0.85, 0.82, 0.80, 0.78]
    line [0.92, 0.88, 0.87, 0.85, 0.82, 0.80, 0.78, 0.75]
```

*Bar = training score, Line = deployment score. Update manually or via sync script.*

---

## ZOOM MICRO: Technique Library

```dataview
TABLE WITHOUT ID
  file.link AS "Technique",
  agent_name AS "Agent",
  created AS "Learned"
FROM "03-Agents/training-events"
WHERE contains(tags, "technique")
SORT created DESC
LIMIT 20
```

---

## Evolution Timeline

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#93C572',
  'primaryBorderColor': '#D4A843',
  'lineColor': '#4ECDC4',
  'secondaryColor': '#4ECDC4',
  'tertiaryColor': '#2d2d44',
  'background': '#1a1a2e',
  'fontFamily': 'Inter, system-ui',
  'textColor': '#e8e8e8',
  'cScale0': '#93C572',
  'cScale1': '#4ECDC4',
  'cScale2': '#D4A843',
  'cScale3': '#2d2d44'
}}}%%
timeline
    title Agent Roster Evolution
    section Original (41 agents)
        Initial deployment : 41 agents from template
        First consolidation : Merged duplicates (ml-engineer, data-analyst)
    section Pruning (25 retired)
        statistical-analysis-subagent absorbed : 2026-03-12
        Generic roles retired : ai-engineer, llm-architect, nlp-engineer
        Specialized survivors : 16 core agents
    section Growth (7 born)
        membot created : Memory crystallization
        evidence-analyst : Dataset profiling
        coc-manager : Chain of custody
        performance-eval : Autolearn scoring
        report-writer : Narrative generation
    section Current (23 active)
        Autolearn active : OTJ learning every run
        Deployment scoring : Real-work measurements
```

---

## Your Annotations

<!-- Which agents need attention? Retraining? Retirement? -->
<!-- What friction patterns keep recurring? -->

