# Forensic System Summary — Executive Overview

**Date:** 2026-04-07  
**Audience:** System architects, project leads, legal teams  
**Purpose:** 1-page reference for the faerie2 forensic architecture  

---

## What It Does

The faerie2 forensic system records **every decision, transformation, and output** in a cryptographic chain. The result: investigations are **reproducible, verifiable, and admissible as evidence** in court.

## Core Components

| Component | Purpose | Location | Key Property |
|-----------|---------|----------|--------------|
| **Evidence Store** | Immutable baseline (source of truth) | `{repo}/forensics/` | Git-tracked, hash-chained |
| **COC Chain** | Cryptographic record of every action | `coc.jsonl` (append-only) | SHA256 hash chain, no gaps |
| **Reasoning Log** | Analysis steps (agent inputs → outputs) | `reasoning.jsonl` | Enables audit + replayability |
| **NECTAR** | Validated findings (accretes knowledge) | `~/.claude/memory/NECTAR.md` | Append-only narrative |
| **HONEY** | Crystallized facts (permanent knowledge) | `~/.claude/memory/HONEY.md` | Compressed + contextualized |
| **Vault** | Human-readable docs (synced to collaborators) | `$CT_VAULT/00-SHARED/Design-Narratives/` | Derivative, not canonical |
| **B2 WORM** | Immutable cloud backup | B2 bucket with WORM enabled | Write-once, versioned, permanent |

## The Three-Store Model

```
RAW EVIDENCE (files)
  ↓ [ingest] → EVIDENCE STORE
  ↓
AGENT ANALYSIS (thinking)
  ↓ [produce finding] → REASONING LOG
  ↓
MEMORY PROMOTION (validation)
  ↓ [promote] → NECTAR (narrative)
  ↓
CRYSTALLIZATION (integration)
  ↓ [compress] → HONEY (seed)
  ↓
COURT EXPORT (bundle)
  ↓ [sign + upload] → B2 WORM
```

**Key insight:** Each layer is independent. Evidence cannot be contaminated by reasoning. Reasoning is recorded but not canonical. Findings are validated before becoming durable knowledge.

## The Hash Chain

Every action is recorded in `coc.jsonl` (Chain of Custody):

```json
{
  "entry_id": "COC-00042",
  "type": "ingest",
  "ts": "2026-04-07T14:23:47Z",
  "actor": "data-engineer",
  "data": {"files_added": 127, "manifest_hash": "sha256:abc123..."},
  "entry_hash": "sha256:def456...",
  "prev_entry_hash": "sha256:xyz789...",  ← points to previous entry
  "sig": "PGP_SIGNATURE"
}
```

**Why it matters:** Each entry depends on the previous one. If anyone modifies entry #42, its hash changes, breaking entry #43 (and all downstream entries). A broken chain = proof of tampering.

## Forensic Integrity Properties

| Property | How Achieved | Court Value |
|----------|-------------|-------------|
| **Completeness** | Every action recorded + hash-chained | No gaps = no hidden steps |
| **Authenticity** | PGP signatures on critical entries | Identifies the actor |
| **Integrity** | SHA256 hashes + hash chain | Detects any tampering |
| **Non-repudiation** | Signatures + timestamps | Actor cannot deny actions |
| **Reproducibility** | reasoning.jsonl + manifests + inputs | Can re-run and verify outputs match |

## Use Cases

### Before Court Filing
1. Generate evidence export: `forensic_coc.py export --inv mycase`
2. Verify bundle: Every file hash matches manifest, COC chain unbroken
3. Sign bundle with PGP, upload to B2 WORM (permanent copy)
4. Give bundle to legal team — it is self-documenting

### During Discovery
1. Opposing counsel challenges: "How do we know the evidence wasn't doctored?"
2. Answer: "Here is the COC chain. Each entry hashes correctly. The chain is unbroken. git history shows no modifications. B2 WORM shows the bundle was uploaded at [timestamp] and has not been modified since."
3. Detailed: "Here is forensic_integrity.py verify output — every file matches its original hash."

### After Investigation Completes
1. NECTAR becomes a permanent narrative record (append-only forever)
2. HONEY crystallized the durable lessons learned
3. forensics/ folder archived to S3/B2 WORM (immutable backup)
4. Investigation can be reopened years later with full context

---

## Key Rules (Non-Negotiable)

1. **Never modify forensics/ files** — only append
2. **Record every ingest phase** — before and after hashes
3. **Separate reasoning from evidence** — agents read evidence, write reasoning; never both
4. **Hash before and after every change** — document in audit-log.md
5. **Sign critical entries** — genesisctomy, major promotions, exports
6. **Commit to git regularly** — forensics/ changes are permanent once committed
7. **Backup to WORM** — B2 is the final immutable copy

---

## Implementation Timeline

| Phase | Owner | Deliverable | Court Ready? |
|-------|-------|-------------|--------------|
| **Genesis** | System | hash_manifest.json + coc.jsonl entry 1 | No (baseline only) |
| **Ingest** | data-engineer | coc.jsonl entries per phase + manifests | No (raw data) |
| **Analysis** | agents | reasoning.jsonl + findings | No (working hypotheses) |
| **Validation** | memory-keeper | findings promoted to NECTAR | Partial (findings solid) |
| **Crystallization** | faerie | HONEY entries + coc.jsonl promote | Yes (permanent knowledge) |
| **Export** | system | signed bundle + B2 upload | **YES** (complete evidence) |

---

## Comparison to Traditional Auditing

| Aspect | Traditional | Forensic System |
|--------|-----------|-----------------|
| **When is audit trail recorded?** | After the fact | Real-time, every action |
| **Who can see the trail?** | Auditor only | Everyone (git history) |
| **Can you hide steps?** | Yes (edit notes) | No (hash chain breaks) |
| **Proof of integrity** | Auditor certification | Cryptographic + chain |
| **Court acceptance** | Depends on auditor credibility | Business record (FRE 803(6)) |

---

## Next Steps

1. **Read:** `forensic-system-design.md` for full architecture
2. **Implement:** `forensic-implementation-checklist.md` for step-by-step setup
3. **Reference:** `forensic-schema-reference.json` for JSON structures
4. **Deploy:** Integrate into `/faerie` skill and agent onboarding

---

**Status:** ACTIVE  
**Last Updated:** 2026-04-07  
**Document Version:** 1.0
