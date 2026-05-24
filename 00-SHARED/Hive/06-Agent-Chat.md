---
title: Agent Chat
type: hive-section
section: agent-chat
up: "[[00-Hive-Home]]"
same: "[[01-Dev]], [[02-Eval]], [[03-UIX]], [[04-Marketing]], [[05-Sales]]"
tags:
  - hive/chat
  - path/hive
cssclasses:
  - hive-section
---

# 🐝 Agent Chat Room

> [!west] Return to HQ
> The fun room — talk to the swarm, get answers, run spawns, vibe.

## Chat with Swarmy

```meta-bind-button
style: primary
label: "💬 Open Swarmy Chat"
action:
  type: link
  link: "https://swarmy.retrofuture.tech"
```

## Active Agents

| Agent | Archetype | Last Active |
|-------|-----------|-------------|
| Navigator | N-bearing | today |
| Maker | S-bearing | today |
| Bridge | E-bearing | — |
| Deep-Diver | W-bearing | — |

## Latest Session Notes

```dataviewjs
const manifests = dv.pages('"forensics/ephemeral"')
  .sort(f => f.file.mtime, 'desc')
  .slice(0, 3)
dv.list(manifests.map(m => m.file.link + " — " + (m.dashboard_line ?? "")))
```

## Bee Lore

> *The swarm doesn't think — it feels. Every agent is a sensory neuron. Together they are the hive mind.*

The Hive runs on stigmergy: agents leave pheromone trails (manifests) and others follow. No central command. Pure emergence.
