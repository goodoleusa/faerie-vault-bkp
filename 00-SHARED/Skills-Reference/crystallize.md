---
type: reference
status: active
tags: [skill, crystallize, memory, HONEY, NECTAR]
parent: Skills-Reference/INDEX
up: Skills-Reference/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:243637ada2c98e0e54c9ea7565ed1af930fa57169fc91a9129ad4c7aa3b2abb4
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Skills-Reference](INDEX.md) · [⌂ Home](../../HOME.md)

# /crystallize — Memory Integrator

Integrates validated findings into crystallized knowledge. Runs on human choice,
never on schedule.

---

## Invocation

```
/crystallize
```

---

## What It Does

Phase 1: Scan NECTAR.md AND `projects/*/memory/feedback_*.md` as one candidate pool.
Phase 2: Surface candidates that appear in ≥3 sessions (recurrence tracking).
Phase 3: Propose HONEY candidates — human approves or rejects each one.
Phase 4: Approved entries are integrated into HONEY.md with full LLM synthesis.

---

## Crystallization vs Compression

**Crystallization** integrates new knowledge against everything known.
Result: denser, richer statements; fewer lines carrying more meaning.

**Compression** just removes words.
Result: shorter text that loses nuance.

These are different. `/crystallize` does crystallization. Do not confuse them.

---

## When to Run

- After a session with significant new findings (high-quality NECTAR entries)
- After ≥3 sessions covering the same domain (recurrence threshold met)
- When HONEY.md is nearing budget (≤5K tokens) and new knowledge must fit

**Do not run:**
- Just because HONEY is long (that is compression, not crystallization)
- On a schedule (crystallization requires judgment, not routine)
- For findings that are session-specific (they belong in NECTAR, not HONEY)

---

## Budget Rules

| File | Budget | Enforcement |
|------|--------|------------|
| HONEY.md | ≤5K tokens | /crystallize gates on this |
| NECTAR.md | unbounded | append-only forever |
| pollen | ephemeral | cleared at /handoff |

HONEY crystallization is a **human choice**. Agents never queue it.

---

## Related

- [[handoff]] — /handoff promotes pollen to NECTAR (precedes crystallize)
- [[../Architecture/memory-topology]] — HONEY/NECTAR/pollen architecture
- [[../Glossary/terms]] — crystallize, HONEY, NECTAR, pollen defined
