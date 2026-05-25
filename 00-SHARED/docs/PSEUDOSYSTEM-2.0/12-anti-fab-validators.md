---
title: "Anti-Fab Validators"
tags: [pseudosystem-2.0, substrate, anti-fabrication, f0, equilibrium]
related: ["11-confab-class-taxonomy", "13-loop-gap-dual-state-fix", "02-auto-edge-inferrer", "14-citation-backlinks"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 12-anti-fab-validators.md

# Anti-Fab Validators

## What it does

Anti-Fab Validators are runtime guards that prevent fabricated findings from entering the forensic record. Two validators are active:

### Validator 1: manifest_metric

Verifies that every hash recorded in a manifest matches the actual file on disk. Steps:
1. Read manifest `finding_hash` field
2. Compute SHA-256 of the file at `output_path`
3. If hashes do not match: reject manifest, emit violation to `forensics/spawn-contract-violations.jsonl`
4. Agent must rewrite the manifest with a valid hash before proceeding

This catches [[11-confab-class-taxonomy|label-conflation confabs]] where an agent writes a hash from a different file.

### Validator 2: empty_probe

Verifies that every factual claim in a manifest has a citation that resolves to a real path. Steps:
1. Extract all citation-format strings from manifest (file paths, manifest IDs, task IDs)
2. Check each path exists on disk OR matches a known manifest ID in forensics/
3. If any citation does not resolve: flag as empty-probe candidate
4. Agent must provide a valid source or retract the claim

This catches [[11-confab-class-taxonomy|empty-probe confabs]] where an agent fabricates a finding when a query returns nothing.

## How it composes with siblings

- Implements detection for both classes in [[11-confab-class-taxonomy|Confab-Class Taxonomy]]
- Produces violation records that [[13-loop-gap-dual-state-fix|Loop-Gap Dual-State Fix]] uses to identify stuck states caused by failed validation
- Guards the citation sources that [[14-citation-backlinks|Citation Backlinks]] uses for D-dimension scoring
- Feeds back into [[02-auto-edge-inferrer|Auto-edge Inferrer]]: only validated claims become edges

## Evidence / Manifests

Both validators are active in production. Evidence:
- `forensics/spawn-contract-violations.jsonl` — running log of validator catches
- `hooks/8x_spawn_contract_enforcer.py` — PreToolUse hook that runs manifest_metric at spawn time
- `hooks/8x_faerie_brief_gatekeeper.py` — gatekeeper hook that runs empty_probe on brief writes

## Status: live

Both validators active. Violation rate tracked in `forensics/spawn-contract-violations.jsonl`. Target: 0 violations per sprint. Current: non-zero (mutations under active repair per mutation discipline protocol).

---

> doc_hash: sha256:pending
