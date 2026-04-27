---
type: blueprint
blueprint_id: blueprint_evidence
name: Evidence Item
version: "1.0"
created: 2026-03-29
status: active
---

# Blueprint: Evidence Item

Structured evidence extracts from raw data processing. Primary deliverables of data-engineer and evidence-curator agents.

## Metadata

| Field | Value |
|-------|-------|
| ID | blueprint_evidence |
| Output dir | 00-SHARED/Agent-Outbox/evidence/ |
| Agent types | evidence-analyst, data-engineer, evidence-curator |
| Promotion target | 30-Evidence/ |
| Human annotation | .ann.md sibling |

## Required Frontmatter

```yaml
---
type: evidence
blueprint: blueprint_evidence
agent_type: {agent_type}
session_id: {session_id}
title: {descriptive title}
status: raw | processed | verified
generated: YYYY-MM-DD
promotion_state: raw
doc_hash: sha256:pending
source_file: {relative path: scripts/audit_results/FILENAME.json}
source_sha256: {sha256 of source file — required}
---
```

## Optional Frontmatter

```yaml
evidence_id: ""
tags: []
source_type: agent-research | tabular | mhtml | pdf | json | vision | osint
confidence_level: 0.0-1.0
hypothesis_support: []
evidence_tier: 1 | 2 | 3 | 4
pipeline_run: ""
git_commit: ""
coc_ref: ""
```

## Required Sections

### Extract
The raw extracted data or summary. May include tables, code blocks, or structured lists.

### Provenance
Where this came from. Source file path, run ID, method used to extract.

### Significance
Why this matters. What hypothesis this bears on. Confidence level reasoning.

## Structure Rules

- source_sha256 must be populated (not pending) before agent returns
- Use `sha256sum {source_file}` to populate
- Source paths use `scripts/audit_results/` relative form
- hypothesis_support array uses canonical IDs (H1, H2, etc.)
- No entity names or case-identifying data in frontmatter fields

## Validation Rules

- source_sha256 must not be empty or "pending"
- sections Extract, Provenance, Significance must be present
- No case data in frontmatter fields
