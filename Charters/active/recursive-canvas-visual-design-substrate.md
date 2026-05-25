---
type: charter
status: active
charter_id: recursive-canvas-visual-design-substrate
semantic_mission: canvas.visual.design
cluster_prefix: ["canvas", "visual", "design"]
phase: ""
author: goodoleusa
created: 2026-05-24
canonical_repo_path: "forensics/charters/active/2026-05-24Z__charter__recursive-canvas-visual-design-substrate__goodoleusa.json"
filename_base: "2026-05-24Z__charter__recursive-canvas-visual-design-substrate__goodoleusa"
tags: [charter, pseudosystem]
blueprint: "[[Charter.blueprint]]"
---

# Charter — recursive-canvas-visual-design-substrate

> **Vault pseudosystem mirror** — canonical source: `forensics/charters/active/2026-05-24Z__charter__recursive-canvas-visual-design-substrate__goodoleusa.json`
> Status: **active** | Phase: **** | Mission: `[[canvas.visual.design]]`

---

## Thesis

Recursive canvas is the operator's visual-design substrate inside the swarmy shell. Brainstorm on
the canvas → frame a region → send the frame to OH as a design spec → OH produces the
implementation. Cards carry front/back semantic (user-facing front, backend architecture back) so
the design naturally flows from concept to dev. The canvas is the headwater (per the canvas-as-
headwater charter); this work makes the headwater FLOW.

## Phases

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| phase_3_selection_frame_to_oh | Cut 3 — rubber-band selection frame; send framed region to O | 4 | queued |
| phase_4_braided_strings_to_nested | Cut 4 — red braided strings between parent card and nested c | 3 | queued |
| phase_5_decker_widget_maker | Cut 5 — Widget MAKER (Decker-inspired custom widget authorin | 6 | queued |
| phase_6_canvas_as_dev_surface_integration | Cut 6 — close the loop: canvas → OH iframe → implementation  | 4 | queued |

## Operator Pain Points

- Text editing requires multiple clicks — mobile-hostile
- No visible affordance for edit mode
- Nested canvas layers aren't visually connected — no sense of where in the parent you are
- Can't send a REGION of the canvas to OH, only one card at a time
- Need custom widgets but no maker UI

## Non-Goals

- Forking Excalidraw (we already use it as an I/O format; not reimplementing)
- Real-time multiplayer canvas editing (single-operator MVP)
- Full Decker feature parity — we lift the concept (HyperCard-style scriptable widgets), not the spec
- Bidirectional code↔canvas sync (one-way: canvas → OH spec → code is enough for now)
- Excalidraw plugin store full mirror — only catalog + port the 10 highest-value scripts; the rest stay one click away in 

## Related Charters

- (none)

---

*To jump to canonical JSON: open `forensics/charters/active/2026-05-24Z__charter__recursive-canvas-visual-design-substrate__goodoleusa.json` in repo. Vault note is navigation-only — do not edit to change charter state.*
