---
type: reference
status: active
tags: [skill, dev-eval, eval, quality, gaps]
parent: Skills-Reference/INDEX
up: Skills-Reference/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:57777f0de4027d34f1995772f303b2b2c377ddd4be39640942c774864a812494
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Skills-Reference](INDEX.md) · [⌂ Home](../../HOME.md)

# /dev-eval — Eval Detail and Gap Analysis

Deep evaluation breakdown with per-dimension scores, gap analysis,
and dual-task improvement suggestions.

---

## Invocation

```
/dev-eval
```

---

## What It Shows

Beyond `/metrics`:
- Per-agent performance scores (which agents beat baseline)
- Dimension-by-dimension gap breakdown
- Dual-task hints (actions that improve 2+ dimensions simultaneously)
- VANILLA baseline comparison (if `/vanilla` has been run)
- Training queue eligibility (agents close to beat-last threshold)

---

## Score Rubric

| Score | Meaning |
|-------|---------|
| 1.0 | Perfect — all criteria met |
| 0.85 | Excellent — 90%+ criteria met |
| 0.70 | Good — 70%+ criteria met (minimum acceptable) |
| 0.50 | Partial — flag for rework |
| 0.25 | Incomplete — rework required |
| 0.0 | Failed |

---

## Dual-Task Hints

A dual-task hint is an action that improves two or more eval dimensions
simultaneously. Example:

```
QUALITY=0.65 → write NECTAR for today's findings (also ↑R citation rate)
```

Writing a finding to NECTAR with a source citation:
- Improves M (task quality) — finding is captured
- Improves R (citation accuracy) — source is documented

These hints are the highest-leverage improvement actions.

---

## VANILLA Comparison

When `/vanilla` has run, `/dev-eval` shows:
```
VANILLA baseline: composite=0.44 (unassisted)
Current:          composite=0.68
Delta:            +0.24 (+55% improvement)
```

If VANILLA has not run recently: `[VANILLA: baseline estimated — run /vanilla after a hard task for real delta]`

---

## Related

- [[metrics]] — quick health snapshot
- [[../Dashboards/eval-snapshot]] — narrative eval view
- [[../Glossary/terms]] — eval dimensions, beat-last, VANILLA defined
