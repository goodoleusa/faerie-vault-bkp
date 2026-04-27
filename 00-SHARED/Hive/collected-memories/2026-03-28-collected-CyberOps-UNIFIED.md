---
type: collected-memory
status: unreviewed
created: 2026-03-28
updated: 2026-03-28
tags: [memory, collected, agent-memory, CyberOps-UNIFIED]
source_project: "/mnt/d/0LOCAL/0/ObsidianTransferring/CyberOps/UNIFIED"
source_file: "MEMORY.md"
source_path_wsl: "/mnt/c/Users/amand/.claude/projects/-mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIFIED/memory/MEMORY.md"
source_path_windows: "C:\Users\amand\.claude\projects\-mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIFIED\memory\MEMORY.md"
source_sha256: "2b62f317b64fdb35f036b82a208eea8572c998a57152f3a032ff919053c99652"
source_size_bytes: 4279
collected_at: "2026-03-28T02:27:57Z"
collector: emergency_handoff.py
parent:
  - "[[agent-history]]"
sibling: []
child: []
memory_lane: inbox
promotion_state: capture
review_status: unreviewed
ann_hash: ""
ann_ts: ""
doc_hash: sha256:e671ef5b1d1b1869949ad89c619619e322a9f8fbf17e6f6d9b4a0519a9818687
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:31Z
hash_method: body-sha256-v1
---

# Collected Memory: CyberOps-UNIFIED

| Field | Value |
|-------|-------|
| Source Project | `/mnt/d/0LOCAL/0/ObsidianTransferring/CyberOps/UNIFIED` |
| Source File | `MEMORY.md` |
| Local Path (WSL) | `/mnt/c/Users/amand/.claude/projects/-mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIFIED/memory/MEMORY.md` |
| Local Path (Windows) | `C:\Users\amand\.claude\projects\-mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIFIED\memory\MEMORY.md` |
| SHA256 (at collection) | `2b62f317b64fdb35f036b82a208eea8572c998a57152f3a032ff919053c99652` |
| Lines | 55 |
| Collected | 2026-03-28T02:27:57Z |

## Content

```markdown
# CyberOps-UNIFIED Vault Memory

## First Principles (read before every action)

**Equilibrium**: Every output must balance an input. Context consumed crystallizes into knowledge. Budgets enforce this — never add to an over-budget file. If a file is over, crystallize first. The system is conservative: energy in = energy out.

**Flow**: Work flows like water — it doesn't pool. Scratch → NECTAR → HONEY. Agents produce → handoff collects → crystallize distills → faerie launches again. If something stops flowing, the system stagnates. Move things through, don't let them accumulate.

**Crystallization**: Not compression. Integration. The new fact is understood against everything already known. Duplicates merge. Contradictions resolve. Cross-references form. Each line carries more meaning. Shorter but deeper. This applies to EVERYTHING — manifests, memories, design docs, dashboards. If you're just appending, you're not crystallizing.

## Session 2026-03-27: Architecture Visualization + Memory Cleanup

### Done
- Rules crystallized (504→274 lines, under 300 budget) with human-readable vault versions
- 16 MermaidJS diagrams in System-Architecture.md (equilibrium color palette, mobile-friendly)
- 31 pseudosystem component notes with excalibrain metadata
- 18 design narrative docs collected with SHA256 provenance manifest + COC
- Session manifests consolidated (87+12 per-minute → 3 crystallized daily narratives)
- design-hash-track.py for lightweight edit tracking
- DataviewJS TOC→Mermaid template for design sessions

### Architecture Decisions
- `.claude/memory/` should be HONEY system only (HONEY + NECTAR + REVIEW-INBOX + scratch)
- forensics/, investigations/, training/ belong at their own `~/.claude/` level
- Session manifests: one crystallized daily .md, JSONs archived
- Two-tier docs: terse system files (tokens) + expanded vault versions (humans)
- Design IP: hash at creation, track edits via design-hash-track.py, COC in design-coc.jsonl

### Liftoff Paradox (crystallized 2026-03-27)
The best thinking happens at context edges — deepest depth, richest connections, most compaction risk. Discipline: **write the jewel before chasing the next one.** Chain-of-consciousness doc `13-CHAIN-OF-CONSCIOUSNESS-2026-03-27.md` was reconstructed after compaction loss — proof of the principle and its violation.

### Open Threads
1. Pseudosystem A/B parallel versions (prev vs next for comparison testing)
2. HONEY flow dashboard (central viz of all HONEY-tier files global→local)
3. `.claude/memory/` architecture refactor (move forensics/investigations/training out)
4. Investigation finish line dashboards (work-units-to-completion)
5. REVIEW-INBOX crystallization (427L, needs siphoning)
6. **Queue COC architecture** — done tasks are forensic evidence, never delete. COC-log all transitions, atomize outputs, enrich knowledge bases (NECTAR, AGENTS.md, agent cards, vault). See project_queue_coc.md.
7. Dashboard sweep (agent running — uncentralized dashboards/templates)
8. Manifest hook frequency fix (should fire once per session, not per tool call)

### Prior Session Work
- emergency_handoff.py (1.5 sec, circuit breaker pattern)
- /handoff and /faerie Step Zero protocol
- Three-layer separation, atomized briefs, deferred hashing

## Memory Index

- [feedback_fast_handoff.md](feedback_fast_handoff.md) — /handoff should delegate to membot immediately, not read files in low-context parent
- [feedback_handoff_is_workday_end.md](feedback_handoff_is_workday_end.md) — /handoff = end of workday ("good night"), not just end of session
- [feedback_rounds_not_percentage.md](feedback_rounds_not_percentage.md) — Context budget = synthesis rounds remaining, not raw percentage
- [feedback_honey_dev_mode.md](feedback_honey_dev_mode.md) — HONEY versions are folders with all 4 levels together, not subfolders per level
- [feedback_honey_living_document.md](feedback_honey_living_document.md) — HONEY is a living document that deepens through crystallization
- [feedback_websearch_claude_docs.md](feedback_websearch_claude_docs.md) — Always websearch for Claude CLI docs, training data may be stale
- [project_queue_coc.md](project_queue_coc.md) — Done tasks are forensic evidence, never delete from queue
```

## Your Annotations

<!-- What's useful here? Should any items be promoted to NECTAR/HONEY? -->
<!-- Are there tasks or threads to queue? -->

