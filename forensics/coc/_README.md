---
type: readme
pseudosystem_folder: Forensics/coc
canonical_repo_path: "forensics/coc.jsonl"
tags: [readme, coc, forensics, pseudosystem]
---

# COC — Chain of Custody (Navigation Notes)

> **The canonical COC lives at `forensics/coc.jsonl` in the repo.**
> This folder contains structural notes about the COC chain — schema, entry types, integrity metrics.
> It does NOT contain the actual COC entries (those are evidence-class).

---

## COC Chain Overview

The Chain of Custody (`coc.jsonl`) is a hash-linked append-only log. Each entry records:

| Field | Purpose |
|-------|---------|
| `entry_hash` | SHA-256 of this entry |
| `prev_hash` | Hash of the previous entry (chain link) |
| `ts` | Timestamp of the event |
| `event_type` | What happened (manifest_sealed, retroactive_signing, etc.) |
| `artifact_path` | Path to the artifact being recorded |
| `signed_by` | Ed25519 signature from the responsible agent |
| `charter_id` | Charter context (v2 schema) |

## Entry Types (v2 Schema)

| Event Type | Trigger |
|------------|---------|
| `manifest_sealed` | Agent seals a manifest |
| `retroactive_signing` | Manifest re-signed with real Ed25519 (post-UNSIGNED era) |
| `promotion` | Ephemeral artifact promoted to canonical forensics/ |
| `b2_upload` | WORM backup queued/confirmed |
| `rekor_anchor` | Sigstore Rekor inclusion proof recorded |

## Schema Versions

| Version | Description |
|---------|-------------|
| v1 | Legacy — `hash` + `prev` fields, no `charter_id` |
| v2 | Current — `entry_hash` + `prev_hash` + `charter_id` + `event_type` |

Currently **1 schema version in play** (v2 dominant; shape `coc.schema.versions_in_play` = 1).

## Integrity Status (2026-05-25)

- 16 entries in `forensics/coc.jsonl`
- Ed25519 signing substrate operational
- Rekor integration in progress via charter [[forensic-coc-v2-rekor]]

## Where to Verify the Chain

```bash
cd /mnt/d/0local/gitrepos/faerie2
python3 scripts/9x_manifest_signer.py verify forensics/coc.jsonl
```

---

*Canonical COC: `forensics/coc.jsonl` in repo. Schema reference: `forensics/COC-ENTRY-SCHEMA.json`.*
