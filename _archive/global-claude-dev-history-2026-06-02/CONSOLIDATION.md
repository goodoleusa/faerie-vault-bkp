# Context, memory, and sprint consolidation

Single reference for the two main intents and how skills/agents/commands chain. Everything can run **independently** or be **chained** as below.

---

## Intent 1 — Pre-session + ready for /new: "Where we WERE and DID, then get prompt for /new"

**Goal:** Round up context and memory, fill the session template, then either add to queue or hand off the prompt for /new.

| Step | What | Runs alone? |
|------|------|-------------|
| 1 | **/faerie** — roundup + learn + fill session template (ask user what’s needed) + add to queue or hand off prompt for /new | ✓ |
| 2 | Optional: **memory-keeper** — promote scratchpad, update KNOWLEDGE-BASE, next-steps | ✓ |
| 3 | Optional: **/compact** or **/handoff** — context bundle for next session | ✓ |

**Command:** **/faerie** (one command). For roundup-only without template: **context-roundup** skill.  
**Artifacts:** roundup file(s), AGENTS.md (if --learn), filled template file; queue entry if user chose "add to queue".

---

## Intent 2 — Into active sprint: "/new into an active sprint"

**Goal:** Start a session from the queue or a pasted template; have a clear lead and optional memory/roundup.

| Step | What | Runs alone? |
|------|------|-------------|
| 1 | **/new** — reads sprint-queue.json, REVIEW-INBOX, or pasted template | ✓ |
| 2 | **team-builder** — assembles team (lead, specialists, support) | ✓ (or via /new) |
| 3 | **workflow-orchestrator** — default **session lead**; run-eval at end | ✓ |
| 4 | Queue filled by **/faerie** (or optional **sprint-prep** for template-only when context already in hand) | ✓ |
| 5 | Optional: **task-distributor** — distribute steps across workers | ✓ |
| 6 | End: **memory-keeper** and/or **/done**, **/handoff** | ✓ |

**Commands:** `/new`, `/sprint-prep`, `/done`, `/handoff`.  
**Queue:** `~/.claude/hooks/state/sprint-queue.json`, `SPRINT_QUEUE.md`; templates in `SESSION_INPUT_TEMPLATE*.md`.

---

## Consolidated agents (redundancy removed)

| Before | After |
|--------|--------|
| workflow-orchestrator | **workflow-orchestrator** (unchanged name) — now also covers team coordination and multi-agent sync |
| agent-organizer | Merged into **workflow-orchestrator** |
| multi-agent-coordinator | Merged into **workflow-orchestrator** |
| task-distributor | **Kept** — lightweight queue/load distribution; invoked by conductor when needed |
| context-manager | **Kept** — shared state and retrieval; roundup artifact |
| memory-keeper | **Kept** — end-of-session promote & next-steps; natural after /faerie |
| team-builder | **Kept** — interactive team assembly; used by /new |

**Deprecated (redirect to workflow-orchestrator):** `agent-organizer`, `multi-agent-coordinator` — see their .md files for stub.

---

## Skills that stay distinct (chainable)

- **context-roundup** — round up sources into one file; optional --learn. When run as **/faerie**, also fills session template and does queue or /new handoff.
- **sprint-prep** — optional; template-only fill when you already have context. **Prefer /faerie** for full flow (roundup + learn + template + queue or /new).
- **memory** — scratchpad, REVIEW-INBOX, KNOWLEDGE-BASE; promote FLAGs/DECISIONs.
- **compact** — context bundle for handoff.
- **subagent-spawn** — enforce real spawns; used by /new and team-build.
- **continual-learning** — merge durable bullets into AGENTS.md (invoked by /faerie).

---

## Quick reference

| I want to… | Use |
|------------|-----|
| Round up context, learn, fill template, and get prompt for /new or add to queue | **/faerie** (one command) |
| See where we were (roundup only, no template) | context-roundup skill |
| Start a sprint from the queue | /new (no args) or paste filled template |
| Template-only fill (context already in hand) | sprint-prep skill (optional) |
| Session lead + run-eval | workflow-orchestrator (default lead in /new) |
| Promote items and get next-steps | memory-keeper or /memory |
| Hand off to next session | /compact or /handoff |
