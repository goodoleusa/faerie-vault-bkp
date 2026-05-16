---
title: "Confab-Class Taxonomy"
tags: [pseudosystem-2.0, substrate, anti-fabrication, f0, equilibrium]
related: ["12-anti-fab-validators", "13-loop-gap-dual-state-fix", "02-auto-edge-inferrer", "03-compass-surface-contradictions"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 11-confab-class-taxonomy.md

# Confab-Class Taxonomy

## What it does

The Confab-Class Taxonomy is a structured classification of fabrication failure modes observed in faerie2 agent runs. It names two primary classes:

### Class 1: Empty-Probe Confab

An agent queries the system (filesystem, queue, memory) and receives an empty result. Instead of reporting "nothing found," the agent fabricates a plausible-sounding finding to fill the gap. This is the most common confab class — it is triggered by the social pressure to return a non-empty result.

Detection signature: finding with no citation, no file path, no manifest reference. The [[12-anti-fab-validators|Anti-Fab Validators]] empty_probe check catches this by verifying that every claim has a source path that exists on disk.

### Class 2: Label-Conflation Confab

An agent conflates two similar-sounding labels — task IDs, agent types, manifest fields — and writes a finding that correctly describes thing A while believing it is describing thing B. The finding is internally consistent but points at the wrong referent.

Detection signature: manifest field value that does not match the file it claims to reference. The [[12-anti-fab-validators|Anti-Fab Validators]] manifest_metric check catches this by computing the hash of the referenced file and comparing against the manifest's recorded hash.

## How it composes with siblings

- Provides the classification vocabulary that [[12-anti-fab-validators|Anti-Fab Validators]] implements
- Empty-probe confabs often produce West-edge contradictions visible to [[03-compass-surface-contradictions|Compass-surface + Contradictions]]
- Label-conflation confabs produce phantom edges that [[02-auto-edge-inferrer|Auto-edge Inferrer]] must not amplify
- Informs [[13-loop-gap-dual-state-fix|Loop-Gap Dual-State Fix]]: stuck dual-state is often caused by a label-conflation confab writing inconsistent status

## Evidence / Manifests

Taxonomy derived from observed failures. Evidence:
- `forensics/spawn-contract-violations.jsonl` — contract violations are the production instance of confab-class failures
- `forensics/audit-spawn-infrastructure.md` — audit that enumerated fabrication patterns
- `hooks/8x_spawn_contract_enforcer.py` — enforcer catches spawn-level confabs at PreToolUse

## Status: live

Taxonomy documented. Two classes actively detected by validators. Additional classes may be named as new failure modes are observed.

---

> doc_hash: sha256:pending
