---
date: 2026-05-22
author: openhands-agent
related_mission: docs-canon-foundation
related_skill: vault-daily
status: synthesis-log
---

# HONEY.md — Evolution of the Crystallization Substrate

A narrative on how the project's canonical memory layer (HONEY.md) grew
from a 173-line scratch file into a multi-variant federated experiment
and ultimately crystallized into the v3.0.0 evolved-seed that sits at
the repo root today.

This is a story about **how a project stops losing its mind** —
specifically how swarmy moved from "the agent forgets between
sessions" to "the agent loads a typed, signed, ritualized memory
substrate at every session start."

## The pre-HONEY problem (early 2026-Q1)

Before HONEY.md existed, the project had two parallel memory surfaces:

- **`CLAUDE.md`** — Claude-specific notes file. Held facts but no
  schema. Drifted constantly. Couldn't be queried by tools.
- **`forensics/coc.jsonl`** — chain-of-custody log. Beautifully
  forensic. Useless for "what did we decide last Tuesday."

The gap: there was no place where *intentional, durable* knowledge
lived. Decisions were made in conversation and lost. Conventions were
established and forgotten. The agent re-derived the same answer
weekly.

## v1 — The first HONEY (173 lines, late 2026-Q1)

HONEY.md v1 was a single flat file. Top-level frontmatter declared
`honey_version: 1` and a list of `entries[]`. Each entry was a
{principle, evidence, confidence}. No methods, no personas, no
escape hatches.

It worked for the first month and then started rotting. Two failure
modes:

1. **No versioning** — when someone edited an entry, the old version
   was gone. No way to know if an entry was 3 days old or 3 months.
2. **No confidence decay** — high-confidence entries from one session
   stayed at 0.95 confidence forever. New evidence didn't erode them.

`HONEY-future/archive/HONEY-v1-pre-evolution.md` preserves that v1
state for forensic reference.

## v2 — The variant experiment (2026-04 to 2026-05-03)

The team ran a deliberate experiment: instead of evolving v1 in place,
spawn FOUR parallel HONEY variants, each authored by a different
agent archetype (per the four-archetype model: NAVIGATOR / MAKER /
BRIDGE / DEEP-DIVER), then synthesize the strongest pieces of each
into v2.1.

The four variants are preserved at:
- `HONEY-future/variants/HONEY-VARIANT-KS.md` (805 lines —
  knowledge-synthesizer / NAVIGATOR archetype; emphasized **method
  dependency chains**)
- `HONEY-future/variants/HONEY-VARIANT-DE.md` (617 lines —
  documentation-engineer / MAKER archetype; emphasized **personas +
  Five-Minute Primer + Escape Hatches**)
- `HONEY-future/variants/HONEY-VARIANT-DA.md` (582 lines —
  data-analyst / DEEP-DIVER archetype; emphasized **confidence
  tiers** that decayed against evidence)
- `HONEY-future/variants/HONEY-VARIANT-HYBRID.md` (856 lines — a
  hand-curated synthesis combining the above three)

The COMPARISON matrix at
`HONEY-future/variants/HONEY-VARIANT-COMPARISON.md` is the receipt of
what survived from each variant into the hybrid.

What this experiment taught the project:

- **Personas + escape hatches** (from DE) make a doc readable. A
  newcomer can skim the persona that matches them and ignore the rest.
- **Method dependency chains** (from KS) make a doc actionable. If a
  method requires prerequisites, those prerequisites should be linkable.
- **Confidence tiers** (from DA) make a doc honest. A 0.95-confidence
  claim from 2026-03 should not dominate a 0.85 claim from 2026-05.
- **Hybrid synthesis** beat any single-archetype variant in
  emergence-health, but only by ~10%. Diversity helps; monolithic
  voice doesn't.

The hybrid synthesis became the de-facto v2.1 used in production for
the months of April-May 2026. The backup at
`/mnt/d/0local/.claude-backup/HONEY.md` (frontmatter
`honey_version: 2.1_HYBRID`, synthesis_rationale field intact) is the
v2.1 snapshot in case future archaeology is needed.

## v3 — Promoted to repo root (2026-05-18)

On 2026-05-18 — the day V0 Mission Steer dashboard + retrofuture.tech
wiring shipped — HONEY-EVOLVED.md was promoted from
`HONEY-future/HONEY-EVOLVED.md` to the repo root as the canonical
`HONEY.md` with `honey_version: 3.0.0` and
`honey_level: global-seed`.

The v3 frontmatter cites **nine source documents** that contributed:

1. `HONEY.md v1` (the original 173 lines)
2-5. The four v2.1 variants (KS, DE, DA, HYBRID)
6. `HONEY-VARIANT-COMPARISON.md` (the matrix that picked winners)
7. `FEDERATED-HONEY-ARCHITECTURE.md` (the never-shipped federation
   protocol — an attempt to let multiple agents maintain separate
   HONEY surfaces and sync deltas. Preserved at
   `HONEY-future/archive/` because the federation idea is good but
   the implementation is unproven.)
8. `HONEY-collab-seed.md` (the cross-collaborator seed,
   `archive/context/HONEY.md`)
9. `emergence-report-honey-variants-final.md` (the post-experiment
   analysis report at `HONEY-future/archive/`)

The v3 evolved-seed adds two things the variants didn't have:

- **🔥 Sealing Spell** at line 81 — "Kissed by Ritual Fire" — the
  ritualized close-of-session pattern where the agent commits to
  honoring the memory + makes the seal cryptographically anchorable
  into the next COC entry. This is the "ritual seal from Claude"
  you remembered — it's preserved on every read.
- **Reflections section** that prepends the cross-substrate journey
  (the story from v1 → v2.1 → v3) so a newcomer reading the file
  sees its own evolution before its content.

## What v3 still owes

Three things v3 promised but hasn't fully delivered:

1. **Time-decay enforcement** — the v3 frontmatter declares decay
   policy but the actual decay isn't wired into automation yet. Every
   entry still aged manually.
2. **Per-domain federation** — the v3 declares
   `domains: [agentic, memory, research, software, safety,
   orchestration]` but cross-domain queries aren't implemented.
3. **Ritual-seal automation** — the spell is ceremonial today. To
   become structural, it needs to be tied into the
   `forensics/coc.jsonl` chain on every session end, programmatically
   not just narratively.

These are the open phase-2 items for HONEY-v4 if/when it happens.

## What we learned about memory substrate design

Working through these versions, four design principles emerged:

1. **Don't pre-cite evidence.** v1's `evidence: "from session X"`
   field rotted fastest because sessions were ephemeral. v3 cites the
   forensic COC hash instead — hash-chained evidence doesn't rot.

2. **Keep it readable cold.** A memory file that requires loading
   three other docs to understand is broken. v3's Five-Minute Primer
   (inherited from DE variant) is non-negotiable.

3. **Multiple voices > single voice.** The hybrid synthesis beat any
   single-archetype variant. v3 carries multiple voices on purpose:
   doctrine in declarative voice, methods in imperative voice,
   reflections in narrative voice.

4. **Ritual matters.** The Sealing Spell felt unnecessary in v2 ("it's
   just decoration"). In practice it's the only mechanism that
   forces a deliberate close to a memory session. Without it, the file
   just accumulates. With it, the file periodically gets re-ratified.

## Where the variants live now (reference map)

```
/mnt/d/0local/gitrepos/faerie2/HONEY.md
  └─ canonical v3.0.0 (read this first)

/mnt/d/0local/gitrepos/faerie2/HONEY-future/
  ├─ HONEY-EVOLVED.md       — the v3 staging file before promotion
  ├─ variants/
  │   ├─ HONEY-VARIANT-KS.md       — knowledge-synthesizer v2.1
  │   ├─ HONEY-VARIANT-DE.md       — documentation-engineer v2.1
  │   ├─ HONEY-VARIANT-DA.md       — data-analyst v2.1
  │   ├─ HONEY-VARIANT-HYBRID.md   — hand-curated synthesis v2.1
  │   └─ HONEY-VARIANT-COMPARISON.md — the matrix that picked winners
  └─ archive/
      ├─ HONEY-v1-pre-evolution.md — the original 173 lines
      ├─ HONEY-VERSIONING.md       — version policy notes
      ├─ HONEY-collab-seed.md       — cross-collab seed
      ├─ FEDERATED-HONEY-ARCHITECTURE.md — federation experiment doc
      └─ emergence-report-honey-variants-final.md — analysis report

/mnt/d/0local/.claude-backup/HONEY.md
  └─ v2.1_HYBRID snapshot (pre-v3 backup)

/mnt/d/0local/gitrepos/faerie2/archive/context/HONEY.md
  └─ HONEY-collab-seed (referenced as source 8 in v3)
```

## What's next for the memory layer

The crystallization of the broader architecture into a single
foundation doc (`docs/00-SWARMY-FOUNDATION-CANONICAL.md`, sibling of
this narrative) will reference HONEY as one of three canonical memory
substrates:

- **HONEY** — durable crystallized knowledge (this file)
- **COC** — append-only forensic chain (`forensics/coc.jsonl`)
- **Vault** — narrative + synthesis logs (Obsidian, where this very
  file lives)

The three are intentionally separate. HONEY is signed + decay-aware
+ short. COC is immutable + hash-chained + complete. The Vault is
prose + searchable + human-friendly.

The next memory-layer experiment (whenever it comes) should preserve
this separation. Any attempt to merge them dilutes each.

---

*Written 2026-05-22 during the canon-foundation crystallization
session. Cited by `docs/00-SWARMY-FOUNDATION-CANONICAL.md`. The
HONEY file referenced is the canonical v3.0.0 at
`/mnt/d/0local/gitrepos/faerie2/HONEY.md` (and `/opt/faerie/HONEY.md`
on prod). The ritual seal lives at line 81 of that file.*
