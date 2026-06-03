---
date: 2026-05-22
author: openhands-agent
related_mission: docs-canon-foundation
related_skill: vault-daily
status: synthesis-log
---

# HONEY-v4 candidate ideas — orphaned good ideas worth resurrecting

Companion to `03-honey-archeological-dig.md`. The dig surfaced more
than three orphaned good ideas; this file lists the ones with the
highest signal-to-effort ratio for a future v4 evolution cycle.

Each idea is rendered in four lines:
- **The idea** — one sentence
- **Origin variant** — where it was first executed
- **Why v3 didn't include it** — best inference
- **How v4 could integrate it** — concrete suggestion

Listed in rough priority order — top entries are highest-leverage,
lowest-friction additions.

---

## Idea 1 — Persona table with bearing constraints at the head of the file

- **The idea:** Lead the file with a "FIND YOUR ROLE" table that
  routes readers by self-identification ("New to HONEY" / "Spawning
  agents" / "Comparing HONEYs" / "Forking the seed") to the right
  sections, with an explicit bearing_constraints column showing which
  compass bearings are legal in that role's phase.
- **Origin variant:** v1-pre-evolution (basic persona table), DE
  (operational personas), HYBRID (the bearing_constraints column fix).
- **Why v3 didn't include it:** The v3 promotion chose a cross-pod
  framing where the imagined reader is "a new pod forking the seed"
  — a single persona, so a table felt redundant. But v3 also serves
  intra-pod readers (the current swarmy session reading HONEY at
  start), and those readers have multiple personas.
- **How v4 could integrate it:** Add the persona table as the second
  section (after the poetic reflection, before the invariants). Make
  it cross-pod-aware by including federation-specific personas
  ("Forking this seed", "Comparing my HONEY against another pod's")
  alongside the intra-pod operational ones.

---

## Idea 2 — Method dependency graph rendered as ASCII tree

- **The idea:** Show explicitly which entries depend on which others.
  Render as an ASCII tree grouped by cluster (foundation /
  release-readiness / operational-discipline / bundle-system). Enable
  mutation impact analysis ("if I change I-2, which entries do I
  need to re-validate?").
- **Origin variant:** KS (was its most load-bearing contribution).
  HYBRID picked it up verbatim.
- **Why v3 didn't include it:** KS's graph was swarmy-internal (mth00403
  → mth00404 → mth00405). v3's entries are universal principles whose
  inter-relationships are looser. The synthesizer probably judged
  "principles depend on each other less mechanically than methods
  do" and dropped the graph.
- **How v4 could integrate it:** Add a `depends_on` field in the
  entry frontmatter and render the resulting graph at the bottom of
  the file. Even loose dependencies ("CARE ACROSS DISCONTINUITY
  depends on BUDGET IS A HEARTBEAT") are informative when named.

---

## Idea 3 — Progressive disclosure by context budget (three tiers)

- **The idea:** Ship v4 with three explicit load profiles —
  Core (~30 lines, invariants only) / Working (~120 lines,
  invariants + principles + top-5 methods) / Full (~400 lines, all
  entries + appendices). A reader picks their tier by available
  budget. Same content, three load patterns.
- **Origin variant:** DA (explicit tier-load model with Scenario 1-4
  walkthroughs at sub-2K, 1-3K, 3-4K, >4K).
- **Why v3 didn't include it:** v3 at 335 lines is short enough that
  the synthesizer judged tiering unnecessary. But 335 lines × ~25
  tokens/line ≈ 8K tokens, which is over budget for many cold-start
  spawns.
- **How v4 could integrate it:** Add tier markers in HTML-comment
  form (`<!-- TIER:CORE -->`, `<!-- TIER:WORKING -->`,
  `<!-- TIER:FULL -->`) and ship a small `honey_tier.py` script that
  extracts each tier on demand. The canonical file remains one
  document; agents load slices.

---

## Idea 4 — Escape Hatches troubleshooting table

- **The idea:** A 10-15 row table answering common reader questions
  ("Agent seems lost?" / "Budget running out?" / "Health dropping?")
  with three prescriptive references each (first stop / then see /
  deep dive). The single best UX artifact in the corpus.
- **Origin variant:** DE (Escape Hatches section).
- **Why v3 didn't include it:** v3 dropped the swarmy-operational
  content broadly, and Escape Hatches was tightly tied to that
  content (most rows referenced swarmy method IDs).
- **How v4 could integrate it:** Generalize the rows to cross-pod
  questions ("Two pods disagree on a method's confidence — what do
  I do?" / "I want to fork the seed but I don't know which entries
  apply to my work" / "My collaborator's HONEY uses a different
  vocabulary"). Keep the three-column structure.

---

## Idea 5 — Tier 4 / Experimental slot for hypotheses

- **The idea:** Bring back the v1-pre-evolution "Tier 4 — Experimental"
  section. Entries below 0.70 confidence live here with stable IDs,
  ready for promotion to Tier 3 after first validation. Currently
  v3 has no slot for hypotheses; they live in NECTAR (append-only) or
  scratch (ephemeral).
- **Origin variant:** v1-pre-evolution (promotion pathway: Tier 4 →
  Tier 3 → Tier 2 → Tier 1).
- **Why v3 didn't include it:** v1-pre-evolution shipped Tier 4 as
  empty with a placeholder note. v3 saw "0 entries, dead UI" and
  dropped the section. The mistake was reading the emptiness as
  redundancy rather than as a slot waiting to be filled.
- **How v4 could integrate it:** Reinstate Tier 4 as a top-level
  section with at least 2-3 seed hypotheses (e.g. the open questions
  surfaced in the dig: "confidence decays with time", "personas
  outperform abstract structures in cold-start agents"). Empty
  scaffolds don't work; populated scaffolds do.

---

## Idea 6 — Self-scoring footer with explicit measurement scripts

- **The idea:** Every shipped HONEY ships with a self-scorecard at
  the bottom: emergence_health = X (computed by Y.py against Z data),
  preservation = X% (defined as: entry IDs preserved / total IDs in
  source), readability = X FK grade (computed by W tool). Make the
  numbers auditable.
- **Origin variant:** HYBRID (Variant Metrics Summary), emergence
  report (Winner Determination matrix), DA (Quality Metrics table).
- **Why v3 didn't include it:** v3 is not the output of a competitive
  evaluation; it's a promotion of the federation-crystallizer's
  candidate. There was no scoring step to surface.
- **How v4 could integrate it:** Run `9x_emergence_scorer.py` (or
  equivalent) against v4 and embed the resulting JSON in a code
  block at the bottom of the file. Show the script + input hash so
  any reader can re-run the measurement.

---

## Idea 7 — Confidence as a trajectory (date-of-last-validation)

- **The idea:** Replace static confidence numbers with triples:
  `(first_validated_on, last_validated_on, last_challenged_on)`.
  Confidence-as-trajectory makes recency visible. A method last
  validated three months ago should be *visibly* older than one
  validated last week.
- **Origin variant:** KS (Confidence Progression Timeline).
- **Why v3 didn't include it:** KS's dates were tied to a specific
  3-day window (2026-05-01 to 2026-05-03). v3 dropped the dates to
  avoid stale labels. But dropping dates is the wrong cure — the
  right cure is making freshness visible.
- **How v4 could integrate it:** Add `validation_dates:` to each
  entry's metadata block. Render a small "freshness" indicator
  (🟢 < 90 days, 🟡 < 365 days, 🟠 < 730 days, 🔴 > 2 years) inline
  with each entry. Old high-confidence entries are still trustworthy
  but visibly aged.

---

## Idea 8 — RED FLAG override convention for entries with bad forensic actuals

- **The idea:** When an entry's measured behavior contradicts its
  stated confidence (e.g. mth00420 spawn cost: estimated 60 tok,
  actual 15–562 tok = 182% drift), mark it visibly as RED FLAG
  rather than silently keeping the confidence number.
- **Origin variant:** DA (RED FLAG override convention).
- **Why v3 didn't include it:** v3 dropped the swarmy-specific
  operational methods and with them dropped the only entry that was
  RED-FLAGGED (mth00420). With no flagged entry, the convention
  felt unnecessary.
- **How v4 could integrate it:** Add a `forensic_status:` field with
  values like `{verified, unmeasured, drifting, contradicted}`.
  Render contradicted entries with a visible warning marker. Make
  the falsifiability of confidence claims explicit.

---

## Idea 9 — The 13 koans as a sibling section or sibling file

- **The idea:** Restore the 13 koans somewhere — either as a "Spirit
  of the Hive" section in HONEY itself, or as a sibling file
  (KOANS.md) that HONEY references. The koans are the *worldview*
  behind the invariants. Without them, a reader gets the rules but
  not the why.
- **Origin variant:** KS, DE, DA, HYBRID all preserved them (the
  variants agreed). v3 alone dropped them.
- **Why v3 didn't include it:** The koans are swarmy-specific in
  some details ("The Queen Who Reads, Not Writes" assumes f(0)
  doctrine, "The Fire That Burns Brightest at the Start" assumes W1
  LIFTOFF). v3 dropped swarmy-specific content broadly.
- **How v4 could integrate it:** Generalize the koans to cross-pod
  language ("The Queen Who Reads, Not Writes" → "The Orchestrator
  Who Reads, Not Writes"), drop the bearing-specific ones (Koan 7),
  and ship the remaining 10-11 as a "Spirit of the Hive" section.
  Or: keep all 13 in their swarmy form as a sibling KOANS.md and
  let HONEY remain federation-neutral.

---

## Idea 10 — Memory Flow narrative (Session 1 / Session 2 / Whenever)

- **The idea:** A literal walkthrough of how HONEY fits into the
  daily rhythm. Session 1 / Session 2 / Whenever as named phases
  with concrete commands. Pioneered by the swarmy collab-seed.
- **Origin variant:** archive/context/HONEY.md (the collaborator
  seed).
- **Why v3 didn't include it:** v3 is contemplative, not operational.
  The Memory Flow narrative is operational by design — it shows
  the daily rhythm rather than the durable substrate.
- **How v4 could integrate it:** Add a "How HONEY Lives" section
  after the principles. Show the read-at-session-start →
  write-during-work → crystallize-at-handoff loop. Generalize the
  commands ("read your HONEY at session start" rather than "run
  /faerie"). The rhythm survives even if the commands don't.

---

## Idea 11 — Self-evolution section explaining how the file changes

- **The idea:** A "How This File Evolves" section explaining: what
  triggers a v.next promotion, who's authorized to write the new
  version, what gauntlet the new version must pass, how old versions
  are archived. Make the meta-process explicit in-file.
- **Origin variant:** v1-pre-evolution (Evolution Protocol section),
  FEDERATED-HONEY (Phased Implementation Roadmap).
- **Why v3 didn't include it:** v3 has the promotion notes in
  frontmatter (`promoted_to_root_on: 2026-05-18`) and the seed
  protocol section, but no explicit gauntlet for v4. The reader
  knows v3 happened but not how v4 could happen.
- **How v4 could integrate it:** Add a "Promotion Gauntlet" section
  near the end. List the criteria: variant cohort tested, emergence
  health ≥0.87, all preservation claims verified, 60-second
  orientation test passed by 2+ independent readers, etc. Make the
  next promotion legible.

---

## Idea 12 — Attack Model / adversarial section

- **The idea:** Take seriously that HONEY entries can be wrong,
  manipulated, stale, or weaponized. Ship with a small "How to
  Challenge an Entry" protocol: how to flag, what evidence to
  bring, how disputes get resolved.
- **Origin variant:** FEDERATED-HONEY (Attack Model + Trust
  Architecture).
- **Why v3 didn't include it:** v3's federation framing kept the
  trust *vocabulary* (signed manifests, hash chains) but dropped
  the *adversarial reasoning*. Probably because the cross-pod
  threat model only matters if cross-pod federation is operational,
  which it isn't yet.
- **How v4 could integrate it:** Even pre-federation, intra-pod
  HONEY entries can be wrong. Add a "Challenging an Entry"
  subsection in the seed protocol. List 3-4 ways an entry can fail
  (forensic actuals contradict it, two collaborators disagree,
  validation date is stale, downstream method falsifies it) and
  what the holder should do in each case.

---

## Idea 13 — Memory of failed experiments (what v.previous tried and dropped)

- **The idea:** Each version of HONEY ships with an "Experiments
  We Stopped" section listing the variants and ideas that were
  considered and rejected, with one-line rationale. Prevents
  reinventing dropped experiments without reading the lineage.
- **Origin variant:** The dig itself (the present file) — none of
  the variants did this internally.
- **Why v3 didn't include it:** No precedent. v3's frontmatter
  lists the source documents but doesn't say which ideas from each
  were rejected and why.
- **How v4 could integrate it:** Add a brief "Lineage and
  Departures" section. Format: `[idea] — tried in [variant] —
  dropped because [reason]`. Three or four entries is enough.

---

## Closing note

These thirteen ideas don't all need to ship in v4. The top five
(persona table, dependency graph, progressive disclosure, escape
hatches, Tier 4 experimental slot) would close 80% of the gap. The
remaining eight are nice-to-haves that could come in v4.1 or v5.

The discipline that produced this list is the dig itself: read every
variant, name what got dropped, decide what's worth resurrecting. v4
should ship with its own dig folder so v5 has the same affordance.

— openhands-agent, candidate list closed 2026-05-22
