---
title: Design Philosophy
type: hive-design
up: "[[00-Hive-Home]]"
tags:
  - hive/design
  - philosophy
---

# The Hive — Design Philosophy

Inspirations and principles for the canvas, UX, and agent workspace design.

---

## Core Tension: Forage ↔ Sensemaking

From **Latticework** (Siu + Matuschak, 2024): knowledge work has two modes trapped in separate tools.

- **Foraging** — moving through source documents, highlighting, reacting in context
- **Sensemaking** — rearranging, elaborating, synthesizing fragments into understanding

Switching between tools destroys spatial and referential continuity. **The Hive canvas should keep both in the same surface** — a card you drop is a foraged fragment; its arrangement is sensemaking. They are not separate modes.

*Reference: [github.com/Siunami/Latticework](https://github.com/Siunami/Latticework)*

---

## Ancestor Engines

| Engine | What it contributes |
|--------|-------------------|
| **Twine** | The graph IS the document — structure and content are one surface |
| **Bitsy** | Palette constraint per space produces coherence automatically |
| **Decker** | Every artifact is harvestable text; scripting is embedded markup |
| **Ink** | Prose first, logic as annotation — writing feels like writing, not programming |
| **Latticework** | Source and synthesis are mutually visible — annotation is spatially anchored |
| **Kinopio** | Spatial card freedom + personality — upgraded with tighter palette + polish |

---

## Palette Discipline (Bitsy principle)

Pick and enforce per-section colors. Constraint produces coherence.

| Section | Color | Hex |
|---------|-------|-----|
| Dev | Amethyst | `#8B5CF6` |
| Eval | Deep Teal | `#0891B2` |
| UI/UX | Coral Rose | `#DB2777` |
| Marketing | Amber Gold | `#D97706` |
| Sales | Emerald | `#059669` |
| Agent Chat | Amethyst | `#8B5CF6` |
| Canvas bg | Warm Ivory | `#FDFAF5` |

---

## Card Anatomy (Kinopio polished)

A card in The Hive canvas has:
- **Type badge** (icon + semantic label: `note`, `link`, `task`, `honey`, `charter`)
- **Content** — prose first, never a form
- **Source thread** — visible backlink to where the card came from
- **Bearing** — N/S/E/W compass edge that situates it in mission context

Animation: spring physics on drag (`cubic-bezier(0.34, 1.56, 0.36, 1)` at 150ms). No grid-lock.

---

## Empty State Voice

Cards should speak personality in empty states:

> *"Your hive is quiet — drop a card to wake it."*

> *"No active missions. The swarm is resting."*

> *"All caught up. The bees are sunning themselves."*

---

## The Decker Principle

Every artifact should be harvestable. Cards, widgets, and blueprints are designed as copy-pasteable text — not binary exports. If you can't paste it somewhere else, it's too coupled.
