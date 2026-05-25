---
type: moc
title: Charters — Map of Content
pseudosystem_folder: Charters
canonical_repo_path: "forensics/charters/"
tags: [moc, charter, pseudosystem]
updated: "2026-05-25"
---

# Charters — Map of Content

> Vault pseudosystem mirror of `forensics/charters/` in the repo.
> Each note here mirrors one charter JSON — frontmatter mirrors key fields; body is a navigable summary.
> **Do not edit** charter state here — the canonical JSON in the repo is the source of truth.

---

## Active Charters (14)

| Charter | Mission | Phase | Status |
|---------|---------|-------|--------|
| [[blockchain-anchored-forensic-chain]] | merkle/blockchain | 1-of-3 | active |
| [[2026-05-21_canvas-as-headwater]] | canvas headwater | phase_1 | active |
| [[mission-docker-deploy-stability]] | [[mission-docker-deploy-stability]] | phase 2 | active |
| [[swarmy-production-runway]] | production runway | phase 2 | active |
| [[swarmy-rename-and-cleanup]] | rename cleanup | phase_1 | active |
| [[hive-pair-coding-foundation]] | [[hive-pair-coding-foundation]] | 6-of-6 | active |
| [[mcp-dispatcher-only-migration]] | mcp.surface.unify | — | active |
| [[oh-version-bump-0.39-to-latest]] | openhands.version.bump | — | active |
| [[swarmy-oh-runtime-bootstrap]] | [[precious.faerie.salvage]] | phase_1 | active |
| [[forensic-coc-v2-rekor]] | [[merkle.rekor.anchor]] | phase_1 | active |
| [[multi-tenancy-and-free-tier-scoping]] | tenancy.scope.isolation | — | active |
| [[recursive-canvas-visual-design-substrate]] | canvas.visual.design | — | active |
| [[doctrinal-hardening-and-pair-production]] | [[swarmy-doctrinal-hardening]] | 1-of-4 | active |
| [[pair-coding-completion-and-dry-cleanup]] | [[swarmy-pair-coding-completion]] | COMPLETE | sealed |

## Proposal Charters (3)

| Charter | Mission | Status |
|---------|---------|--------|
| [[court-admissible-evidence-chain]] | evidence.chain.admissibility | proposed |
| [[rekor-merkle-root-public-anchor]] | — | proposed |
| [[publication-prep-bundle-curation]] | — | proposed |

## Sealed Charters

> Sealed (completed) charters move to `Charters/sealed/`. See that subfolder when it populates.

---

## Dataview Query (Obsidian Dataview plugin)

```dataview
TABLE status, semantic_mission, phase
FROM "Charters/active"
WHERE type = "charter"
SORT created DESC
```

---

*Canonical charter directory: `forensics/charters/` in repo. Max active charters: 15 (shape: `charter.active.over_cap`).*
