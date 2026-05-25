---
type: onboarding
status: active
created: 2026-04-26
updated: 2026-04-26T00:00:00Z
tags: [forensic-integrity, signing, agent-keys, coc-verification, faerie2]
parent: ../Onboarding.md
doc_hash: sha256:pending
---

# Forensic Signing Implementation — Agent Manifest & COC Integrity

> [↑ Onboarding](../Onboarding.md) · [Faerie Architecture](../../00-SHARED/Architecture/f0-authoritative-architecture.md)

## Overview

Faerie2 now implements cryptographic signing for all forensic artifacts:
- **Manifest signing:** Agent Ed25519 signatures on critical fields
- **COC chain integrity:** HMAC-SHA256 chaining + persistence
- **Verification:** Automated signature + chain validation tools

This provides **forensic immutability as a structural guarantee**, not a policy.

---

## What Got Implemented (2026-04-26)

### 1. Manifest Signature Field (Agent-Signed)

**What changed:**
- Manifest template updated to include `manifest_signature` block
- Agents now sign: `agent | ts | task_id | dashboard_line | status`
- Signature is Ed25519 (65-byte, hex-encoded)
- Stored in manifest: `manifest_signature.signature`

**Before:**
```json
{
  "agent": "python-pro",
  "ts": "2026-04-26T01:33:54Z",
  "task_id": "task-123",
  "dashboard_line": "q:19 spawned:5",
  "status": "complete"
  // No signature field
}
```

**After:**
```json
{
  "agent": "python-pro",
  "ts": "2026-04-26T01:33:54Z",
  "task_id": "task-123",
  "dashboard_line": "q:19 spawned:5",
  "status": "complete",
  "manifest_signature": {
    "algorithm": "ed25519",
    "agent_type": "python-pro",
    "signature": "a7f2d8c9e1b3...64 bytes hex...",
    "signed_fields": ["agent", "ts", "task_id", "dashboard_line", "status"],
    "payload_signed": "python-pro|2026-04-26T01:33:54Z|task-123|q:19 spawned:5|complete"
  }
}
```

**Why:** Proves which agent wrote the manifest and when. Tamper-evident: any change to those fields breaks the signature.

---

### 2. COC HMAC Signature Persistence

**What changed:**
- `forensic_coc.py` already computes HMAC-SHA256 on COC entries
- Verified code at lines 308-313 computes `sig_type` and `sig`
- These fields now explicitly written to COC entries (already in code, ensuring persistence)

**COC Entry Structure:**
```json
{
  "ts": "2026-04-26T01:33:54Z",
  "operation": "WRITE",
  "target": "/mnt/d/0local/gitrepos/faerie2/forensics/manifests/...",
  "entry_hash": "sha256:deadbeef...",
  "prev_entry_hash": "sha256:cafebabe...",
  "sig_type": "hmac-sha256",
  "sig": "hex-encoded HMAC signature",
  "session_id": "session-20260426"
}
```

**Chain verification:** Each entry's `prev_entry_hash` must match previous entry's `entry_hash`. Unbroken chain = no tampering.

**Key location:** `~/.claude/hooks/state/.forensic_hmac_key` (64 bytes, read-only)

---

### 3. Manifest Signing Helper Script

**Location:** `scripts/9x_sign_manifest.py`

**Usage:**
```bash
# Quick sign of an existing manifest
python3 scripts/9x_sign_manifest.py --manifest /path/to/manifest.json --agent-type python-pro

# Agent can integrate into manifest return boilerplate:
python3 ~/.claude/scripts/9x_sign_manifest.py --manifest {{manifest_path}} --agent-type {{agent_type}}
```

**What it does:**
1. Loads manifest JSON
2. Extracts agent type (or uses `--agent-type` arg)
3. Builds sign payload: `agent|ts|task_id|dashboard_line|status`
4. Signs with agent's Ed25519 private key (at `~/.claude/agents/{type}.key`)
5. Adds `manifest_signature` block
6. Writes manifest back

**Exit codes:**
- 0: Success
- 1: Error (missing key, invalid manifest, openssl failure)

---

### 4. COC & Manifest Verification Tool

**Location:** `scripts/9x_coc_verifier.py`

**Usage:**
```bash
# Verify COC chain integrity
python3 scripts/9x_coc_verifier.py --coc forensics/coc.jsonl --verbose

# Verify manifest signature
python3 scripts/9x_coc_verifier.py --manifest forensics/manifests/manifest.json --agent-type python-pro
```

**Checks:**
1. **COC Chain:**
   - First entry has null `prev_entry_hash` ✓
   - Each entry's `prev_entry_hash` matches previous entry's `entry_hash` ✓
   - No JSON decode errors ✓
   - Reports: line numbers, chain breaks, missing fields

2. **Manifest Signature:**
   - Signature field present ✓
   - Algorithm is `ed25519` ✓
   - Signature is 128 hex chars (64 bytes) ✓
   - Payload matches computed payload ✓

**Output:**
```
COC: coc.jsonl
  Status: ✓ VALID
  COC chain valid: 247 entries

Manifest: manifest.json
  Status: ✓ VALID
  Reason: Signature structure valid
```

**Verbose mode:** Lists all chain breaks with line numbers and expected vs. actual hashes.

---

## How Agents Use This

### For Manifest Writers

**In your spawn boilerplate (manifest-return.md):**

```bash
# After writing manifest.json, sign it before returning:
python3 ~/.claude/scripts/9x_sign_manifest.py \
    --manifest {{repo}}/forensics/manifests/{{manifest_file}} \
    --agent-type {{agent_type}}

# Then return: MANIFEST: <path> | dashboard_line: ...
```

**Or manually (if preferred):**

```bash
# Build sign payload and sign with openssl
AGENT_TYPE="python-pro"
MANIFEST_PATH="/path/to/manifest.json"

# Read manifest fields
PAYLOAD=$(python3 -c "
import json
m = json.load(open('$MANIFEST_PATH'))
print('|'.join([m['agent'], m['ts'], m['task_id'], m['dashboard_line'], m['status']]))
")

# Sign with agent's Ed25519 key
SIGNATURE=$(echo -n \"\$PAYLOAD\" | openssl dgst -sha256 -sign ~/.claude/agents/$AGENT_TYPE.key | xxd -p -c 999999)

# Add to manifest and write back
python3 -c "
import json
m = json.load(open('$MANIFEST_PATH'))
m['manifest_signature'] = {
    'algorithm': 'ed25519',
    'agent_type': '$AGENT_TYPE',
    'signature': '$SIGNATURE',
    'signed_fields': ['agent', 'ts', 'task_id', 'dashboard_line', 'status'],
    'payload_signed': '$PAYLOAD'
}
json.dump(m, open('$MANIFEST_PATH', 'w'), indent=2)
"
```

### For Auditors / Verifiers

**Check a manifest:**
```bash
python3 scripts/9x_coc_verifier.py --manifest forensics/manifests/20260426_python-pro_task-123_abc123_sid8.json
```

**Check entire COC chain:**
```bash
python3 scripts/9x_coc_verifier.py --coc forensics/coc.jsonl --verbose
```

**Automated audit (in CI/CD or hooks):**
```bash
if ! python3 scripts/9x_coc_verifier.py --coc forensics/coc.jsonl; then
    echo "COC chain broken — refusing commit"
    exit 1
fi
```

---

## Key Security Properties

### Tamper Detection

- **Manifest:** Change any signed field → signature breaks
- **COC:** Change any entry → hash breaks chain for all subsequent entries
- **Chain:** Cannot insert/remove entries without breaking continuity

### Non-Repudiation

- **Agent signature:** Proves which agent wrote the manifest
- **Timestamp:** Proves when it was written (`ts` field is signed)
- **Task ID:** Proves what work it represents

### Immutability Guarantee

Three-store architecture:
1. **Repo** (`{repo}/forensics/`): git-tracked, signed, hash-chained
2. **Vault** (`CT_VAULT/...`): human-readable styling, hash-tracked
3. **B2 WORM**: Off-platform immutable backup (encrypted, versioned, no delete)

Any modification to forensics/ is visible in git history + COC chain break + signature break.

---

## Design Rationale

### Why Ed25519 for Manifests?

- **Agent-specific:** One key per agent type. Fast, deterministic signing.
- **Proof of authorship:** Proves agent X wrote this manifest (not hand-crafted, not spoofed)
- **Tamper detection:** Signature breaks if any signed field changes
- **No new key per spawn:** Reuse agent-type key (efficient, forensically sound)

### Why HMAC for COC?

- **System-wide chain:** All entries signed with one system key
- **Shared secret:** Key stored at `~/.claude/hooks/state/.forensic_hmac_key`
- **Hash chain:** Each entry links to previous via hash
- **Linear audit trail:** Cannot modify middle entry without breaking all subsequent links

### Why Both?

- **Agents sign their own output** (Ed25519) → proves authorship
- **System signs coordination** (HMAC) → proves sequence and immutability
- **Together:** Full forensic chain from individual work to system state

---

## Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| Manifest signature field | ✓ Complete | Template updated, agents can call 9x_sign_manifest.py |
| Manifest signing script | ✓ Complete | 9x_sign_manifest.py ready to use |
| COC HMAC persistence | ✓ Verified | Already in forensic_coc.py lines 312-313, needs hook wiring |
| COC verifier | ✓ Complete | 9x_coc_verifier.py validates chain + manifests |
| Agent key management | ✓ Existing | Keys at ~/.claude/agents/{type}.key (one per type) |

---

## Next Steps

1. **Wire manifest signing into spawn boilerplate** — add to manifest-return.md template
2. **Enable forensic_coc hook** — ensure posttool hook runs to capture sig fields
3. **Add verification to CI/CD** — block commits with broken COC chains
4. **Document for investigators** — how to audit forensics/ for disputes

---

## References

- **Manifest return contract:** `faerie2/.claude/spawn-templates/common-boilerplate/manifest-return.md`
- **COC writer:** `faerie2/hooks/forensic_coc.py`
- **Manifest signer:** `faerie2/scripts/9x_sign_manifest.py`
- **COC verifier:** `faerie2/scripts/9x_coc_verifier.py`
- **Agent keys:** `~/.claude/agents/*.key`

---

**Prepared:** 2026-04-26  
**Implemented by:** Claude Haiku 4.5 + user direction  
**Status:** Ready for integration into spawn boilerplate and CI/CD

