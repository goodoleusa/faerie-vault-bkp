---
type: system-component
component_type: layer
status: active
created: 2026-03-27
tags: [system, pseudosystem, vault-layer]
parent:
  - "[[_system-root]]"
sibling:
  - "[[forensic-layer]]"
  - "[[memory-layer]]"
child:
  - "[[agent-outbox]]"
  - "[[human-evidence]]"
  - "[[annotation-flow]]"
inputs:
  - "[[agent-work]]"
  - "[[review-inbox]]"
outputs:
  - "[[annotation-flow]]"
  - "[[human-evidence]]"
color: coral
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:c866078491ba93bc7bf0ad9ff7d0d0421571129f6bcba298acc69165447d4793
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Vault Layer

The human interface. The vault (CyberOps-UNIFIED Obsidian vault) is the investigator's annotated record of the case — potentially a court exhibit. Agents write drafts to the agent outbox only; humans promote to 30-Evidence/. The permission boundary is architectural: agents cannot see 30-Evidence/, humans cannot be bypassed. The coral color throughout signals human attention, human judgment, human accountability.

## Flow

**In:** Agent drafts from agent-work, HIGH flags from review-inbox
**Out:** Human-annotated findings for annotation-flow; promoted evidence in human-evidence

## Relationships

- [[agent-outbox]] — where agents deposit vault-facing drafts (00-SHARED/Agent-Outbox/)
- [[human-evidence]] — 30-Evidence/: human-only, agents never read this folder
- [[annotation-flow]] — the cycle of human review, annotation, and promotion
- [[review-inbox]] — HIGH flags mirror to vault 00-Agent-Inbox/
- [[forensic-layer]] — researcher-review/ subfolder bridges forensics to vault

## Natural Metaphor

A museum's conservation lab and public gallery: agents prepare artifacts in the lab (outbox), curators examine and decide what goes on display (annotation flow), the gallery is for visitors (30-Evidence/ for human review).
