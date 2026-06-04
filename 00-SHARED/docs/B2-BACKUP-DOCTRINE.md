---
canonical_source: reckon/docs/167-B2-FORENSIC-COC-BACKUP-DOCTRINE.md
cross_ref: reckon/docs/166-WORM-MEETS-GDPR.md
status: CANONICAL
replaces: archive/B2-WORM-SETUP.md (already archived), ONBOARDING/2026-04-29-b2-setup/B2-SETUP-CHECKLIST.md (archived)
created: 2026-06-04
---

# B2 Backup Doctrine — Faerie Vault

> **One-line summary:** Compliance-lock the proof (hashes/COC); governance-lock the data (bytes/PII).

Canonical source of truth lives in the reckon repo:
- `reckon/docs/167-B2-FORENSIC-COC-BACKUP-DOCTRINE.md` — object-lock mode doctrine, data-class split
- `reckon/docs/166-WORM-MEETS-GDPR.md` — 5-key model, GDPR erasure flow

This document is the **faerie-vault-specific application** of that doctrine.
Where this document and the reckon docs disagree, the reckon docs are authoritative.

---

## 0. Faerie-Vault Bucket Map (new doctrine model)

| Bucket | Mode | Retention | Holds | Notes |
|--------|------|-----------|-------|-------|
| `faerie-worm` (existing) | **GOVERNANCE/90d** | 90 days | Orchestration records, agent manifests | Pre-doctrine bucket; see §1 |
| `faerie2-worm` (planned) | **GOVERNANCE** | 365 days | repo/forensics/ backups | Per B2-WORM-SETUP.md plan |
| `reckon-cust-reckon-self-worm` | **COMPLIANCE** | 10 years | Sealed COC, hashes, finished findings — NO third-party raw PII | reckon-self operator profile |
| `reckon-cust-reckon-self-working` | **GOVERNANCE** | — | Drafts, raw evidence (incl. others' PII), scratch | Erasable |

**faerie-worm note:** This bucket exists and has GOVERNANCE/90d Object Lock (the "existing
governance/90d WORM bucket" referenced in mission context). Under the new doctrine this is
correctly classified — `bypassGovernance` on the operator-master key provides the escape hatch
if needed. The 90d retention floor is appropriate for orchestration records (not long-lived
investigation evidence). No change required; model is consistent.

---

## 1. The Core Doctrine (Mode Follows Data Class)

Full specification: `reckon/docs/167-B2-FORENSIC-COC-BACKUP-DOCTRINE.md`

The key principle: two opposite data classes require opposite modes.

| Data class | Legal requirement | Mode |
|---|---|---|
| Forensic COC / hashes / sealed evidence | court-grade immutability — un-alterable even by operator | **COMPLIANCE** |
| Raw personal / working data / PII | GDPR right-to-erasure — must be deletable | **GOVERNANCE** |

**"Always GOVERNANCE" is wrong** — weakens evidence to "trust me" (operator could have tampered).
**"Always COMPLIANCE" is wrong** — makes third-party PII un-erasable → GDPR violation.
The mode is derived from **what the bucket holds**.

---

## 2. faerie-worm in the New Model Context

`faerie-worm` holds **orchestration records** — agent manifests, session state, hook logs.
This data does not constitute "sealed forensic evidence" requiring court-grade immutability;
it is operational/system data. GOVERNANCE/90d is the correct mode for this class.

Under the new doctrine:
- `faerie-worm` → GOVERNANCE (correct — operational records, short retention, erasable)
- Any operator's own sealed COC/hashes/finished findings → COMPLIANCE (`reckon-cust-reckon-self-worm`)
- The distinction matters: the vault's own operational data vs. the operator's forensic findings
  are different data classes living in different buckets

The `5x_b2_realtime_uploader.py` script (referenced in `coc.md` and `ONBOARDING-NEW-USER.md`)
streams to `faerie-worm`. This is correct — it streams the COC *entries* (metadata, hashes)
not raw investigation bytes. The governance mode is appropriate here because faerie-worm is
orchestration provenance, not sealed investigation evidence.

If in future the sealed COC is committed to a compliance bucket, the `5x_b2_realtime_uploader.py`
should route hashes/COC entries to the compliance bucket and raw data to governance. See §3.

---

## 3. The 5-Key Custody Model

Full specification: `reckon/docs/166-WORM-MEETS-GDPR.md §2`

| Key | Holder | Scope | Purpose |
|-----|--------|-------|---------|
| Agent-write | Runtime agents | -worm + -working write | Streams COC in; NO delete |
| Customer-read | Customer | All buckets read | Self-service audit |
| Customer-delete (GDPR key) | Customer | GOVERNANCE buckets only | GDPR erasure; `bypassGovernance` |
| Operator-master | Operator only | All + `bypassGovernance` | Legal hold, compliance override |
| Crypto sign+decrypt | Customer (seed-derived) | Content layer | Client-side encryption |

The pre-doctrine B2-WORM-SETUP.md used a 3-key model (write/read/detonate). The
`detonate` key maps to the new `customer-delete` GDPR key — functionally the same,
but now properly named and documented in the context of GDPR Art. 17 compliance.

---

## 4. Separation of Proof (for vault-stored evidence)

```
-worm bucket (COMPLIANCE, if used for sealed evidence)
    → hashes + COC entries + metadata ONLY
    → NEVER raw investigation bytes, NEVER third-party PII

-working/-canonical (GOVERNANCE)
    → raw bytes (may contain PII)
    → erasable via customer-delete bypassGovernance
```

On GDPR erasure: wipe the governance bucket (bytes gone); compliance COC survives,
holding hashes that point at deleted data. That dangling hash is NOT a violation —
it is proof the data existed and was erased on date X (GDPR Art. 5(2) demonstrability).

---

## 5. Archived / Superseded Docs

| File | Was | Status |
|------|-----|--------|
| `00-SHARED/docs/archive/B2-WORM-SETUP.md` | Per-repo WORM setup guide (pre-doctrine) | Already archived; single-mode (no data-class split) |
| `ONBOARDING/2026-04-29-b2-setup/B2-SETUP-CHECKLIST.md` | CyberTemplate setup checklist | Archived — superseded by cybertemplate/docs/B2-BACKUP-DOCTRINE.md |

Both files are retained as provenance; not deleted.

---

## Full Doctrine Text (from reckon canonical sources)

The full text of both canonical docs is reproduced below for readability.
The canonical files take precedence on any discrepancy.

### reckon/docs/167 — Object-Lock Doctrine (key sections)

> **North-star: SEPARATION OF PROOF FROM DATA.**
> The immutable thing (COC: hashes + metadata) and the erasable thing (raw bytes,
> possibly containing personal data) live in different buckets with different modes.

**Two retention modes:**

| Mode | Delete/overwrite | Escape hatch | Proves operator could not tamper? |
|---|---|---|---|
| **GOVERNANCE** | only with `bypassGovernance` cap | yes | No |
| **COMPLIANCE** | forbidden for everyone until retention expires | none | YES |

**Compliance is math; governance is policy.** That distinction is the whole doctrine.

**Compliance retention floors (extend-only; minimums):**

| Scope | Retention | Why |
|---|---|---|
| `reckon-self-worm` (operator evidence/perf) | 10 years | published findings + perf proof |
| cybertemplate evidence (first live test case) | **30 years** | long-term legal/historical significance |

Governance data buckets carry no retention floor (must stay erasable for GDPR).

**Flush-PII guard:** COMPLIANCE buckets must refuse payloads containing raw PII.
Only hashes, COC entries, sealed/finished artifacts are admissible.
This is enforced at write time — accidentally locking PII in COMPLIANCE is irreversible.

**When COMPLIANCE is genuinely required:**
- Investigation COC (cybertemplate-class) — court admissibility depends on operator being unable to alter it
- SEC 17a-4 / FINRA financial records — regulator mandates non-bypassable WORM
- Litigation / legal hold — evidence must survive even a hostile admin
- The operator's own published findings — locked beyond even your own reach = unimpeachable

### reckon/docs/166 — WORM Meets GDPR (key sections)

**The reconciliation:**
1. GOVERNANCE mode (not COMPLIANCE) — Object-Lock GOVERNANCE allows `bypassGovernance` deletion
2. Customer-held `bypassGovernance` key — customer (not operator) holds the erasure key
3. Mass-not-selective erasure — bucket granularity only; no per-file selective deletion surface
4. Cryptographic tamper-evidence before deletion — SHA-256 of file ID list → COC entry → Rekor anchor

**GDPR Art. 17 compliance:** GOVERNANCE + customer-delete key = right-to-erasure without "technically impossible" defence.
COMPLIANCE on customer personal data = Art. 83 fines (4% global turnover), no technical defence.

**After erasure:** content is gone; the forensic record of its existence (COC + Rekor) is not.
This satisfies GDPR accountability (Art. 5(2)) — demonstrability survives erasure.

**Canonical tools (reckon repo):**
- `reckon/scripts/b2-admin/b2-admin-provision.py` — provisions 5-key model, dual-mode buckets
- `reckon/scripts/b2-admin/b2-admin-erase.py` — GDPR mass-erase (bucket granularity; refuses COMPLIANCE buckets)
