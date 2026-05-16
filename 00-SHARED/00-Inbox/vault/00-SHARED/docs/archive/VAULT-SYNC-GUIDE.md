---
type: design-insight
status: final
created: 2026-04-05
updated: 2026-04-05
tags: [sync, syncthing, collab, vault, setup, cross-platform]
title: "Vault Sync Guide — Syncthing Setup for Cross-Platform Collaboration"
category: infrastructure
priority: high
system_area: sync
blueprint: "[[Design-Insight]]"
agent_type: documentation-engineer
doc_hash: "sha256:pending"
promotion_state: awaiting-annotation
---

# Vault Sync Guide — Syncthing Setup for Cross-Platform Collaboration

> **TL;DR:**
> - Syncthing keeps the Obsidian vault in sync across Windows, WSL, and ZimaBoard.
> - Add both Windows path (`D:\...`) and WSL path (`/mnt/d/...`) as separate Syncthing folders.
> - Conflict resolution: Windows GUI wins; WSL is read-mostly.
> - See the Syncthing web UI at `http://127.0.0.1:8384` to monitor sync status.
> - ZimaBoard is the off-site backup node — always-on, runs headless Syncthing.


Two investigators, two vaults, one shared layer. This guide sets up bidirectional sync of `00-SHARED/` only — private folders (01-PROTECTED/, 30-Evidence/) stay local.

---

## Section 1: Architecture Overview

```
Person A (Windows 11 + WSL2)          Person B (macOS / Linux)
─────────────────────────────          ──────────────────────────
CyberOps-UNIFIED\                      ~/CyberOps-Vault/
  01-PROTECTED\   ← local only           01-PROTECTED/  ← local only
  30-Evidence\    ← local only           30-Evidence/   ← local only
  00-SHARED\  ◄─── junction ───►  D:\Syncthing\CyberOps-SHARED\
                                         ▲
                                   Syncthing sync
                                         ▼
                               ~/Syncthing/CyberOps-SHARED/
                                         │
                                  symlink ▼
                               ~/CyberOps-Vault/00-SHARED/
```

**Why symlinks/junctions:** Syncthing syncs a flat folder. The junction/symlink lets Obsidian see `00-SHARED/` as part of its vault tree while Syncthing operates on it independently. Neither side's private folders are ever exposed to the sync layer.

**Ownership model at a glance:**

| Folder | Written by | Read by |
|---|---|---|
| Agent-Outbox/, Human-Inbox/, Droplets/, Dashboards/ | Person A's agents | Both |
| Queue/sprint-queue.md | Both humans | Agents (Person A) |
| 00-Inbox/ | Person B (QuickAdd) | Person A's agents |
| .ann.md files | Designated human | Both |

---

## Section 2: Person A Setup (Windows 11 + WSL2)

Syncthing runs natively on Windows — do not install it inside WSL.

**Step 1 — Install Syncthing**

Download the Windows installer from https://syncthing.net/downloads/ and run it. Syncthing will auto-start and open a browser at `http://localhost:8384`.

Alternatively via winget:
```powershell
winget install Syncthing.Syncthing
```

**Step 2 — Create the sync folder**

```powershell
New-Item -ItemType Directory -Path "D:\0LOCAL\Syncthing\CyberOps-SHARED" -Force
```

**Step 3 — Create a junction from the sync folder into the vault**

Run PowerShell as Administrator:
```powershell
New-Item -ItemType Junction `
  -Path "D:\0LOCAL\Syncthing\CyberOps-SHARED\00-SHARED" `
  -Target "D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED\00-SHARED"
```

Use Junction (not SymbolicLink) — Syncthing follows NTFS junctions reliably. Symlinks on Windows require Developer Mode or elevated privileges and behave inconsistently with Syncthing.

**Step 4 — Add folder in Syncthing UI (localhost:8384)**

1. Click "Add Folder"
2. Folder Label: `CyberOps-SHARED`
3. Folder Path: `D:\0LOCAL\Syncthing\CyberOps-SHARED`
4. Folder Type: `Send & Receive`
5. File Versioning: `Staggered File Versioning` — keep versions for 30 days
6. Under "Ignore Patterns", add:
   ```
   .obsidian
   .trash
   *.sqlite
   *.sqlite-shm
   *.sqlite-wal
   __pycache__
   *.pyc
   .DS_Store
   ```
7. Save

**Step 5 — Share with Person B**

1. Go to "Add Device" and enter Person B's Device ID (found in their Syncthing UI under Actions > Show ID)
2. After Person B accepts, share the `CyberOps-SHARED` folder with their device

---

## Section 3: Person B Setup (macOS / Linux)

**Step 1 — Install Syncthing**

macOS:
```bash
brew install syncthing
brew services start syncthing
```

Linux (Debian/Ubuntu):
```bash
sudo apt install syncthing
systemctl --user enable syncthing
systemctl --user start syncthing
```

Open `http://localhost:8384` to reach the UI.

**Step 2 — Create vault and sync directories**

```bash
mkdir -p ~/CyberOps-Vault/00-SHARED
mkdir -p ~/Syncthing/CyberOps-SHARED
```

**Step 3 — Create symlink**

```bash
ln -s ~/CyberOps-Vault/00-SHARED ~/Syncthing/CyberOps-SHARED/00-SHARED
```

Verify Syncthing is configured to follow symlinks: in the Syncthing UI go to the folder's Advanced settings and confirm "Follow Symlinks" is enabled (it is by default on Linux/macOS).

**Step 4 — Accept the shared folder**

1. Person A sends the share invitation (Step 5 above)
2. In your Syncthing UI, click "Add" when the folder appears
3. Set local path to: `~/Syncthing/CyberOps-SHARED`
4. Folder type: `Send & Receive`
5. Add the same ignore patterns as Person A

**Step 5 — Open in Obsidian**

Open `~/CyberOps-Vault/` as an Obsidian vault. The `00-SHARED/` folder will appear in the file tree, populated with everything from Person A.

---

## Section 4: Obsidian Setup (Both Sides)

**Required plugins (install via Settings > Community plugins):**

| Plugin | Purpose |
|---|---|
| Dataview | Query agent outputs by frontmatter — powers dashboards |
| QuickAdd | Fast task creation directly to Queue/ |
| Homepage | Opens HOME.md on vault launch (command center) |

**Settings (configure manually on both sides):**

- Templates folder: `templates/`
- Daily notes location: `00-Inbox/`
- Set Homepage target to `00-SHARED/Dashboards/HOME.md` (or local equivalent)

Do not sync the `.obsidian/` folder — plugin state, theme, and hotkey preferences differ per person. The ignore pattern above excludes it.

---

## Section 5: The Ownership Protocol (CRITICAL)

**One writer per file. This eliminates most conflicts before they happen.**

### Agent-owned files (Person A's agents write; both humans read)
- `Agent-Outbox/**`
- `Human-Inbox/**`
- `Droplets/**`
- `Dashboards/**`
- `Session-Briefs/**`
- `Hive/**`

Neither human edits these files directly.

### Human-owned files (humans write; agents read)
- `Queue/sprint-queue.md` — both humans may edit; rare simultaneous edits handled by Syncthing versioning
- `00-Inbox/**` — Person B's QuickAdd entries; Person A's agents consume these
- `LAUNCH/**` — collaborative documents; treat as shared-write (edit, then wait for sync)

### Annotation convention
To comment on an agent file without editing it:
```
Agent writes:  Agent-Outbox/analysis/network-map.md
You annotate:  Agent-Outbox/analysis/network-map.ann.md  ← sibling file, your name owns it
```
The `.ann.md` file links back to the original via `original_doc` in frontmatter. Agents never touch `.ann.md` files.

---

## Section 6: Conflict Prevention

Syncthing uses "last write wins" by default and surfaces conflicts as `.sync-conflict-YYYYMMDD-HHMMSS-deviceid` files.

**Why conflicts are rare with this system:**
- Agent outputs are write-once (agents create new files, never rewrite existing ones)
- Annotation files (.ann.md) are assigned to one person each
- Queue/ is the only high-risk shared-write file

**If a `.sync-conflict-*` file appears:**
1. Open both versions (original + conflict file)
2. Manually merge the content you want to keep
3. Save the merged content to the original filename
4. Delete the `.sync-conflict-*` file

**For Queue/ specifically:** If both people edit it simultaneously, Syncthing keeps both versions. Open both, merge the task lists, save to `sprint-queue.md`, delete the conflict file. This should happen at most once per week.

---

## Section 7: Testing the Sync

Run this checklist after completing setup on both sides.

1. **Person A writes a test file:**
   Create `00-SHARED/Agent-Outbox/sync-test.md` with any content.

2. **Person B confirms receipt:**
   Within 60 seconds (on LAN) or a few minutes (over internet), `sync-test.md` should appear in Person B's Obsidian vault under Agent-Outbox/.

3. **Person B writes a task:**
   Add a line to `00-SHARED/Queue/sprint-queue.md`: `- [ ] Test task from Person B`

4. **Person A confirms receipt:**
   Open `Queue/sprint-queue.md` — the task should be there.

5. **Agent output with frontmatter:**
   Person A's agents write a file with YAML frontmatter to `00-SHARED/Droplets/LIVE-test.md`. Person B confirms Dataview can query it (`type: droplet` etc.).

6. **Delete test files** after verification.

---

## Section 8: Troubleshooting

**Syncthing not following symlinks (Windows)**
Use a Junction, not a Symbolic Link. Junctions work without elevated privileges and Syncthing follows them by default on NTFS. To verify:
```powershell
Get-Item "D:\0LOCAL\Syncthing\CyberOps-SHARED\00-SHARED" | Select-Object LinkType
# Should return: Junction
```

**Syncthing not following symlinks (Linux/macOS)**
In the Syncthing folder's Advanced settings, ensure "Follow Symlinks" is checked. If still failing, use a bind mount instead:
```bash
# Add to /etc/fstab:
/home/user/CyberOps-Vault/00-SHARED  /home/user/Syncthing/CyberOps-SHARED/00-SHARED  none  bind  0  0
```

**Path case sensitivity**
Windows is case-insensitive; Linux/macOS are case-sensitive. Never create files that differ only by case (e.g. `Report.md` and `report.md`). If this happens, Syncthing will sync both but one OS will collapse them.

**WSL agents cannot see synced files**
The vault at `D:\0LOCAL\...` is accessible from WSL at `/mnt/d/0LOCAL/...`. Syncthing runs on the Windows side so it writes to `D:\`. WSL agents read/write at `/mnt/d/` — they see the same files. No special configuration needed.

**Large files slowing sync**
Keep the vault markdown-only. No binaries, no images larger than a few hundred KB. If you need to share a large file, put it in a separate Syncthing folder (not this one) and link to it by path.

**Firewall blocking sync**
Syncthing requires:
- TCP port 22000 (data sync)
- UDP port 21027 (local discovery)

On both machines, open these ports or set Syncthing to "Relay" mode (slower but works through firewalls without port forwarding).

**Syncthing shows "Out of sync" indefinitely**
Usually caused by a file locked by another process (Obsidian has it open) or a permissions issue. Check the Syncthing UI's "Failed items" list for the specific file and error.

---

## Section 9: Alternative Architecture (Send-Only / Stricter Control)

If you want to prevent any accidental overwrites across the boundary, use two directional folders instead of one bidirectional folder.

**Setup:**

Create two Syncthing shares:

| Share | Person A | Person B | Contains |
|---|---|---|---|
| `CyberOps-A-Sends` | Send Only | Receive Only | Agent-Outbox/, Droplets/, Dashboards/ |
| `CyberOps-B-Sends` | Receive Only | Send Only | Queue/, 00-Inbox/, .ann.md files |

**How:**
1. Separate the subfolders into two sync directories on each machine
2. Create two separate junctions/symlinks pointing to the appropriate vault subfolders
3. Configure each folder's type accordingly in Syncthing

**Trade-off:** More initial setup, zero risk of accidental overwrites. Recommended if the investigation involves sensitive material where a mistaken overwrite would be costly.

---

## Quick Reference

```
Person A vault:  D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED\
Sync folder:     D:\0LOCAL\Syncthing\CyberOps-SHARED\
Junction:        D:\0LOCAL\Syncthing\CyberOps-SHARED\00-SHARED
                 → D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED\00-SHARED

Person B vault:  ~/CyberOps-Vault/
Sync folder:     ~/Syncthing/CyberOps-SHARED/
Symlink:         ~/Syncthing/CyberOps-SHARED/00-SHARED → ~/CyberOps-Vault/00-SHARED

Syncthing UI:    http://localhost:8384 (both machines)
Sync port:       TCP 22000
Discovery port:  UDP 21027
```
