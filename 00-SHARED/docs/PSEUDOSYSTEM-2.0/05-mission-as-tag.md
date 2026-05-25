---
title: "Mission-as-Tag (Step 1)"
tags: [pseudosystem-2.0, substrate, mission, f0, stigmergy, equilibrium]
related: ["06-mission-auto-promotion", "07-mission-primary-refactor", "01-idea-compass", "08-stigmergic-clustering"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 05-mission-as-tag.md

# Mission-as-Tag (Step 1)

## What it does

Mission-as-Tag is step 1 of the three-step mission refactor. In this step, the platform's mission statement — "f(0): orchestration burden on main ≈ 0" — is embedded as a structural tag (`#f0`) applied to every note, manifest, and agent card in the system.

This is not decorative tagging. The `#f0` tag is a machine-readable claim: "this artifact contributes to the mission." It enables:

- Graph-layer filtering: show only nodes contributing to f(0)
- Drift detection: notes that accumulate without `#f0` are off-mission candidates
- Dataview queries that surface mission-aligned vs mission-drifted work

The key design decision of step 1: mission is expressed as a tag applied to existing structure, not as a new graph node. That comes in [[07-mission-primary-refactor|Step 3]].

```dataview
TABLE status, tags
FROM #f0
WHERE contains(tags, "pseudosystem-2.0")
SORT created DESC
```

## How it composes with siblings

- Prerequisite for [[06-mission-auto-promotion|Mission Auto-Promotion (Step 2)]]: auto-promotion needs tags to score
- Prerequisite for [[07-mission-primary-refactor|Mission-Primary Refactor (Step 3)]]: refactor promotes the tag into a first-class node
- Feeds [[08-stigmergic-clustering|Stigmergic Clustering]]: `#f0` tag creates a cross-cutting cluster that spans all topic clusters
- Anchored by [[01-idea-compass|Idea Compass]]: mission notes have North edges pointing to substrate primitives they depend on

## Evidence / Manifests

Step 1 landed. Evidence:
- `CLAUDE.md` and `docs/` consistently carry `#f0` framing
- `forensics/coc.jsonl` — all COC entries reference f(0) mission frame
- `skills/faerie/BODY.md` — faerie skill body encodes mission

## Status: live

`#f0` tag active across all Pseudosystem 2.0 notes and faerie2 manifests.

---

> doc_hash: sha256:pending
