---
type: blueprint
blueprint_id: blueprint_agent_evolution
name: Agent Evolution Record
version: "1.1"
created: 2026-03-29
updated: 2026-03-29
status: active
---

# Blueprint: Agent Evolution Record

Longitudinal narrative of an agent type's learning arc — training scores, deployment performance,
OTJ learnings, and redemption record. One file per agent type, updated in place.
Process-only — no case data. Court-defensible.

## Metadata

| Field | Value |
|-------|-------|
| ID | blueprint_agent_evolution |
| Output dir | 00-SHARED/Agent-Outbox/agent-evolution/ |
| Filename pattern | `{agent-type}-evolution.md` |
| Agent types | Any agent type (self-written at OTJ shutdown) |
| Promotion target | `~/.claude/agents/{type}.md` (technique extraction via training pipeline) |
| Human annotation | .ann.md sibling |

## Required Frontmatter

```yaml
---
type: agent-evolution
blueprint: blueprint_agent_evolution
agent_type: {agent_type}
session_id: {session_id}
title: "{agent_type} Evolution — {date}"
status: active | archived
generated: YYYY-MM-DD
promotion_state: raw
doc_hash: sha256:pending
latest_score: 0.00
latest_deployment_score: 0.00
tier: BASELINE | MED | PRO | ELITE
redeemed_on_the_job: false
coc_ref: ~/.claude/memory/forensics/
---
```

## Optional Frontmatter

```yaml
tags: [agent-evolution, performance, self-improvement]
hash_ts: ISO8601
hash_method: body-sha256-v1
```

## Required Sections

### Current State
Single snapshot of current scores and tier. Updated in-place each run.
Format: `Score: {N} | Deployment: {N} ({date}) | Tier: {tier}`.

### Last Training
Most recent training event summary. Format matches agent card convention:
```
Score: {score} (prev: {prev}, delta: +{delta})
Context: {training|deployment|baseline}
Deployment: {score} (from {date})
```
Link to training task ID or session stream when available.

### Training Timeline
Markdown table: Date | Score | Delta | Context | Key Learning. Most recent row first.

### What It Learned (Process Only)
Bulleted list of transferable techniques and behavioral adjustments.
Court-defensibility test: could a defense attorney argue this biased future analysis? If yes, omit.

### Performance Trajectory
1-3 paragraph narrative written for a future instance of the same agent type.
Describes what drove improvements, where gaps remain, and what the ELITE path looks like.

## Structure Rules

- H1 = `{Agent Name} — Evolution Story`
- All five H2 sections required
- Training Timeline rows sorted most-recent-first
- Score tiers: BASELINE (0.0-0.69), MED (0.7-0.84), PRO (0.85-0.94), ELITE (0.95+)
- `redeemed_on_the_job: true` when deployment score beats previous training target
- File is updated in place — not a new file per training run
- Techniques extracted to `~/.claude/agents/{type}.md` after human review

## Validation Rules

- No case data: entity names, IPs, domains, dataset names are forbidden
- All five sections must be present
- `tier` must be one of: BASELINE, MED, PRO, ELITE
- Score values must be 0.0-1.0 floats
- Court-defensibility test applied to all content

## Example Output

See `00-SHARED/Agent-Outbox/agent-evolution/example-agent-evolution.md`
