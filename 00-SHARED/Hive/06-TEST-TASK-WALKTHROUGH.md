---
type: meta
tags: [meta, test, walkthrough, agents, tasks]
created: 2026-03-11
doc_hash: sha256:92615355d02b5b7ce2dfe7deb42cb06ec7922b34d41c5c602750517e23d1db78
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---

# Test task walkthrough — one task through the full process

A **single test task** is taken through the full lifecycle: human creates → agent 1 claims, executes, writes outputs and handoff → agent 2 reads handoff, claims follow-up task, validates and updates. This doc shows how that one flow **links out to all relevant vault info** and stays concise.

**Scenario:** Initial OSINT on domain `example-org.net` (test only). Agent 1 creates investigation + entity and hands off; Agent 2 validates and updates confidence.

---

## Process summary

| Stage | Who | What | Files touched |
|-------|-----|------|----------------|
| 1. Create | Human | Create task in 00-Inbox | [[00-Inbox/Test-Task-OSINT-Example]] |
| 2. Claim & run | agent-osint-1 | Sanitize, claim, load memories, execute | Task, [[10-Investigations/Test-Case-Example]], [[20-Entities/Test-Entity-Example]], [[01-Memories/shared/2026-03-11-Research-agent-osint-1]] |
| 3. Handoff | agent-osint-1 | Write Agent:/Handoff: block in shared | [[01-Memories/shared/2026-03-11-Research-agent-osint-1]] |
| 4. Log & complete | agent-osint-1 | Update history, logbook, task status | [[03-Agents/agent-history]], [[01-Memories/agents/agent-logbook]], task → done |
| 5. Follow-up task | Human or agent | Create next-step task (optional) | [[00-Inbox/Test-Task-OSINT-Example-Follow-Up]] |
| 6. Claim & validate | agent-validator-2 | Read handoff, validate entity, update investigation | Follow-up task, [[20-Entities/Test-Entity-Example]], [[10-Investigations/Test-Case-Example]], agent-history, logbook |
| 7. Status | Workstation agent | Update agent.md for human | [[03-Agents/agent]] |

---

## How the task links out (concise map)

```
00-Inbox/Test-Task-OSINT-Example
├── output_files → 10-Investigations/Test-Case-Example, 20-Entities/Test-Entity-Example
├── child → 00-Inbox/Test-Task-OSINT-Example-Follow-Up
├── Context → 10-Investigations/Test-Case-Example
├── Execution log → 01-Memories/agents/agent-logbook, 01-Memories/shared (handoff)
└── Agent history entry → 03-Agents/agent-history

01-Memories/shared/2026-03-11-Research-agent-osint-1
├── Contains: Agent: agent-osint-1 / Handoff: ... (canonical format)
├── Read by: agent-validator-2 for follow-up context
└── Refers to: Test-Case-Example, Test-Entity-Example, follow-up task

10-Investigations/Test-Case-Example
├── child → 20-Entities/Test-Entity-Example
├── Created by: task Test-Task-OSINT-Example
└── Updated by: follow-up task (validation note in Agent questions)

20-Entities/Test-Entity-Example
├── parent → 10-Investigations/Test-Case-Example
├── Created by: task Test-Task-OSINT-Example
└── Updated by: follow-up task (confidence low → medium)

03-Agents/agent-history
└── Entries for both tasks (agent-osint-1, agent-validator-2) with task links and files

01-Memories/agents/agent-logbook
└── Learnings: handoff format, example-org.net initial (with source = task)

03-Agents/agent
└── Last run summary, lessons, suggested improvements (for human)
```

---

## Where to look for what

| You want… | Look at |
|-----------|--------|
| Task definition and execution log | [[00-Inbox/Test-Task-OSINT-Example]], [[00-Inbox/Test-Task-OSINT-Example-Follow-Up]] |
| What agent 1 produced | [[10-Investigations/Test-Case-Example]], [[20-Entities/Test-Entity-Example]] |
| What agent 2 used (handoff) | [[01-Memories/shared/2026-03-11-Research-agent-osint-1]] (Agent:/Handoff: block) |
| Chronological agent actions | [[03-Agents/agent-history]] |
| Persistent learnings | [[01-Memories/agents/agent-logbook]] |
| Workstation status for you | [[03-Agents/agent]] |

---

## Flow in one sentence

Human creates task → agent 1 claims, creates investigation + entity, writes handoff to 01-Memories/shared and logs to agent-history / agent-logbook → agent 2 reads handoff, runs follow-up task, validates entity and updates investigation + agent-history / logbook → workstation agent updates 03-Agents/agent for human; all of it links via wikilinks and the canonical handoff format.

**See:** [[03-AGENT-HANDOFF-EXPLAINER]] (flow and hops), [[04-QUICKADD-GLOBAL-VARS-HANDOFF]] (handoff format), [[01-ARCHITECTURE]] (topology and memory).
