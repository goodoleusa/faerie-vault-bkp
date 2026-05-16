---
title: "Citation Backlinks"
tags: [pseudosystem-2.0, substrate, anti-fabrication, f0, stigmergy, equilibrium]
related: ["12-anti-fab-validators", "02-auto-edge-inferrer", "11-confab-class-taxonomy", "08-stigmergic-clustering"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 14-citation-backlinks.md

# Citation Backlinks

## What it does

Citation Backlinks is the primitive that lifted the D-dimension (Depth) eval score from 0.12 to 0.89 in the faerie2 membench eval. It works by injecting bidirectional citation links into the forensic record:

**Forward citation** (existing): an agent's manifest cites the source artifact it drew from.

**Backlink** (new): the source artifact's metadata is updated to record that it was cited by this manifest. The backlink is a reverse-edge in the citation graph.

With backlinks active:
1. Any forensic artifact can answer "who cited me and when?" without full-graph scan
2. Depth scoring can traverse the citation graph in both directions
3. Orphaned artifacts (never cited) become visible as graph nodes with no inbound edges
4. The D-dimension score reflects actual depth of evidence chains, not just claimed depth

The 0.12 → 0.89 lift came from: at 0.12, the eval could only follow forward citations (shallow); at 0.89, bidirectional traversal revealed 7-hop evidence chains that forward-only traversal could not see.

## How it composes with siblings

- Depends on [[12-anti-fab-validators|Anti-Fab Validators]] to verify that forward citations are real before writing backlinks
- Feeds [[02-auto-edge-inferrer|Auto-edge Inferrer]]: citation edges are a high-confidence signal for compass East edges (co-cited = similar)
- Amplifies [[08-stigmergic-clustering|Stigmergic Clustering]]: co-citation density is a clustering signal
- Backlink graph exposes label-conflation confabs detected by [[11-confab-class-taxonomy|Confab-Class Taxonomy]]: a backlink pointing to a file that disagrees with the claiming manifest is a confab signal

## Evidence / Manifests

D-dimension lift is a measured result. Evidence:
- `scripts/eval/eval_harness.py` — eval harness that measures D-dimension
- `forensics/mutation-gates-test-20260424_115036.json` — mutation gate test results referencing D-dimension scoring
- `forensics/mutation-gates-test-20260424_115155.json` — second gate test confirming lift
- `scripts/9x_mutation_metrics_gates.py` — gates script that enforces D-dimension minimum

## Status: live

Backlink injection active for all new manifest writes. D-dimension score at 0.89 and held. Backlink graph queryable via `9x_lean_query.py`.

---

> doc_hash: sha256:pending
