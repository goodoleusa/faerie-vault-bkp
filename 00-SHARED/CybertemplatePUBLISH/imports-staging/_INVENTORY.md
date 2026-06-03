---
date: 2026-05-22
author: openhands-agent
source: D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED
target: 00-SHARED/CybertemplatePUBLISH/imports-staging
status: roundup-pending-human-curation
size_total: 453M (the whole CyberOps-UNIFIED vault)
---

# CyberOps-UNIFIED → CybertemplatePUBLISH import roundup

Inventory of cybertemplate / critical-exposure material in the
companion vault at `D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED`
that's a candidate for the final publish push.

**453M total vault.** Most of that is binaries (sprites, datasets,
SpiderFoot runs). The PROSE candidates that should land here for
review are catalogued below by likely relevance.

## Tier A — HIGH PRIORITY (likely to publish or directly inform)

### Project-defining narrative
- `NARRATIVE-DESIGN.md` — narrative design doctrine (likely sister
  to swarmy's own narrative discipline; check for cybertemplate-
  specific framing)
- `ASYNC-COLLAB.md` — async collaboration patterns; may inform the
  Recursive Canvas dev↔prod bridge story
- `02-Narrative/` — narrative test cases (small, 4K)

### Long-form analysis (publication-worthy)
- `The State of Directed Energy Weapons and Neurotechnology — A Comprehensive Analysis.md` (+ v2)
  → if cybertemplate covers DEW/neurotech, this is publication-bound
- `Human Computer Interface and AI thought reading white paper 2026.md`
  → adjacent to DEW work; consider for site

### Investigation work product
- `10-Investigations/13-DESIGN-NARRATIVE-2026-03-30.md` — design
  narrative for an investigation; check date relevance
- `10-Investigations/Test-Case-Example.md` — pattern reference

### Protected zone (read carefully before importing)
- `01-PROTECTED/ON-RESISTANCE-2026-03-22.md` — protected; only import
  if site-bound content has been redacted
- `01-PROTECTED/HONEY-FULL-2026-03-22.md` — old HONEY snapshot; folds
  into the HONEY archeological dig already shipped at
  `00-SHARED/Daily/2026-05-22/03-honey-archeological-dig.md`
- `01-PROTECTED/CRYSTALLIZED-AMBER-2026-03-22.md` — crystallized
  memory snapshot

## Tier B — REFERENCE (likely stays in source vault but may inform writes)

### Vault structure / meta
- `VAULT-INDEX.md`, `VAULT-RULES.md`, `VAULT-SCHEMA.md` — meta-docs
  about the source vault's own organization
- `VAULT-PHASE-BC-COMPLETION-REPORT.md` — phase report; consider as
  inspiration for similar reports in faerie-vault
- `ONBOARDING-INDEX.md`, `ONBOARDING-ROUTING-AUTOMATION.md`,
  `ONBOARDING-SYSTEM-SUMMARY.md` — onboarding patterns
- `frontmatter-template.md` — likely candidate to inform faerie-vault
  templater

### Project-internal
- `HOW-TO-SAVE-MONEY.md` — operational notes
- `SYNCTHING-*.md` — sync setup notes; not publication-relevant

### Investigations / Networks / Evidence (data tiers)
- `10-Investigations/`, `25-Networks/`, `30-Evidence/`,
  `40-Intelligence/`, `50-Financial/`, `60-Chronology/`, `70-Sources/`
  — these are evidence/data tiers. **These should NOT come into the
  faerie-vault as prose** — they should go into the cybertemplate
  repo's `data/timelines/` tree where the curated investigation work
  already lives. Cross-check with cybertemplate's `forensics/promotion_log.json`.

## Tier C — SKIP (deprecated / sync metadata)

- `00-Inboxdeprecated/` — name says it
- `99-Archives/` — already archived
- `0a-SpiderFoot-Runs/` — raw tool output; data tier, not publication
- `Excalidraw/` — diagrams; if needed, import via the new
  `excalidraw_list/read` MCP tools (commit pending)
- `.copilot/`, `.makemd/`, `.space/`, `.stfolder/` — tool metadata
- `Untitled.md`, `Untitled 1.md` — empty/abandoned drafts
- `excalibrain.md` — plugin config

## Recommended import workflow

1. **Don't bulk copy.** That risks polluting faerie-vault with
   abandoned drafts. Curate one Tier-A item at a time.

2. **Per-item flow:**
   ```
   # 1. cp from source to imports-staging/
   cp "D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED\<file>" \
      /mnt/d/0local/faerie-vault/00-SHARED/CybertemplatePUBLISH/imports-staging/

   # 2. Read it cold. Decide:
   #    - publication-bound? → move to drafts/ + add frontmatter
   #    - reference material? → leave in imports-staging/ (keep but flag)
   #    - skip? → delete

   # 3. If publication-bound, add the canonical frontmatter:
   #    ---
   #    date: 2026-05-22
   #    author: goodoleusa
   #    related_mission: cybertemplate-publish
   #    status: draft
   #    imported_from: CyberOps-UNIFIED/<original-path>
   #    ---

   # 4. swarmy-status-set drafts/<file> reviewing  # when ready to read
   # 5. swarmy-status-set reviewing/<file> annotating  # mid-write
   # 6. swarmy-publish ready-to-publish/<file>  # final gate
   ```

3. **Big files (>50K) get a synthesis pass first.** Don't drop the
   1MB "Directed Energy Weapons" white paper into drafts/ as-is.
   First run a `summarize` agent over it, write a 1-2K synthesis
   into drafts/, link back to the original. The original stays
   in imports-staging/ as the source.

4. **Cross-check with cybertemplate's curated tier list.** If
   `cybertemplate/data/timelines/00-master/curated/` already has the
   evidence in its tiered structure, the vault narrative just needs
   to CITE that — don't re-import the evidence itself.

## What's NOT here yet but probably should be

- The user's earlier journal entries about the investigation
  experience (look for `Daily/` folder content in the source vault
  that wasn't catalogued)
- Conversations with collaborators (look for `03-Agents/`,
  `04-Agents/` AI session outputs)
- The "smoking gun" tier (Tier 1) evidence summaries — these are
  THE highest-leverage publication candidates

## Next moves

1. Goodoleusa picks 3-5 items from Tier A to import first (manual `cp`
   from Windows path → imports-staging/ via WSL).
2. Each gets the canonical frontmatter + a status of `draft`.
3. The Publishing Dashboard surfaces them in the workflow buckets.
4. The CybertemplatePUBLISH-specific dashboard (queued from
   `Daily/2026-05-22/05-dashboard-audit.md`) becomes worth building
   once there are 5-10 items in flight.

---

*Source vault is at `D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED`
(Windows path) = `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED`
(WSL path). 453MB total. The prose-bound items above are <5MB total;
the rest is data + plugin metadata.*
