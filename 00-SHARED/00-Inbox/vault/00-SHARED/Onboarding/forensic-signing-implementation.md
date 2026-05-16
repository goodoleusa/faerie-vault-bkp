---
type: onboarding
status: active
created: 2026-04-26
tags: [forensic-integrity, signing, agent-keys, coc-verification, faerie2]
parent: ../Onboarding.md
---

# Forensic Signing Implementation — Agent Manifest & COC Integrity

> [Faerie Architecture](../Architecture/f0-authoritative-architecture.md)

## Overview

Faerie2 now implements cryptographic signing for all forensic artifacts:
- **Manifest signing:** Agent Ed25519 signatures on critical fields
- **COC chain integrity:** HMAC-SHA256 chaining + persistence
- **Verification:** Automated signature + chain validation tools

---

## What Got Implemented (2026-04-26)

### 1. Manifest Signature Field (Agent-Signed)

Agents now sign: `agent | ts | task_id | dashboard_line | status`

**Schema:**
```json
{
  "manifest_signature": {
    "algorithm": "ed25519",
    "agent_type": "python-pro",
    "signature": "hex-encoded 64-byte signature",
    "signed_fields": ["agent", "ts", "task_id", "dashboard_line", "status"],
    "payload_signed": "python-pro|2026-04-26T01:33:54Z|task-123|q:19|complete"
  }
}
```

**Why:** Proves which agent wrote the manifest. Tamper-evident: any change breaks the signature.

---

### 2. COC HMAC Signature Persistence

COC entries now include `sig_type` and `sig` (HMAC-SHA256 hash-chained).

**Chain verification:**
- First entry has null `prev_entry_hash`
- Each entry's `prev_entry_hash` matches previous entry's `entry_hash`
- Unbroken chain = no tampering

---

### 3. Signing & Verification Tools

**Sign a manifest:**
```bash
python3 scripts/9x_sign_manifest.py --manifest <path> --agent-type <type>
```

**Verify COC or manifest:**
```bash
python3 scripts/9x_coc_verifier.py --coc forensics/coc.jsonl --verbose
python3 scripts/9x_coc_verifier.py --manifest forensics/manifests/manifest.json
```

---

## How to Use

### Agents: Add Signing to Manifest Return

```bash
# After writing manifest.json:
python3 ~/.claude/scripts/9x_sign_manifest.py \
    --manifest {{manifest_path}} \
    --agent-type {{agent_type}}

# Then return: MANIFEST: <path> | dashboard_line: ...
```

### Auditors: Verify Forensics

```bash
# Quick check
python3 scripts/9x_coc_verifier.py --coc forensics/coc.jsonl

# Detailed report
python3 scripts/9x_coc_verifier.py --coc forensics/coc.jsonl --verbose
```

---

## Key Properties

✓ **Tamper Detection:** Change any signed field → signature breaks  
✓ **Non-Repudiation:** Agent signature proves authorship + timestamp  
✓ **Immutability:** COC chain breaks if any entry modified  
✓ **Audit Trail:** Every operation logged, signed, hash-chained  

---

## Files

| File | Purpose |
|------|---------|
| `scripts/9x_sign_manifest.py` | Sign manifests with Ed25519 |
| `scripts/9x_coc_verifier.py` | Verify COC chains + manifests |
| `~/.claude/agents/*.key` | Agent Ed25519 private keys |
| `~/.claude/hooks/state/.forensic_hmac_key` | System HMAC key |

---

**Status:** ✓ Ready for integration into spawn boilerplate and CI/CD

