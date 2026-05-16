---
type: hub
status: active
tags: [install, validation, checklist, vault-infrastructure-overhaul]
created: 2026-05-06T00:00:00Z
updated: 2026-05-06T00:00:00Z
doc_hash: ""
---

# Installation Checklist — Pre-Release Validation

Validate every item before marking the vault-infrastructure-overhaul install as release-ready.
Check each item. Items marked REQUIRED must pass. Items marked OPTIONAL are enhancement targets.

---

## Phase 1: Environment Setup

- [ ] **REQUIRED** `git` available: `git --version` returns version string
- [ ] **REQUIRED** `python3` available: `python3 --version` returns 3.9+
- [ ] **REQUIRED** `one-click-install.sh` runs to completion without `[error]` lines
- [ ] **REQUIRED** Runtime is under 120 seconds on broadband connection
- [ ] **REQUIRED** `faerie-env.json` created in install dir with correct paths
- [ ] **REQUIRED** `faerie-env.sh` created and sourceable: `source faerie-env.sh && echo $FAERIE2_ROOT`
- [ ] **OPTIONAL** Obsidian detected automatically (Linux, macOS, WSL all tested)
- [ ] **OPTIONAL** Symlinks from ct_vault/CT_VAULT variants resolve to canonical ct-vault path

---

## Phase 2: Repository Clones

- [ ] **REQUIRED** `faerie2/` directory exists and contains `.git`
- [ ] **REQUIRED** `faerie-vault/` directory exists and contains `.git`
- [ ] **REQUIRED** `ct-vault/` directory exists and contains `.git` or is a placeholder dir
- [ ] **REQUIRED** Idempotency: re-running install on existing directories does `git pull` not error
- [ ] **OPTIONAL** `--depth=1` shallow clone completes (saves ~200MB vs full clone)

---

## Phase 3: Obsidian Plugin Configs

- [ ] **REQUIRED** `faerie-vault/.obsidian/app.json` present and valid JSON
- [ ] **REQUIRED** `faerie-vault/.obsidian/community-plugins.json` lists all 7 required plugins
- [ ] **REQUIRED** `faerie-vault/.obsidian/core-plugins.json` present
- [ ] **REQUIRED** `faerie-vault/.obsidian/plugins/dataview/data.json` present and valid
- [ ] **REQUIRED** `faerie-vault/.obsidian/plugins/breadcrumbs/data.json` present with compass hierarchy defined
- [ ] **REQUIRED** `faerie-vault/.obsidian/plugins/quickadd/data.json` present with daily+mission templates
- [ ] **REQUIRED** `faerie-vault/.obsidian/snippets/compass-graph-colors.css` present
- [ ] **REQUIRED** `faerie-vault/.obsidian/workspace.json` opens to `00-START-HERE.md` on first launch
- [ ] **OPTIONAL** ct-vault gets its own `.obsidian/` config (investigation data vault settings)

---

## Phase 4: Templates and Onboarding

- [ ] **REQUIRED** `faerie-vault/Templates/daily-note-template.md` present with `mission_choice` frontmatter
- [ ] **REQUIRED** `faerie-vault/Templates/mission-note-template.md` present with compass fields
- [ ] **REQUIRED** `faerie-vault/00-SHARED/ONBOARDING/00-START-HERE.md` present
- [ ] **REQUIRED** `install/ONBOARDING-NEW-USER.md` present (standalone reference)
- [ ] **REQUIRED** `install/PLUGIN-INSTALL-MATRIX.json` present and valid JSON

---

## Phase 5: Obsidian Runtime Validation

Run these checks after opening vault in Obsidian (requires Obsidian installed):

- [ ] **REQUIRED** Vault opens without "Vault not found" error
- [ ] **REQUIRED** Opening vault lands on `00-SHARED/ONBOARDING/00-START-HERE.md` (workspace.json)
- [ ] **REQUIRED** Settings → Community Plugins → plugins list shows all 7 plugins as available
- [ ] **REQUIRED** Enable all community plugins (disable safe mode first)
- [ ] **REQUIRED** Dataview: create a test note with `status: active` frontmatter, verify query `TABLE file.name FROM ""` returns it
- [ ] **REQUIRED** Breadcrumbs: add `north: [[some-file]]` to test note, verify breadcrumb trail renders in sidebar
- [ ] **REQUIRED** QuickAdd: `Cmd+P → QuickAdd: Daily Note` creates file with full frontmatter
- [ ] **REQUIRED** Search: `Cmd+Shift+F → mission_choice` returns notes containing that field
- [ ] **OPTIONAL** Excalidraw: create drawing, embed in note, verify renders in preview
- [ ] **OPTIONAL** Meta Bind: `INPUT[text:mission_choice]` widget renders and updates frontmatter

---

## Phase 6: Compass Navigation Validation

- [ ] **REQUIRED** Create two test notes (A and B) with:
  - A: `south: [[B]]`
  - B: `north: [[A]]`
- [ ] **REQUIRED** Breadcrumbs shows A → B trail when viewing A
- [ ] **REQUIRED** Prev/Next buttons navigate A ↔ B correctly
- [ ] **OPTIONAL** Graph view shows colored edges (N=blue, S=green) via CSS snippet
- [ ] **OPTIONAL** Excalibrain (if installed) renders mission-graph with compass colors

---

## Phase 7: Sync Connectivity

- [ ] **REQUIRED** `python3 scripts/0x_vault_sync_test.py --vault ../faerie-vault --faerie2 .` exits 0 (or exits non-zero with clear error, not crash)
- [ ] **REQUIRED** `FAERIE_VAULT` and `CT_VAULT` env vars resolve to valid directories after sourcing faerie-env.sh
- [ ] **REQUIRED** `forensics/` directory exists in faerie2 with correct subdirectory structure
- [ ] **OPTIONAL** PostToolUse hook fires: write a test manifest, verify it appears in vault within 10 seconds

---

## Phase 8: Frontmatter Validator

- [ ] **REQUIRED** `python3 .claude/scripts/8x_vault_frontmatter_validator.py install/ONBOARDING-NEW-USER.md` exits 0 (valid frontmatter)
- [ ] **REQUIRED** Validator correctly rejects a note missing `type` field (returns non-zero + error message)
- [ ] **OPTIONAL** PreToolUse hook wired: validator fires on vault Write/Edit (check settings.json PreToolUse hooks)

---

## Phase 9: Docker Option (Optional)

- [ ] **OPTIONAL** `Dockerfile.vault` builds without errors: `docker build -f Dockerfile.vault .`
- [ ] **OPTIONAL** Container mounts faerie-vault volume correctly
- [ ] **OPTIONAL** Vault files accessible at `/vault` inside container

---

## Phase 10: OS Coverage

- [ ] **REQUIRED** Tested on: Linux (Ubuntu 20.04+) or WSL2
- [ ] **OPTIONAL** Tested on: macOS 12+
- [ ] **OPTIONAL** Tested on: WSL2 on Windows 11 (primary target platform for this repo)
- [ ] **NOTE** Windows native (not WSL) not supported — Bash scripts require WSL

---

## Release Gates

All REQUIRED items must be checked before tagging a release.

| Gate | Criteria | Status |
|------|----------|--------|
| Install completes | All Phase 1-5 REQUIRED items pass | PENDING |
| Navigation works | All Phase 6 REQUIRED items pass | PENDING |
| Sync works | All Phase 7 REQUIRED items pass | PENDING |
| Validation works | All Phase 8 REQUIRED items pass | PENDING |
| Runtime | < 120 seconds on broadband | PENDING |

When all gates pass, update this table to PASS and file a manifest with `bearing: S` (ready for release).

---

## Known Issues (Pre-Release)

| ID | Issue | Severity | Workaround |
|----|-------|----------|-----------|
| KI-001 | `8x_vault_frontmatter_validator.py` not wired to PreToolUse hook | P1 | Manually run validator before committing vault notes |
| KI-002 | 6 competing ct-vault path variants may cause script confusion | P1 | Source `faerie-env.sh` to set canonical `CT_VAULT` env var |
| KI-003 | `4x_verify_vault_hash_chains.py` has hardcoded forensic log path | P2 | Set `FORENSIC_REPO_PATH` env var to faerie2 root before running |
| KI-004 | `body_hash` / `file_hash` / `doc_hash` field name inconsistency | P2 | Use `doc_hash` in all new notes; validator enforces this |
| KI-005 | QuickAdd macro JS is pseudocode (not wired) | P3 | Use template-only mode (macros optional) |

---

*Checklist version: 1.0.0 | Mission: vault-infrastructure-overhaul | Generated: 2026-05-06*
