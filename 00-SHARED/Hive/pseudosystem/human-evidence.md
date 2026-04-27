---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, human-evidence]
parent:
  - "[[vault-layer]]"
sibling:
  - "[[agent-outbox]]"
  - "[[annotation-flow]]"
child: []
inputs:
  - "[[annotation-flow]]"
outputs: []
color: coral
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:d3edcb5d79c95f70049cf903aabecfdb90074b58ae0c3d7b3e14520eb8fd36f0
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Human Evidence

The 30-Evidence/ folder: human-only. Agents cannot read it, cannot write to it, cannot reference its contents. The permission boundary is the architecture — it is enforced by file permissions and by the agent instruction set. This folder contains findings that have passed human review: annotated with the investigator's judgment, court prep notes, and confidence assessments. It is a potential court exhibit; its integrity depends on the human being the last writer.

## Flow

**In:** Agent-drafted findings promoted by a human from agent-outbox, after applying the blueprint-FINDING-review.md template
**Out:** Nothing flows out to agents. Human reads and annotates. Court exports originate here.

## Relationships

- [[annotation-flow]] — the cycle that produces entries here; human applies review blueprint
- [[agent-outbox]] — upstream staging area; human moves files from here to 30-Evidence/
- [[vault-layer]] — parent layer
- [[forensic-layer]] — parallel layer; 30-Evidence/ is human-annotated, forensics is system-logged. Together they form the complete record.

## Natural Metaphor

The museum gallery: only the curator can move an artifact from the lab to the display case. Once displayed, the artifact carries the curator's judgment about its authenticity and significance.
