# Mobile Obsidian — Vault Prep Guide

> Read this before opening the vault on your phone for the first time.
> The vault was authored desktop-first; a few small changes make it
> phone-survivable.

## Vault inventory (top-level, post-2026-05-23 rename)

```
00-Inbox/         ← daily landing zone for new notes (mobile-friendly)
00-Publications/  ← finished narratives, papers, reports (was 80-Publications)
00-SHARED/        ← cross-folder linked resources (Daily, Templates, etc.)
01-Memories/      ← session memories + crystallized recall
01-PROTECTED/     ← operator-private; do NOT share
02-Skills/        ← agent skill files (mostly used by sub-agents, not humans)
03-Agents/        ← agent persona definitions
10-Investigations/← long-running investigation hubs
Blueprints/       ← reusable structure templates
Dashboards/       ← live data views (Dataview / MetaBind queries)
Excalidraw/       ← visual brainstorm files (DESKTOP-PRIMARY — heavy on mobile)
Narratives/       ← long-form writing in progress
Tags/             ← tag-page index
Templates/        ← QuickAdd + Templater sources
forensics/        ← signed evidence chain (read-only on mobile recommended)
docs/             ← vault meta-documentation
install/          ← bootstrap scripts (desktop-only)
scripts/          ← maintenance scripts (desktop-only)
copilot/          ← AI-pair-coding scratch (mostly outdated; review for archive)
stray/            ← unsorted (target for cleanup)
0dotclaude/       ← legacy .claude content (target for archive)
```

## What's mobile-friendly out of the box

Read freely on your phone:

- `00-Inbox/` — capture quick thoughts; the desktop later resolves them into permanent locations
- `00-Publications/` — your finished writing, including the new honey-mesh narrative
- `00-SHARED/Daily/` — daily journal (one note per day)
- `01-Memories/` — recall what you crystallized
- `Narratives/` — drafts in progress
- `Tags/` — find things by tag
- `docs/` — vault meta-docs (Compass, Architecture, etc.)

## What to skip on mobile (don't open these directly)

| Folder | Why |
|---|---|
| `Excalidraw/` | Excalidraw files are heavy + the mobile renderer is slow. View on desktop. |
| `forensics/` | Signed COC chain; mobile shouldn't write here. Read-only via the swarmy-hive-plugin's chip preview is fine. |
| `Dashboards/` | Dataview queries that scan the whole vault — slow on mobile. The chip preview shows the top-of-each-dashboard summary; tap to open only when needed. |
| `01-PROTECTED/` | Operator-private content; mobile leak risk if your phone gets borrowed. Consider not syncing this folder at all (see "Selective sync" below). |
| `scripts/`, `install/`, `0dotclaude/`, `stray/`, `copilot/` | Meta-infrastructure; you don't read these from the phone. |

## Selective sync — don't sync the whole vault to mobile

If your full vault is >1 GB (likely with Excalidraw + forensics), sync
**only what you'll actually open on the phone.** Obsidian-Git on mobile
isn't a "git clone the whole thing" model — you can use sparse-checkout
to skip heavy folders.

On desktop, set up a mobile-specific branch with sparse-checkout:

```bash
cd /mnt/d/0local/gitrepos/faerie-vault

# Create a mobile branch
git checkout -b mobile

# Configure sparse-checkout to include only mobile-friendly folders
git sparse-checkout init --cone
git sparse-checkout set \
  00-Inbox \
  00-Publications \
  00-SHARED \
  01-Memories \
  Narratives \
  Tags \
  Templates \
  docs

# Verify what's included
git sparse-checkout list

# Push the mobile branch
git push -u origin mobile
```

Then on the phone's Obsidian Git plugin, clone the `mobile` branch
instead of `main`. You get ~15% of the vault size; everything you
actually need on the go.

When you want desktop-edited content on mobile, merge `main` into
`mobile` periodically:

```bash
# Desktop:
git checkout mobile
git merge main
git push
# Phone:
# Pull in Obsidian-Git command palette: "Obsidian Git: pull"
```

## Recommended plugins on mobile

Per `MOBILE-OPTIMIZATION.md` in swarmy-hive-plugin: **install only
swarmy-hive-plugin and Obsidian Git on mobile.** Skip everything else.

- swarmy-hive-plugin absorbs ~10 plugins' worth of functionality with
  mobile-aware gating (heavy features auto-skip on mobile).
- Obsidian Git handles the sync.

That's it. Two plugins = stable mobile boot. If you have other plugins
already enabled in this vault profile, disable them on mobile via the
plugin's mobile-toggle setting (Obsidian → Settings → Community plugins →
each plugin → "Don't load on mobile").

## Daily mobile workflow

1. **Open Obsidian.** Pull on startup (auto if configured per
   `docs/OBSIDIAN-GIT-MOBILE-SETUP.md`).
2. **Capture.** Write to `00-Inbox/{YYYY-MM-DD}-{slug}.md`. Don't try to
   organize on the phone; let the desktop session sort it later.
3. **Read.** `00-Publications/` for finished work, `01-Memories/` for
   recall, `Narratives/` for drafts. Use the swarmy-hive-plugin chip
   previews so links to forensics/manifests render their content
   inline without opening the heavy folder.
4. **Push.** Manual push via command palette: "Obsidian Git: push." Set
   sync interval = 0 (manual only) until you're confident the auto-push
   isn't causing conflicts.

## Conflict handling on mobile

You will eventually edit the same note on desktop and phone before
syncing. The plugin handles simple cases; complex conflicts need desktop
resolution.

Pattern:
1. If `git pull` on phone shows a conflict, **don't try to resolve on
   the phone.** The conflict markers will mangle in the Obsidian editor.
2. Switch to desktop, `cd vault && git fetch && git status` to see the
   conflict, resolve there, commit + push.
3. On phone: "Obsidian Git: pull" to re-sync.

## Backup-before-mobile checklist

Before first mobile sync, do this once on desktop:

```bash
cd /mnt/d/0local/gitrepos/faerie-vault
git status                   # clean working tree?
git push origin main         # remote is up to date?
git log -5 --oneline         # last few commits look right?
du -sh .                     # vault size (likely 200MB-2GB)
```

Then the mobile clone:

- iOS: pull straight into the Obsidian app's storage; ~200MB-1GB vault should clone in 5-10 min on WiFi.
- Android: same; consider cloning over USB-tethered desktop if WiFi is slow.

Once mobile is synced, you're set. Daily workflow above; resolve
conflicts on desktop.

## See also

- `docs/OBSIDIAN-GIT-MOBILE-SETUP.md` (in the swarmy-hive-plugin repo) — Obsidian Git plugin install + PAT setup
- `swarmy-hive-plugin/docs/MOBILE-OPTIMIZATION.md` — why one plugin instead of ten
