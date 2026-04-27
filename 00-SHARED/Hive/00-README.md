---
type: meta
tags: [meta, docs, index, business, platform]
doc_hash: sha256:ebb2b36616132fcd6fe126e89c66d3a5137d9c0afe776ce7555b865006f1dfc8
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---

# 00-META — Doc index and reading order

## 🚀 FOR OPERATORS: Build This as a Platform

**This is not just a tool. This is infrastructure for emergent intelligence.**

→ **[[BUSINESS-MODEL-PLATFORM|BUSINESS-MODEL-PLATFORM]]** — **START HERE if you're building a SaaS/platform around this.** Revenue model, network effects, how to monetize HONEY sharing, competitive moats, go-to-market strategy. $1-2M ARR potential within 18 months.

**Related docs:**
- [[MULTI-SESSION-DAG-DESIGN]] — How independent teams coordinate without knowing each other (the technical foundation)
- [[01-ARCHITECTURE]] — Remote deployment architecture (manifest API, HONEY registry)

---

## 📚 FOR INVESTIGATORS: Use This Today

**Start here for the big picture:** [[00-OVERVIEW|00-OVERVIEW]] — why this vault exists, the multi-fold problem, core principles, metaphors, solving the black box, OSINT and the crossroads, 2026 orchestration, [entity-name]. Read it first.

**Start collaborating:** [[KICKSTART-COLLAB|KICKSTART-COLLAB]] — where to drop tasks and briefs (`00-SHARED/…`), folder naming (**no new numeric prefixes** except protected/private/tooling), first-hour checklist.

**Human ↔ agent async:** [[12-ASYNC-HUMAN-AGENT-BRIDGE|12-ASYNC-HUMAN-AGENT-BRIDGE]] — same note for structured agent output and human read/reply (sections + optional traceability fields).

---

Canonical docs for the CyberOps vault. The table below is **suggested reading order by topic** — meta filenames still use numbers like `01-ARCHITECTURE` for sorting only; **you do not need numbered names for your own case folders** (see KICKSTART-COLLAB).

### For Operators (Building the Platform)

| Step | Doc | Purpose |
|-------|-----|--------|
| **FIRST** | [[BUSINESS-MODEL-PLATFORM\|BUSINESS-MODEL-PLATFORM]] | **Platform vision:** Revenue model, network effects, HONEY marketplace, threat synthesis engine, competitive moats, go-to-market. This is what faerie becomes at scale. |
| **Then** | [[MULTI-SESSION-DAG-DESIGN\|MULTI-SESSION-DAG-DESIGN]] | **Technical foundation:** How teams coordinate through manifests. f(0) scaling. The infrastructure that enables the business model. |
| **Then** | [[01-ARCHITECTURE\|01-ARCHITECTURE]] | **Remote deployment:** Manifest API, HONEY registry, agent integration, multi-session orchestration. |

### For Investigators (Using This Today)

| Step | Doc | Purpose |
|-------|-----|--------|
| **Start** | [[00-OVERVIEW\|00-OVERVIEW]] | **Big picture:** Problem (a–e), principles, metaphors, black box, Why this exists, 2026, [entity-name], dyad, what this vault is. Read before architecture. |
| **Collab** | [[KICKSTART-COLLAB\|KICKSTART-COLLAB]] | **Hands-on:** inboxes/outboxes under `00-SHARED/`, naming policy, kickstart checklist. |
| **Bridge** | [[12-ASYNC-HUMAN-AGENT-BRIDGE\|12-ASYNC-HUMAN-AGENT-BRIDGE]] | **Async loop:** YAML + body layout so agents write and humans respond in the **same** note; optional `vault_path` / `sha256`. |
| **01** | [[01-ARCHITECTURE\|01-ARCHITECTURE]] | **Canonical** architecture: what the vault is, topology (laptop ↔ ZimaBoard ↔ workstation), folder layout, roles, task lifecycle, memory, QuickAdd+Blueprint summary, agent integration. |
| **02** | [[02-QUICKADD-SETUP\|02-QUICKADD-SETUP]] | Step-by-step QuickAdd setup: Template choices, Macros, global settings, manual checklist. |
| **03** | [[03-AGENT-HANDOFF-EXPLAINER\|03-AGENT-HANDOFF-EXPLAINER]] | **Agent handoff explainer**: how QuickAdd globals actuate handoff, request/hop flow through the system, iterative improvement and self-healing, and how the workstation agent keeps the human updated via the vault (e.g. `03-Agents/agent.md`). |
| **04** | [[04-QUICKADD-GLOBAL-VARS-HANDOFF\|04-QUICKADD-GLOBAL-VARS-HANDOFF]] | Reference: QuickAdd global variables for handoff (HandoffBlock, ResearchFolder, etc.), contract (location + format), and integration points (runner, rule, skill, hook). |
| **05** | [[05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK\|05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK]] | Agent insights dashboard, agent.md one-stop shop, raw vs approved, sync-back to air-gap, agent write map, and concise language for human decisions. |
| **06** | [[06-TEST-TASK-WALKTHROUGH\|06-TEST-TASK-WALKTHROUGH]] | **Test walkthrough**: One task taken through the full process (create → agent 1 → handoff → agent 2 → status); shows how the task links out to investigation, entity, handoff, agent-history, logbook, agent.md. |
| **08** | [[08-AGENT-ADAPTIVE-CONTEXT-AND-EVOLVING-PROMPT\|08-AGENT-ADAPTIVE-CONTEXT-AND-EVOLVING-PROMPT]] | **What to collect from the day's tasks** for maximum agent adaptation, and how to maintain a **continuously crystallized, evolving prompt** the agent reads at run start. |
| **09** | [[09-HUMAN-PROMOTES-AI-EXECUTES\|09-HUMAN-PROMOTES-AI-EXECUTES]] | **Vault-wide theme:** Human promotes, AI executes. Where humans must intervene; concise approval language for fast review. |
| **SCALE** | [[MULTI-SESSION-DAG-DESIGN\|MULTI-SESSION-DAG-DESIGN]] | **Multi-session orchestration:** How to run multiple concurrent teams with zero coordination overhead. Manifest-based dependency signaling; agents self-coordinate via shared manifest directory. See 01-ARCHITECTURE §14. |
| **QUALITY** | [[STREAMING-AND-CITATIONS-GUIDE\|STREAMING-AND-CITATIONS-GUIDE]] | **Agent quality standards:** Mandatory streaming (5-20 findings/run, emit immediately) + mandatory citations (100% citation accuracy). These rules enable cross-session trust and evalbot scoring. Current baseline: 11% → Target: 100%. |
| **BUSINESS** | [[BUSINESS-MODEL-PLATFORM\|BUSINESS-MODEL-PLATFORM]] | **If you're scaling this:** Platform vision, revenue model, HONEY marketplace, threat synthesis. How faerie becomes a network-effect business. (Also see "For Operators" section above.) |
| **11** | [[11-FAERIE-IMPACT-AB\|11-FAERIE-IMPACT-AB]] | **Honest A/B:** native session memory vs faerie (`HONEY`, `NECTAR`, inbox, queue, agent cards); demo protocol and confounders for marketing. |

**Redirects from vault root:** [[ARCHITECTURE]], [[QUICKADD-BLUEPRINT-SETUP]], [[QUICKADD-GLOBAL-VARS-AGENT-HANDOFF]], [[QUICKADD-AND-BLUEPRINTS]] point here. Keep architecture in 01; avoid duplicating content. **Test flow:** See 06 for a full task walkthrough and link map. **Paths:** In **CyberOps-UNIFIED**, agent inboxes live under **`00-SHARED/`** — not always at vault root; see KICKSTART-COLLAB.
