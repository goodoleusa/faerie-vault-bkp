---
type: bundle-index
project: hustle
date: 2026-04-02
session_id: hustle-2026-04-02b
doc_hash: sha256:b3cc0f12d098c569763145059af64b0e6c5f5da341d37a8646ee04810787430e
status: final
promotion_state: awaiting-annotation
hash_ts: 2026-04-03T00:36:16Z
hash_method: body-sha256-v1
---

# Hustle — Complete Project Hub

All hustle business docs, session products, architecture, and playbooks in one folder.

## Contents

### 1. Architecture Diagram (Excalidraw)
**File**: hustle-architecture-diagram-2026-04-02.md
**Editable**: https://excalidraw.com/#json=Ic7Pa023qK8XW0qQ2O7UP,9XBkKFO22gojQMa5zaFy-A
Full intake-to-delivery pipeline: 3 stages (Acquire, Build, Ship), 9 templates, zero-cost stack.

### 2. Theme Builder Products
**File**: hustle-theme-builder-2026-04-02.md
- 25 named palette presets (Amethyst, Obsidian, Vaporwave, Forensic, etc.)
- 91-font library across 7 categories
- Per-heading font hierarchy (h1=logo, h2=hero, h3=cards, body)
- CSS export with Download button
- Educational CSS labels on every control

### 3. Intake Flow (Stripe)
**File**: hustle-intake-flow-2026-04-02.md
- /pricing page — 3 tiers (Starter $799, Signature $1,299, Powerhouse $2,499)
- /intake form — wired to POST /api/intake → Stripe checkout
- "No fine print" transparent pricing
- 12-24hr turnaround promise

### 4. Design Prompt Guide
**File**: hustle-design-prompt-guide.md
- Luma AI prompt templates for style tiles, heroes, color boards
- Translation pipeline: Luma output → code
- Font hierarchy cheat sheet
- Aesthetic vocabulary glossary

## What Changed in Code

| File | Change |
|------|--------|
| TemplatePreview.astro | Palette selector, font hierarchy, 91 fonts, CSS export |
| palettes.ts | 25 named palettes (NEW) |
| fonts.ts | 91 Google Fonts across 7 categories (NEW) |
| admin/index.astro | 6 doc panels, idea capture, password gate, surge deploy |
| pricing.astro | Package selection page (NEW) |
| intake.astro | Stripe-wired intake form (NEW) |
| order.astro | Alternative intake form (NEW) |
| 02-build.sh | Platform-agnostic build script (NEW) |
| 05-deploy-surge.sh | Surge dev preview deploy |
| templates/package.json | courtready added, build scripts updated |
| package.json | npm run build/deploy:surge from root |

## Pre-Existing Docs (already in this folder)

| File | What |
|------|------|
| 01-EXECUTIVE-SUMMARY.md | Business overview |
| 02-HOW-IT-WORKS.md | Product explanation |
| 03-RXREADY-DEEP-DIVE.md | Pharmacy vertical deep dive |
| 04-IMPLEMENTATION-ROADMAP.md | Build roadmap |
| 05-PRICING-PLAYBOOK.md | Pricing strategy |
| 06-COMPLIANCE-BOUNDARIES.md | What's in/out of scope |
| 07-SALES-PITCH-SCRIPT.md | Ready-to-use pitch |
| 08-DEMO-SITE-CHECKLIST.md | Pre-demo checklist |
| ARCHITECTURE.md | System architecture |
| BUSINESS-PLAN.md | Full business plan |
| hive-roadmap-to-revenue.md | Revenue milestones |
| hive-marketing-ideas.md | Marketing playbook |
| hive-pipeline-design.md | Pipeline architecture |
| hive-business-plan-design.md | Business plan design notes |
| sales/ | Sales templates and scripts |
| pharmacy/ | RxReady vertical docs |
| templates/ | Template architecture docs |
| frameworks/ | Business frameworks |
| checklists/ | Operational checklists |

## Next Steps
- [ ] Wire order.astro mock to real Stripe (or delete — intake.astro already works)
- [ ] New "BoldOS" template from purple/white COMMUNITY.OS mockup
- [ ] GitHub OAuth for production admin (password gate is stopgap)
- [ ] First real client test — run full pipeline end to end
