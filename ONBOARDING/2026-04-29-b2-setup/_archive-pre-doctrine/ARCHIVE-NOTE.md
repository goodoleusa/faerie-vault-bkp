---
status: ARCHIVE
archived: 2026-06-04
reason: Superseded by faerie-vault/00-SHARED/docs/B2-BACKUP-DOCTRINE.md (data-class lock-mode doctrine)
canonical: 00-SHARED/docs/B2-BACKUP-DOCTRINE.md
reckon_source: reckon/docs/167-B2-FORENSIC-COC-BACKUP-DOCTRINE.md
---

# Archive: Pre-Doctrine B2 Setup Checklist

This checklist predates the data-class → lock-mode doctrine (reckon docs 166/167, 2026-06-04).

## What was wrong

- Single GOVERNANCE mode for all bucket prefixes (no compliance/governance split by data class)
- 3-key model (write/read/detonate) — predates the 5-key model with named GDPR customer-delete key
- Did not distinguish COC/hashes from raw PII bytes for lock-mode selection

## What replaced it

`00-SHARED/docs/B2-BACKUP-DOCTRINE.md` — vault-specific application of the new doctrine.
Canonical reckon source: `reckon/docs/167-B2-FORENSIC-COC-BACKUP-DOCTRINE.md`
