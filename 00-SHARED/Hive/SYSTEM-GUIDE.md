---
type: system-guide
status: active
created: 2026-03-28
updated: 2026-03-28
tags:
  - system
  - guide
  - index
  - learning
  - architecture
aliases:
  - Learn the System
  - System TOC
  - How It Works
parent:
  - "[[_system-root]]"
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:85feec9f82d70cfb27ff3bb199ea51d44cfaa82eda6ecdbbf2859f25da972fb5
hash_ts: 2026-03-29T16:10:27Z
hash_method: body-sha256-v1
---

# Learn the System — Clickable Guide

Start here. Every concept links to its deep-dive doc. Read in order or jump to what matters.

---

## 1. Big Picture

| Concept | Doc | What you'll learn |
|---------|-----|-------------------|
| Full system map | [[System-Architecture]] | 7 Mermaid diagrams: piston, memory, forensics, faerie, data flow |
| Agent orchestration | [[AGENT-SYSTEM-ARCHITECTURE-ZIMA]] | Six layers, team composition, async collaboration |
| Pipeline end-to-end | [[PIPELINE-DESIGN]] | AUDIT/EXTRACT/TRANSFORM/DASHBOARD/REPORT/STAT/PUBLISH |
| DAE evolution story | [[DAE-Evolution-Narrative]] | How the tool got here — plugin to CLI to session bus |
| Modular architecture | [[15-MODULAR-SECRET-SAUCE]] | Paid features as removable scripts, graceful degradation |
| Marketing angle | [[MARKETING-IDEAS]] | How to position this for employers and users |

---

## 2. Session Lifecycle

The system runs in sessions. Each session: `/faerie` (start) → work → `/handoff` (end).

| Phase | Doc | What happens |
|-------|-----|-------------|
| Session START | [[faerie-start]] | Orient from handoff, read HONEY, launch agents |
| Agent work | [[agent-work]] | Subagents execute tasks in 200K context windows |
| Subagent spawning | [[subagent-spawning]] | How agents are routed, typed, launched |
| Context phases | [[context-budget]] | LIFTOFF → ORBIT → DEORBIT → REENTRY |
| Session END | [[handoff-end]] | Crystallize, queue threads, write brief |
| Emergency handoff | [[emergency-handoff]] | Mechanical roundup when session drops |
| Handoff snapshot | [[handoff-snapshot]] | JSON artifact that cold-starts next session |

---

## 3. The Piston Engine (Agent Wave Rhythm)

| Concept | Doc | What you'll learn |
|---------|-----|-------------------|
| Piston model design | [[PISTON-MODEL-DESIGN]] | Problem, solution, wave timing, relaunch cycle |
| System architecture diagrams | [[System-Architecture#The Piston Session Engine]] | Visual wave flow |
| Session lifecycle visual | [[System-Architecture#Session Lifecycle]] | How compact/resume fits |
| Modular sauce | [[15-MODULAR-SECRET-SAUCE#The Pattern]] | How piston.py imports work |

---

## 4. Memory Architecture

Three layers: working (session), durable (cross-session), forensic (immutable).

| Layer | Doc | Purpose |
|-------|-----|---------|
| Scratch (working) | [[scratch-working]] | Per-session MEM blocks, gitignored |
| HONEY (preferences) | [[honey-seed]] | Crystallized prefs/methods, earned through time |
| NECTAR (findings) | [[nectar-narrative]] | Validated findings, append-only, never compress |
| REVIEW-INBOX | [[review-inbox]] | HIGH flags queued for human review |
| Memory flow diagram | [[13-MEMORY-FLOW-ARCHITECTURE]] | Full Mermaid flow: scratch → NECTAR → HONEY |
| Crystallization cycle | [[crystallization]] | How knowledge gets denser (not shorter) |
| Equilibrium principle | [[equilibrium]] | Token budgets, over-budget = crystallize first |
| Debloat cycle | [[debloat-cycle]] | Mechanical pre-pass before LLM crystallization |

---

## 5. Forensics & Integrity

Agents can WRITE to forensics (via hooks) but NEVER READ. This ensures COC can't influence analysis.

| Concept | Doc | What you'll learn |
|---------|-----|-------------------|
| Forensic layer | [[forensic-layer]] | Agent-blind write-only architecture |
| COC hash chains | [[coc-hash-chain]] | HMAC-SHA256 signed, hash-chained entries |
| Hash integrity | [[hash-integrity]] | Pre/post hashing for every operation |
| How annotation COC works | [[HOW-ANNOTATION-COC-WORKS]] | Signing, receipts, scientific rigor |
| Forensics isolation visual | [[System-Architecture#Forensics Isolation Architecture]] | Deny rules, per-repo layout |

---

## 6. Agent System

| Concept | Doc | What you'll learn |
|---------|-----|-------------------|
| Agent layer | [[agent-layer]] | 20+ specialized types, fresh 200K each |
| Agent cards | [[agent-cards]] | Per-type identity, KPIs, training scores |
| OTJ learning | [[otj-learning]] | Agents improve themselves after each run |
| Agent outbox | [[agent-outbox]] | Where agents write findings (never 30-Evidence/) |
| Human promotes | [[09-HUMAN-PROMOTES-AI-EXECUTES]] | Agent-outbox → human review → evidence |
| Human evidence | [[human-evidence]] | What goes in 30-Evidence/ (human only) |
| Agent adaptive context | [[08-AGENT-ADAPTIVE-CONTEXT-AND-EVOLVING-PROMPT]] | How prompts evolve with learning |
| Faerie A/B impact | [[11-FAERIE-IMPACT-AB]] | Measured difference faerie makes |

---

## 7. Queue & Sprint System

| Concept | Doc | What you'll learn |
|---------|-----|-------------------|
| Sprint queue | [[sprint-queue]] | Task lifecycle: queued → claimed → done |
| Task lineage | [[10-TASK-LINEAGE-AND-HANDBACK]] | Parent/child/sibling task linking |
| State engine | [[state-engine]] | How state files coordinate everything |
| Brief atoms | [[brief-atoms]] | Atomized session briefs (not monolithic files) |

---

## 8. Vault & Obsidian Integration

The vault is the human-readable interface. Repos are canonical. Vault = message bus.

| Concept | Doc | What you'll learn |
|---------|-----|-------------------|
| Vault layer | [[vault-layer]] | Folder routing, what goes where |
| Vault schema | [[VAULT-SCHEMA]] | Full folder structure with owners |
| Async bridge | [[12-ASYNC-HUMAN-AGENT-BRIDGE]] | One note, two audiences (human + agent) |
| Annotation flow | [[annotation-flow]] | Human annotations → agent pickup |
| Sync mechanism | [[HOW-SYNC-WORKS]] | Syncthing, not git |
| Frontmatter + wikilinks | [[FRONTMATTER-WIKILINKS]] | YAML schema for Obsidian notes |
| Agent-Obsidian integration | [[AGENT-OBSIDIAN-INTEGRATION]] | How agents interact with the vault |

---

## 9. Design Philosophy

| Concept | Doc | What you'll learn |
|---------|-----|-------------------|
| Equilibrium | [[equilibrium]] | Every output balances an input |
| Chain of consciousness | [[13-CHAIN-OF-CONSCIOUSNESS-2026-03-27]] | Why the best thinking happens at context edges |
| Buddhist philosophy | [[14-BUDDHIST-PHILOSOPHY-AND-SYSTEM-DESIGN]] | Impermanence, emergence, middle way in system design |
| Original design narrative | [[00-DESIGN-NARRATIVE-2026-03-22]] | How the system was conceived |
| Kickstart collab | [[KICKSTART-COLLAB]] | How to onboard a new collaborator |

---

## 10. Modular Architecture (Paid Tier)

| Concept | Doc | What you'll learn |
|---------|-----|-------------------|
| Secret sauce strategy | [[15-MODULAR-SECRET-SAUCE]] | Why, what, how of removable modules |
| Pain point → sauce mapping | [[System-Architecture#Modular Secret Sauce Paid Feature Architecture]] | Visual: which scripts fix which pain points |
| Removal protocol | [[15-MODULAR-SECRET-SAUCE#How Removal Works]] | Exact commands to strip sauce |
| Implementation status | [[15-MODULAR-SECRET-SAUCE#Implementation Status]] | What's modularized vs pending |
| DAE release path | [[DAE-Evolution-Narrative]] | How DAE ships standalone |

---

## Pseudosystem Component Index

Every system component has a dedicated note with ExcaliBrain metadata (parent/child/sibling links, color, concurrency).

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Component",
  component_type AS "Type",
  status AS "Status"
FROM "00-SHARED/Hive/pseudosystem"
WHERE type = "system-component"
SORT component_type ASC, file.name ASC
```

---

## Design Docs (Hive)

All system design docs, narratives, and guides in this folder.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Doc",
  type AS "Type",
  default(status, "—") AS "Status",
  dateformat(default(updated, created), "yyyy-MM-dd") AS "Updated"
FROM "00-SHARED/Hive"
WHERE file.name != "SYSTEM-GUIDE"
  AND !contains(file.folder, "pseudosystem")
  AND !contains(file.folder, "honey-dev")
  AND !contains(file.folder, "collected-memories")
  AND !contains(file.folder, "Color")
  AND !contains(file.folder, "system-changes")
  AND file.name != "_index"
SORT default(updated, created) DESC
```

---

## State Files & Rules (System Reference)

```dataview
LIST
FROM "00-SHARED/Hive"
WHERE type = "system-guide" OR type = "system-doc"
SORT file.name ASC
```
