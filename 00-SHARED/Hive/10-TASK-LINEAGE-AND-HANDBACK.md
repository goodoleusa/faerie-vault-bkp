---
type: meta
tags:
  - meta
  - tasks
  - lineage
  - handback
created: 2026-03-11
updated: 2026-03-11
parent: []
child: []
sibling: []
memory_lane: nectar
promotion_state: raw
doc_hash: sha256:3d9420d379b550c4923c5346b4b077ea7d57f05ecdff7f6f0943106e21f13f66
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:18Z
hash_method: body-sha256-v1
---

# Task lineage, handback summary, and tracking

How tasks link traceably to each other, how the **crystallized summary** in the task file gives the next agent full context when a task (or follow-up) returns to the inbox, and how to track **parent → subtasks** without noise.

**See also:** [[01-ARCHITECTURE]] (task lifecycle), [[05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK]] (agent write map), [[Templates/Task-Inbox]] (task template).

---

## 1. Compressed summary in the task file

Every task file includes a **Compressed summary (for handback / next agent)** section. The **completing agent** fills it with short bullets:

- **Major learnings** (what we found, what we concluded)
- **Key conclusions** (decisions, confidence, caveats)
- **Open questions** (what’s still unknown or needs another expertise)
- **What the next agent should know** (handoff in one place)

So when the **same task** is re-queued or a **follow-up task** is created for a different expertise agent, that agent gets context **inside the task file** without hunting across agent.md or handoff notes. The task is self-contained for handback.

**Agent Learnings** in the same file is the longer-form version; the **Compressed summary** is the minimal version that must be in the task so handback works.

---

## 2. Linking tasks traceably (parent / child / sibling)

### 2.0 Frontmatter format (canonical)

All task frontmatter that carries links or multi-value lists uses **multi-line YAML arrays**. Wikilinks in frontmatter must be **correctly formatted** so Obsidian and Dataview resolve them.

- **tags, parent, sibling, child, touched_by** — Always use multi-line array form. Empty = one line with a single dash and nothing after, or a dash then space.
- **Wikilinks** — Use vault-relative paths in double brackets: `[[00-Inbox/Task-Name]]` or `[[Task-Name]]` if the note is in 00-Inbox. In YAML list items, **quote the wikilink** so colons/slashes don’t break parsing: `- "[[00-Inbox/Parent-Task]]"`. No spaces inside the brackets; path must match an existing or soon-to-exist note.
- **Example (subtask with parent):**
```yaml
tags:
  - task
  - inbox
parent:
  - "[[00-Inbox/OSINT-Main-Task]]"
sibling:
  - 
child:
  - 
touched_by:
  - agent-osint-1
```

So: **multi-line array by default** for tags, parent, sibling, child, touched_by; **wikilinks as `[[correctlyformatted]]`** (quoted in YAML when in a list).

### 2.1 Frontmatter

- **parent** — The task this one was spawned from (umbrella task). One link: `[[00-Inbox/Parent-Task-Name]]` in a multi-line list: `parent:\n  - "[[00-Inbox/Parent-Task-Name]]"`.
- **child** — Subtasks or follow-ups spawned from **this** task. Multiple links, each quoted: `- "[[Child-Task-1]]"`, `- "[[Child-Task-2]]"`.
- **sibling** — Other tasks at the same level under the same parent. Optional; same format as parent/child.

### 2.2 Is it safe for agents to create subtasks outside their scope?

**Yes, when:**

1. The agent is **completing the current task** and spawning a **follow-up** for another skill (e.g. OSINT agent finishes and creates a validation subtask), and the follow-up is clearly scoped (description, acceptance criteria, `skill_required`).
2. The **task description or human** explicitly asks for a subtask (e.g. “Create a validation subtask for agent-validator”).

**Requirement:** The agent that creates the subtask **must write the correct frontmatter** on both:
- The **new task**: `type`, `status`, `parent` (one wikilink), `requester` (e.g. current assignee or “human”), `skill_required`, `tags`, `task_id`, and **touched_by** with the creating agent’s id (they “touched” it by creating it). Use the canonical format: multi-line arrays, wikilinks as `"[[00-Inbox/Parent-Name]]"`.
- The **parent task**: append the new task to **child** (and update **Task lineage → Children** in the body).

If the creating agent does not set `parent` and update the parent’s `child`, the lineage is broken and the subtask is untrackable. Agents that create subtasks must follow the checklist below.

### 2.3 Convention when creating a subtask or follow-up

1. **Create the new task** with frontmatter (canonical format):
   - `type: task`, `status: pending`, `task_id: TASK-YYYYMMDDHHmm` (or equivalent).
   - `parent:` multi-line list with **one** wikilink: `- "[[00-Inbox/Parent-Task-Name]]"`. Use vault-relative path; no spaces inside `[[...]]`.
   - `requester:` set to the agent or human who requested it (e.g. parent task’s assignee).
   - `skill_required:` set to the intended skill for the subtask (e.g. validation, stats).
   - `tags:` multi-line list including `task`, `inbox`, and any other tags.
   - `touched_by:` multi-line list with the **creating agent’s id** (e.g. `- agent-osint-1`). They created the note so they are the first “touch.”
   - `assignee:` can be left empty for the router to fill, or set if known.
   - `sibling:` and `child:` multi-line list empty (e.g. `child:\n  - `).
2. **Update the parent task** in the same run:
   - Add the new task to the parent’s **child** frontmatter: one new line `- "[[New-Task-Name]]"` (or `- "[[00-Inbox/New-Task-Name]]"`). Keep multi-line format; quote the wikilink.
   - Fill the parent’s **Task lineage** section in the body: **Children:** list including the new task (wikilink in body: `[[New-Task-Name]]`).

So **both directions** are linked: the child points to the parent, and the parent lists the child. The agent that creates the follow-up/subtask does both updates so the lineage stays consistent.

### 2.4 Siblings

When multiple subtasks share the same parent (e.g. one OSINT parent, two children: validation + stats), each child has the same `parent`. Optionally set **sibling** on each child to the other child task(s) so “same level” is explicit. Use multi-line list and quoted wikilinks: `sibling:\n  - "[[00-Inbox/Other-Child-Task]]"`. The parent’s **Children** list already shows all subtasks; siblings are for cross-linking between peers.

---

## 3. touched_by and task_signature (audit and signing)

These fields extend the vault’s **cryptographic hashing and signing** approach to tasks: all ingested vault content can be hashed/signed for integrity; tasks get an audit trail of who touched them and (when implemented) a signature.

### 3.1 touched_by

- **Purpose:** Audit trail of every agent (or human) who **completed** or **returned** the task — i.e. who last modified it in a meaningful way (marked done, handed back to inbox, or created it).
- **Format:** Multi-line YAML array of strings. Each entry is an **agent id** or **human** (e.g. `agent-osint-1`, `agent-validator-2`, `human`).
- **When to append:**
  - When an agent **creates** a new (sub)task, they add their id to `touched_by` on that new task.
  - When an agent **completes** a task (sets `status: done`), they **append** their id to `touched_by` (do not overwrite).
  - When an agent **returns** a task to the inbox (e.g. re-queues it or hands off to another agent), they append their id if they modified it.
- **Example:** After OSINT agent completes, then validator completes, `touched_by` might be: `- agent-osint-1`, `- agent-validator-2`. Humans reviewing can append `human` if desired.

So: **every agent who completes or returns a task adds their name/id to touched_by**. This supports accountability and, with `task_signature`, future verification that the task content matches the signer.

### 3.2 task_signature

- **Purpose:** Reserved for **cryptographic signature** of the task (e.g. HMAC-SHA256 over canonical task content or frontmatter). Aligns with the existing design: “Task signing (HMAC-SHA256)” and “evidence hashes, signed memories” (see [[01-ARCHITECTURE]]).
- **When implemented:** After each agent “touch,” the runner or agent can compute a signature over the task file (or a canonical serialization of frontmatter + key body sections), store it in `task_signature`, and optionally verify on read. This gives tamper-evidence and chain-of-custody for tasks, similar to evidence pipeline hashes.
- **Until then:** Leave `task_signature` empty. The presence of `touched_by` still gives a clear audit trail of who touched the task.

---

## 4. Task lineage section (in the task body)

Each task has a **Task lineage** section in the body:

- **Parent:** Link to the parent task (if this is a subtask/follow-up).
- **Children:** Links to all subtasks/follow-ups spawned from this task.
- **Siblings:** Links to sibling tasks (same parent), if any.

This duplicates the frontmatter in a **scannable place** so humans and agents can open one task and see the tree without running a query. When an agent adds a child, it updates both the parent’s **child** frontmatter and the parent’s **Task lineage → Children** in the body.

---

## 5. Tracking parent → subtasks without noise

- **Single place to look:** Open the **parent task**. Its **Compressed summary** gives the big picture (what’s learned, what’s open). Its **Task lineage → Children** (and frontmatter `child`) lists all subtasks. Each child can have a different `assignee` / `skill_required` (e.g. validation, stats).
- **Dashboard:** Use a Dataview table that lists tasks that have **child** non-empty, e.g. “Parent task | Children | Assignees” so you see which parents have subtasks and who’s doing them. No need to open every task; open only the parent when coordinating.
- **Bidirectional links:** Because parent frontmatter has `child` and each child has `parent`, Obsidian’s graph and backlinks show the tree. The **Task lineage** section is for quick in-file scanning.

So: **one parent task** = one place for compressed context + list of children. Subtasks stay linked; coordination is “open parent, see summary and children.”

---

## 6. Quick reference

| What | Where |
|------|--------|
| Compressed summary for handback | Task file section **Compressed summary (for handback / next agent)**; agent fills on completion |
| Parent of this task | Frontmatter `parent` + Task lineage **Parent:** |
| Subtasks/follow-ups from this task | Frontmatter `child` + Task lineage **Children:** |
| Same-level tasks under same parent | Frontmatter `sibling` + Task lineage **Siblings:** |
| When creating a subtask | Set child’s `parent` to this task; add child to this task’s `child` and **Task lineage → Children**; use canonical frontmatter (multi-line arrays, quoted `[[wikilinks]]`) |
| Who touched this task | Frontmatter `touched_by` — each agent who completes or returns the task appends their id |
| Task signature (future) | Frontmatter `task_signature` — HMAC-SHA256 over task content when implemented |

See [[Agent-Insights]] for tasks needing review. For a Dataview “parent → children” table, add a block that lists tasks where `length(child) > 0` and displays `file.link`, `child`, `assignee` (or link to parent and list children).
