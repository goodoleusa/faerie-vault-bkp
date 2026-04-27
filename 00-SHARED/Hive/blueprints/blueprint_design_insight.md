---
type: blueprint
blueprint_id: blueprint_design_insight
name: Design Insight
version: "1.0"
created: 2026-03-29
status: active
---

# Blueprint: Design Insight

ADR-style record of a significant design decision — problem, solution, trade-offs, impact.
Lives in the Hive/ narrative sequence. Numbered with the NN- prefix to maintain temporal order.
Captures the "why" behind architectural choices so future agents and collaborators understand
the reasoning, not just the outcome.

## Metadata

| Field | Value |
|-------|-------|
| ID | blueprint_design_insight |
| Output dir | 00-SHARED/Hive/ |
| Filename pattern | `{NN}-{slug}.md` (e.g., `18-vault-blueprint-system.md`) |
| Agent types | fullstack-developer, knowledge-synthesizer, faerie (design sessions) |
| Promotion target | NECTAR (key decisions) + `~/.claude/memory/HONEY.md` (gauntlet-proven insights) |
| Human annotation | .ann.md sibling |

## Required Frontmatter

```yaml
---
type: design-narrative
blueprint: blueprint_design_insight
title: "{concise decision title}"
agent_type: {agent_type}
session_id: {session_id}
generated: YYYY-MM-DD
status: draft | active | superseded | archived
doc_hash: sha256:pending
promotion_state: raw
coc_ref: ~/.claude/memory/forensics/
---
```

## Optional Frontmatter

```yaml
tags: [design, adr, {topic-tag}]
supersedes: "[[NN-old-decision.md]]"
superseded_by: ""
related:
  - "[[NN-related.md]]"
impact: LOW | MED | HIGH | CRITICAL
hash_ts: ISO8601
hash_method: body-sha256-v1
```

## Required Sections (ADR Format)

### Context
What situation or problem drove this decision? What constraints existed?
1-3 paragraphs. Honest about uncertainty at the time of decision.

### Decision
What was decided? State it clearly in one sentence, then elaborate.
The decision should be writable as: "We will X because Y."

### Alternatives Considered
What else was on the table? Why was it rejected or deferred?
Bullet list. At least one alternative. "We only considered one option" is a red flag.

### Trade-offs
What does this decision cost? What does it give up? What risks does it introduce?
Table format preferred:

| Trade-off | Description |
|-----------|-------------|
| Gains | ... |
| Costs | ... |
| Risks | ... |
| Deferred | ... |

### Impact
What changed as a result? What other parts of the system does this affect?
Where does this show up in the running system?

## Structure Rules

- H1 = `{NN} — {Decision Title}`
- All five ADR sections required
- `status: superseded` + `superseded_by:` when a later decision overrides this
- Numbered prefix NN- is sequential within Hive/ — check existing files before assigning
- `impact: CRITICAL` for decisions that change memory routing, forensics, or agent prompts
- Written at decision time, not retrospectively — capture the thinking in the moment
- References use wikilink format: `[[NN-slug.md]]`

## Validation Rules

- All five ADR sections must be present (Context, Decision, Alternatives Considered, Trade-offs, Impact)
- `status` must be one of: draft, active, superseded, archived
- `impact` must be one of: LOW, MED, HIGH, CRITICAL (if set)
- At least one alternative in Alternatives Considered
- Trade-offs table must have Gains and Costs rows
- No case data in frontmatter fields

## Example Output

```markdown
---
type: design-narrative
blueprint: blueprint_design_insight
title: "Blueprint System for Agent Output Types"
agent_type: fullstack-developer
session_id: 2026-03-29-a3f8c1
generated: 2026-03-29
status: active
impact: HIGH
doc_hash: sha256:pending
promotion_state: raw
coc_ref: ~/.claude/memory/forensics/
tags: [design, adr, blueprints, vault-schema]
---

# 18 — Blueprint System for Agent Output Types

## Context

Audit revealed 50 blueprints defined in VAULT-SCHEMA.md but only 7 used (86% unused).
Agents were writing output files with improvised frontmatter — missing agent_type, session_id,
promotion_state, and blueprint reference fields. Without a live template, each agent invented
its own schema. This made Dataview queries unreliable and membot promotion fragile.

## Decision

We will create per-type blueprint files in `Hive/blueprints/` covering the 5 most active
output types, each with required frontmatter spec, validation rules, and an example output
in Agent-Outbox/. Blueprints are referenced by name in vault note frontmatter via
`blueprint: blueprint_{type}`.

## Alternatives Considered

- **Single VAULT-SCHEMA.md mega-document:** Already exists and is ignored in practice.
  Splitting by type makes each schema digestible and linkable.
- **Enforce via Python validation script:** Useful but downstream — the agent still needs
  to know what to write. Script catches errors; blueprint prevents them.
- **Dataview template injection:** Obsidian templates can inject frontmatter, but agents
  writing via CLI don't use Obsidian templates. Agent-readable blueprint files solve both sides.

## Trade-offs

| Trade-off | Description |
|-----------|-------------|
| Gains | Per-type schema clarity; agents can reference single authoritative file |
| Costs | 5 new files to maintain; drift risk if blueprint updated but old outputs not |
| Risks | Agents may still not check blueprint if not in spawn prompt |
| Deferred | Automated validation at write time (separate task) |

## Impact

All agent output types now have canonical schema in Hive/blueprints/. System-Architecture.md
updated with blueprint registry section. Future agents receive blueprint path in spawn prompts.
Dataview queries for promotion_state and agent_type become reliable.
```
