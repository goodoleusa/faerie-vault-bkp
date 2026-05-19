---
type: dashboard
tier: graph
title: "Compass Graph — Typed NSEW view"
status: live
N: '[00-Home](00-Home.md)'
E: ['[00-Home](00-Home.md)', '[01-Today](01-Today.md)', '[02-Missions-Emergent](02-Missions-Emergent.md)', '[03-Anchors](03-Anchors.md)', '[04-Eval-Dimensions](04-Eval-Dimensions.md)', '[05-Stigmergy](05-Stigmergy.md)']
W: '[00-Home](00-Home.md)'
tags: [dashboard, graph, juggl, compass]
juggl-config:
  layout: 'cola'
  styleGroups:
    - filter: 'edge[type = "N"]'
      style: { line-color: '#C73E1D' }
    - filter: 'edge[type = "S"]'
      style: { line-color: '#2E8540' }
    - filter: 'edge[type = "E"]'
      style: { line-color: '#FF8E3C' }
    - filter: 'edge[type = "W"]'
      style: { line-color: '#FFB300' }
---

> **🐝 Navigate:** [00 Home](00-Home.md) · [01 Today](01-Today.md) · [02 Missions](02-Missions-Emergent.md) · [03 Anchors](03-Anchors.md) · [04 Eval Dimensions](04-Eval-Dimensions.md) · [05 Stigmergy](05-Stigmergy.md)

# Compass Graph

Typed graph view of the dashboard frontier. Edges are colored by compass bearing:

- **N (jasper #C73E1D)** — unblock predecessor / parent
- **S (emerald #2E8540)** — conclude / child / downstream
- **E (coral #FF8E3C)** — parallel sister at same DAG level
- **W (amber #FFB300)** — return-to-baseline anchor

```juggl
local: true
expand-initial: true
toolbar: true
```

Open with `Cmd/Ctrl-P → Juggl: Open Juggl` if the block above does not auto-render.
