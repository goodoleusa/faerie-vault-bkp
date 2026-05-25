---
type: reference
status: active
tags: [architecture, forensics, COC, hash-chain, integrity]
parent: Architecture/INDEX
up: Architecture/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:9d9905d64ba57766dc82d7612e20ebef1314b92f7c9dc79b1a3d1ba533a3973f
hash_ts: 2026-04-25T01:10:48Z
hash_method: body-sha256-v1
---

> [↑ Architecture](INDEX.md) · [⌂ Home](../../HOME.md)

# Forensic Integrity

Chain of custody, hash chains, and the three-store architecture.

---

## Three-Store Architecture

```
Store 1: {repo}/forensics/    ← canonical COC (git-tracked, system of record)
Store 2: Vault (Obsidian)     ← styled derivative artifacts (not canonical)
Store 3: S3/B2 WORM           ← immutable backup of repo/forensics/
```

The git repo is the system of record. Vault docs are derivative — they reference
the canonical forensics/ entries but are not authoritative themselves.

---

## Hash Chain Structure

Every COC entry chains to the previous one:

```json
{
  "ts": "2026-04-24T15:30:00Z",
  "agent_type": "documentation-engineer",
  "agent_run_id": "ar-20260424-abc123",
  "manifest_path": "forensics/manifests/20260424T153000_documentation-engineer_...",
  "manifest_hash": "sha256:abc123...",
  "output_path": "forensics/docs/20260424T153000_...",
  "output_hash": "sha256:def456...",
  "prev_entry_hash": "sha256:xyz789...",
  "entry_hash": "sha256:000aaa..."
}
```

`entry_hash` = sha256 of this entry (excluding itself).
`prev_entry_hash` = `entry_hash` from the previous entry.

Altering any entry invalidates all subsequent entries. The chain is self-proving.

---

## Forensic Filename Convention

```
{TS}_{agent-type}_{task-id}_{agent-id}_{sid8}.{ext}
```

Example:
```
20260424T153000_documentation-engineer_task-042_ar8bc1d2e_35918dd1.json
```

- `{TS}` — ISO 8601 timestamp (date-first for filesystem sorting)
- `{agent-type}` — agent type slug
- `{task-id}` — task identifier (enables grep-discovery)
- `{agent-id}` — agent run ID (8 chars)
- `{sid8}` — first 8 chars of CLAUDE_SESSION_ID (cross-session isolation)

---

## Proof-in-Place Principle (mth00076)

The compliance proof must live on a stronger substrate than the system it proves.

| Artifact | Must live in | Why |
|----------|-------------|-----|
| WORM genesis proof | B2 bucket with compliance-mode lock | Admin cannot bypass bucket lock |
| Vault doc_hash | Git-tracked forensics/ | Force-push required to alter |
| Chain re-anchor | Cross-repo hash commit | Alters visible git history |

See: [[../Hive/proof-in-place]] for the full principle.

---

## Agent Write Rule

**Agents WRITE to forensics/. Agents do NOT READ from forensics/.**

Reading forensic artifacts during analysis would allow agents to reason backward
from prior conclusions. The forensic layer is write-only from the agent's perspective.

Hooks handle forensic reads (for chain verification). Agents never browse forensics/.

---

## Deletion Safety

Files in forensics/ are never deleted. Archive protocol:

```
1. Hash before removal
2. Move to forensics/deletions/{date}-{hash8}/
3. Append COC entry to forensics/coc.jsonl
```

`git rm` and `rm` on forensics/ paths require explicit human confirmation.

---

## COC File Locations

| File | Purpose |
|------|---------|
| `{repo}/forensics/coc.jsonl` | Primary chain of custody (append-only) |
| `{repo}/forensics/manifests/` | All agent manifests |
| `{repo}/forensics/droplets/` | Forensic droplet records |
| `~/.claude/memory/forensics/agent-runs.jsonl` | Global agent run log |

---

## Related

- [[../Hive/proof-in-place]] — the proof-in-place principle
- [[../Hive/the-five-principles]] — artifacts-in-forensics (principle 2)
- [[memory-topology]] — how forensics/ relates to other memory layers
- [[../Glossary/terms]] — COC, hash chain, WORM defined
