---
type: index
status: active
created: 2026-03-28
updated: 2026-03-29
tags:
  - blueprints
  - index
  - reference
doc_hash: sha256:8131c961669b53b90d7f7e1f73b48160baa3823f0a228ef90ec60dac777ab7c4
hash_ts: 2026-03-29T16:16:46Z
hash_method: body-sha256-v1
---

# Blueprints

Obsidian Blueprints (`.blueprint` files) are applied to existing notes to add structured sections. Unlike Templates (which create new notes), Blueprints augment notes that already exist.

For Templater templates (`.md` files for creating new notes), see [[Templates/_index|Templates Index]].

---

## Entity Blueprints

Applied to entity notes in `20-Entities/`.

| Blueprint | Purpose |
|---|---|
| [[Blueprints/Entity-Stub.blueprint\|Entity-Stub]] | Generic entity structure |
| [[Blueprints/Person.blueprint\|Person]] | Person profile sections |
| [[Blueprints/Organization.blueprint\|Organization]] | Standard organization profile |
| [[Blueprints/Organization-Master.blueprint\|Organization-Master]] | Extended organization with BITE model, HCG sections |
| [[Blueprints/Domain.blueprint\|Domain]] | Domain entity with DNS, SSL, WHOIS |
| [[Blueprints/IP-Address.blueprint\|IP-Address]] | IP address with network info, ports, certificates |
| [[Blueprints/Threat-Actor.blueprint\|Threat-Actor]] | Threat actor profile |
| [[Blueprints/Network-Map.blueprint\|Network-Map]] | Network map visualization |
| [[Blueprints/High-Control-Group.blueprint\|High-Control-Group]] | High-control group analysis (BITE model) |
| [[Blueprints/Financial-Trail.blueprint\|Financial-Trail]] | Financial trail and transaction tracking |
| [[Blueprints/Shadow-Operation.blueprint\|Shadow-Operation]] | Covert/shadow operation documentation |

## Evidence & Findings Blueprints

Applied to evidence notes and agent-generated findings.

| Blueprint | Purpose |
|---|---|
| [[Blueprints/Evidence-Item.blueprint\|Evidence-Item]] | Full evidence item with provenance and hypothesis relevance |
| [[Blueprints/Finding-Review.blueprint\|Finding-Review]] | Human review sections for agent-drafted findings |
| [[Blueprints/Flag-Review.blueprint\|Flag-Review]] | Human review sections for agent-flagged items |
| [[Blueprints/Source-Assessment.blueprint\|Source-Assessment]] | Source reliability and quality rating |

## Investigation & Reporting Blueprints

Applied to investigation cases and reports.

| Blueprint | Purpose |
|---|---|
| [[Blueprints/Investigation-Case.blueprint\|Investigation-Case]] | Full investigation case structure |
| [[Blueprints/Intelligence-Report.blueprint\|Intelligence-Report]] | Intelligence report structure |
| [[Blueprints/Chronology-Entry.blueprint\|Chronology-Entry]] | Timeline/chronology entry |
| [[Blueprints/Phase-Narrative.blueprint\|Phase-Narrative]] | Phase narrative for pipeline runs (data ingest tracking) |
| [[Blueprints/Research-Brief.blueprint\|Research-Brief]] | Research brief structure |

## Agent & System Blueprints

Applied to agent workflow notes and system documentation.

| Blueprint | Purpose |
|---|---|
| [[Blueprints/Agent-Skill.blueprint\|Agent-Skill]] | Agent skill definition |
| [[Blueprints/Agent-Training-Event.blueprint\|Agent-Training-Event]] | Agent training event record |
| [[Blueprints/Context-Bundle.blueprint\|Context-Bundle]] | Context bundle for agent handoff |
| [[Blueprints/Session-Handoff.blueprint\|Session-Handoff]] | Session handoff record |
| [[Blueprints/Session-Manifest.blueprint\|Session-Manifest]] | Session manifest structure |
| [[Blueprints/Brief-Assembly.blueprint\|Brief-Assembly]] | Brief assembly for faerie session briefs |
| [[Blueprints/Task-Inbox.blueprint\|Task-Inbox]] | Task structure for inbox items |
| [[Blueprints/Task-Claim.blueprint\|Task-Claim]] | Task claim sections (agent claiming work) |
| [[Blueprints/Gate-Review.blueprint\|Gate-Review]] | Pipeline gate review checklist |

## Collaboration & Communication Blueprints

Applied to notes used for human-agent collaboration.

| Blueprint | Purpose |
|---|---|
| [[Blueprints/Annotation-Commit.blueprint\|Annotation-Commit]] | Annotation commit record with hash chain |
| [[Blueprints/Collab-Export.blueprint\|Collab-Export]] | Collaboration export for sharing |
| [[Blueprints/Observer-Drop.blueprint\|Observer-Drop]] | Observer drop (async communication) |
| [[Blueprints/Dead-Drop.blueprint\|Dead-Drop]] | Dead drop (anonymous async communication) |
| [[Blueprints/NECTAR-Entry.blueprint\|NECTAR-Entry]] | NECTAR finding entry |
| [[Blueprints/Human-Annotation.blueprint\|Human-Annotation]] | Human annotation record linked to source notes |

## Documentation Blueprints

Applied to system documentation and design notes.

| Blueprint | Purpose |
|---|---|
| [[Blueprints/System-Design.blueprint\|System-Design]] | System design document structure |
| [[Blueprints/TechDoc.blueprint\|TechDoc]] | Technical documentation structure |
| [[Blueprints/Faerie-Brief.blueprint\|Faerie-Brief]] | Faerie session brief generation |

## Utility Blueprints

| Blueprint | Purpose |
|---|---|
| [[Blueprints/Daily-Research.blueprint\|Daily-Research]] | Daily research log sections |
| [[Blueprints/Memory-Entry.blueprint\|Memory-Entry]] | Memory entry (MEM block) structure |
| [[Blueprints/Normalize-Frontmatter.blueprint\|Normalize-Frontmatter]] | Normalize frontmatter fields across notes |
| [[Blueprints/Thread.blueprint\|Thread]] | Investigation thread tracking |

---

## How to Use

1. Open an existing note in Obsidian
2. Run the Blueprints plugin command (`Ctrl+Shift+P` > "Blueprints: Apply")
3. Select the appropriate blueprint from the list
4. The blueprint adds structured sections to the note without overwriting existing content

## Investigation Setup

All blueprints are investigation-agnostic. When starting a new investigation:

- `chain_id` fields are blank — agents fill these at note creation from the investigation config
- `investigation_id` fields are blank — fill from your `investigation.json` / ARCHITECTURE.md
- Hypothesis tables use generic `H1 — *(your hypothesis)*` placeholders — replace with your actual hypotheses
- The `chain_id` for all notes should match your investigation's identifier (set in `~/.claude/memory/HONEY.md` env section)
