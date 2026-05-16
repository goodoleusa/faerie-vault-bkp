---
type: reference
status: active
created: 2026-04-21
tags: [forensics, write-locations, paths]
up: README.md
prev: FORENSIC-SYSTEM-INDEX.md
---

> [↑ Readme](README.md) · [← Forensic System Index](FORENSIC-SYSTEM-INDEX.md) · [⌂ Home](../../README.md)

# Canonical Write Locations — Single Source of Truth

**Date:** 2026-04-07  
**Audience:** All agents, developers, architects  
**Purpose:** Definitive routing for all durable file writes  

---

## Core Principle

**One writer per file. Multiple readers.**

Every durable file has exactly one canonical owner. Secondary copies may exist (vault mirror, local scratch), but writes go to the canonical location only.

---

## Canonical Locations by File Type

### Forensic Chain of Custody

| File | Canonical Location | Owner | Read By | Frequency |
|------|---|---|---|---|
| COC entries | `{repo}/forensics/coc.jsonl` | faerie + membot | faerie (narrative), legal (export) | Append-only, ~1/phase |
| Audit log | `{repo}/forensics/audit-log.md` | data-engineer | faerie, legal | Append-only, per ingest |
| Genesis manifest | `{repo}/forensics/manifests/genesis_manifest.json` | system (once) | evidence-curator, security-auditor | Read-only (baseline) |
| Rawdata manifests | `{repo}/forensics/manifests/rawdata_manifest_{RUN}.json` | data-engineer | evidence-curator, data-scientist | Append per ingest |
| Evidence manifest | `{repo}/forensics/manifests/evidence_manifest.json` | data-engineer | all agents | Updated per ingest |

**Key rule:** Never modify files in `forensics/`. Only append to `coc.jsonl` and `audit-log.md`. Create new manifest files per run (versioned).

### Memory & Knowledge Base

| File | Canonical Location | Owner | Read By | Frequency |
|------|---|---|---|---|
| NECTAR | `~/.claude/memory/NECTAR.md` | memory-keeper | faerie, agents, humans | Append-only, per sprint |
| HONEY | `~/.claude/memory/HONEY.md` | faerie (crystallize) | all agents (startup) | Update per crystallization |
| HONEY (project) | `{repo}/.claude/memory/HONEY.md` | faerie (rare) | agents in this project | Read-only, accretes slowly |
| REVIEW-INBOX | `~/.claude/memory/REVIEW-INBOX.md` | agents (HIGH flags) | humans, faerie | Append-only, per flag |

**Key rule:** NECTAR and REVIEW-INBOX are append-only forever. HONEY is crystallized (compressed + contextualized) — never accumulate, integrate.

### Session & Investigation State

| File | Canonical Location | Owner | Read By | Frequency |
|------|---|---|---|---|
| Reasoning log | `~/.claude/memory/investigations/{inv_id}/reasoning.jsonl` | agents (all) | data-scientist, faerie | Append-only, per agent run |
| Transforms log | `~/.claude/memory/investigations/{inv_id}/transforms.jsonl` | data-engineer | faerie (lineage) | Append-only, per phase |
| Master COC | `~/.claude/memory/investigations/{inv_id}/forensics/master-coc.jsonl` | faerie (consolidated) | legal (export) | Append-only, per session |

**Key rule:** Investigation-level logs are append-only and never read by agents (prevents feedback loops). Only faerie and downstream (legal, audit) consume them.

### Agent Cards & Skills

| File | Canonical Location | Owner | Read By | Frequency |
|------|---|---|---|---|
| Agent card | `~/.claude/agents/{type}.md` | agent (self-update on OTJ beat) | faerie, that agent | Update only on improvement |
| Skill definition | `~/.claude/skills/{skill}/SKILL.md` | skill maintainer | faerie (load), agents (learn) | Rare updates |
| System rules | `~/.claude/rules/*.md` | humans (via PR) | all agents (Step Zero) | Rare updates |

**Key rule:** Agent cards are updated only when an agent beats its baseline score with durable learning. Skill files are updated by maintainers via PR. System rules are updated by consensus.

### Investigation Artifacts

| File | Canonical Location | Owner | Read By | Frequency |
|------|---|---|---|---|
| Evidence export | `{repo}/forensics/exports/evidence_export_{TS}.tar.gz` | system | legal, auditors, courts | Once per investigation phase |
| Vault docs | `$CT_VAULT/00-SHARED/Design-Narratives/{inv_id}/` | faerie + agents | humans, other agents | Per-document updates |
| Scratch (session) | `{repo}/.claude/memory/pollen-{SID}.md` | agent (working notes) | memory-keeper (promotion) | Ephemeral, per session |
| Scratch (project) | `{repo}/.claude/memory/scratch-{SID}.md` | agent (working notes) | memory-keeper (promotion) | Ephemeral, per session |

**Key rule:** Exports are immutable once generated (signed + B2 WORM). Vault docs are synced mirrors (not canonical — forensics/ is canonical). Scratch is ephemeral and gitignored.

---

## Write Routing Decision Tree

When an agent or process needs to write something durable:

```
1. Is it a forensic event (ingest, promote, crystallize)?
   → Write to {repo}/forensics/coc.jsonl (append-only)
   → Write to {repo}/forensics/audit-log.md (append-only)
   DONE

2. Is it evidence or manifest data?
   → Write to {repo}/forensics/manifests/{name}_{VERSION}.json
   → Reference in coc.jsonl
   DONE

3. Is it a finding or observation (working hypothesis)?
   → Write to {repo}/.claude/memory/pollen-{SID}.md (scratch, ephemeral)
   → Append <!-- MEM --> block
   DONE (wait for memory-keeper promotion)

4. Is it a validated finding (promoted from scratch)?
   → memory-keeper writes to ~/.claude/memory/NECTAR.md (append-only)
   → Create COC entry: type=promote
   DONE

5. Is it crystallized knowledge (durable, permanent)?
   → faerie writes to ~/.claude/memory/HONEY.md
   → Create COC entry: type=crystallize
   DONE

6. Is it a HIGH priority flag?
   → Agent writes to ~/.claude/memory/REVIEW-INBOX.md (append-only)
   → Also writes to vault: 00-SHARED/Human-Inbox/flags/
   DONE (human acts on it)

7. Is it an agent self-improvement (beat baseline)?
   → Agent updates ~/.claude/agents/{type}.md "## Last Training" section
   → Append to ~/.claude/hooks/state/training-log.jsonl
   DONE

8. Is it a memory promotion or session bookkeeping?
   → memory-keeper writes to ~/.claude/memory/NECTAR.md
   → faerie writes to ~/.claude/hooks/state/ (state files)
   DONE
```

---

## Anti-Patterns (Do NOT Do These)

| Anti-Pattern | Problem | Correct Way |
|---|---|---|
| Write to `.claude/projects/*/memory/MEMORY.md` | Fragments knowledge across paths | Write to canonical locations only (NECTAR, HONEY, REVIEW-INBOX) |
| Modify `forensics/coc.jsonl` entries | Breaks hash chain, evidence is compromised | Append only, never edit |
| Overwrite manifest files | Loses baseline, prevents replayability | Create new versioned manifest: `rawdata_manifest_{RUN}.json` |
| Write to HONEY.md without crystallizing | Accumulates noise, budget bloat | Read all related entries, integrate, compress |
| Scatter memory files in project root | Fragmentation, agents can't find them | Use canonical paths: `~/.claude/memory/`, `{repo}/.claude/memory/` |
| Delete from REVIEW-INBOX | Hides flags from human review | Append-only forever; move to archive if needed |
| Write to reasoning.jsonl from non-agents | Contaminates forensic record | Only agents write; faerie reads for narrative |

---

## Migration & Cleanup

### Old Files to Sunset

If you find files in non-canonical locations:

| Found Location | Canonical Location | Action |
|---|---|---|
| `{repo}/.claude/AGENTS.md` | `~/.claude/memory/HONEY.md` + `~/.claude/memory/NECTAR.md` | Crystallize findings to HONEY, narrative to NECTAR, delete |
| `{repo}/.claude/memory/KNOWLEDGE-BASE.md` | `~/.claude/memory/NECTAR.md` | Merge entries, delete |
| Scattered `docs/*.md` with memory | `~/.claude/memory/HONEY.md` (durable) or `~/.claude/memory/NECTAR.md` (findings) | Integrate, delete |
| `.claude/projects/*/memory/` | Canonical locations (see routing above) | Re-write to canonical, delete fragment folder |

### Migration Checklist

- [ ] Identify all non-canonical memory files (grep, ls, audit)
- [ ] For each: determine if it's durable (HONEY) or narrative (NECTAR)
- [ ] Migrate content to canonical location
- [ ] Update git: `git rm` old file
- [ ] Commit: `git commit -m "refactor: migrate memory to canonical locations"`
- [ ] Verify: all agents can find memory at startup

---

## Subagent Write Restrictions (Sandboxing)

**Important:** Subagents spawned via `Agent` tool have restricted Write access to `~/.claude/` paths.

**Pattern for subagents:**

```
SUBAGENT WORK:
1. Read files from canonical locations
2. Analyze, compute, produce changes
3. Return changes as JSON structure (patches)

PARENT SESSION:
1. Receives patches from subagent
2. Applies patches via Bash subprocess (Python inline script)
3. Writes to canonical locations (Bash has unrestricted access)
```

See `~/.claude/rules/subagent-write-protocol.md` for full protocol.

---

## Verification Checklist

Before committing any session's work:

- [ ] All forensic events recorded in `{repo}/forensics/coc.jsonl`
- [ ] All audit actions in `{repo}/forensics/audit-log.md`
- [ ] All findings promoted from scratch to NECTAR
- [ ] All durable knowledge integrated into HONEY
- [ ] All HIGH flags in `~/.claude/memory/REVIEW-INBOX.md`
- [ ] No scattered memory files in project root
- [ ] No overwritten files in `forensics/`
- [ ] All manifests versioned (not overwritten)
- [ ] Vault mirrors exist and are synced (`$CT_VAULT/00-SHARED/Design-Narratives/`)
- [ ] `git status` shows only expected changes
- [ ] Ready to commit

---

## Related Documents

- **Forensic System Design:** `forensic-system-design.md`
- **Memory Routing:** `~/.claude/rules/memory-routing.md` (global rule)
- **Subagent Write Protocol:** `~/.claude/rules/subagent-write-protocol.md`
- **Script Writing:** `~/.claude/rules/script-writing.md`

---

**Status:** NORMATIVE — must follow to maintain coherent architecture  
**Last Updated:** 2026-04-07  
**Document Version:** 1.0
