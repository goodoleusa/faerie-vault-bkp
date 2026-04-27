---
type: dashboard
stage: review
tags: [dashboard, agent-insights, review]
parent:
  - "[[HOME]]"
sibling:
  - "[[Annotation-Dash]]"
  - "[[Chain-of-Custody]]"
  - "[[Unprocessed-Stubs]]"
doc_hash: sha256:9d75e85558428cb60812435f01bb89a5e8cc13933abbc2f06757fd7403e53f73
hash_ts: 2026-03-29T16:10:00Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|← HOME]] · [[Phase1-AgentSync|← Investigation]] · [[Annotation-Dash|← Annotate]] · **Agent Insights** · [[Chain-of-Custody|COC →]]

# Agent Insights — Last 24h feed + validate & promote

Single place to see **agent insights, updates, and questions** from the last 24 hours, and to **validate each item and promote it to the next phase**.

**Theme:** **Human promotes, AI executes.** [[09-HUMAN-PROMOTES-AI-EXECUTES]] — Agents stop at intervention points; you promote so they can continue.

**Design:** [[05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK]] — agent.md is the source of truth; this dashboard aggregates a view and makes review/promotion easy.

---

## ⚠️ Human intervention required

The sections below are where **you must intervene** before the agent can continue. Use [[03-Agents/agent]] for open questions and suggested improvements; use the task tables for verdicts. Agents phrase each decision in short **Decision needed:** + **Options:** form so you can run through approvals quickly.

---

## 1. Validate & promote — workflow

| Step | Action |
|------|--------|
| **Tasks** | Open the task → set **Review** section: **Reviewed by**, **Review date**, **Verdict** (`approved` or `needs-revision`), **Feedback**. Set frontmatter `review_verdict: approved` (or `needs-revision`) so the dashboard stops listing it in "Needs review." |
| **Promote task** | After **approved**: move the task note to **99-Archives/** (or your "done" folder) so it leaves the inbox and is considered promoted to the next phase. |
| **Open questions** | Open [[03-Agents/agent]] → answer under "Open questions for human" (or in the linked investigation/task). Agent reads back on next run. |
| **Logbook items** | If a logbook entry should drive a follow-up task or promotion to knowledge base, create a task or add to [[01-Memories/agents/agent-logbook]] / KNOWLEDGE-BASE as appropriate. |

---

## 2. ⚠️ Tasks needing review (human promotes → then move to 99-Archives)

Completed tasks that still have **Verdict: pending** (or no `review_verdict`). Open each link, fill the Review section and set `review_verdict` in frontmatter; when approved, move to 99-Archives to promote.

```dataview
TABLE
  file.link as "Task",
  assignee as "Agent",
  result_summary as "Summary",
  dateformat(file.mtime, "yyyy-MM-dd HH:mm") as "Done"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Queue"
WHERE type = "task" AND status = "done" AND (review_verdict != "approved" OR !review_verdict)
SORT file.mtime DESC
LIMIT 25
```

---

## 3. Approved — ready to promote (move to 99-Archives)

Tasks you’ve marked **approved** but that are still in the inbox. Move each to **99-Archives/** to complete promotion.

```dataview
TABLE
  file.link as "Task",
  assignee as "Agent",
  dateformat(file.mtime, "yyyy-MM-dd HH:mm") as "Approved"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Queue"
WHERE type = "task" AND status = "done" AND review_verdict = "approved"
SORT file.mtime DESC
LIMIT 15
```

---

## 4. ⚠️ Agent status & open questions (human intervention required)

**→ [[03-Agents/agent]]** — Last 24h insights, **open questions for human**, lessons, suggested improvements.  
**Validate:** Open the note and answer or triage each open question; agent reads back after sync.

---

## 5. Recently completed tasks (last 24h feed)

All completed tasks in the last 24 hours (by file modification time).

```dataview
TABLE
  file.link as "Task",
  result_summary as "Summary",
  review_verdict as "Verdict",
  dateformat(file.mtime, "yyyy-MM-dd HH:mm") as "Completed"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Queue"
WHERE type = "task" AND status = "done"
SORT file.mtime DESC
LIMIT 20
```

---

## 6. Agent logbook & history

- **[[01-Memories/agents/agent-logbook]]** — Learnings; promote notable ones to knowledge base or new tasks.
- **[[03-Agents/agent-history]]** — Chronological task completions and files touched.

---

## 7. Task lineage — parent tasks with subtasks

Parent tasks (this task has at least one **child**). Open the parent to see **Compressed summary** and **Task lineage → Children** for coordination. See [[10-TASK-LINEAGE-AND-HANDBACK]].

```dataview
TABLE
  file.link as "Parent task",
  child as "Children",
  assignee as "Assignee"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Queue"
WHERE type = "task" AND child
SORT file.mtime DESC
LIMIT 20
```

---

## 8. Investigation scratchpad (agent findings)

**[[Agent-Findings]]** — Recently updated investigations with agent questions and discoveries. Validate and promote findings into investigations or evidence as needed.

---

See [[05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK]] for dashboard vs agent.md and safe sync-back to the air-gapped workstation.  
**Task linking:** [[10-TASK-LINEAGE-AND-HANDBACK]] — parent/child/sibling, crystallized summary for handback, tracking without noise.
