---
type: audit
task: dashboards-deprecated
date: 2026-05-19
note: "User reviews and decides whether to `git rm` or archive. DO NOT delete automatically."
---

# Dashboards — Deprecation Candidates (2026-05-19)

C/D-rated finds from the roundup. One-line reason each.

## Duplicates (safe to remove first)

- `faerie2/forensics/dashboards/2026-05-04_01-00-56_mission_intelligence.md` — byte-identical copy of 01-00-52
- `faerie2/forensics/dashboards/2026-05-04_01-01-09_mission_intelligence.md` — byte-identical copy of 01-00-52
- `faerie2/forensics/dashboards/2026-05-04_01-01-15_mission_intelligence.md` — byte-identical copy of 01-00-52
- `faerie2/forensics/dashboards/2026-05-04_01-05-56_mission_intelligence.md` — byte-identical copy of 01-00-52
- `faerie-vault/00-Inbox/CT_VAULT/2026-04-28/00-DASHBOARD.md` — legacy inbox copy of CyberOps daily
- `faerie-vault/00-Inbox/faerie-vault/2026-04-28/00-DASHBOARD.md` — deeper-inbox copy of same
- `faerie-vault/00-SHARED/00-SHARED/faerie-vault/2026-04-28/00-DASHBOARD.md` — double-shared duplicate (sync glitch)
- `CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/2026-04-28/2026-04-28/00-DASHBOARD.md` — nested-folder duplicate
- `CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/2026-04-29/2026-04-28/00-DASHBOARD.md` — misfiled duplicate

## Empty / stub

- `faerie-vault/Dashboards/Dashboards/Data-Ingest-Pipeline.md` — 0 bytes
- `CyberOps-UNIFIED/Dashboards/Dashboards/Data-Ingest-Pipeline.md` — 0 bytes
- `faerie-vault/00-SHARED/piston-status.md` — empty (canonical version lives in new 00-Home)
- `faerie-vault/00-SHARED/mission-control.md` — only ~50 bytes, no useful content (replaced by 00-Home)
- `faerie-vault/00-SHARED/Dashboards/Dashboards.md` — 3-line sticker-only stub
- `CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/Dashboards.md` — stub

## Replaced by canonical

- `CyberOps-UNIFIED/00-SHARED/Dashboards/.claude-garbage-Investigation-Overview.md` — cannibalized into new `Dashboards/00-Investigation-Home.md`
- `CyberOps-UNIFIED/00-SHARED/Dashboards/.claude-garbage-Mission-Control.md` — cannibalized into `Dashboards/00-Investigation-Home.md`
- `CyberOps-UNIFIED/00-SHARED/Dashboards/.claude-garbage-Agent-Findings.md` — patterns folded into `01-Evidence-Recent.md`
- `faerie-vault/00-SHARED/Dashboards/.claude-garbage-Investigation-Overview.md` — duplicate of CyberOps version
- `CyberOps-UNIFIED/00-SHARED/ONBOARDING/2026-04-21-eval-brief/02-DASHBOARD-roster-eval.md` — replaced by `04-Eval-Dimensions.md` (broken data source)

## Onboarding docs that are not dashboards (move out of dashboard search results)

- `CyberOps-UNIFIED/00-SHARED/ONBOARDING/2026-04-18-ship-dae-faerie2-cybertemplate/05-DASHBOARDS.md`
- `CyberOps-UNIFIED/00-SHARED/ONBOARDING/2026-04-20/F0-DASHBOARD-REALITY-CHECK.md`
- `CyberOps-UNIFIED/00-SHARED/Hive/05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK.md` — spec doc, not dashboard
- `faerie-vault/00-SHARED/Hive/05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK.md` — duplicate of CyberOps spec
- `CyberOps-UNIFIED/00-Inboxdeprecated/*` — entire folder marked deprecated by user already
