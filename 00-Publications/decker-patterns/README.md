# Decker Pattern Library — Overview

> NOTE TO OPERATOR: The 8 JSON files in this directory (counter.json, toggle.json, etc.)
> should be deleted. They are machine-readable schema files that belong in the repo at
> `forensics/schemas/canvas-patterns/` only. The vault is for human-facing essays only.
> JSON files are not readable in Obsidian and violate the vault content policy.
>
> Canonical location for JSON schemas: faerie2/forensics/schemas/canvas-patterns/
> This vault directory can be removed entirely, or retained only for this README.

## The Eight Canonical Decker Patterns

The Decker canvas ships with eight built-in patterns — templates that pre-fill
both faces of a Decker card when a user invokes "Complete pair." Each pattern
encodes a front face (the visual design, the interaction model) and a back face
(the React code that makes it work). Together they are the starter vocabulary
of the ideate-to-product loop.

**Counter** — A numerical display with +/- buttons. The prototypical stateful
widget. Front: a large number and three buttons. Back: `useState(0)` with
increment, decrement, reset. Symmetric trajectory — works equally well as a
UI sketch or a state spec. Use it for scores, lap counts, tallies.

**Toggle** — A pill-shaped on/off switch. Front: animated sliding knob, color
transition grey-to-gold. Back: `useState(false)`, aria-checked for
accessibility. Back-led trajectory — you usually know the boolean state before
you know the exact visual. Use it for feature flags, settings, mode switches.

**Button** — A single gold CTA with press animation. Front: retro-bold box-
shadow, translate-on-click. Back: click handler stub with optional click
counter. Front-led — you see the button before you decide what it does. Use it
for actions, submissions, navigations.

**List** — An add/remove item list with checkboxes. Front: input + scrollable
rows with check + delete. Back: `useState([])` with add/toggle/remove
operations on `{id, text, done}` objects. Back-led — the data shape (array of
items with done state) is clearer than the exact UI. Use it for todos, shopping
lists, checklists.

**Form Field** — A labeled text input with submit. Front: label, input with
gold-on-focus border, dark submit button, success message. Back: controlled
input + submitted state. Front-led — the form interaction is the primary design
concern. Use it for search, settings inputs, any single-field collection.

**Gauge** — A 260-degree SVG arc showing 0-100. Front: arc track (grey) + arc
fill (gold) + centered value label + slider scrubber. Back: polar coordinate
math, `useState(50)`. Back-led — the metric value drives the visual. Use it
for progress, utilization, health scores, percentages.

**Info Card** — A titled description panel. Front: cream background, retro
border, bold title, body text, timestamp. Back: static React component, no
state. Front-led — the content structure is the design concern. Use it for
about sections, summaries, entity descriptions.

**Timer** — A MM:SS countdown with start/pause/reset. Front: large tabular
display (red under 10s), progress bar, buttons, duration slider. Back:
`useEffect` + `useRef` interval pattern, elapsed counting up. Symmetric — you
might start from "I need a 25-minute Pomodoro" (back) or "I need a big clock
with a progress bar" (front). Use it for Pomodoro, presentations, countdowns.

---

These eight patterns are the vocabulary. The canvas is the grammar. A Decker
card picks one pattern, completes both faces, and becomes a full-stack atom
ready to send to an agent for scaffolding.

Machine-readable schemas: `faerie2/forensics/schemas/canvas-patterns/`
