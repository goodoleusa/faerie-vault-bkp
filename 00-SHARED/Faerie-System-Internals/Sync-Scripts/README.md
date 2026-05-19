---
type: internals-readme
title: "Sync scripts — crystallization machinery"
emoji: "⚙️"
N: ['[../00-Home](../00-Home.md)']
S: ['[../../HELP/crystallization-workflow](../../HELP/crystallization-workflow.md)']
E: ['[../Formulas](../Formulas)', '[../Spawn-Bundles](../Spawn-Bundles)']
W: ['[../../Dashboards/00-Home](../../Dashboards/00-Home.md)']
tags: [internals, sync, crystallization]
---

# ⚙️ Sync scripts

Canonical home: `faerie2/scripts/dev/vault/`. This page documents what each
script does and its status.

| Script | Status | Purpose |
|---|---|---|
| `06-daily-mirror.py` | ✅ active | Pulls `forensics/ephemeral/{date}/` into vault `Daily/{date}/`. Drafts demoted if no source manifest. |
| `09-internals-sync.py` | ✅ active | Re-renders `Faerie-System-Internals/` from canonical sources. Stale templates auto-purge. |
| `10-crystallize.py` | 🟡 queued (task #39) | Crystallizer: sibling-detect + merge + write Honey droplet + retire siblings with `superseded_by:`. |
| `11-weekly-digest.py` | 🟡 queued (task #40) | Roll Daily folders >30d into `Weekly/{YYYY-Www}/`. |
| `12-monthly-digest.py` | 🟡 queued (task #40) | Roll Weekly folders >90d into `Monthly/{YYYY-MM}/`. |
| `13-annual-anchor.py` | 🟡 queued (task #40) | Promote year-stable principles into `Anchors/`. |

All scripts read source-of-truth from `faerie2/forensics/` and write into
this vault. None mutate forensic state in-place — promotion is the only path
canonical → canonical, and it's gated by hooks.
