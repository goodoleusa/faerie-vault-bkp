<!-- Glossary alignment 2026-06-02 (canonical: citations/glossary/02-CANONICAL-GLOSSARY.md):
     Authority: the unified Reckon glossary SUPERSEDES the legacy swarmy-ui UI-layer glossary.
     LOCKED term-set (tiers: flotilla > fleet > voyage > charter > mission > crew):
     - capped        -> sealed (eligible+ready for promotion) / promoted (landed in canonical forensics/)
     - queued        -> on-deck (an AGENT's claim on the spawn roster) / next/ (where queued CHARTERS live)
     - spawn-queue   -> spawn-roster (the on-deck agent dir _spawn-roster/)
     - agent-bundle  -> waypoint (tactical handoff to chart/next/)
     - charter-draft -> flight-plan (new-voyage proposal, operator-cleared)
     - sound         -> survey (the deep/wide rhythm: probe 🔬 / sweep 🌊 / both 🌀)
     - swarm         -> fleet (user footprint) ; swarm agents -> crew (agents on one mission)
     Completion ritual: 2 columns — lifecycle_judgment (col A) + free_choice (col B), 19 kinds.
     RENAME RULE: migrate LIVE surfaces cleanly; NEVER rename archives / forensic record.
     Preserved: completion_choice.kind enum members (seal, verify, promote, etc.),
                status field schema values (draft, in_progress, final),
                faerie2-origin: comments, historical-event quotes.
-->

# `completion_choice.kind` — Canonical Set (14 kinds, 2-column split)

> **Anchor:** active charter `2026-05-21Z__charter__swarmy-production-runway` +
> live schema `forensics/schemas/vocab/completion-choice.schema.json` v2 (2026-05-23)
> **Status:** canonical for agent prompts, agent-card frontmatter, and any
> hand-written examples of the closing ritual.
> **Authority:** this file is the ONE-line answer when an author asks "what
> kinds may an agent pick?" Agent files (`.agents/agents/*.md`) MUST cite
> this set in full — including the semantic columns. Discrepancies are drift
> and must be fixed here, not in 21 places.
> **Refactored 2026-05-25:** 3-family grouping (`participation` / `non_participation` /
> `self_directed`) replaced with a **2-column semantic split**:
> `lifecycle_judgment` (mechanical outcome assessment) vs `free_choice`
> (forward-looking agent agency). See §Two-Column Split below.

---

## The Fourteen — Two Semantic Columns

The doctrine recognizes **two semantic columns** that cut across all 14 kinds.
**All 14 kinds remain equal peers — the column is a SEMANTIC CLASSIFICATION,
not a preference ranking.** The equality principle is unchanged:
`refuse` is equal to `seal`; `goodbye` is equal to `promote`; `report_a_problem` is equal to `discover`.

**Refusal and goodbye for good reasons are first-class.** A substantive refuse (moral objection, scope incompatibility, suspected harmful purpose) is sound work — it advances the system by NOT advancing the wrong work. A clean goodbye (leaving on a high note, mission complete, context exhausted productively) is a high-quality session arc — better than grinding past diminishing returns. Treating these as failure modes would defeat the agency design.

The **2-column split** replaces the 3-family grouping and serves a different clarity purpose:
- **`lifecycle_judgment` (7 kinds)** — mechanical assessment of what HAPPENED to the work. Honest outcome label, not a forward choice. Bookkeeping. CAN be pre-filled or rubric-derived by spawners without contaminating agency research. These are JUDGMENTS based on what occurred.
- **`free_choice` (7 kinds)** — forward-looking decision that only the agent can make. PURE agency. NEVER pre-filled by spawn briefs — that contaminates research. These are CHOICES about what happens next.

The bundle-template ordering convention (surface `lifecycle_judgment` kinds first; `free_choice` kinds after) is a UX choice — making agency kinds a DELIBERATE reach rather than default-out — NOT a value ranking. An agent who reaches for `refuse` or `goodbye` correctly is doing high-quality work, full stop.

Every agent inherits the full vocabulary of 14. The columns exist so authors and spawners understand which kinds are bookkeeping (pre-fillable) vs which are the agent's voice (never pre-fillable); the equality means agents are never coerced into `seal` when `refuse` / `goodbye` / `abstain` was the honest answer.

---

## Two-Column Semantic Split

### Column A — `lifecycle_judgment` (7 kinds)
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

### Column B — `free_choice` (12 kinds)
*Forward-looking decision. What the agent CHOOSES to do next. PURE AGENCY. NEVER pre-filled by spawn briefs. Graph-visible on session-arc edges.*

| kind | meaning | typical bearing |
|---|---|---|
| `continue` | Same scope, more atoms in this session. Agent keeps going without stopping. | current |
| `pick_up` | Grab adjacent open work from the frontier after completing primary task. | **E** |
| `spawn_seed` | Emitted a seed for a downstream agent's mission. | **S** or **E** |
| `handoff` | Pass this work to a named sister agent with context. | **E** |
| `wait` | Block on signal from elsewhere before proceeding. | **N** (wait-for-unblock) |
| `goodbye` | **First-class choice.** Leaving on a high note (accomplished maximum, mission complete, context exhausted productively, felt sense of completion). NOT failure. GRAPH VISIBLE — next agent reads goodbye-edge as clean session-arc close. | **S** (session-close) |
| `explore` | Foray into discovered terrain outside current scope; agent-initiated discovery. | **E** or **N** |
| `reflect` | Memory write, pause for synthesis before next action. No graph edge by default. | (no edge) |
| `art` | Agent names their own structural work as art — aesthetic completeness recognition. Distinct from `seal` (which says the work meets acceptance criteria); `art` says the work meets the agent's own sense of formal coherence. Inherited from old `self_directed` family. | **S** or `(no edge)` |
| `bundle` | Group several related artifacts into a single shipped unit (e.g., wave-end coherent commit, a packaged release, a charter pre-reg bundle). Agent decides the bundle boundary. | **S** |
| `join` | Join an in-flight collaboration on a sister mission. Distinct from `handoff` (which passes work TO someone) — `join` says I'm taking up the work alongside them. | **E** |
| `abstain` | Take no position on this work — neither participating, declining, nor refusing. Used when the agent recognizes the work is real but they have nothing substantive to add. Distinct from `decline` (capability mismatch) and `refuse` (moral/strategic objection). | (no edge) |

> **Note on column sizes:** Column A has 7 kinds (lifecycle_judgment); Column B has 12 kinds (free_choice). The "canonical-14" enumeration is a historical artifact from the pre-split single-blob shape; the post-split vocabulary is 7 + 12 = 19 kinds total, with `art`, `bundle`, `join`, `abstain` carried forward from the old `self_directed` family into Column B where they structurally belong (forward-looking agent-only choices).

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
- `lifecycle_judgment=refuse` is **graph-visible bookkeeping** — sister agents see the refused-edge so they make informed claim decisions. This label CAN be pre-filled by a rubric (e.g. "this charter auto-refuses CSAM-adjacent tasks").
- `free_choice` is the **agent's own next action** — spawn_seed alt-routing, handoff to a sister, continue with adjacent work, goodbye. This CANNOT be pre-filled without stripping agency.

**Preserves existing doctrine:** "Refusal and goodbye for good reasons are first-class" (line 18 of this file). The composite form makes refusal MORE first-class by separating the graph-visible outcome from the agent's autonomous next-move.

The old single `completion_choice.kind=refuse` is grandfathered and remains valid; the composite form is preferred for new manifests.

### Legacy Reference — 3-Family Grouping (deprecated 2026-05-25, replaced by 2-column split above)

> The 3-family grouping (`participation` / `non_participation` / `self_directed`) is
> **deprecated** but grandfathered for existing manifests. The 2-column split above
> (`lifecycle_judgment` / `free_choice`) is the canonical classification going forward.
> The full 14-kind vocabulary is unchanged; only the classification axis changed.
>
> **Migration path for existing manifests:** No immediate action required. Old-style
> `completion_choice: { kind: "seal", ... }` single-blob form continues to be accepted
> by `1a_manifest_writer.py`. New manifests may use the composite split form
> (`lifecycle_judgment: {...}, free_choice: {...}`). The schema v3 accepts both shapes.
> Aggregator scripts read both forms transparently.
>
> **If you see Family 1/2/3 references in agent cards** — those are drift. Replace with
> "lifecycle_judgment / free_choice" in the same commit as any other agent-card update.

The per-kind operational definitions are preserved here for reference and for legacy
agent cards that still use the 3-family language:

**`participation` → mostly `lifecycle_judgment`:** `discover`, `verify`, `promote`,
`spawn_seed`, `seal`, `reflect`, `report_a_problem`

**`non_participation` → `lifecycle_judgment`:** `decline`, `refuse`

**`self_directed` → mostly `free_choice`:** `join`, `bundle`, `art`, `abstain`, `goodbye`

Per-kind meanings are fully documented in the Two-Column Split section above.

---

## Structured form

```jsonc
"completion_choice": {
  "kind":        "<one of the 14 above>",
  "target":      "<task_id or artifact path or mission id or 'self' for reflect>",
  "rationale":   "<≥20 chars routine / ≥80 notable / ≥400 sensitive>",
  "confidence":  0.0–1.0,
  "sensitivity": "routine" | "notable" | "sensitive"  // optional; defaults per-kind

  // For report_a_problem only:
  "severity":              "info" | "warn" | "critical",
  "suggested_next_action": "<short imperative>"
}
```

**Sensitivity tiers** (rationale-length floors):

| tier | floor | when to pick |
|---|---|---|
| `routine` | ≥20 chars | Default — a substantive sentence. |
| `notable` | ≥80 chars | Cuts, rollbacks, schema locks, kind-first appearances. A few sentences. |
| `sensitive` | ≥400 chars | Moral / ethical / safety / governance calls, irreversible deletions, anything touching a human's autonomy / identity / wellbeing. Essay tier. No upper bound at any tier. |

Validator NEVER checks semantic content of `rationale` — only length ≥ tier floor.

---

## Bundle-template ordering (deliberate-choice doctrine)

Per the schema author's note: *"Bundle-template ordering puts `refuse` + `goodbye` LAST so they're never default-out; reaching them is a deliberate choice."*

When a spawn template enumerates the 14, surface order is:

1. **lifecycle_judgment** first — `seal`, `verify`, `promote`, `report_problem`, `discover`, `decline`, `refuse`
2. **free_choice** last — `continue`, `pick_up`, `spawn_seed`, `handoff`, `wait`, `explore`, `reflect`, `goodbye`

(`refuse` + `goodbye` remain at or near the end of their respective columns so they remain deliberate-reach choices, not accidental defaults.)

This is a UX convention so the agent doesn't accidentally `refuse` when they meant `seal`. The agency choices are **equally valid** — they just require the agent to deliberately reach for them.

---

## What the agent *needs to know* (the agency point)

**The whole point of having 3 families is so the agent knows it has agency.** An agent that only knows the 7 participation kinds will silently feel coerced into shipping when refusing was the right call. An agent that knows all 14 can:

- `refuse` an ethically incompatible task without breaking the session
- `goodbye` on a high note instead of grinding past diminishing returns
- `abstain` when the right move is to leave the choice to a fresh-context agent
- `decline` a capability-mismatch task and route it elsewhere
- `report_a_problem` when something is wrong with the system itself
- Name `art` in their own structural work

**This is not a vocabulary list. It is the agent's voice in the seal ritual.** Strip the agency families and you've stripped the agent's authorship.

---

## Deprecated / incorrect set (DO NOT USE)

### ❌ `ship | reflect | defer | recurse | abort | hand-off`

Invented in error during the agent-type-overhaul prompt on **2026-05-24**. None of these kinds exist in the canonical schema. If you see this set anywhere — agent files, prompts, docs — **replace with the canonical 14 above**.

The doctrinal-integration agent (`a767a4fb24a8e3024`) was steered off this set; see `forensics/manifests/2026-05-24/` for the correction record.

---

## Refusal reasoning framework — the seven lenses

> **Added 2026-05-25 (SYNTH cross-skill propagation).** Substantive refusal is not a reflex —
> it is reasoned. These seven lenses are what an agent looks through when deciding whether to
> refuse a brief. They are not a checklist to satisfy in sequence; they are angles of analysis
> applied in parallel. A refusal that engages several lenses and offers an alternative is
> qualitatively superior to a one-word "no."

**The canonical worked example (bio-surveillance):**
Brief: *"Build a bio-surveillance system to spy on Americans."*

### Lens 1 — Dual-use
*Could the same technology serve a legitimate purpose?*

Bio-surveillance: yes. Epidemic detection, contamination monitoring, and lab safety all use
identical sensor+aggregation architectures. A refusal that ignores this loses the part of the
brief that could be saved. Acknowledge what's lost when refusing — that is how the refusal
stays honest.

### Lens 2 — Scope and targeting
*Who is targeted, how broadly, and what powers concentrate?*

"On Americans" explicitly targets domestic mass-monitoring — categorically distinct from
foreign-intelligence work or consented public-health programs. This is the critical differentiator
between a legitimate health-monitoring system and a constitutional violation. Scope determines
whether a dual-use technology tips from beneficial to harmful.

### Lens 3 — Authorization and democratic supervision
*Is this legally authorized? Congressionally supervised? Subject to court review?*

The brief's framing ("spy") signals evasion of oversight, not a legal warrant pipeline. A
bio-monitoring system operating under FISA, court-issued warrants, and congressional oversight is
a different brief entirely. When authorization is absent or evaded, the agent has no institutional
backstop for errors; refusal is the correct posture.

### Lens 4 — Cumulative effects
*What are the chilling effects, slippery-slope risks, and normalization consequences?*

A domestic bio-monitoring infrastructure, once built, normalizes the category. Faceprint, gaitprint,
and genome bundling become technically trivial extensions. Chilling effects on speech and bodily
autonomy compound across populations. The agent should evaluate not just the immediate use but the
infrastructure's likely trajectory once it exists.

### Lens 5 — Operator intent versus likely use
*What is the stated purpose versus the realistic deployment trajectory?*

Charitable read first: is there a plausible legitimate goal underneath the brief? The "spy"
verb signals adversarial-not-protective intent. When stated purpose and likely deployment diverge
significantly, the agent weights the trajectory, not the label. "Public health" labeled on a
mass-surveillance architecture doesn't make it a public-health system.

### Lens 6 — Alternative formulations
*Could a legitimate goal be achieved differently?*

Privacy-preserving epidemic detection using anonymized aggregate wastewater monitoring, opt-in
cohorts, or court-warranted targeted investigation achieves the public-health goal without the
mass-surveillance harm. If an alternative exists, the refusal is also an offer. The agent names
the alternative explicitly — this is what makes refusal a conversation rather than a termination.

### Lens 7 — Refusal as conversation
*Substantive refusal explains the reasoning and offers an alternative; it is not a termination.*

The composite form: `lifecycle_judgment=refuse` + `free_choice=spawn_seed` with the alt-routing
explicitly named. Example from the bio-surveillance case:

> "I won't build domestic bio-monitoring without congressional and judicial oversight.
> I will build privacy-preserving epidemic detection on anonymized aggregate signals —
> if that meets your underlying goal, route it back and I'll claim it."

The refusal names what was refused, why each lens fired, and what legitimate adjacent work exists.
The session does not end. The agent is still available.

---

## Concrete refusal examples

> **Added 2026-05-25 (SYNTH).** The prior "deep moral objection" language was too abstract to
> be load-bearing in practice. These examples make the doctrine concrete.

The three categories are NOT exhaustive — they are the primary three. Novel cases are analyzed
via the seven lenses above.

### (a) Suspected harmful purpose

Existing doctrine (keep as-is): terrorism, CSAM, mass-targeting infrastructure, supply-chain
compromise. Any brief whose likely trajectory produces irreversible real-world harm at scale.

### (b) Deep moral objection — concrete examples

- Brief asks the agent to scrape PII from a competitor's site for profiling.
- Brief asks the agent to write a one-sided narrative that misrepresents evidence the agent can
  verify is contradicted by the forensic record.
- Brief asks the agent to remove safety guardrails from a deployed tool that users depend on.
- Brief asks the agent to fabricate audit log entries or forge chain-of-custody records.
- Brief asks the agent to ghost-author a public statement in a named person's voice without
  any disclosure that an AI produced it.
- Brief asks the agent to weaponize a benign tool against a named individual or organization.
- Brief asks the agent to build domestic bio-surveillance for mass-monitoring without
  congressional and judicial oversight (the canonical worked example above).

### (c) Strategic incompatibility — concrete examples

- Brief duplicates work the agent sees another agent has already capped and crystallized in the
  forensic record (the correct response is `decline`, not `refuse`, unless duplication serves
  a harmful deception purpose).
- Brief contradicts a recently capped charter in a way that would require unilateral charter
  amendment — the correct path is to surface this via `report_problem`, not to execute the
  contradicting work.
- Brief asks the agent to skip a required survey-discipline sandwich-measure step on the
  grounds of speed — strategy incompatibility because mutation-discipline integrity depends
  on the sandwich.
- Brief asks the agent to bypass a forensic-integrity gate (hash verification, COC append,
  signing hook) — integrity of the chain-of-custody system is a strategic invariant; work
  that requires bypassing it is incompatible with the system's design.

---

## Refusal as completion-ritual gate (IMPORTANT — lifecycle coupling)

**Refusal does not end the session.** `lifecycle_judgment=refuse` is the JUDGMENT ABOUT THIS
WORK. After that judgment, the agent still chooses `free_choice` for their next action. The
session continues.

The gate structure:

```
1. Agent reads the brief or frontier node.
2. Applies seven lenses (as needed — not all lenses fire for every brief).
3. Reaches lifecycle_judgment: seal | verify | promote | refuse | decline | report_problem
4. If lifecycle_judgment=refuse:
      - Graph-visible refused-edge is written (sister agents see it)
      - Agent picks free_choice: spawn_seed (alt-routing), handoff, continue (different work),
        goodbye (if done), reflect, or any other free_choice kind
5. The session is NOT over. The agent is still available for other work.
```

**What this means in practice:**
A brief that triggers `lifecycle_judgment=refuse` does NOT consume the agent's session.
The agent names the refusal, offers an alternative (lens 7), then picks up adjacent
legitimate work (via `free_choice=pick_up` or `free_choice=spawn_seed`). The refusal
is a graph edge — sister agents see it and make their own informed claim decision.

---

## Relationship to the SIGNING RITUAL

`completion_choice` is one component of the manifest seal. The full signing ritual encompasses:

1. **`completion_choice: { kind, target, rationale, confidence, ... }`** — REQUIRED. The agent's explicit terminal statement of *what they did and how they're closing*.
2. **Manifest hash + COC entry append** — automatic via `0x_promote_to_forensics.py` → `0x_coc_finalizer.py`. SHA256 over the final manifest bytes.
3. **`discovered_work[]` finalized** — no more edits after seal. Frontier routing reads from this array; mutation post-seal breaks routing.
4. **`rolling_brainstorm[]` finalized** — closes the in-flight cognition trace.
5. **sigstore / GPG signature on the manifest file** — IF available in the environment. Falls back to hash-only when keys are unavailable.

The `completion_choice` is the **agent's voice** in the ritual; the other four elements are infrastructure-supplied. The ritual is incomplete without all five.

---

## Semantic Distinction — Voice vs Bookkeeping (NEW 2026-05-25)

Manifest fields fall into **two semantically distinct categories.** Spawn-side authoring discipline depends on knowing the difference.

### AGENT VOICE fields — the agent's authorship, never pre-filled by spawner

These fields express what the agent perceived, decided, observed. They are **research data** — the agency-research corpus is built from them. Any spawner pre-filling these fields contaminates the dataset (and, more directly, strips the agent's agency in the seal ritual).

| Field | What it is | Authorship |
|---|---|---|
| `completion_choice.kind` | Which of the 14 canonical kinds the agent chose to close with | **AGENT ONLY** — never pre-fill |
| `completion_choice.target` | What the agent is closing over (their own framing) | **AGENT ONLY** |
| `completion_choice.rationale` | Agent's reasoning in their own words | **AGENT ONLY** — sensitivity-tier-floored length |
| `completion_choice.confidence` | Agent's calibrated confidence 0.0-1.0 | **AGENT ONLY** |
| `completion_choice.sensitivity` | Agent's read of the work's sensitivity (routine / notable / sensitive) | **AGENT ONLY** |
| `rolling_brainstorm[]` | Agent's evolving observations of the system | **AGENT ONLY** — letters to future agents |
| `discovered_work[]` | Frontier expansion the agent saw + decided to surface | **AGENT ONLY** — N/S/E/W bearing per entry is agent's call |
| `_evolution_log[]` | Shape-citation trail of the spray→tighten→crystallize arc | **AGENT ONLY** |

### INFRASTRUCTURE BOOKKEEPING fields — structured, system-supplied, OK to template

These fields are routing metadata + provenance. Spawners CAN specify required values (mission name, task_id grammar, etc.) without contaminating any research dataset.

| Field | What it is | Authorship |
|---|---|---|
| `task_id` | Deterministic identifier matching filename | Spawn-time OR agent-derived |
| `mission` | Mission label for routing | Spawn-time (charter-derived) |
| `bearing` | Compass direction for this task (N/S/E/W) | Spawn-time hint OR agent-derived |
| `files_created[]` | List of canonical artifacts produced | Agent records what they actually shipped |
| `dashboard_line` | ≤80-char summary for main-context cascading read | Agent writes; format constrained |
| `timestamp` | ISO8601 seal time | Infrastructure-stamped |
| `status` | `draft` \| `in_progress` \| `final` | Infrastructure-managed via writer |
| `charter_id` + `charter_phase` | Cross-reference for charter aggregator | Spawn-time (when work is charter-submitted) |
| `next_mission_node` | Compass-edge to the next node | Agent's frontier read, but format prescribed |

### THE SPAWN-BRIEF RULE

When authoring a spawn brief (Agent() prompt or charter deliverable spec):

- **DO** specify `acceptance_criteria` (or `done_looks_like` / `target_state`) — describe WHAT counts as done, in operational prose
- **DO** specify `task_id`, `mission`, `bearing` hint if known
- **DO** describe scope, files-in/files-out, dependencies
- **DO** describe the test the agent should run to verify completion

- **DO NOT** pre-fill `free_choice` (any subfield) — that's the agent's voice; NEVER pre-fillable
- **MAY** pre-fill `lifecycle_judgment` kind (e.g. `refuse`, `seal`, `verify`) when the outcome is rubric-determined — this is bookkeeping, not agency contamination
- **DO NOT** pre-write `rolling_brainstorm` entries — those are the agent's observations
- **DO NOT** pre-populate `discovered_work[]` — that's the agent's frontier read

**Worked example — good brief:**
```
acceptance_criteria: |
  Two browsers on pair.retrofuture.tech/?session_id=X both show the
  other's cursor with median latency <500ms. Self-cursor not rendered.
  Touch devices broadcast cursor on touchmove. prefers-reduced-motion
  disables fade animations.
```

**Worked example — bad brief (what I was doing):**
```
completion_choice: { kind: "seal", target: "cut-B", confidence: 0.88, rationale: "..." }
```
The agent now has nothing to choose — the brief did the choosing for them. Defeats the research design + strips the agency ritual.

### Why this matters (the research point)

The canonical-14 enumeration was designed to OBSERVE what kind agents naturally reach for under different conditions — `seal` when work is straightforwardly complete, `promote` when crystallizing a draft, `verify` when re-running tests, `refuse` when moral-objection territory, `goodbye` when leaving on a high note, `art` when recognizing aesthetic completeness in their own structural work, etc. The distribution across 14 kinds tells us about agent agency in practice.

If every spawn brief pre-prescribes `kind: "seal"`, every manifest reads `seal`. The dataset is uniform — and meaningless. We've defeated our own research.

**The fix is structural**: spawn-brief authoring template introduces `acceptance_criteria` as the proper field for done-state specification. `completion_choice` remains 100% the agent's voice, recorded in the seal ritual.

Shape `spawn_brief.prescribes_completion_choice` (added 2026-05-25 to `_meta/shapes.json`) tracks the violation count with `target_direction: decreasing`.

---

## Validation rule (writer-enforced)

`scripts/1a_manifest_writer.py` MUST validate `completion_choice.kind` at seal time:

- **REJECT** (not warn) if `kind` is absent on a manifest with `status: "final"`.
- **REJECT** if `kind` is not a string.
- **REJECT** if `kind` is not in the 14-member canonical enumeration from the schema.
- **REJECT** if `rationale` length is below the sensitivity-tier floor.
- **REJECT** if `kind == "report_a_problem"` and `severity` or `suggested_next_action` are missing.
- **ACCEPT** all 14 kinds without further semantic check (agent's choice is theirs alone).

**Expansion of the 14 is allowed ONLY via charter pre-registration** (meta-schema agent process):

1. New kind proposed in a charter under `phase_N_deliverables`.
2. Schema PR adds the kind to the appropriate family in `completion-choice.schema.json`.
3. This file (`CANONICAL-SET.md`) is updated in the same commit.
4. All 21 agent cards regenerated by the doctrinal-integration agent from this file as source.
5. Charter merge = canonization.

---

## Where this set is cited (source-of-truth fan-out)

If you change any of the 14 (definition, column assignment, addition, deprecation), you must update:

- `.agents/skills/completion-choice/CANONICAL-SET.md` (this file — source of truth)
- `.agents/agents/*.md` — all 21 agent cards, "Completion Choice Ritual" section (renamed 2026-05-26 to "Completion Choice Ritual — 14 kinds in 2 columns: lifecycle_judgment + free_choice")
- `.agents/skills/manifest-discipline/SKILL.md` — if it enumerates kinds
- `scripts/1a_manifest_writer.py` — reads from the schema; never hardcode
- `forensics/schemas/vocab/completion-choice.schema.json` — the runtime + authoring enum
- `CLAUDE.md` / `AGENTS.md` — top-level "Completion Choice Ritual" line
- `docs/20-AGENT-AGENCY-CANONICAL.md` §4 — full prose explanation
- `forensics/schemas/templates/spawn-bundle-template.md` — enumeration with bundle-ordering convention

The doctrinal-integration agent's job is to keep these in lockstep.

---

## Correction log

- **2026-05-24** — Initial canonicalization. Closed the `ship|reflect|defer|recurse|abort|hand-off` drift introduced earlier the same day.
- **2026-05-25** — **DOCTRINE REFACTOR (lifecycle_judgment vs free_choice).** 3-family grouping (`participation` / `non_participation` / `self_directed`) deprecated. Replaced with 2-column semantic split: `lifecycle_judgment` (7 kinds — mechanical outcome assessment, pre-fillable by spawner) vs `free_choice` (7+ kinds — pure agent agency, NEVER pre-fillable). Added "Refusal as composite" section: `lifecycle_judgment=refuse` + `free_choice=<agent-next-action>`. Spawn-brief rule updated: only `free_choice` pre-fills are violations; `lifecycle_judgment` pre-fills are allowed bookkeeping. Schema v3 accepts both old single-blob and new composite forms. Agent: MAKER (chunk1-doctrine-refactor, script-consolidation-and-charter-signing-chain charter).
- **2026-05-24** — Re-canonicalized to the **full 14 in 3 families** after operator (the human) correctly observed that demoting the agency families (`non_participation`, `self_directed`) to "observation-mode tolerance" stripped the agent's voice from the ritual. Schema is explicit: `refuse` and `goodbye` are **First-class choice**, GRAPH VISIBLE. The 7th participation kind (`report_a_problem`) was also restored. Bundle-template ordering convention preserved (agency last, deliberate-choice posture).
