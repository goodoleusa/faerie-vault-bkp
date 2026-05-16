---
type: audit-spec
status: active
created: 2026-04-23
tags: [audit, repo-organization, deprecation, feature-archaeology]
parent: "[[ARCHITECTURE]]"
up: "[[ARCHITECTURE]]"
sibling: []
cites:
  - "HONEY mth00076 (proof-in-place — preserve evidence, don't delete)"
  - "HONEY mth00077 (bundle + delta discipline)"
  - "forensics/audits/*agent-perms* (pattern: dead hooks encode valuable capabilities)"
  - "forensics/audits/*settings-audit* (pattern: 19 unique capabilities lost in orphan file)"
---

> [↑ Architecture](./ARCHITECTURE.md) · [⌂ Docs](./README.md)

# Repo Archaeology Audit — Organize + Recover Lost Features

**User directive 2026-04-23:** "the repo folder itself needs to be audited, organized, deprecated what has been abandoned and use what got deprecated/abandoned for hints on old features."

**Key principle:** deprecations are feature memory. Don't delete — catalog, then decide. What was abandoned may encode a capability we want back.

## Scope

Target: `/mnt/d/0local/gitrepos/faerie2/` (the faerie2 repo root). All of it. Read-only.

## Audit Method (in order)

### 1. Caller-graph per script

For every file in `scripts/`, `hooks/`, `config/`, `schemas/`, `templates/`:
- Count references across the repo: `grep -r "{filename}" --include="*.py" --include="*.md" --include="*.json" --include="*.yaml"`
- Classify:
  - **ACTIVE**: 3+ references outside own directory
  - **SEMI-ACTIVE**: 1-2 external references
  - **ISOLATED**: Only self-references (likely abandoned)
  - **ZOMBIE**: No references anywhere; exists but nothing points at it

### 2. Doc reachability

For every `*.md` in `docs/`, vault pointers, `.claude/`:
- Does any other doc link to it? Does any script cite it?
- Orphaned docs = feature memory to recover

### 3. Test-to-script correspondence

For every `tests/test_*.py`:
- Does the tested script still exist + still have the tested entry points?
- Dead tests pointing at renamed-or-deleted scripts = capability hint

### 4. Audit results history

Scan `scripts/audit_results/*` and `forensics/audits/*`:
- Sort by date
- For each, extract "what was audited" and "what was the finding"
- Produce timeline: when did each capability become live / deprecate / audit-find-drift?

### 5. Deprecated / archive folders

Known locations:
- `docs/DEPRECATED-CONFIGS/` (per git status)
- `forensics/deletions/` (archived deletions)
- Prior `.claude/` subfolders that may have orphan content

For each archived item: extract the capability it encoded. Is it still needed? If yes, the current system has a gap.

### 6. Recently renamed/moved (hint at mental-model drift)

Use `git log --name-status --diff-filter=R` to find renames in last 30 days.
- A rename often signals: feature was reorganized but some callers missed the update
- Find dangling references to old names

## Deliverable Format

Single audit report at `forensics/audits/{ts}_audit_task-61-repo-archaeology_{agent}_{sid8}.md` with:

1. **Active inventory** — top 20 most-referenced scripts + their role
2. **Isolated / zombie list** — ranked by severity (what are they? why abandoned? is the capability still needed?)
3. **Orphaned docs** — what feature did they describe? current status of that feature?
4. **Dead tests** — what scripts/features they targeted
5. **Capability timeline** — chronological view of features entering/exiting the system
6. **Recovery recommendations** — capabilities worth reactivating (like the 19 orphan hooks pattern)
7. **Reorganization proposal** — suggested folder structure if drift is significant
8. **Deprecation candidates** — ranked, with archive-not-delete protocol pointers (never rm; always archive to `forensics/deletions/`)

## Output Requirements

- **Do not modify any file.** Read-only audit.
- **Report via 4x_coc_writer.py COC entry** (task_id=task-61-repo-archaeology)
- **Manifest** at `/mnt/d/0LOCAL/.claude/hooks/state/task-61-repo-archaeology-manifest.json` with dashboard_line (≤80 chars), active_count, zombie_count, recovery_candidates_count, deprecation_candidates_count, report_path
- **Do not return the full report inline** — write to forensics path, inline only the dashboard summary + top-5 findings

## Explicit Non-Goals

- Not renaming/moving files (proposal only)
- Not deleting anything (only recommending archival candidates)
- Not fixing capabilities found (that's follow-up tasks)
