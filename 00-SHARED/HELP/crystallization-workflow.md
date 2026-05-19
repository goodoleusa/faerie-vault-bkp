---
type: help
title: "Crystallization workflow — read the crystals, not the volume"
emoji: "💎"
tags: [path/onboarding, help, crystallization]
path-step: 5
summary: "How the voluminous→crystallized cycle works in your vault, and how to read it."
N: ['[hive-plugin-tutorial](hive-plugin-tutorial.md)']
S: ['[../Dashboards/00-Home](../Dashboards/00-Home.md)']
E: ['[../Anchors/_index](../Anchors/_index.md)', '[../Honey/_index](../Honey/_index.md)']
W: ['[plugin-install-checklist](plugin-install-checklist.md)']
---

# 💎 Crystallization workflow

> Canonical principle: [CRYSTALLIZATION-DISCIPLINE.md](https://github.com/Persistech/faerie-hive-plugin/blob/main/docs/CRYSTALLIZATION-DISCIPLINE.md) in `faerie-hive-plugin`.

## What it feels like as a user

You annotate freely. Agents write generously. The vault looks busy at
the end of a long session — and that is the point. **Don't curate the
volume.** The cycle does that.

By the next morning, the noise has been distilled. You don't reread
twelve takes on a problem; you read one droplet that survived.

🐝 → 🌼 → 🍯 → 💎

## The lifecycle ladder

Each rung is a folder under `00-SHARED/`. Notes flow downward by age,
upward by importance.

| Tier | Folder | When | Retention |
|---|---|---|---|
| 📌 Daily | `Daily/{YYYY-MM-DD}/` | atomic notes, mirrored from forensics ephemeral | indefinite, rolled at 30d |
| 🗓️ Weekly | `Weekly/{YYYY-Www}/` | 30d+ digests | indefinite, rolled at 90d |
| 📆 Monthly | `Monthly/{YYYY-MM}/` | 90d+ digests | indefinite, promoted at 1y |
| ⚓ Anchors | `Anchors/` | durable principles | **permanent** |
| 🍯 Honey | `Honey/{YYYY-MM-DD}/` | crystallized droplets | indefinite |
| 📜 Charters | `Charters/` | declared intent | **permanent** |

## How to read the crystals

**Start at the top, drill down only when you need detail:**

1. Open `Dashboards/00-Home.md` — the daily landing.
2. Skim the **Lifecycle ladder** section (this week's digest, this
   month's, anchor set).
3. Tap into `Anchors/` to see what principles currently hold.
4. Tap into `Honey/` for crystallized session memory.
5. Only descend into `Daily/` when you want the raw atomic record.

If the crystals feel wrong, drop a `> [!charter]` callout proposing the
new shape. The next cycle reconciles.

## The mindset — trust the cycle

The anti-bloat is structural, not behavioral. You don't have to clean
up. Sync scripts (planned + active under
`Faerie-System-Internals/Sync-Scripts/`) run the refinement pass. Your
job is to **read**, not to file.

## Where this is enforced

- Forensic source of truth: `faerie2/forensics/`
- Vault mirror: this repo, `00-SHARED/`
- Sync scripts: `scripts/dev/vault/06-daily-mirror.py` (active),
  `10-crystallize.py` / `11-weekly-digest.py` / `12-monthly-digest.py` /
  `13-annual-anchor.py` (queued — tasks #39, #40).

See also: [[../Faerie-System-Internals/Sync-Scripts/README]].
