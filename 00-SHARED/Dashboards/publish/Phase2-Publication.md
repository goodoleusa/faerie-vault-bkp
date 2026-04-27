---
type: dashboard
stage: publish
tags: [dashboard, publication, writing, pre-publish]
description: Publication mode — section editing, website mirror, pre-publish checklist
updated: 2026-03-23
parent:
  - "[[HOME]]"
sibling:
  - "[[Phase1-AgentSync]]"
  - "[[Annotation-Dash]]"
doc_hash: sha256:bd3ee92a464b6eb4ce417d0ed1fc6c4775c04be7c916a28448309240eb9ab68e
hash_ts: 2026-03-29T16:10:00Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|← HOME]] · [[Phase1-AgentSync|← Investigation]] · [[Annotation-Dash|← Annotate]] · **Phase 2 — Publication**

# Phase 2 — Publication Dashboard

> **Mode:** Human-driven writing. Agents assist on demand.
> **Entry condition:** All Wave notes in Review status + Tier 1 covers H1-H4.

---

## 📄 Report Sections — Writing Status

| # | Section | Maps to | Status | Notes |
|---|---------|---------|--------|-------|
| 00 | Executive Summary | `report.html#executive` | ⬜ Not started | Write last |
| 01 | The Jan 14 Inflection | `report.html#inflection` + [[WAVE-01-The-Emergence]] | 📝 Draft in Wave | Needs prose polish |
| 02 | Infrastructure Overview | `report.html#infrastructure` + [[WAVE-02-The-Infrastructure]] | 📝 Draft in Wave | |
| 03 | Foreign Fingerprints | `report.html#foreign` + [[WAVE-03-The-Foreign-Fingerprints]] | 📝 Draft in Wave | |
| 04 | DOGE Malware | `report.html#malware` + [[WAVE-04-The-Malware]] | 📝 Draft in Wave | |
| 05 | Statistical Evidence | `report.html#statistics` | ⬜ Queued | Needs Wave-05 |
| 06 | Personnel | `report.html#personnel` | ⬜ Queued | Needs Wave-06 |
| 07 | Nuclear Triple | `report.html#nuclear` | ⚠️ Blocked | LLNL cert unverified |
| 08 | Technical Appendix | `report.html#appendix` | ⬜ Not started | |
| 09 | Executive Summary | `report.html#top` | ⬜ Write last | |

---

## 🌐 Website Pages — Content Readiness

| Page | File | Content Source | Ready? |
|------|------|---------------|--------|
| Main report | `report.html` | Sections 00-08 above | ⬜ |
| Network map | `map.html` | Evidence coords + viz feed | ✅ Live (Layer P added) |
| Timeline | `timeline-enriched.html` | viz_treasury_timeline.json | ✅ Live |
| Network graph | network graph page | viz_shodan_clusters.json | 🔧 Needs wiring |
| Admin | `admin.html` | — | ✅ |

---

## ✅ Pre-Publish Checklist

### Legal / Forensic
- [ ] All Tier 1 evidence reviewed and annotated by human
- [ ] COC export generated (`python3 scripts/coc.py export --format court`)
- [ ] Baseline reproducibility report clean (`scripts/baseline_reproducibility.py --report`)
- [ ] Agent card lint passes (`scripts/lint_agent_cards.py`)
- [ ] No named individuals without corroborated sourcing

### Content
- [ ] All 6 Wave notes in "Final" status
- [ ] Executive summary written (last)
- [ ] H5 null result clearly framed (not just "no evidence")
- [ ] Nuclear triple footnoted with current status (LANL confirmed, ORNL hostname only, LLNL pending)
- [ ] Statistical section includes Bonferroni correction explanation for lay readers

### Technical
- [ ] IPFS publish + OpenTimestamps (`/ipfs-publisher`)
- [ ] All internal links resolve
- [ ] Mirrors footer on every public page
- [ ] Mobile tested (Mullvad Browser target)

### Citations
```dataview
TABLE WITHOUT ID
  file.link AS "Finding",
  confidence_level AS "Conf",
  tier AS "Tier",
  hypothesis_support AS "H"
FROM "00-SHARED/Agent-Outbox" OR "00-SHARED/Human-Inbox"
WHERE (tier = 1 OR tier = "1") AND (ann_hash = null OR ann_hash = "")
SORT confidence_level DESC
```

---

## 📝 Section Notes (00-WORKSPACE)

> *Write prose here — agents read these to render HTML sections.*

- [[00-WORKSPACE/sections/01-inflection|01 · The Jan 14 Inflection]]
- [[00-WORKSPACE/sections/02-infrastructure|02 · Infrastructure]]
- [[00-WORKSPACE/sections/03-foreign-fingerprints|03 · Foreign Fingerprints]]
- [[00-WORKSPACE/sections/04-malware|04 · DOGE Malware]]
- [[00-WORKSPACE/sections/05-statistics|05 · Statistical Evidence]]
- [[00-WORKSPACE/sections/06-personnel|06 · Personnel]]
- [[00-WORKSPACE/sections/07-nuclear-triple|07 · Nuclear Triple]]
- [[00-WORKSPACE/sections/08-appendix|08 · Technical Appendix]]
- [[00-WORKSPACE/sections/00-executive-summary|00 · Executive Summary (write last)]]

---

## 🔗 Navigation

- [[Annotation-Dash]] — Smoking guns, your annotations, court prep
- [[Phase1-AgentSync]] — Switch back here if new findings come in
- [[Hypothesis-Tracker]] — Per-hypothesis evidence
