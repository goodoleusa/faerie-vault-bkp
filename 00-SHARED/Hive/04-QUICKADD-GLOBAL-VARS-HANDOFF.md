---
type: meta
tags: [meta, quickadd, handoff, agents, how-to]
created: 2026-03-11
updated: 2026-03-11
doc_hash: sha256:cf10d2e1efb7a2fc304e9a42d2df1610606c3f6ec6697b72b6d729aa47ce2735
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---

# QuickAdd Global Variables for Agent Handoff

Focused guide: **maximize understanding and use of QuickAdd global variables** for async agent–human handoff. How the **HandoffBlock** works, where handoff content lives, and how **agents** (runner script, Claude Code, skills, hooks) discover and use it so the vault stays compatible with [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [hooks in skills and agents](https://code.claude.com/docs/en/hooks#hooks-in-skills-and-agents), and rules.

**See also:** [[02-QUICKADD-SETUP]] (full QuickAdd setup), [[01-ARCHITECTURE]] (§5 Communication, §7 Memory, §13 Integrating agents).

---

## 1. Why QuickAdd globals for handoff?

- **Single format:** Everyone (human, Cursor, Claude Code, agent_runner) uses the same handoff shape: `Agent: <who>` and `Handoff: <what>`. QuickAdd globals let you define that once and reuse it in templates and captures.
- **Consistent location:** Handoff content lives in **01-Memories/shared/** (research logs and any note you append to). Agents and hooks read that folder; no need to remember paths.
- **Expand before prompts:** Globals expand first, then QuickAdd runs `{{VALUE:agent}}` and `{{VALUE:handoff}}`, so one Capture choice can insert a full handoff block in one go.
- **Compatibility:** The resulting text in the vault is **plain, parseable markdown**. Runner scripts, Claude Code rules, skills, and hooks can all look for the same pattern without Obsidian or QuickAdd running.

---

## 2. Recommended globals (handoff-focused)

Set these in **Settings → QuickAdd → Global Variables**. They are not in the QuickAdd package; define once per vault.

| Name | Value | Use for handoff |
|------|--------|------------------|
| **ResearchFolder** | `01-Memories/shared` | Where research logs and handoff content live. Use in Template “Create in folder” or Capture target path. |
| **TodayDate** | `{{DATE:YYYY-MM-DD}}` | Date stamp in handoff or log heading. |
| **AgentName** | `{{VALUE:agent}}` | “Who is handing off?” — single prompt, reuse in file names or body. |
| **HandoffBlock** | `Agent: {{VALUE:agent}}\nHandoff: {{VALUE:handoff}}` | **Canonical handoff snippet.** Two lines; QuickAdd prompts for `agent` and `handoff`, then inserts. Use in a Capture that inserts at cursor or appends to a file in `01-Memories/shared`. |

Optional for broader use: **LeadSource**, **ThreatLevel**, **CaseIdPrefix**, **InboxFolder** (see [[02-QUICKADD-SETUP#1c. QuickAdd Global Variables (reusable snippets)]]).

---

## 3. How the HandoffBlock works (step-by-step)

### 3.1 What you configure

1. **Global variable (once)**  
   In QuickAdd → Global Variables, add:
   - **Name:** `HandoffBlock`  
   - **Value:** `Agent: {{VALUE:agent}}\nHandoff: {{VALUE:handoff}}`  
   (Use a real newline between the two lines if the UI allows; otherwise `\n` may be stored literally and rendered as newline when QuickAdd expands.)

2. **Capture choice (once)**  
   QuickAdd → Add choice → **Capture**.  
   - **Name:** e.g. `Insert handoff snippet`  
   - **Capture format:** `{{GLOBAL_VAR:HandoffBlock}}`  
   - **Where to capture:** “Insert at cursor” (or “Append to file” and choose a note in `01-Memories/shared`, e.g. today’s research log).

### 3.2 What happens when you run it

1. You run **Command Palette → QuickAdd → Insert handoff snippet** (or whatever you named it).
2. QuickAdd **expands** `{{GLOBAL_VAR:HandoffBlock}}` first → the value becomes `Agent: {{VALUE:agent}}\nHandoff: {{VALUE:handoff}}`.
3. QuickAdd then **prompts** for each `{{VALUE:...}}`: you get one prompt for `agent` and one for `handoff` (or a single one-page form if you enabled “One-page input for choices”).
4. Your answers replace the placeholders; QuickAdd **inserts** the resulting block into the current note (or appends to the target file).

**Result in the note:** Two lines of plain text, e.g.:

```text
Agent: researcher-claude
Handoff: Summary of today's OSINT run; three new entities in 20-Entities; open question on Source X in Case Alpha.
```

No special syntax — just a fixed **format** so that scripts and agents can find it reliably.

### 3.3 Where to put the handoff

- **In a research log:** Use the Capture with “Append to file” → pick a note in `01-Memories/shared` (e.g. `YYYY-MM-DD-Research-YourName.md`). Then the handoff lives in the same place agents already read for context.
- **In any note:** Use “Insert at cursor” when you want the block in the current note (e.g. an investigation’s “Context Snapshot” or “Agent questions” section). The note might be in `10-Investigations/` or `01-Memories/shared/`; agents can still parse the block if they read that file.

---

## 4. How the agent “knows” to look for it (runner, rule, skill, hook)

The handoff is **not** magic: nothing automatically routes it to an agent. The vault and format are a **contract** so that **you** (or your automation) can tell the agent where and what to read.

### 4.1 Contract: location + format

- **Location:** Handoff content is in **01-Memories/shared/** (and optionally in investigation notes under sections like “Context Snapshot” or “Agent questions (for reviewer)”).
- **Format:** A block of the form:
  - Line 1: `Agent: <identifier or name>`
  - Line 2: `Handoff: <free text>`
  (Optional: allow more lines after `Handoff:` as part of the same block.)

Any runner, rule, skill, or hook that needs “what was handed off” should read from that location and parse this pattern (e.g. grep for `Agent:` and `Handoff:`, or a simple line-by-line parser).

### 4.2 Integration points (who looks for it)

| Integration point | How it uses the handoff | Where it’s configured |
|--------------------|--------------------------|------------------------|
| **agent_runner script** (workstation) | When building context for a task, read **`00-SHARED/Memories/shared`** (e.g. latest research logs) and optionally grep for `Agent:` / `Handoff:` blocks; inject that text into the prompt or context file sent to Claude/LLM. | In the script: add a step that reads `$VAULT/00-SHARED/Memories/shared/*.md` (or a subset) and extracts handoff blocks before calling the LLM. See [[01-ARCHITECTURE#13. Integrating Agents]] and [[scripts/README]]. |
| **CLAUDE.md / .claude/rules** (vault or repo) | Instruct the agent: “When working in this vault, read 01-Memories/shared for recent handoffs. Look for lines starting with `Agent:` and `Handoff:`; treat that as context from the previous session or human.” | In the vault root or parent repo: `CLAUDE.md` or `.claude/rules/*.md` with that instruction. |
| **Skill** (Claude Code / Cursor) | A skill that loads “recent handoff context” from the vault: read 01-Memories/shared, parse `Agent:` / `Handoff:` blocks, return them as a string for the agent. The skill is invoked or preloaded so the agent sees handoffs in context. | Skill frontmatter and body (e.g. “Read vault path from env; list 01-Memories/shared; extract handoff blocks”). Skills can also define [hooks](https://code.claude.com/docs/en/hooks#hooks-in-skills-and-agents) scoped to that skill. |
| **SessionStart / UserPromptSubmit hook** | A hook that runs when a session starts (or when you submit a prompt): read the vault’s `01-Memories/shared`, find recent `Agent:` / `Handoff:` blocks, and return them as `additionalContext` (or in the hook output). Claude then sees handoffs at session start or before each prompt. | Claude Code settings: `hooks.SessionStart` or `hooks.UserPromptSubmit` with a command that reads the vault path (e.g. from `CYBEROPS_VAULT`) and outputs context. See [Hooks reference](https://code.claude.com/docs/en/hooks). |

So: **the agent knows to look for it** because you configure one (or more) of: the runner script, a rule (CLAUDE.md), a skill, or a hook to read `01-Memories/shared` and parse the `Agent:` / `Handoff:` format. The QuickAdd HandoffBlock only **writes** that format into the vault; it doesn’t notify the agent by itself.

---

## 5. Vault metadata and Claude Code (subagents, skills, hooks, rules)

The vault is structured so that **Claude Code** (and Cursor) can use the same paths and formats for agents, subagents, skills, and hooks.

### 5.1 Frontmatter and folders

- **`type: daily`** and **`investigator`** in research logs (01-Memories/shared) mark “who / when” for Dataview and for any skill or hook that filters by type.
- **01-Memories/** layout: `human/`, `agents/`, `shared/` — so a rule or skill can say “load memories from `01-Memories/agents` and `01-Memories/shared`; treat `shared` as handoff + research log.”
- **Handoff format** is plain text (`Agent:` / `Handoff:`), so no Obsidian-specific features are required; any script or hook that can read files can parse it.

### 5.2 Aligning with Claude Code docs

- **Subagents** ([Create custom subagents](https://code.claude.com/docs/en/sub-agents)): A subagent can have a **skill** or **description** that says “when working on the CyberOps vault, read 01-Memories/shared and parse Agent:/Handoff: blocks for context.” Subagents can also define **hooks** in frontmatter (e.g. `PreToolUse`) scoped to that agent.
- **Hooks in skills and agents** ([Hooks reference](https://code.claude.com/docs/en/hooks#hooks-in-skills-and-agents)): Hooks defined in a skill or agent’s frontmatter run only while that component is active. For example, a “vault handoff” skill could expose a **SessionStart** or **UserPromptSubmit** hook that injects recent handoffs from `01-Memories/shared` as `additionalContext`, so every time you start a session or send a prompt, Claude sees the latest handoff without you pasting it.
- **Rules**: `.claude/rules/*.md` or project CLAUDE.md can state: “Vault path is in CYBEROPS_VAULT; before running tasks, read 01-Memories/shared and any line pair `Agent:` / `Handoff:` as handoff context.”

By keeping **location** (01-Memories/shared) and **format** (Agent: / Handoff:) fixed, you can add or change the integration point (runner, rule, skill, hook) without changing how humans or QuickAdd write handoffs.

---

## 6. Summary

| Topic | Detail |
|-------|--------|
| **What** | QuickAdd global `HandoffBlock` = `Agent: {{VALUE:agent}}\nHandoff: {{VALUE:handoff}}`. A Capture using it inserts a two-line block into a note. |
| **Where** | Prefer **01-Memories/shared** (e.g. research log or a dedicated handoff note) so all agents and hooks read the same folder. |
| **How agent sees it** | Configure **agent_runner**, a **CLAUDE.md/rule**, a **skill**, or a **SessionStart/UserPromptSubmit hook** to read that folder and parse lines starting with `Agent:` and `Handoff:`. |
| **Claude Code** | Vault layout and handoff format are designed to work with [subagents](https://code.claude.com/docs/en/sub-agents) and [hooks in skills and agents](https://code.claude.com/docs/en/hooks#hooks-in-skills-and-agents); use rules/skills/hooks to inject handoff context into the session. |

For full QuickAdd setup (templates, macros, other globals), see [[02-QUICKADD-SETUP]]. For architecture and agent integration, see [[01-ARCHITECTURE]].
