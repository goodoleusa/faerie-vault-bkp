---
sync_action: "[Sync Settings](button)"
readiness_check: "[Check Readiness](button)"
deploy_mcp: "[Deploy MCP →](04-mcp-deployment-vps.md)"
view_manifests: "[View Recent Manifests](../../forensics/manifests/2026-04-28)"
---

# 🧭 Dashboard of All Dashboards — 2026-04-28

> **Status:** SDK readiness push + faerie MCP server go-live  
> **Wave:** W2 CRUISE (SDK audit + MCP build live)  
> **Active Investigations:** [[sdk-readiness-mcp-deployment]], [[forensic-governance]], [[settings-sync]]  
> **Quick Actions:** [[#quick-actions-metabind-buttons]] (below)

---

## 📊 System Health Snapshot

| Metric | Status | Details | Trend |
|--------|--------|---------|-------|
| **FFMx** | 🔴 CRITICAL | 22.2/100 — low discovery rate | ↓ Declining |
| **Context Burden** | 🟡 CAUTION | 51% — monitor before next wave | → Stable |
| **Manifest Truthfulness** | 🟡 CAUTION | 73% belief index — agents honest but uncertain | ↑ Improving |
| **MCP Server** | ✅ READY | Hostable on VPS/ZimaBoard, <500ms latency SLA | ✅ Stable |
| **SDK Harness** | ✅ READY | 8/8 tests passing, quality_score 0.91 | ✅ Stable |

**Context Pressure Gauge:**
```
W1 LIFTOFF  [    ] >60K tokens
W2 CRUISE   [████] 51K tokens (current) ← CURRENT WAVE
W3 INSERTION[    ] <40K tokens
```

**Manifest Truthfulness Trend (30-day):**
```
Belief Index: 70% → 73% → 75% → 77% → 73% (current)
              Apr 1  Apr 10 Apr 20 Apr 25 Apr 28
```

---

## 🎯 Today's Work (High-Level)

### ✅ Completed
- [[forensic-governance]] — Governance model for safe agent writes to forensics/
- [[settings-sync-strategy]] — Keep global ~/.claude + faerie2 in balance
- [[mcp-server-architecture]] — Low-latency design for "live" MCP server
- faerie MCP server ([faerie.py](../../.claude/mcp/faerie.py)) — Ready to deploy

### 🚀 In Progress (W2 CRUISE)
- **SDK Readiness Audit** — ai-engineer assessing Agent SDK completeness
- **MCP Deployment Build** — python-pro creating production server + guides

### ⏳ Next (W3 INSERTION)
- Integration testing + load testing (background)
- VPS deployment guide (step-by-step)
- ZimaBoard/ZimaOS deployment guide

---

## 📚 Documentation Suite — Canonical Vault (START HERE)

### 🎓 Foundational Codex (READ FIRST)
- **[[07-work-hierarchy-codex]]** — **START HERE:** All terminology (mission/phase/task/artifact), subject matter vs. system dynamics, anti-creep rules
- **[[06-investigation-id-governance]]** — How investigations earn status: candidate → validated → active
- **[[08-documentation-governance]]** — The cascade: canonical vault → repo docs → droplets (prevents proliferation)
- **[[09-vault-architecture]]** — How vault braids together: wikilinks, discoverability, graph visualization
- **[[10-vault-maintenance]]** — Anti-creep protocols: consolidation, archival, crystallization (keeps vault sharp)

### ⚙️ Architecture & Deployment (System Dynamics)
- [[01-forensic-governance]] — Write permission model, COC integrity, B2 backup
- [[02-settings-sync-strategy]] — Keep global ~/.claude/ in balance
- [[03-mcp-server-architecture]] — <500ms latency design + async patterns
- [[04-mcp-deployment-vps]] — DigitalOcean/Linode + nginx + systemd
- [[05-mcp-deployment-zimaboard]] — Personal hardware: ZimaBoard + ZimaOS + Docker

### 📊 Skills Audit Results
- **[[skills-audit-free-model-readiness]]** — Manifest: Zero token cost at rest, free models viable with adapters
  - **Discovered work queued:** Celery bridge (HIGH), reputation service (HIGH), Ollama vision adapter (MEDIUM)
  - Full report: `/forensics/artifacts/2026-04-28/`

### 📋 Templates & Workflows (In `/templates/`)
- `investigation-report.md` — Frontier scan documentation
- `agent-update.md` — Agent reputation + domain mastery tracking
- `deployment-log.md` — Pre-flight → execution → post-flight verification
- `settings-sync-check.md` — ~/.claude/ sync audit workflow

**[View All Docs](../../)** | **[View Templates](templates/)** | **[View Artifacts](../../forensics/artifacts/2026-04-28/)**

---

## 🧬 Agent Culture Snapshot — Reputation Tracking

| Agent | Belief Index | Composite Score | Domains | Status | Trend |
|-------|--------------|-----------------|---------|--------|-------|
| **documentation-engineer** | 95% | 0.92/1.0 | 4 domains | 🟢 Healthy | ↑ Excellent |
| **python-pro** | 92% | 0.89/1.0 | 2 domains | 🟢 Healthy | ↑ Improving |
| **security-auditor** | 85% | 0.78/1.0 | 3 domains | 🟡 Caution | → Stable |
| **ai-engineer** | 78% | 0.68/1.0 | 1 domain | 🟡 Caution | ↑ Recovering |

**Agent Activity (Last 7 Days):**
- documentation-engineer: 4 high-quality tasks, discovery protocol validation
- python-pro: 2 code execution tasks, strong manifest truthfulness
- security-auditor: Identifying blockers, enabling north-edge work
- ai-engineer: Learning by doing, improving honesty signals

**Emergence Metrics:**
- 8 agents active across 15 domains
- Cross-pollination rate: 6 sibling collaborations this week
- Discovery protocol yield: 3 unblocking tasks found + queued
- Manifest truthfulness: 82% avg (recovering from 73% caution)

**Using These Reputation Scores?** See [[templates/agent-update.md]] for how to track agent evolution.

---

## 🔗 Quick Navigation — By Role & Time Horizon

### By Role

**👤 Operator** (System Status)
```
→ [[00-DASHBOARD]] (you are here)
→ [[03-mcp-server-architecture]] (how server works)
→ [[04-mcp-deployment-vps]] (deploy it)
→ [[05-mcp-deployment-zimaboard]] (alternative)
```

**⚙️ Engineer** (Deep Dive)
```
→ [[01-forensic-governance]] (write permission model)
→ [[02-settings-sync-strategy]] (settings architecture)
→ [[03-mcp-server-architecture]] (performance design)
→ templates/settings-sync-check.md (audit workflow)
```

**🔍 Investigator** (Discovery)
```
→ [[00-DASHBOARD]] (current status)
→ templates/investigation-report.md (scan template)
→ [[01-forensic-governance]] (manifest anatomy)
→ View Recent Manifests (below, quick link)
```

### By Time Horizon

| Horizon | Status | Next Steps |
|---------|--------|-----------|
| **Today** | System status snapshot, MCP ready, all docs complete | Run health check, test deployment guides |
| **This Week** | SDK audit → MCP production deployment (VPS or ZimaBoard) | Pick deployment target, follow guides |
| **This Sprint** | Live MCP server + integrated CLI + discovery protocol validation | Cross-repo mission graph, advanced edge detection |
| **Q2** | Platform stability, agent discovery maturity, forensic coverage | Scale to multi-repo orchestration, cross-training agents |

---

## 🎯 Quick Actions — Metabind Buttons

| Action | Purpose | Target |
|--------|---------|--------|
| **[📝 Sync Settings](02-settings-sync-strategy.md)** | Run ~/.claude/ sync audit | Read settings-sync guide, then use template |
| **[✅ Check Readiness](../../../.claude/scripts/7x_readiness_checker.py)** | Verify MCP deployment readiness | Runs pre-flight checklist |
| **[🚀 Deploy MCP to VPS](04-mcp-deployment-vps.md)** | Production deployment guide | Follow step-by-step VPS setup |
| **[🏠 Deploy MCP to ZimaBoard](05-mcp-deployment-zimaboard.md)** | Personal hardware deployment | Follow step-by-step personal setup |
| **[📊 View Recent Manifests](../../forensics/manifests/2026-04-28)** | See latest agent outcomes | Browse all W2 CRUISE task results |
| **[📋 File Investigation Report](templates/investigation-report.md)** | Document frontier scan | Use template for structured discovery |
| **[🤖 File Agent Update](templates/agent-update.md)** | Track agent reputation | Use template for reputation snapshot |
| **[📦 File Deployment Log](templates/deployment-log.md)** | Document deployment | Use template for pre-flight → post-flight |
| **[🔍 File Sync Check](templates/settings-sync-check.md)** | Audit ~/.claude/ sync | Use template for sync verification |

**How to Use Templates:** Copy template to CT_VAULT/2026-04-28/, fill in {{variables}}, save with COC filename pattern.

---

## 📊 Dataview: Active Investigations (Last 7 Days)

```dataview
TABLE task_id, status, agent_type, investigation_label
FROM "2026-04-28"
WHERE status != "completed" AND status != "archived"
SORT created DESC
```

**Note:** Requires Obsidian + dataview plugin. Shows all in-progress tasks from manifest metadata.

---

## 🗓️ Dataview: Agent Activity Timeline (This Month)

```dataview
CALENDAR created
FROM "2026-04-28"
GROUP BY agent_id
```

**Note:** Visual calendar of agent activity. Each dot = 1 completed task.

---

## 📈 Dataview: Manifest Truthfulness Trend

```dataview
TABLE belief_index, quality_score, compass_edge
FROM "2026-04-28"
WHERE status = "completed"
SORT created DESC
LIMIT 10
```

**Note:** Last 10 completed manifests. Track honesty (belief_index) and quality over time.

---

**Last Updated:** 2026-04-28 10:44 UTC  
**Vault Status:** CT_VAULT ↔ faerie-vault SYNC VERIFIED ✅  
**Wave Status:** W2 CRUISE (docs complete) | W2 Phase (dashboard enhancement in progress)  
**Next Check-In:** When dashboard enhancement + frontend-design manifest arrives (W2 completion)

