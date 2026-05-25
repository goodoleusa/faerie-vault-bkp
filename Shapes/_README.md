---
type: readme
pseudosystem_folder: Shapes
canonical_repo_path: "_meta/shapes.json"
tags: [readme, pseudosystem]
---

# Shapes — Pseudosystem README

## What This Folder Is

`Shapes/` contains vault dossiers for every shape registered in `_meta/shapes.json`. A **shape** is a mechanically-detectable pattern of work — a count that the measurement substrate (RAP, mutation assessment, membench) uses to assess whether a change was beneficial, neutral, or harmful.

Each shape note here provides:
- The shape's description and measurement semantics
- Current count + history table
- The detector script that produces the count
- Interpretation guidance

## What This Folder Is NOT

- Not the canonical shape registry (that's `_meta/shapes.json`)
- Not where you edit counts (counts flow from detector scripts → shapes.json)
- Not where you define new shapes (author shapes in `_meta/shapes.json` + register their detectors)

## Shape ID Grammar

```
{domain}.{subject}.{mode}
```

Examples:
- `mcp.tools.granular` — MCP domain, tools subject, granular mode (each standalone tool = 1 count)
- `manifest.signed_by.missing` — manifest domain, signed_by subject, missing mode
- `charter.active.over_cap` — charter domain, active subject, over_cap mode

## Target Direction

| Direction | Meaning |
|-----------|---------|
| `decreasing` | System is healthier with fewer of these |
| `increasing` | System is healthier with more of these |
| `bounded` | System requires this count to stay within a range |
| `stable` | Count should not change; variation is a signal |

## Mutation Assessment

When a change is made:
1. Run relevant detector scripts → get before/after counts
2. Compare to `target_direction`: moving toward target = **beneficial**, away = **harmful**, no change = **neutral**
3. Record verdict in `shapes.json` `history[]`

## How to Add a New Shape Note

1. Add the shape to `_meta/shapes.json` (using the authoring protocol in SHAPES-README.md)
2. Blueprint → `Shape.blueprint` in Obsidian
3. Save to `Shapes/{shape_id}.md`
4. Add row to `_MOC.md`

---

*Part of the Vault Pseudosystem — see `PSEUDOSYSTEM-README.md` at vault root.*
