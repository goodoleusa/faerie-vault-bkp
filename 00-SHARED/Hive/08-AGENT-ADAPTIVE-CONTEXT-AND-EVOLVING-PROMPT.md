---
type: meta
tags:
  - meta
  - agents
  - memory
  - adaptation
  - prompts
created: 2026-03-11
updated: 2026-03-11
parent: []
child: []
sibling: []
memory_lane: nectar
promotion_state: raw
doc_hash: sha256:58b6c29104e6646b927479028accad613accaa6ed9c86e0eb281cea40f52f714
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:17Z
hash_method: body-sha256-v1
---

# What to collect from the day's tasks — and an evolving, crystallized prompt

Which information from the day's tasks is **most effective** at making the workstation agent more adaptive and skilled on the next run, and how to turn it into a **continuously crystallized, evolving prompt** the agent reads at run start.

**See also:** [[05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK]] (agent.md, dashboard, sync-back), [[03-AGENT-HANDOFF-EXPLAINER]] (handoff, agent.md), [[01-Memories/human/corrections]] (corrections log).

---

## 1. Highest-value info to collect (in order of impact)

These are the signals that most directly improve the **next** run when the agent reads them as context.

| Priority | What to collect | Where it comes from | Why it helps |
|----------|-----------------|---------------------|--------------|
| **1** | **Human corrections** | [[01-Memories/human/corrections]] — "Agent claimed X / Correction: Y / Evidence / Impact" | Directly changes behavior: agent stops doing X and does Y. Highest signal. |
| **2** | **Review verdict + feedback** | Task Review section: Verdict (approved / needs-revision), **Feedback** text | Teaches what "good" looks like and what to avoid. Needs-revision + feedback = concrete "do less of this." |
| **3** | **What worked (approved patterns)** | Tasks with verdict **approved** + short note on *why* (e.g. "handoff was parseable", "entity linked to investigation") | Reinforces successful patterns so the agent repeats them. |
| **4** | **Open questions you answered** | agent.md "Open questions for human" → your answers | Aligns agent with your preferences and decisions (e.g. "always use low confidence until validated"). |
| **5** | **Edge cases and failures** | Tasks that got needs-revision, or tasks where the agent asked for clarification | "When you see X, do Y" or "Don't do Z in situation W" — adapts to similar cases next time. |
| **6** | **Distilled lessons (agent's own)** | agent.md "Lessons learned" + logbook "Implications" | Agent's own summary of what to do differently; most useful when phrased as **rules** ("Always …", "When … then …", "Never …"). |
| **7** | **Suggested improvements (human-approved)** | Suggestions the human has approved and that are safe to inject as context | Doc/rule ideas you've vetted; agent can follow them without changing code. |

**Low value for adaptation:** Raw execution logs, full task bodies, long narrative. Those are for audit and dashboard; for **behavior change**, use **short, actionable bullets** and **corrections + verdict feedback**.

---

## 2. From "daily feed" to "evolving prompt"

You already have:

- **agent.md** — status, last 24h, lessons, open questions, suggestions  
- **corrections.md** — human corrections  
- **agent-logbook.md** — learnings that apply to **all agents in the swarm only** (rare); session- or agent-specific learnings go in agent.md or task file  
- **Task Review** — verdict + feedback

To make the agent **more adaptive**, turn the **best of the above** into a single, **bounded block** the agent reads at **every** run: an **evolving context** that is **crystallized** so it doesn’t grow without limit.

### 2.1 Idea: one "agent context" block that evolves

- **Location:** e.g. **`03-Agents/agent-context-evolving.md`** (or a section at the top of a single "system extension" note).  
- **Content:** Short, bullet-form **rules and reminders** derived from:
  - Recent **corrections** (formatted as "Do: … / Don't: …")
  - **Approved** task feedback (one line per pattern to keep)
  - **Needs-revision** feedback (one line per thing to avoid)
  - **Answered open questions** (one line per preference)
  - **Lessons / implications** from agent.md and logbook, rewritten as rules

- **Update rule:** After each run (or once per day), a **crystallization step** merges the latest corrections, verdicts, answers, and lessons into this block and **trims** so the block stays under a **token or line budget** (e.g. 50 lines or ~500 tokens). Old, superseded items drop off; only the most recent and high-signal rules remain.

So the "prompt that continuously gets crystallized and evolves" is **literally this file**: the agent always reads `agent-context-evolving.md` at run start as **"Your evolving context (adapt from this): …"**. It changes over time; size stays bounded.

---

## 3. What the crystallization step does

- **Inputs (each run or daily):**
  - New entries in **corrections.md** → convert to "Don't: [old]. Do: [new]."
  - Tasks with **review_verdict: approved** and non-empty **Feedback** → one bullet: "Keep doing: [feedback]."
  - Tasks with **review_verdict: needs-revision** and **Feedback** → one bullet: "Avoid / fix: [feedback]."
  - **Open questions** in agent.md that now have **Human answer** below them → one bullet: "Preference: [answer]."
  - **Lessons learned** and logbook **Implications** from this run → rewrite as "When … then …" or "Always …" if not already.

- **Merge:** Append the new bullets to `agent-context-evolving.md` (or to a "pending" section).

- **Trim (keep under budget):**
  - Option A: Keep only the **last N lines** (e.g. 50).  
  - Option B: Keep only the **last K days** of contributions.  
  - Option C: Ask the LLM (or a small script) to **summarize** the full list into a fixed number of bullets, preserving the most important corrections and verdict-driven rules.

Result: a **single, short block** that carries the best of the day's (or week's) feedback into the next run. The agent gets a **continuously evolving prompt** without unbounded growth.

---

## 4. Who runs the crystallization step

- **Option A — Agent does it:** At the **end** of each run, the workstation agent has an instruction: "Before exiting, update `03-Agents/agent-context-evolving.md`: add 1–3 bullets from today's lessons and from any corrections/verdict feedback you have access to; then trim the file to the last 50 lines (or 500 tokens)." So the **same** agent run that did the tasks also updates the evolving context.  
- **Option B — Separate step:** After the agent run, a **script or a tiny LLM call** reads agent.md, corrections.md, and tasks with verdicts, and writes/trims `agent-context-evolving.md`. Keeps the main agent run simpler and lets you enforce a strict format.  
- **Option C — Human-assisted:** You run a QuickAdd macro or a command that (1) shows you "New bullets proposed from today's feedback" and (2) lets you approve/edit before they’re merged and the file is trimmed. Highest control, more manual.

Recommendation: start with **Option A** (agent updates the file at end of run) and a simple trim rule (e.g. keep last 40 lines). If the block gets noisy or format drifts, move to Option B and a script.

---

## 5. Format of `agent-context-evolving.md`

Keep it **scannable** and **actionable**. Example structure:

```markdown
# Evolving context (read at run start; stay under 50 lines)

## Do / prefer
- When creating entity stubs, link parent to investigation; set confidence low until validated.
- Use canonical handoff format (Agent: / Handoff:) in 01-Memories/shared so next agent can parse.
- [From approved feedback] Keep writing clear result_summary and output_files in task frontmatter.

## Don't / avoid
- [Correction 2026-03-11] Don't promote entity confidence to medium before human or second-agent validation.
- [Needs-revision] Avoid leaving "Open questions" empty when the task touched ambiguous data.

## When …
- When task has parent task: include handoff reference in Context section.
- When evidence is unverified: set source_quality to unverified and confidence low.
```

The agent is instructed (in agent_runner or system prompt): **"At run start, read 03-Agents/agent-context-evolving.md and adapt your behavior to these rules."** So the **prompt** that evolves is this file; it’s **compressed** by trimming (and optionally summarizing) so it stays within budget.

---

## 6. Quick reference

- **Most effective for adaptation:** Corrections > verdict + feedback > what worked (approved patterns) > answered open questions > edge cases/failures > distilled lessons > approved suggestions.  
- **Evolving prompt:** A single file (e.g. `03-Agents/agent-context-evolving.md`) that gets **appended** from the day's feedback and **trimmed** to a fixed size each run (or daily).  
- **Compression:** New bullets from corrections, verdicts, answers, lessons → merge into file → keep last N lines (or last K days, or LLM-summarize).  
- **Who updates:** Agent at end of run (Option A), or a script (Option B), or human-assisted merge (Option C).

This gives you a **continuously crystallized, evolving prompt** so the agent becomes more adaptive and skilled next time without blowing context size.
