---
type: reference
status: active
tags: [architecture, global, mirror, source, direction]
parent: Architecture/INDEX
up: Architecture/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:daf0c5b7857a0234479f6b3e63b6f7a69c94b3e971b49bc1d20628d136bb13da
hash_ts: 2026-04-25T01:10:51Z
hash_method: body-sha256-v1
---

> [↑ Architecture](INDEX.md) · [⌂ Home](../../HOME.md)

# Source-Mirror Direction

The relationship between the global Claude configuration and the faerie2 repo.

---

## The Direction

```
~/.claude/ (global)  ←  SOURCE
faerie2 repo          ←  MIRROR (curated derivative)
```

Global configuration is the canonical source. faerie2 is a curated view
of the orchestration concepts, stripped of investigation-specific content,
formatted for human learning.

---

## What Lives Where

| Content | Location | Authority |
|---------|----------|-----------|
| HONEY.md (global methods) | `~/.claude/HONEY.md` | Canonical |
| NECTAR.md (findings) | `~/.claude/NECTAR.md` | Canonical |
| Rules (agents, core, memory) | `~/.claude/rules/` | Canonical |
| Skills (BODY.md files) | `~/.claude/skills/` | Canonical |
| Scripts | `~/.claude/scripts/` | Canonical |
| Hooks | `~/.claude/hooks/` | Canonical |
| faerie2 vault docs | `faerie2/vault/` | Derivative |
| faerie2 CLAUDE.md | `faerie2/CLAUDE.md` | Project mirror |

---

## Mutation Discipline

When global and project instructions conflict, the conflict is a **mutation**.
Mutations are classified: beneficial / neutral / harmful / uncertain.

Protocol:
1. Measure baseline before repair (T+1 Preservation Rate is destroyed if fixed before wired)
2. Audit → Measure → Pause → Fix → Measure again → Publish

The T=0 mutation baseline is locked at:
`faerie2/forensics/mutation-baselines/mutation-baseline-T0.json`

---

## faerie2's Role

faerie2 is the platform. It contains:
- The eval infrastructure (eval harness, agent cards, scoring)
- The spawn contract enforcement (hook + template system)
- The piston implementation (scripts, skills)
- The forensic COC system (coc.jsonl, hash chain)

The global `~/.claude/` directory is the operating environment.
faerie2 provides the tools that make that environment work.

---

## Related

- [[memory-topology]] — global vs repo HONEY distinction
- [[../Hive/the-five-principles]] — platform-agnostic design
- [[../Glossary/terms]] — global, mirror, mutation defined
