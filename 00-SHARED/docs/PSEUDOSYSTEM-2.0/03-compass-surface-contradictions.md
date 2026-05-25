---
title: "Compass-surface + Contradictions"
tags: [pseudosystem-2.0, substrate, compass, f0, anti-fabrication, equilibrium]
related: ["01-idea-compass", "02-auto-edge-inferrer", "04-convergence-detector-hook", "11-confab-class-taxonomy"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 03-compass-surface-contradictions.md

# Compass-surface + Contradictions

## What it does

The compass-surface operation is a traversal verb that walks the West edges of every note in a cluster and surfaces pairs with semantic tension. "Contradictions" in this system are not errors — they are structurally valuable signals. Two notes linked via West edges that assert conflicting states form a contradiction pair worth surfacing to a synthesizer agent.

The verb:
1. Traverses all West edges in a target cluster
2. Computes pairwise tension score between West-linked notes
3. Emits contradiction pairs above threshold to a synthesis queue
4. Tags both notes with `#contradiction-flagged` until resolved or dismissed

This is the mechanism that prevents the graph from silently holding conflicting beliefs. In a large multi-session corpus, contradictions accumulate; this verb makes them visible.

## How it composes with siblings

- Depends on [[01-idea-compass|Idea Compass]] West edges — no West edges, no contradiction surface
- Depends on [[02-auto-edge-inferrer|Auto-edge Inferrer]] having populated West slots
- Feeds [[04-convergence-detector-hook|Convergence Detector Hook]]: a cluster with many unresolved contradictions is a convergence candidate
- Informs [[11-confab-class-taxonomy|Confab-Class Taxonomy]]: label-conflation confabs often produce West-edge contradictions
- Pairs with [[12-anti-fab-validators|Anti-Fab Validators]] to distinguish real contradictions from fabricated ones

## Evidence / Manifests

Contradiction detection logic referenced in:
- `forensics/spawn-contract-violations.jsonl` — captures cases where conflicting contract assertions appeared
- `docs/EMERGENCE-AND-MUTATION-GLOSSARY.md` — authoritative definition of contradiction as mutation class

## Status: live

Surface verb active. Contradiction pairs emitted to synthesis queue when tension score > 0.7.

---

> doc_hash: sha256:pending
