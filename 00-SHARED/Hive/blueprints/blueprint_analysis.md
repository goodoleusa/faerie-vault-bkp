---
type: blueprint
blueprint_id: blueprint_analysis
name: Analysis Report
version: "1.0"
created: 2026-03-29
status: active
---

# Blueprint: Analysis Report

Statistical or analytical work products. Quantitative reasoning with methodology disclosed. Anti-p-hacking rules enforced.

## Metadata

| Field | Value |
|-------|-------|
| ID | blueprint_analysis |
| Output dir | 00-SHARED/Agent-Outbox/analysis/ |
| Agent types | data-scientist, data-analyst, statistical-analysis-subagent |
| Promotion target | Human review only (not promoted to 30-Evidence directly) |
| Human annotation | .ann.md sibling |

## Required Frontmatter

```yaml
---
type: analysis
blueprint: blueprint_analysis
agent_type: {agent_type}
session_id: {session_id}
title: {descriptive title}
status: draft | final
generated: YYYY-MM-DD
promotion_state: raw
doc_hash: sha256:pending
method: {named statistical method — required, not empty}
---
```

## Optional Frontmatter

```yaml
tags: []
confidence_level: 0.0-1.0
hypothesis_support: []
source_files: []
pipeline_run: ""
p_value: null
sample_size: null
updated: YYYY-MM-DD
```

## Required Sections

### Methodology
What statistical or analytical approach was used. Enough detail to replicate.

### Results
The findings. Tables, charts (as mermaid or links), key numbers.

### Limitations
What this analysis cannot tell us. Potential confounds. Data quality issues.

### Implications
What these results mean for the investigation. Which hypotheses are supported or challenged.

## Structure Rules

- method field must be named (not "I ran some analysis")
- p-values reported with sample size (anti-p-hacking)
- Confidence intervals preferred over point estimates
- All source files listed in frontmatter source_files array
- Charts embedded as Mermaid or linked from Agent-Outbox/viz/

## Validation Rules

- method field must not be empty
- sections Methodology, Results, Limitations, Implications must be present
- No case data in frontmatter fields
