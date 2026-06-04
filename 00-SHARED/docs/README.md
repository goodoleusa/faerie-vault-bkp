---
type: index
status: archived-mirror
created: 2026-04-21
updated: 2026-06-04
tags: [index, docs, faerie]
up: ../README.md
note: "This folder was a mirror of reckon/docs/. Canonical docs live at reckon/docs/. 104 files archived to _archive-2026-06-04/ on 2026-06-04."
---

> [↑ Readme](../README.md) · [⌂ Home](../README.md)

# docs/ — Archived Mirror (canonical: reckon/docs/)

> **NOTICE (2026-06-04):** This folder was a legacy mirror of `reckon/docs/`. The 104 docs
> that lived here have been archived to `_archive-2026-06-04/`. The **canonical source of
> truth for all Reckon documentation is `reckon/docs/`** (the engine repo).
>
> Two files are retained here:
> - `ARCHITECTURE.md` — vault-specific architecture notes
> - `README.md` — this notice

**Active docs:** See [reckon/docs/](../../../../reckon/docs/) — that tree is always current.  
**Archived (2026-06-04):** 84 files in `_archive-2026-06-04/`

---

## Core Architecture

| File | Purpose |
|------|---------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System architecture — phases, sprints, progress. Read first. (Legacy notice — see root ARCHITECTURE.md for current state.) |
| [F0-NARRATIVE-DESIGN.md](./F0-NARRATIVE-DESIGN.md) | f(0) perpetual piston architecture briefing — current design narrative |
| [QUEUE-CLAIMING-ARCHITECTURE.md](./QUEUE-CLAIMING-ARCHITECTURE.md) | Queue-claiming agent architecture — stigmergic wave patterns |
| [MODEL-ROUTING.md](./MODEL-ROUTING.md) | Model routing policy — Haiku-default with strategic Sonnet/Opus |

## Business Strategy

| File | Purpose |
|------|---------|
| [BUSINESS-CASE-F0.md](./BUSINESS-CASE-F0.md) | f(0) business case, economics, GTM, and profitability roadmap |
| [business/BUSINESS_PLAN.md](./business/BUSINESS_PLAN.md) | Market analysis, competitive positioning, pricing |
| [business/NOVELTY_TABLE.md](./business/NOVELTY_TABLE.md) | Competitive differentiation and IP novelty |
| [business/SURVIVAL_LAUNCH_PLAN.md](./business/SURVIVAL_LAUNCH_PLAN.md) | Zero-budget launch and revenue strategy |

## Operations & Setup

| File | Purpose |
|------|---------|
| [FOUNDER-GUIDE.md](./FOUNDER-GUIDE.md) | Getting started — vision, values, operational principles |
| [SETUP-CHECKLIST.md](./SETUP-CHECKLIST.md) | First-time installation and configuration |
| [COMMAND-GUIDE.md](./COMMAND-GUIDE.md) | Power-user command reference |
| [PHILOSOPHY.md](./PHILOSOPHY.md) | Design philosophy and guiding principles |
| [DYNAMO.md](./DYNAMO.md) | Multi-session faerie: running 2+ Claude sessions on the same queue |
| [ONBOARDING.md](./ONBOARDING.md) | ⚠️ DEPRECATED — See ONBOARDING-GENERIC.md or ONBOARDING-COLLAB.md |
| [ONBOARDING-GENERIC.md](./ONBOARDING-GENERIC.md) | New team member setup (solo user or fresh machine) |
| [ONBOARDING-COLLAB.md](./ONBOARDING-COLLAB.md) | Onboarding for collaborative investigation setup |

## Technical References

| File | Purpose |
|------|---------|
| [SPAWN-BOILERPLATE.md](./SPAWN-BOILERPLATE.md) | Agent spawn bundle rendering using template registry |
| [MEMORY-AS-SERVICE-ARCHITECTURE.md](./MEMORY-AS-SERVICE-ARCHITECTURE.md) | Memory system design — HONEY/NECTAR/pollen architecture |
| [SPAWN-BOILERPLATE-INJECTION-ARCHITECTURE.md](./SPAWN-BOILERPLATE-INJECTION-ARCHITECTURE.md) | Deprecated spawn injection system (see SPAWN-BOILERPLATE.md instead) |
| [README-local-overlays.md](./README-local-overlays.md) | Local configuration files not shipped (mcp.json, memory setup) |

## Design Documentation

| Folder | Purpose |
|--------|---------|
| [design/](./design/) | Forensic system and artifact registry design docs |

## Evaluation & Benchmarking

| Folder | Purpose |
|--------|---------|
| [eval-sets/](./eval-sets/) | Evaluation test fixtures |
| [benchmark-results/](./benchmark-results/) | Benchmark outputs |
| [eval-April-audit_results/](./eval-April-audit_results/) | April 2026 compliance and framework audit results |

## Auto-Updated Narrative

| Folder | Purpose |
|--------|---------|
| [narrative/](./narrative/) | Investigation narrative (auto-appended by session_stop_hook). Read INVESTIGATION-NARRATIVE.md for running log. |

---

## Archive

Historical narratives, sprint artifacts, and superseded design docs are in [ARCHIVE/](./ARCHIVE/). See [ARCHIVE/README.md](./ARCHIVE/README.md) for an indexed list with summaries.

### Recently Consolidated (2026-04-24)

The following documents have been merged into primary references to reduce duplication:

- **FAERIE-BUSINESS-CASE.md** → merged into [BUSINESS-CASE-F0.md](./BUSINESS-CASE-F0.md)
- **SPAWN-BOILERPLATE-REFERENCE.md** → merged into [SPAWN-BOILERPLATE.md](./SPAWN-BOILERPLATE.md)
- **ARCHITECTURE_QUEUE_CLAIMING.md** → merged into [QUEUE-CLAIMING-ARCHITECTURE.md](./QUEUE-CLAIMING-ARCHITECTURE.md)
- **ARCHITECTURE-MODEL-ROUTING.md** → merged into [MODEL-ROUTING.md](./MODEL-ROUTING.md)

All content preserved. Use the canonical files above instead.

---

## Structure Overview

```
docs/
├── ARCHITECTURE.md                             [Legacy notice]
├── F0-NARRATIVE-DESIGN.md
├── QUEUE-CLAIMING-ARCHITECTURE.md
├── MODEL-ROUTING.md
├── BUSINESS-CASE-F0.md
├── SPAWN-BOILERPLATE.md
├── MEMORY-AS-SERVICE-ARCHITECTURE.md
├── FOUNDER-GUIDE.md
├── COMMAND-GUIDE.md
├── PHILOSOPHY.md
├── DYNAMO.md
├── SETUP-CHECKLIST.md
├── ONBOARDING.md                               [Deprecated redirect]
├── ONBOARDING-GENERIC.md
├── ONBOARDING-COLLAB.md
├── SPAWN-BOILERPLATE-INJECTION-ARCHITECTURE.md [Legacy]
├── README-local-overlays.md
├── business/
│   ├── README.md
│   ├── BUSINESS_PLAN.md
│   ├── NOVELTY_TABLE.md
│   └── SURVIVAL_LAUNCH_PLAN.md
├── design/
│   ├── README.md
│   ├── forensic-system-design.md
│   ├── FORENSIC-SYSTEM-INDEX.md
│   ├── CANONICAL-WRITE-LOCATIONS.md
│   ├── forensic-system-summary.md
│   ├── artifact-registry-design.md
│   └── forensic-implementation-checklist.md
├── eval-sets/
├── benchmark-results/
├── eval-April-audit_results/
├── narrative/
├── ARCHIVE/
└── README.md                                   [This file]
```
