---
type: index
tags: [meta, index]
doc_hash: sha256:65f5e7b541949145b10b9b590591d4b563c88616dbcf20e2f7b3888ee541fe28
hash_ts: 2026-03-29T16:10:51Z
hash_method: body-sha256-v1
---

# 02-Skills — Agent Capabilities

**For humans**: Browse what your agents can do. Each skill is a reusable prompt template.
**For agents**: Load the relevant skill spec before executing a task. Skills define your prompt, tools, output format, and quality criteria.

## Skill Categories
- **Research**: Web research, OSINT lookups, source verification
- **Analysis**: Pattern detection, cross-referencing, statistical analysis
- **Writing**: Report generation, evidence summaries, plain-language explainers
- **Data**: Extraction, cleaning, transformation, enrichment
- **Review**: Evidence assessment, quality scoring, gap analysis

## Skill Protocol
- Skills are Markdown files with structured frontmatter (see [[Agent-Skill.blueprint]])
- `input_schema` defines what the skill expects
- `output_schema` defines what it produces
- `quality_criteria` defines how to evaluate output

## All Skills
```dataview
TABLE skill_category, complexity, last_used
FROM "02-Skills"
WHERE type = "skill"
SORT skill_category ASC, file.name ASC
```
