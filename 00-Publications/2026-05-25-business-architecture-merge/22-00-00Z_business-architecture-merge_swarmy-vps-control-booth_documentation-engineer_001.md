---
title: "swarmy / faerie business architecture — merge plan & control booth"
subtitle: "VPS collab space as the seat of dev, sales, ops, and memory — with pair-coding as a customer-facing primitive"
investigation_label: business-architecture-merge
mission: swarmy-vps-control-booth
lane: 1
agent: documentation-engineer
task_id: biz-arch-merge-2026-05-25
date: 2026-05-25
status: draft
compass_edge: S
next_task_queued: vps-deploy-bake-pdf-skill
quality_score: 0.78
belief_index: 0.80
tags:
  - business
  - architecture
  - merge-plan
  - swarmy-vps
  - control-booth
  - pair-coding
  - product-extraction
sources:
  - swarmy-ui/docs/COMPARISON.md
  - swarmy-ui/CLAUDE.md
  - faerie2/CLAUDE.md
  - faerie2/deploy/CT-LIVE-COLLAB-SETUP.md
  - faerie2/deploy/README.md
  - swarmy-hive-plugin/src/pdf-export.ts
artifacts:
  pdf: ./business-architecture-merge.pdf
  diagrams: ./diagrams/
related:
  - 00-Publications/2026-05-25-swarmy-ui-faerie2-comparison/
dashboard_machine_readable:
  team_size: 2
  team_members:
    - { handle: goodoleusa, role: backend-system }
    - { handle: JescaLyn, role: frontend-design }
  source_repos:
    - swarmy-ui
    - faerie2
    - swarmy-hive-plugin
    - faerie-vault
    - cybertemplate
  merged_surfaces:
    - swarmy-product
    - control-booth
    - faerie-engine
    - pdf-publication-pipeline
  control_booth_modes:
    - { id: dev, status: live, notes: "OpenHands pair-edit working today" }
    - { id: sales, status: planned, notes: "funnel, content studio, lightweight CRM" }
    - { id: ops, status: planned, notes: "deploys, health, costs" }
    - { id: memory, status: partial, notes: "vault exists, no in-booth browser yet" }
  phases:
    - { id: 0, label: foundation-comparison, status: in-progress }
    - { id: 1, label: control-booth-hub, status: planned }
    - { id: 2, label: business-surfaces, status: planned }
    - { id: 3, label: pair-coding-as-product, status: planned }
  key_decisions_open:
    - multi-tenant-isolation-strategy
    - billing-model
    - which-substrate-becomes-public-api
  pair_coding_product_primitives:
    - multi-user-authed-editor
    - live-preview-pane
    - agent-assist-chatroom
    - shared-filesystem-git
    - per-session-isolation
---

# Premise

The team is two people:

- **goodoleusa** — back-end, system architecture, faerie engine
- **JescaLyn** — front-end, design, UX

There are no departments. Sales, ops, marketing, and dev all need to land somewhere — and the natural answer is the place where dev already lives: **`swarmy.retrofuture.tech`**, the OpenHands-based VPS collab space. It already authenticates both humans via GitHub OAuth, mounts shared workspaces, hot-reloads previews, and runs agents on-demand. Extending it from "dev IDE" to "company control booth" is a smaller leap than building a separate ops stack.

This doc proposes:

1. A merge architecture that pulls `swarmy-ui`, `faerie2`, `swarmy-hive-plugin`, `faerie-vault`, and `cybertemplate` into four named surfaces
2. A four-mode control booth on top of the existing VPS
3. Extraction of the pair-coding primitive as a customer-facing feature
4. A phased rollout that doesn't break what's working

# Current state — what's actually running

![Current state](diagrams/01-current-state.png)

**On disk (local Win11 + WSL):**

- `swarmy-ui` — UI prototype, the product mental model. Beekeeping vocabulary.
- `faerie2` — orchestration substrate, mission graph, compass bearings, skills, deploy configs.
- `swarmy-hive-plugin` — Obsidian plugin that wraps the PDF pipeline.
- `faerie-vault` — Obsidian vault holding publications, memory, charters.

**On the VPS (`swarmy.retrofuture.tech`):**

- OpenHands web UI — both humans authenticate, get a shared workspace
- swarmy MCP server — agent backend
- `chat-mvp` — chat sidecar + auth gate (`/auth/check`)
- `admin-dashboard` — operator console
- Caddy — TLS + forward_auth via chat-mvp
- `cybertemplate` sidecar — Astro dev mode, hot-reloads at `ct-dev.retrofuture.tech`

The pieces already cooperate; nothing is wasted. What's missing is **one surface that ties them into a daily company control panel.**

# Target — the four-mode control booth

![Target control booth](diagrams/02-target-control-booth.png)

A single hub at `swarmy.retrofuture.tech` with four mode tabs. Each tab is a thin shell over things that already exist or are close to existing.

## Dev mode (live today; polish only)

- OpenHands pair-edit (works)
- Live preview pane (works for cybertemplate; add per-repo previews for `swarmy-ui` and any other in-flight project)
- Agent-assist chat (works via chat-mvp)

## Sales / marketing mode (new build)

- **Funnel dashboard** — signups, free-trial conversions, churn signals
- **Content studio** — write blog posts, social copy, email sequences with agent assist; publishes to landing pages and the marketing site
- **Lightweight CRM** — leads, conversation threads, follow-up reminders. Don't reach for HubSpot; for a 2-person team a flat-file CRM with the same beekeeping metaphor (leads = nectar, contacts = pollen, deals = ambrosia, closed = honey) keeps cognitive load tiny.

## Ops mode (new build, thin)

- Deploy / rollback console — buttons that wrap the existing `git push` → CI → droplet flow
- Service health — uptime, error rates, queue depths from the swarmy MCP
- Cost / token / spend — API costs, droplet bill, summed weekly

## Memory mode (vault as a first-class booth tab)

- Browse `faerie-vault` publications without leaving the booth
- COC chain explorer — verify any artifact's hash lineage in two clicks
- HONEY / NECTAR live view — what the system has crystallized recently

# Architectural merge plan

![Merge flows](diagrams/03-merge-flows.png)

Five source repos collapse into **four merged surfaces**:

| Surface | Composed from | Lives at |
|:---|:---|:---|
| **swarmy product** (customer-facing app) | `swarmy-ui` + `cybertemplate` | Customer subdomains; per-tenant isolation |
| **control booth** | `swarmy-ui` chrome + `faerie-vault` views + `chat-mvp` + `admin-dashboard` | `swarmy.retrofuture.tech` |
| **faerie engine** (shared orchestration core) | `faerie2` skills, mission graph, COC, forensics | Runs as the brain inside both swarmy product and control booth |
| **PDF / publication pipeline** | `faerie2/.agents/skills/pdf` + `swarmy-hive-plugin` | Used by anyone, anywhere; preset parity already in place |

The merge is **logical, not literal** — the repos stay separate (their git histories carry value). What changes is the *deployment graph*: one VPS, one shared engine, two product surfaces (internal booth + external product) sharing it.

## What this fixes

- **No duplicate orchestration logic.** Today, the booth and the product would each try to spawn agents; with a shared engine they don't.
- **No duplicate UI components.** `swarmy-ui`'s hex cells, bee SVGs, hive screens are reused inside the booth's "Memory" tab and the product's project screens.
- **Single PDF pipeline.** The Obsidian plugin and the headless skill already share `print-ready-header.tex`; this just makes that contract explicit at the system level.

# Pair-coding as a customer-facing primitive

![Pair-coding product extraction](diagrams/04-pair-coding-product.png)

The collab space you and JescaLyn use *is itself* a product. Extract the primitives:

1. Multi-user authed editor
2. Live preview pane
3. Agent-assist chatroom
4. Shared filesystem + git
5. Per-session isolation

Repackage as **Hive Room** — a customer-facing feature embedded in any project type:

- **Pair-coding hive** — 2–5 humans + worker bees, shared cell, live agents. Sold to small dev teams as "Replit + Cursor + a bee swarm."
- **Async stigmergic room** — humans drop nectar (notes, dumps), workers ripen ambrosia, the room crystallizes honey overnight. Sold as a research / investigation tool.
- **Embedded mode** — Hive Rooms appear inside FlowSearch flights, Survey flights, etc. Every project type gains a "shared room" surface.

This is the highest-leverage product extraction available: the thing you're already using daily becomes the feature you sell.

## Why this is differentiated

- Most pair-coding tools are 2-human or human-agent, not human + agent swarm
- The beekeeping metaphor gives every customer a stable mental model (capped/uncapped, hive/cell, nectar/honey)
- Forensic COC means every shared session is *auditable* — a real selling point for regulated industries

# Phased rollout

![Phased rollout gantt](diagrams/05-phased-rollout.png)

**Phase 0 — Foundation comparison (now).**
Glossary alignment (done), PDF pipeline shared (done), plugin preset parity (in progress).

**Phase 1 — Control booth hub (foundation).**
Bake PDF skill into VPS deploy. Scaffold the unified hub UI. Polish dev mode. (~2 weeks, mostly UI work)

**Phase 2 — Business surfaces.**
Sales/marketing + ops + memory tabs. None are deep; each is a thin shell over existing data. (~3 weeks)

**Phase 3 — Product extraction.**
Pull the pair-coding primitive into a reusable "Hive Room" component. Embed in the customer-facing swarmy product. Add multi-tenant isolation. (~5 weeks; this is the revenue lever)

# Open questions

These need decisions before Phase 3:

1. **Multi-tenant isolation strategy.** OpenHands today is shared-workspace. For customer use we need per-tenant containers, per-tenant volumes, per-tenant COC chains. Buy (Render / Fly multi-tenant) or build (k8s on the same droplet)?
2. **Billing model.** Per-hive subscription? Per-flight credits? Per-agent-hour metered? Per-honey-artifact?
3. **Which substrate becomes the public API?** The MCP server is the natural answer but it's currently internal-only. Hardening + rate-limiting is non-trivial.
4. **What sits at `swarmy.retrofuture.tech` vs. the product domain?** The control booth and the product probably want different domains (e.g. `app.swarmy.tech` for product, `booth.swarmy.tech` for the team-internal hub) so customers never accidentally see the ops mode.

# Immediate next steps (this week)

1. Commit the plugin's `comparison` preset (currently uncommitted; sits on top of in-flight Step 3.5 work)
2. Bake `faerie2/.agents/skills/pdf` into the VPS deploy (`deploy/0x_setup-vps.sh` adds `pandoc texlive-xetex curl`; whitelist mermaid.ink in any egress rules)
3. Draft a one-page **Hive Room product brief** with the 5 primitives above as the contract
4. Spike the **memory mode** tab — easiest one to ship; it's just a vault file browser inside the booth

# Companion artifact

- **PDF (typeset):** [`business-architecture-merge.pdf`](./business-architecture-merge.pdf)
- **Diagram sources:** `./diagrams/*.mmd`
- **Diagram renders:** `./diagrams/*.png`
- **Rebuild command:** `faerie2/.agents/skills/pdf/scripts/build_pdf.sh ./THIS_FILE.md`
