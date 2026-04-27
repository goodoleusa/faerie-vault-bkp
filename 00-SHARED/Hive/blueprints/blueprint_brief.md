---
type: blueprint
blueprint_id: blueprint_brief
name: Session Brief
version: "1.0"
created: 2026-03-29
status: active
---

# Blueprint: Session Brief

Session summary atoms written by agents at session end. Consumed by faerie at next startup and by dashboards.

## Metadata

| Field | Value |
|-------|-------|
| ID | blueprint_brief |
| Output dir | 00-SHARED/Session-Briefs/ |
| Agent types | memory-keeper, context-manager, knowledge-synthesizer |
| Promotion target | Dashboards/session-manifests/ (auto) |
| Human annotation | Not expected — machine-consumed |

## Required Frontmatter

```yaml
---
type: brief
blueprint: blueprint_brief
brief_type: session-summary | stage-summary | finding-promotion | hypothesis-update | blocker-flag
agent_type: {agent_type}
session_id: {session_id}
generated: YYYY-MM-DDTHH:MM:SSZ
status: final
promotion_state: raw
doc_hash: sha256:pending
schema_version: "1.0"
---
```

## Optional Frontmatter

```yaml
sprint_id: ""
phase: SEED | DEEPEN | EXTEND | FULL | ad-hoc
pipeline_stage: ""
hypothesis_touched: []
confidence_delta: {}
blockers: []
review_status: unreviewed | endorsed | promoted
```

## Required Sections

### Done This Session
Bulleted list. What was completed. Be specific (file paths, task IDs).

### Key Findings
What the session produced that's worth knowing. Link to finding files if created.

### Open Threads
What was started but not finished. Queue items generated.

### Next Session Hint
One sentence for faerie: what to pick up first next time.

## Structure Rules

- generated uses ISO8601 with timezone (Z suffix)
- hypothesis_touched uses canonical IDs (H1, H2, etc.)
- blockers formatted as `[BLOCKER] Description — what it blocks`
- Body terse — machine-consumed
- File paths in body use vault-relative form

## Validation Rules

- generated must be valid ISO8601 with timezone
- sections Done This Session, Key Findings, Open Threads, Next Session Hint must be present
- No case data in frontmatter fields
