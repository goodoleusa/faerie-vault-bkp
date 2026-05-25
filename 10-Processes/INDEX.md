---
doc_hash: sha256:pending
created: 2026-04-25
type: playground-index
folder: 10-Processes
breadcrumb: "vault / 10-Processes / INDEX"
---

# 10-Processes — From Spawn Bundle to COC Entry

Every agent invocation in faerie2 follows a fixed pipeline. Nothing escapes it; the hook enforces compliance at the PreToolUse layer. This folder walks through each stage with real artifacts.

---

## The Spawn Pipeline

```
Task in sprint-queue.json
        │
        ▼
7x_spawn_template.py --bundle
  Renders mustache template
  Injects: task_id, session_id, manifest_path, wave, model
  Embeds: discovery.json inline (anti-gaming: agent never reads own card)
  Signs: TEMPLATE-SIGNED header (HMAC-SHA256)
        │
        ▼
8x_spawn_contract_enforcer.py  (PreToolUse hook)
  Checks: prompt carries TEMPLATE-SIGNED header
  Mode WARN: logs violation → forensics/spawn-contract-violations.jsonl
  Mode BLOCK: exits 2 → Claude Code rejects the Agent() call
        │
        ▼
Agent() invocation
  Subagent starts with clean, isolated context
  Reads bundle only — no HONEY.md, no NECTAR.md, no own agent card
  Budget: depends on wave (W1 hot, W2 standard, W3 deep synthesis)
        │
        ▼
Subagent execution
  Writes artifacts → forensics/{type}/{date}/
  Writes progress → manifest (in-progress → draft → final)
  Appends insights → $CT_VAULT/00-SHARED/Droplets/
  Signs output → Ed25519 key at ~/.claude/agents/*.key
        │
        ▼
4x_coc_writer.py  (PostToolUse hook)
  Appends COC entry to forensics/coc.jsonl
  Chain: prev_entry_hash → entry_hash (HMAC-SHA256)
  Forensic immutability: never overwrite, append only
        │
        ▼
Main reads manifest dashboard_line (≤80 chars)
  Cross-cut synthesis only — no reformulation of subagent output
  Routing decision → next wave dispatch
```

---

## A Real Bundle JSON (Annotated)

This is what `7x_spawn_template.py --bundle` produces. Main passes this as the Agent() prompt — main composes nothing.

```json
{
  "TEMPLATE-SIGNED": "hmac-sha256:a3f2...c9b1",
  "template_id": "w2-evidence-curation",
  "version": "1.0",
  "agent_type": "documentation-engineer",
  "wave": 2,
  "model": "haiku",
  "task_id": "task-20260425-152144-a4e5",
  "session_id": "1c0c5ef4",
  "manifest_path": "forensics/manifests/20260425_manifest_task-20260425-152144-a4e5_documentation-engineer_1c0c5ef4.json",
  "timeout_seconds": 900,
  "run_in_background": false,
  "discovery": {
    "predecessor_manifests": ["forensics/manifests/20260424_manifest_task-..._a7f2c9b1.json"],
    "grep_pattern": "_task-20260425-152144-a4e5_"
  },
  "prompt": "You are a documentation-engineer subagent...\n\nTask: [rendered from template]\n\nStigmergy: write all artifacts to forensics/. Write manifest progressively..."
}
```

Key points:
- `TEMPLATE-SIGNED` header is what the hook checks. Without it, the call is blocked/warned.
- `discovery` is inlined by the parent — agent greps `forensics/` for predecessors without reading its own card.
- `model: haiku` — `HAIKU_DEFAULT_ENFORCE=true` routes all non-synthesis-heavy tasks to Haiku (2.5x cost savings).

---

## Model Routing Rules

| Tag | Model | Rationale |
|-----|-------|-----------|
| (default) | haiku | Extraction, classification, bulk evidence curation |
| `synthesis-heavy` | sonnet | Multi-file refactors, 5+ manifest synthesis, adversarial design |
| explicit `opus` | opus | Architecture decisions only — very rare |

The tag lives in the task's `tags` array in sprint-queue.json. The template renderer picks model automatically; main does not choose.

---

## The Forensic Artifact Pattern

Every artifact follows: `{ts}_{type}_{task_id}_{agent}_{session_id8}.{ext}`

```
forensics/manifests/20260425_manifest_task-20260425-152144-a4e5_documentation-engineer_1c0c5ef4.json
forensics/bundles/20260425_bundle_task-20260425-152144-a4e5_documentation-engineer_1c0c5ef4.json
```

A new agent finding related work does:
```bash
grep -r "_task-20260425-152144-a4e5_" forensics/
```
Zero context cost. No vector DB. No retrieval. Pure filesystem.

---

## Manifest Schema

Every agent writes a manifest at the path given in its bundle. The manifest evolves:

```json
{
  "status": "in_progress",          // → "draft" → "final"
  "task_id": "task-20260425-152144-a4e5",
  "agent_run_id": "ARN-20260425-1c0c5ef4",
  "dashboard_line": "vault_consolidated=y, folders_authored=5, deprecated_archived=y",
  "next_task_queued": null,
  "artifacts": ["forensics/..."],
  "session_id": "1c0c5ef4"
}
```

`dashboard_line` is the ONLY thing main reads per subagent return. Everything else is weight.

---

## COC Chain Integrity

`forensics/coc.jsonl` is an HMAC-SHA256 hash chain. Each entry includes:

```json
{
  "ts": "2026-04-25T15:21:44Z",
  "agent": "documentation-engineer",
  "session_id": "1c0c5ef4",
  "operation": "artifact_written",
  "artifact": "forensics/manifests/...",
  "prev_entry_hash": "a3f2...",
  "entry_hash": "c9b1..."
}
```

Tamper any past entry → hash chain breaks → forensic integrity compromised. This is your audit trail. It is append-only, git-tracked, never deleted.

---

[[00-Welcome/INDEX]] | [[20-Queue-Mission/INDEX]] | [[30-Dashboards/INDEX]] | [[40-Roster-Routing/INDEX]] | [[50-Honesty-System/INDEX]]

*sha256:pending*
