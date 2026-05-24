---
title: The Hive
type: hive-home
up: "[[00-SHARED/Dashboards/00-Home]]"
down: "[[01-Dev]], [[02-Eval]], [[03-UIX]], [[04-Marketing]], [[05-Sales]], [[06-Agent-Chat]]"
tags:
  - hive
  - hub
cssclasses:
  - hive-home
---

# 🐝 The Hive

**Swarmy Operations Center** — dev, eval, UI/UX, marketing, sales, and agent chat, all under one roof.

---

## Sections

| | Section | Purpose |
|--|---------|---------|
| 🛠 | [[01-Dev]] | Mission frontier, OpenHands, GitHub repos |
| 📊 | [[02-Eval]] | Eval runs, metrics, publishing |
| 🎨 | [[03-UIX]] | Mockups, themes, assets, design playground |
| 📣 | [[04-Marketing]] | Content, campaigns, brand |
| 💰 | [[05-Sales]] | Intake pipeline, clients, Stripe |
| 🐝 | [[06-Agent-Chat]] | Talk to the swarm |

---

## System Status

```dataviewjs
// Quick status snapshot
const today = new Date().toISOString().slice(0, 10)
dv.paragraph(`**Date:** ${today}`)
```

```meta-bind-button
style: primary
label: "🔄 Sync Vault"
action:
  type: command
  command: "swarmy:vault-sync"
```

```meta-bind-button
style: default
label: "🖼 Open Canvas"
action:
  type: command
  command: "app:open-file"
```

---

> *The swarm doesn't wait to be told what to do. It reads the pheromone trails and moves.*

![[Hive.canvas]]
