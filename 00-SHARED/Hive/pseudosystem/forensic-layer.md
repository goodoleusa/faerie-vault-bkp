---
type: system-component
component_type: layer
status: active
created: 2026-03-27
tags: [system, pseudosystem, forensic-layer]
parent:
  - "[[_system-root]]"
sibling:
  - "[[vault-layer]]"
  - "[[agent-layer]]"
child:
  - "[[coc-hash-chain]]"
  - "[[hash-integrity]]"
inputs:
  - "[[agent-work]]"
  - "[[subagent-spawning]]"
outputs: []
color: dark
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:03006e2705279c651dce7beebfd09eef28f59bafc1979f81e3e7433768395df8
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Forensic Layer

The bedrock. The forensic layer is write-only for agents — they append logs, sign entries, and never read from it. This architectural constraint is non-negotiable: if agents could read forensic logs, those logs could influence findings, destroying court admissibility. The forensic layer records: every tool call, every agent spawn, every file touch, every finding with the exact agent version that produced it. HMAC-SHA256 hash chains ensure tamper evidence.

## Flow

**In:** Every tool call (via PostToolUse hook, automatic and silent), agent spawn events, file operations
**Out:** Nothing flows out to agents. Researchers access via Obsidian vault mirror. Court exhibits are exported from here.

## Relationships

- [[coc-hash-chain]] — the chain-of-custody log: session ID, agent type, agent version, tool calls, timestamps
- [[hash-integrity]] — SHA256 verification of every file at time of access
- [[agent-work]] — every action during work is logged here automatically
- [[agent-cards]] — agent version (date_score) embedded in every COC entry
- [[vault-layer]] — researcher-review/ subfolder mirrors here for Obsidian access

## Natural Metaphor

Bedrock: ancient, immutable, load-bearing. Everything above is built on it. You cannot dig it up to change what's there; you can only build on top. The geological record proves what happened when.
