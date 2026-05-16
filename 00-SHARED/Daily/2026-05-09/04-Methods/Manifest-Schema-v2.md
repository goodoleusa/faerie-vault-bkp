---
type: methodology
status: active
created: 2026-04-20
tags: [methods, schema, manifest, stigmergy]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Collection-Procedure]]"]
child: []
doc_hash: sha256:9ea62523c45d007b86451eb46b2ac883411a9af47f179891c6f4f237a277c30c
hash_ts: 2026-04-20T21:59:42Z
hash_method: body-sha256-v1
---

> [↑ Methods Index](_INDEX.md) · [← Collection](Collection-Procedure.md) · [⌂ Home](../HOME.md)

# Manifest Schema v2

Two new required fields added to every agent manifest final status block. These fields enable CDr (Cascade Depth) and SDR (Stigmergic Discovery Rate) measurement.

**Patch reference:** `/mnt/d/0LOCAL/gitrepos/membench/PATCHES/spawn-boilerplate-v2.md`

---

## New Fields

### `triggered_by`

What caused this agent to run.

**Type:** string  
**Required:** Yes (schema v2)  
**Values:**
- `"{manifest_path}"` — absolute path to the manifest that triggered this run
- `"user"` — directly requested by the human
- `"faerie-turn-0"` — spawned at faerie session startup
- `"scheduled-task"` — queue-initiated, no upstream manifest

**Example:**
```json
"triggered_by": "/mnt/d/0LOCAL/.claude/hooks/state/wave1-triage-result.json"
```

**Used by:** CD collector — chain-walks `triggered_by` from root to leaf.

---

### `files_read`

All files the agent read during execution.

**Type:** array of strings (absolute paths)  
**Required:** Yes (schema v2)  
**Includes:** Every file opened via Read tool or Bash cat/read during the run.

**Example:**
```json
"files_read": [
  "/mnt/d/0LOCAL/.claude/hooks/state/wave1-triage-result.json",
  "/mnt/d/0LOCAL/gitrepos/cybertemplate/BENCHMARKS.md",
  "/mnt/d/0LOCAL/.claude/HONEY.md"
]
```

**Used by:** SDR collector — compares `files_read` against paths in spawn prompt to determine self-discovery rate.

---

## Full v2 Manifest Shape (final status)

```json
{
  "status": "final",
  "agent": "documentation-engineer",
  "ts": "2026-04-20T12:34:56Z",
  "dashboard_line": "membench vault: 19 metrics + 6 lit + 3 dashboards written",
  "files_written": [
    "/mnt/d/0LOCAL/gitrepos/membench/ObsidianVault/HOME.md"
  ],
  "files_read": [
    "/mnt/d/0LOCAL/gitrepos/membench/BENCHMARKS.md",
    "/mnt/d/0LOCAL/.claude/CLAUDE.md"
  ],
  "triggered_by": "user",
  "output_path": "/mnt/d/0LOCAL/gitrepos/membench/ObsidianVault/HOME.md",
  "next": "Run stamp_doc_hash.py on all vault files",
  "task_id": "membench-vault-2026-04-20",
  "droplets": [
    {"path": "/mnt/d/.../Droplets/documentation-engineer-a1b2c3d4.md", "count": 2}
  ]
}
```

---

## Backward Compatibility

Schema v1 manifests (without `files_read` or `triggered_by`) are not penalized. The SDR and CD collectors detect absence and skip those manifests with a `schema_v1_skipped` count in their output. Sessions before schema v2 adoption will report `SDR: null` and `CD: 0` (or null), not artificially low values.

---

## Adoption Path

1. Apply patch from `PATCHES/spawn-boilerplate-v2.md` to cybertemplate's SPAWN-BOILERPLATE.md
2. All agents spawned after the patch include `files_read` and `triggered_by` in their final manifests
3. SDR and CD metrics become measurable from the first post-patch session
4. Pre-patch sessions remain in baselines as `schema_v1` labeled entries
