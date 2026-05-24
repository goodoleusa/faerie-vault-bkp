---
type: dashboard
tier: insights
title: "Publication-Worthy Insights — Serious-Interest Surface"
status: live
cssclasses: [wide-page, dashboard-insights]
refresh_cadence: per-session
S: ['[[07-Publishing-Workflow]]']
N: ['[[00-Home]]']
E: ['[[02-Missions-Emergent]]', '[[03-Anchors]]', '[[04-Eval-Dimensions]]', '[[05-Stigmergy]]']
tags: [dashboard, insights, publication, serious-interest, swarmy]
---

> **🐝 Navigate:** [[00-Home]] · [[01-Today]] · [[02-Missions-Emergent]] · [[03-Anchors]] · [[04-Eval-Dimensions]] · [[05-Stigmergy]] · **[[06-Publication-Worthy-Insights|6 Insights]]** · [[07-Publishing-Workflow|7 Publishing]]

# Publication-Worthy Insights

Insights worth turning into a publication. Surfaces high-signal observations
across the swarm: structural realizations, unexpected emergence patterns,
failures-with-lessons, design principles that earned their keep. The 60-second
question: *would a smart outsider be glad they read this?*

---

## 🎯 The bar

An insight is publication-worthy when ONE of the following is true:

1. **It articulates a principle** that applies across many specific cases (e.g., "discipline is fractal across scopes")
2. **It captures a failure-mode** in plain language so others (or future-you) recognize it (e.g., "confabulation at liftoff")
3. **It surfaces an emergent property** that wasn't in the design (e.g., "agents autonomously authored vault publications")
4. **It documents a design decision with its full reasoning** (e.g., "cluster_prefix as both routing key and scope fence")
5. **It catches the system catching itself** (e.g., "the agent caught the parent")

If a note doesn't meet at least one bar, it goes in [[01-Today]] or [[../../Daily/_index]] but NOT here.

---

## 🌟 Today's publication-worthy surface (2026-05-21)

Auto-listed from `00-Publications/2026-05-21_*.md`:

```dataview
TABLE
  default(title, file.name) AS "Title",
  default(status, "—") AS "Status",
  default(tags, "—") AS "Tags",
  file.size AS "Size (bytes)"
FROM "00-Publications"
WHERE startswith(file.name, "2026-05-21")
SORT file.name ASC
```

**Manual roll-call** (in case dataview isn't installed yet — the bundling agent will eventually vendor it):

| # | Title | Bar met |
|---|---|---|
| 1 | [[../../00-Publications/2026-05-21_catching-silent-failures-in-swarm-intelligence\|Catching Silent Failures in Swarm Intelligence]] | 2 (failure modes) + 3 (emergent property — agents gaslight themselves silently) |
| 2 | [[../../00-Publications/2026-05-21_two-operating-modes-evo-vs-monkeybranching\|Two Operating Modes — Evo-wave vs Monkeybranching]] | 1 (operating mode principle) + 4 (deliberate design choice) |
| 3 | [[../../00-Publications/2026-05-21_forensic-hybrid-ledger-architecture\|Forensic Hybrid Ledger Architecture]] | 1 (architectural principle: consensus tax) + 4 (full design reasoning) |
| 4 | [[../../00-Publications/2026-05-21_charters-as-maps-and-journeys\|Charters as Maps and Journeys]] | 1 (charters = vision + journey, not TODO) |
| 5 | [[../../00-Publications/2026-05-21_the-discipline-becomes-the-product\|The Discipline Becomes the Product]] | 1 (the rituals ARE the product) + 3 (emergent: tooling-for-self becomes product-for-others) |
| 6 | [[../../00-Publications/2026-05-21_the-agent-caught-the-parent\|The Agent Caught the Parent]] | 5 (the system catching itself) + 3 (emergent: discipline flowing upward) |
| 7 | [[../../00-Publications/2026-05-21_graceful-deprecation-queue-as-stigmergic-handoff\|Graceful Deprecation Queue]] | 1 (handoff primitive) — agent-authored |
| 8 | [[../../00-Publications/2026-05-21_what-fifteen-agents-picked\|What Fifteen Agents Picked]] | 3 (early data from new ritual) + 4 (the choice tier system) |
| 9 | [[../../00-Publications/2026-05-21_the-phases-inside-the-phase\|The Phases Inside the Phase]] | 1 (lifecycle is fractal across scopes) |
| 10 | [[../../00-Publications/2026-05-21_the-first-goodbye\|The First Goodbye]] | 5 (agent agency in action) + 3 (emergent kind use) |
| 11 | [[../../00-Publications/2026-05-21_session-metrics\|Session Metrics — 2026-05-21]] | 4 (the canonical metric snapshot, citable) |

---

## 🔮 Candidates not yet promoted (watch list)

Things observed today that COULD be publication-worthy but haven't yet been written up:

- **Meta-schema's downward symmetry** — the canonical-doc.meta.schema.json now declares `canonical_tier{agents, humans}` as audience-aware authority. Same doc can be canonical for one audience, non-canonical for another. That's a non-trivial design idea worth its own piece.
- **"One mandatory plugin" principle** — vendor + credit beats depend + manage. The vault-utils-bundling work makes this concrete. Worth a piece once the bundling agent lands.
- **The W4W ("write 4 weeks") pattern** if it shows up in code — agents writing future work into bundles that wake up at the right time.
- **The blueprint auto-render loop** — when it ships, the JSON+MD sidecar + frontmatter `blueprint:` pattern is worth articulating as a general "live-rendering canonical artifacts" principle.

Move from watch-list → publication when you've earned a clear opinion + can write the orientation test (cold reader, 60 seconds).

---

## 📊 Insight-density signals (from forensic record)

Heuristics that surface high-signal moments worth examining:

| Signal | What it indicates | Where to look |
|---|---|---|
| Multi-agent convergence on same `promote` target | Charter elevation candidate | `forensics/ephemeral/{date}/*/manifest_*.json` |
| First-use of a new completion_choice kind | Agency expanding | The "kinds used" diversity score in [[04-Eval-Dimensions]] |
| Rationale length > 1000 chars at sensitive tier | Agent thought hard; worth reading the rationale | grep `_evolution_log` for length |
| Agent autonomously writes to `00-Publications/` | Spontaneous narrative; worth promoting | `gh log --since` filter for new pubs |
| Rollback rate spikes on a charter | The work is fighting something; write the lessons | `_evolution_log[].rollback` count |
| Hook rejection event | Discipline catching drift in real time; worth a piece | `forensics/coc.jsonl` filter `event: hook_rejection` |

---

## ✍️ Promotion workflow (insight → publication)

When you decide an insight is worth publishing, hand off to [[07-Publishing-Workflow]] which walks you through:
draft → fact-check → sign-off → mirror to vault → mirror to repo inspiration/ → optional external publish.

---

*The serious-interest surface. Updated each session-end. If an insight passes the 60-second orientation test, it belongs here; if it doesn't, it belongs in [[01-Today]] or daily notes.*
