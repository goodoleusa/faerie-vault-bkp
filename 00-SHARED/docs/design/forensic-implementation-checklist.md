# Forensic Implementation Checklist — Step-by-Step Setup

**Date:** 2026-04-07  
**Audience:** System architects, implementation engineers  
**Purpose:** Hands-on checklist for deploying forensic COC in a new investigation  

---

## Phase 0: Pre-Flight (Before Any Work Starts)

### Setup Folder Structure

- [ ] Create investigation folder:
  ```bash
  mkdir -p ~/.claude/memory/investigations/{inv_id}/forensics
  mkdir -p ~/.claude/memory/investigations/{inv_id}/forensics/manifests
  mkdir -p ~/.claude/memory/investigations/{inv_id}/forensics/exports
  ```

- [ ] Create vault mirror:
  ```bash
  mkdir -p $CT_VAULT/00-SHARED/Design-Narratives/{inv_id}
  ```

- [ ] Create repo structure (if not present):
  ```bash
  mkdir -p {repo}/forensics/manifests
  mkdir -p {repo}/forensics/exports
  touch {repo}/forensics/coc.jsonl
  touch {repo}/forensics/audit-log.md
  ```

### Initialize Git

- [ ] Add forensics/ to git:
  ```bash
  git add {repo}/forensics/
  git commit -m "chore: initialize forensic COC infrastructure"
  ```

- [ ] Verify .gitignore:
  ```bash
  # Should NOT ignore:
  # - forensics/coc.jsonl
  # - forensics/audit-log.md
  # - forensics/manifests/
  
  # Should ignore:
  # - forensics/exports/ (reconstructible)
  # - forensics/.session-*.json (ephemeral)
  ```

### Prepare PGP Keys

- [ ] Verify PGP key pair exists:
  ```bash
  gpg --list-keys
  ```

- [ ] If not: generate one:
  ```bash
  gpg --full-generate-key
  # Use: RSA, 4096 bits, 5-year expiry, name + email
  ```

- [ ] Export public key:
  ```bash
  gpg --armor --export {email} > {repo}/forensics/forensic-pgp.pub
  git add {repo}/forensics/forensic-pgp.pub
  ```

---

## Phase 1: Genesis (Baseline Snapshot)

### Generate Genesis Manifest

- [ ] Run genesis manifest generator:
  ```bash
  python3 scripts/4a_hash_guardian.py --phase genesis --output {repo}/forensics/manifests/genesis_manifest.json
  ```

  This produces:
  ```json
  {
    "manifest_id": "genesis",
    "ts": "2026-04-07T14:23:47Z",
    "file_count": 658,
    "total_size_bytes": 5368709120,
    "files": [
      {
        "path": "raw/evidence_001.pdf",
        "sha256": "abc123...",
        "size_bytes": 1024,
        "mtime": "2026-04-06T10:00:00Z"
      },
      ...
    ]
  }
  ```

- [ ] Verify manifest integrity:
  ```bash
  python3 ~/.claude/scripts/9c_forensic_integrity.py --verify-manifest {repo}/forensics/manifests/genesis_manifest.json
  ```

- [ ] Store manifest hash for audit trail:
  ```bash
  MANIFEST_HASH=$(sha256sum {repo}/forensics/manifests/genesis_manifest.json | cut -d' ' -f1)
  echo $MANIFEST_HASH  # Save for COC entry
  ```

### Create Genesis COC Entry

- [ ] Append to coc.jsonl:
  ```bash
  cat >> {repo}/forensics/coc.jsonl << 'EOF'
  {
    "entry_id": "COC-00001",
    "type": "genesis",
    "ts": "2026-04-07T14:23:47Z",
    "actor": "system",
    "action": "init_investigation",
    "scope": "investigation-{inv_id}",
    "data": {
      "manifest_file": "forensics/manifests/genesis_manifest.json",
      "manifest_hash": "{MANIFEST_HASH}",
      "file_count": 658,
      "total_size_gb": 5.37
    },
    "entry_hash": "{SHA256_OF_THIS_ENTRY}",
    "prev_entry_hash": "genesis",
    "sig": "UNSIGNED_BASELINE"
  }
  EOF
  ```

- [ ] Calculate entry_hash:
  ```bash
  python3 << 'HASH_EOF'
  import json, hashlib
  entry = {
    "entry_id": "COC-00001",
    "type": "genesis",
    "ts": "2026-04-07T14:23:47Z",
    "actor": "system",
    "action": "init_investigation",
    "scope": "investigation-{inv_id}",
    "data": {...}
  }
  entry_hash = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
  print(entry_hash)
  HASH_EOF
  ```

- [ ] Update coc.jsonl with correct entry_hash

### Create Genesis Audit Log Entry

- [ ] Append to audit-log.md:
  ```markdown
  ## FSL-001: Genesis Initialization

  **Timestamp:** 2026-04-07T14:23:47Z  
  **Actor:** system  
  **Action:** Initialize investigation {inv_id}  

  - Created manifest: genesis_manifest.json (658 files, 5.37 GB)
  - Manifest hash: {MANIFEST_HASH}
  - Hash algorithm: SHA256
  - Baseline established — all subsequent changes will be logged
  - Committing to git now for wall-clock timestamp

  See `forensics/coc.jsonl` entry COC-00001 for cryptographic record.
  ```

### Commit

- [ ] Stage and commit:
  ```bash
  git add {repo}/forensics/
  git commit -m "feat: forensic COC genesis — baseline investigation {inv_id}" \
    -m "Files: 658 | Size: 5.37 GB | Manifest: genesis_manifest.json" \
    -m "Hash: {MANIFEST_HASH}"
  ```

- [ ] Verify commit is permanent:
  ```bash
  git log --oneline -1
  ```

---

## Phase 2: Ingest (Add Evidence)

### Before Ingest

- [ ] Record pre-ingest state:
  ```bash
  FSL_NUM=002
  echo "## FSL-$FSL_NUM: Ingest Phase 1 Start" >> {repo}/forensics/audit-log.md
  echo "" >> {repo}/forensics/audit-log.md
  echo "**Timestamp:** $(date -u +'%Y-%m-%dT%H:%M:%SZ')" >> {repo}/forensics/audit-log.md
  ```

### During Ingest

- [ ] Data-engineer ingests evidence and logs:
  ```bash
  python3 scripts/1a_ingest_remaining.py \
    --output {repo}/forensics/manifests/rawdata_manifest_{RUN}.json \
    --log {repo}/forensics/audit-log.md
  ```

  Script should:
  - Hash each file BEFORE and AFTER ingest
  - Create manifest with hashes
  - Append to audit-log.md
  - Return file count + total size

- [ ] Data-engineer reports metrics:
  ```
  Files added: 127
  Total size: 342 MB
  Hash collisions: 0
  Time: 23s
  Manifest: rawdata_manifest_RUN-005.json
  ```

### After Ingest

- [ ] Create COC entry for ingest phase:
  ```bash
  cat >> {repo}/forensics/coc.jsonl << 'EOF'
  {
    "entry_id": "COC-00002",
    "type": "ingest",
    "ts": "2026-04-07T15:45:22Z",
    "actor": "data-engineer",
    "action": "ingest_phase_5",
    "scope": "investigation-{inv_id}",
    "data": {
      "files_added": 127,
      "total_size_mb": 342,
      "manifest_file": "forensics/manifests/rawdata_manifest_RUN-005.json",
      "manifest_hash": "{MANIFEST_HASH}",
      "hash_collisions": 0,
      "phase_duration_seconds": 23
    },
    "entry_hash": "{SHA256_OF_THIS_ENTRY}",
    "prev_entry_hash": "COC-00001_HASH",
    "sig": "UNSIGNED_PHASE_RECORD"
  }
  EOF
  ```

- [ ] Append to audit-log.md:
  ```markdown
  - Files ingested: 127
  - New manifest: rawdata_manifest_RUN-005.json
  - Manifest hash: {MANIFEST_HASH}
  - Phase duration: 23s
  - Hash collisions: 0
  - Next action: verification before commit
  ```

### Verification Before Commit

- [ ] Run integrity check:
  ```bash
  python3 ~/.claude/scripts/9c_forensic_integrity.py \
    --verify \
    --inv {inv_id}
  ```

  Should output:
  ```
  ✓ coc.jsonl: hash chain valid
  ✓ All referenced files exist
  ✓ All manifest hashes match current files
  ✓ No orphaned COC entries
  ✓ COC integrity: PASSED
  ```

- [ ] Commit immediately (do NOT batch with analysis):
  ```bash
  git add {repo}/forensics/
  git commit -m "feat: ingest phase 5 — 127 new files added"
  ```

---

## Phase 3: Analysis (Agents Produce Findings)

### Agent Instrumentation

- [ ] Each agent run logs to reasoning.jsonl:
  ```json
  {
    "agent": "data-scientist",
    "phase": "STAT_ANALYST",
    "run_id": "run-20260407-003",
    "ts": "2026-04-07T16:12:33Z",
    "input": {
      "data_file": "scripts/audit_results/analysis_input.json",
      "data_hash": "sha256:input123..."
    },
    "output": {
      "findings_file": "scripts/audit_results/stat_results.json",
      "findings_hash": "sha256:output456..."
    },
    "status": "success",
    "note": "Hypothesis 1 confidence → 0.87 (+0.05)"
  }
  ```

- [ ] Append to reasoning.jsonl:
  ```bash
  echo '{"agent":"data-scientist",...}' >> ~/.claude/memory/investigations/{inv_id}/reasoning.jsonl
  ```

### Finding Promotion

- [ ] When a finding is validated (agent → memory-keeper):
  - Do NOT append to coc.jsonl yet
  - Promote to NECTAR.md first
  - Memory-keeper records: "Finding promoted, confidence 0.87"

### No COC Entry for Analysis

- [ ] Reasoning logs stay in reasoning.jsonl (not in coc.jsonl)
  - Exception: Major findings that are PROMOTED get a coc.jsonl entry

---

## Phase 4: Validation (Promote to NECTAR)

### When a Finding is Promoted

- [ ] Memory-keeper appends to NECTAR.md:
  ```markdown
  ## Sprint 2026-04-07 — Phase Analysis

  Hypothesis confidence updates:
  - H1 (DOGE credential misuse) → 0.87 (+0.05) [via stat_results.json, Bonferroni p<0.05]
  ```

- [ ] Create COC entry: type=promote
  ```bash
  cat >> {repo}/forensics/coc.jsonl << 'EOF'
  {
    "entry_id": "COC-00003",
    "type": "promote",
    "ts": "2026-04-07T16:45:11Z",
    "actor": "memory-keeper",
    "action": "promote_finding",
    "scope": "investigation-{inv_id}",
    "data": {
      "finding": "H1 confidence → 0.87",
      "source": "reasoning.jsonl",
      "nectar_entry": "H1-2026-04-07-stat",
      "confidence": 0.87
    },
    "entry_hash": "{SHA256}",
    "prev_entry_hash": "COC-00002_HASH",
    "sig": "UNSIGNED_PROMOTION"
  }
  EOF
  ```

- [ ] Append to audit-log.md:
  ```markdown
  ## FSL-003: Finding Promotion

  **Timestamp:** 2026-04-07T16:45:11Z  
  **Actor:** memory-keeper  
  **Finding:** H1 confidence updated to 0.87  
  **Source:** stat_results.json (p<0.05)  
  **Promotion level:** NECTAR (validated)  
  ```

---

## Phase 5: Crystallization (Integrate Knowledge)

### When HONEY is Updated

- [ ] Faerie reads N NECTAR entries (all related findings)

- [ ] Faerie integrates into 1-3 HONEY bullets

- [ ] Create COC entry: type=crystallize
  ```bash
  cat >> {repo}/forensics/coc.jsonl << 'EOF'
  {
    "entry_id": "COC-00004",
    "type": "crystallize",
    "ts": "2026-04-07T17:30:22Z",
    "actor": "faerie",
    "action": "crystallize_knowledge",
    "scope": "investigation-{inv_id}",
    "data": {
      "sources": [
        "NECTAR:H1-2026-04-07-stat",
        "NECTAR:H2-2026-04-05-cert"
      ],
      "result": "fnd00042: DOGE/Treasury temporal signals 0.87 confidence",
      "result_hash": "sha256:honey123..."
    },
    "entry_hash": "{SHA256}",
    "prev_entry_hash": "COC-00003_HASH",
    "sig": "UNSIGNED_CRYSTALLIZATION"
  }
  EOF
  ```

- [ ] Commit HONEY.md + coc.jsonl:
  ```bash
  git add ~/.claude/memory/HONEY.md {repo}/forensics/coc.jsonl
  git commit -m "feat: crystallize H1 confidence findings into fnd00042"
  ```

---

## Phase 6: Export (Prepare for Court)

### Generate Evidence Bundle

- [ ] Collect all forensic logs:
  ```bash
  python3 scripts/forensic_coc.py export \
    --inv {inv_id} \
    --format court \
    --output {repo}/forensics/exports/evidence_export_2026-04-07.tar.gz
  ```

  Output:
  ```
  evidence_export_2026-04-07/
  ├── coc.jsonl (complete)
  ├── audit-log.md (complete)
  ├── manifests/
  │   ├── genesis_manifest.json
  │   ├── rawdata_manifest_RUN-005.json
  │   └── evidence_manifest.json
  ├── reasoning.jsonl (for replayability)
  ├── INTEGRITY_REPORT.txt (verification details)
  └── COURT_AFFIDAVIT.txt (prepared for filing)
  ```

### Verify Bundle

- [ ] Check integrity:
  ```bash
  python3 ~/.claude/scripts/9c_forensic_integrity.py \
    --verify-export {repo}/forensics/exports/evidence_export_2026-04-07.tar.gz
  ```

  Should output:
  ```
  ✓ All files present
  ✓ All hashes verified (bit-for-bit match)
  ✓ COC chain unbroken
  ✓ Export integrity: PASSED
  ```

### Sign Bundle

- [ ] PGP-sign the bundle:
  ```bash
  gpg --armor --detach-sign {repo}/forensics/exports/evidence_export_2026-04-07.tar.gz
  ```

  Creates: `evidence_export_2026-04-07.tar.gz.asc`

- [ ] Verify signature:
  ```bash
  gpg --verify evidence_export_2026-04-07.tar.gz.asc evidence_export_2026-04-07.tar.gz
  ```

### Upload to B2 WORM

- [ ] Upload to B2:
  ```bash
  b2 upload-file \
    --no-progress \
    cybertemplate-evidence \
    {repo}/forensics/exports/evidence_export_2026-04-07.tar.gz \
    evidence_export_2026-04-07.tar.gz
  ```

  Note: WORM protection prevents deletion

- [ ] Verify upload:
  ```bash
  b2 list-file-versions cybertemplate-evidence evidence_export_2026-04-07.tar.gz
  ```

### Record Export in COC

- [ ] Append to coc.jsonl:
  ```bash
  cat >> {repo}/forensics/coc.jsonl << 'EOF'
  {
    "entry_id": "COC-00005",
    "type": "export",
    "ts": "2026-04-07T18:15:47Z",
    "actor": "system",
    "action": "export_for_court",
    "scope": "investigation-{inv_id}",
    "data": {
      "bundle_file": "evidence_export_2026-04-07.tar.gz",
      "bundle_hash": "sha256:export123...",
      "signature": "PGP_SIGNATURE_VALID",
      "pgp_key": "0x{KEY_FINGERPRINT}",
      "b2_location": "s://cybertemplate-evidence/evidence_export_2026-04-07.tar.gz",
      "b2_worm_enabled": true
    },
    "entry_hash": "{SHA256}",
    "prev_entry_hash": "COC-00004_HASH",
    "sig": "PGP_SIGNED"
  }
  EOF
  ```

- [ ] Final commit:
  ```bash
  git add {repo}/forensics/
  git commit -m "feat: export court evidence bundle — verified + signed + B2 WORM"
  ```

---

## Final Verification Checklist

Before declaring forensic setup complete:

- [ ] Genesis manifest created and committed
- [ ] All ingest phases logged to coc.jsonl
- [ ] All hash chains verified (no gaps)
- [ ] All findings promoted from reasoning → NECTAR → HONEY
- [ ] All COC entries have valid cryptographic hashes
- [ ] No forensics/ files have been modified (only appended)
- [ ] All changes committed to git
- [ ] Evidence bundle exported, signed, and uploaded to B2 WORM
- [ ] forensic_integrity.py verify passes (100%)
- [ ] Legal team has B2 link + PGP key

---

## Troubleshooting

### Scenario: Hash Mismatch on Re-Verify

**Problem:** `forensic_integrity.py verify` reports file hash doesn't match manifest.

**Solution:**
1. Get original hash from genesis_manifest.json
2. Retrieve file from B2 WORM backup (immutable)
3. Compare: `sha256sum file_from_b2`
4. If different: file was corrupted locally
5. Append FSL entry: "File recovery: {name} redeemed from B2"
6. Continue (do not patch coc.jsonl)

### Scenario: COC Entry Hash Chain Broken

**Problem:** `forensic_integrity.py verify` reports entry #42 hash doesn't match expected.

**Solution:**
1. **DO NOT FIX** — chain is broken means tampering occurred
2. Append FSL entry: "CRITICAL: COC chain broken at entry {N} — investigation compromised"
3. Create NEW investigation with fresh genesis
4. Preserve NECTAR (validated findings) in new investigation
5. Document chain break in forensic export for court filing
6. File incident report

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-07  
**Status:** APPROVED for production use
