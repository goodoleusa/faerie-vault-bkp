# Faerie — human guide (high level)

> **LEGACY:** This document predates the 2026-04-05 overhaul.
> For current docs, see [README.md](../README.md) or the vault LAUNCH/ folder.
> Kept for historical reference.

**Audience:** Operators and curious humans learning the system.  
**Not for agent context:** Do **not** paste this file into Claude as “the faerie skill.” Agents use **`.claude/commands/faerie.md`** (crystalline Turn 1 only). This doc is **narrative** and **long** on purpose.

---

## 1. What faerie is

**Faerie** is the **session-start orchestrator** for the faerie / Claude Code stack: one command (`/faerie`) that orients the **main** session, reads shared state (memory, queue, handoffs), **launches** high-priority work on **background subagents**, prints a **short brief**, and kicks the **dashboard** (Mission Control). Think **passenger → pilot**: the human gets a clear picture; heavy work runs in **fresh subagent contexts**, not in the main thread.

Design goals:

- **One Turn 1** — no “fast vs deep” branching; the model always knows what to read.
- **Act first** — no “ready to launch?” for queued `HIGH` work.
- **Hooks first** — hooks and small scripts own the happy path; long manual bash is for recovery (see **`docs/DESIGN-QUESTIONS.md`**).
- **Token discipline** — the **slash** (`faerie.md`) stays small; this guide lives in **`docs/`** so it never bloats the default session.

---

## 2. Mental model

| Idea | Meaning |
|------|--------|
| **Orbit** | Main session stays lean; subagents carry heavy work in separate contexts. |
| **One queue** | `sprint-queue.json` + lock protocol — same contract on Windows, macOS, Linux (`SPRINT_QUEUE.md`). |
| **Piston** | Queue entries are **claim-ready** (template + context bundle); work **chains** upstream → downstream; follow-ups land back on the queue; **git commit** often so a crash doesn’t wipe progress. |
| **Machine truth** | `s3a_faerie_turn1.py` JSON, `faerie-brief.json`, and **`training`** from `faerie_training_orchestrator.py` — prose in chat should not restate schemas. |

---

## 3. Turn 1 (what happens in one response)

1. **Read** (in priority order, stop when enough): fresh **`faerie-brief.json`** (if &lt; ~12h) → **investigations** (`index` + `inv-*/state`) → **handoffs** → **HONEY** head → **queue** (`queue_ops.py list`) → **agent-messages** (`*-Q`) → **scratch** only if brief/handoff are thin.
2. **Run** `s3a_faerie_turn1.py` (or equivalent) so **training** and **hooks** from the orchestrator are merged into the picture.
3. **Launch** up to **three** `HIGH` + `queued` tasks as **`Agent`** with **`run_in_background=true`**, correct **`subagent_type`**, TRAINING block (**subagent-spawn** contract).
4. **Brief** the human in **≤10 lines** (LAUNCHED, NEW, REVIEW, QUEUE, checkin).
5. **Dashboard** — `faerie-dashboard-launcher.py` so Mission Control (or the watch line) appears.

Stale brief or recovery? **membot** may run in the background to repair handoff/brief; **launches do not wait** for permission.

---

## 4. Memory and roles

| Piece | Role |
|--------|------|
| **faerie** | Human-facing orientation, template fill, queue adds, **brief**, spawn decisions. |
| **membot** | Mechanical promotion: scratch → REVIEW-INBOX → HONEY/NECTAR, run-eval, W&B sprint logging when configured. |
| **HONEY / NECTAR** | Durable preferences and findings (bounded reads; see **`memory-routing.md`**). |
| **faerie-brief.json** | Stop hook + Turn 1 fast path — compact snapshot for the next session. |

Rule of thumb: **humans** talk to `/faerie`; **agents** doing grunt memory work should run **`membot`**, not inline in faerie.

---

## 5. Queue, templates, and “piston” discipline

Every task faerie (or sprint-prep) adds should be **subagent-ready**:

- Filled **`SESSION_INPUT_TEMPLATE`** (or OSINT variant) under **`sprint-queue/sprint-*.md`** when using files.
- **`queue_ops.py add`** with **`--context-file`** whose bundle includes **`highest_value`**, **`done_looks_like`**, **`source_files`** (see **`SPRINT_QUEUE.md`** and **`queue_ops.py`** dead-reckoning).

Dependencies: **`spawned_by`**, **`next_on_success` / `next_on_failure`**, **`agent-messages/*-A.md`** for blocking Q&A. Cross-project work **must** be queued with `--source faerie:cross-project` (or similar), not only mentioned in chat.

---

## 6. Roster, rules, training, and eval

- **Roster:** `subagent-options.json` + **`select_agent.py`** for choosing types.
- **Cards:** `~/.claude/agents/{type}.md` — **bounded** reads per **`memory-routing.md`**.
- **Project digest:** `{repo}/.claude/memory/HONEY.md` (crystallized project facts).
- **Training:** `training-queue.json`, `training-log.jsonl`; Turn 1 **training** JSON from **`faerie_training_orchestrator.py`** (read the **module docstring** for semantics).
- **Benchmarks:** `run-benchmarks.json` for prior scores and “beat last” context.

Full path table: **`.claude/commands/faerie.md`** § “Roster, rules, training & eval.”

---

## 7. Dashboard and hooks

- Hooks try to spawn **`dashboard.py`** / launcher — **no** main-session token cost for the default path.
- If no frame appears, **`docs/DASHBOARD-QUICKSTART.md`** — second window watcher (`dashboard.py --watch`) as fallback.
- **Session heartbeats** (`session_heartbeat.py`) register sessions; **`investigation_id`** links collaborators working on the same case.

---

## 8. Investigation mode

- Active investigation: **`investigations/index.json`** → **`inv-{id}/state.md`**.
- Override: **`/faerie --inv inv-…`**.
- Link session: **`session_heartbeat.py link INV --also-active`** or **`/investigation`** helpers.

---

## 9. Session modes (flags)

| Flag | Meaning |
|------|--------|
| `/faerie` | Default: orient + launch HIGH + dashboard + brief. |
| `--train` | Surface training / autotune queue. |
| `--review` | Review / red-team; **no** queue task launch. |
| `--queue` | Queue management only. |
| `--crystallize` | Intentional close — promote memory, queue threads. |
| `--explain` | Narrate subsystems (teaching mode). |

**End of day:** prefer **`/faerie --crystallize`**; stop hook still writes **`faerie-brief.json`**.

---

## 10. Related docs (read next)

| Doc | Purpose |
|-----|--------|
| `docs/DESIGN-QUESTIONS.md` | Hooks vs scripts, token budget, hot files |
| `docs/DASHBOARD-QUICKSTART.md` | Full dashboard / watch |
| `docs/ARCHITECTURE.md` | System map |
| `hooks/state/SPRINT_QUEUE.md` | Queue schema + lock protocol |
| `.claude/rules/memory-routing.md` | Bounded reads, crystallization |
| `.claude/commands/faerie.md` | **Agent** canonical slash (short) |

---

## 11. Human vs agent docs

Long narrative and positioning live in **`docs/`** (this file and others) so they do **not** load into Claude’s slash-command path. The agent-facing slash is **`.claude/commands/faerie.md`** only.
