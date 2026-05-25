# Forensic Integrity — Proof-in-Place Discipline (mth00076)

## Core Principle

The artifact attesting to a system's compliance must be administratively stronger than the system it attests to. WORM genesis proof lives IN the `faerie-worm` B2 bucket with compliance-mode retention (unbypassable by admin), not merely in an external log.

**Audit test:** "Can the thing being audited tamper with its own audit trail?" If yes, move the trail to a stronger substrate (compliance-mode lock, separate-key signing, cross-repo hash commit, Bitcoin timestamp).

## COC System of Record

`{repo}/forensics/` — git-tracked, append-only, hash-chained.

- Agents WRITE only; never read forensic folders (prevents contamination)
- HMAC-SHA256 chain: `prev_entry_hash` → `entry_hash`
- `forensic_coc.py` PostToolUse hook handles chain silently
- Forensics folders MUST NOT be gitignored; track full tree
- Evidence is immutable — never overwrite: `hash_manifest*.json`, `coc_*.json`, `forensic-script-log.md`, `genesis_manifest.json`

## Three-Store Architecture

1. `{repo}/forensics/` — canonical COC (git; system of record)
2. Vault (Obsidian) — styled derivative artifacts (not canonical)
3. S3/B2 WORM — immutable backup of `repo/forensics/`

## Deletion Safety

NEVER delete unprompted. Archival protocol:

1. Hash the file before removal
2. Move to `~/.claude/forensics/deletions/{date}-{hash8}/`
3. Append COC entry documenting the archival

Never delete forensic logs under any circumstance.

## Hash Discipline

HASH BEFORE + AFTER every durable write:
- `hash_tracker.py snapshot --name before-{op}`
- `hash_tracker.py snapshot --name after-{op}`

Per-file SHA256 in COC + directory-level hash_tracker = belt + suspenders.
