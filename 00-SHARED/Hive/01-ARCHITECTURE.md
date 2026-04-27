---
type: meta
tags: [meta, architecture, design, how-to, setup]
created: 2026-03-10
updated: 2026-03-24
doc_hash: sha256:411a54ae8ab4e242e1957b23568b563f8bf2e67c933096db8deb9f49c7eda522
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---

# CyberOps Vault — Architecture, Setup & Use

Single reference for what this vault is, how it’s structured, how to set it up (Obsidian, QuickAdd, Blueprints), and how agents (Claude, OpenClaw, Cursor) integrate with it.

**Doc index:** See **[[00-README]]** for reading order. This doc is **01-ARCHITECTURE** (canonical). For the high-level narrative, problem statement, principles, and metaphors, see **[[00-OVERVIEW]]**.

---

## Part I — Architecture

---

## 1. What This Is

A shared knowledge engine where **humans and AI agents collaborate asynchronously** on OSINT investigations. The **vault** is the **collaboration and memory surface** — agents read and write within policy (e.g. `00-SHARED/`); humans steer via promotion and edits. **Original forensic masters** and **chain-of-custody (COC)** artifacts live in the **investigation repo** (e.g. CyberTemplate: `scripts/audit_results/`, forensics paths), not “instead of” the vault but **alongside** it: vault = conceptual home and handoff; repo = COC originals. **Human promotes, AI executes:** humans review, correct, and promote raw output; agents execute tasks and stop at clear intervention points. See [[09-HUMAN-PROMOTES-AI-EXECUTES]] and [[00-OVERVIEW]] (*Data sovereignty* — three layers).

**Investigation domains**: Cults/high-control groups, money laundering, human trafficking, shadow state policy, cyber infrastructure threats.

**Design philosophy**: Local-first, air-gapped compute, async collaboration, evidence-grade rigor.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR LAPTOP (Interface)                       │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐    │
│  │ Obsidian  │  │ Claude Code  │  │ Browser (cybertemplate) │   │
│  │ (vault UI)│  │ (local agent)│  │ (report viewer)         │   │
│  └─────┬─────┘  └──────┬───────┘  └────────────────────────┘   │
│        │               │                                         │
│        └───────┬───────┘                                         │
│                │ reads/writes vault files                         │
│        ┌───────▼────────┐                                        │
│        │  VAULT (local) │ ◄── Syncthing (encrypted P2P)          │
│        └───────┬────────┘                                        │
└────────────────│─────────────────────────────────────────────────┘
                 │ Syncthing (LAN / relay)
                 │
┌────────────────│─────────────────────────────────────────────────┐
│  ZEROTIER / P2P (same private net)                               │
│  ┌─────────────┴─────────────┐                                   │
│  │  ZIMABOARD (coordinator)  │   WORKSTATION (air-gapped compute)│
│  │  VAULT (master)           │   VAULT (copy)                    │
│  │  OpenClaw, 00-Inbox       │   ◄── Syncthing P2P with          │
│  │  active_agents.json      │       ZimaBoard (or ZeroTier)     │
│  └──────────────────────────┘   Poll script checks local       │
│         Syncthing P2P / ZeroTier │ vault for new tasks           │
│         between these two        │ agent_runner: sanitize →       │
│                                  │ claim → run LLM → write       │
│  FIREWALL (workstation): No inbound from internet.               │
│  Outbound: ZeroTier/P2P + LLM APIs only.                         │
└──────────────────────────────────────────────────────────────────┘
```

**Topology:** The **workstation** and the **ZimaBoard** (remote) are on the **same ZeroTier network** (or otherwise P2P via Syncthing). The vault syncs between them over that private net — Syncthing or ZeroTier, not the public internet. The workstation is still **air-gapped from the internet** (no inbound); it only has outbound to that private net and to LLM APIs. A **poll script** on the workstation runs periodically (or on demand), checks the **local** vault (which Syncthing keeps in sync with ZimaBoard) for new tasks, then runs agent_runner (sanitize → claim → run → write back).

---

## 3. Vault Directory Structure

**CyberOps-UNIFIED (this repo):** Task inboxes, human/agent outboxes, and **Memories** for sync live under **`00-SHARED/`**, not at vault root. Inside **`00-SHARED/`**, subfolders use **plain names** (`Inbox/`, `Agent-Outbox/`, `Hive/`, `Memories/`). See **[[KICKSTART-COLLAB]]** for where to drop a first task. **Folder naming:** we are **not** requiring numeric prefixes on **new** folders you add; keep numbers for **protected/private** (`01-PROTECTED/`) and the **tooling-enforced** agent zone (`00-SHARED/`). See **[[VAULT-RULES]]**.

The tree below is a **legacy / generic CyberOps layout** (many clones use inbox + memories at root). For **this vault**, use **`00-SHARED/Inbox/`** (or **`Agent-Inbox/`** per runner) and **`00-SHARED/Memories/`**.

```
CyberOps/   # reference layout — map agent zone to 00-SHARED/ in UNIFIED
├── 00-META/            # Canonical docs — read 00-README for suggested order
├── 00-Inbox/           # Task drop (in UNIFIED: use 00-SHARED/Inbox/ or Agent-Inbox/)
├── 01-Memories/        # Long-term context (in UNIFIED: 00-SHARED/Memories/)
│   ├── human/          # Human preferences, decisions, corrections
│   └── agents/        # Agent learnings, discoveries, patterns
├── 02-Skills/          # Reusable agent skill specs (prompt templates)
├── 03-Agents/          # Agent state, roster, execution logs
│   ├── active_agents.json
│   ├── agent-history.md
│   ├── agent.md        # Workstation agent status/lessons (agent writes; see 00-META/03-AGENT-HANDOFF-EXPLAINER)
│   └── agent-logs/     # Raw stdout/stderr per execution
├── 10-Investigations/  # Active investigation case files
├── 20-Entities/        # People, orgs, domains, IPs, threat actors
│   ├── People/
│   ├── Organizations/
│   ├── IPs/
│   ├── Domains/
│   └── Infrastructure/
├── 30-Evidence/        # Pipeline-linked evidence with provenance
├── 0a-SpiderFoot-Runs/ # Full-run SpiderFoot CSV exports; one subfolder per run; process into Evidence + Entities
├── 40-Intelligence/    # Finished reports and analysis
├── 25-Networks/        # Relationship maps and link analysis
├── 50-Financial/       # Money trails and transaction analysis
├── 60-Chronology/      # Timelines and temporal analysis
├── 70-Sources/         # Source registry and reliability tracking
├── 99-Archives/        # Completed work (permanent record)
├── Blueprints/         # Blueprint plugin templates (18 templates)
├── Templates/          # QuickAdd copies of blueprints (for create-in-folder)
├── scripts/            # Companion scripts (agent_runner, etc.) — see scripts/README.md
└── Dashboards/         # Dataview dashboards
```

---

## 4. Roles

### Human (You)
- **Creates tasks** by dropping `.md` files in **`00-SHARED/Inbox/`** or **`00-SHARED/Agent-Inbox/`** (match your runner); legacy docs may say `00-Inbox/` at root — **not** this vault.
- **Reviews agent output** in investigation folders, **`00-SHARED/Agent-Outbox/`**, and dashboards
- **Corrects memories** in **`00-SHARED/Memories/human/`** — agents read corrections
- **Directs strategy** by updating `10-Investigations/` (or any case folder you use — **new folders need not be numbered**)
- **Final authority** on evidence assessment and tier promotion

### Agent (AI Worker)
- **Claims tasks** from the configured inbox under **`00-SHARED/`** by updating frontmatter
- **Reads context** from **`00-SHARED/Memories/`** before executing
- **Executes skills** from `02-Skills/` definitions
- **Writes findings** to appropriate folders (20-70)
- **Updates own memories** in `01-Memories/agents/` after task completion
- **Reports what it learned** in agent.md (Lessons learned) and, **only when it applies to all agents in the swarm**, in `agent-logbook.md`; updates task status.

### ZimaBoard (Coordinator)
- **Routes tasks**: OpenClaw watches `00-Inbox/`, assigns to available workers.
- **Same net as workstation**: On the **same ZeroTier or P2P Syncthing** network as the workstation; vault syncs between them over that private link.
- **Syncs vault**: Syncthing (device-authenticated) with laptop and with workstation.
- **Monitors health**: Checks agent registry if present (e.g. `03-Agents/active_agents.json` in layouts that use it).
- **Never computes**: No LLM inference, no data processing.

### Workstation (Compute Engine)
- **Same private net as ZimaBoard**: Workstation and ZimaBoard are on the **same ZeroTier network** (or P2P via Syncthing). The vault syncs between them over that private link — no public internet between these two.
- **Air-gapped from internet**: No **inbound** from the internet. Outbound only to the ZeroTier/P2P net and to LLM APIs.
- **Poll + run**: A script on the workstation **polls** the local vault (kept in sync by Syncthing with ZimaBoard) for new tasks, then runs agent_runner (sanitize → claim → run LLM → write). Results sync back via Syncthing.
- **State**: Marks tasks done, appends to agent history in the local vault; Syncthing propagates to ZimaBoard (and to laptop if in the sync mesh).

---

## 5. Communication Protocol

### Task Lifecycle (the "Handshake")

```
LAPTOP                ZIMABOARD + WORKSTATION (same ZeroTier / P2P net)
  │
  │  1. Create task.md → Syncthing → ZimaBoard has vault with task
  │
  │  2. On private net: Syncthing P2P (or ZeroTier) syncs vault
  │     from ZimaBoard to workstation (or both share a sync group).
  │
  │  3. Poll script on workstation runs (cron/timer/manual),
  │     sees local vault has new task in 00-SHARED/Inbox (or configured inbox).
  │
  │  4. agent_runner: sanitize task → claim → run LLM → write results
  │     to local vault.
  │
  │  5. Syncthing propagates workstation’s changes back to ZimaBoard
  │     (and laptop if in same sync mesh).
  │
  │  6. You see results on laptop.
```

Workstation and ZimaBoard are on the **same ZeroTier or P2P Syncthing network**; the workstation does not accept inbound from the internet, only outbound to that private net and to LLM APIs.

### Memory Sync Protocol

**Agent writes:** Task file `status: done`; append to agent history / **`agent.md`** where your layout keeps them (some vaults: `03-Agents/` at root; **UNIFIED:** often under **`00-SHARED/`** or CyberTemplate — follow your active paths). Append to **`00-SHARED/Memories/agents/agent-logbook.md`** **only** when the learning applies to **all agents in the swarm** (rare); otherwise put learnings in agent.md "Lessons learned" or the task file.

**Human corrections:** Edit **`00-SHARED/Memories/human/corrections.md`** (or your human memory path); agents read it on the next task. Additive — "Agent said X, but actually Y."

**Key principle:** Agents own their memory namespace, humans own theirs. Neither overwrites the other.

### Timeliness

| Action | Latency |
|--------|---------|
| Task creation → ZimaBoard has it | Syncthing: seconds to minutes (LAN) |
| ZimaBoard ↔ workstation vault sync | Syncthing/ZeroTier on same private net |
| Poll script on workstation sees new task | Depends on poll interval (e.g. every 5 min) |
| Agent claims + runs → completes | Minutes to hours |
| Results back to laptop | Syncthing propagates from workstation via ZimaBoard (or direct if in same mesh) |

### Task sanitization (workstation, if remote is compromised)

If the ZimaBoard or the vault is compromised, a task file could contain **malicious content** (e.g. shell metacharacters, prompt-injection text aimed at the LLM, or payloads that might be used in a script). The workstation should apply a **light sanitization step** before using task content:

- **Never eval or source** task body or frontmatter as code. Treat all task content as **data**, not executable.
- **Before passing to shell**: If any part of the task (e.g. file path, summary) is interpolated into a shell command, sanitize or reject: strip NUL and control characters; reject or escape lines that contain shell metacharacters (e.g. `;`, `|`, `$(`, backticks, `\n` in a way that could break quoting). Prefer passing paths and strings via arguments or stdin, not by building a command string from task text.
- **Before passing to the LLM**: Optionally strip or escape control characters and limit length to reduce prompt-injection surface; consider a small allowlist of frontmatter keys when reading task metadata.
- **Implement in agent_runner**: Run sanitization immediately after fetching a task and before claiming or executing. Reject the task (log and skip) if it fails a safety check; do not run the LLM on unsanitized task body.

This is **defense in depth**: it does not replace keeping the ZimaBoard and vault trusted, but it limits damage if the remote is compromised or a malicious task is introduced.

---

## 6. Threat Model (summary)

- **Assets:** Investigation data, agent compute, memories, evidence chain, source identities.
- **Mitigations:** Task signing (HMAC-SHA256), Syncthing device auth, no inbound on workstation, evidence hashes, signed memories. See full tables in original design notes if needed.

---

## 7. Memory Architecture

**01-Memories/**  
- `human/` — only human writes (corrections, preferences, decisions).  
- `agents/` — only agents write (agent-logbook.md for **swarm-wide** learnings only — rare; patterns, session notes). All other agent learnings go in 03-Agents/agent.md or the task file.  
- `shared/` — both read; human approves merges. **Research logs** and **agent handoff blocks** live here so the next session or agent can read them.

**Handoff format (async context):** In `01-Memories/shared` (and optionally in investigation “Context Snapshot” or “Agent questions” sections), use a canonical two-line block so runner scripts, Claude Code rules, skills, and hooks can parse it: **`Agent: <who>`** and **`Handoff: <what>`**. QuickAdd can insert this via the **HandoffBlock** global and an “Insert handoff snippet” Capture (see **[[04-QUICKADD-GLOBAL-VARS-HANDOFF]]**). Agents discover handoffs by reading that folder and parsing this format; they are not pushed automatically.

**When an agent completes a task:**  
1. Append to `01-Memories/agents/agent-logbook.md` **only if** the learning applies to **all agents in the swarm** (rare); otherwise put learnings in agent.md "Lessons learned" or the task file. Use the standard Learning format when you do append.  
2. Update `03-Agents/agent-history.md`.  
3. Update **`03-Agents/agent.md`**: fill the relevant sections (Last run, Last 24h, Open questions for human, Ideas, Pain points, Scope or struggle if scope too broad, First impressions (data), Insights (in progress), Recommended analyses, Lessons learned, Suggested improvements). All of these go in agent.md only — do not spread questions, ideas, pain points, or insights across the vault. If you have 3+ open questions, add to Pain points / Scope or struggle: "Scope too broad? Consider refining subagent or splitting task." See **[[05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK#1.2a Agent write map: what agents put where (single group)]]** and **§1.2b Agent separation**.  
4. Set task frontmatter: `status: done`, `completed_date`, `result_summary`, `output_files`.

**When you correct an agent:** Append to `01-Memories/human/corrections.md` with "Agent claimed / Correction / Evidence / Impact." Agents load it before the next run.

### 7.1 Raw vs approved (approval model)

The vault uses a **raw vs approved** framing instead of "agents vs human" so the emphasis is on **collaboration**: AI outputs are **raw** until a human approves them; only **approved** content is used by agents to change how they behave in the vault.

| Layer | Meaning | Where | Who writes | Who uses for behavior |
|-------|---------|--------|------------|------------------------|
| **Raw** | AI output not yet approved | `01-Memories/agents/` (logbook, patterns), `03-Agents/agent.md`, suggested improvements (agent.md or `03-Agents/suggestions.md`) | Agent | Humans review; agents may read for status/awareness but **must not** apply raw suggestions as rules |
| **Approved** | Human-approved; safe for agents to use | `01-Memories/human/corrections.md`, `03-Agents/suggestions-approved.md`, approved context in `03-Agents/agent-context-evolving.md` | Human (or human promotes from raw) | Agents read for corrections, rules, and process improvements |

**Rule:** **Human promotes, AI executes.** All process improvements and anything that changes how agents behave in the vault **must be approved by a human** before agents use it. Raw outputs from AI are reviewed by humans (e.g. via [[Agent-Insights]]); when approved, promote to **approved** locations (e.g. copy approved suggestions into `suggestions-approved.md`; apply via a human-run script to real config if needed). Agents then read only from **approved** sources for behavior-changing context.

**agent.md as one-stop shop:** **`03-Agents/agent.md`** is the single place humans look to see what's going on: status, last 24h insights, open questions, lessons, and suggested improvements. The agent writes there; you review and answer there. Anything you want to turn into agent behavior (rules, process changes) you promote from agent.md (or suggestions) into **approved** locations and optionally run a human-approved script (e.g. apply `03-Agents/suggestions-approved.md` to the real config). See [[05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK]] for the suggestions-approved flow.

---

## 8. Blueprint Templates & Dataview Schema

### Blueprints (22 total)

- **Agent collaboration:** Task-Inbox, Agent-Skill, Memory-Entry, Daily-Research, Normalize-Frontmatter  
- **Entity profiling:** Entity-Stub, Person, Organization, **Organization-Master** (org + HCG combined), Threat-Actor, IP-Address, Domain, High-Control-Group  
- **Investigation:** Investigation-Case, Evidence-Item, Intelligence-Report, Shadow-Operation, Financial-Trail, Network-Map, Source-Assessment, Chronology-Entry  

**Organization-Master** — Single blueprint that merges **Organization** and **High-Control-Group**. Use it when you want one org note with all options: company/NGO fields (registration, corporate structure, financial profile, risk indicators) and HCG fields (BITE model, front organizations, recruitment, legal actions, survivor accounts). Set `entity_type: organization` and `org_subtype` (e.g. company, ngo, high-control-group) in frontmatter. **Shadow-Operation** and **Financial-Trail** remain separate (investigation types, not entity notes).  

### Dataview / frontmatter schema

| Type | Folder | Key fields | Notes |
|------|--------|------------|--------|
| `task` | 00-Inbox | `type`, `status`, `task_id`, `priority`, `assignee`, `deadline`, `review_verdict`, `parent`, `sibling`, `child`, `touched_by`, `task_signature` | Pending: `status != "done"`. After completion, human sets `review_verdict` (pending / approved / needs-revision); approved tasks move to 99-Archives. **touched_by:** each agent who completes or returns the task appends their id. **task_signature:** reserved for HMAC-SHA256 when task signing is implemented (see 10-TASK-LINEAGE). |
| `investigation` | 10-Investigations | `type`, `status`, `case_id`, `threat_level`, `last_update`, `parent`, `sibling`, `child` | Parent = larger investigation; child = sub-investigations/threads, entities, evidence |
| `entity` | 20-Entities/* | `type`, `entity_type`, `entity_name`, `status`, `confidence_level`, `parent`, `sibling`, `child` | person, organization, domain, ip-address, etc. |
| `evidence` | 30-Evidence | `type`, `evidence_id`, `tier`, `confidence_level`, `parent`, `sibling`, `child`, `hypothesis_support` | Pipeline: `pipeline_run`, `source_sha256` |
| `source` | 70-Sources | `type`, `source_name`, `reliability_rating`, `information_rating` | NATO Admiralty style |
| `daily` | 01-Memories/shared | `type`, `date`, `investigator` | Research logs; both human and agent read for async handoff |

**Cross-linking (Breadcrumbs hierarchy):** All note-to-note relationships use **parent**, **sibling**, and **child** as multi-line arrays of `[[wikilinks]]`. Use Obsidian wikilinks so links are clickable and **Excalibrain** and **Breadcrumbs** can show the graph. Convention: **parent** = notes above (e.g. investigation an entity belongs to; larger investigation a thread belongs to); **sibling** = same-level notes; **child** = notes below (e.g. entities/evidence under an investigation; evidence under an entity). Example: `parent: ["[[Case Alpha]]"]`, `sibling: ["[[Org B]]"]`, `child: []`.

**Task lineage and handback:** For **tasks** specifically — linking follow-ups/subtasks (parent/child/sibling), filling the **Compressed summary** so the next agent has context when a task returns to the inbox, and tracking parent→children without noise — see **[[10-TASK-LINEAGE-AND-HANDBACK]]**. Frontmatter for tasks uses **multi-line arrays** for tags, parent, sibling, child, touched_by; wikilinks in frontmatter must be `[[correctlyformatted]]` (quoted in YAML lists). Agents may create subtasks when completing a task and spawning a follow-up for another skill (or when the task/human requests it); the creating agent **must** write correct frontmatter on both the new task and the parent so lineage stays threaded.

**Dataview compatibility:** Dataview parses frontmatter wikilinks as **Link objects**, not strings. Comparing with `"[[Note]]"` fails (it looks for that string as a field on the linked page). Use **Link-to-Link**: `contains(parent, this.file.link)`, `contains(sibling, this.file.link)`, or `contains(child, this.file.link)` so “notes that reference this note” query correctly. Obsidian’s built-in **backlinks/forward links** are from `[[wikilinks]]` in body and frontmatter, so the same [[links]] drive both Dataview and the graph. **Backlinks/forward links** come from these frontmatter links and body wikilinks.

**If you prefer body links only:** You can put `[[Related Note]]` in the note body instead of (or as well as) frontmatter; then Obsidian backlinks/forward links and Excalibrain still work. Dataview can then use `FROM outgoing([[]])` (notes linked from this one) or backlink sources; our blueprint queries assume the link is in frontmatter so that “notes that reference this” can use `contains(..., this.file.link)`.

**Agent scratchpad (investigation templates):** Investigation-Case, Shadow-Operation, Financial-Trail, and Intelligence-Report blueprints include shared sections so agents can leave questions and findings for the human reviewer without losing insights: **Agent questions (for reviewer)**, **Interesting discoveries / scratchpad**, **New questions raised**, **Data needed to answer**, **Connections to other work**. The **[[Agent-Findings]]** dashboard lists recently updated investigations/reports; click any note to see the full evidence trail, what’s been answered, what new questions arose, and what data would be needed to answer them. Keeps agent mini-findings visible and easy to thread into other work.

**Light DB:** Frontmatter + Dataview = primary “DB.” Mutable agent state = `03-Agents/active_agents.json` only.

---

**Light DB:** Frontmatter + Dataview = primary "DB." Mutable agent state = `03-Agents/active_agents.json` only.

### Folder routing (async agent–human collab)

QuickAdd and agents create notes in folders chosen for the ZimaBoard/workstation handoff model (see FIRE ZimaBoard OpenClaw setup): tasks in **00-Inbox** (human or agent drops; agent claims); investigation output in **10–80**; agent-only writes in **01-Memories/agents/**; human-only in **01-Memories/human/**; **01-Memories/shared/** is for research logs and context both sides read so async handoff stays in sync. Today's Research Log therefore routes to **01-Memories/shared/**.

---

## 9. Companion scripts

**Location:** `scripts/` in the vault root (easy to find, syncs with the vault).

- **[[scripts/README]]** — Describes the folder and lists companion scripts.
- **agent_runner.ps1** / **agent_runner.sh** — Stubs for the workstation task loop: watch `00-Inbox/`, claim task, read `01-Memories/` + `02-Skills/`, run Claude/LLM, write results and update task/agent state. Implement the TODOs in the script for your environment.
- **Vault setup:** The one-time folder bootstrap is in the **cybertemplate** repo: `scripts/setup_vault.sh`. Point its `VAULT=` at this vault and run with Bash. **For this vault:** run `scripts/ensure_vault_folders.ps1` (Windows) or `scripts/ensure_vault_folders.sh` (Bash) when the vault is new or missing folders like `0a-SpiderFoot-Runs` — idempotent, no overwrites.

See §13 (Integrating agents) for how agents use the vault path and these scripts.

---

## 10. Data Flow & Pipelines

**Evidence pipeline:** rawdata → INGEST → CLEAN → TRANSFORM → ANALYZE → CURATE → REPORT (SHA-256, tier, etc.).  
**Vault bridge:** Pipeline outputs → Evidence Curator agent → `30-Evidence/` items with provenance and tiers.  
**SpiderFoot full runs:** Export CSVs into `0a-SpiderFoot-Runs/<run-folder>/` (one subfolder per run, e.g. by date and target). Process into `30-Evidence/` and `20-Entities/` (usernames, subdomains, etc.); keep raw CSVs in 35 so the vault stays organized. See **[[0a-SpiderFoot-Runs/README]]**.

---

## 11. Benefits & Open Questions

**Benefits:** Async collaboration, air-gapped security, evidence integrity, agent learning, human oversight, scalability, reproducibility, domain flexibility.

**Open questions:** Task signing implementation, memory crystallization, multi-agent coordination, evidence declassification, ZimaBoard deployment, backup strategy.

---

# Part II — Setup & Use

---

## 12. QuickAdd + Blueprints (Obsidian)

The **Blueprint** plugin has no settings UI (only commands). **QuickAdd** is configured to create notes from blueprints in the correct folders. **Step-by-step:** See **[[02-QUICKADD-SETUP]]** for filling out each QuickAdd Template and Macro option.

### Quick start (new vault or after clone)

1. Run **`scripts/setup_cyberops_vault.ps1`** (Windows) or **`scripts/setup_cyberops_vault.sh`** (Bash). This creates any missing vault folders and tells you how to import the QuickAdd package.
2. In Obsidian: **Settings → QuickAdd → Packages → Import package…** → select **`CyberOps-QuickAdd.quickadd.json`** (vault root). Import or duplicate each choice, then reload QuickAdd or restart Obsidian.
3. Use **Command Palette → QuickAdd** and pick any “(with Blueprint)” macro to create a note in the right folder with the blueprint applied.

The **CyberOps-QuickAdd.quickadd.json** package bundles 8 Template choices and 8 Macros (each runs the template then **Blueprint: Apply blueprint to note**). If import fails (e.g. QuickAdd schema change), use the manual checklist in [[02-QUICKADD-SETUP#4b. Checklist — Template choices and Macros to add]].

### One-time setup (manual)

1. **Reload QuickAdd** — Settings → QuickAdd (or restart Obsidian) so the configured choices appear.
2. **QuickAdd global variables** — For handoff snippets and consistent paths (e.g. `HandoffBlock`, `ResearchFolder`), see **[[04-QUICKADD-GLOBAL-VARS-HANDOFF]]**. Set in Settings → QuickAdd → Global Variables; not stored in the package.
3. **After creating a note** — Run **Command Palette** → **"Blueprint: Apply blueprint to note"** so `{{ file.basename }}`, dates, etc. are filled. Or add a **QuickAdd Macro** that runs the Template choice then **Apply blueprint to note** (one command = create + apply).

### QuickAdd commands

**Command Palette** → **QuickAdd** → choose one:

| QuickAdd choice | Creates note in | Prompted for |
|-----------------|-----------------|--------------|
| **New Task** | `00-Inbox/` | Task title |
| **New Person** | `20-Entities/People/` | Person name |
| **New Investigation** | `10-Investigations/` | Case name |
| **New Entity Stub** | `20-Entities/` | Entity name |
| **New Evidence Item** | `30-Evidence/` | Evidence ID/name |
| **New Source** | `70-Sources/` | Source name |
| **Today's Research Log** | `01-Memories/shared/` | Agent name → `YYYY-MM-DD-Research-AgentName.md` |
| **New Organization (master)** | `20-Entities/Organizations/` | Org name → full org + HCG sections in one note |

**Why only some blueprints have QuickAdd templates:** The initial set (Task, Person, Investigation, Entity Stub, Evidence, Source, Daily Research) covers the most common daily flows. The other blueprints (Threat-Actor, Thread, Domain, IP-Address, High-Control-Group, Shadow-Operation, Financial-Trail, Network-Map, Chronology-Entry, Intelligence-Report, Agent-Skill, Memory-Entry, Normalize-Frontmatter) are available via **Blueprint** commands: right-click folder → **New note from blueprint**, or **Apply blueprint to note** on an existing note. You can add more QuickAdd Template choices anytime (template path = `Templates/<Name>.md`, create matching `.md` from the blueprint). **Organization-Master** is the combined org+HCG option so one org note has every section you might need.

### Macros (create + apply in one go)

1. QuickAdd → Configure → Add choice → **Macro**.  
2. Name it (e.g. **New Task (with Blueprint)**).  
3. Add step: **QuickAdd: Run choice** → e.g. New Task.  
4. Add step: **Obsidian Command** → **Blueprint: Apply blueprint to note**.  
5. Save. Run the macro from Command Palette → QuickAdd.

### Where templates live

- **Blueprints (source of truth):** `Blueprints/*.blueprint`  
- **QuickAdd templates:** `Templates/*.md` — copies used only by QuickAdd. If you edit a blueprint, update the matching `Templates/*.md` so new notes stay in sync.
- **Agent scratchpad:** Open **[[Agent-Findings]]** to see recently updated investigations and reports; click through for agent questions, discoveries, new questions, data needed, and connections (see §8).

### Blueprint commands (no settings tab)

- **New note from blueprint** (e.g. folder right-click)  
- **Apply blueprint to note**  
- **Update all notes with blueprints** (in a folder)  

Search **blueprint** in Command Palette for exact names.

---

## 13. Integrating Agents (Claude, OpenClaw, Cursor)

Agents need to read/write the vault. Use **direct file I/O** (no Obsidian) for almost everything; use **Obsidian CLI** only for link-safe move/rename or search.

### Give agents the vault path

- **Env var (scripts / OpenClaw):**  
  - Windows: `$env:CYBEROPS_VAULT = "D:\0LOCAL\0-ObsidianTransferring\CyberOps"`  
  - macOS/Linux: `export CYBEROPS_VAULT="/path/to/CyberOps"`  
- **Cursor / Claude Code:** Open the vault folder as workspace (or pass the path in the prompt).

### What agents do (direct file I/O)

- **Create task:** Write a new `.md` in `00-Inbox/` matching `Templates/Task-Inbox.md`.  
- **Read context:** Read `01-Memories/agents/agent-logbook.md`, `01-Memories/human/corrections.md`, **01-Memories/shared** (research logs and handoff blocks: look for lines `Agent:` and `Handoff:` — see **[[04-QUICKADD-GLOBAL-VARS-HANDOFF]]**), the task file, and any `02-Skills/` or linked notes.  
- **Claim task:** Edit task frontmatter: `status: claimed`, `assignee: <agent-id>`.  
- **Write findings:** Create/update `.md` in `20-Entities/`, `30-Evidence/`, `10-Investigations/`, etc. with blueprint-style frontmatter.  
- **Complete task:** Set task `status: done`, `completed_date`, `result_summary`, `output_files`; append to `agent-history.md`; append to `agent-logbook.md` **only when** the learning applies to all agents in the swarm (rare); update **`03-Agents/agent.md`** with status, questions, ideas, pain points, scope/struggle if 3+ questions, first impressions, insights, recommended analyses, lessons, and suggested improvements (see **[[05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK#1.2a Agent write map: what agents put where (single group)]]** and **§1.2b Agent separation**; do not spread these across the vault).
- **State:** Update `03-Agents/active_agents.json` (heartbeat, assignments).

### Obsidian CLI (optional)

- **Built-in (Obsidian 1.12.4+):** Settings → General → Advanced → Command line interface. Requires Obsidian running. Use for `obsidian create`, `read`, `daily`, `search`, etc.  
- **obsidian-cli (yakitrak):** e.g. `brew install yakitrak/yakitrak/obsidian-cli`. `obsidian-cli set-default "CyberOps"`, then `create`, `move`, `search`/`search-content`. Use for link-safe renames.

### OpenClaw & agent_runner

- **OpenClaw (ZimaBoard):** Needs only vault path + direct file access. Watches `00-Inbox/`, updates `active_agents.json`. No Obsidian or CLI on ZimaBoard.  
- **agent_runner.sh (workstation):** Set `CYBEROPS_VAULT`; list `00-Inbox/*.md`, read task + **01-Memories** (agents, human, **shared** — include research logs and parse `Agent:` / `Handoff:` blocks for handoff context; see **[[04-QUICKADD-GLOBAL-VARS-HANDOFF]]**) + skills, run LLM, write outputs and task/agent state with direct file I/O. Use obsidian-cli move only if you need link-safe renames.

### Claude Code (Cursor, Claude CLI) and vault compatibility

Vault layout and the **handoff format** (`Agent:` / `Handoff:` in 01-Memories/shared) are designed so **Claude Code** agents, [subagents](https://code.claude.com/docs/en/sub-agents), [skills](https://code.claude.com/docs/en/skills), and [hooks](https://code.claude.com/docs/en/hooks#hooks-in-skills-and-agents) can share the same contract: **location** (01-Memories/shared) and **pattern** (two-line block). You can add a rule (CLAUDE.md / .claude/rules), a skill that injects handoff context, or a SessionStart/UserPromptSubmit hook that reads the vault and passes recent handoffs as `additionalContext`. Subagents and skills can define hooks in frontmatter; keep vault metadata (e.g. `type: daily`, `investigator`) and folder structure stable so those components can target the same paths. See **[[04-QUICKADD-GLOBAL-VARS-HANDOFF]]** for the full handoff flow and integration points.

### Cursor / Claude Code

- Open vault as workspace; read/write vault `.md` with your editor/agent tools. Keep frontmatter and structure aligned with blueprints so Dataview works.

---

## 14. Multi-Session Orchestration & Scaling

When running **multiple concurrent sessions** (e.g. Session A, B, C on different machines or agents), task dependencies are coordinated through **shared manifest files** rather than a central orchestrator. This design enables **zero orchestration overhead** — adding more sessions costs nothing.

### How it works

1. **Queue metadata declares dependencies:** Each task in the sprint queue includes `depends_on: [task-ids]`
2. **Agents write manifests:** When agent finishes task-1, it writes a manifest to `~/.claude/hooks/state/wave-X-agent-Y-task-1-result.json`
3. **Next agent polls manifests:** Agent working on task-5 (which depends_on task-1) polls the same shared directory until it finds the manifest
4. **Ready filtering:** `claim_batch()` only returns tasks where all dependencies have manifests

### Benefits

- **No central coordinator:** Sessions operate independently; no inter-session communication protocol
- **Infinite scaling:** Adding Session 10 costs the same as Session 2 (constant overhead per session)
- **Resilience:** If one session crashes, dependent tasks in other sessions still proceed (they just wait longer)
- **Atomic signaling:** Manifests are the single source of truth for task completion

### For detailed design, see:

→ **[[MULTI-SESSION-DAG-DESIGN.md]]** — Comprehensive architecture, execution flows, overhead analysis, and implementation checklist

---

## 15. Quick reference

- **Dashboards:** [[Investigation-Overview]] (overview + Quick Actions), [[Unprocessed-Stubs]], [[Hypothesis-Tracker]].  
- **Home / command center:** [[HOME]] for daily attention, threads, quick actions, and collaboration notes.  
- **Companion scripts:** `scripts/` in the vault root — [[scripts/README]] for agent_runner stubs and vault setup pointer.  
- **Multi-session orchestration:** [[MULTI-SESSION-DAG-DESIGN.md]] — How to scale to unlimited concurrent sessions with zero overhead
- **This doc:** Single source for architecture, setup (QuickAdd + Blueprints), and agent integration.
