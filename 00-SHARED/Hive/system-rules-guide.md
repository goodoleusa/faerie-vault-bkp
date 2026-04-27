---
type: system-guide
status: current
created: 2026-03-27
updated: 2026-03-27
tags:
  - system
  - rules
  - guide
  - human-readable
  - faerie
parent:
  - "[[00-SHARED]]"
  - "[[AGENT-SYSTEM-ARCHITECTURE-ZIMA]]"
sibling:
  - "[[HOW-ANNOTATION-COC-WORKS]]"
  - "[[HOW-SYNC-WORKS]]"
child:
  - "[[system-memory-guide]]"
  - "[[system-agents-guide]]"
  - "[[system-vault-safety-guide]]"
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:49109c4208873bc75356f20ea88d8a143741874f07952a559f72726dfd43d3aa
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# How the Faerie System Works (Human-Readable Guide)

This document explains the rules that govern how Claude agents operate in this investigation environment. The actual system files are terse for token efficiency — this is the expanded, human-friendly version.

---

## Memory: Where Knowledge Lives

The system has a **three-tier memory hierarchy**, like how your brain works:

### HONEY.md — The Seed Memory (≤200 lines)
Location: `C:\Users\amand\.claude\memory\HONEY.md`

This is the **crystallized essence** of everything the system knows about how to work well. Every agent reads it at startup. It contains preferences, methods, environment details, and hard-won insights. Think of it as the "personality and skills" file.

**Crystallization** is key: when new knowledge arrives, it doesn't just get appended. It gets *integrated* — merged with related entries, contradictions resolved, cross-references formed. The file gets shorter but the knowledge gets deeper. Like forming a crystal from solution: more ordered, more dense, more useful.

### NECTAR.md — The Investigation Record (unbounded)
Location: `C:\Users\amand\.claude\memory\NECTAR.md`

This is the **append-only forensic truth**. Validated findings, confirmed connections, sprint summaries. It never gets compressed or crystallized — that would be evidence tampering. New entries accumulate. Agents read the tail (most recent entries) for investigation context.

### Scratch Files — Working Notes (per-session)
Location: `{repo}\.claude\memory\scratch-{session-id}.md`

Temporary working notes during a session. Agents write observations, flags, ideas here using `<!-- MEM -->` blocks. At session end, a memory-keeper agent reviews scratch and promotes valuable items to NECTAR (findings) or HONEY (methods).

### REVIEW-INBOX.md — Human Attention Queue
Location: `C:\Users\amand\.claude\memory\REVIEW-INBOX.md`

When agents find something that needs human eyes — a HIGH-priority flag, a smoking gun, a decision point — it goes here. This is your "things to look at" queue. Agents only append, never remove.

---

## Agents: How They Learn

Each agent type (data-scientist, evidence-curator, research-analyst, etc.) has an **agent card** at `C:\Users\amand\.claude\agents\{type}.md`. This card contains:

- **Role definition** — what the agent does
- **KPIs** — how to measure success
- **Last Training** — when it last improved, what it learned

### On-the-Job Learning (OTJ)
Every agent, every run, spends ~2K tokens reflecting: What worked? What was harder than expected? What would I do differently? This reflection writes to scratch memory, and if the agent demonstrably improved, it updates its own card.

**Critical rule**: Agent cards contain ONLY process/methodology learnings. Never case-specific data. This is a **legal requirement** — if a defense attorney could argue "this learning biased the analysis," it doesn't belong in the card. Case-specific observations go to NECTAR.

### Two Score Tracks
- **Training score** — performance on controlled drills (artificial)
- **Deployment score** — performance on real work (the true test)
A training score of 1.0 doesn't mean the agent peaked — it means the drill was easy.

---

## Forensic Integrity: Court-Grade Provenance

### Chain of Custody (COC)
Every finding links immutably to the agent state that produced it. COC logs record: session ID, agent type, agent version, tool calls, timestamps, and a hash chain where each entry's hash includes the previous entry's hash. This proves in court: "Finding F was produced at time T by agent version V."

The `forensic_coc.py` hook logs automatically after every tool use. Agents can WRITE to forensic logs but never READ them — this prevents forensic records from influencing future analysis.

### Hash Integrity
Before moving any `.claude` or forensic artifact: hash it. After moving: hash again. `hash_tracker.py` takes directory-level snapshots. `emergency_handoff.py` computes per-file SHA256 inline. Belt + suspenders.

### Three-Layer Separation
1. **COC layer** (`forensics/`) — immutable, hash-chained, agents write-only
2. **Human layer** (vault `30-Evidence/`, `## Your Annotations`) — agents never touch
3. **Narrative layer** (NECTAR/HONEY/atoms) — agents write JSON, Blueprints render human-readable

---

## Session Lifecycle

### /faerie — Session START
1. Reads the latest handoff snapshot (one file replaces 15 scattered reads)
2. Reads HONEY.md (preferences, methods)
3. Checks the task queue
4. Launches HIGH-priority tasks immediately
5. Shows a 10-line dashboard

### /handoff — Session END
1. **Step Zero** (mandatory, ~1.5 seconds): Fires `emergency_handoff.py` — collects all splintered memories, writes durable snapshot files
2. Graceful steps (if context permits): Promote flags, write to NECTAR, crystallize HONEY, queue threads, spawn memory-keeper
3. Even if only Step Zero runs, next `/faerie` has everything it needs

### Emergency Resilience
At 1% context, `/handoff` fires Step Zero only — a Python script that runs in <2 seconds, no LLM inference needed. The script writes `handoff-snapshot.json` + `faerie-brief.json`. These survive auto-compact. Next session starts clean.

---

## The Vault: Human-Readable Mirror

The Obsidian vault (`CyberOps-UNIFIED/`) is the human-facing view of investigation work.

### Two-Stage Finding Architecture
1. **Agent drafts** go to `00-SHARED/Agent-Outbox/` — agents write here freely
2. **Human promotes** to `30-Evidence/` after review — agents never see this folder

This permission boundary is the enforcement. Agents draft findings; humans validate and annotate them.

### Folder Map
| What | Where |
|---|---|
| Findings (human-validated) | `30-Evidence/` |
| Investigation narrative | `10-Investigations/` |
| Entity profiles | `20-Entities/` |
| Timeline | `60-Chronology/` |
| Agent drafts | `00-SHARED/Agent-Outbox/` |
| Human review queue | `00-SHARED/Human-Inbox/` |
| Shared knowledge | `00-SHARED/Hive/` |

### Annotation Flow
Agents write drafts → Human reviews in Obsidian → Human annotates (`## Your Annotations`, `## Court Prep Notes`) → Annotations are sacred, agents never touch them.

---

## State Files: Where the System Tracks Itself

All state files live at `C:\Users\amand\.claude\hooks\state\`:

| File | Purpose | Updated by |
|---|---|---|
| `handoff-snapshot.json` | Complete memory roundup (~700KB) | emergency_handoff.py |
| `faerie-brief.json` | Lightweight cold-start pointer | emergency_handoff.py, session_stop_hook |
| `sprint-queue.json` | Task queue with priorities | queue_ops.py |
| `brief-atoms/` | Accumulating checkpoint history | emergency_handoff.py, briefgen.py |
| `handoff-checkpoint.json` | Resumability after auto-compact | emergency_handoff.py |
| `memory-collection-coc.jsonl` | Hash-chained COC for memory ops | emergency_handoff.py |
| `pending-hash-snapshot.json` | Deferred hash work for next /faerie | emergency_handoff.py |
| `run-benchmarks.json` | Agent performance KPIs | performance-eval |
| `subagent-options.json` | Agent type → team routing | manual + train |

---

## Component Mapping to Standard Patterns

If you're familiar with software engineering, here's how this maps:

| Our Component | Standard Pattern |
|---|---|
| `/faerie` | CI/CD workflow dispatch (GitHub Actions) |
| HONEY/NECTAR/scratch | Tiered knowledge store (RAG with promotion) |
| `/data-ingest` | ETL pipeline (Airflow DAGs) |
| `/handoff` + emergency script | Checkpoint/restart (K8s job checkpointing) |
| Agent cards + OTJ learning | Model registry (MLflow) |
| sprint-queue.json | Task queue (Celery/Redis) |
| Atomized briefs | Event sourcing |
| COC/forensics | SIEM audit logging |
| Obsidian vault | CMS + annotation layer |
| emergency_handoff.py | Circuit breaker pattern |

---

## Budget System

Every durable file has a token budget to prevent context bloat:

| File | Budget | Why |
|---|---|---|
| Rules (all) | 300 lines | Loaded every session, directly eats context |
| HONEY.md | 200 lines | Core seed memory, must stay focused |
| Agent cards | 80 lines (120 trained) | Each card read by its agent type |
| CLAUDE.md | 30 lines | Top-level project instructions |
| NECTAR.md | Unbounded | Forensic truth, never compress |
| REVIEW-INBOX | Unbounded | Append-only human attention queue |

When a file exceeds budget, it must be **crystallized** (not just compressed) before adding new content. Crystallization is LLM work — it integrates, deduplicates, and enriches.

---

*This guide was generated from the system rule files on 2026-03-27. The authoritative versions are the rule files themselves — this is the human-friendly explanation.*
