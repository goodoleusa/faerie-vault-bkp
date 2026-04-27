---
type: design-insight
status: final
created: 2026-04-05
updated: 2026-04-05
tags: [audit, blueprints, vault, quality, stigmergy]
title: "Vault Blueprint System Audit — Share-Ready Assessment"
category: infrastructure
priority: high
system_area: vault
blueprint: "[[Design-Insight]]"
agent_type: code-reviewer
session_id: vault-audit
doc_hash: sha256:20394e554b23ceba33de5a29b86234930c43415882deae7a98c8631af438cb3b
promotion_state: awaiting-annotation
hash_ts: 2026-04-06T01:57:04Z
hash_method: body-sha256-v1
---

# Vault Blueprint System Audit — Share-Ready Assessment

**Audited:** 2026-04-05 | **Agent:** code-reviewer | **Scope:** Blueprints/, Agent-Outbox/, stigmergy paths, dataview queries

## Executive Summary

The vault has 48 blueprints with strong structural coverage (45/48 pass 4 core checks). Stigmergy paths all exist; 14/18 have _index.md files. The critical gap is Agent-Outbox frontmatter compliance: of 10 sampled files, only 1 is fully compliant. Most files are missing `blueprint:`, `agent_type:`, and `status:` fields. Dataview dashboards also reference 2 fields (`ann_synced`, `review_verdict`) that are not defined in any blueprint, causing silent dashboard failures. The vault is functional for current use but needs frontmatter hardening before a new collaborator agent can use it reliably without manual correction.

---

## 1. Blueprint Compliance Matrix

48 blueprints audited. Checks: fm=valid frontmatter, type=has type: field, tags=has tags: field, status=has status: field, bp=has blueprint: self-reference, ph=has {{ }} placeholders, sec=has {% section %} markers.

| Blueprint | fm | type | tags | status | blueprint: | placeholders | sections | RESULT |
|---|---|---|---|---|---|---|---|---|
| Agent-Skill | Y | Y | Y | Y | NO | Y | Y | WARN |
| Agent-Training-Event | Y | Y | Y | Y | Y | Y | Y | PASS |
| Annotation-Commit | Y | NO | NO | Y | NO | N | Y | FAIL |
| Brief-Assembly | Y | Y | Y | Y | Y | Y | Y | PASS |
| Chronology-Entry | Y | Y | Y | Y | Y | Y | Y | PASS |
| Collab-Export | Y | Y | Y | Y | Y | Y | Y | PASS |
| Context-Bundle | Y | Y | Y | Y | NO | Y | Y | WARN |
| Crystallization-Candidate | Y | Y | Y | Y | Y | Y | Y | PASS |
| Daily-Research | Y | Y | Y | Y | NO | Y | Y | WARN |
| Dead-Drop | Y | Y | Y | Y | Y | Y | Y | PASS |
| Design-Insight | Y | Y | Y | Y | Y | Y | Y | PASS |
| Domain | Y | Y | Y | Y | Y | Y | Y | PASS |
| Entity-Stub | Y | Y | Y | Y | NO | Y | Y | WARN |
| Evidence-Item | Y | Y | Y | Y | Y | Y | Y | PASS |
| Faerie-Brief | Y | Y | Y | Y | Y | Y | Y | PASS |
| Feature-Eval | Y | Y | Y | Y | Y | Y | Y | PASS |
| Feature-Proposal | Y | Y | Y | Y | Y | Y | Y | PASS |
| Financial-Trail | Y | Y | Y | Y | Y | Y | Y | PASS |
| Finding-Review | Y | Y | Y | NO | Y | Y | Y | FAIL |
| Flag-Review | Y | Y | Y | NO | Y | Y | Y | FAIL |
| Gate-Review | Y | Y | Y | Y | Y | Y | Y | PASS |
| High-Control-Group | Y | Y | Y | Y | Y | Y | Y | PASS |
| Human-Annotation | Y | Y | Y | Y | Y | Y | Y | PASS |
| IP-Address | Y | Y | Y | Y | Y | Y | Y | PASS |
| Intelligence-Report | Y | Y | Y | Y | NO | Y | Y | WARN |
| Investigation-Case | Y | Y | Y | Y | NO | Y | Y | WARN |
| Memory-Entry | Y | Y | Y | Y | NO | Y | Y | WARN |
| NECTAR-Entry | Y | Y | Y | Y | Y | Y | Y | PASS |
| Network-Map | Y | Y | Y | Y | Y | Y | Y | PASS |
| Normalize-Frontmatter | Y | Y | Y | Y | NO | Y | Y | WARN |
| Observer-Drop | Y | Y | Y | Y | Y | Y | Y | PASS |
| Organization-Master | Y | Y | Y | Y | Y | Y | Y | PASS |
| Organization | Y | Y | Y | Y | Y | Y | Y | PASS |
| Person | Y | Y | Y | Y | Y | Y | Y | PASS |
| Phase-Narrative | Y | Y | Y | Y | Y | Y | Y | PASS |
| Problem-Log | Y | Y | Y | Y | Y | Y | Y | PASS |
| Research-Brief | Y | Y | Y | Y | Y | Y | Y | PASS |
| Session-Handoff | Y | Y | Y | Y | NO | Y | Y | WARN |
| Session-Manifest | Y | Y | Y | Y | Y | Y | Y | PASS |
| Session-Review | Y | Y | Y | Y | Y | Y | Y | PASS |
| Shadow-Operation | Y | Y | Y | Y | Y | Y | Y | PASS |
| Source-Assessment | Y | Y | Y | Y | Y | Y | Y | PASS |
| System-Design | Y | Y | Y | Y | Y | Y | Y | PASS |
| Task-Claim | Y | Y | Y | Y | NO | Y | Y | WARN |
| Task-Inbox | Y | Y | Y | Y | Y | Y | Y | PASS |
| TechDoc | Y | Y | Y | Y | Y | Y | Y | PASS |
| Thread | Y | Y | Y | Y | NO | Y | Y | WARN |
| Threat-Actor | Y | Y | Y | Y | NO | Y | Y | WARN |

**Summary:** 35 PASS | 10 WARN (missing blueprint: self-reference only) | 3 FAIL

**FAIL details:**
- `Annotation-Commit` — missing type: and tags: fields entirely; appears to be a partial/patch blueprint not a standalone template
- `Finding-Review` — missing status: field
- `Flag-Review` — missing status: field

**WARN details (all missing `blueprint:` self-reference field):**
Agent-Skill, Context-Bundle, Daily-Research, Entity-Stub, Intelligence-Report, Investigation-Case, Memory-Entry, Normalize-Frontmatter, Session-Handoff, Task-Claim, Thread, Threat-Actor

The `blueprint:` self-reference is needed for `vault_hash_sync.py` to link annotation hashes. Without it, agent outputs using these blueprints will have broken provenance chains.

---

## 2. Agent-Outbox Frontmatter Quality

10 files sampled from different subdirectories. Checks: fm=valid YAML frontmatter, type=has type:, tags=has tags:, status=has status:, bp=has blueprint: wikilink, dh=has doc_hash:, at=has agent_type:.

| File | Subdir | fm | type | tags | status | blueprint: | doc_hash | agent_type | Score |
|---|---|---|---|---|---|---|---|---|---|
| _index.md | analysis | Y | Y | Y | N | N | Y | N | 4/7 |
| 2026-03-24-findings.md | criticalexposure | Y | Y | Y | N | N | Y | N | 4/7 |
| vault-org-report-2026-03-28.md | reports | Y | Y | Y | N | N | Y | N | 4/7 |
| GAPS-AND-INVESTIGATIVE-PRIORITIES.md | evidence | Y | Y | Y | Y | N | N | N | 4/7 |
| _index.md | extractions | Y | Y | Y | N | N | Y | N | 4/7 |
| example-dashboard.md | dashboards | Y | Y | Y | Y | Y | Y | Y | 7/7 |
| example-droplet-LIVE.md | droplets | N | N | N | N | N | N | N | 0/7 |
| 2026-03-29-HONEY-export.md | Agent-Outbox | Y | Y | N | Y | N | N | N | 3/7 |
| blueprint-compliance-report.md | Agent-Outbox | Y | Y | N | N | Y | N | Y | 4/7 |
| blueprint-audit-2026-03-29.md | Agent-Outbox | Y | Y | N | Y | N | Y | Y | 5/7 |

**Average compliance: 3.9/7 (56%)**

**Patterns observed:**
- `status:` field most commonly missing from older/index files — these predate the current standard
- `blueprint:` wikilink absent in 8/10 files — this is the field dataviewjs uses to find typed outputs
- `agent_type:` absent in 7/10 — annotation trail broken for most files
- `example-droplet-LIVE.md` has zero frontmatter — the droplet convention (inline metadata in body) conflicts with dataview query requirements
- `example-dashboard.md` is the only fully compliant file and was clearly written as a reference implementation — it works as a gold standard

**Dataview findability:** A query `WHERE type = "analysis"` would find only 3/10 sampled files (those with both `type:` set AND a known value). The majority would be invisible to typed dataview queries.

---

## 3. Stigmergy Path Status

All 18 paths checked for existence and _index.md presence. New agent guidance assessment: "clear" = would a fresh agent know what to write here without reading additional documentation?

| Path | Exists | _index.md | Files | Agent Guidance |
|---|---|---|---|---|
| Agent-Outbox/ | YES | YES | 21 files, 14 subdirs | Clear — _index.md explains purpose |
| Agent-Outbox/criticalexposure | YES | YES | 81 files | Clear |
| Agent-Outbox/analysis | YES | YES | 7 files | Clear |
| Agent-Outbox/reports | YES | YES | 2 files | Clear |
| Agent-Outbox/briefs | YES | NO | 0 files | UNCLEAR — empty, no index |
| Agent-Outbox/evidence | YES | YES | 11 files | Clear |
| Agent-Outbox/extractions | YES | YES | 1 file | Clear |
| Agent-Outbox/dashboards | YES | NO | 1 file | UNCLEAR — no index |
| Agent-Outbox/droplets | YES | NO | 1 file | UNCLEAR — no index |
| Human-Inbox/ | YES | YES | 38 files | Clear |
| Human-Inbox/flags | YES | YES | 51 files | Clear |
| Human-Inbox/findings | YES | YES | 31 files | Clear |
| Droplets/ | YES | YES | 1 file | Clear |
| Dashboards/ | YES | YES | 8 files, 11 subdirs | Clear |
| Queue/ | YES | YES | 3 files | Clear |
| Hive/ | YES | YES | 63 files | Clear |
| Agent-Context/ | YES | NO | 10 files | UNCLEAR — has README.md not _index.md |
| Session-Briefs/ | YES | NO | 0 files, 1 subdir | UNCLEAR — empty, no index |

**4 paths missing _index.md:** briefs/, dashboards/, droplets/ (under Agent-Outbox/), Agent-Context/, Session-Briefs/

The 3 subdirs under Agent-Outbox without indexes are particularly problematic for new agents: they will see the folder exists but have no guidance on the file naming convention or frontmatter expectations for content placed there.

---

## 4. Dataview Compatibility

**Queries audited:** 14 active dashboard files (excludes `.claude-garbage-*` files)

| Check | Result | Detail |
|---|---|---|
| Blueprints define fields used in WHERE clauses | PARTIAL | 13 of 15 custom fields found in blueprints |
| `ann_synced` field defined in blueprints | FAIL | Used in Chain-of-Custody.md, not in any blueprint |
| `review_verdict` field defined in blueprints | FAIL | Used in Agent-Insights.md, not in any blueprint |
| `file.mtime` vs bare `mtime` usage | FAIL | 5 dashboards use bare `mtime` without `file.` prefix — Obsidian dataview requires `file.mtime` |
| `file.ctime` vs bare `ctime` | FAIL | 2 dashboards use bare `ctime` |
| `file.name`/`file.folder` vs bare | FAIL | 2 dashboards use bare `name`, `folder` |
| Blueprint query points to correct path | WARN | example-dashboard.md queries `"00-SHARED/Hive/blueprints"` — blueprints live in `Blueprints/` at vault root |
| Agent evolution queries | PASS | Queries for `agent-evolution` type with correct fields |
| Evidence/tier queries | PASS | Fields `tier`, `confidence_level`, `hypothesis_support` all defined |
| COC annotation queries | PARTIAL | `ann_hash`, `ann_ts` defined; `ann_synced` missing |

**Field-level mismatches (high impact):**
- `ann_synced` — queried in Chain-of-Custody.md dashboard but undefined in blueprints. The COC dashboard will silently return empty results for the annotation sync status column.
- `review_verdict` — queried in Agent-Insights.md but undefined. Agent review verdicts won't surface in the dashboard.
- Bare `mtime`/`ctime`/`name` — these return `null` in Obsidian dataview (must be `file.mtime` etc). Affects 5 dashboards with sort/filter on these fields.

---

## 5. BLOCKERS for Sharing

These issues will cause a new collaborator agent to fail or produce incorrect outputs without manual intervention.

**BLOCKER-1: Frontmatter compliance too low for reliable dataview discovery**
Only 1/10 sampled Agent-Outbox files is fully compliant. A new agent writing to the vault following existing patterns will produce files invisible to dataview queries. The `blueprint:` wikilink field is missing in 80% of sampled files — this is the key field the coverage dashboard uses.
*Fix:* Run a normalization pass on existing Agent-Outbox files using the Normalize-Frontmatter blueprint to backfill missing fields. Then enforce via blueprint in spawn prompts.

**BLOCKER-2: `example-droplet-LIVE.md` has zero frontmatter**
The only droplet example file is entirely unstructured. A new agent writing droplets will follow this example and produce files invisible to any dataview query. The Droplets/ directory under Agent-Outbox/ also has no _index.md.
*Fix:* Replace example-droplet-LIVE.md with a properly frontmatted template, or add a README explaining that droplets are append-only within a single file with per-droplet inline metadata (and update the Droplets blueprint accordingly).

**BLOCKER-3: `Annotation-Commit` blueprint missing type: and tags:**
This blueprint is used to retrofit annotation structure onto existing notes. Without `type:` and `tags:`, it fails the 4 core checks. Any note created from this blueprint will be invisible to type-based queries.
*Fix:* Add `type: annotation` and `tags: [annotation, coc]` to the Annotation-Commit.blueprint frontmatter.

**BLOCKER-4: 5 dashboards use bare `mtime`/`ctime`/`name` instead of `file.mtime` etc**
These queries silently return empty result sets in current Obsidian dataview. A new collaborator checking "no recent activity" may conclude the vault is empty when it is not.
*Fix:* Replace bare field names with `file.mtime`, `file.ctime`, `file.name` in: Data-Ingest-Pipeline.md, Phase1-AgentSync.md, _index.md, queries/blueprint-index.md, review/Agent-Insights.md.

---

## 6. WARNINGS

These issues degrade quality but do not prevent basic function.

**WARN-1: 16 blueprints missing `blueprint:` self-reference field**
Affects: Agent-Skill, Annotation-Commit, Context-Bundle, Daily-Research, Entity-Stub, Intelligence-Report, Investigation-Case, Memory-Entry, Normalize-Frontmatter, Session-Handoff, Task-Claim, Thread, Threat-Actor (plus Finding-Review, Flag-Review which also FAIL).
Impact: vault_hash_sync.py cannot link annotation hashes to the originating blueprint. Provenance chain weakened.

**WARN-2: `Finding-Review` and `Flag-Review` blueprints missing `status:` field**
These are critical workflow blueprints (human review flow). Without `status:`, the Annotation-Dash dataview queries that filter `WHERE status = "awaiting-annotation"` will miss files created from these blueprints.

**WARN-3: `ann_synced` and `review_verdict` used in dashboards but undefined in any blueprint**
Chain-of-Custody.md and Agent-Insights.md reference these fields. Files will never populate these dashboard columns. Either add fields to relevant blueprints or remove the queries.

**WARN-4: 4 stigmergy paths missing _index.md**
Agent-Outbox/briefs/, Agent-Outbox/dashboards/, Agent-Outbox/droplets/, Agent-Context/, Session-Briefs/ have no index file. New agents have no written guidance on what to write there. Risk: agents write to the wrong subdir or use wrong naming conventions.

**WARN-5: example-dashboard.md queries `"00-SHARED/Hive/blueprints"` (non-existent path)**
Blueprints live at vault root `/Blueprints/`. The example dashboard blueprint query will always return empty. The path should be `"Blueprints"`.

**WARN-6: Human-Inbox contains many unstructured files (38 root-level files)**
Files like `Untitled.md`, `yeahh.md`, `yeah.md` suggest accumulation of unreviewed organic notes alongside agent-written structured findings. A new collaborator agent reading the inbox will have difficulty distinguishing structured agent findings from unstructured human notes.

**WARN-7: `review_status` field defined in blueprints but not in Normalize-Frontmatter or Evidence-Item**
Dashboard queries in HOME.md and Phase1-AgentSync.md filter on `review_status`. Evidence-Item blueprint (the most commonly used for findings) does not define this field, so evidence files are invisible to review-status-based queries.

---

## 7. VERDICT: Share-Ready?

**NO — with conditions**

The vault architecture is sound. Blueprints are comprehensive (48 types, strong section structure, good placeholder coverage). The stigmergy path structure exists and most paths are documented. The dashboards are well-designed and the HOME.md command-center pattern is excellent.

However, three issues must be fixed before handing to a new collaborator agent:

1. **Fix BLOCKER-1** (frontmatter normalization pass on Agent-Outbox) — otherwise the new agent's first dataview query returns near-empty results and they will conclude the vault is empty or misconfigured.
2. **Fix BLOCKER-2** (droplet example file) — the only example a new agent will follow for droplets is structurally wrong.
3. **Fix BLOCKER-4** (bare field names in dataview) — 5 dashboards are silently broken; a new agent debugging them will waste significant time.

After those 3 blockers: the vault is share-ready for a new collaborator agent with the understanding that WARN-1 through WARN-7 represent technical debt that degrades dashboard fidelity over time.

**Estimated fix effort:** 2-3 hours (1 normalization agent run for Agent-Outbox backfill + targeted edits to 5 dashboards + example-droplet-LIVE.md replacement + 3 blueprint field additions).

---

*Audit produced by code-reviewer agent | session: vault-audit | 2026-04-05*
*Blueprint-MAP.md reference: `/mnt/c/Users/amand/.claude/agents/BLUEPRINT-MAP.md`*
