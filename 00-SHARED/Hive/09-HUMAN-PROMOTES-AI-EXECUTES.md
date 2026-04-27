---
type: meta
tags:
  - meta
  - theme
  - human-in-the-loop
  - approvals
created: 2026-03-11
updated: 2026-03-11
parent: []
child: []
sibling: []
memory_lane: nectar
promotion_state: raw
doc_hash: sha256:f65fb3b9ecfe637982eb56ac55d1036a93b0ea848d40305fbaf4c964b93280f7
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:17Z
hash_method: body-sha256-v1
---

# Human promotes, AI executes

**Vault-wide theme.** Use this phrase everywhere to avoid term drift: **Human promotes, AI executes.**

- **Human promotes:** Raw AI output (tasks completed, questions, ideas, suggestions, insights) is reviewed by a human. The human **promotes** what is good — e.g. sets task verdict to approved, answers open questions, copies approved suggestions into approved locations, moves tasks to 99-Archives. Nothing that changes agent behavior or moves to the next phase happens without human promotion.
- **AI executes:** The agent runs tasks, writes raw output to agent.md and task files, and reads **approved** content (corrections, suggestions-approved, context-evolving). The agent does not promote its own work; it executes and then stops at clear **Human intervention required** points.

**Where humans must intervene before the agent can continue:** Tasks needing review (verdict pending), open questions in agent.md, suggested improvements awaiting promotion to approved locations, and any item in agent.md that the agent has marked **Decision needed**. The dashboard and agent.md make these points visually clear (see [[Agent-Insights]], [[03-Agents/agent]]). **Scope too broad:** If an agent has 3+ open questions, it must add to Pain points / Scope or struggle that the subagent may need refinement or task splitting (see [[05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK#1.2b Agent separation: few questions, scope too broad]]).

**Concise approval language:** Agents use a short, scannable format when they need a human decision so reviewers can run through many approvals quickly. See [[05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK#1.2c Agent language for human decisions (fast approvals)]].

**Agent separation:** Agents stay as separate as possible; only extremely important questions go to the orchestrator. Many questions = scope too broad → agent reports "Scope too broad?" in agent.md so humans can refine the subagent or split the task.
