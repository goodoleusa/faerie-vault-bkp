---
title: "Mission Auto-Promotion (Step 2)"
tags: [pseudosystem-2.0, substrate, mission, f0, equilibrium, multi-session]
related: ["05-mission-as-tag", "07-mission-primary-refactor", "04-convergence-detector-hook", "10-multi-session-heartbeat"]
created: 2026-04-25
doc_hash: sha256:pending
status: pending
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 06-mission-auto-promotion.md

# Mission Auto-Promotion (Step 2)

## What it does

Mission Auto-Promotion is step 2 of the three-step mission refactor. It is not yet landed. When implemented, this primitive will:

1. Score all `#f0`-tagged notes by mission-signal strength (citation count, convergence events, agent reference frequency)
2. Auto-promote high-scoring notes to a "mission-surface" dashboard updated every session
3. Demote stale notes that carry `#f0` but have not been referenced in N sessions (default: 3)

The goal: the mission surface is always current, always reflecting what the system is actually doing, not what it was doing when notes were first written. Auto-promotion prevents mission drift from accumulating silently.

This is distinct from [[05-mission-as-tag|Mission-as-Tag (Step 1)]] which simply asserts membership, and from [[07-mission-primary-refactor|Mission-Primary Refactor (Step 3)]] which restructures the graph around mission as a node.

## How it composes with siblings

- Depends on [[05-mission-as-tag|Mission-as-Tag (Step 1)]]: needs `#f0` tags to exist before it can score them
- Feeds [[07-mission-primary-refactor|Mission-Primary Refactor (Step 3)]]: auto-promotion output identifies which notes become mission-node edges
- Uses [[04-convergence-detector-hook|Convergence Detector Hook]] signals as one scoring input (convergence = high signal)
- Coordinates with [[10-multi-session-heartbeat|Multi-Session Heartbeat]] so promotion decisions persist across session boundaries

## Evidence / Manifests

Not yet implemented. Design referenced in:
- `docs/bundle-evolution-system-design-2026-04-24.md` — bundle evolution discusses auto-surface of mission-aligned content
- `forensics/vault-2026-04-24-bundle-evolution-synthesis/` — synthesis artifacts from the design session

## Status: pending

Design complete. Implementation blocked on [[07-mission-primary-refactor|Step 3]] graph schema. Estimated: next sprint after mission-primary-refactor lands.

---

> doc_hash: sha256:pending
