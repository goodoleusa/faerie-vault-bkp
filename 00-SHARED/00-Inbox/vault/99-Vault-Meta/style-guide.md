---
type: style-guide
status: active
tags: [style, typography, diagrams, vault-meta]
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:cb4d0ab060a66a1ba6425603126d3e1c04983cff44b90cd88e3d44504691531c
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Vault Meta](INDEX.md) · [⌂ Home](../HOME.md)

# faerie2 Vault Style Guide

This document defines the visual and editorial standards for all content in this vault.
The goal is a clean, technical aesthetic that reads like a well-produced whitepaper —
not a blog post, not a sketchpad.

---

## Typography

### Text font

**Open Sans** — the primary typeface for all prose, headings, tables, and UI text.

- Fallbacks in order: Inter, system-ui, sans-serif
- Why Open Sans: neutral, highly legible at small sizes, strong technical pedigree
- Do NOT use: Virgil, Cascadia, Comic Sans, or any handwriting/display face

### Code font

**JetBrains Mono** — for all inline code, code blocks, and terminal output.

- Fallbacks: Fira Code, ui-monospace, monospace
- Weight: regular (400) for most code; no bold code except explicit emphasis

### Sizes and weights

| Element | Size | Weight |
|---|---|---|
| H1 (doc title) | 1.85em | 600 |
| H2 (main section) | 1.40em | 600 |
| H3 (subsection) | 1.15em | 600 |
| Body text | 15px / 1.0em | 400 |
| Table | 0.92em | 400 (header 600) |
| Code | inherit from mono | 400 |

Letter spacing: -0.005em body, -0.015em headings. Line height: 1.55.

---

## Heading Hierarchy

| Level | Use | Notes |
|---|---|---|
| H1 | Document title only | One per document, at top |
| H2 | Main sections | Start after the intro paragraph |
| H3 | Subsections | Only when H2 content genuinely subdivides |
| H4+ | Never | Restructure instead |

If you feel you need H4, the document structure is wrong. Refactor.

---

## Color Palette

Four colors total. No exceptions without a documented reason.

| Role | Hex | Use |
|---|---|---|
| Black | `#000000` | Text, borders, arrows |
| White | `#FFFFFF` | Background, fill on light elements |
| Info / primary | `#3B82F6` | Primary nodes, accent lines, important labels |
| Success | `#10B981` | Completion states, positive signals |
| Blocker | `#EF4444` | Error states, blockers, warnings |

Background fills in diagrams use opacity variants of the info blue (`dbeafe`, `bfdbfe`, `f0f9ff`) — not additional colors.

---

## Diagrams (Excalidraw)

All diagrams use Obsidian Excalidraw plugin format (`.excalidraw.md`).

### Required settings for every diagram

| Setting | Value |
|---|---|
| `roughness` | `0` — clean machine-drawn lines |
| `strokeStyle` | `"solid"` — no hand-sketched dashes for structure |
| `strokeWidth` | `1.5` — consistent across all elements |
| `fontFamily` | `1` (Helvetica/built-in) — overridden by CSS to Open Sans |
| `appState.viewBackgroundColor` | `"#FFFFFF"` |
| `appState.gridSize` | `20` — all elements snap to 20px grid |

### What diagrams must not do

- No `roughness > 0` (eliminates hand-sketch wobble)
- No Virgil or Cascadia fonts inside diagrams (CSS override handles this, but do not set explicitly)
- No gradients, drop shadows, or decorative fills
- No more than 4 colors per diagram (see palette above)
- No clip art, icons, or emoji inside diagram elements

### Diagram naming

Filename pattern: `{concept-slug}.excalidraw.md`

All diagrams live in `00-SHARED/Diagrams/`. Embed via wiki-link:

```
![[Diagrams/diagram-name.excalidraw]]
```

---

## Content Patterns

### Tables

Use for: comparisons, property lists, configuration reference, two-column fact pairs.

Do not use for: sequential steps (use numbered list), single-column enumerations (use bullets).

### Lists

- **Bullet lists** — unordered enumerations, properties, features
- **Numbered lists** — sequences where order matters (steps, phases, ranked items)
- Never nest lists more than two levels deep

### Blockquotes

For definitions, principles, and key callouts only. Not for large blocks of prose.

```
> **Term:** Definition or key principle.
```

### Code blocks

Always specify the language. Use triple backtick with language tag:

````
```python
code here
```
````

For shell commands, use `bash`. For config files, use `json`, `yaml`, or `toml`.

---

## Links and References

- **Wiki-links preferred** — `[[Target Doc]]` over external URLs for in-vault navigation
- **Breadcrumb required** — every doc starts with a breadcrumb line after frontmatter:
  `> [↑ Parent](parent.md) · [⌂ Home](../../HOME.md)`
- **External URLs** — use sparingly; link to canonical sources only

---

## Frontmatter (required on every doc)

```yaml
---
type: narrative | reference | guide | style-guide | index | diagram
status: active | draft | deprecated
tags: [relevant, tags]
parent: Parent/Path
up: Parent/Path
created: YYYY-MM-DD
updated: YYYY-MM-DD
doc_hash: sha256:pending
---
```

`doc_hash` must be stamped before the document is considered final. Run `stamp_doc_hash.py` on the file.

---

## Voice and Tone

- **Direct and declarative** — say what things are, not what they might be
- **No hedging** — avoid "might", "could", "possibly" unless genuinely uncertain
- **No AI tell-phrases** — no "delve", "leverage", "seamlessly", "unlock potential"
- **Technical precision** — use exact terms (manifest, task_id, wave, queue) rather than paraphrases
- **Neutral register** — not casual, not formal. Engineering document tone.

---

## What This Vault Is Not

- Not a blog. No introductory fluff.
- Not a marketing page. No benefits-focused language.
- Not a sketchpad. No rough diagrams or placeholder text in published docs.
- Not a whiteboard export. All diagrams engineered, not sketched.
