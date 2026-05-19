---
type: roundup
status: active
created: 2026-05-17T12:36:00Z
updated: 2026-05-17T12:36:00Z
tags: [publications, roundup, eval, metrics, research]
parent: 80-Publications.md
intent_modes:
  - learn-explore
  - analyze  
  - review
  - finalize
doc_hash: pending
---

> [← Publications](80-Publications.md)

# Publications Roundup — 2026-05-19

**Purpose:** Single entry point to find publication-worthy docs organized by your intent mode.  
**Last updated:** 2026-05-19

---

## 🆕 New (2026-05-19) — Stigmergy session field package

Four cross-linked docs from the 2026-05-19 ad-hoc stigmergic coordination session. Citable as a coherent set; together they form a publication-grade argument for stigmergy as the coordination substrate for AI agent teams.

| Doc | Genre | Use it to… |
|---|---|---|
| [`STIGMERGY-FOR-AGENT-TEAMS.md`](STIGMERGY-FOR-AGENT-TEAMS.md) | Technical narrative / position piece | Cite in an application or pitch where the question is *why does this pattern matter*. Walks through six concrete Agent Teams bugs and how stigmergy maps onto each, with a three-tier proposal for what Anthropic could ship. |
| [`POTEMKIN-FAERIE-FIELD-REPORT.md`](POTEMKIN-FAERIE-FIELD-REPORT.md) | Forensic field report | Cite when the question is *did the pattern actually work*. Full session timeline, observed failure modes, quantified throughput/cost deltas, failure-mode → faerie-component mapping. |
| [`ORCHESTRATOR-OBSERVATIONS.md`](ORCHESTRATOR-OBSERVATIONS.md) | First-person practitioner notes | Cite when the question is *what does it feel like to run*. Honest first-person observation layer with specific pre-/during-/post-spawn tweaks. |
| [`FOR-SKEPTICS-zero-confabulation.md`](FOR-SKEPTICS-zero-confabulation.md) | Skeptic-facing methodology explainer | Cite when the question is *can the 0% confabulation / 100% manifest-truthfulness numbers be trusted*. Explains the citability + promotion-gate model end-to-end. |
| [`MONKEYBRANCHING-2-AGENT-FIELD-REPORT.md`](MONKEYBRANCHING-2-AGENT-FIELD-REPORT.md) | Field report companion (2-agent variant) | Cite alongside POTEMKIN for the 5→N progression. Charter-first + atomic claims + cap N=2-3 = stigmergic coordination without throughput-for-cleanup tradeoff. |

All five reference the canonical reputation/COC infrastructure (`docs/22-AGENT-CARD-REPUTATION-SCHEMA.md`, `forensics/ORGANIZATION.md`, `scripts/9x_reputation_tracker.py`) so a reader can verify the empirical claims from the same evidence chain.

---

## Quick Links by Intent

### 🎯 Want to publish/research?
→ Go to [finalize](#-finalize) section below

### 🔬 Want to understand eval/metrics deep-dive?
→ Go to [analyze](#-analyze) section below

### ✏️ Want to review/annotate quality?
→ Go to [review](#-review) section below

### 📚 Want to learn/explore casually?
→ Go to [learn-explore](#-learn-explore) section below

---

## 📚 learn-Explore — Quick Entry Points

**For:** Casual users, newcomers, investors who want the quick version

| Doc | What it is | Start here |
|-----|-----------|-----------|
| [[QUICKSTART]] | Getting started in 5 min | YES |
| [[START-HERE]] | Full onboarding | YES |
| [[80-Publications/README]] | Publications overview | YES |
| [[nectar-narrative]] | What is NECTAR? (2 min read) | YES |
| [[00-SHARED/QUICKSTART]] | Vault quickstart | If exploring vault |

### Key Insights (Quick)
- **Composite health score:** 0.797 (improving +8.7%)
- **Throughput:** 164 tasks/session median
- **Multi-agent advantage:** +258% vs vanilla Claude

### New Tech Docs Added (May 2026)
- **[docs/55-EMERGENCE-AND-MUTATION-GLOSSARY]** — 32KB glossary of emergence terminology
- **[docs/88-DASHBOARD-ICON-GLOSSARY]** — Dashboard icons including Flow Friction Flags (🔥🎯💧)
- **[docs/FAERIE2-ARCHITECTURE-HONEY-INJECTION-TIMING]** — Honey injection architecture

---

## 🔬 analyze — Deep Metrics & Technical

**For:** Scientists, researchers, engineers who want the data

### Eval Reports & Metrics

| Doc | What it measures | Priority |
|-----|-----------------|----------|
| [[eval-report-2026-05-04]] | System eval, composite 0.797 | ⭐ PRIMARY |
| [[emergence-quality-metrics-system]] | Emergence quality framework | ⭐ PRIMARY |
| [[canonical-emergence-metrics]] | Canonical emergence metrics | Secondary |
| [[80-Publications/eval-report-2026-05-04]] | Same as above | Reference |

### Dimension Scores (from eval-report)

| Dimension | Score | Status |
|-----------|-------|--------|
| A — Throughput | 0.5 | Instrumenting |
| B — Memory | 0.667 | Hit rate unwired |
| C — Resilience | 1.0 | Ceiling artifact |
| D — Quality | 1.0 | Citation framework |
| E — Discovery | TBD | Not yet measured |
| F — Model Routing | TBD | Depends on roster |

### Key Findings

> **Throughput:** Real 164 tasks/session. But cost-per-finding and tokens-per-task are NOT YET WIRED. This is masking true capability.

> **Memory:** NECTAR corpus growing (240 lines). outcome_coverage_rate = 0.95. But we haven't measured whether agents actually USE memory (honey_hit_rate unwired).

> **Resilience:** 100% manifest coverage — BUT this is a ceiling artifact. Only 2 agents in roster, PostToolUse hook not populating properly.

### Formulas & Pseudo-System

| Doc | Purpose |
|-----|---------|
| [[03-CANONICAL-FAERIE-FORMULAS]] | Spawn formulas reference |
| [[faerie2-formulas.json]] | Living formula parameters |
| [[formula-living-system-narrative]] | How formulas evolved |
| [[00-SHARED/Hive/faerie2-pseudo-system-design-20260503]] | Pseudo-system design |

### Technical Deep-Dives (from /docs/)

| Doc | Focus | Key Insight |
|-----|-------|-------------|
| [[docs/55-EMERGENCE-AND-MUTATION-GLOSSARY]] | Emergence + mutation terminology | 32KB - comprehensive glossary |
| [[docs/88-DASHBOARD-ICON-GLOSSARY]] | Dashboard icon meanings | Flow Friction Flags explained |
| [[docs/AGENT-BUNDLE-EMISSION-INTEGRATION]] | Agent bundle emission | Prevents forensics bloat |
| [[docs/EVAL-NARRATIVE-BASELINE-FFMx-v2-2026-04-29]] | FFMx baseline eval | v2 baseline narrative |
| [[docs/FAERIE2-ARCHITECTURE-HONEY-INJECTION-TIMING]] | Honey injection timing | Architecture deep-dive |
| [[docs/ZIMABOARD-DEPLOYMENT]] | ZimaBoard setup | Deployment guide |
| [[docs/TIME-TRACKING-INTEGRATION]] | Time tracking | Integration documentation |
| [[docs/MIGRATION-MANIFEST-FAERIE2-SYNC]] | Faerie2 sync | Migration manifest |

### Forensics & COC Architecture

| Doc | Focus | Size |
|-----|-------|------|
| [[forensics/EPHEMERAL-CAPTURE-ARCHITECTURE]] | Ephemeral capture system | 21KB |
| [[forensics/EPHEMERAL-CAPTURE-SUMMARY]] | Capture summary | 10KB |
| [[forensics/COC-ENTRY-SCHEMA]] | Chain of Consciousness schema | 17KB |
| [[forensics/FFMX-EQUATION-SPECIFICATION]] | FFMx equations | 15KB |
| [[forensics/SYNC-COC-ARCHITECTURE]] | Sync + COC architecture | 21KB |
| [[forensics/FRONTMATTER-METADATA-INJECTION-RULES]] | Frontmatter rules | 15KB |

### Session & Droplet Data

| Folder | What's there |
|--------|--------------|
| [[00-SHARED/Droplets]] | Live agent insights |
| [[00-SHARED/Dashboards/session-briefs]] | Session emergence |
| [[00-SHARED/Daily]] | Daily agent outputs |

---

## ✏️ review — Annotations & Quality

**For:** Quality audit, annotations, design review

### Quality Frameworks

| Doc | Focus |
|-----|-------|
| [[emergence-quality-metrics-system]] | Quality of emergence scoring |
| [[canonical-emergence-metrics]] | Metrics definitions |
| [[80-Publications/canonical-emergence-metrics]] | Canonical version |

### Governance & Schema

| Doc | Purpose |
|-----|---------|
| [[VAULT-SCHEMA]] | Vault structure rules |
| [[00-SHARED/Dashboards/VAULT-STRUCTURE]] | Dashboard governance |
| [[COMPASS-FRONTMATTER-TEMPLATE]] | Frontmatter standard |

### Deprecations & Known Issues

- Multiple docs NOT updated to new frontmatter schema (see VAULT-STRUCTURE.md violations table)
- `mission_field` absent in almost all files
- `compass_edge` absent everywhere
- Day-folder pattern NOT fully adopted (loose files at root)

---

## 🎯 finalize — Publication Ready

**For:** Writing research papers, cutting-edge articles

### Research Paper Framework

| Doc | Status | Use for |
|-----|--------|---------|
| [[4x-RESEARCH-PAPER-OUTLINE]] | Active | Paper structure |
| [[80-AUTONOMY-SYCOPHANCY-FRAMEWORK]] | Active | Core framework |
| [[107-NARRATIVE-FAERIE-EVOLUTION]] | Active | Chronological narrative |

### Publication-Quality Docs

| Doc | What's here |
|-----|------------|
| [[02-CANONICAL-GLOSSARY]] | Complete terminology |
| [[03-CANONICAL-FAERIE-FORMULAS]] | Formula reference |
| [[formula-system-diagrams]] | Visual diagrams |
| [[nectar-narrative]] | NECTAR explanation |

### Key Narratives & Evolution

| Doc | Focus |
|-----|-------|
| [[107-NARRATIVE-FAERIE-EVOLUTION]] | Chronological evolution |
| [[DAE-Evolution-Narrative]] | Detailed evolution |
| [[Narratives/045-STIGMERGY-IN-ACTION-NARRATIVE]] | Stigmetry in action |

### Scripts & Tools (for reproducibility)

| Script | Purpose |
|--------|---------|
| [[scripts/7x_ffmx_calculator]] | FFMx formula calculations |
| [[scripts/7x_formula_gates]] | Formula gating logic |
| [[scripts/8x_time_estimate_analyzer]] | Time estimation |
| [[scripts/9x_honey_sync_to_vault]] | Honey to vault sync |

### Installation & Setup

| Doc | Purpose |
|-----|---------|
| [[install/ONBOARDING-NEW-USER]] | New user onboarding |
| [[install/PLUGIN-INSTALL-MATRIX]] | Obsidian plugin matrix |
| [[install/INSTALLATION-CHECKLIST]] | Installation checklist |

---

## What's Missing / Needs Work

Based on this roundup, gaps I've found:

1. **Eval metrics not fully wired:**
   - `honey_hit_rate` unwired — don't know if agents use memory
   - `tokens_consumed` unwired — cost-per-finding unknown
   - `subagent-roster.json` not populating — resilience inflated

2. **Schema violations:**
   - Many files missing `mission_field`, `compass_edge`, `hash`
   - Day-folder pattern partially adopted

3. **Dashboards:**
   - `Mission-Control.md` and `Nectar-View.md` are empty (0 bytes)
   - session-briefs/ and session-manifests/ have data but dashboards appear broken

---

## How to Use This Doc

1. **Decide your intent:** Which mode are you in right now?
2. **Navigate to section:** Click the link above
3. **Find relevant docs:** Table shows priority and purpose
4. **Dive in:** Start with PRIMARY docs for your intent

---

## Contributing

To add new publication docs to this roundup:
1. Add to appropriate intent section above
2. Update `updated` timestamp
3. Add to frontmatter `tags`
4. Recompute `doc_hash` after editing