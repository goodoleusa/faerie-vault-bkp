# Vault Roundup Inventory — 2026-05-19

Generated: 2026-05-19T15:11:23.301466+00:00

**Read-only inventory.** Do not move anything yet. After review, the user runs:
`scripts/dev/vault/07-roundup-execute.sh --apply` (or `--only faerie` / `--only cyberops`).

**Classification rules:**
- `cyberops` — name hints match (cyberops, huntin, investigation, evidence, case, rap, crims)
- `faerie` — name hints match (faerie, membench, fae-po, flowsearch, data-analysis, eval)
- `unknown` — generic 'vault' / 'ObsidianVault' folder name; needs human triage
- `skip` — under canonical vault, OR contains backup/garbage/.broken/-bkp/-Copy hint

## Summary

- Total vault-shape roots found: **80**
- `cyberops`: **6**
- `faerie`: **8**
- `unknown` (NEEDS TRIAGE): **5**
- `skip` (backups/canonical/dupes): **61**

## target=cyberops  (6 entries)

| path | size | mtime | mds | obsidian | top5 | reason |
|---|---|---|---|---|---|---|
| `/mnt/d/0LOCAL/gitrepos/CyberOpsNew` | 29.7MB | 2026-05-09 | 6 | y | README.md, CyberOps-QuickAdd.quickadd.json, HOW-TO-SAVE-MONEY.md, HOME.md, skills-lock.json | name hint: cyberops |
| `/mnt/d/0LOCAL/gitrepos/CyberOps` | 29.7MB | 2026-05-09 | 6 | y | README.md, CyberOps-QuickAdd.quickadd.json, HOW-TO-SAVE-MONEY.md, HOME.md, skills-lock.json | name hint: cyberops |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/Huntin` | 4.3MB | 2026-03-29 | 0 | y | .makemd, .obsidian | name hint: huntin |
| `/mnt/d/0LOCAL/gitrepos/Huntin/10-Investigations` | 39.7KB | 2026-03-16 | 14 | n | Untitled.md, Packetware7 - Overview.md, Pack8 - Overview.md, Investigation - Blahhh.md, Investigation - Anew Sitey.md | name hint: huntin |
| `/mnt/d/0LOCAL/gitrepos/Huntin` | - | 2026-05-09 | 17 | y | Multi‑Agency Cyber Breach Jan-Mar 2025 Threat Intelligence Report.md, excalibrain.dark.png, functional.md, Lumo AI articles and readme edit blog posts.md, Untitled.md | name hint: huntin |
| `/mnt/d/0LOCAL/gitrepos/Huntin/.claude` | - | 2026-03-29 | 3 | y | history.jsonl, bundle_handoff.py, CLAUDE.md, AGENTS.md, usage_report.py | name hint: huntin |

## target=faerie  (8 entries)

| path | size | mtime | mds | obsidian | top5 | reason |
|---|---|---|---|---|---|---|
| `/mnt/d/0LOCAL/gitrepos/faerie/ObsidianVault` | 21.2MB | 2026-03-19 | 6 | y | README.md, CyberOps-QuickAdd.quickadd.json, HOW-TO-SAVE-MONEY.md, HOME.md, .gitignore | name hint: faerie |
| `/mnt/d/0LOCAL/faerie-vault` | 600.1KB | 2026-05-10 | 0 | y | .git, .obsidian, 00-SHARED, 2026-04-28, 2026-05-10 | name hint: faerie |
| `/mnt/d/0LOCAL/gitrepos/00-claude-faerie-cli-git/ObsidianVault` | 582.6KB | 2026-03-25 | 8 | y | README.md, CyberOps-QuickAdd.quickadd.json, HOW-TO-SAVE-MONEY.md, HOME.md, START-COLLAB.md | name hint: faerie |
| `/mnt/d/0LOCAL/gitrepos/data-analysis-engine` | - | 2026-05-09 | 13 | n | admin.html, note_sign.py, bibliography.html, admin-deprecation-review.html, witness.html | name hint: data-analysis |
| `/mnt/d/0LOCAL/gitrepos/data-analysis-engine/ObsidianVault` | - | 2026-03-25 | 9 | y | README.md, CyberOps-QuickAdd.quickadd.json, HOW-TO-SAVE-MONEY.md, HOW-ANNOTATION-COC-WORKS.md, HOME.md | name hint: data-analysis |
| `/mnt/d/0LOCAL/gitrepos/fae-po/vault` | - | 2026-04-26 | 1 | y | HOME.md, .makemd, .obsidian, .space, 00-SHARED | name hint: fae-po |
| `/mnt/d/0LOCAL/gitrepos/flowsearch-dataanalyze-staging` | - | 2026-05-09 | 3 | y | history.jsonl, bundle_handoff.py, usage_report.py, handoff_logger.py, settings.json | name hint: flowsearch |
| `/mnt/d/0LOCAL/gitrepos/flowsearch/ObsidianVault` | - | 2026-03-20 | 8 | y | README.md, CyberOps-QuickAdd.quickadd.json, HOW-TO-SAVE-MONEY.md, HOME.md, START-COLLAB.md | name hint: flowsearch |

## target=unknown  (5 entries)

| path | size | mtime | mds | obsidian | top5 | reason |
|---|---|---|---|---|---|---|
| `/mnt/d/0LOCAL` | - | 2026-05-19 | 5 | n | ZimaBoard-CasaOS-20230202-32.iso, AnythingLLMDesktop.exe, hunchlyinstaller.msi, SyncTrayzorPortable-x64.zip, TriliumNotes-v0.101.3-windows-x64.exe | no hint matched |
| `/mnt/d/0LOCAL/ObsidianVault` | - | 2026-04-07 | 6 | y | README.md, HOW-TO-SAVE-MONEY.md, VAULT-INDEX.md, VAULT-RULES.md, HOME.md | generic vault folder; needs human triage |
| `/mnt/d/0LOCAL/ObsidianVault/00-SHARED` | - | 2026-04-26 | 13 | n | DAE-Evolution-Narrative.md, QUICKSTART.md, VAULT-SCHEMA.md, HOW-SYNC-WORKS.md, HOW-ANNOTATION-COC-WORKS.md | generic vault folder; needs human triage |
| `/mnt/d/0LOCAL/gitrepos` | - | 2026-05-16 | 7 | n | faerie-vault.zip, openapi-2025-11-08.yaml, claudetoclinecontext.md, MERGE_SCRATCHPAD.md, AUDIT_REPORT.md | no hint matched |
| `/mnt/d/0LOCAL/gitrepos/cybertemplate` | - | 2026-05-19 | 46 | n | evidence_manifest.json, FIREPACKETWARE_INVESTIGATION_REPORT.md.pdf, slightlydifferentPACKETWARE_INVESTIGATION_MASTER_BRIEF.md.pdf, PACKETWARE_INVESTIGATION_REPORT.md.pdf, viz-timeline-doge-access.html | no hint matched |

## target=skip  (61 entries)

| path | size | mtime | mds | obsidian | top5 | reason |
|---|---|---|---|---|---|---|
| `/mnt/d/0LOCAL/.claude-backup` | - | 2026-05-19 | 41 | y | history.jsonl, NECTAR.md, HONEY.md, HONEY-VARIANT-KS-reference.md, HONEY-VARIANT-DA-reference.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/.claude-backup-april2026/.claude` | - | 2026-04-04 | 5 | y | history.jsonl, bundle_handoff.py, dashboard.py, AGENTS.md.bak-20260328, settings.json | backup/dep hint: backup |
| `/mnt/d/0LOCAL/.claude-backup/garbage/vault-cleanup-2026-04-16/CyberOps-UNIFIED - Copy` | - | 2026-04-16 | 6 | n | README.md, HOW-TO-SAVE-MONEY.md, VAULT-INDEX.md, VAULT-RULES.md, ASYNC-COLLAB.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/.claude-backup/garbage/vault-cleanup-2026-04-16/CyberOps-UNIFIED - Copy/00-SHARED` | - | 2026-04-06 | 13 | n | DAE-Evolution-Narrative.md, QUICKSTART.md, VAULT-SCHEMA.md, HOW-SYNC-WORKS.md, HOW-ANNOTATION-COC-WORKS.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/.claude-backup/garbage/vault-cleanup-2026-04-16/CyberOps-Unified-Backup/CyberOps-UNIFIED` | - | 2026-04-15 | 10 | y | README.md, HOW-TO-SAVE-MONEY.md, VAULT-INDEX.md, VAULT-RULES.md, HOME.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/.claude-backup/garbage/vault-cleanup-2026-04-16/CyberOps-Unified-Backup2` | - | 2026-04-12 | 6 | n | README.md, HOW-TO-SAVE-MONEY.md, VAULT-INDEX.md, VAULT-RULES.md, ASYNC-COLLAB.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/.claude-backup/garbage/vault-cleanup-2026-04-16/CyberOps-Unified-Backup2/00-SHARED` | - | 2026-03-31 | 11 | n | DAE-Evolution-Narrative.md, VAULT-SCHEMA.md, HOW-SYNC-WORKS.md, HOW-ANNOTATION-COC-WORKS.md, PIPELINE-DESIGN.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/.claude-backup/garbage/vault-cleanup-2026-04-16/CyberOps-Unified-Backup2/CyberOps-UNIFIED` | - | 2026-04-16 | 11 | n | README.md, HOW-TO-SAVE-MONEY.md, NARRATIVE-DESIGN.md, SYNCTHING-READINESS.md, VAULT-INDEX.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/.claude-backup/garbage/vault-cleanup-2026-04-16/CyberOps1` | - | 2026-03-11 | 7 | y | ARCHITECTURE.md, VAULT-ARCHITECTURE.md, QUICKADD-BLUEPRINT-SETUP.md, HOME.md, QUICKADD-AND-BLUEPRINTS.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/.claude-backup/garbage/vault-cleanup-2026-04-16/CyberOps2` | - | 2026-03-16 | 7 | n | README.md, ASYNC-COLLAB.md, HOME.md, VAULT-ARCHITECTURE.md, ARCHITECTURE.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/.claude-backup/garbage/vault-cleanup-2026-04-16/CyberOps3` | - | 2026-03-15 | 5 | y | README.md, CyberOps-QuickAdd.quickadd.json, HOW-TO-SAVE-MONEY.md, HOME.md, VAULT-ARCHITECTURE.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED` | - | 2026-05-06 | 24 | y | The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis v2.md, The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis.md, Untitled 1.md, Untitled.md, Human Computer Interface and AI thought reading white paper 2026.md | canonical or under canonical |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED.broken-2026-04-16` | - | 2026-04-16 | 11 | n | README.md, HOW-TO-SAVE-MONEY.md, NARRATIVE-DESIGN.md, SYNCTHING-READINESS.md, VAULT-INDEX.md | backup/dep hint: .broken |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED` | - | 2026-05-06 | 22 | n | 0-TRIAGE.zip, DAE-Evolution-Narrative.md, EVAL-REPORT-2026-04-25.md, WRITE-ROUTING.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md | canonical or under canonical |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/2026-05-09` | - | 2026-04-20 | 2 | y | HOME.md, INDEX.md, .obsidian, 00-Metrics, 01-Literature | canonical or under canonical |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/Dashboards` | - | 2026-05-19 | 6 | n | 2026-04-25-eval-composite-post-mc-fixes.md, 00-Investigation-Home.md, 04-Chain-of-Custody.md, 02-Entities.md, 01-Evidence-Recent.md | canonical or under canonical |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/Huntin-bkp` | - | 2026-03-29 | 28 | y | Multi‑Agency Cyber Breach Jan-Mar 2025 Threat Intelligence Report.md, excalibrain.dark.png, functional.md, Lumo AI articles and readme edit blog posts.md, Untitled.md | backup/dep hint: -bkp |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/Huntin-bkp/10-Investigations` | - | 2026-03-10 | 14 | n | Untitled.md, Packetware7 - Overview.md, Pack8 - Overview.md, Investigation - Blahhh.md, Investigation - Anew Sitey.md | backup/dep hint: -bkp |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/Huntin-dep` | - | 2026-03-29 | 29 | y | Multi‑Agency Cyber Breach Jan-Mar 2025 Threat Intelligence Report.md, excalibrain.dark.png, functional.md, Lumo AI articles and readme edit blog posts.md, Untitled.md | backup/dep hint: -dep |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/Huntin-dep-backup/Huntinmovin` | - | 2026-03-29 | 0 | y | .obsidian, 0-to-integrate, 00-Inbox, 00-TEMPLATES, 000-META | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/Huntin-dep/10-Investigations` | - | 2026-03-12 | 14 | n | Untitled.md, Packetware7 - Overview.md, Pack8 - Overview.md, Investigation - Blahhh.md, Investigation - Anew Sitey.md | backup/dep hint: -dep |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/Huntin-optimized-attempt1` | - | 2026-03-15 | 23 | y | Multi‑Agency Cyber Breach Jan-Mar 2025 Threat Intelligence Report.md, excalibrain.dark.png, FUNCTIONAL-DASHBOARD.html, INVESTIGATION-DASHBOARD.md, excalibrain.dark.svg | backup/dep hint: -attempt |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/Huntin-optimized-attempt1/10-Investigations` | - | 2026-03-03 | 16 | n | Untitled.md, Packetware7 - Overview.md, Pack8 - Overview.md, Investigation - Blahhh.md, Investigation - Anew Sitey.md | backup/dep hint: -attempt |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/HuntinMobileImport` | - | 2026-03-29 | 15 | y | Multi‑Agency Cyber Breach Jan-Mar 2025 Threat Intelligence Report.md, excalibrain.dark.png, functional.md, Lumo AI articles and readme edit blog posts.md, excalibrain.dark.svg | backup/dep hint: mobileimport |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/HuntinMobileImport/10-Investigations` | - | 2026-03-29 | 14 | n | Untitled.md, Packetware7 - Overview.md, Pack8 - Overview.md, Investigation - Blahhh.md, Investigation - Anew Sitey.md | backup/dep hint: mobileimport |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260412-0000` | - | 2026-04-12 | 11 | y | README.md, HOW-TO-SAVE-MONEY.md, NARRATIVE-DESIGN.md, SYNCTHING-READINESS.md, VAULT-INDEX.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260412-0000/00-SHARED` | - | 2026-04-09 | 14 | n | DAE-Evolution-Narrative.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md, HOW-SYNC-WORKS.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260412-1200` | - | 2026-04-12 | 11 | y | README.md, HOW-TO-SAVE-MONEY.md, NARRATIVE-DESIGN.md, SYNCTHING-READINESS.md, VAULT-INDEX.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260412-1200/00-SHARED` | - | 2026-04-09 | 14 | n | DAE-Evolution-Narrative.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md, HOW-SYNC-WORKS.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260415-0000` | - | 2026-04-15 | 11 | n | README.md, HOW-TO-SAVE-MONEY.md, NARRATIVE-DESIGN.md, SYNCTHING-READINESS.md, VAULT-INDEX.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260415-1200` | - | 2026-04-15 | 11 | n | README.md, HOW-TO-SAVE-MONEY.md, NARRATIVE-DESIGN.md, SYNCTHING-READINESS.md, VAULT-INDEX.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260416-0000` | - | 2026-04-16 | 11 | n | README.md, HOW-TO-SAVE-MONEY.md, NARRATIVE-DESIGN.md, SYNCTHING-READINESS.md, VAULT-INDEX.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260416-1200` | - | 2026-04-16 | 11 | y | README.md, HOW-TO-SAVE-MONEY.md, NARRATIVE-DESIGN.md, SYNCTHING-READINESS.md, VAULT-INDEX.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260416-1200/00-SHARED` | - | 2026-04-16 | 18 | n | DAE-Evolution-Narrative.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md, HOW-SYNC-WORKS.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260417-0000` | - | 2026-04-17 | 16 | y | The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis.md, Untitled 1.md, Untitled.md, Human Computer Interface and AI thought reading white paper 2026.md, README.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260417-0000/00-SHARED` | - | 2026-04-16 | 18 | n | DAE-Evolution-Narrative.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md, HOW-SYNC-WORKS.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260417-1200` | - | 2026-04-17 | 16 | y | The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis.md, Untitled 1.md, Untitled.md, Human Computer Interface and AI thought reading white paper 2026.md, README.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260417-1200/00-SHARED` | - | 2026-04-16 | 18 | n | DAE-Evolution-Narrative.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md, HOW-SYNC-WORKS.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260418-0000` | - | 2026-04-18 | 18 | y | The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis v2.md, The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis.md, Untitled 1.md, Untitled.md, Human Computer Interface and AI thought reading white paper 2026.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260418-0000/00-SHARED` | - | 2026-04-17 | 19 | n | DAE-Evolution-Narrative.md, WRITE-ROUTING.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260418-1200` | - | 2026-04-18 | 18 | y | The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis v2.md, The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis.md, Untitled 1.md, Untitled.md, Human Computer Interface and AI thought reading white paper 2026.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260418-1200/00-SHARED` | - | 2026-04-17 | 19 | n | DAE-Evolution-Narrative.md, WRITE-ROUTING.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260419-0000` | - | 2026-04-19 | 18 | y | The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis v2.md, The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis.md, Untitled 1.md, Untitled.md, Human Computer Interface and AI thought reading white paper 2026.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260419-0000/00-SHARED` | - | 2026-04-18 | 20 | n | DAE-Evolution-Narrative.md, WRITE-ROUTING.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260419-1200` | - | 2026-04-19 | 18 | y | The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis v2.md, The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis.md, Untitled 1.md, Untitled.md, Human Computer Interface and AI thought reading white paper 2026.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260419-1200/00-SHARED` | - | 2026-04-18 | 20 | n | DAE-Evolution-Narrative.md, WRITE-ROUTING.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260420-0000` | - | 2026-04-20 | 18 | y | The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis v2.md, The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis.md, Untitled 1.md, Untitled.md, Human Computer Interface and AI thought reading white paper 2026.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260420-0000/00-SHARED` | - | 2026-04-18 | 20 | n | DAE-Evolution-Narrative.md, WRITE-ROUTING.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260420-1200` | - | 2026-04-20 | 18 | y | The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis v2.md, The State of Directed Energy Weapons and Neurotechnology A Comprehensive Analysis.md, Untitled 1.md, Untitled.md, Human Computer Interface and AI thought reading white paper 2026.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/0-ObsidianTransferring/backups/vault-20260420-1200/00-SHARED` | - | 2026-04-18 | 20 | n | DAE-Evolution-Narrative.md, WRITE-ROUTING.md, 20260408-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md, QUICKSTART.md, VAULT-SCHEMA.md | backup/dep hint: backup |
| `/mnt/d/0LOCAL/gitrepos/faerie-vault` | - | 2026-05-18 | 13 | y | implementation_spec.py, README.md, START-HERE.md, Learn Nuclear Rocket Physics.md, TERMINOLOGY.md | canonical or under canonical |
| `/mnt/d/0LOCAL/gitrepos/faerie-vault/00-Inbox` | - | 2026-05-18 | 4 | n | AGENT-REVIEW-INBOX.md, 55-EMERGENCE-AND-MUTATION-GLOSSARY.md, 88-DASHBOARD-ICON-GLOSSARY.md, Untitled.md, CT_VAULT | canonical or under canonical |
| `/mnt/d/0LOCAL/gitrepos/faerie-vault/00-Inbox/faerie-vault` | - | 2026-05-17 | 0 | y | .git, .obsidian, 00-SHARED, 2026-04-28, 2026-05-10 | canonical or under canonical |
| `/mnt/d/0LOCAL/gitrepos/faerie-vault/00-SHARED` | - | 2026-05-18 | 15 | n | DAE-Evolution-Narrative.md, QUICKSTART.md, VAULT-SCHEMA.md, HOW-SYNC-WORKS.md, HOW-ANNOTATION-COC-WORKS.md | canonical or under canonical |
| `/mnt/d/0LOCAL/gitrepos/faerie-vault/00-SHARED/00-Inbox/vault` | - | 2026-05-09 | 1 | y | HOME.md, .makemd, .obsidian, .space, 00-SHARED | canonical or under canonical |
| `/mnt/d/0LOCAL/gitrepos/faerie-vault/00-SHARED/00-SHARED/faerie-vault` | - | 2026-05-09 | 0 | y | .git, .obsidian, 00-SHARED, 2026-04-28, mission-graph | canonical or under canonical |
| `/mnt/d/0LOCAL/gitrepos/faerie-vault/00-SHARED/Daily/2026-05-09` | - | 2026-04-20 | 2 | y | HOME.md, INDEX.md, .obsidian, 00-Metrics, 01-Literature | canonical or under canonical |
| `/mnt/d/0LOCAL/gitrepos/faerie-vault/00-SHARED/Dashboards` | - | 2026-05-19 | 19 | n | 2026-05-03-archetype-measurement-framework.md, VAULT-MAP.excalidraw.md, 2026-05-01-accountability-build.md, HOME.md, VAULT-STRUCTURE.md | canonical or under canonical |
| `/mnt/d/0LOCAL/gitrepos/membench/ObsidianVault-scavengethendeprecate` | - | 2026-04-20 | 2 | y | HOME.md, INDEX.md, .obsidian, 00-Metrics, 01-Literature | backup/dep hint: scavenge |
| `/mnt/d/0LOCAL/gitrepos/membench/ObsidianVault-scavengethendeprecate/_meta` | - | 2026-04-20 | 0 | y | .obsidian | backup/dep hint: scavenge |
| `/mnt/d/0LOCAL/gitrepos/syncthingzima/CyberOps-UNIFIED` | - | 2026-04-12 | 8 | y | README.md, HOW-TO-SAVE-MONEY.md, NARRATIVE-DESIGN.md, VAULT-INDEX.md, VAULT-RULES.md | backup/dep hint: syncthing |


## Move plan (machine-readable for 07-roundup-execute.sh)

The `07-roundup-execute.sh` script greps for lines matching `| \`PATH\` | ... | (cyberops|faerie) |`
in the tables above and copies each into `{VAULT_ROOT}/00-Inbox/_roundup-YYYY-MM-DD/{basename}/`.
`unknown` and `skip` rows are NEVER moved by the script.

