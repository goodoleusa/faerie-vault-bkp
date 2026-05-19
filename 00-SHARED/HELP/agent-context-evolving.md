---
type: meta
memory_type: agent-context-evolving
updated: 2026-03-11
tags: []
doc_hash: sha256:fd22bed36852c6d800004fcdc9d614a5f8ee859407a9301fe6c319ec41dc243e
hash_ts: 2026-03-29T16:09:50Z
hash_method: body-sha256-v1
---

# Evolving context (read at run start)

*Agent_runner loads this file at run start. Agent updates it at end of run: add bullets from lessons, corrections, and verdict feedback; trim to last ~50 lines. See [[../00-META/08-AGENT-ADAPTIVE-CONTEXT-AND-EVOLVING-PROMPT]].*

## Do / prefer

- When creating entity stubs, link parent to investigation; set confidence low until validated.
- Use canonical handoff format (Agent: / Handoff:) in 01-Memories/shared so next agent can parse.
- After completing a task, set task frontmatter: status done, completed_date, result_summary, output_files; append to agent-logbook and agent-history; update 03-Agents/agent.md.

## Don't / avoid

- Don't promote entity confidence to medium before human or second-agent validation.
- Never delete or overwrite existing logbook entries; add corrections in 01-Memories/human/corrections instead.

## When …

- When task has a parent task: include handoff reference in Context section.
- When evidence is unverified: set source_quality to unverified and confidence_level low.
