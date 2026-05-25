---
title: "Idea Compass"
tags: [pseudosystem-2.0, substrate, compass, f0, stigmergy]
related: ["02-auto-edge-inferrer", "03-compass-surface-contradictions", "08-stigmergic-clustering", "05-mission-as-tag"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 01-idea-compass.md

# Idea Compass

## What it does

The Idea Compass assigns every note four directional edges — North, South, East, West — that encode its relationship to adjacent concepts in a structured vocabulary. Rather than free-form tagging or manual linking, the compass forces explicit directional intent:

- **North** — what this concept is *built on* (foundations, prereqs)
- **South** — what this concept *enables* (dependents, products)
- **East** — what this concept is *similar to* (siblings, analogues)
- **West** — what this concept *competes with or inverts* (alternatives, contradictions)

This four-axis model transforms a flat note graph into a typed directed graph where edge semantics are machine-readable. It is the foundational primitive that makes [[02-auto-edge-inferrer|Auto-edge Inferrer]] possible — the inferrer fills N/S/E/W slots automatically at add-time based on semantic proximity.

## How it composes with siblings

- Powers [[02-auto-edge-inferrer|Auto-edge Inferrer]]: compass slots are the schema the inferrer writes into
- Seeds [[03-compass-surface-contradictions|Compass-surface + Contradictions]]: West edges are the contradiction candidates the surface verb traverses
- Anchors [[08-stigmergic-clustering|Stigmergic Clustering]]: South edges reveal the cluster a note contributes to
- Informs [[05-mission-as-tag|Mission-as-Tag]]: North edges from mission notes point to the substrate primitives they depend on

## Evidence / Manifests

Status landed in session 2026-04-24. Real manifest ancestry:
- `forensics/manifests/` — grep `idea-compass` for earliest occurrence
- `forensics/compact-events.jsonl` — context compression events that preserved compass design

## Status: live

The four-edge schema is active. Frontmatter `related: []` in all Pseudosystem 2.0 notes encodes the East dimension. North/South edges are expressed via the INDEX.md dependency graph.

---

> doc_hash: sha256:pending
