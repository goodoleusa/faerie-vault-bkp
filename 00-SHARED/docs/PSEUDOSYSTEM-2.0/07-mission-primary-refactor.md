---
title: "Mission-Primary Refactor (Step 3)"
tags: [pseudosystem-2.0, substrate, mission, f0, stigmergy, equilibrium]
related: ["05-mission-as-tag", "06-mission-auto-promotion", "08-stigmergic-clustering", "01-idea-compass"]
created: 2026-04-25
doc_hash: sha256:pending
status: pending
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 07-mission-primary-refactor.md

# Mission-Primary Refactor (Step 3)

## What it does

Mission-Primary Refactor is step 3 of the three-step mission refactor. It is not yet landed. When implemented, this primitive promotes mission from a tag to a first-class graph node — the central attractor in the Obsidian graph view.

The refactor:
1. Creates a dedicated `MISSION.md` node with edges to every `#f0`-tagged note
2. Restructures the compass such that North edges from all substrate primitives terminate at MISSION
3. Makes MISSION the canonical hub note that the Obsidian graph renders as the gravitational center
4. Enables mission-distance scoring: how many hops from any note to MISSION?

After this refactor, the Obsidian graph view reveals the constellation structure immediately — all notes cluster around the mission node, topic clusters appear as satellite constellations.

## How it composes with siblings

- Culminates [[05-mission-as-tag|Mission-as-Tag (Step 1)]] and [[06-mission-auto-promotion|Mission Auto-Promotion (Step 2)]]
- Restructures [[01-idea-compass|Idea Compass]] North edges globally — every primitive's North edge terminates at MISSION
- Creates the primary hub that [[08-stigmergic-clustering|Stigmergic Clustering]] orbits
- Once landed, [[06-mission-auto-promotion|Step 2]] can score mission-distance instead of raw citation count

## Evidence / Manifests

Not yet implemented. Precursor design in:
- `docs/bundle-evolution-system-design-2026-04-24.md`
- `forensics/vault-2026-04-24-bundle-evolution-synthesis/` — synthesis session that produced the three-step plan

## Status: pending

Blocked on [[06-mission-auto-promotion|Step 2]] scoring signals. Target: establish MISSION.md node with manually curated edges first, then automate edge maintenance via Step 2 output.

---

> doc_hash: sha256:pending
