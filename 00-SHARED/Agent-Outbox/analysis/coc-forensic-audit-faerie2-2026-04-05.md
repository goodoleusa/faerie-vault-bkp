---
type: design-insight
status: final
created: 2026-04-05
updated: 2026-04-05
tags: [audit, coc, forensic, faerie2, chain-of-custody, security]
title: "COC Forensic Audit — faerie2 Manifest/Stigmergy/Vault Pipeline"
category: security
priority: critical
system_area: forensic-integrity
blueprint: "[[Design-Insight]]"
agent_type: security-auditor
session_id: coc-audit-2026-04-05
doc_hash: sha256:ea5868e5665c73010512fcb5e7f9703cbb99bd6063bf18dd6f2d7d07c5f19ad7
promotion_state: awaiting-annotation
hash_ts: 2026-04-06T01:59:29Z
hash_method: body-sha256-v1
---

# COC Forensic Audit — faerie2 AI Orchestration Framework

**Audit Date:** 2026-04-05  
**Scope:** faerie2 (primary), cybertemplate (reference), data-analysis-engine (cross-ref)

## Executive Summary

faerie2 has a **well-architected COC foundation** at the session level (hash-chained JSONL, PostToolUse hook). Three critical gaps compromise the manifest-stigmergy-vault pipeline:

1. **doc_hash permanently `sha256:pending`** — the PostToolUse hook that was supposed to auto-fill it does not exist
2. **Wave manifests not hash-chained** — each manifest is forensically isolated
3. **Vault writes invisible to COC** — vault path missing from `DATA_PATH_HINTS`

## Critical Gaps

### C-1: Auto-stamp doc_hash on vault writes
`blueprint_inject.py` line 229 claims "the PostToolUse hook fills it automatically" — **this is FALSE**. The hook contains no such code. Every vault file since system deployment has `doc_hash: sha256:pending`. `stamp_doc_hash.py` exists but requires manual invocation.

**Fix:** Extend `forensic_coc.py` to detect vault writes + invoke stamp_doc_hash.py automatically.

### C-2: Add vault path to DATA_PATH_HINTS
All writes to Agent-Outbox/, Human-Inbox/, Droplets/ produce **zero forensic log entries**. Add vault shared path patterns to `DATA_PATH_HINTS` in forensic_coc.py.

### C-3: Port stamp_input()/stamp_output() from cybertemplate
cybertemplate's `coc.py` wraps every pipeline file operation with SHA-256 stamps. faerie2 has no equivalent. Port as shared module to `brain/coc.py`.

## Comparison Matrix

| Capability | cybertemplate | faerie2 | Gap |
|---|---|---|---|
| PostToolUse hook | Full, vault-aware | Present but vault-blind | HIGH |
| Session hash chain | Git-tracked forensic/ | Gitignored ~/.claude | HIGH |
| Master COC JSONL | Git-tracked, court-ready | Gitignored, local-only | HIGH |
| Vault mutation tracking | Auto .sha256 sidecar | Manual-only | CRITICAL |
| PGP agent signing | Pre-commit automated | Manual-only | HIGH |
| Court-ready export | Implemented | Stubbed ("not yet implemented") | HIGH |
| doc_hash auto-stamping | Auto via vault_sync.py | Broken — hook absent | CRITICAL |
| Pipeline stamp_input/output | Woven into every phase | Absent | CRITICAL |

## Files to Port from cybertemplate

| Source | Destination | Why |
|---|---|---|
| `scripts/coc.py` (stamp functions) | `brain/coc.py` | Pipeline-level hashing |
| `scripts/4a-forensic-sign.py` | `.git/hooks/pre-commit` | Automated PGP signing |
| `forensics/README.md` | `forensic/README.md` | Git-tracked COC folder |

## High Priority

- **H-1:** Move master COC from gitignored to git-tracked `forensic/` folder
- **H-2:** Implement court-ready export in forensic_coc_check.py
- **H-3:** Add inter-manifest hash chain to vault_manifest.py (line 113 comment)
- **H-4:** Run stamp_doc_hash on session stop (belt + suspenders)
- **H-5:** Add `agent_hash` field to all blueprint templates

## Key Insight

> The session-level COC is genuinely strong. The gap is specifically at the vault output layer: the path between "agent writes a finding file" and "that file has a verified hash in its frontmatter" is not automated. blueprint_inject.py's false claim actively misdirects agents into believing a safety net exists that does not.
