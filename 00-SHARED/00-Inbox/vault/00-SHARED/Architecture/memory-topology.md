---
type: reference
status: active
tags: [architecture, memory, HONEY, NECTAR, pollen, topology]
parent: Architecture/INDEX
up: Architecture/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:bbecc63da0514f47fd6ba788346226da7c8bc24dc71613bde37382a0534cd88c
hash_ts: 2026-04-25T01:10:49Z
hash_method: body-sha256-v1
---

> [↑ Architecture](INDEX.md) · [⌂ Home](../../HOME.md)

# Memory Topology

Where things live, why they live there, and how they move between layers.

---

## The Four Layers

```
                    LIFESPAN                   PURPOSE
HONEY.md        ←  crystallized, ≤5K tokens   identity, universal methods
NECTAR.md       ←  append-only forever         validated findings across sessions
pollen          ←  ephemeral, one session      working observations during a session
forensics/      ←  immutable, hash-chained     artifacts and COC records
```

---

## Layer Details

### HONEY.md (≤5K tokens)

**What:** Crystallized knowledge. Dense. Hard-won.
**Where:** `~/.claude/HONEY.md` (global) + `{repo}/.claude/HONEY.md` (project)
**Mutates:** Only via `/crystallize` with human approval
**Read by:** Every agent at startup (global) or startup (project, read first)

Two-tier rule:
- Insight names entity / domain / investigation-specific? → **repo HONEY**
- Universal method true across ALL future projects? → **global HONEY** (gauntlet required)

---

### NECTAR.md (unbounded)

**What:** Validated findings. Append-only forever.
**Where:** `~/.claude/NECTAR.md`
**Mutates:** Append only. Never edited. Never compressed.
**Read by:** Agents at startup (tail-30), research agents when pattern-matching

Promotion path: pollen → `/handoff` → NECTAR (HIGH priority entries auto-promote).
Crystallization path: NECTAR → `/crystallize` → HONEY (recurrence ≥3 sessions).

---

### pollen (ephemeral)

**What:** Working observations during a session.
**Where:** `{repo}/.claude/memory/pollen-{SESSION_ID}.md`
**Mutates:** Append only during session. Promoted at `/handoff`.
**Read by:** Within-session only (agents emit to it, memory-keeper reads it at handoff)

Format: MEM blocks with category, priority, timestamp.

```markdown
<!-- MEM agent=data-engineer ts=2026-04-24T15:00Z session=abc123 cat=FINDING pri=MED av=baseline -->
**[FINDING]** Pipeline null pointer at task 079 — line 42 of ingest.py

Traced to missing null check on field `user_id`. Fix: add default empty string.

Files: scripts/ingest.py:42 | Next: write fix + test
<!-- /MEM -->
```

---

### forensics/ (immutable)

**What:** Permanent artifacts. Hash-chained. Git-tracked.
**Where:** `{repo}/forensics/`
**Mutates:** Append only. Never deleted (archive to `forensics/deletions/` with COC entry).
**Read by:** Agents via task_id grep only. Never browsed randomly.

---

## Write Routing

| Content type | Write to |
|---|---|
| Working observation | pollen MEM block |
| HIGH flag | pri=HIGH pollen block → auto-promotes to NECTAR at /handoff |
| Validated finding | memory-keeper promotes to NECTAR |
| Investigation-specific method | repo HONEY (via /crystallize + human approval) |
| Universal method/preference | global HONEY (gauntlet required) |
| Agent training | `~/.claude/agents/{type}.md` |
| Real-time insight | Vault Droplets/LIVE-{date}.md |

---

## Retrieval Protocol

Strong triggers (always read HONEY+NECTAR):
- User says "we used to..." or "remember when..."
- About to recommend X but the domain feels familiar
- Architectural decision territory (memory, piston, forensics, equilibrium)

Weak triggers (discipline required):
- Any domain word matches a MEMORY.md line
- User's tone shifts to correction ("no, that's not how...")
- 20+ turns without a memory read

---

## Budget Rules

| File | Token budget |
|------|-------------|
| Global HONEY.md | ≤5K tokens |
| Repo HONEY.md | ≤5K tokens |
| Agent cards | ≤800 tokens (≤1.2K if trained) |
| NECTAR.md | unbounded |
| pollen | ephemeral |

Check budget: `wc -c < file` / 4 before writing.

---

## Related

- [[forensic-integrity]] — how forensics/ is structured and protected
- [[../Hive/the-five-principles]] — artifacts-in-forensics (principle 2)
- [[../Skills-Reference/crystallize]] — /crystallize skill
- [[../Skills-Reference/handoff]] — /handoff skill (promotes pollen)
- [[../Glossary/terms]] — HONEY, NECTAR, pollen, COC defined
