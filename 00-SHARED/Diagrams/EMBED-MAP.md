---
type: embed-map
status: pending
tags: [embed-map, diagrams, visual-design]
created: 2026-04-24
doc_hash: sha256:90306eee36c685296ca61d611a66de4267bfb5da78354ab49e8243872898f9f0
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

# Diagram Embed Map

This file records which diagrams should be embedded in which docs once the curator
agent creates them. Apply these embeds during a follow-up pass — search for each
target doc and insert the embed syntax at the indicated anchor text.

---

## Applied Embeds (already inserted)

| Diagram | Target Doc | Status |
|---|---|---|
| `f0-queen-bee.excalidraw` | `vault/HOME.md` | DONE — after f(0) blockquote |
| `five-principles-compass.excalidraw` | `00-SHARED/Hive/what-is-faerie.md` | DONE — before Related section |

---

## Pending Embeds (curator doc not yet created)

### `00-SHARED/Hive/piston-rocket-physics.md`

Embed after the wave model table or intro paragraph:

```
![[../Diagrams/piston-waves.excalidraw]]
```

Anchor: insert after any H2 section introducing W1/W2/W3.

---

### `00-SHARED/Hive/stigmergic-recursion.md`

Embed near the top, after the opening definition:

```
![[../Diagrams/stigmergic-recursion.excalidraw]]
```

Anchor: after the first paragraph describing the cycle.

---

### `00-SHARED/Architecture/memory-topology.md`

Embed after the memory layer table or intro:

```
![[../Diagrams/memory-topology.excalidraw]]
```

Anchor: before or after the HONEY/NECTAR/pollen description.

---

### `00-SHARED/Architecture/phase-anchoring.md`

Embed after the phase manifest definition:

```
![[../Diagrams/phase-anchoring.excalidraw]]
```

Anchor: after the first section describing what a phase manifest contains.

---

### `00-SHARED/Hive/staged-chain-stigmergy.md`

Embed after the chain/DAG explanation:

```
![[../Diagrams/staged-chain-dag.excalidraw]]
```

Anchor: near any description of blockedBy or task sequencing across sessions.

---

## Embed Syntax Reference

Obsidian wiki-embed (no file extension needed, but `.excalidraw` suffix is optional):

```
![[Diagrams/diagram-name.excalidraw]]
```

From a doc inside `00-SHARED/Hive/` or `00-SHARED/Architecture/`, use relative path:

```
![[../Diagrams/diagram-name.excalidraw]]
```

From `vault/HOME.md` (root level):

```
![[00-SHARED/Diagrams/diagram-name.excalidraw]]
```

or with the path Obsidian resolves from vault root:

```
![[Diagrams/diagram-name.excalidraw]]
```

---

## Diagram Inventory

| File | Subject | Palette |
|---|---|---|
| `f0-queen-bee.excalidraw.md` | Main as queen, agents radiating | Blue center, white agents |
| `piston-waves.excalidraw.md` | W1/W2/W3 rocket stage bars | Blue bars, black axes |
| `stigmergic-recursion.excalidraw.md` | Cycle: agent→manifest→hook→queue→spawn | Blue/green nodes |
| `memory-topology.excalidraw.md` | Pyramid: pollen→NECTAR→HONEY | Blue gradient tiers |
| `phase-anchoring.excalidraw.md` | Phase manifest → tasks + auditor | Blue header, white tasks |
| `staged-chain-dag.excalidraw.md` | Task chain with blockedBy edges | Green/blue/white nodes |
| `five-principles-compass.excalidraw.md` | Pentagon with f(0) center | Blue center, white vertices |
