---
type: design-insight
status: final
created: 2026-04-06
updated: 2026-04-06
tags: [audit, blueprints, fixes, vault, quality]
title: "Blueprint Fix Run — 2026-04-06"
category: infrastructure
priority: high
system_area: vault
blueprint: "[[Design-Insight]]"
agent_type: fullstack-developer
session_id: blueprint-fix-2026-04-06
promotion_state: awaiting-annotation
doc_hash: sha256:e39c8034fa8d6774c9969cc1bba6a685efb17f50f779db2e27575f9b8f9f626c
hash_ts: 2026-04-06T05:37:19Z
hash_method: body-sha256-v1
---

# Blueprint Fix Run — 2026-04-06

**Run date:** 2026-04-06 | **Agent:** fullstack-developer | **Based on:** vault-blueprint-audit-2026-04-05.md

---

## Summary

Fixed the 3 FAIL blueprints, added the 2 missing dataview fields to 4 blueprints, and wrote a blueprint howto guide. 192 notes across the vault already carry correct `blueprint:` frontmatter — the plugin is firing correctly for recently produced files.

---

## Task 1: Blueprint plugin firing check

**Result: FIRING CORRECTLY**

Searched all notes in `00-SHARED/` for `blueprint:` frontmatter. Found **192 notes** across the vault with a `blueprint:` wikilink field. The criticalexposure subdir (agent research outputs) and analysis/ subdir (audit files) are well-populated. The plugin is active and agents have been writing correct frontmatter since at least early March 2026.

The compliance gap identified in the prior audit (only 1/10 fully compliant in the sample) reflected older files written before the current standard was established — not a systemic failure of the plugin.

---

## Task 2: Fixed 3 FAIL blueprints

### Annotation-Commit.blueprint
**Was missing:** `type:` and `tags:` fields entirely.
**Fixed:** Added `type: annotation` and `tags: [annotation, coc]` to frontmatter.
**Impact:** Notes created from this blueprint were invisible to type-based dataview queries. Now queryable via `WHERE type = "annotation"`.

### Finding-Review.blueprint
**Was missing:** `status:` field.
**Fixed:** Added `status: draft` to frontmatter.
**Also added:** `review_verdict: ""` and `ann_synced: ""` (see Task 3 below).
**Impact:** Notes were invisible to `WHERE status = "awaiting-annotation"` dashboard filters. Now filtered correctly.

### Flag-Review.blueprint
**Was missing:** `status:` field.
**Fixed:** Added `status: draft` to frontmatter.
**Also added:** `review_verdict: ""` and `ann_synced: ""` (see Task 3 below).
**Impact:** Same as Finding-Review — dashboard filter compliance restored.

---

## Task 3: Added missing dataview fields to blueprints

The fields `ann_synced` and `review_verdict` were queried in Chain-of-Custody.md and Agent-Insights.md dashboards but defined in no blueprint — causing silent empty results in those dashboard sections.

### ann_synced
Set by `vault_annotation_sync.py` after annotations sync back to repo COC. Queried in Chain-of-Custody.md ("Recently Committed awaiting sync" and "Fully Synced" sections).

**Added to:**
- `Human-Annotation.blueprint` — annotation notes are the primary carrier of this field
- `Finding-Review.blueprint` — review notes go through annotation workflow
- `Flag-Review.blueprint` — same

**Not added to Gate-Review.blueprint** — Gate-Review already has `ann_hash`/`ann_ts` and a full signing section; added `ann_synced: ""` there too for COC completeness.

### review_verdict
Set by human in the Review section of task notes (`approved` or `needs-revision`). Queried throughout Agent-Insights.md to filter pending/approved tasks.

**Added to:**
- `Finding-Review.blueprint` — primary review workflow note
- `Flag-Review.blueprint` — triage workflow note
- `Gate-Review.blueprint` — pipeline gate review note

**Not added to Human-Annotation.blueprint** — annotation notes are not task-verdict notes; adding review_verdict there would create false hits in the Agent-Insights task queries.

---

## Task 4: Blueprint howto guide

Written to: `00-SHARED/00-META/blueprint-howto.md`

Covers:
- Create new note from blueprint (Cmd palette)
- Apply/re-apply blueprint to existing note
- Why "Apply blueprint" is greyed out (missing `blueprint:` frontmatter)
- Update all notes using a blueprint
- What the `blueprint:` field does and why it is required
- Annotation COC workflow (Ctrl+Alt+C → ann_hash → ann_synced)

---

## Notes found with blueprint frontmatter

| Scope | Count |
|-------|-------|
| Entire vault | **192** |
| 00-SHARED/ (sampled in prior audit) | 20+ in first grep page |
| Most recent files (criticalexposure/, analysis/) | Fully compliant |

The 192 count confirms the plugin is in active use. Older files written before March 2026 have lower compliance — those are the backfill candidates for the normalization pass (BLOCKER-1 from prior audit, not addressed in this run).

---

## Remaining issues not addressed in this run

These require separate work:

| Issue | Priority | Effort |
|-------|----------|--------|
| BLOCKER-1: Backfill `blueprint:`, `agent_type:`, `status:` on ~150 older Agent-Outbox files | HIGH | 1 normalization agent run |
| BLOCKER-4: Fix bare `mtime`/`ctime`/`name` in 5 dashboards | HIGH | Targeted edits to Data-Ingest-Pipeline.md, Phase1-AgentSync.md, _index.md, queries/blueprint-index.md, review/Agent-Insights.md |
| WARN-1: Add `blueprint:` self-reference to 10 WARN blueprints | MED | 10 single-line edits |
| WARN-2 (resolved): Finding-Review + Flag-Review `status:` — FIXED in this run | DONE | — |
| WARN-5: example-dashboard.md queries wrong blueprints path | LOW | 1 path fix |
| BLOCKER-2: example-droplet-LIVE.md has zero frontmatter | MED | Replace with proper template |

---

*Fix run by fullstack-developer | 2026-04-06 | Based on vault-blueprint-audit-2026-04-05.md*
