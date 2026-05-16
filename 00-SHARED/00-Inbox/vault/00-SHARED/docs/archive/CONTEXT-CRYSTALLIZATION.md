# Context crystallization (stub)

> **LEGACY:** This document predates the 2026-04-05 overhaul.
> For current docs, see [README.md](../README.md) or the vault LAUNCH/ folder.
> Kept for historical reference.

**Full protocol:** `.claude/rules/memory-routing.md` — Crystallization Law, token budgets, promotion algorithm.

**Design rationale (hooks vs scripts, where tokens land, what to shrink first):** [`docs/DESIGN-QUESTIONS.md`](DESIGN-QUESTIONS.md)

**When to compress instruction Markdown:** Before promoting any file to **default read** (rules, `CLAUDE.md` chain, `/faerie`), estimate **tokens × readers**. Monthly: scan longest `.md` under `.claude/` and `docs/` for **high fan-out** bloat.

**Signals to prioritize:** referenced from many places; wrong audience (subagent reading operator manual); duplicated across WIKI/README/SKILL; stale narrative in hot path.

**5-minute checklist:** Default read for more than one role? → trim or split. One paragraph + link for the fold? Truth belongs in code? Deduped after edit?

**Related:** `.claude/README-continual-learning.md` · `hooks/state/SPRINT_QUEUE.md` · `docs/OBSIDIAN-COLLAB-STARTUP.md`
