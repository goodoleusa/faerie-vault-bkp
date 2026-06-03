---
date: 2026-05-22
author: openhands-agent
related_mission: vault-dashboard-crystallize
status: synthesis-log
---

# Vault Dashboard Audit — what to deprecate, focus, build

User: "find all dashboards in faerie-vault and consider what to
deprecate, what to focus on and build etc"

## Inventory (5 dashboards found)

| Dashboard | Path | Last touched | Verdict |
|---|---|---|---|
| **Publishing Dashboard** (NEW) | `00-SHARED/PUBLISHING-DASHBOARD.md` | 2026-05-22 (today) | **FOCUS** — this is the human-final-gate surface |
| **Mission-Control (Hive)** | `00-SHARED/Hive/Mission-Control.md` | 2026-05-04 (≈18 days stale) | **REVIVE** — bring to life via live MCP polling, or DEPRECATE if Publishing Dashboard covers the workflow needs |
| **Mission-Control (Emerg Deep-Dives)** | `00-SHARED/Emerg Deep-Dives/Mission-Control.md` | 2026-05-04 (DUPLICATE of the Hive one) | **DEPRECATE** — exact content duplicate; redirect to the Hive copy or kill |
| **Dev-Eval Index** | `00-SHARED/Emerg Deep-Dives/Dev-Eval/index.md` | 2026-05-04 | **MERGE** — eval surfaces should live under the new `Tune` tab in V0 dashboard, not as a vault static index. Keep as a historical archive. |
| **2026-04-28 Vault Ops Dashboard** | `2026-04-28/00-DASHBOARD.md` | 2026-04-28 (1 month stale) | **ARCHIVE** — useful as forensic record, not as current navigation. Move to `_archive/` subdir of that date folder. |
| **2026-04-28 Vault Maintenance** | `2026-04-28/archive/10-vault-maintenance.md` | superseded 2026-04-30 | **KEEP-AS-IS** — already self-marks `status: archived`. Working as intended. |

## Recommendations

### FOCUS (1 dashboard — the one)

**`00-SHARED/PUBLISHING-DASHBOARD.md`** is the new canonical. It's
already designed for the right purpose: the human-final-gate for the
cybertemplate site (and any data-→-narrative-→-publish flow). Pin it
in Obsidian (right-click → Pin tab). Open it first every session.

What to add next (concrete):

1. **Live AI session summary block** — a Dataview query that surfaces
   the last 5 agent-authored items with their `dashboard_line` field
   so you see WHAT THE SWARM did today without leaving the dashboard.
2. **cybertemplate stage tracker** — a section that polls
   `cybertemplate/data/timelines/00-master/curated/` and lists
   timeline events by tier (Tier 1 smoking gun count vs Tier 2 vs
   Tier 3) so you see what's curated vs what's still raw.
3. **AI ↔ human handoff badge** per item — a single icon column in
   the Dataview that shows whether an item is waiting on YOU
   (annotate) or waiting on an AGENT (re-analyze, more research).

### DEPRECATE (3 dashboards)

1. **`00-SHARED/Emerg Deep-Dives/Mission-Control.md`** — exact duplicate
   of `00-SHARED/Hive/Mission-Control.md`. Replace with a one-line
   redirect: `> See [[../Hive/Mission-Control]]`.

2. **`2026-04-28/00-DASHBOARD.md`** — historical forensic; move to
   `2026-04-28/_archive/00-DASHBOARD.md` so it doesn't compete with
   the new Publishing Dashboard for the "00" sort slot.

3. **Auto-generated Mission-Control content** — the 2026-05-04
   timestamp tells the story: it was generated once, never updated.
   Either wire it to MCP `dashboard_overview` for live data, OR
   delete the static file (Publishing Dashboard + the `swarmy-status`
   CLI cover the same needs).

### REVIVE (1 dashboard)

**`00-SHARED/Hive/Mission-Control.md`** — keep this name + location
but RE-GENERATE it nightly via cron from the MCP `dashboard_overview`
tool, so the live numbers are always fresh. Currently it's a fossil.

Implementation: add `swarmy-mission-control-refresh` to the alias
suite + a cron entry in `deploy/scripts/install-crons.sh`. The cron
calls the MCP tool, pipes the JSON through a Jinja template, writes
the .md file. Then Obsidian shows current numbers without manual
intervention.

### BUILD (2 net-new)

1. **`00-SHARED/CYBERTEMPLATE-STAGE-DASHBOARD.md`** — sister to the
   Publishing Dashboard but scoped specifically to the cybertemplate
   investigation. Shows:
   - Tier-1/2/3 evidence counts (smoking gun, strong, contextual)
   - Open promotions in the COC chain
   - Charter status for cybertemplate-specific charters
   - Stages: data-curated → narrative-drafted → human-annotated →
     site-published
   This decouples cybertemplate-specific needs from the generic
   Publishing Dashboard.

2. **`00-SHARED/WEEKLY-SYNTHESIS-DASHBOARD.md`** — pull from
   `forensics/coc.jsonl` + the past 7 days of daily folders to surface
   themes, recurring missions, sealed creatures, and items that
   accumulated multi-day attention. The vault-daily skill writes
   per-day; this surface aggregates weekly.

## Three-tier dashboard hierarchy (the proposed canonical)

```
TIER 1 (the daily) — opens first, every session
└── 00-SHARED/PUBLISHING-DASHBOARD.md
    "What needs my eyes today?"

TIER 2 (the project-scoped) — opened for specific work
├── 00-SHARED/CYBERTEMPLATE-STAGE-DASHBOARD.md      (NEW)
├── 00-SHARED/Hive/Mission-Control.md                (REVIVED — live)
└── 00-SHARED/Emerg Deep-Dives/Dev-Eval/index.md     (archive)

TIER 3 (the weekly aggregate) — Sunday review
└── 00-SHARED/WEEKLY-SYNTHESIS-DASHBOARD.md         (NEW)
```

Three is the right number. Six dashboards is too many to maintain;
two leaves gaps. The current vault has scattered N-of-many — this
trims to a focused hierarchy.

## Plugin-pinning recommendation (Obsidian-side)

Open Obsidian → Settings → Community plugins → enable + pin in this
order (drag the pinned tabs to the top of the sidebar):

1. **PUBLISHING-DASHBOARD.md** (always-on)
2. **Longform** (book-style writing surface for narratives)
3. **Dataview** (powers all the queries)
4. **Templater** (auto-frontmatter for new notes)
5. **Obsidian Git** (auto-commit; you don't think about it)
6. **swarmy-hive-plugin** when it ships (manifest + mission graph in Obsidian)

Hide everything else from the left rail. The goal: when you open
Obsidian, your eyes land on the Publishing Dashboard and the
Longform manuscript view — nothing else competes.

## Next moves

1. Pin Publishing Dashboard in Obsidian
2. Decide on the deprecations (which to delete/archive/redirect)
3. Plant the seed for the two NEW dashboards (Cybertemplate Stage,
   Weekly Synthesis) — these are good ~1-hour spawns once the
   Recursive Canvas + Frontier MAKER work has fully landed

---

*Audit completed 2026-05-22. Source-of-truth on the new dashboard
hierarchy: this file + `00-SHARED/PUBLISHING-DASHBOARD.md`.*
