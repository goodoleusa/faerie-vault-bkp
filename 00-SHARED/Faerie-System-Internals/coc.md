---
type: system-sidecar
subtype: data-file
status: active
date: 2026-05-20
tags: [system, coc, forensics, chain-of-custody, hash, immutable, sidecar]
memory_lane: system
promotion_state: permanent
N:
  - "[[00-Home]]"
  - "[[Flow-Cryptographic]]"
E:
  - "[[manifest-index]]"
  - "[[mission-graph]]"
S:
  - "[[Flow-Memory]]"
---

# coc.jsonl

System sidecar for `forensics/coc.jsonl` — the Chain of Custody log.

**Role:** Immutable, hash-chained audit trail of every durable write in the system.  
**Format:** newline-delimited JSON — one entry per write event.  
**Location:** `{repo}/forensics/coc.jsonl`  
**Integrity:** SHA-256 hash-chained — each entry records the hash of the previous entry. Any tampering breaks the chain.

## Fields per entry

| Field | Type | Description |
|---|---|---|
| `seq` | int | Monotonic sequence number |
| `ts` | ISO-8601 | Timestamp (UTC) |
| `task_id` | string | Task that produced this artifact |
| `mission` | string | Semantic mission |
| `file_path` | string | Canonical path written |
| `sha256` | string | SHA-256 of file content |
| `prev_hash` | string | SHA-256 of previous COC entry |
| `agent_type` | string | Archetype that wrote it |
| `session_id` | string | 8-char session identifier |

## Verification

```bash
python3 scripts/verify_coc.py forensics/coc.jsonl
# → 1,270 entries, 0 hash mismatches ✅
```

## Write path

Every agent write → `0x_promote_to_forensics.py` → symlink to canonical → `0x_coc_finalizer.py` appends entry → `5x_b2_realtime_uploader.py` queues WORM backup.

## Related

- [[Flow-Cryptographic]] — cryptographic flow (hash chain, HMAC verification)
- [[Flow-Memory]] — full crystallization pipeline
- [[manifest-index]] — in-flight tracking companion
