---
type: blueprint
blueprint_id: blueprint_report
name: Report
version: "1.0"
created: 2026-03-29
status: active
---

# Blueprint: Report

Formal written reports for human consumption. Long-form synthesis with executive summary, methodology, and conclusions.

## Metadata

| Field | Value |
|-------|-------|
| ID | blueprint_report |
| Output dir | 00-SHARED/Agent-Outbox/reports/ |
| Agent types | report-writer, research-analyst, knowledge-synthesizer, documentation-engineer |
| Promotion target | Human review; may surface to Human-Inbox/ |
| Human annotation | .ann.md sibling |

## Required Frontmatter

```yaml
---
type: report
blueprint: blueprint_report
agent_type: {agent_type}
session_id: {session_id}
title: {descriptive title}
status: draft | final
generated: YYYY-MM-DD
promotion_state: raw
doc_hash: sha256:pending
---
```

## Optional Frontmatter

```yaml
tags: []
priority: HIGH | MED | LOW
confidence_level: 0.0-1.0
hypothesis_support: []
sources: []
updated: YYYY-MM-DD
classification: internal | draft | review-ready
```

## Required Sections

### Executive Summary
3-5 bullets. What the reader needs to know before diving in.

### Background
Context needed to understand the report. Brief.

### Findings
The substance. May use sub-headers. Links to source finding files.

### Conclusions
What the findings mean collectively. Confidence assessment.

### Recommendations
What to do next. Prioritized.

## Structure Rules

- Executive Summary is always first body section
- Findings section may nest H3 sub-sections
- Source links use vault-relative paths
- No raw data pasted in-line — link to evidence files instead
- Conclusions must state confidence level explicitly

## Validation Rules

- sections Executive Summary, Background, Findings, Conclusions, Recommendations must be present
- No case data in frontmatter fields
- Links use relative vault paths
