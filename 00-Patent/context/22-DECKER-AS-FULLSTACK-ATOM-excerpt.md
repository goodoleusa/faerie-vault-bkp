# 22 — Decker as Full-Stack Atom (excerpt)

> **Source:** `/mnt/d/0local/gitrepos/faerie2/docs/22-DECKER-AS-FULLSTACK-ATOM.md`
> **Copied:** 2026-05-25 for publication-prep bundle
> **Bundle note:** This excerpt covers the ontology paragraph, two-faces table, three trajectories,
> and the AUTO-FILLED badge. Full doc at source path. Supports the
> `2026-05-25-decker-as-full-stack-atom.md` primary paper and whitepaper §8 (UI canvas substrate).

**Series:** Architecture Canonicals | **Status:** Canonical | **Since:** 2026-05-25

---

## The Ontology in One Paragraph

A Decker card is not a visual widget with an optional code backing. It is a
two-faced atom whose front face encodes *frontend-design* — the visual surface,
the user's mental model, the interaction contract — and whose back face encodes
*backend-dev* — the data shape, the control flow, the system contract. The two
faces are inseparable by definition: a front without a back is a promise without
an implementation; a back without a front is logic that serves no human. The
card holds both professions as a single ontological unit. When you touch a
Decker card, you are always thinking full-stack, whether you realize it or not.

---

## The Two Faces as the Two Professions

| Face | Profession | Concerns |
|------|-----------|----------|
| **Front** | Frontend-Design | Visual layout, UI/UX reasoning, component structure, user empathy, interaction affordances, typography, spacing, accessibility |
| **Back** | Backend-Dev | Data schema, API shape, state management, business logic, control flow, persistence layer, system contracts |

These are not a "view layer" and a "logic layer" in the classical MVC sense.
They are two professional disciplines, each with its own reasoning mode, each
requiring genuine craft. The Decker card makes them share a single address —
the card ID — so that the seam between them is internal to the atom rather than
a handoff across a silo boundary.

The **AUTO-FILLED badge** marks honest provenance. When the system generates one
face from the other (via the Complete-pair function), the generated face is
tagged AUTO-FILLED to signal that it was derived, not hand-authored. This
preserves epistemic integrity: a human front-face sketch + an AUTO-FILLED
back-face spec is a different cognitive artifact than two hand-authored faces.
The badge does not diminish the generated face; it accurately names where it
came from. Treat it as a starting point for refinement, not a finished product.

---

## Three Valid Trajectories

The card is symmetric across entry point. There is no "correct" starting face.

### (a) Front-First — Sketch the UI, Derive the Back

The designer or developer begins on the front face: lays out the visual, defines
the interaction, names the inputs and outputs that the user will touch. Once the
front face is concrete, the back face can be derived: what state must exist to
render this UI? What API must exist to populate that state? What DB schema must
exist to back that API?

Front-first is natural when the problem begins with a user need that is most
clearly expressed as a visual.

### (b) Back-First — Spec the Data, Derive the Front

The developer begins on the back face: defines the data schema, the control
flow, the API contract. Once the back face is concrete, the front face can be
derived: what component renders this data? What interaction exposes this
control? What visual makes this contract legible to a user?

Back-first is natural when the problem begins with a data or system constraint
that must be expressed before the UI can be reasoned about.

### (c) Blueprint-Chain — Multiple Deckers Linked via NSEW Hierarchy

A single Decker card is one atom. A feature is a molecule: several cards linked
via the canvas hierarchy's NSEW edges (North = parent to child, South = child to
parent, East/West = siblings at the same level). A three-card chain
UI-card to API-card to DB-card is a complete full-stack feature specification.
Each card is internally full-stack (front + back); the chain makes the
inter-layer contracts explicit as hierarchy edges.

Blueprint-chain trajectory is natural when the feature is too large for one
card, or when different cards will be built by different people or agents.

---

## The Compass Hierarchy (NSEW Bearing on the Canvas)

Cards in a blueprint chain use the same compass grammar as the mission DAG:

| Bearing | Meaning on canvas | Meaning in mission graph |
|---------|------------------|--------------------------|
| **N** (North) | Parent card — the card above this one in the hierarchy | Unblock predecessor |
| **S** (South) | Child card — the card below this one | Conclude / move downstream |
| **E** (East) | Sibling card at the same level (→) | Parallel / sister work |
| **W** (West) | Sibling card at the same level (←) | Return / baseline |

The compass grammar is the same system used for manifest routing in the
mission graph. This means a Decker blueprint chain is directly representable
as a mission sub-graph: each card is a mission node; NSEW edges are compass
bearings. An agent can traverse a blueprint chain using the same frontier-read
logic it uses to navigate any mission cluster.

---

## The Dopamine Loop (canvas UX principle)

The dual-face card creates a specific feedback loop:

1. Author sketches front face (design intent, visual, interaction).
2. System derives back face (AUTO-FILLED: data shape, API contract).
3. Author reviews back face, corrects mismatches, refines.
4. System derives updated front face suggestions based on refined back face.
5. The two faces converge.

The loop is intrinsically motivating: each refinement on either face immediately
updates the derived twin. Authors experience the card "understanding" them. The
convergence point is a fully specified, internally consistent full-stack atom.

---

> Full canonical doc at `docs/22-DECKER-AS-FULLSTACK-ATOM.md` in the faerie2 repo.
> This excerpt covers the ontology, two-faces table, three trajectories, compass hierarchy,
> AUTO-FILLED badge, and dopamine loop. Sections on worked examples (login card, counter card,
> blog blueprint chain) and the canvas substrate integration are in the full doc.
