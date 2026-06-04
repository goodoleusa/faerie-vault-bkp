---
status: INDEX
created: 2026-06-04
---

# B2 Backup — Doc Index (Faerie Vault)

Canonical doctrine: `00-SHARED/docs/B2-BACKUP-DOCTRINE.md` (this repo)
Ultimate source: `reckon/docs/167-B2-FORENSIC-COC-BACKUP-DOCTRINE.md` + `reckon/docs/166-WORM-MEETS-GDPR.md`

## Active Docs

| File | Role |
|------|------|
| `00-SHARED/docs/B2-BACKUP-DOCTRINE.md` | CANONICAL — data-class doctrine, faerie-worm model context, 5-key, doctrine text |
| `00-SHARED/docs/B2-BACKUP-INDEX.md` | This index |
| `00-SHARED/Architecture/forensic-integrity.md` | Three-store architecture overview (mentions B2 WORM — consistent with doctrine) |
| `00-SHARED/Faerie-System-Internals/coc.md` | COC sidecar doc; references `5x_b2_realtime_uploader.py` — consistent |
| `00-SHARED/COC-Entries/RETENTION.md` | COC retention policy; mentions B2 WORM backup — consistent |

## Archived Docs

| File | Reason |
|------|--------|
| `00-SHARED/docs/archive/B2-WORM-SETUP.md` | Pre-doctrine, single-mode, 3-key model |
| `ONBOARDING/2026-04-29-b2-setup/_archive-pre-doctrine/B2-SETUP-CHECKLIST.md` | Pre-doctrine checklist |

## Bucket Map (faerie-vault context)

| Bucket | Mode | Retention | Purpose |
|--------|------|-----------|---------|
| `faerie-worm` (existing) | GOVERNANCE | 90 days | Orchestration records, agent manifests — correct class |
| `faerie2-worm` (planned) | GOVERNANCE | 365 days | Repo forensics/ backups |
| `reckon-cust-reckon-self-worm` | COMPLIANCE | 10 years | Operator's own sealed COC/findings |
| `reckon-cust-reckon-self-working` | GOVERNANCE | — | Drafts, raw evidence (PII-erasable) |
