# Context, memory, and sprint consolidation

> **LEGACY:** This document predates the 2026-04-05 overhaul.
> For current docs, see [README.md](../README.md) or the vault LAUNCH/ folder.
> Kept for historical reference.

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
**Artifacts:** roundup file(s), HONEY.md (if --learn), filled template file; queue entry if user chose "add to queue".

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
- **continual-learning** — promote to NECTAR, crystallize to HONEY (invoked by /faerie).

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

---

## 2026-03-15: Desktop/CLI Split + Forensic Consolidation

### Three output folders created:
- `claude-cli/` — deduplicated CLI config (canonical)
- `claude-desktop/` — Desktop-compatible subset (no Agent tool, no hooks)
- `claude-forensic/` — all investigation data from 8 session fragments (193 session files, 41 primary + 152 subagent)

### Deduplication applied:
- Single status footer definition (rules/token-optimization.md canonical; CLAUDE.md references by path)
- Single REVIEW-INBOX (memory/REVIEW-INBOX.md canonical)
- Single continual-learning entry (/faerie is the only user-facing command)
- Merged proposal queues (memory/improvement-proposals.md: code fixes + rule changes)
- Removed deprecated: multi-agent-coordinator, agent-organizer, statistical-analysis-subagent, membot.md.bak
- Fixed data-ingest SKILL.md: multi-agent-coordinator -> workflow-orchestrator
- Restored commands/new.md (was 1 byte)
- Wired presend_estimate.py -> usage_log.jsonl (was 0 entries)
- Wired session_stop_hook.py -> token-context-log.json (was empty)
- Vault agent memory protocol: local push/pull marked ACTIVE (vault_push.py created)
- Vault target files created/seeded: AGENT-REVIEW-INBOX.md, KNOWLEDGE-BASE.md

### Hash/Sign/COC script hierarchy (documented):
- `hash_tracker.py` (C:\Users\amand\hashtracker\) — foundation HMAC + PGP
- `forensic_sign.py` — commit hook wrapper (calls hash_tracker)
- `hash_guardian.py` — full rawdata SHA-256 audit
- `coc.py` — pipeline integration module (stamp_input/stamp_output)

### Forensic provenance recovered:
- 4 buried COC files returned to cybertemplate/forensic/: hash_update_017.json, pipeline_log.json, prisma_vision_hashes.json, prisma_coc_log.json
- 28 provenance docs consolidated in claude-forensic/provenance/
