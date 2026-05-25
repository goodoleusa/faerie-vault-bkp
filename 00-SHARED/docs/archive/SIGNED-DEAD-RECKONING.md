# Signed Dead Reckoning Architecture — 2026-04-06

## Decision: Blocking vs Advisory on Provenance Failure

**Middle path (ADOPTED):** Block on HIGH investigation tasks. Advisory on all other categories.
- HIGH + broken provenance → route to security-auditor (read-only) for manual re-sign → requeue
- Infrastructure / training / meta / publishing → emit FLAG pri=HIGH, proceed with "unverified provenance" tag

## Key Management

One GPG subkey per agent type (ed25519, no passphrase for automation):
- Private: `~/.claude/agents/keys/{agent-type}.gpg` (gitignored, mode 600)
- Public:  `~/.claude/agents/keys/{agent-type}.pub.gpg` (committable)
- Keyring: `~/.claude/agents/keys/faerie-keyring.gpg` (all public keys)

Key spec:
```
%no-protection
Key-Type: EDDSA
Key-Curve: ed25519
Name-Real: evidence-analyst
Name-Email: evidence-analyst@faerie
Expire-Date: 0
```

Key rotation: only on compromise. New `## Last Training` version strings do NOT rotate the key.
Priority agents to key first: `evidence-curator`, `research-analyst`, `data-scientist`, `data-engineer`, `report-writer`

## Signed Manifest Schema

```json
{
  "task_id": "task-20260406-120000-abcd",
  "agent": "evidence-analyst",
  "agent_version": "2026-04-06",
  "findings": ["..."],
  "output_path": "scripts/audit_results/evidence_RUN007.json",
  "dashboard_line": "...",
  "signature": {
    "signer": "evidence-analyst@2026-04-06",
    "payload_fields": ["task_id", "agent", "agent_version", "findings", "output_path"],
    "payload_hash": "sha256:...",
    "pgp_sig": "-----BEGIN PGP SIGNATURE-----\n...",
    "key_fingerprint": "...",
    "signed_at": "2026-04-06T14:23:00Z",
    "warning": null
  }
}
```

Graceful degrade: if no key exists for agent type, `pgp_sig=null`, `warning="no agent key — hash only"`.
Chain keeps moving; weakness is surfaced.

## Context Bundle Provenance Schema

```json
{
  "context_bundle": {
    "highest_value": "...",
    "done_looks_like": "...",
    "source_files": ["..."],
    "provenance": {
      "source_task": "task-20260406-120000-abcd",
      "source_agent": "evidence-analyst@2026-04-06",
      "source_manifest_path": "scripts/audit_results/evidence_RUN007.json",
      "source_payload_hash": "sha256:...",
      "source_signature_hash": "sha256:...",
      "chain_depth": 1
    }
  }
}
```

`chain_depth` increments per chained task. Task C sees depth=2 and can walk back to origin.

## queue_ops.py Integration Points

**Point 1 — `cmd_complete`: accept manifest + sign + inject provenance**
```
def cmd_complete(task_id: str, manifest_path: str = "", agent_version: str = "")
```
After `t["status"] = "completed"`:
1. Call `_sign_manifest(manifest_path, agent_type, agent_version)`
2. Store `t["output_manifest"]` and `t["output_hash"]`
3. Inject `provenance` block into next_on_success context_bundle

**Point 2 — `_sign_manifest()` helper**
- Canonical payload: `json.dumps(payload, sort_keys=True, separators=(',',':'))`
- HMAC-SHA256 using `.forensic_hmac_key` if no GPG key (reuses `forensic_coc.py` pattern)
- Full PGP sign if `~/.claude/agents/keys/{agent-type}.gpg` exists
- Writes `signature` block to manifest in-place (append only)

**Point 3 — `cmd_fail`: sign failure manifests too**
Signed failure proves "agent V1 could not attribute this; V2 found it" — OTJ improvement forensics.

**Point 4 — argparse additions**
```
complete TASK_ID --manifest PATH --agent-version 2026-04-06
```

**Existing state (confirmed by audit):**
- Lines 1-80: no signing hooks
- Lines 150-166: `_enforce_dead_reckoning_bundle` — structural only, no provenance
- Lines 308-311: `next_on_success` / `next_on_failure` fields exist
- Lines 356-378: `cmd_complete` auto-queues success chain (no manifest arg yet)
- Lines 468-533: archive COC logs queue-level SHA256 only

## 3-Step Implementation Plan

### Step 1: Key store + gen script + verify-chain.py (1-2h)
- Create `~/.claude/agents/keys/` with `.gitignore` blocking private keys
- Write `gen-agent-key.sh`: generates ed25519 key, exports pub, appends to keyring
- Generate keys for 5 priority agents
- Write `verify-chain.py`: walks provenance chain, verifies each hash + sig
- Test: generate → sign test payload → verify → roundtrip confirmed

### Step 2: `_sign_manifest` + `cmd_complete` extension (2-3h)
- Add `_sign_manifest()` to `queue_ops.py` with graceful degrade
- Extend `cmd_complete`: accept `--manifest`, call `_sign_manifest`, store `output_hash`
- Extend next_on_success: inject `provenance` block when `output_hash` present
- Test: `queue_ops.py complete TASK_ID --manifest path/to/manifest.json --agent-version 2026-04-06`

### Step 3: Agent lifecycle rule + verify-on-claim (1-2h)
- Add to `agent-lifecycle.md` §1 Startup: if `context_bundle.provenance` present, verify before proceeding
- HIGH priority: block on failure → security-auditor re-sign → requeue
- Add `agent_version` to manifest return template in each agent card
- Test: full A → B → C chain with verified provenance at each link

## Related files
- `queue_ops.py`: `~/.claude/hooks/state/queue_ops.py`
- `forensic_coc.py`: `~/.claude/hooks/forensic_coc.py` (HMAC pattern to reuse)
- `note_sign.py`: `/mnt/d/0local/gitrepos/faerie2/scripts/note_sign.py` (ed25519 + agent_author role)
- `verify-chain.py`: to be written at `~/.claude/scripts/verify-chain.py`
