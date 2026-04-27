---
type: template
tags: [FFFF, dashboard, design-principle]
created: 2026-03-28
doc_hash: sha256:a1e85a3ca13b0c62b2d058f03fb763817fca2f701926f09a2096826c6e976019
hash_ts: 2026-03-29T16:10:51Z
hash_method: body-sha256-v1
---

# FFFF Dashboard Template

> **Findings / Flags / Friction / Flow** at every zoom level.

Every dashboard, report, or status view MUST show all four F's. This applies at every zoom level: team, sprint, agent, technique.

## Structure

### FINDINGS — What was discovered
- Confirmed facts, new evidence, hypothesis movements
- Confidence levels and source counts

### FLAGS — What needs attention
- HIGH priority items, blockers, warnings
- Items awaiting human review

### FRICTION — Where things struggled
- Failed tasks, stalled queues, recurring errors
- Agent performance dips, tool failures

### FLOW — What went smoothly
- Successful patterns, beat-last scores
- Techniques that worked, clean pipelines

## Zoom Levels

| Level | Scope | Example |
|-------|-------|---------|
| TEAM | All agents across investigation | Team Overview dashboard |
| SPRINT | Single sprint or session | Session handoff brief |
| AGENT | Single agent type | Agent card + evolution |
| TECHNIQUE | Single method or tool | Technique library entry |

## Palette

MermaidJS: pistachio `#93C572`, teal `#4ECDC4`, gold `#D4A843`, dark `#2d2d44`.
