---
type: audit
task: dashboards-roundup
date: 2026-05-19
scope: ["CyberOps-UNIFIED", "faerie-vault", ".claude", "faerie2/forensics/dashboards"]
---

# Dashboards Roundup — 2026-05-19

Cross-vault inventory of every dashboard-like artifact across CyberOps-UNIFIED, faerie-vault,
~/.claude, and faerie2/forensics/dashboards. Rating scale:
- **A** canonical-worthy (working bones + reusable structure)
- **B** good idea, needs rework (broken queries / bad paths / stale)
- **C** skeleton only (frontmatter + headers, no content)
- **D** dead (empty, stub, or only-noise)

Total finds: **38** dashboard-ish files / dirs. **A: 6 · B: 9 · C: 8 · D: 15.**

## A — Canonical-worthy

| Path | Rating | What it does | Bones to cannibalize |
|------|--------|--------------|----------------------|
| CyberOps-UNIFIED/00-SHARED/Dashboards/01-SYSTEM-OVERVIEW.md | A | f(0) health, wave status, agent roster | FFFF section structure; context-pressure ASCII gauge |
| CyberOps-UNIFIED/00-SHARED/00-META/DASHBOARD-INDEX.md | A | Index of all dashboards by mtime | Clean Dataview `TABLE ... WHERE type=dashboard` |
| CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/2026-04-28/00-DASHBOARD.md | A | Daily system health snapshot | Health-table layout, mission/compass_edge frontmatter, wave gauge |
| CyberOps-UNIFIED/00-SHARED/Dashboards/system/metrics-dashboard-20260425.md | A | Dimension scores (Composite, Throughput, Memory, Resilience, Quality, Piston, Routing) | Dimension table + deep-dive sections |
| CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/2026-05-09/02-Dashboards/Metric-Trends.md | A | Last-10 trend tables per metric (SBI/SI/MBI/IRR/SDR/OMR) | Per-metric Dataview snippets — clean and copy-paste-ready |
| faerie-vault/00-SHARED/templates/FFFF-dashboard-template.md | A | Findings/Flags/Friction/Flow template | Whole template adopted as canonical scaffold |

## B — Good idea, needs rework

| Path | Rating | Issue | Salvage |
|------|--------|-------|---------|
| CyberOps-UNIFIED/00-SHARED/Dashboards/.claude-garbage-Investigation-Overview.md | B | "garbage" prefix; references 20-Entities which lives elsewhere | Dataview blocks for active investigations, evidence pipeline, tasks |
| CyberOps-UNIFIED/00-SHARED/Dashboards/.claude-garbage-Mission-Control.md | B | Same "garbage" branding | Mission-control concept; reuse layout |
| CyberOps-UNIFIED/00-SHARED/Dashboards/.claude-garbage-Agent-Findings.md | B | Same | Findings query pattern |
| CyberOps-UNIFIED/00-SHARED/ONBOARDING/CyberTemplate-Investigation/FFFF-Dashboard.md | B | Investigation-specific hardcoded H1-H5 | dataviewjs dynamic-TOC mermaid renderer is gold |
| CyberOps-UNIFIED/00-SHARED/Hive/blueprints-justmd/blueprint_dashboard.md | B | Blueprint spec, not a live dashboard | Frontmatter schema and required sections |
| CyberOps-UNIFIED/00-SHARED/Agent-Outbox/dashboards/example-dashboard.md | B | Example with stale links | Coverage-gaps dataviewjs pattern |
| CyberOps-UNIFIED/00-SHARED/ONBOARDING/2026-04-21-eval-brief/02-DASHBOARD-roster-eval.md | B | All zeros (data source path broken) | Roster/training-events idea |
| CyberOps-UNIFIED/00-SHARED/Hive/05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK.md | B | Long prose spec, not a dashboard | Agent-insights design pattern (24h feed over agent.md) |
| faerie-vault/00-SHARED/mission-control.md | B | Empty content, only stub | Filename worth reviving |

## C — Skeleton only

- faerie-vault/00-SHARED/Dashboards/Dashboards.md (3 lines, sticker frontmatter)
- faerie-vault/00-SHARED/Dashboards/.claude-garbage-Investigation-Overview.md (copy of CyberOps)
- faerie-vault/Dashboards/Dashboards/Data-Ingest-Pipeline.md (0 bytes)
- CyberOps-UNIFIED/Dashboards/Dashboards/Data-Ingest-Pipeline.md (0 bytes)
- CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/Dashboards.md (stub)
- faerie-vault/00-SHARED/00-META/DASHBOARD-INDEX.md (mirrors CyberOps index, sparser)
- faerie-vault/00-SHARED/Hive/00-OVERVIEW.md (overview, not dashboard)
- faerie-vault/00-SHARED/Hive/05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK.md (duplicate)

## D — Dead

- faerie-vault/00-SHARED/piston-status.md (empty)
- faerie-vault/00-Inbox/CT_VAULT/2026-04-28/00-DASHBOARD.md (legacy copy of daily)
- faerie-vault/00-Inbox/faerie-vault/2026-04-28/00-DASHBOARD.md (same, deeper inbox)
- faerie-vault/00-SHARED/00-SHARED/faerie-vault/2026-04-28/00-DASHBOARD.md (double-shared duplicate)
- CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/2026-04-28/2026-04-28/00-DASHBOARD.md (nested duplicate)
- CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/2026-04-29/2026-04-28/00-DASHBOARD.md (wrong-folder duplicate)
- faerie2/forensics/dashboards/2026-05-04_01-00-52_mission_intelligence.md (5x 735KB identical dumps; pick one)
- faerie2/forensics/dashboards/2026-05-04_01-00-56_mission_intelligence.md (duplicate)
- faerie2/forensics/dashboards/2026-05-04_01-01-09_mission_intelligence.md (duplicate)
- faerie2/forensics/dashboards/2026-05-04_01-01-15_mission_intelligence.md (duplicate)
- faerie2/forensics/dashboards/2026-05-04_01-05-56_mission_intelligence.md (duplicate)
- CyberOps-UNIFIED/Dashboards/Dashboards/Data-Ingest-Pipeline.md (0 bytes — already in C, listed for cleanup)
- CyberOps-UNIFIED/00-SHARED/ONBOARDING/2026-04-20/F0-DASHBOARD-REALITY-CHECK.md (postmortem text, not a dashboard)
- CyberOps-UNIFIED/00-SHARED/ONBOARDING/2026-04-18-ship-dae-faerie2-cybertemplate/05-DASHBOARDS.md (onboarding doc)
- CyberOps-UNIFIED/00-Inboxdeprecated (legacy folder, ignore)

## Notable HTML / Canvas / Excalidraw

- faerie2/forensics/dashboards/dashboard/membench-eval-dashboard.html (65KB) — **A-** standalone HTML dashboard; works in browser; visualizes memory benchmark eval. Keep as-is, reference from canonical Eval-Dimensions.
- CyberOps-UNIFIED/00-SHARED/VAULT-MAP.excalidraw.md (14KB) — vault topology drawing; not strictly a dashboard but related.
- CyberOps-UNIFIED/.obsidian/snippets/dashboard-home.css — CSS for the `dashboard-home` cssclass referenced by blueprint.

## Patterns observed

1. **Three "Dashboard of Dashboards" attempts** (00-META/DASHBOARD-INDEX, Daily-Dashboards/00-DASHBOARD, Daily-Dashboards/Dashboards.md) all trying the same thing — none consolidated.
2. **FFFF (Findings/Flags/Friction/Flow) is the de-facto canonical structure** — appears in 4 files, never propagated.
3. **The `.claude-garbage-` prefix on 3 of the most useful dashboards** suggests an abandoned cleanup pass; their Dataview queries are actually the most reusable.
4. **Per-metric trend tables (SBI/SI/MBI/IRR/SDR/OMR)** are clean and copy-paste-ready — the closest thing to a real working dashboard in the entire crop.
5. **faerie-vault is dashboard-bare** — Dashboards/ folder is empty except for a 0-byte stub; canonical work should land there.
