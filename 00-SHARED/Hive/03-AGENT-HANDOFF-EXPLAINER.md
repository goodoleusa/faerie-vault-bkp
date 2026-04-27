---
type: meta
tags: [meta, handoff, agents, flow, quickadd, improvement]
created: 2026-03-11
updated: 2026-03-11
doc_hash: sha256:575d8de8bbbbe0e3d9042c9ca7db981bdc23d32afd6e94494fec38b4ba9fff95
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---

# Agent handoff explainer

How **QuickAdd global variables** actuate agent handoff, the **flow of requests and hops** through the system, **iterative improvement** (including self-healing and agent feedback), and how the **air-gapped workstation agent** keeps you updated by editing its own **agent.md** in the vault (while the real agent process and config stay protected on the workstation).

**See also:** [[01-ARCHITECTURE]] (canonical topology), [[04-QUICKADD-GLOBAL-VARS-HANDOFF]] (globals reference), [[02-QUICKADD-SETUP]] (QuickAdd setup).

---

## 1. How QuickAdd globals actuate the handoff

### 1.1 Chain: Global → Capture → Vault

1. **You define a global** in QuickAdd (e.g. `HandoffBlock` = `Agent: {{VALUE:agent}}\nHandoff: {{VALUE:handoff}}`). Globals expand **before** other tokens, so the value can contain prompts.
2. **You run a Capture choice** whose format is `{{GLOBAL_VAR:HandoffBlock}}`. QuickAdd expands the global, then prompts for `agent` and `handoff`, then inserts the result into a note (cursor or append to file).
3. **The note lives in the vault** — usually in **01-Memories/shared** (e.g. research log or a dedicated handoff note). Syncthing (and the rest of the mesh) syncs that file to ZimaBoard and to the workstation.
4. **Agents don’t get “notified”** — they discover handoffs by **reading** that location and **parsing** the format (`Agent:` / `Handoff:`). The runner script, a rule, a skill, or a hook is configured to do that read+parse and inject the result into context.

So: **QuickAdd globals actuate handoff** by giving you a single, repeatable way to **write** the canonical handoff block into the vault; the **actuation** is “human runs QuickAdd → text appears in vault → next agent read sees it.”

### 1.2 Why this helps

- **One format everywhere**: Runner, Cursor, Claude Code, and hooks all look for the same two-line block. No custom APIs; just file I/O and a simple parse.
- **Location fixed**: `01-Memories/shared` (and optionally “Context Snapshot” / “Agent questions” in investigations). Agents that work on the vault can rely on that contract (see [[04-QUICKADD-GLOBAL-VARS-HANDOFF]]).

---

## 2. Flow of requests and hops through the system

### 2.1 Request flow (high level)

```
YOU (laptop)                    ZIMABOARD + WORKSTATION (same ZeroTier/P2P)
     │
     │  1. You create a task (or handoff) in the vault.
     │     QuickAdd / Obsidian writes to 00-Inbox or 01-Memories/shared.
     │
     │  2. Syncthing syncs vault to ZimaBoard (and/or direct to workstation
     │     if in same mesh).
     │
     │  3. On the workstation: poll script runs, sees new or updated files
     │     in local vault (e.g. 00-Inbox task, or 01-Memories/shared handoff).
     │
     │  4. agent_runner: sanitize task → claim task → build context
     │     (01-Memories/agents, human/corrections, shared handoffs, 02-Skills)
     │     → run LLM → write results to vault (20–80, agent-logbook, etc.).
     │
     │  5. Workstation agent may also update 03-Agents/agent.md (see §4).
     │
     │  6. Syncthing propagates workstation changes back. You see results
     │     (and agent.md) on the laptop.
```

### 2.2 Hops in more detail

| Hop | From | To | What moves |
|-----|------|----|------------|
| 1 | You | Laptop vault | New/updated .md (task, handoff, or edit). |
| 2 | Laptop vault | ZimaBoard vault | Syncthing (P2P / ZeroTier). |
| 3 | ZimaBoard vault | Workstation vault | Syncthing (same private net). |
| 4 | Workstation poll script | agent_runner | “New task” or “updated shared” (file paths / content). |
| 5 | agent_runner | LLM | Sanitized task + context (memories, handoffs, skills). |
| 6 | LLM | agent_runner | Completion (findings, summaries, decisions). |
| 7 | agent_runner | Workstation vault | Updated/created .md (tasks, 01-Memories/agents, 03-Agents/agent.md, 10–80). |
| 8 | Workstation vault | ZimaBoard / laptop | Syncthing. |

Handoff content enters at **hop 1** (you run QuickAdd → write to 01-Memories/shared). It is read in **hop 4/5** when the runner builds context. So the “handoff” is just **data in the vault** that crosses the same hops as everything else.

### 2.3 Diagram (oriented for agent feedback)

The same flow can be drawn so agents working on the vault see where they can **read** and **write**:

```
                    ┌──────────────────────────────────────────────────┐
                    │  VAULT (syncs: laptop ↔ ZimaBoard ↔ workstation) │
                    │  00-Inbox     ← tasks from human (and agents)     │
                    │  01-Memories/shared ← handoffs, research logs     │
                    │  01-Memories/agents ← agent logbook, lessons      │
                    │  03-Agents/agent.md ← workstation agent status   │
                    │  10–80        ← findings, entities, evidence      │
                    └──────────────────────────────────────────────────┘
                         ▲ read (context)    ▲ write (results, status)
                         │                    │
                    ┌────┴────────────────────┴────┐
                    │  WORKSTATION (air-gapped)     │
                    │  poll → sanitize → claim →   │
                    │  LLM (context + task) →      │
                    │  write vault + agent.md      │
                    └─────────────────────────────┘
```

Agents that edit the vault (Cursor, Claude Code, or the workstation agent) can **offer feedback** by writing to `01-Memories/agents/` or to a dedicated “suggestions” note; the diagram keeps **one** vault and makes the read/write boundaries explicit so improvements (e.g. rule changes, doc fixes) can be proposed in the vault and applied by you or the next run.

---

## 3. Iterative improvement and self-healing

### 3.1 How agents can improve the flow

- **Propose changes in the vault**: The workstation agent (or a Cursor/Claude Code agent) writes **suggestions** into the vault instead of executing them directly — e.g. a note in `01-Memories/agents/` or `03-Agents/` like “Suggested improvement: add X to sanitization” or “Recommend updating [[02-QUICKADD-SETUP]] section Y because…”. You (or a later agent with permission) apply them.
- **Self-healing within the run**: The agent can **fix** vault content it’s allowed to write — e.g. normalize frontmatter, fix broken links, or append to agent-logbook with “Lesson learned: do Z next time.” That doesn’t change code or runner config unless you expose that via a controlled path (e.g. “write suggested rule to `02-Skills/suggested-rule.md` for human review”).
- **Feedback loop**: If the agent reads `01-Memories/human/corrections.md` and `01-Memories/agents/agent-logbook.md` (and optionally `03-Agents/agent.md`), it can align its next run with past corrections and lessons. So “memories and lessons” are updated **by the agent** in the vault; the **canonical** agent process and config stay on the workstation (see §4).

### 3.2 Making the diagram useful for agent feedback

- **Single source of truth**: The diagram in §2.3 shows one vault and one direction of data (vault ↔ workstation). Agents can be instructed: “You may only read/write the paths shown; suggest changes to docs or rules by creating/editing notes in 01-Memories/agents or 03-Agents, not by editing runner scripts or protected config.”
- **Explicit “suggestions” path**: You can add a convention: e.g. `03-Agents/suggestions.md` or `01-Memories/agents/improvement-ideas.md` where the agent appends proposed doc/rule/sanitization changes. You review and apply; optionally a **human-approved** script could apply a subset (e.g. “append to QUICKADD doc”) to keep the loop tight.

---

## 4. Canonical agent on air-gap workstation: keeping you updated via the vault

### 4.1 The split

- **Canonical agent** = the process and config that run on the **air-gapped workstation** (agent_runner, Claude CLI, prompts, env). That stays **protected** — no direct access from the laptop or ZimaBoard.
- **Vault-facing “agent” presence** = what the workstation agent **writes into the vault** so you can see status, lessons, and next steps without touching the workstation. That’s the **only** place the workstation agent can “speak” to you asynchronously.

### 4.2 agent.md (or equivalent) in the vault

- **Location**: e.g. **`03-Agents/agent.md`** (or `agent-status.md`). In the vault structure, `03-Agents/` already holds `agent-history.md`, `active_agents.json`, `agent-logs/`. Adding **agent.md** gives a single, human-readable note that the workstation agent **updates** after each run (or when it has something to report).
- **Content** (agent-written): Short status, last run time, tasks completed, **lessons learned** (what to do differently next time), **open questions** for you, and optionally **suggested improvements** (e.g. “Consider adding X to sanitization” or “Handoff format in file Y was unparseable; suggest Z”). So the agent keeps **memories and lessons** updated **in the vault** by editing this file; it does **not** need to change the real agent config or memory cache on the workstation — the vault **is** the shared memory surface you and the agent both see.
- **Real agent config / memory on workstation**: The actual prompts, .claude/rules, or local “memory” cache stay on the workstation. The agent can **optionally** read from the vault at the start of each run (including `03-Agents/agent.md` and `01-Memories/agents/agent-logbook.md`) and use that as **context** for the run; then it **writes back** to the vault (including updating `agent.md`). So the “canonical” agent lives on the air-gap box, but the **durable, sync’d record** of what it did and what it learned lives in the vault.

### 4.3 Summary

| Where | What | Who updates |
|-------|------|-------------|
| Workstation (protected) | agent_runner, LLM, real config/memory | You (via secure access) or deploy pipeline |
| Vault `03-Agents/agent.md` | Status, lessons, suggestions, open questions | Workstation agent (writes each run) |
| Vault `01-Memories/agents/` | agent-logbook.md, patterns, improvement ideas | Workstation agent |
| Vault `01-Memories/shared` | Handoffs, research logs | You (QuickAdd) and optionally agents |

So: **agents keep memories and lessons updated** by editing **their own** agent-facing note (`agent.md`) and the agents memory folder in the vault; the **real** agent lives on the air-gap workstation and stays protected, while the vault copy is the **mirror** that keeps you updated and gives you a single place to read status and apply suggested improvements.

---

## 5. Quick reference

- **Handoff actuation**: QuickAdd `HandoffBlock` → Capture → text in `01-Memories/shared` → agents read and parse.
- **Request flow**: Laptop → Syncthing → ZimaBoard → Syncthing → workstation → poll → sanitize → claim → LLM → write vault (+ agent.md) → sync back.
- **Improvement**: Agents propose changes by writing to the vault (e.g. `01-Memories/agents/`, `03-Agents/suggestions.md`); you or an approved process apply. Diagram is optimized so agents know where they can read/write.
- **Agent ↔ you**: Workstation agent writes **agent.md** (and agents memory) in the vault; real agent and config stay on the workstation.

For globals and integration points, see [[04-QUICKADD-GLOBAL-VARS-HANDOFF]]. For full architecture, see [[01-ARCHITECTURE]].
