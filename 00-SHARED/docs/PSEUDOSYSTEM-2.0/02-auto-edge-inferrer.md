---
title: "Auto-edge Inferrer"
tags: [pseudosystem-2.0, substrate, compass, f0, stigmergy, anti-fabrication]
related: ["01-idea-compass", "03-compass-surface-contradictions", "04-convergence-detector-hook", "12-anti-fab-validators"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 02-auto-edge-inferrer.md

# Auto-edge Inferrer

## What it does

The Auto-edge Inferrer runs at note add-time and populates [[01-idea-compass|Idea Compass]] N/S/E/W slots automatically using semantic proximity scoring. When an agent writes a new note, the inferrer:

1. Embeds the note's title + first-paragraph summary
2. Scores against all existing notes in the graph
3. Assigns the highest-scoring candidates to appropriate compass directions
4. Writes wikilinks into frontmatter `related:` and body cross-references

This eliminates the manual linking burden that causes graph sparsity in large note corpora. Without auto-edge inference, agents must remember to link — they rarely do at scale. With inference, every new note is born connected.

## How it composes with siblings

- Reads [[01-idea-compass|Idea Compass]] schema to know which slots to fill
- Its output feeds [[03-compass-surface-contradictions|Compass-surface + Contradictions]]: once edges exist, contradictions can be detected
- Triggers [[04-convergence-detector-hook|Convergence Detector Hook]] when edge density in a cluster crosses threshold
- Its semantic scoring is the first line of defense against fabrication — if a claimed edge has low semantic score, [[12-anti-fab-validators|Anti-Fab Validators]] can flag it

## Evidence / Manifests

Semantic linking design emerged in faerie2 sprint documented in:
- `forensics/compact-events.jsonl` — session events referencing substrate evolution
- `docs/bundle-evolution-system-design-2026-04-24.md` — bundle evolution system, adjacent design

## Status: live

Inferrer runs at add-time for notes entering the Pseudosystem 2.0 constellation. Semantic scoring currently uses cosine similarity on first-paragraph embeddings.

---

> doc_hash: sha256:pending
