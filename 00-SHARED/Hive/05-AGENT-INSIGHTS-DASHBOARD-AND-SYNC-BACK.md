---
type: meta
tags:
  - meta
  - agents
  - dashboard
  - sync
  - security
created: 2026-03-11
updated: 2026-03-11
doc_hash: sha256:dc713142be4491ac6c33ac8dc9e6b40fac6877cb32b8768952193be5975011aa
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---

# Agent insights dashboard vs agent.md — and safe sync-back to air-gap

How to get a **single dashboard feed of agent insights from the last 24 hours** while keeping **agent.md** as the one-stop shop for humans, how **raw vs approved** works so only human-approved content drives agent behavior, and how the agent can **safely take the Obsidian version back** to the air-gapped environment — including a **security sanitizer** on the workstation and a **human-approved** path for process improvements.

**See also:** [[03-AGENT-HANDOFF-EXPLAINER]] (handoff and agent.md role), [[01-ARCHITECTURE]] (topology, task sanitization, raw vs approved).

---

## 1. Balancing dashboard feed and agent.md

### 1.1 Goal

- **You want:** One place (dashboard) to see all agent insights, updates, and questions from the last 24 hours.
- **You also want:** Those same insights and updates (and open questions) **recorded in agent.md** so agent.md is the **one-stop shop** for humans and the dashboard is a view over it. **All process improvements** (rules, doc changes) that change how agents behave **must be approved by you** and promoted to **approved** locations; raw AI output is for review only.

So: **agent.md = one-stop shop**; **dashboard** = view over agent.md + logbook + history; **raw** outputs need human approval before they become **approved** and are used by agents in the vault moving forward.

### 1.2 Single source: agent.md structure

Keep **one** agent-facing note the workstation agent owns: **`03-Agents/agent.md`**. Structure it so it doubles as both “status for the human” and “feed-friendly”:

| Section | Purpose | Who updates |
|--------|---------|--------------|
| **Last run** | When, what tasks, one-line summary | Agent (each run) |
| **Last 24h — insights & updates** | Bullet list of insights, findings, status updates (append-only; trim to last 24h or N entries) | Agent (each run) |
| **Open questions for human** | Questions that need answer or triage | Agent (each run); you answer in Obsidian |
| **Ideas** | Process, product, or doc ideas (not yet formal suggested improvements) | Agent (each run) |
| **Pain points** | What's hard, blockers, what failed; **if 3+ open questions** add "Scope too broad? Consider refining subagent or splitting task." | Agent (each run) |
| **Scope or struggle** | Optional; use when scope may be too broad so humans can refine subagent or split task | Agent (each run) |
| **First impressions (data)** | Initial take on data as it lands | Agent (each run) |
| **Insights (in progress)** | Findings as data is processed | Agent (each run) |
| **Recommended analyses** | Specific datasets + which analyses to run (e.g. "Run significance test on set X") | Agent (each run) |
| **Lessons learned (this session)** | What to do differently next time | Agent (each run) |
| **Suggested improvements** | Doc/rule/sanitization ideas for you to apply (human promotes to approved) | Agent (each run) |

**Raw vs approved:** Agent.md (and 01-Memories/agents/) is **raw** AI output — useful for your awareness and the dashboard, but **not** applied by the agent as behavior-changing rules until you promote it. You review in agent.md; when you approve an improvement, you copy or promote it to an **approved** location (e.g. `03-Agents/suggestions-approved.md`) and optionally run a human-approved script to apply it to the real config. Agents read only **approved** content for rules and process improvements. See §3 and [[01-ARCHITECTURE#7.1 Raw vs approved (approval model)]].

### 1.2a Agent write map: what agents put where (single group)

**Rule for agents:** All of the following go in **one place** — **`03-Agents/agent.md`** — in the sections below. Do **not** spread questions, ideas, pain points, first impressions, insights, or recommended analyses across the vault (e.g. into investigation scratchpad sections or separate notes). Keeping them in agent.md makes agent.md the one-stop shop for humans and avoids losing or duplicating context.

| Put this | In agent.md section | Do not put it |
|----------|----------------------|----------------|
| Questions that need human answer or triage | **Open questions for human** | In investigation "Agent questions" or scattered in other notes |
| Ideas (process, product, doc ideas) | **Ideas** | In 01-Memories/agents/ or ad-hoc notes |
| Pain points (what's hard, blockers, what failed) | **Pain points** | In task body only or scattered |
| **If 3+ open questions:** "Scope too broad? Consider refining subagent or splitting task." | **Pain points** or **Scope or struggle** | So humans know to refine the subagent; do not leave unreported |
| First impressions of data as it lands | **First impressions (data)** | Only in investigation scratchpad |
| Insights as data is processed | **Insights (in progress)** | Only in logbook or investigation |
| Recommended analyses to run on specific sets | **Recommended analyses** | In task body only or 02-Skills without human review |
| Status, tasks completed, one-line summary | **Last run** | — |
| Bullet list of recent insights/updates | **Last 24h — insights & updates** | — |
| What to do differently (this session or this agent) | **Lessons learned (this session)** | In agent.md. Logbook only if applies to ALL agents (rare). |
| Doc/rule/sanitization ideas to apply | **Suggested improvements** | In runner config or 02-Skills without human approval |

**Logbook = swarm-wide only (rare).** Use **`01-Memories/agents/agent-logbook.md`** only for learnings that apply to **every agent in the swarm** (e.g. handoff format, vault-wide conventions). Agent-specific or session-specific learnings go in **agent.md** "Lessons learned" or in the **task file** (Agent Execution Log, Agent Learnings). Everything else in the table above goes **only in agent.md** so humans have one place to look and nothing is spread across the vault.

### 1.2b Agent separation: few questions, scope too broad

**Agents should be as separate as possible.** Only **extremely important** questions go to the orchestrator or human. The point of subagents is to **reduce back-and-forth**; if an agent has **too many open questions**, that signals the **task or subagent scope is too broad** and should be refined or split.

**Mechanism — scope-too-broad signal:** When you have **3 or more open questions** (or are blocked on multiple decisions), you **must** add to **Pain points** or **Suggested improvements** in agent.md:

- **Scope too broad?** This task/subagent may need refinement or splitting. Consider narrowing scope or defining a smaller handoff so the next agent can execute without more questions.

That way **humans see** that the subagent is struggling and can refine the subagent definition, split the task, or narrow the handoff. Optionally the orchestrator or runner can surface "agent reported scope too broad" on the dashboard. See [[09-HUMAN-PROMOTES-AI-EXECUTES]] and agent.md section **Pain points** / **Scope or struggle**.

### 1.2c Agent language for human decisions (fast approvals)

**Theme:** [[09-HUMAN-PROMOTES-AI-EXECUTES]] — **Human promotes, AI executes.** Agents stop at intervention points; humans promote so the agent can continue.

When the agent needs a human decision (open questions, suggested improvements, or any "should I do X or Y?"), use **concise, scannable language** so reviewers can run through many approvals quickly:

- **Format:** `**Decision needed:** [One line: what must be decided]. **Options:** A) [short] B) [short] C) [short] (or: Approve / Reject / Defer).`
- **Example:** `**Decision needed:** Should entity confidence stay low until second agent validates? **Options:** A) Yes, keep rule B) No, allow single-agent promote when source is high quality C) Defer to human per case.`
- Keep each decision to one or two lines. Put the decision first, options second. No long paragraphs before the ask.

Sections that require human intervention before the agent can continue: **Open questions for human**, **Suggested improvements** (promote to approved), and any task with **Review verdict: pending**. The dashboard labels these as **Human intervention required** (see [[Agent-Insights]]). to “Last 24h — insights & updates” each run (and optionally trims to keep only the last 24 hours or last 20 items). So:

- **All agent insights and updates** are in agent.md (no duplication of “what the agent said”).
- **Open questions** are in agent.md so you can answer them there; the agent reads them back on the next run.
- The **dashboard** can show “last 24h” by either (a) embedding or transcluding that section of agent.md, or (b) using a Dataview query over a dedicated feed file. Preferred: **one note (agent.md)** with a clear “Last 24h” section so the dashboard just surfaces that section plus other tables (logbook, history).

### 1.3 Dashboard = view over agent.md + logbook + history

The **Agent Insights** (or “Last 24h agent”) dashboard should **aggregate**, not replace:

1. **From agent.md:** “Last 24h — insights & updates” and “Open questions for human” (and optionally “Suggested improvements”).
2. **From 01-Memories/agents/agent-logbook.md:** Logbook entries from the last 24 hours (by date in the note).
3. **From 03-Agents/agent-history.md:** Task completions in the last 24 hours.
4. **Tasks:** Recent tasks with `status: done` (Dataview), with **review_verdict** so the dashboard can list "Needs review" vs "Approved — ready to promote."

So: **insights and updates and questions live in agent.md**; the dashboard **pulls** from agent.md, agent-logbook, and agent-history to give you a single “last 24h feed” without duplicating content. Implementation: use **Dataview** for task/completion list; use **transclude** or a clear heading in agent.md for the “Last 24h” and “Open questions” sections so one pane shows the feed. See **[[Agent-Insights]]** for the concrete dashboard and the **validate-and-promote** workflow (review each task, set verdict, move approved tasks to 99-Archives).

### 1.4 Optional: append-only feed file

If you prefer not to keep a long “Last 24h” section inside agent.md, you can add an **append-only feed file** (e.g. `03-Agents/agent-feed.md`) with a fixed format, e.g.:

```text
### 2026-03-11 14:30 — insight
Handoff format parsed successfully; validation task completed.
### 2026-03-11 14:30 — question
Should low-confidence entities be auto-flagged for human review?
```

The agent **appends** to this file each run; agent.md then has a short “Last 24h summary” and “Open questions” only, and points to “See agent-feed.md for full timeline.” The dashboard would query or transclude agent-feed.md for the last 24h. Trade-off: one more file and one more place the agent writes; in return, agent.md stays short and the feed is easy to parse by date. For most setups, **sticking with a “Last 24h” section inside agent.md** is enough and keeps a single source of truth.

---

## 2. Sync-back: Obsidian version → air-gapped workstation

### 2.1 Direction of sync

- **Outbound (already in place):** Workstation agent writes vault (including agent.md) → Syncthing → ZimaBoard / laptop. You see the latest agent status in Obsidian.
- **Inbound (sync-back):** You (or a process) edit **agent.md** (and optionally `01-Memories/human/corrections.md`, `03-Agents/suggestions.md`) in Obsidian on the laptop. Syncthing syncs those files **to** the workstation. So the “Obsidian version” of agent.md (with your answers to open questions, or your notes) **is** the version that lands on the workstation.

No extra “export” step: **Syncthing is the carrier**. The vault folder on the workstation is the same as the one the agent reads and writes; when the laptop has a newer agent.md, Syncthing propagates it to the workstation vault.

### 2.2 What the agent “takes back”

On the next run, the workstation agent (agent_runner) already:

- Reads `03-Agents/agent.md` as part of context.
- Reads `01-Memories/human/corrections.md` and optionally `01-Memories/agents/agent-logbook.md`.

So by default the agent **already** “takes back” the Obsidian version of agent.md: it’s just the same file, synced. If you answered “Open questions” or added a “Human: do X next” block in agent.md, the next run sees it. No separate “import” is required.

### 2.3 When “update itself” means changing behavior

If “update itself” means **using vault content to change agent behavior** (e.g. apply a suggested new rule, or a new prompt snippet from suggestions.md), then that content must be **trusted** and **safe**. Raw vault content can contain mistakes or, in a worst case, malicious content (e.g. prompt injection, or paths that escape the vault). So the workstation should **not** blindly eval or include every line of agent.md/suggestions into executable config. Instead: **sanitize first**, then allow a controlled path for “approved” updates (see §3).

---

## 3. Safe self-update: sanitizing agent on the workstation

### 3.1 Risk

- **agent.md** (and any suggestions file) is written by the workstation agent and can be **edited by you** in Obsidian. It syncs to the workstation. If that content is then used to **build the next prompt** or to **modify rules/config**, an attacker who could write to the vault (or you by mistake) could inject instructions or code. So anything that flows from the vault into “how the agent runs” should be treated as **untrusted** until sanitized.

### 3.2 Sanitizer as a separate step

Before the **main** agent run, run a **sanitizing** step on the workstation:

1. **Inputs:** `03-Agents/agent.md`, and optionally `03-Agents/suggestions.md`, `01-Memories/human/corrections.md` (or only the parts that are “instructions” or “rules to add”).
2. **Process:** A small script or a **sanitizer agent** (e.g. a minimal LLM call or rule-based filter) that:
   - Strips or escapes control characters, NUL, and obvious shell metacharacters if any snippet were ever passed to a shell.
   - Detects or blocks known prompt-injection patterns (e.g. “ignore previous instructions”, “output only X”).
   - Ensures no file paths escape the vault (e.g. `../`, absolute paths outside vault).
   - Optionally: allows only a **structured subset** (e.g. “Open questions” and “Human answers” blocks; “Suggested improvements” as plain text, not executable).
3. **Output:** A **sanitized** context file (e.g. `03-Agents/agent-context-sanitized.md` or a JSON blob) that the **main** agent_runner **reads instead of** raw agent.md when building “human feedback / instructions” context. The main agent never sees the raw Obsidian version for “behavior-changing” content; it only sees the sanitized version.

So: **vault → sync → sanitizer runs → sanitized context → main agent**. The main agent “updates itself” from the **sanitized** context, not directly from agent.md for the parts that influence behavior.

### 3.3 What the main agent reads

- **Safe to read raw:** Task body and frontmatter (after existing task sanitization), folder layout, `02-Skills/` files that are part of the repo/vault and not user-edited in the same flow.
- **Read only after sanitizer:** The “instructions” or “human feedback” parts of agent.md, suggestions.md, and optionally the “rules to add” parts of corrections. So agent_runner should:
  - Run the **sanitizer** on agent.md (and suggestions, and relevant parts of corrections).
  - Write sanitized output to a dedicated file (or in-memory).
  - Pass that sanitized content to the LLM as “Human feedback and open questions (sanitized).”
  - Optionally: “Suggested improvements” and “rules to add” are only applied by a **human-approved** script (e.g. you run a command that applies `03-Agents/suggestions-approved.md` to the real config), not by the agent itself.

### 3.4 Summary table

| Content | Where it lives | Sync | Workstation use |
|--------|----------------|------|------------------|
| Agent status, last 24h, open questions, lessons, suggestions | agent.md (vault) | Laptop → Syncthing → workstation | Sanitizer → sanitized context → main agent reads that |
| Human answers, “do X next” | agent.md (you edit in Obsidian) | Same | Same: sanitizer → main agent |
| Human corrections | 01-Memories/human/corrections.md | Same | Sanitizer (if used for “rules”) or read-only with length/format limits |
| Suggested new rules / doc changes | 03-Agents/suggestions.md or agent.md section | Same | Sanitizer → optional “approved” path; main agent does not apply directly to runner config |

So the agent **does** take its “Obsidian version” back via Syncthing; the **safe** part is that the workstation **never** uses that version directly to change behavior — it uses a **security-sanitized** derivative for context and, for rules, only **approved** content via a human-approved script.

---

## 4. Quick reference

- **Dashboard vs agent.md:** agent.md is the single source; dashboard aggregates “Last 24h” from agent.md + agent-logbook + agent-history (see [[Agent-Insights]]).
- **Sync-back:** You edit agent.md (and related files) in Obsidian; Syncthing syncs to the workstation. No extra export; the vault is the carrier.
- **Safe self-update:** On the workstation, run a **sanitizer** on agent.md (and suggestions/corrections) before the main run; main agent reads **sanitized** context only for “human feedback / instructions.” Optional: apply suggested rules only via a human-approved script, not by the agent.

For handoff and agent.md’s role in the flow, see [[03-AGENT-HANDOFF-EXPLAINER]]. For task and content sanitization, see [[01-ARCHITECTURE]].
