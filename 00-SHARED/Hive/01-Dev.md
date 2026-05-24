---
title: Dev
type: hive-section
section: dev
up: "[[00-Hive-Home]]"
same: "[[02-Eval]], [[03-UIX]], [[04-Marketing]], [[05-Sales]], [[06-Agent-Chat]]"
tags:
  - hive/dev
  - path/hive
cssclasses:
  - hive-section
---

# 🛠 Dev

> [!north] Mission Frontier
> Active swarmy sessions, OpenHands tasks, and blocked/ready work.

## OpenHands Workspace

- [[Mission-Graph]] — live compass DAG from `forensics/mission-graph.json`
- [Swarmy Chat](https://swarmy.retrofuture.tech) — chat-mvp V0 (Mission Steer)
- [Admin Panel](https://admin.retrofuture.tech) — V4 Admin Ops

## Active Repos

| Repo | Purpose | Status |
|------|---------|--------|
| [faerie2](https://github.com/Persistech/faerie) | Swarmy core + MCP server | active |
| [faerie-vault](https://github.com/Persistech/faerie-vault) | Obsidian vault | active |
| [cybertemplate](https://github.com/goodoleusa/cybertemplate) | Client site builder | active |
| [hustle](https://github.com/goodoleusa/hustle) | Marketing site | active |

## Quick Actions

```meta-bind-button
style: primary
label: "↺ Refresh Mission Graph"
action:
  type: command
  command: "swarmy:refresh-mission-graph"
```

```meta-bind-button
style: default
label: "📋 Recent Manifests"
action:
  type: command
  command: "swarmy:manifest-list"
```

## Pending

- [ ] MCP tool consolidation: 62 → ~30
- [ ] Forensics pruning: 17 → ~10 subdirs
- [ ] CI/CD auto-deploy pipeline
- [ ] Watchdog + disk crons
