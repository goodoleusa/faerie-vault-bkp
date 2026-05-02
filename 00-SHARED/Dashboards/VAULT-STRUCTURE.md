---
type: governance
created: 2026-04-30T00:00:00Z
tags: [vault-structure, governance, faerie, vault-braiding-org]
parent: Dashboards.md
mission_field: vault-braiding-org
compass_edge: null
hash: pending
---

> [↑ Dashboards](Dashboards.md)

# Vault Structure — Faerie↔Obsidian Sync Governance

**Mission:** vault-braiding-org  
**Applies to:** faerie-vault + CyberOps-UNIFIED vaults  
**Last updated:** 2026-04-30

---

## Directory Structure

```
{vault}/00-SHARED/Dashboards/
├── Dashboards.md           ← master index (TOC + recent entries)
├── VAULT-STRUCTURE.md      ← this file (governance)
├── YYYY-MM-DD/             ← day-folders (one per active day)
│   ├── INDEX.md            ← daily index (required in every day-folder)
│   ├── eval-report.md      ← system eval (if generated that day)
│   ├── system-health.md    ← piston + context metrics
│   ├── accountability-build.md
│   └── {type}-{slug}.md   ← any additional artifacts
├── Droplets/               ← live session droplets (separate cadence)
├── investigate/            ← investigation workspaces
├── review/                 ← annotation + review artifacts
└── queries/                ← blueprint/query indexes
```

**Naming rules:**
- Day-folders: `YYYY-MM-DD/` (ISO 8601 date, no time)
- Artifact files: `{NN}-{type}-{slug}.md` (NN = 2-digit sort prefix, optional)
- Root-level loose files: `YYYY-MM-DD-{type}-{slug}.md` (pre-day-folder pattern, tolerated but deprecated)

---

## Frontmatter Schema (All Daily Artifacts)

Every file written by faerie scripts or agents MUST include this YAML frontmatter:

```yaml
---
type: <see type registry below>
created: <ISO 8601 datetime, e.g. 2026-04-30T14:22:00Z>
tags: [<mission-id>, faerie, <type>, <additional>]
parent: ../Dashboards.md          # navigation breadcrumb (relative path)
mission_field: <investigation_label>   # from mission_dispatch.py
compass_edge: <N|S|E|W|null>          # bearing if discovered work exists
hash: <sha256-of-body | pending>       # body hash for integrity
---
```

### Required Fields

| Field | Required | Values | Notes |
|-------|----------|--------|-------|
| `type` | YES | see registry | Enables Dataview queries |
| `created` | YES | ISO 8601 | Script-generated, not hand-edited |
| `tags` | YES | array | First tag = mission_field |
| `parent` | YES | relative path | Always `../Dashboards.md` from day-folder |
| `mission_field` | YES | investigation_label | Matches forensics/ manifest field |
| `compass_edge` | YES | N/S/E/W/null | null if no discovered work |
| `hash` | YES | sha256 or "pending" | Set to "pending" until body finalized |

### Optional Fields

| Field | Notes |
|-------|-------|
| `status` | active / archived / superseded |
| `updated` | ISO 8601, if file is mutated after creation |
| `source_artifact` | relative path to forensics/ source |
| `session_id` | 8-char session ID prefix |
| `doc_hash` | alias for hash (legacy, tolerated) |

---

## Type Registry

| type | Description | Typical producer |
|------|-------------|-----------------|
| `eval-report` | System eval scores, composite metrics | eval scripts |
| `system-health` | Piston state, context fill, FFMx | presend hooks |
| `accountability-build` | Spawn cost infrastructure updates | agent manifests |
| `mission-dispatch` | Wave launch records, agent rosters | spawn.py |
| `design-narrative` | Analytical write-ups, evidence synthesis | agents |
| `daily-dashboard` | Day-of overview (00-DASHBOARD.md) | dashboard scripts |
| `governance` | Structure/rule documents (like this file) | hand-authored |
| `forensic-governance` | COC, immutability rules | agent manifests |
| `investigation-index` | INDEX.md per day-folder | auto-generated |

---

## Schema Violation Audit (2026-04-30 baseline)

### Faerie Vault (`faerie-vault/00-SHARED/Dashboards/`)

| File | Violations |
|------|-----------|
| `2026-05-01-accountability-build.md` | Missing frontmatter entirely (no `---` block) |
| `Agent-Findings.md` | Has frontmatter; missing `mission_field`, `compass_edge`, `hash` |
| `piston-status.md` | Has frontmatter; fields unknown — needs audit |
| `HOME.md` | Has frontmatter; navigation file, governance schema optional |
| `Dashboards.md` | Has `---` block but body is near-empty (only sticker field) |
| `_index.md` | Has frontmatter; likely missing mission fields |
| Day-folder pattern | MISSING — artifacts at root instead of `YYYY-MM-DD/` sub-folders |

### CT Vault (`CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/`)

| File | Violations |
|------|-----------|
| `2026-04-26/eval-report-faerie-T100.md` | Has `type`, `parent`; missing `mission_field`, `compass_edge`, `hash` |
| `2026-04-29/01-baseline-eval-narrative.md` | Has `type`, `tags`; missing `parent`, `mission_field`, `compass_edge`, `hash` |
| `2026-04-28/00-DASHBOARD.md` | Has MetaBind buttons as frontmatter — non-standard, no type/tags schema |
| `2026-05-01-spawn-cost-accountability.md` | Root-level loose file (deprecated pattern) — needs day-folder migration |
| `2026-04-27/INDEX.md` | Needs audit |

**Primary gaps across both vaults:**
1. `mission_field` absent in almost all files
2. `compass_edge` absent everywhere
3. `hash` absent or `pending` and never finalized
4. `parent` absent in newer CT vault files
5. Loose root-level files instead of day-folder pattern

---

## Navigation Breadcrumb Rules

Every artifact must render a human-readable nav header immediately after frontmatter:

```markdown
> [↑ Dashboards](../Dashboards.md) · [⌂ Home](../../HOME.md)
```

For root-level files (not in day-folder):
```markdown
> [↑ Dashboards](Dashboards.md) · [⌂ Home](../HOME.md)
```

---

## Hash Integrity Protocol

1. Write file body (leave `hash: pending`)
2. Compute SHA256 of file body (excluding frontmatter block)
3. Update `hash:` field
4. Log hash to `forensics/coc.jsonl` via vault-mutation-tracker.py

Scripts use `hash_tracker.py snapshot` for directory-level hashing in addition to per-file SHA256.

---

## Dataview Query Pattern

Day-folder artifacts are queryable via Obsidian Dataview:

```dataview
TABLE created, type, mission_field, compass_edge
FROM "00-SHARED/Dashboards"
WHERE type != null AND type != "governance"
SORT created DESC
LIMIT 20
```

Mission-filtered:
```dataview
TABLE created, type, file.link
FROM "00-SHARED/Dashboards"
WHERE mission_field = "vault-braiding-org"
SORT created DESC
```
