---
type: moc
title: Forensics — Map of Content
pseudosystem_folder: Forensics
canonical_repo_path: "forensics/"
tags: [moc, forensics, pseudosystem]
updated: "2026-05-25"
---

# Forensics — Map of Content

> **IMPORTANT:** This folder is a vault-side NAVIGATION companion to the repo's `forensics/` directory.
> The canonical forensics live in the repo (git-tracked, hash-chained, immutable).
> The vault is read-only from forensics' perspective — it provides navigable summaries, not copies.

---

## Subfolder Guide

| Subfolder | Purpose | Canonical Repo Path |
|-----------|---------|---------------------|
| `coc/` | Summary view of COC chain structure + entry types | `forensics/coc.jsonl` |
| `sessions/` | Navigable summaries of archived Claude Code sessions | `forensics/_claude-session-archive/` |
| `waves/` | Per-wave dossiers — each wave is one multi-agent dispatch | `forensics/manifests/<date>/` |

---

## COC Chain Status (2026-05-25)

The COC chain at `forensics/coc.jsonl` contains **16 entries** (per mission-graph.json `coc_entries`).

Key metrics:
- Hash-linked entries (SHA-256 chain)
- Ed25519 signing substrate operational (pynacl 1.6.2)
- Real-time B2 WORM backup queued via hook
- Rekor public anchoring in progress (charter: [[forensic-coc-v2-rekor]])

See `forensics/coc/` subfolder for structural notes on the COC chain.

---

## Mission Graph Edges

| Edge Type | Count |
|-----------|-------|
| COC edges | 10 |
| Discovered edges | 527 |
| Branch merge edges | 2 |
| Branch fork edges | 0 |

---

## Related Pseudosystem Folders

- [[Charters/_MOC]] — charters that govern forensic infrastructure
- [[Manifests/_MOC]] — sealed manifests (the input to the COC chain)
- [[Missions/_MOC]] — missions that produce forensic artifacts

---

*Canonical forensics tree: `forensics/` in repo. Vault is a navigable companion, not a replica.*
