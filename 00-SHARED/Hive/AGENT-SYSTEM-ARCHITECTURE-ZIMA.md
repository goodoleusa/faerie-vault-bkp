---
type: meta
tags: [zima]
parent: []
child: []
sibling: []
memory_lane: nectar
promotion_state: raw
doc_hash: sha256:227d97a2e65eac42ea907a6a90610d9b7e16b262cf25c6a2a3d42b0013f2770b
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:23Z
hash_method: body-sha256-v1
---
# CyberOps Agent System — Architecture

**Owner:** amand
**Last updated:** 2026-03-11
**Status:** Active production design
**Source notes:** `Huntin/00-dailynotes/FIRE zimaboard openclaw setup lumo.md`

---

## One-Line Summary

A federated, human-in-the-loop investigative AI system split across three physical
nodes: ZimaBoard (stateless memory & coordination), Workstation (compute & execution),
and Obsidian on the human's machine (review & steering). The vault is the shared bus —
agents communicate through vault files, never directly with each other.

---

## The Full System (read this first)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  HUMAN LAYER                                                                 │
│                                                                              │
│  Obsidian (Windows)           ZimaOS Native Chat                            │
│  ─────────────────────        ───────────────────────────────               │
│  1. Drop task in 00-Inbox     "Start task: research X"                      │
│  2. Review REVIEW-INBOX       → creates .task.md via ZimaOS API             │
│  3. Approve / connect stubs   "Status of project alpha?"                    │
│  4. Annotate sprint bundle    → ZimaBoard reads active_agents.json          │
│  5. Seed next sprint          → returns summary to chat                     │
└──────┬───────────────────────────────┬───────────────────────────────────────┘
       │ Syncthing P2P                 │ Syncthing P2P
       │ (LAN direct + ZeroTier WAN)  │
       ▼                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  ZIMABOARD — Stateless Memory & Coordination Layer                           │
│                                                                              │
│  Vault (6TB HDD) ← canonical copy; all Syncthing peers mirror from here     │
│                                                                              │
│  OpenClaw (Docker)                                                           │
│    • Scans 00-Inbox for new .task.md files                                  │
│    • Reads task metadata (priority, type, required skill)                   │
│    • Updates 03-Agents/active_agents.json to claim/track task               │
│    • Triggers agent_runner.sh on Workstation via SSH                        │
│    • Monitors 04-Projects / vault folders for completion signals            │
│    • Does NOT execute tasks — routes only                                   │
│                                                                              │
│  Firewall (UFW):                                                             │
│    INBOUND:  deny all except SSH:22 from human IP, Syncthing:21027/22000    │
│              from Workstation IP only                                        │
│    OUTBOUND: allow HTTPS (OpenClaw model fetch, Syncthing relays)           │
│                                                                              │
│  ZimaOS Chat backend:                                                        │
│    • Reads active_agents.json + latest 04-Projects files on query           │
│    • Creates .task.md in 00-Inbox on "start task:" commands                 │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │ Syncthing P2P (LAN primary, ZeroTier failover)
       │ + SSH (OpenClaw triggers agent_runner.sh)
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  WORKSTATION — Compute & Execution Layer (air-gapped)                        │
│                                                                              │
│  agent_runner.sh (daemon, WSL)                                               │
│    • Polls 00-Inbox for unclaimed tasks                                     │
│    • Claims atomically (temp+rename, prevents double-claim)                 │
│    • Calls context_builder.py (champagne pyramid)                           │
│    • Invokes: claude --print --model <model> < prompt                       │
│    • Signs outputs via hash_tracker.py                                      │
│    • Archives completed tasks to 99-Archives/                               │
│                                                                              │
│  Claude CLI (headless, WSL + NVM)                                           │
│    Simple task → single agent, reads/writes vault as CWD                   │
│    Complex task → team-builder spawns sub-team:                             │
│      orchestrator → researchers (haiku) → analysts (sonnet) → writers      │
│                                                                              │
│  Firewall (UFW):                                                             │
│    INBOUND:  deny all                                                        │
│    OUTBOUND: ZimaBoard IP, LLM API endpoints, DNS, NTP only                 │
└──────┬───────────────────────────────────────────────────────────────────────┘
       │ Syncthing P2P (optional, async)
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  COLLABORATOR WORKSTATION (optional, additional compute node)                │
│                                                                              │
│  Same agent_runner.sh + Claude CLI stack                                    │
│  Same vault sync (Syncthing from ZimaBoard)                                 │
│  Same trust model: egress-only, no inbound                                  │
│  Use case: parallel task execution, second team, async collaboration        │
└──────────────────────────────────────────────────────────────────────────────┘
                                │ Syncthing P2P
                                ▼
                    ┌───────────────────────────────────┐
                    │  Obsidian Vault (shared state)    │
                    │  canonical: ZimaBoard 6TB HDD     │
                    │                                   │
                    │  00-Inbox/     ← task queue       │
                    │  01-Memories/  ← agent memory     │
                    │  20-Entities/  ← entity stubs     │
                    │  30-Evidence/  ← evidence         │
                    │  40-Intelligence/ ← reports       │
                    │  99-Archives/  ← done tasks       │
                    └───────────────────────────────────┘
```

---

## Roles: ZimaBoard vs. Workstation

This split is the key to understanding the system. They do fundamentally different things.

| | ZimaBoard (OpenClaw) | Workstation (Claude CLI) |
|---|---|---|
| **Role** | Manager — routes, tracks, doesn't think | Worker — thinks, executes, produces |
| **Runs** | OpenClaw, Syncthing, ZimaOS Chat | agent_runner.sh, Claude CLI, hash_tracker |
| **Vault** | Canonical source (6TB HDD), always online | Mirror; syncs from ZimaBoard |
| **CPU need** | Minimal — file watching + routing only | High — LLM inference via API |
| **Network** | Inbound SSH (human only), Syncthing from WS | Outbound only: ZimaBoard + LLM APIs |
| **Fails safe** | Tasks queue in 00-Inbox until WS reconnects | Vault survives WS going offline |
| **Secrets** | None — routing only | API keys via env vars, not in vault |

**Why this split works:** The ZimaBoard stays always-on and lock-down-simple. The
Workstation does all the AI heavy lifting but is fully isolated — it can't be remotely
commanded by anything except the vault itself (Syncthing drops a file → agent_runner picks it up).

---

## Network Topology

```
Internet
   │
   │  (blocked by Workstation UFW — no inbound)
   │  (blocked by ZimaBoard UFW — SSH only from human IP)
   │
   ├─── ZimaBoard ◄──SSH:22─── Human IP only
   │         │
   │         │ ZeroTier VPN (LAN extension when not on same network)
   │         │ + Syncthing P2P direct (same LAN preferred)
   │         │
   │         ├─── Workstation (Syncthing:21027/22000 only)
   │         └─── Collaborator WS (same)
   │
   └─── LLM APIs (outbound from Workstation only: api.anthropic.com etc.)

Recommended: ZimaBoard + Workstation on dedicated VLAN
             (isolated from home/office network broadcast domain)
```

**Conflict resolution:** Agents always create new files with unique names
`{type}-{date}-{slug}-{session[:8]}.md`. Humans edit Review or Final versions,
not raw agent output. Syncthing creates `.sync-conflict` files on simultaneous
edits — these should be treated as human review items.

---

## Network Sync Strategy (Syncthing, not Git)

The live vault uses **Syncthing** (not Git) for these reasons:

| Concern | Syncthing | Git |
|---|---|---|
| Agent write speed | Near-instant, no staging | Commit overhead per write |
| Conflict handling | Auto `.sync-conflict` files | Manual merge required |
| Large files (6TB) | Efficient binary diff | Slow, bloats `.git` |
| Agent-friendliness | Simple file write, done | Requires commit + push |
| Security | P2P, no cloud credentials | SSH keys on every node |
| Version history | File versioning (optional) | Full history, but noisy |

**Archival:** `99-Archives/` is a candidate for a weekly Git snapshot on the
ZimaBoard for long-term versioned history of completed investigations.

**Publishing (optional):** Quartz or Flowershow can run as a separate Docker
container on ZimaBoard pointing at a **read-only snapshot** of the vault —
never the live sync folder. Publishing never interferes with agent operations.

---

## The Six Layers

### Layer 1 — Task Input

**Three paths to create a task:**

1. **Human in Obsidian** → QuickAdd macro → structured `.task.md` in `00-Inbox/`
2. **ZimaOS Chat** → "Start task: X" → ZimaBoard API creates `.task.md`
3. **Agent THREAD entry** → memory-keeper Phase 9 → `.task.md` stub in `00-Inbox/`

Task frontmatter: `priority: HIGH|MED|LOW`, `type:`, `tags:`, `web_tools: true` (opt-in),
optional `context_bundle: path/to/sprint-bundle/` (loads prior sprint as T2.5 context).

**OpenClaw sees the task first** (ZimaBoard). It logs the claim in `active_agents.json`
and signals the Workstation. `agent_runner.sh` then does the actual execution claim
(atomic prepend via temp+rename — prevents double-claim if both race).

---

### Layer 2 — Context Assembly (Champagne Pyramid)

`context_builder.py` assembles a calibrated prompt before every task:

```
T1  (~1K tok)   Mission + focus sections from AGENT-CONTEXT.md      ← always
T2  (~3K tok)   KB sections matching task keywords                  ← filtered
T2.5 (opt)      Sprint bundle forensics.md (if context_bundle: set) ← human-staged
T3  (~5K tok)   Entity stubs named in the task file                 ← matched
T4  (~2K tok)   HANDOFF MEM blocks from newest 2 handoff files      ← recency-capped
T5  (≤20K tok)  The task file itself                                ← always
Footer          COC path + run-log path + execution instructions    ← always
──────────────────────────────────────────────────────────────────────────────
~31K tokens assembled | ~169K breathing room for agent response
```

Agents get exactly the relevant slice of memory — not so little they hallucinate,
not so much they run out of context.

---

### Layer 3 — Execution (Agent + Team)

**Single-agent path:** `agent_runner.sh` → `claude --print` → vault writes + COC.

**Multi-agent path:** orchestrator spawns `team-builder`, which:
1. Assembles optimal team with model assignments (haiku for bulk, sonnet for analysis, opus for architecture)
2. Produces visual kickoff Mermaid diagram at session START
3. Coordinates step-by-step execution with shared scratchpad

**Each agent MUST:**
- Write FIRST IMPRESSIONS before touching any file (OBSERVATION entry to scratchpad)
- Log every file operation to `03-Agents/agent-logs/coc-{session}.md` (COC format)
- Append progress to run log `03-Agents/agent-logs/{session}-{task}.md`
- Write HANDOFF MEM entry at step boundary
- Write DONE entry to COC on completion

---

### Layer 4 — Memory (Three Scopes)

```
SESSION-SCOPED (.claude/memory/)      LOCAL (~/.claude/memory/)     VAULT (01-Memories/)
────────────────────────────────      ─────────────────────────     ────────────────────────────
scratch-{agent}-{session}.md          REVIEW-INBOX.md               agents/AGENT-CONTEXT.md
team-{session}.md                     KNOWLEDGE-BASE.md             agents/KNOWLEDGE-BASE.md
chain-{session}.md (COC)              scratchpad.jsonl              human/corrections.md
                                      improvement-proposals.md      shared/*.md (handoffs)
                                                                     00-Inbox/AGENT-REVIEW-INBOX.md
Cleared after sprint bundle sealed.   Human reviews locally.        Syncthing → all nodes.
```

**Memory promotion path (memory-keeper at /done):**
```
Agent MEM entry → scratchpad
                      ↓
              memory-keeper reviews
                      ↓
  FLAG/IDEA/PAIN    → REVIEW-INBOX        (human action queue)
  DECISION HIGH     → KNOWLEDGE-BASE      (validated facts)
  HEADLINE          → AGENT-REVIEW-INBOX  (potential story)
  CONNECTION        → entity stubs + 25-Networks/
  THREAD            → new .task.md in 00-Inbox  (seeds next sprint)
```

**KB validation gap:** Agents promote their own observations to KNOWLEDGE-BASE.
Until a `/kb-promote` human-approval flow is built, treat all KB entries as
`[UNVALIDATED]` unless explicitly marked `validated_by: human`.

---

### Layer 5 — Sprint Bundle + Human Review

At `/done`, the sprint is sealed as an immutable, signed evidence bundle:

```
.claude/sprints/{git-short}-{YYYYMMDD-HHMM}-{slug}/
├── README.md                ← key findings; how to challenge a conclusion
├── forensics.md             ← narrative; AGENT FLOW DIAGRAM (Mermaid, post-run);
│                               STEP-BY-STEP OUTPUT (per-agent bullets)
├── chain-of-custody.md      ← every file operation (READ/CREATE/MODIFY/EXEC/SPAWN)
├── memory/                  ← all scratchpads (per-agent + team + main)
├── outputs/                 ← copies of all vault files created this sprint
├── scripts/                 ← scripts used + hash_tracker.py copy
├── git-state.txt            ← git log + status at sprint end
├── snapshot.json            ← per-file SHA-256 + HMAC-SHA256 over manifest
└── snapshot.json.asc        ← GPG detached signature
```

**The bundle is a stage, not just an archive.** Human actions after the bundle:

| Human action | Mechanism | Effect on system |
|---|---|---|
| Approve finding | Edit entity stub `status: confirmed` | KB confidence upgrade |
| Make connection | Add `sibling:` links in entity stubs | 25-Networks/ update |
| Annotate sprint | Add `## Human Notes` to forensics.md | Read by next team if context_bundle: used |
| Reject / correct | Edit `01-Memories/human/corrections.md` | T5 in every future prompt |
| Seed next sprint | Create `.task.md` in `00-Inbox/` from OPEN QUESTIONS | Triggers next execution |
| Handoff to new team | Set `context_bundle:` in new task frontmatter | T2.5 tier in new team's prompt |
| Promote to KB | (manual now; `/kb-promote` planned) | Validated fact for all future agents |

---

### Layer 6 — Async Collaboration

Multiple compute nodes (workstations) can run simultaneously:

```
Human creates task → 00-Inbox (via Obsidian or ZimaOS Chat)
        ↓ Syncthing
ZimaBoard (OpenClaw sees it) → marks in active_agents.json → signals available WS
        ↓ Syncthing
Available Workstation (agent_runner.sh polls) → claims it → executes → pushes results
        ↓ Syncthing
Human sees new files in Obsidian → reviews → actions (see Layer 5)
```

**Conflict prevention rules:**
- Agents write **new unique files** (`{type}-{date}-{slug}-{session[:8]}.md`) — never overwrite
- Agents **append** to memory files (JSONL, scratchpads) — never overwrite
- `active_agents.json` written by Python read-modify-write (small file, low collision risk)
- Task claiming is atomic (temp+rename) — only one agent can claim a task

---

## Secrets Management

**Rule: No secrets in the vault. Ever.** Syncthing would distribute them to all nodes.

| Secret | Location | Access pattern |
|---|---|---|
| LLM API keys | WSL env: `~/.bashrc` or `~/.env.local` | `export ANTHROPIC_API_KEY=...` |
| GPG signing key | WSL GPG keyring (`~/.gnupg/`) | hash_tracker.py via `gpg` subprocess |
| GPG key config | `~/.pgp_keys/key_config.json` (WSL home) | NOT in vault |
| ZimaBoard SSH key | `~/.ssh/` (human machine) | SSH to ZimaBoard only |
| Syncthing device IDs | Syncthing config | Not secret but don't publish |

Use `pass` or `age` for any secrets that need to be accessible by scripts.

---

## Gaps and Open Design Questions

### Gap 1 — OpenClaw ↔ agent_runner.sh Integration
**Current state:** agent_runner.sh polls 00-Inbox independently. OpenClaw and agent_runner.sh
may both try to claim the same task.
**Design needed:** Decide authority: either OpenClaw is the sole claimer and SSH-triggers
agent_runner.sh with a specific task file, OR agent_runner.sh is the sole claimer and
OpenClaw is purely observational (reads active_agents.json). Current atomic claim logic
handles the race, but the authority model should be explicit.

### Gap 2 — No Human-Approval Gate for KNOWLEDGE-BASE
**Problem:** Agents promote observations to KB with no human sign-off.
**Design idea:** `/kb-promote` QuickAdd macro: marks checked REVIEW-INBOX items as
`confidence: HIGH, validated_by: human` and appends to KB.

### Gap 3 — Bundle as Next-Sprint Context (T2.5)
**Status:** Designed but not implemented in context_builder.py.
`context_bundle: path/to/bundle/` in task frontmatter should trigger T2.5 tier loading
the bundle's forensics.md (filtered to task keywords, capped at 3K tokens).

### Gap 4 — Team Handoff Protocol
**Design idea:** `/handoff-bundle` command writes `handoff.md` into bundle with:
what was found, what was NOT investigated, hypothesis confidence table, recommended
next team composition (models + agent types).

### Gap 5 — Hypothesis Tracker Not Auto-Updated
**Problem:** `Dashboards/Hypothesis-Tracker.md` exists; memory-keeper doesn't write to it.
**Fix:** Add to memory-keeper Phase 9: one-line entry per HEADLINE/CONNECTION promoted.

### Gap 6 — KB Compression (Summarizer Agent)
**Problem:** KNOWLEDGE-BASE.md and 01-Memories/ grow unbounded over time, degrading
T1/T2 context quality as the files get large.
**Design idea:** A weekly Summarizer Agent that: compresses old logbook entries into
`memory-summary-YYYY-MM.md`, prunes KB entries older than 90 days into an archive,
keeps active KB under ~5K tokens. Runs on ZimaBoard via cron (OpenClaw or crontab).

### Gap 7 — ZimaOS Chat → Vault Status Query
**Current state:** Not implemented. ZimaBoard can read active_agents.json and vault
files; ZimaOS Chat needs a backend script to parse and return status.
**Design idea:** A simple Python script `vault_status.py` that reads active_agents.json,
counts items by folder, returns a markdown summary. Triggered by ZimaOS Chat on query.

---

## Key Files Reference

| File | Node | Role |
|---|---|---|
| `00-Inbox/*.task.md` | Vault | Task queue; atomic claim by agent_runner.sh |
| `01-Memories/agents/AGENT-CONTEXT.md` | Vault | Steering doc; T1 in every prompt |
| `01-Memories/agents/KNOWLEDGE-BASE.md` | Vault | Validated facts; T2 source |
| `01-Memories/human/corrections.md` | Vault | Human overrides; T5 always included |
| `01-Memories/shared/*.md` | Vault | Handoff files; T4 source (newest 2) |
| `03-Agents/active_agents.json` | Vault | Live agent registry (OpenClaw + agent_runner) |
| `03-Agents/agent-logs/coc-{session}.md` | Vault | Chain of custody (every file op) |
| `03-Agents/agent-logs/{session}-{task}.md` | Vault | Run log (agent progress updates) |
| `scripts/agent_runner.sh` | Workstation | Vault inbox watcher daemon |
| `scripts/context_builder.py` | Workstation | Champagne pyramid context assembler |
| `00-Inbox/AGENT-REVIEW-INBOX.md` | Vault | Human review queue |
| `.claude/sprints/{hash}-{date}-{slug}/` | Workstation | Immutable signed sprint bundle |

---

## Design Principles

1. **Vault is the bus.** All agents read and write the same vault. No agent-to-agent
   direct communication — they communicate through vault files and the shared memory protocol.

2. **ZimaBoard manages, Workstation executes.** The ZimaBoard (OpenClaw) never thinks —
   it routes. The Workstation (Claude CLI) never manages — it executes. Clean separation
   means either can fail independently without taking down the other.

3. **Context is curated, not dumped.** The champagne pyramid prevents context bloat.
   Agents get exactly the relevant slice of memory for their task.

4. **Everything is traceable.** Chain of custody + sprint bundle + git hash = full
   provenance for any finding. "How did you reach this conclusion?" has a folder for an answer.

5. **Humans steer, agents execute.** AGENT-CONTEXT.md and corrections.md are human-written.
   Agents propose (REVIEW-INBOX); humans approve. This maintains epistemic integrity.

6. **Air-gapped by default.** Agents can only call external APIs if `web_tools: true`
   is set in the task. The vault is the world; the internet is an opt-in.

7. **Sprint bundles are stages, not archives.** A human-annotated bundle IS the context
   for the next sprint or team. `context_bundle:` in task frontmatter loads it as T2.5.

8. **No secrets in the vault.** Syncthing distributes everything. API keys, GPG keys,
   SSH keys live in env vars and OS keystores — never in vault files.
