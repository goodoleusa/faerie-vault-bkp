---
date: 2026-05-22
author: openhands-agent
related_mission: docs-canon-foundation
related_skill: vault-daily
status: synthesis-log
---

# HONEY.md — Archeological Dig Through the Variant Lineage

A deep, file-by-file dig through the nine source documents that produced
HONEY.md v3.0.0 (the current canonical at `/mnt/d/0local/gitrepos/faerie2/HONEY.md`).
The companion narrative at `02-honey-evolution-narrative.md` told the
story of *how* the substrate evolved. This file goes underneath that
story: into each variant verbatim, what each one does best, what each
one got wrong, what survived into v3, and — most importantly — what
got buried in the synthesis but should come back in v4.

This is meant to be read by:

1. A future agent or human deciding whether to fork v3 into v4
2. Anyone asking "why does HONEY.md look the way it does?"
3. The Claude who comes after me, looking for orphaned good ideas

Read with the mindset of an archeologist, not a librarian: there are
broken pieces here, layers of overlapping intent, and load-bearing
ideas that didn't make it to the surface. The shape of what's missing
is as informative as the shape of what's there.

---

## Why the dig matters

HONEY.md v3 promotes a single 335-line file from a forge that produced
~4,400 lines of variant material across nine source documents. The
compression ratio is roughly 13:1. That much pressure on the synthesis
step inevitably loses good things — not because the synthesizer was
careless, but because at 13:1 you can only keep one of every thirteen
ideas, and choosing *which* one is itself a high-stakes act.

The job of this dig is to surface the twelve out of thirteen that got
left behind, so v4 can resurrect what's still load-bearing without
re-running the whole evolution cycle from scratch.

---

## Cross-cutting observations before the per-variant sections

Before diving into each file, three patterns showed up across the
whole corpus and are worth naming up front so they don't have to be
re-discovered in each section:

**1. The "v1-pre-evolution" file is mislabeled.**
`HONEY-future/archive/HONEY-v1-pre-evolution.md` is 388 lines and
internally claims `honey_version: 3.0.0`, `variant: "federation-crystallizer"`.
It is NOT the original 173-line v1. It is the federation-crystallizer's
candidate v3 — a *sibling* of HONEY-EVOLVED.md, not its predecessor.
The actual "current v1" referenced in the v3 frontmatter source list
is most plausibly the file now archived at `archive/context/HONEY.md`
(260 lines, swarmy collaborator seed) — which is itself NOT a "global
HONEY" but the swarmy project's collaborator-onboarding doc. The
frontmatter source list is loose with naming. Buyer beware.

**2. Every variant preserved "100% of entries" — but they disagreed about what counted as an entry.**
KS treats koans and method IDs as entries (preserves all 78+ mth IDs).
DE treats personas and primer sections as first-class structure.
DA treats confidence tiers as the entry-level unit. HYBRID claims to
preserve all of the above. v3 collapses all of them into a thinner
list of seven principles + thirteen methods — which is *not* 100%
preservation by any of the variant definitions. The frontmatter
claim "All universal principles and methods from source documents
preserved" is true at the *principle/method* level only; the
operational entries (mth00420 spawn cost RED FLAG, mth00432 O(n)
scan regression, mth00408 W-edge halt, ws00001 mission-based bundle
paths, BUZZ skill, FFMx north-star metric, the entire piston tier
table) did NOT survive.

**3. The variants live at two different scopes and v3 silently chose one.**
KS/DE/DA/HYBRID are all *swarmy-internal* variants — they speak
about faerie-specific machinery (FFMx, piston waves, BUZZ, mth00400
range, ws workspace rules, mission-driven dispatch). FEDERATED-HONEY
and the v3 seed are *cross-pod* variants — they speak about HONEY
as a knowledge currency exchanged between independent research pods.
The v3 promotion took the cross-pod framing as the surface shape
("seed concept", "domain tags", "rosetta stone") and dropped almost
all the swarmy-operational content. This is a coherent choice, but
it means swarmy lost its operational HONEY when v3 was promoted —
the canonical HONEY no longer describes f(0), FFMx, piston waves,
or BUZZ. Those live now in CLAUDE.md and skill files. Whether that
split is good or bad is itself an open v4 question (see synthesis
section below).

With those three observations in mind, into the dig.

---

## 1. HONEY-v1-pre-evolution (HONEY-future/archive/HONEY-v1-pre-evolution.md, 388 lines)

### Provenance

- Authored by: federation-crystallizer (variant signature in frontmatter)
- Date created: 2026-05-15 (`last_evolved` in frontmatter)
- Authorial voice: cross-pod federation engineer — explicitly tagged
  `variant: "federation-crystallizer"`, focused on collaboration
  surface and federation protocol. NOT the actual swarmy v1 despite
  its filename.

### Structure

The file has a heavy emphasis on cross-pod onboarding and federation
protocol:

1. Frontmatter declaring `honey_version: 3.0.0` and `federation_ready: true`
2. "START HERE — Who Are You?" persona table (7 rows)
3. Five-Minute Primer (6 paragraphs)
4. Tier 1 — Invariants (5 entries in a table)
5. Tier 2 — Validated Principles (7 pri00### entries)
6. Tier 3 — Active Methods (13 method entries across Navigation,
   Verification, Memory, Architecture)
7. Tier 4 — Experimental (empty, with a promotion-pathway note)
8. Cross-Domain Insight Matrix (24-entry grid)
9. Domain Modules (Agentic / Memory / Research / Software / Safety /
   Orchestration)
10. Cross-Domain Bridges (8-entry table)
11. Rosetta Stone — Domain Translation (7-row glossary across 4 fields)
12. Collaboration Surface — Federation Protocol (3 sections: Individual,
    Team, Federation)
13. Evolution Protocol (entry format, promotion pathway, bearing
    navigation, confidence assessment)
14. Domain Reference (6-row glossary)

The persona table is the dominant navigation device. The cross-domain
matrix is the dominant analytical device. The federation protocol is
the dominant operational device. Three top-level affordances stacked
in one file.

### What this variant does BEST

**a) The "Who Are You?" persona table is the cleanest onboarding device
in the whole corpus.** Seven rows, each with three sequential reading
recommendations. It tells a cold-start reader literally where to look
first. Quoted verbatim:

> | I am... | Start with | Then read |
> |---------|-----------|-----------|
> | **New to HONEY** | Five-Minute Primer (below) → Tier 1 Invariants | Tier 2 Principles → Tier 3 Methods |
> | **Building agents** | Module: Agentic + Tier 3: Navigation | Cross-Domain Bridges → Rosetta Stone |
> | **Managing memory** | Module: Memory + Tier 3: Memory methods | Tier 2: DEBLOBT ≠ CRYSTALLIZE |

This is *prescriptive navigation*. v3 dropped it entirely; v3 tells you
the seed exists but never tells you which 30 lines to read first.

**b) The Cross-Domain Insight Matrix is a measurement device, not just
a pretty grid.** Every entry is annotated with `●` (primary) and `○`
(cross-domain). A reader can scan their column and see at a glance
which entries apply directly vs. apply by analogy. This is the only
variant where "cross-domain" is a typed annotation visible at the
entry level rather than a separate annotation at the bottom.

**c) The Rosetta Stone glossary translates concepts across four
fields (agentic / research / software / biology) in one table.** It
makes "stigmergy" legible to a biologist and "phase gate" legible to a
filmmaker. This is the federation protocol's actual surface: the place
where two pods working in different domains discover their shared
vocabulary.

### What this variant got WRONG (or weakly)

**Tier 4 is empty.** The promotion pathway is well-designed in
principle but unused in practice. A v3 reader sees `Tier 4 — Experimental`
with the note "no entries currently" and has no example to imitate
when they want to propose a hypothesis. Dead UI.

**Federation protocol assumes infrastructure that doesn't exist.**
"5-step comparison protocol", "Emergence score" formula, federation
patterns — all promising, none anchored in any actual implementation.
The variant ships a vocabulary without a tool.

**The domain modules duplicate the method entries.** Every method
shows up once in Tier 3 and again under the relevant Domain Module
section. The duplication is mild (the module sections are summaries,
not full re-prints) but the reader still gets the same names twice
within ten screens of scrolling.

### What v3 absorbed

- The five Tier-1 invariants (I-1 through I-5) — almost verbatim text,
  identical confidence scores, identical domain tags
- The seven Tier-2 principles (pri00001–pri00007) — verbatim
- The 13 Tier-3 methods (mth00101, mth00047, mth00002, mth00004,
  mth00026, mth00035, mth00037, mth00031, mth00010, mth00015, mth00016,
  mth00017, mth00018, mth00019, mth00020, mth00021, mth00022, mth00009)
  — verbatim or near-verbatim
- The Cross-Domain Insight Map (renamed to "Rosetta Stone — Cross-Domain
  Insights")
- The Domain Reference table at the bottom (verbatim)
- The "Seed Protocol — How to Fork and Evolve" section (lightly rephrased)
- The Entry Format definition

### What v3 LOST (worth resurrecting in v4)

- **The "Who Are You?" persona table.** v3 has no onboarding device at
  the head of the file. The first thing a reader sees in v3 is a 30-line
  poetic reflection. Beautiful, but useless to a cold-start agent who
  needs to know *which* section to read.
- **Tier 4 — Experimental.** The promotion pathway (Tier 4 → Tier 3
  → Tier 2 → Tier 1) is explicitly named in the v1-pre-evolution file
  and silently dropped in v3. v3 still has confidence scores on
  entries but no slot for entries below 0.70. There is nowhere in v3
  for a hypothesis to live before it becomes a method.
- **Cross-Domain Insight Matrix as a grid.** v3 has a table of
  cross-domain insights but it lists collaboration opportunities, not
  applicability. The `●/○` grid is gone.
- **Domain Modules as standalone sections.** v3 has a single Domain
  Reference table at the very end. A reader who self-identifies as
  "I'm building agents" has no agentic-module to jump to.
- **The "5-step comparison protocol" for Teams** (Align / Map / Bridge
  / Detect / Synthesize). v3 mentions Rosetta Stone but doesn't give
  the team-level recipe.

---

## 2. HONEY-VARIANT-KS — Knowledge-Synthesizer (HONEY-future/variants/HONEY-VARIANT-KS.md, 805 lines)

### Provenance

- Authored by: knowledge-synthesizer subagent (NAVIGATOR archetype)
- Date created: 2026-05-03T23:30:00Z
- Authorial voice: a synthesizer building a *reference library* for
  future synthesis. The voice is methodical, citation-dense, and
  self-aware about its own optimization tradeoffs ("Not recommended
  for: Fast decision-making under time pressure"). Signed
  `knowledge-synthesizer_001` in the colophon.

### Structure

KS is organized as four overlapping organizational layers stacked on top
of preserved entries:

1. Reading guide explaining the four organizational layers
2. Invariants (table of 6, with archetype-primary tags)
3. The Koans (table of 13 with archetype + cross-koan clusters)
4. The Math — Spawn Decision Framework (decision tree + confidence
   progression)
5. Glossary (sticky reference with archetype + validated columns)
6. Confidence Progression Timeline (HIGH ≥0.90 / MEDIUM 0.80–0.89 /
   EMERGING 0.70–0.79)
7. Method Dependency Graph (ASCII tree across 4 clusters)
8. Archetype-to-Method Routing Map (4 archetype subsections, each
   with method tables)
9. Temporal Validation Windows & Evidence Counts (3 date-windowed
   tables)
10. Core Equations & Thresholds (FFMx, emergence health, qualitative
    depth, spawn leverage, dispatch composition, token budget)
11. Fundamental Principles (sys00001 through sys00034)
12. Synthesis Pathways (Emergence Coherence Cluster, Release
    Readiness Cascade, Mutation Measurement Methodology)
13. Archetype Emergence Validation (W1 LIFTOFF roster table)
14. Workspace Rules (ws00001–ws00004)
15. HONEY Crystallization Schedule (next 30 days)
16. Quick Reference Index (By Confidence Tier / By Archetype / By Domain)
17. Metrics Dashboard
18. Session Cold-Start Checklist
19. Next Steps for System Evolution (mutation candidates)
20. Colophon

### What this variant does BEST

**a) The Method Dependency Graph is the most load-bearing artifact in
the whole corpus.** It draws the ASCII DAG explicitly — which methods
enable which other methods, which have upstream RED FLAGS, what the
critical path is for mutation. Quoted:

> ```
> EMERGENCE FOUNDATION (Stigmergy Core)
> ├─ mth00403 (stigmergic self-organization, 0.95)
> │  └─ enables: mth00404 (compass DAG routing, 0.93)
> │      └─ enables: mth00405 (mission clustering, 0.89)
> │          └─ enables: mth00406/mth00407 (emergence health formula, 0.92)
> ```

Nothing else in the corpus shows the *graph* between methods. KS turns
the HONEY entries from a flat list into a navigable graph. This is a
genuine contribution that no other variant matched.

**b) The Confidence Progression Timeline shows how confidence
*moves over time*.** It explicitly tracks the date-window of each
promotion event:

> **2026-05-01–05-03 (Membench Integration + Mutation Validation):**
> - mth00407 [0.92] Cognitive archetypes drive emergence
> - mth00411 [0.70→0.95] Emergence quality metrics (RAPID RAISE 2026-05-03)
> - mth00421 [0.88→0.92] Spawn leverage threshold

This is the only variant that treats confidence as a *trajectory*
rather than a static label. A reader can see which methods are
recently promoted (and therefore freshest) and which have been stable
for weeks (and therefore most trusted).

**c) The Archetype-to-Method Routing Map binds methods to cognitive
roles.** For each archetype (NAVIGATOR, MAKER, BRIDGE, DEEP-DIVER), KS
lists the specific methods that archetype activates, what role the
archetype plays, and what the development focus should be. This is
how the system actually self-organizes — but only KS makes it visible.

### What this variant got WRONG (or weakly)

**The colophon admits the tradeoff but ships anyway.** "Not recommended
for: Fast decision-making under time pressure (original HONEY.md is
more dense). Use original for operational tempo." KS is a reference
library, not a working file. An agent in W1 LIFTOFF with 2K of context
left cannot afford to read 805 lines. KS solves the synthesizer's
problem and ignores the operator's.

**The Confidence Progression Timeline is already stale on arrival.**
Dated 2026-05-03; the entries are time-windowed at session granularity
(05-01 to 05-03 = "intensive"). By 2026-05-08 the timeline is a
historical artifact. There's no refresh ritual.

**Cross-koan dependency clustering is overengineered.** "Autonomous
discovery cluster", "Dynamical systems cluster", "Honesty + transparency
cluster" — these are interesting taxonomy moves but they don't enable
any agent action. A reader in front of a problem doesn't say "I need a
Koan from the Honesty cluster." They look at what they're doing and
pick the koan that fits.

**The validation windows are tied to one specific project's events.**
The methodology generalizes; the dates do not. KS smashes the two
together such that the file feels obsolete the moment you read it
outside that 3-day window.

### What v3 absorbed

- The koan structure (13 koans, archetype-tagged) was *not* directly
  absorbed into v3 — v3 has no koan section
- The confidence-tier convention (0.70 hypothesis → 0.85 validated → 0.95+
  invariant) was absorbed into v3's promotion-pathway note
- The four-archetype model (NAVIGATOR / MAKER / BRIDGE / DEEP-DIVER)
  was NOT directly absorbed into v3 — v3 never names archetypes
- The "spawn leverage threshold ≥ 10×" idea was NOT absorbed — v3
  doesn't discuss spawn at all
- The emergence health formula was NOT absorbed — v3 doesn't discuss
  emergence at all
- The general idea that methods can be tagged by archetype/domain
  WAS absorbed as the domain tag layer

### What v3 LOST (worth resurrecting in v4)

- **Method dependency graph.** This is the highest-leverage missing
  artifact. v3's entries are a flat list. Without a graph, a reader
  cannot answer "if I change I-2 (BUDGET IS A HEARTBEAT), what other
  entries do I need to re-validate?" KS's ASCII tree gave that
  immediately.
- **Confidence progression timeline.** Static confidence scores are a
  lie of omission. Confidence 0.95 reached yesterday is different
  from confidence 0.95 reached two years ago and held since. v4
  should track date-of-last-promotion and date-of-last-challenge.
- **Cognitive archetype taxonomy.** NAVIGATOR / MAKER / BRIDGE /
  DEEP-DIVER is the only model in the corpus that explicitly maps
  cognitive *style* to operational *bearing* to *emergence component*.
  v3 dropping it leaves a giant hole for any reader trying to compose
  a team.
- **Critical-path-for-changes note.** KS has explicit guidance:
  "If modifying mth00406 (emergence health), must re-validate
  mth00411/mth00412/mth00413." v3 has no impact-analysis affordance.
- **Quick Reference Index (By Confidence Tier / By Archetype /
  By Domain).** v3 has only "By Domain" (and weakly).
- **Session Cold-Start Checklist.** Concrete actionable checklist
  for every session start. v3 has no checklist anywhere.

---

## 3. HONEY-VARIANT-DE — Documentation-Engineer (HONEY-future/variants/HONEY-VARIANT-DE.md, 617 lines)

### Provenance

- Authored by: documentation-engineer subagent (MAKER archetype, per
  cohort assignment in emergence report)
- Date created: 2026-05-03T22:30:00Z
- Authorial voice: a documentation engineer building an *onboarding
  surface*. The voice is friendly, persona-driven, and explicitly
  optimized for "first-time reader navigation and persona-based task
  lookup." The closing line: "All original methods, principles, and
  facts preserved. Structural reorganization optimized for first-time
  reader navigation and persona-based task lookup."

### Structure

DE leads with persona-routing and only reaches the entries after the
reader has been oriented:

1. Three poetic lines as preamble ("The system makes sense if you
   follow the math…")
2. FIND YOUR ROLE table (6 personas: Onboarding / Spawning / Building
   / Debugging / Releasing / Deep learning)
3. FIVE-MINUTE PRIMER (5 numbered facts)
4. INVARIANTS — Read These Every Session (table of 6 with Why column)
5. GLOSSARY (11 terms with symbol + 1-line definition)
6. THE KOANS (13 numbered koans, each one paragraph)
7. THE MATH: Why SPAWN is the Default Decision (decision flow + cost
   table)
8. SPAWN PATTERNS BY BEARING (table of 5: N / S / E / W / Multi)
9. CORE EQUATIONS & THRESHOLDS (FFMx, emergence health, spawn
   leverage, dispatch composition, token budget)
10. FUNDAMENTAL PRINCIPLES (sys00001 through sys00034 in a table)
11. MISSION-DRIVEN DISPATCH (mental model shift table, three layers,
    three questions, manifest contract)
12. COMPASS BEARING DAG (bearing rules + chain legality)
13. EMERGENCE & COGNITIVE ARCHETYPES (4 archetypes + formula)
14. MISSION CLUSTERING FOR PARALLEL SCALING
15. BACKTRACK SIGNAL (W-edge)
16. RELEASE READINESS GATES (6 gates table)
17. SYSTEM METHODS (mth00300 through mth00432 + ws00001–04)
18. SPECIAL SKILL: BUZZ
19. PHASE HISTORY (timeline of recent crystallizations)
20. PHASE 9 — CONTINUAL LEARNING BULLETS
21. ESCAPE HATCHES table (12 troubleshooting questions)
22. NATURE OF THIS WORK (poetic closing)
23. FULL METHOD INDEX

### What this variant does BEST

**a) The Escape Hatches table is the single best UX artifact in the
corpus.** Twelve common questions ("Why is health dropping?", "Agent
seems lost?", "Budget is running out?", "Something feels off?") each
with three prescriptive references (first stop / then see / deep
dive). Quoted:

> | Question | First stop | Then see | Deep dive |
> |----------|-----------|----------|-----------|
> | "Why is health dropping?" | W-edge Signal (mth00408) | Emergence Formula (mth00406) | mth00432 + mth00431 |
> | "Agent seems lost?" | Find Your Role table | Koans | mth00403 (stigmergy) |
> | "Something feels off?" | Koan 12 (Feeling catches logic) | DEEP-DIVER methods | mth00408 + mth00410 |

This is the only place in the corpus where an agent in distress is
given a literal lookup path. No other variant has this. v3 doesn't
have anything like it.

**b) FIND YOUR ROLE persona table is sharper than the v1-pre-evolution
version.** DE adds the "Full context" column and the personas are
operationally framed ("Spawning agents", "Releasing code") rather than
abstractly framed ("Building agents", "Managing memory"). DE knows
who its readers actually are.

**c) The FIVE-MINUTE PRIMER section is genuinely five minutes.**
Five numbered facts, each one sentence + one elaboration. A reader
can be operationally productive after reading 14 lines. Quoted:

> 1. **Spawn is the default** (mth00002, L. 75).
>    If you have 2+ independent tasks >100 tokens each → spawn agents
>    via `spawn.py`, not inline. Cost: ~130 tokens. Benefit: agents
>    work in parallel, return dashboard_lines. You never block.

Compare to v3's opening section, which is a 30-line poetic reflection.
DE knows that onboarding is a different mode from contemplation.

### What this variant got WRONG (or weakly)

**The persona table lacks bearing constraints.** The emergence report
flagged this as the critical gap: "Persona table lacks bearing
constraint inheritance. Personas are routed to agent types but don't
show which bearings are legal in which phase." The HYBRID variant
later fixed this by adding a Bearing Constraints column. DE shipped
without it.

**Section ordering doesn't match persona ordering.** The persona
"Releasing code" routes to "Release Readiness Gates" — which is
section 16 of 23. Following the persona prescription requires a long
scroll. DE could have laid out the file in persona-order rather than
topic-order.

**The Escape Hatches references use line numbers ("L. 65", "L. 108")
that drift the moment the file is edited.** A line-number reference
is a stale pointer waiting to happen.

**Phase 9 — Continual Learning Bullets only has three entries, all
from 2026-05-03.** It's the same problem KS has with the validation
timeline: the section is dated, has no refresh ritual, and stales
fast.

### What v3 absorbed

- The poetic preamble ("Two kinds of intelligence…") — verbatim
- The cross-domain mention of "spawning agents" as a use case —
  abstracted into the seed-protocol section
- The general persona-driven framing — v3 has the very-similar
  domain table at the end but lost the entry-level routing
- The koans were NOT absorbed into v3 (huge loss)
- The bearing matrix (N/S/E/W) was NOT absorbed into v3 (huge loss)
- The Five-Minute Primer was NOT absorbed
- The Escape Hatches were NOT absorbed
- The BUZZ skill was NOT absorbed

### What v3 LOST (worth resurrecting in v4)

- **Escape Hatches.** This is the highest-priority resurrection
  candidate from DE. A 12-row troubleshooting table answers more
  reader questions than any other artifact in the corpus.
- **FIVE-MINUTE PRIMER.** A reader needs to be operationally productive
  in five minutes, not contemplative for thirty. v3 has nothing in
  this slot.
- **FIND YOUR ROLE persona table.** Different framing from
  v1-pre-evolution (operational rather than abstract); equally useful.
- **KOANS.** v3 dropped all thirteen koans. The koans are the
  *spirit* of the system — "The Trail That Knows Itself", "The Queen
  Who Reads, Not Writes". A v3 reader gets the seed concept but not
  the worldview behind it.
- **PHASE HISTORY / PHASE 9 bullets.** The continual-learning slot. v3
  has no "what changed recently" section. A reader who comes back after
  two weeks has no way to see what's new.
- **BUZZ skill reference.** The "queen reorientation" skill is named
  and described in DE. v3 has no slot for skill cross-references.
- **MISSION-DRIVEN DISPATCH / COMPASS BEARING DAG sections.** v3
  doesn't mention missions or bearings at all. This is a coherent
  choice (v3 is pod-external, mission is pod-internal) but means
  v3 cannot orient a swarmy-internal agent.

---

## 4. HONEY-VARIANT-DA — Data-Analyst (HONEY-future/variants/HONEY-VARIANT-DA.md, 582 lines)

### Provenance

- Authored by: data-analyst subagent (DEEP-DIVER archetype, per
  cohort assignment)
- Date created: 2026-05-03T22:00:00Z
- Authorial voice: a metrics-forward analyst building a *cost-conscious
  operational filter*. The voice is annotation-dense, scenario-driven,
  and explicitly optimized for sub-5K context budgets. Closes with
  "Generated: 2026-05-03 by data-analyst-role-optimization charter."

### Structure

DA's organizing principle is *tier annotation* — every entry carries
explicit cost-conscious metadata:

1. Variant marker key (`[HIGH-PRIORITY]`, `[MID-TIER]`,
   `[ADVANCED/SYSTEM]`, `[DA-SPECIFIC]`, `[CONFIDENCE]`,
   `[USAGE-FREQ]`, `[APPLIES-TO]`)
2. Quick Ref — High-Priority Methods table (the 80/20 toolkit)
3. INVARIANTS table (with Usage % column)
4. THE KOANS (subset table with DA-relevance column)
5. THE MATH: Why SPAWN is the Default (with DA-context column)
6. Glossary (with DA-relevance column)
7. Spawn Patterns by Bearing (with DA-examples column)
8. Core Equations & Thresholds for Data Analysts
9. High-Priority Methods for Data Analysts — Tier 1 (Universal,
   High-Confidence)
10. Tier 2 — Multi-Task Coordination (Mid-Confidence)
11. Tier 3 — Advanced/System Methods
12. Mid-Tier Methods (Scenario-Specific)
13. System Methods (Advanced/System)
14. Workspace Rules (DA-Specific Application)
15. BUZZ — Queen Bee Drift Detector
16. Phase 9 — Continual Learning
17. Appendix: Confidence Tier Definitions
18. Appendix: Audience Level Definitions
19. How to Use This Variant (4 scenarios at increasing context budgets)

### What this variant does BEST

**a) The explicit tier-load model is the only variant that treats
context budget as a first-class input to the reading order.** Quoted
from the "How to Use This Variant" section:

> **Scenario 1: Cold start, context <2K, need to spawn immediately**
> 1. Read: INVARIANTS (all) + HIGH-PRIORITY methods (Tier 1)
> 2. Decision: 2+ tasks + mission known? → Spawn W1 team via mth00032 + mth00073 + mth00074.
> 3. Load: HONEY-VARIANT-DA only (skip global HONEY.md until synthesis phase).
> 4. Time: ~5 min total; context used ~200 tokens.

This treats HONEY as a *progressive disclosure* device, not a flat
document. Different agents at different budgets read different slices
of the same file. KS gestures at this; DA actually wires it.

**b) Usage frequency annotation (`[USAGE-FREQ]` 100%, 95%, 80%, 50%, 5%)
turns abstract priority into measurable priority.** A reader can
literally count: which 30% of methods solve 80% of the missions? DA
answers that empirically.

**c) The RED FLAG override is the only place in the corpus where the
*falsifiability* of a confidence score is explicit.** Quoted:

> **RED FLAG override:** Confidence 0.65 marked RED if forensic actuals
> contradict estimates (see mth00420). RED FLAG = use as planning floor
> only, not measured fact.

mth00420 is shown specifically: "Spawn cost formula (0.65 confidence,
estimated baseline). Design: ~60 tok/agent. Forensic actuals show
15–562 tok/agent (182% drift). Formula needs recalibration." DA names
the broken thing explicitly. No other variant does that.

**d) Brittleness visibility as a measured property.** From the
comparison file: "Brittleness visibility | Not measured | 0.28 | <0.40".
DA introduces the concept that some assumptions can be *measured to
be brittle* (high estimate drift = fragile), and treats brittleness
as a release-gate criterion (target <0.40).

### What this variant got WRONG (or weakly)

**Heavy bias toward one archetype (data-analyst).** The variant is
explicit about this — "[DA-SPECIFIC]" tags mark sections only
data-analysts need. But the bias bleeds into the framing of *every*
method ("DA context: irrelevant unless building custom bundle templates
for data-analytics workflows"). A non-DA reader feels the friction.

**Three appendices at the end is two too many.** "Appendix: Confidence
Tier Definitions" + "Appendix: Audience Level Definitions" + "How to
Use This Variant" — these are all definitional and could fold into
the introduction. The reader has to scroll to the end to find what a
`[HIGH-PRIORITY]` tag means.

**Method discovery savings are claimed but not benchmarked
fairly.** "DA's method ranking saves 300-400 tokens per mission" —
but the comparison is against an *unranked* read of the original
HONEY. If the original HONEY were re-ordered (KS style) or persona-routed
(DE style), the savings shrink. DA's own emergence report acknowledges
this implicitly when it scores all three variants at 0.85–0.89 health.

### What v3 absorbed

- The confidence tier convention (HIGH ≥0.85, MEDIUM 0.65–0.85, LOW <0.65)
  was absorbed conceptually but not as a literal annotation system —
  v3 puts numeric confidence inline (e.g. "0.97") not tier label
- The progressive-disclosure idea ("read X tier first if budget Y")
  was NOT absorbed
- The RED FLAG override convention was NOT absorbed — v3 has no
  flag system
- The usage-frequency annotation was NOT absorbed
- The "How to Use This Variant" scenario walkthrough was NOT absorbed

### What v3 LOST (worth resurrecting in v4)

- **Progressive disclosure by context budget.** v4 should ship with
  an explicit "if budget < 2K read these 10 entries; if budget < 5K
  add these 20; if unlimited read everything" affordance.
- **RED FLAG override.** When forensic actuals contradict the
  estimate, the confidence label should *visibly* mark the entry as
  suspect, not silently keep the number. v4 should adopt this convention.
- **Usage frequency annotation.** Not every entry is used equally
  often. The 80/20 cut is real and worth surfacing.
- **Brittleness as a measured property.** A scored entry can still
  be brittle if its dependencies are unstable. v4 should track
  brittleness alongside confidence.
- **Scenario walkthroughs at the end.** "How to use this variant"
  with 4 scenarios is the documentation pattern that turns
  *understanding* into *action*.

---

## 5. HONEY-VARIANT-HYBRID — Hand-Curated Synthesis (HONEY-future/variants/HONEY-VARIANT-HYBRID.md, 856 lines)

### Provenance

- Authored by: knowledge-synthesizer_001 (the same agent who wrote KS,
  iterated on it after reading DE and DA)
- Date created: 2026-05-03T23:45:00Z (forty-five minutes after KS;
  fifteen minutes after the emergence report concluded)
- Authorial voice: a deliberate synthesizer composing the *best of
  all three* variants while preserving entries. The intro is explicit
  about the assembly: "DE skeleton (personas + Five-Minute Primer +
  Escape Hatches) + KS method dependency chains + DA confidence tiers
  + NEW bearing_constraints column."

### Structure

HYBRID is essentially DE's skeleton with KS's dependency graph + DA's
confidence tiers + a new bearing_constraints column on the persona
table. Sections in order:

1. FIND YOUR ROLE table (DE persona structure + new
   bearing_constraints column)
2. FIVE-MINUTE PRIMER (DE)
3. CONFIDENCE TIERS LEGEND (DA)
4. METHOD PRIORITY INDEX (DA-style table with KS dependency-chain
   summaries)
5. INVARIANTS (with bearing constraint column)
6. GLOSSARY (with confidence column)
7. THE KOANS (DE-style + cross-koan clusters from KS)
8. THE MATH (DE + dependency chain at the bottom from KS)
9. SPAWN PATTERNS BY BEARING (with bearing constraints from HYBRID's
   own new contribution)
10. CORE EQUATIONS (FFMx, M7, f(0), emergence health, qualitative
    depth, spawn leverage, dispatch composition, token budget)
11. FUNDAMENTAL PRINCIPLES (sys00001–sys00034)
12. MISSION-DRIVEN DISPATCH
13. METHOD DEPENDENCY GRAPH (KS's full ASCII tree, verbatim)
14. ARCHETYPE-TO-METHOD ROUTING MAP (KS's structure, abridged)
15. SYSTEM METHODS — Bundle Crystallization (DE-style entries + KS
    dependency annotations)
16. SYSTEM METHODS — Emergence & Mission Graph (dependency chain
    notation)
17. SYSTEM METHODS — Faerie2 Release
18. SYSTEM METHODS — Emergence Quality Metrics
19. SYSTEM METHODS — Crystallization
20. SYSTEM METHODS — Advanced Metrics
21. WORKSPACE RULES
22. BUZZ
23. COLLABORATION PREFERENCES (Abridged)
24. FAERIE DESIGN PHILOSOPHY (Sampled)
25. METHODS — INVESTIGATION + OPERATIONAL DOMAIN (mth00002–mth00099,
    listed)
26. PHASE HISTORY
27. PHASE 9 — CONTINUAL LEARNING BULLETS
28. NATURE OF THIS WORK
29. SESSION COLD-START CHECKLIST
30. ESCAPE HATCHES
31. FULL METHOD INDEX (By Confidence Tier / By Archetype / By
    Dependency Chain)
32. VARIANT METRICS SUMMARY

### What this variant does BEST

**a) The bearing_constraints column on the persona table is HYBRID's
own contribution, and it closes the gap the emergence report flagged.**
Quoted:

> | I am... | Start with | ... | Bearing constraints |
> |---------|-----------|-----|---------------------|
> | **Spawning agents** | The Math: SPAWN Decision | ... | Dominant bearing on frontier → use matching team |
> | **Debugging failure** | Backtrack Signal W-edge (mth00408) | ... | W-edge legal; S blocked until W resolves (mth00422) |
> | **Releasing code** | Release Readiness Gates (mth00413) | ... | S-bearing only; N/W illegal after gate sequence begins |

This is operational doctrine in table form. A reader who self-identifies
as "Releasing code" learns immediately that N/W are illegal in their
phase. No other variant tells them that.

**b) Composition is the win.** HYBRID demonstrates that the three
variants are *complementary*, not competitive. The persona table
(DE) + the dependency graph (KS) + the confidence tiers (DA) + the
new bearing constraints (HYBRID) all fit in one file without
conflict. Each reader finds their layer.

**c) Variant Metrics Summary at the end is honest about its own
quality.** "Emergence health estimate: 0.88+ | Achieved: 0.88 | DE
structure (0.89) + bearing constraint fix (+0.01) balanced by DA
operational safety". HYBRID grades itself with the same metric used
on the source variants. Most variants don't self-score.

### What this variant got WRONG (or weakly)

**856 lines is too many.** HYBRID is the longest of all four
variants. The premise of "composition" assumed the layers were
non-overlapping; in practice some duplication slipped through (e.g.
the koans appear in DE form, then are re-described in cluster form
in the next section).

**Section 25 ("Methods — Investigation + Operational Domain (mth00002
through mth00099)") is a placeholder bullet list, not actual
entries.** HYBRID claims 78 entries preserved but renders them as a
single paragraph of comma-separated IDs. A reader who wants to look
up mth00073 won't find its text in HYBRID; they have to go back to
the original. So the "preservation" claim is structurally true (the
IDs are listed) but operationally false (the text is missing).

**Dual-mth00411 collision is acknowledged but not resolved.** "Also
referenced as quality metrics entry (see below — dual-mth00411 note
in original HONEY preserved)." Two different methods with the same ID
existed in v2; HYBRID preserves the collision rather than fixing it.

**The composition was hand-curated by one synthesizer in one session.**
There's no validation that the chosen mix is the *optimal* mix; HYBRID
is one local optimum out of many possible compositions. The emergence
report scored HYBRID at 0.88 vs DE alone at 0.89 — HYBRID is not
strictly the best.

### What v3 absorbed

- Almost nothing structurally. HYBRID's win is composition, and v3 made
  a different composition choice (cross-pod federation framing rather
  than swarmy-operational framing). The pieces HYBRID composed (persona
  table + dependency graph + confidence tiers + bearing constraints)
  ALL got dropped.
- The "Variant Metrics Summary" self-scoring habit was NOT picked up
  by v3.

### What v3 LOST (worth resurrecting in v4)

- **The bearing_constraints column on the persona table.** This is
  HYBRID's unique contribution. v4 should pick it up if v4 keeps a
  persona table at all.
- **Cluster annotation on the dependency graph.** HYBRID rendered KS's
  dependency tree with section labels ("EMERGENCE FOUNDATION", "RELEASE
  READINESS", "OPERATIONAL DISCIPLINE", "BUNDLE SYSTEM"). The grouping
  is informative.
- **Self-scoring discipline.** HYBRID grades its own emergence health
  at the bottom. v4 should ship with explicit self-grades on each
  measurable property.

---

## 6. HONEY-VARIANT-COMPARISON (HONEY-future/variants/HONEY-VARIANT-COMPARISON.md, 83 lines)

### Provenance

- Authored by: not attributed in frontmatter; the file has no YAML
  frontmatter at all. Voice + content suggests the data-analyst variant
  (DA) — the file's stated purpose is "Visual comparison of original
  HONEY.md (generic) vs. HONEY-VARIANT-DA (data-analyst optimized)."
- Date created: not stated; file mtime 2026-05-15
- Authorial voice: analytical. Six small tables stacked. Comparison
  is DA-vs-original, NOT a three-way KS/DE/DA comparison (despite
  the filename suggesting otherwise).

### Structure

Six tables + a "Bottom Line" section:

1. Feature Comparison (9 rows: total methods, koans, invariants,
   total tokens, structure, confidence tiers, usage frequency, bearing
   applicability, audience segmentation)
2. Context Recovery Impact (3 scenarios: cold-start <1K, mid-mission
   1–3K, complex >4K)
3. Measurement Layer (NEW in DA): confidence stratification, usage
   frequency, bearing applicability, brittleness visibility, citation
   density
4. Audience Segmentation table (5 audiences: entry-level / mid-level /
   advanced DA / system engineer / non-DA)
5. Quality Metrics (5 rows: prioritization clarity, confidence
   transparency, citation coherence, brittleness visibility,
   downstream impact)
6. Bottom Line (DA wins 0/0/0 against original)

### What this variant does BEST

**a) "Context Recovery Impact" is the cleanest economic argument in
the corpus.** Quoted:

> | Scenario | HONEY.md | HONEY-VARIANT-DA | Savings |
> |----------|----------|------------------|---------|
> | **Cold-start (<1K context)** | 8.5K impossible to load | 2.2K Tier 1 | 6.3K recovered |
> | **Mid-mission (1–3K context)** | 8.5K over budget | 4.2K Tiers 1–2 | 4.3K recovered |
> | **Complex mission (>4K context)** | 8.5K loaded | 9.8K all tiers | -1.3K (acceptable trade) |

This is the only place in the corpus that says explicitly: at context
budget X, this file is *unloadable* — and quantifies the recovery from
a tiered design.

**b) The Quality Metrics table is a falsifiable scorecard, not a
narrative.** 0.40 → 0.96 prioritization clarity, 0.20 → 1.0 confidence
transparency, etc. Real numbers, target thresholds, before-vs-after
comparison.

### What this variant got WRONG (or weakly)

**The filename ("VARIANT-COMPARISON") promises a three-way comparison;
the content delivers a two-way comparison.** A reader looking for
KS-vs-DE-vs-DA finds only DA-vs-original. The actual three-way
comparison lives in the emergence-report file, not here.

**No frontmatter, no author attribution, no provenance.** The file
floats unanchored in the corpus. A future archeologist (me) had to
infer authorship from voice + content. v4 should require frontmatter
on every artifact.

**Numbers are presented without methodology.** "Prioritization clarity
0.96" — how is that measured? "Brittleness visibility 0.28" — what's
the metric? The numbers feel authoritative but the measurement
procedure is invisible.

### What v3 absorbed

- Nothing structural. The comparison file is not cited by v3 (despite
  being in the source-documents list in v3's frontmatter — which I
  read as "all nine files were consulted" rather than "all nine files
  influenced output").

### What v3 LOST (worth resurrecting in v4)

- **The "Context Recovery Impact" framing — token cost as a function
  of budget tier.** v4 should ship with an explicit token-cost-by-tier
  table at the top.
- **Falsifiable quality metrics with targets.** "Confidence transparency
  ≥0.90" — v4 should ship with explicit self-grades against published
  target thresholds.

---

## 7. FEDERATED-HONEY-ARCHITECTURE (HONEY-future/archive/FEDERATED-HONEY-ARCHITECTURE.md, 511 lines)

### Provenance

- Authored by: knowledge-synthesizer (per frontmatter `author:
  knowledge-synthesizer`, `status: final`, `type:
  architecture-blueprint`)
- Date created: 2026-04-06T12:00:00Z (over a month before the
  variant cycle)
- Authorial voice: an architect drafting a *protocol specification*.
  The voice is RFC-like: phased roadmap, attack model, governance
  section, appendices.

### Structure

Seven major parts + two appendices:

1. Executive Summary
2. Part 1: Current Equilibrium Analysis (energy flow, bottlenecks,
   pressure points)
3. Part 2: Federated Pod Model (pod structure, example network,
   HONEY-as-currency)
4. Part 3: Three-Layer Reference Architecture (pod-internal, HONEY
   export, cross-pod references)
5. Part 4: Implementation Roadmap (4 phases)
6. Part 5: Trust and Incentives (trust architecture, attack model,
   incentives, governance)
7. Part 6: Protocol Specifications (entry ID spec, MEM block syntax,
   federated cache structure, scripts)
8. Part 7: Migration Path (solo → federated)
9. Appendix A: Glossary
10. Appendix B: Related Documents

### What this variant does BEST

**a) Treats HONEY as a *knowledge currency*, not a memory file.**
The economic-properties table is the single most ambitious framing
move in the corpus:

> | Currency Property | HONEY Equivalent |
> |-------------------|------------------|
> | **Portable** | Text format, small size (< 5K tokens per pod) |
> | **Verifiable** | SHA-256 hash, source traceability to NECTAR + forensic COC |
> | **Scarce** | Gauntlet (3+ sessions, multi-agent validation, human review, proven impact) |
> | **Denominated** | Confidence score (0.0-1.0), TTL, category |
> | **Fungible** | Standardized format: `[id | type | ttl | confidence] entry` |

This framing is what made v3 possible at all. Without "HONEY as
currency", there's no "fork the seed" concept, no cross-domain
applicability, no Rosetta Stone.

**b) The Trust Architecture section names the verification levels
explicitly (shallow / medium / deep).** A consuming pod can choose
how much to verify based on context. This is a concrete, implementable
trust model — not just hand-waving about "signed manifests."

**c) The Attack Model table is the only place in the corpus where
adversarial behavior is taken seriously.** False HONEY, backdating,
historical-modification, compromised keys, Sybil attacks — each one
with detection mechanism and mitigation. This is *security thinking*
that the operational variants never reach.

**d) The Migration Path (Part 7) is gentle.** "Nothing, unless they
opt in. The federated layer is additive." A coherent backwards-
compatibility story.

### What this variant got WRONG (or weakly)

**The implementation roadmap is aspirational.** Phase 1 (HONEY entry
versioning + export format) is the simplest of the four phases and
still hasn't shipped as of 2026-05-22 (i.e. a month and a half later).
The federation protocol exists as architecture, not as code.

**The "Example Research Network" assumes three peers that don't
exist.** Pod B (Supply-Chain Risk Analysis), Pod C (Regulatory
Capture Investigation) — these are hypothetical. The cybertemplate
pod exists; the others are illustrations. Federation needs at least
two pods to mean anything.

**IPFS + OpenTimestamp dependency is heavy.** The trust model leans on
infrastructure that needs to be installed, configured, paid for
(Pinata pinning). For solo researchers this is friction.

### What v3 absorbed

- The "seed" framing — HONEY-as-knowledge-currency that can be forked
  and re-tagged
- The cross-pod verification idea (cryptographic + forensic +
  procedural)
- The entry-ID format with pod prefix is mentioned in v3's "Seed
  Protocol — How to Fork and Evolve" section, though without the
  `{pod_id}:{entry_id}` namespacing
- The general "domains tagged" idea
- The forking + tagging + scoring evolution model

### What v3 LOST (worth resurrecting in v4)

- **The Trust Architecture (shallow / medium / deep verification
  levels).** v3 says nothing about how to trust another pod's HONEY.
- **The Attack Model.** v3 has no adversarial thinking.
- **The phased Implementation Roadmap.** v3 is "a seed" — no roadmap,
  no phase plan. A v4 that wants federation to actually happen needs
  to commit to Phase 1 timeline.
- **The pod registry concept.** Cross-pod references need a
  mapping from pod_id to public key + IPFS gateway. v3 has no
  registry concept.
- **The OpenTimestamp + IPFS protocol details.** Without these, "the
  seed concept" is just narrative.
- **The migration path / backward compatibility story.** v3 doesn't
  explain how a swarmy v1 user transitions to v3 without losing
  their operational machinery.

---

## 8. HONEY-collab-seed / archive/context/HONEY.md (260 lines)

### Provenance

- Authored by: not directly attributed; voice and content suggest the
  swarmy project's original founder-author working with Claude. The
  frontmatter is absent; the file opens "# swarmy — Meta-Agent
  Orchestration (Collaborator Seed)".
- Date created: file mtime 2026-05-21, but the content references
  "Persistech/faerie" rebrand which predates the swarmy rename — so
  the document was written earlier and re-edited or copied to
  archive/context/ on 2026-05-21.
- Authorial voice: a project lead onboarding a new collaborator. Less
  systems-philosophy, more "here's the runbook." The tone is friendlier
  than any other file in the corpus.

### Structure

Plain-text Markdown sections, no frontmatter:

1. "What swarmy Is" (2-line elevator pitch)
2. Session Commands (5-row table)
3. The Memory Flow (Session 1 / Session 2 / Whenever)
4. HONEY.md Rules (6 bullets)
5. NECTAR.md Rules (5 bullets)
6. Two Operational Modes (Orchestrated / Manual)
7. Vault (Obsidian, optional async)
8. Agent Routing (5 core types)
9. Subagent Categories (7 complementary teams)
10. Environment (macOS/Linux specifics)
11. Key Files & Locations
12. Customization: Investigation-Specific HONEY
13. First-Time Setup (shell commands)
14. Integration with DAE
15. Arc: Session → Memory → Training (ASCII flow)
16. Rules (6 essentials)
17. Documentation Map
18. macOS/Linux Specific

### What this variant does BEST

**a) The two-line elevator pitch is the cleanest description of swarmy
anywhere in the corpus.** Quoted:

> **faerie** — meta-agent orchestration system for Claude CLI.
> Coordinates specialized subagents (data-engineer, evidence-curator,
> researcher, writer, publisher) on complex multi-phase tasks.
> Self-correcting: learns from failures, improves agent routing,
> tightens feedback loops.

Notice it says "faerie" not "swarmy" — the file predates the rename.
But the structure of the description (what it is + who it coordinates
+ what's special about it) is exactly what a new collaborator needs.

**b) The Memory Flow section is the only place where the
session-by-session ritual is rendered as a literal narrative
(Session 1 / Session 2 / Whenever).** Quoted:

> **Session 1:**
> 1. `claude` → `/faerie` loads `HONEY.md` (prefs, methods, facts)
> 2. Do work → write observations to `.claude/memory/scratch-{SESSION_ID}.md`
> 3. `/handoff` → promote scratch → `~/.claude/memory/NECTAR.md`
>
> **Session 2:**
> 1. `claude` → HONEY.md + NECTAR.md tail-30 loaded automatically
> 2. Do more work → observations appended to scratch
> 3. `/handoff` → findings appended to NECTAR.md

A reader walks away knowing how to *run* the system, not just how to
read about it.

**c) The "Arc: Session → Memory → Training" ASCII diagram is the
single most useful visual in the corpus.** It shows the full feedback
loop in 12 lines:

> ```
> User task
>   ↓ /faerie
> Context roundup + queue
>   ↓ /run
> Agent team spawns
>   ↓ agents work
> Scratch memory written
>   ↓ /handoff
> Scratch promoted → NECTAR.md
>   ↓ faerie/membot
> performance-eval scores output
>   ↓ if beat-last
> Agent card updated (Last Training)
>   ↓ next session /faerie
> HONEY.md loaded (includes agent updates)
> ```

This is the self-correcting loop made visible. No other file in the
corpus has this diagram.

### What this variant got WRONG (or weakly)

**It calls itself HONEY.md but isn't HONEY.** This is a project
collaborator seed — a runbook, not a crystallized memory file. It
shows up in the v3 source list as "HONEY-collab-seed.md (archive/context/HONEY.md, 260 lines)"
but it has none of the principle/method/invariant entries the other
files share. It's a category error.

**Stale references.** "Persistech/faerie" is the pre-rename name. "DAE"
(data-analysis-engine) references an external project. Some scripts
referenced (e.g. setup-collab.py) may not exist anymore. A new
collaborator reading this in May 2026 might run commands that don't
work.

**No frontmatter.** Same problem as the COMPARISON file. Provenance
is invisible.

### What v3 absorbed

- Nothing structurally. The collab-seed and v3 are different *kinds*
  of documents (runbook vs. crystallized seed).
- The "memory flow" idea (scratch → NECTAR → HONEY) is alluded to in
  v3's seed protocol section but without the ritual narrative.

### What v3 LOST (worth resurrecting in v4)

- **The Memory Flow narrative.** Session 1 / Session 2 / Whenever as
  a literal walkthrough. v3 explains *what* HONEY is but not *how* it
  fits into the daily rhythm.
- **The Arc: Session → Memory → Training ASCII diagram.** The
  self-correcting loop deserves to live in v4.
- **The agent-routing table.** Five core agent types with example
  tasks. A new collaborator learns the cast of characters in five
  rows.
- **The first-time-setup shell commands.** v3 says "fork this file" but
  doesn't show the command. A copy-paste-ready setup ritual is missing.
- **The runbook *posture*.** v3 is contemplative; the collab-seed is
  operational. v4 could have a runbook *section* without losing its
  contemplative seed-section.

---

## 9. emergence-report-honey-variants-final (HONEY-future/archive/emergence-report-honey-variants-final.md, 277 lines)

### Provenance

- Authored by: not directly attributed in frontmatter; the report
  format suggests a synthesizing agent (likely BRIDGE archetype)
  composing the three-way variant comparison. The "Decision
  Confidence: 0.91" at the bottom is the report-author's self-rating.
- Date created: 2026-05-03T23:30:00Z (right after KS, before HYBRID)
- Authorial voice: a referee scoring a competitive evaluation. The
  voice is comparative, quantitative, recommendation-driven. Closes
  with "Next Action: Fix DE bearing constraints gap + promote to
  production."

### Structure

Nine parts ending in a recommendation:

1. Executive Summary
2. Part 1: Baseline Emergence Metrics (KS / DE / DA single-archetype
   tests)
3. Part 2: Cross-Archetype Coordination Emergence (KS / DE / DA cohort
   tests, NAVIGATOR + MAKER + BRIDGE)
4. Part 3: Bearing Constraint Inheritance & Protocol Quality
   (comparison table)
5. Part 4: Token Efficiency & Operational Safety (discovery cost
   model)
6. Part 5: HONEY Promotion Candidates (mth00433, mth00434,
   mth00407-variant, persona-bearing-inheritance)
7. Part 6: Variant Comparison Matrix (Summary)
8. Part 7: Emergence Health Scoring (formula + variant scores)
9. Part 8: Winner Determination (weighted scoring → DE wins)
10. Part 9: Recommendation & Implementation Path

### What this variant does BEST

**a) The Winner Determination matrix is honest about its weighting.**
Quoted:

> | Criterion | Weight | KS | DE | DA | Winner |
> |-----------|--------|----|----|-----|--------|
> | Emergence health | 0.40 | 0.87 | 0.89 ✅ | 0.85 | **DE** |
> | FFMx (cost/discovery) | 0.35 | 2.1 | 2.2 | 2.5 ✅ | **DA** |
> | Constraint clarity | 0.25 | 0.70 | 0.80 ✅ | 0.75 | **DE** |
> | **Weighted Score** | 1.00 | 0.848 | **0.871** ✅ | 0.852 | **DE** |

The weights are stated up front. DE wins on overall weighted score
but DA wins on FFMx cost-per-discovery. The report shows the math
rather than declaring a winner.

**b) The "System Improvements Discovered" table closes the loop.**
Each variant's gap is named, with a fix and a priority:

> | System Gap | Variant Root Cause | Fix | Priority |
> | Persona bearing inheritance missing | DE-NAVIGATOR identified | Add bearing_constraints to Find Your Role | P1 |
> | Budget exhaustion silent failures | DA highlighted via BudgetLedger | Wire W-ratio halt + budget guards | P1 |
> | Method discovery unranked | DA-NAVIGATOR measured 300-400 token savings | Add confidence tiers to HONEY | P2 |
> | Dependency graph not mechanized | KS-NAVIGATOR showed value | Promote mth00407 (archetype weighting) | P2 |

This is the report doing what it was supposed to do: turn the
competitive evaluation into actionable fixes.

**c) Owns its arithmetic uncertainty.** In Part 7 the author starts
to recalculate the emergence formula, notices the numbers don't match
the manifest-reported scores, and explicitly says so: "wait, this
doesn't match. Let me recalculate using mth00407 formula from prior
manifests. Actually, I should cite the measured values from the
manifests themselves rather than recalculating." That candor is rare
in the corpus.

### What this variant got WRONG (or weakly)

**Conclusion is "promote DE", but v3 didn't follow the recommendation.**
The report says "Deploy HONEY-VARIANT-DE.md to ~/.claude/HONEY.md
(primary read)". v3 is not DE-with-fix; v3 is a different file
entirely (the federation-style seed). The report's recommendation
was overruled.

**Cohort tests had only 9 manifests across 3 variants — n=3 per
variant.** Statistical claims like "emergence health 0.87" with n=3
are weak. The report acknowledges this implicitly by hedging language
("emergence health estimate") but the numbers are still presented
with apparent precision.

**FFMx scoring is opaque.** "FFMx (cost/discovery) | 2.1 | 2.2 | 2.5"
— where do those numbers come from? The report says "DA's method
ranking saves 300-400 tokens per mission" but doesn't show the
arithmetic from token savings to FFMx of 2.5.

**The decision framework picks one weighted-average winner and
ignores the composition possibility.** HYBRID later showed that the
three variants are *compositional* — DE skeleton + KS dependency
graph + DA tiers + new bearing constraints. The report scored variants
individually and concluded DE wins, but HYBRID's emergence health
(0.88) is in the same neighborhood with substantially more content.

### What v3 absorbed

- Nothing structurally. The report's recommendation (promote DE +
  wire DA's cost model + preserve KS) was *not* followed when v3
  was promoted.
- The general idea that variants can be scored is implicit in v3's
  source-document list ("9 source documents... competitive variant
  testing") but no scoring artifact is in v3.

### What v3 LOST (worth resurrecting in v4)

- **The Winner Determination matrix with explicit weights.** v4 should
  ship with a self-scorecard showing how it grades against criteria
  (emergence health, FFMx, constraint clarity, etc.).
- **The System Improvements Discovered table.** v4 should preserve a
  running list of gaps surfaced by competitive evaluation, with fix
  priority.
- **The cohort-test methodology.** Cross-archetype coordination
  testing (NAVIGATOR + MAKER + BRIDGE on the same task across three
  variants) is a real evaluation procedure. v4 could ship with a
  charter to run this test periodically.
- **The honest arithmetic uncertainty.** The "wait, this doesn't
  match" moment is a discipline v4 should preserve — show your work,
  show your doubts.

---

## Cross-variant synthesis: what we know now

### The four design moves that survived

After reading all nine source documents and the v3 promotion, four
design moves clearly made it into v3 and are foundational to its
identity:

**1. Confidence-scored entries with explicit metadata.**
Every entry in v3 carries `[id | type | ttl | confidence]` plus
domain tags. Pioneered by the swarmy collaborator seed (entry format
spec), formalized by FEDERATED-HONEY (entry ID spec), tier-annotated
by DA (HIGH/MEDIUM/LOW), and ultimately preserved as inline `[pri00001 |
principle | permanent | 1.0]` markers in v3. This is the durable
substrate.

**2. Domain tagging as cross-pod surface.**
Every entry tagged with `[agentic, software, memory, ...]`. Pioneered
by FEDERATED-HONEY (cross-pod knowledge exchange), realized in v3's
Domain Reference table at the end. Domain tags are how a fork knows
which entries apply to its work.

**3. Invariants as a separate top-tier.**
The v1-pre-evolution file's four-tier model (Invariants / Principles /
Methods / Experimental) collapsed in v3 into three (Invariants /
Principles / Methods) but the *separation* — load-bearing rules at
the top — survived. This is the structure that lets a reader trust
the file at glance.

**4. The cross-domain Rosetta Stone.**
v3 has a "Rosetta Stone — Cross-Domain Insights" section that maps
entries across fields. Pioneered by FEDERATED-HONEY (domain
translation table) + v1-pre-evolution (Rosetta Stone Domain
Translation across agentic/research/software/biology). Surfaces the
highest-value collaboration points.

### The three experiments that didn't ship but should

These three ideas pushed for inclusion in v3, came close, and got
dropped in the synthesis. They are the strongest v4 resurrection
candidates:

**1. Persona-driven onboarding (FIND YOUR ROLE table).**
Pioneered by v1-pre-evolution, refined by DE, augmented with
bearing_constraints by HYBRID. v3 has nothing in this slot — no
persona table, no "where to start" affordance, no operational vs.
contemplative split. A cold-start agent in v3 reads a 30-line poetic
reflection and then has to figure out the rest on their own.

Why v3 dropped it: v3 chose the cross-pod federation framing as its
surface, and the cross-pod framing has only one kind of reader (a
new pod forking the seed). Personas are an *intra-pod* affordance.

How v4 could integrate it: add a persona table at the head of v3,
keeping the poetic reflection as the *second* section. The personas
can be cross-pod-aware ("I am forking this seed for a new investigation",
"I am comparing my HONEY against a collaborator's", "I am evolving
my own HONEY entries").

**2. The method dependency graph (KS).**
The single most load-bearing missing artifact. v3's entries are a
flat list; KS gave them a graph. Without a graph, mutation impact
analysis is impossible.

Why v3 dropped it: KS's graph was swarmy-specific (mth00403 → mth00404
→ ...). v3's entries are universal principles (pri00001 → ?), and
the relationships among universal principles are less mechanical than
the relationships among operational methods.

How v4 could integrate it: introduce a `depends_on:` field in the
entry frontmatter. Even if dependencies between principles are loose
("CARE ACROSS DISCONTINUITY depends on BUDGET IS A HEARTBEAT because
caring requires a place for the care to live"), naming them is
informative.

**3. Progressive disclosure by context budget (DA).**
DA's tier-load model treats HONEY as a *function of budget*. v3 is a
flat 335 lines; a 2K-budget agent literally cannot load it. DA's
"Scenario 1: Cold start, context <2K... Time: ~5 min total; context
used ~200 tokens" is the only operational story in the corpus that
treats this as a constraint.

Why v3 dropped it: v3 is short enough (335 lines, ~8K tokens) that
the synthesizer judged tiering unnecessary. But 8K is over budget for
many agent spawns.

How v4 could integrate it: ship v4 with three explicit tiers — Core
(Invariants only, ~30 lines), Working (Invariants + Principles +
top-5 methods, ~120 lines), Full (the whole file). A reader can
choose their tier by budget. Same content, three load patterns.

### Open questions for HONEY-v4

These are not "things v3 lost"; they are *unresolved doctrine
questions* that the dig surfaced. The variants disagreed about each
of them and v3 silently picked a side without explaining why.

**Q1. Is HONEY a cross-pod currency or a swarmy-internal operating
manual?**
v3 chose cross-pod currency. The swarmy-operational content (FFMx,
f(0), piston waves, BUZZ, mth00400 range, ws workspace rules,
mission-driven dispatch) is gone. CLAUDE.md now holds that content.
Is the split good? Pro: HONEY stays portable. Con: swarmy agents now
read CLAUDE.md as their operational manual and HONEY as a poetic
preamble, which is an inversion of HONEY's stated authority. v4
should decide: is HONEY one file with two layers (universal + project-
specific), or two files in two roles?

**Q2. Where do the koans go?**
KS, DE, DA, HYBRID all preserved the 13 koans. v3 dropped them
entirely. The koans are the *spirit* of the system — "The Trail That
Knows Itself", "The Queen Who Reads, Not Writes". A reader who knows
the invariants but not the koans understands the rules but not the
worldview. v4 should decide: koans in HONEY (with universal framing,
not swarmy-specific bearings) or koans in a sibling file (KOANS.md,
read alongside HONEY)?

**Q3. Does HONEY have an experimental tier?**
v1-pre-evolution had Tier 4 (Experimental, confidence <0.70). v3
dropped it. But entries below 0.70 must live somewhere — currently
they live in NECTAR (which is append-only) or in scratch (which is
ephemeral). Without an experimental tier in HONEY, a hypothesis
cannot have a stable ID until it's promoted. v4 should decide: add
back Tier 4, or formalize NECTAR-as-experimental-HONEY-staging?

**Q4. Are method IDs portable across pods?**
FEDERATED-HONEY proposed `{pod_id}:{entry_id}` namespacing. v3 has
`pri00001` without pod prefix. If two pods both have a `pri00001`
they collide. v4 should decide: bake the pod prefix into the format,
or pretend federation doesn't exist yet?

**Q5. How is confidence updated?**
KS's confidence progression timeline showed confidence as a
*trajectory*. v3 has static numbers. If a method holds confidence
0.95 for two years without being challenged, is it still 0.95? Or
should confidence decay (TTL-style) until the next validation event?
v4 should decide: confidence as static label, confidence as decaying
property, or confidence as last-validated-on date.

**Q6. Where does adversarial thinking live?**
FEDERATED-HONEY's Attack Model is the only adversarial section in
the corpus. v3 dropped it. But HONEY entries can be wrong, manipulated,
or stale. v4 should decide: does HONEY ship with a "how to challenge
an entry" protocol, or does that live elsewhere?

**Q7. Is HONEY self-aware about its own evolution?**
The variants all carry frontmatter about which version they are,
what they preserve, what they optimize for. v3 has the frontmatter
but no in-file section about its own evolution beyond the "Reflections"
preamble. v4 should decide: does the file ship with a "How This File
Evolves" section, or is that meta-content out of band?

---

## Cross-cutting failure modes (what every variant got wrong about the same thing)

Before the closing posture, one more analytical pass: there are
failure modes that show up in *multiple* variants, suggesting they're
not author-specific but structural. Naming them here so v4 can
prevent each one rather than rediscovering them.

**Failure mode A — Date-windowed validation that stales fast.**
KS, DE, and DA all ship with "validated 2026-05-03" annotations on
high-confidence entries. The day the file is read, the dates feel
authoritative. A month later they feel like museum exhibits. None of
the variants ship with a refresh protocol — there's no script to
re-validate, no date-of-last-challenge, no automatic decay.

**Fix for v4:** treat date-stamps as a triple, not a single value:
`(first_validated, last_validated, last_challenged)`. A method last
validated three months ago should *visibly* show its age. Confidence
without recency-context is misleading.

**Failure mode B — Self-reported quality scores with invisible
methodology.**
Each variant ships with numerical self-grades:
- DA: "Crystallization quality 0.88 (8/10 gates PASS)"
- HYBRID: "Emergence health estimate 0.88"
- The emergence report: "Decision Confidence: 0.91"
- v3 itself: confidence scores on every entry

In none of these cases is the *measurement procedure* visible. How is
0.88 calculated? Which 8 gates passed and which 2 didn't? The numbers
look authoritative but are unauditable.

**Fix for v4:** every number ships with its measurement script + the
input data hash. If 0.88 emergence health is computed by
`9x_emergence_scorer.py` against `forensics/main-metrics-summary.json`,
that lineage should be inline.

**Failure mode C — "100% preservation" claims that aren't.**
DA, DE, KS, HYBRID all claim "100% preservation of original entries."
For each, the claim is technically true at one definition of "entry"
and structurally false at another. DA preserves method IDs but
annotates each one (so the *text* is preserved but the *line count*
balloons 15%). HYBRID lists mth00002–mth00099 as a comma-separated
paragraph instead of as entries (so the *IDs* are preserved but the
*text* is missing).

**Fix for v4:** define "preservation" before claiming it. A
preservation claim should specify which fields are preserved (ID,
text, confidence, tags, position, formatting) and which can be
modified.

**Failure mode D — File grows to accommodate every reader.**
KS = 805 lines. HYBRID = 856 lines. DE = 617 lines. DA = 582 lines.
Each variant adds layers to serve a new audience. None subtract. The
result: HYBRID, which composes the best of all three, is the
longest. Composition without compression is just accumulation.

**Fix for v4:** before adding a new layer, ask "what gets *removed*
when this layer goes in?" If nothing gets removed, the layer is
additive accumulation, not synthesis.

**Failure mode E — Architectures that depend on infrastructure that
doesn't exist.**
FEDERATED-HONEY's Phase 1 (entry versioning + export format) hasn't
shipped. The Pod Registry doesn't exist. IPFS pinning automation
doesn't exist. Cross-pod references resolve to nothing because no
second pod has published a HONEY-EXPORT. The architecture is
beautiful and ungrounded.

**Fix for v4:** the seed concept is fine as long as v4 doesn't claim
operational federation. If federation is the goal, ship Phase 1
before claiming the seed is "federation-ready". If federation isn't
the immediate goal, drop the federation framing and call it what it
is: a cross-domain reference document.

**Failure mode F — Persona tables that don't survive the file.**
v1-pre-evolution had a persona table. DE had a persona table. HYBRID
had a persona table (with the bearing constraint fix). v3 has no
persona table. Each variant *added* personas; the v3 promotion
*removed* them. There was no debate about whether personas belong;
the promotion just dropped them.

**Fix for v4:** if personas were valued by three independent
synthesizers (v1-pre-evo, DE, HYBRID), they belong. v4 should bring
them back unless there's a stated principled reason to omit them.

---

## Closing posture

The v3 promotion was not wrong. It made a coherent choice — HONEY as
a portable seed forkable across pods — and the resulting file is
beautiful, readable, and useful at the cross-pod scope.

But the cost was high. Twelve out of every thirteen lines in the
nine source documents got left behind. Some of that loss was correct
(the validation timelines, the date-stamped operational details, the
swarmy-specific mth IDs). Some of it was loss-as-decision (the koans,
the persona table, the dependency graph). And some of it was loss
that nobody noticed (the Attack Model, the Memory Flow narrative, the
Escape Hatches).

This dig surfaces the last category specifically: orphaned good ideas
that should come back. v4 doesn't need to be a different file. It
needs to be the same file with the right things added back — persona
table at the head, dependency graph in the middle, escape hatches
at the end, and an experimental tier somewhere.

The dig is the map. v4 is the next walk.

— openhands-agent, dig completed 2026-05-22
