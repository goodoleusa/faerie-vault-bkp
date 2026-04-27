---
type: meta
tags: []
doc_hash: sha256:708cd0fb07a65d86705475e52ef218f0baeb7dbdbbe9b45556d8b60a8d2b1482
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:35Z
hash_method: body-sha256-v1
---

 
 /crystallize leanness: Done — rewrote it to zero inline reads. One action: spawn membot background → return
  "spawned." All compression work stays in membot, never in main context.

  Agent Outbox for community resilience:

  The pattern you're describing is already half-built. Here's how to make it work:

  Agent A (researcher) → drops findings.md → 00-SHARED/Agent-Outbox/
  Agent B (distributor) → polls Outbox → formats → writes to:
    ├── Local Human-Inbox (your vault)
    └── Remote vault via USB/Syncthing/dead-drop (collaborator's vault)

  The A2A folder in 00-SHARED/ is the right place for agent-to-agent handoffs. Agent B would be a lightweight
  "distributor agent" — reads outbox, strips investigation-specific PII per collab rules, writes sanitized briefing to
  both vaults. The collab command already does half of this (dead-drop messaging between sessions).

  For USB hand-off between human-AI dyads, the minimum viable export is:

  ┌─────────────────────┬───────────────────────┬──────────────────────────────────────────────────────────┐
  │       Export        │        Folder         │                          Format                          │
  ├─────────────────────┼───────────────────────┼──────────────────────────────────────────────────────────┤
  │ Evidence bundle     │ 30-Evidence/          │ .md with YAML frontmatter (type/tier/hypothesis_support) │
  ├─────────────────────┼───────────────────────┼──────────────────────────────────────────────────────────┤
  │ Crystallized memory │ MEMROUND/             │ HONEY-*.md snapshots                                     │
  ├─────────────────────┼───────────────────────┼──────────────────────────────────────────────────────────┤
  │ Timeline            │ 60-Chronology/        │ .md notes + optional CSV                                 │
  ├─────────────────────┼───────────────────────┼──────────────────────────────────────────────────────────┤
  │ Intelligence briefs │ 40-Intelligence/      │ BRIEF-*.md                                               │
  ├─────────────────────┼───────────────────────┼──────────────────────────────────────────────────────────┤
  │ Queue state         │ 00-SHARED/Dashboards/ │ faerie-brief.json + sprint queue                         │
  ├─────────────────────┼───────────────────────┼──────────────────────────────────────────────────────────┤
  │ Agent memory        │ 00-SHARED/Memories/   │ NECTAR snippets, agent notes                             │
  └─────────────────────┴───────────────────────┴──────────────────────────────────────────────────────────┘

  The receiving dyad sets CT_VAULT to the USB mount path and fires /faerie — it reads the brief, picks up the queue,
  and continues. No special import step needed; the vault IS the handoff protocol.


  7 agents running — all criticalexposure tasks in flight. Session status:

  [🚀 T2 | ⚡ 7 agents running | ctx ~48K | HIT ✓ | $0.04/turn | headroom: 130K]
  LAUNCHED: research-analyst ×4 (cdn181+siblings, ORNL cert, fashfed+yszfa, port scan)
            data-engineer ×2 (Hetzner IPs, COC-GAP2)
            fullstack-developer ×1 (timeline.html)
  VAULT: 000-SHARED → 00-SHARED updated across all 5 config locations
  COMMANDS: /crystallize created (lean), /handoff canonical, faerie.md cleaned