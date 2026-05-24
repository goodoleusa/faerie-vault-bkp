---
title: Eval & Metrics
type: hive-section
section: eval
up: "[[00-Hive-Home]]"
same: "[[01-Dev]], [[03-UIX]], [[04-Marketing]], [[05-Sales]], [[06-Agent-Chat]]"
tags:
  - hive/eval
  - path/hive
cssclasses:
  - hive-section
---

# 📊 Eval & Metrics

> [!east] Parallel Tracks
> Run evals, publish results, compare agent team performance across sessions.

## Live Metrics

```dataviewjs
const evals = dv.pages('"forensics/evals"').sort(f => f.file.mtime, 'desc').slice(0, 5)
dv.table(["Run", "Q", "R", "M", "F", "Date"], 
  evals.map(e => [e.file.link, e.Q ?? "—", e.R ?? "—", e.M ?? "—", e.F ?? "—", e.file.mtime.toFormat("MM-dd")]))
```

## Benchmarks

| Metric | Target | Last | Trend |
|--------|--------|------|-------|
| Q (quality) | ≥0.80 | 0.38 | ↓ |
| R (relevance) | ≥0.80 | 0.67 | → |
| M (mission alignment) | ≥0.80 | 0.67 | → |
| F (forensic integrity) | ≥0.90 | 0.50 | ↓ |

## Quick Actions

```meta-bind-button
style: primary
label: "▶ Run Eval"
action:
  type: command
  command: "swarmy:run-eval"
```

```meta-bind-button
style: default
label: "📤 Publish Report"
action:
  type: command
  command: "swarmy:publish-eval-report"
```

## Reports Archive

- [[Eval-Reports/]] — all published eval runs
- [NECTAR entries](~/.claude/NECTAR.md) — crystallized learning
