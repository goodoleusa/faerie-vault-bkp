---
type: blueprint
blueprint_id: blueprint_finding
name: Finding
version: "1.0"
created: 2026-03-29
status: active
---

# Blueprint: Finding

Agent-produced findings destined for human review and potential promotion to 30-Evidence/.

## Metadata

| Field | Value |
|-------|-------|
| ID | blueprint_finding |
| Output dir | 00-SHARED/Agent-Outbox/findings/ |
| Agent types | evidence-analyst, data-scientist, research-analyst, security-auditor |
| Promotion target | 30-Evidence/ |
| Human annotation | .ann.md sibling |

## Required Frontmatter

```yaml
---
type: finding
blueprint: blueprint_finding
agent_type: {agent_type}
session_id: {session_id}
title: {descriptive title}
status: draft | review-ready | awaiting-annotation
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
source_file: ""
source_sha256: ""
evidence_tier: 1 | 2 | 3 | 4
updated: YYYY-MM-DD
coc_ref: ""
chain_id: ""
```

## Required Sections

Every finding must have these H2 sections:

### Summary
One paragraph. What was found. No case-specific names in generic fields.

### Evidence
What data supports this finding. Links to source files using relative vault paths.

### Next Steps
What the human reviewer should do with this. Promote? Verify? Discard?

## Structure Rules

- Title at H1 level
- Sections at H2 level
- Links use relative vault paths (not absolute WSL paths)
- No case data in generic metadata fields (agent_type, session_id, tags)
- Case-specific content goes in body only

## Example Output

```markdown
---
type: finding
blueprint: blueprint_finding
agent_type: evidence-analyst
session_id: 2026-03-29-abc123
title: TLS Certificate Overlap Between Entity Clusters
status: review-ready
generated: 2026-03-29
promotion_state: raw
doc_hash: sha256:pending
priority: HIGH
confidence_level: 0.87
---

# TLS Certificate Overlap Between Entity Clusters

## Summary
Analysis of certificate transparency logs reveals shared issuing infrastructure across three distinct entity clusters. Pattern is consistent with operational coordination.

## Evidence
- Source: [[00-SHARED/Agent-Outbox/evidence/tls-cert-extract.md]]
- Supporting: [[00-SHARED/Agent-Outbox/analysis/cert-clustering.md]]

## Next Steps
Promote to 30-Evidence/ after human review confirms entity match. Cross-reference with financial timeline.
```
