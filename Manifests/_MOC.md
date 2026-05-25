---
type: moc
title: Manifests — Map of Content
pseudosystem_folder: Manifests
canonical_repo_path: "forensics/manifests/"
tags: [moc, manifest, pseudosystem]
updated: "2026-05-25"
---

# Manifests — Map of Content

> Vault pseudosystem mirror of `forensics/manifests/` in the repo.
> One vault note per sealed manifest JSON. Organized by date (daily subfolders).
> **Canonical source:** signed JSON files in `forensics/manifests/<date>/`.

---

## Daily Folders

| Date | Notes | Description |
|------|-------|-------------|
| [[Manifests/2026-05-25/\|2026-05-25]] | 8 manifests | Today — doctrinal hardening, branch-maker, wandb, viewer, deep-diver |

> Earlier dates (2026-05-24 and prior) are in the repo's `forensics/manifests/` but not yet mirrored here.
> Add subfolders as needed using the `Manifest.blueprint`.

---

## Today's Manifests (2026-05-25)

| Task ID | Mission | Agent | Bearing | Signed |
|---------|---------|-------|---------|--------|
| [[doctrinal-hardening-P3-P4]] | swarmy-doctrinal-hardening | opus-main | S | yes |
| [[doctrinal-hardening-P1-P2]] | swarmy-doctrinal-hardening | opus-main | S | — |
| [[readability-polish-2026-05-25]] | canvas-extension-and-readability-polish | polisher | — | — |
| [[branch-maker-b1b2b3-complete]] | coc-branching-merkle-rollup | branch-maker | — | — |
| [[wandb-curator-20260525]] | publication-export-and-token-instrumentation | wandb-curator | — | — |
| [[anon-viewer-cut-g]] | viewer-readonly | anon-viewer | — | — |
| [[deep-diver-sigstore-remediation-seal]] | sigstore-remediation | deep-diver | — | — |
| [[P1-P5-backend-wiring]] | swarmy-pair-coding-completion | — | — | — |

---

## Dataview Query

```dataview
TABLE mission, agent_type, bearing, signed
FROM "Manifests"
WHERE type = "manifest"
SORT date DESC
LIMIT 20
```

---

*Canonical manifests: `forensics/manifests/` in repo (shape probe: `manifest.signed_by.missing`).*
