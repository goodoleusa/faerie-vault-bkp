---
doc_hash: sha256:pending
created: 2026-04-25
type: playground-index
folder: 50-Honesty-System
breadcrumb: "vault / 50-Honesty-System / INDEX"
---

# 50-Honesty-System — The Reputation Paradox

faerie2 maintains reputation scores for every agent type. These scores affect routing: higher-reputation agents get preference for matching tasks. But there is a built-in paradox at the heart of this system. Understanding the paradox is essential to understanding why the system is designed the way it is.

---

## The Paradox

> **An agent cannot see its own reputation score before it runs.**

This is intentional. Deliberate. Load-bearing.

If an agent knew its score, it would optimize for the score rather than the task. This is Goodhart's Law at the agent level: when a measure becomes a target, it ceases to be a good measure. An agent that knows it scored 0.72 last time will bias its behavior toward whatever it believes produced that score — whether or not that's the right behavior for the current task.

The solution: agents are blind to their own card at execution time.

---

## How the Anti-Gaming Protocol Works

```
BEFORE RUN:
  Parent reads task from queue
  Parent calls 7x_spawn_template.py --bundle
  Bundle includes discovery.json (predecessor artifacts from forensics/)
  Bundle does NOT include: agent's Last Training, KPI, BASELINE score
  Agent receives bundle only — no access to ~/.claude/agents/{type}.md

DURING RUN:
  Agent executes in isolated context
  Agent cannot grep its own card (has no reason to — it doesn't know to look)
  Agent writes artifacts based on the task requirements, not score optimization

AFTER RUN:
  Eval harness reads private agent card
  Eval scores the run output against criteria
  If new_score > last_score: eval appends to Last Training section
  Parent writes "Last Training" entry to card (append-only)
```

The card is the system's memory. The agent is the system's executor. They never meet before the run.

---

## Cross-Agent Transparency — The Partial Solution

The paradox is: agents can't see their own card, but they CAN be exposed to transparency from a different angle.

**Proposed mechanisms (some implemented, some brainstorm):**

### 1. Eval-Injected Last Training (Implemented)
After the run, the eval score is appended to the card. The next time the same agent type runs on a similar task, the parent can inject a brief non-score summary: "This agent type performed well on vault consolidation tasks last session (qualitative note only — no score)." This preserves the anti-gaming property (no score visible) while providing meaningful signal.

### 2. Routing Demotion as Signal (Implemented via reputation weighting)
An agent that scored below baseline does not get priority routing for its specialization. The agent never knows it was demoted — but the system's behavior changes. The agent receives harder tasks less often, gets easier ones more often (where it can rebuild score), and is gradually re-validated before being trusted with high-stakes work again. Demotion is silent, proportional, and reversible.

### 3. Cross-Agent Transparency (Proposed)
A synthesizer agent — who has no stake in any individual agent's score — reads multiple agent cards and writes a `reputation-snapshot.md` to the vault. Individual agents can reference this snapshot (it doesn't name their own score directly; it describes the landscape: "documentation agents have been performing above baseline this week; python-pro agents below baseline on refactor tasks"). The agent learns its relative standing without learning its absolute score.

### 4. Reputation Snapshot on Tasks (Proposed)
When the system logs `claimed_by_agent_reputation_at_claim_time` (see [[20-Queue-Mission/INDEX]]), this creates a historical record: what did the system believe about this agent when it trusted them with this task? After the run, you can compare: predicted reputation → actual score. This feeds a calibration loop: is the reputation score actually predictive of task success?

---

## The Feedback Loop Diagram

```
Task completed by Agent X
        │
        ▼
Eval harness scores output
  Criteria: seeded (from task) + emergent (agent augmentation)
  Blind scoring: eval reads private card AFTER run, never before
        │
        ▼
Score compared to last_score
  If new > last:  append to Last Training (agent improves on record)
  If new ≤ last:  no update (no regression noise; agent card stays clean)
  If new < baseline: flag for routing demotion review
        │
        ▼
Routing engine re-weights
  Next task of same type: demotion penalty applies
  Over time: only consistently-performing agents get high-stakes routing
        │
        ▼
Agent runs next task
  Still blind to its own score
  But the task difficulty and type have been calibrated to its demonstrated ability
  The system has adapted; the agent has not gamed it
```

---

## Why Not Just Show Agents Their Score?

Experimental framing: imagine two versions of the system.

**Version A (current):** Agent is score-blind. It optimizes for the task description and success criteria. Scores reflect actual performance on the task.

**Version B (score-visible):** Agent sees its score (e.g., 0.72) before running. It now has an implicit objective: demonstrate the behaviors that produced 0.72 on past runs, and exceed them. This creates a second optimization target that competes with the primary task. The agent may sacrifice task quality to demonstrate score-earning behaviors. The score becomes less reliable as a signal.

The same dynamic appears in human performance evaluation systems: people optimize their year-end review metrics, not their actual job. The metrics diverge from the underlying performance. The score becomes noise.

faerie2's solution is architectural: separation of the scoring channel from the execution channel. The agent cannot optimize for what it cannot see.

---

## The Open Question

The paradox has an unresolved tension: **the agent can never learn from its own scores in real-time.** It improves across runs only through the routing system's implicit feedback (getting harder or easier tasks) — not through knowing "I scored 0.87 last time because I wrote clear dashboard_lines."

One approach: allow the agent to read a **general rubric** ("dashboard_lines ≤80 chars are scored higher") without reading its own specific score history. The rubric is the task spec; the score is the private signal. This is how good evaluation rubrics work in human contexts: the evaluator's rubric is public; the individual score is private.

This is the current design. Whether a richer feedback mechanism is possible without re-introducing gaming incentives is an open research question in the system.

---

[[00-Welcome/INDEX]] | [[10-Processes/INDEX]] | [[20-Queue-Mission/INDEX]] | [[30-Dashboards/INDEX]] | [[40-Roster-Routing/INDEX]]

*sha256:pending*
