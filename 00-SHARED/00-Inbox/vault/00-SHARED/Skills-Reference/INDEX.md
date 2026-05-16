---
type: index
status: active
tags: [index, skills, commands, reference]
parent: 00-SHARED/INDEX
up: 00-SHARED/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:4feb8f682115b79cef7643e3eb1b0c47577ce8c7ffe7da29245615e7c0f53aa8
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ 00-SHARED](../INDEX.md) · [⌂ Home](../../HOME.md)

# Skills Reference

Quick-reference for every `/skill` command in faerie2.

---

## Skills

| Skill | Role | Doc |
|-------|------|-----|
| `/faerie` | Session orchestrator — orient, run waves, dashboard | [[faerie]] |
| `/run` | Queue consumer — claim and execute tasks | [[run]] |
| `/metrics` | System health snapshot | [[metrics]] |
| `/dev-eval` | Eval detail and gap analysis | [[dev-eval]] |
| `/crystallize` | Memory integrator — pollen → NECTAR → HONEY | [[crystallize]] |
| `/handoff` | Session closer — promote memory, sync vault | [[handoff]] |
| `/droplet` | Insight capture — write to droplets vault | [[droplet]] |
| `/queue` | Queue manager — view, add, shape tasks | [[queue]] |

---

## Quick Decision Guide

| Situation | Use |
|-----------|-----|
| Starting a session | `/faerie` |
| Executing queued work | `/run` |
| Checking system health | `/metrics` |
| Investigating a score drop | `/dev-eval` |
| Adding/reprioritizing tasks | `/queue` |
| Capturing an insight now | `/droplet` |
| End of session | `/handoff` |
| Deliberate memory integration | `/crystallize` |

---

## Related

- [[../COMMAND-PRIMER]] — **Command Primer** — comprehensive reference organized by intent (run / eval / train / tweak)
- [[../Onboarding/02-skills-tour]] — narrative overview of all skills
- [[../Hive/what-is-faerie]] — context for why these skills exist
- [[../Glossary/terms]] — terms used in skill outputs
