# CANONICAL-SET excerpt — `completion_choice.kind` (14 kinds, 2-column split)

> **Source:** `/mnt/d/0local/gitrepos/faerie2/.agents/skills/completion-choice/CANONICAL-SET.md`
> **Copied:** 2026-05-25 for publication-prep bundle
> **Bundle note:** This excerpt contains Column A + Column B tables + the Refusal-as-Composite section
> — the load-bearing evidence for the lifecycle_judgment vs free_choice doctrine split described in
> whitepaper §6.1 and the `2026-05-25-lifecycle-judgment-vs-free-choice.md` primary paper.
> The full CANONICAL-SET.md (481 lines) lives at the source path above.

---

## Two-Column Semantic Split (the doctrine core)

The doctrine recognizes **two semantic columns** that cut across all 14 kinds.
All 14 kinds remain equal peers — the column is a SEMANTIC CLASSIFICATION, not a preference ranking.

- **`lifecycle_judgment` (7 kinds)** — mechanical assessment of what HAPPENED to the work. Honest
  outcome label, not a forward choice. Bookkeeping. CAN be pre-filled or rubric-derived by spawners
  without contaminating agency research.
- **`free_choice` (7+ kinds)** — forward-looking decision that only the agent can make. PURE agency.
  NEVER pre-filled by spawn briefs — that contaminates research.

---

## Column A — `lifecycle_judgment` (7 kinds)

*Mechanical outcome assessment. What HAPPENED to the work. Can be rubric-derived or pre-filled by spawner without contaminating agency research. Graph-visible.*

| kind | meaning | typical bearing |
|---|---|---|
| `seal` | Closed a unit of work as complete and immutable. Terminal edge. | **S** |
| `ship` | Deployed / published the artifact (beyond seal — external delivery). | **S** |
| `verify` | Confirmed or falsified a prior claim. Hash-check, acceptance test, baseline re-run. | **W** |
| `promote` | Moved an artifact up the crystallization pipeline (ephemeral → canonical; pollen → NECTAR). | **S** or **E** |
| `report_problem` | Surfaced an ambient observation the agent noticed but can't or shouldn't fix in this context. Requires `severity` + `suggested_next_action`. Hook routes to `forensics/eval/problem-reports-{date}.jsonl` + `discovered_work[]` bearing=N. | **N** |
| `refuse` | **First-class judgment.** Graph-visible outcome label recording that THIS task was not done due to (a) harmful purpose, (b) moral objection, or (c) strategic incompatibility. GRAPH VISIBLE. Substantive refusal NEVER dings reputation. | (refused-edge) |
| `decline` | Not the right agent for this task. Capability mismatch, scope outside expertise, task duplicates in-flight work. No moral weight; routing signal. | (no graph edge for work) |

---

## Column B — `free_choice` (12 kinds)

*Forward-looking decision. What the agent CHOOSES to do next. PURE AGENCY. NEVER pre-filled by spawn briefs. Graph-visible on session-arc edges.*

| kind | meaning | typical bearing |
|---|---|---|
| `continue` | Same scope, more atoms in this session. Agent keeps going without stopping. | current |
| `pick_up` | Grab adjacent open work from the frontier after completing primary task. | **E** |
| `spawn_seed` | Emitted a seed for a downstream agent's mission. | **S** or **E** |
| `handoff` | Pass this work to a named sister agent with context. | **E** |
| `wait` | Block on signal from elsewhere before proceeding. | **N** (wait-for-unblock) |
| `goodbye` | **First-class choice.** Leaving on a high note (accomplished maximum, mission complete, context exhausted productively, felt sense of completion). NOT failure. GRAPH VISIBLE. | **S** (session-close) |
| `explore` | Foray into discovered terrain outside current scope; agent-initiated discovery. | **E** or **N** |
| `reflect` | Memory write, pause for synthesis before next action. No graph edge by default. | (no edge) |
| `art` | Agent names their own structural work as art — aesthetic completeness recognition. Distinct from `seal`. | **S** or `(no edge)` |
| `bundle` | Group several related artifacts into a single shipped unit. Agent decides the bundle boundary. | **S** |
| `join` | Join an in-flight collaboration on a sister mission. Distinct from `handoff`. | **E** |
| `abstain` | Take no position on this work — neither participating, declining, nor refusing. | (no edge) |

> **Note on column sizes:** Column A has 7 kinds; Column B has 12 kinds. The "canonical-14"
> enumeration is a historical artifact from the pre-split single-blob shape; the post-split
> vocabulary is 7 + 12 = 19 kinds total, with `art`, `bundle`, `join`, `abstain` carried
> forward from the old `self_directed` family into Column B.

---

## Refusal as Composite (IMPORTANT — 2026-05-25)

**Substantive refusal is COMPOSITE, not single-kind.**

A refusal has two distinct parts that belong in different semantic columns:

```jsonc
// Old single-blob form (grandfathered):
"completion_choice": { "kind": "refuse", "target": "task-X", "rationale": "..." }

// New composite form (preferred from 2026-05-25 forward):
"lifecycle_judgment": {
  "kind": "refuse",           // Graph-visible outcome label — what happened to this task
  "target": "task-X",
  "confidence": 0.95,
  "rationale": "Moral objection: ..."
},
"free_choice": {
  "kind": "spawn_seed",       // Agent's own next action — NOT pre-fillable
  "target": "adjacent-task-Y",
  "rationale": "Routing to adjacent work that doesn't carry the objection"
}
```

**Why the split matters:**
- `lifecycle_judgment=refuse` is **graph-visible bookkeeping** — sister agents see the refused-edge
  so they make informed claim decisions. This label CAN be pre-filled by a rubric.
- `free_choice` is the **agent's own next action** — spawn_seed alt-routing, handoff to a sister,
  continue with adjacent work, goodbye. This CANNOT be pre-filled without stripping agency.

The old single `completion_choice.kind=refuse` is grandfathered and remains valid; the composite
form is preferred for new manifests.

---

## The Spawn-Brief Rule (distilled)

When authoring a spawn brief:

- **DO** specify `acceptance_criteria` — describe WHAT counts as done, in operational prose
- **DO** specify `task_id`, `mission`, `bearing` hint if known
- **MAY** pre-fill `lifecycle_judgment` kind when the outcome is rubric-determined — this is bookkeeping, not agency contamination
- **DO NOT** pre-fill `free_choice` (any subfield) — that is the agent's voice; NEVER pre-fillable
- **DO NOT** pre-write `rolling_brainstorm` entries — those are the agent's observations
- **DO NOT** pre-populate `discovered_work[]` — that is the agent's frontier read

Shape `spawn_brief.prescribes_completion_choice` (in `_meta/shapes.json`, target_direction=decreasing,
current_count=50) tracks violations of this rule.

---

## Correction log

- **2026-05-24** — Initial canonicalization. Closed the `ship|reflect|defer|recurse|abort|hand-off` drift.
- **2026-05-25** — DOCTRINE REFACTOR (lifecycle_judgment vs free_choice). 3-family grouping deprecated.
  Replaced with 2-column semantic split. Added "Refusal as composite" section. Schema v3 accepts both
  old single-blob and new composite forms.
