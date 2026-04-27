---
title: Forensic Chain of Custody — Vault Registry
type: forensic-registry
status: live
created: 2026-04-01
doc_hash: sha256:57ba5a781f0b2ee1045996e825486468bdbb9b287ddb68a2c357fe583a8df833
hash_ts: 2026-04-01T16:30:12Z
hash_method: body-sha256-v1
---

# Forensic Chain of Custody — Vault Registry

**CRITICAL: This is the system of record for all vault mutations and forensic evidence.**

All agent and human mutations to vault files are logged here with:
- Timestamp (UTC, ISO8601)
- Mutator (agent type or human user)
- File path (relative to vault root)
- Content hash (SHA256, excluding version control fields)
- Previous version hash (creates unbreakable chain)
- Session ID and context (WHY the change was made)

**Why it lives in vault, not .claude/**
- `.claude/` is local-only and undefended — vulnerable to machine compromise
- Vault is the authoritative record — backed to B2/S3 WORM for immutability
- Hash chain spans vault + forensic log — breaking it requires recomputing all downstream hashes
- Court-admissible: provenance trail is unbroken, signatures can be verified

## Files in This Directory

- **vault-mutations.jsonl** — Append-only log of all file mutations (one JSON entry per line)
  - Entry format: timestamp, vault_path, version, doc_hash, previous_hash, mutator, session_id, mutation_context, entry_hash (signature)
  - Hash chain: each entry includes `chain_prev_entry_hash` linking to prior entry
  - Tamper detection: altering any entry breaks all subsequent entry_hash values

## Backup & Replication

Forensic logs sync to:
1. **B2 Backup** (via backup_forensics.py) — immutable, append-only
2. **Git history** (via /handoff commit) — for changelog + human review
3. **Forensic archive** (optional S3 WORM) — for long-term legal holds

## Verification Tools

- `query-vault-mutations.py <path>` — Show full mutation history for a file
- `verify-vault-hash-chains.py` — Validate chain integrity (no tampering)
- `hash_tracker.py snapshot --name before-op` → `--name after-op` — Belt+suspenders validation

---

*This registry is machine-generated and append-only. Do not edit by hand.*
