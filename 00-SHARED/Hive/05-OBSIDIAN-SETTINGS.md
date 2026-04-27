---
type: meta
tags: []
doc_hash: sha256:a2f28cacd7f1b9a446aeac1b020756c07ad38469034580456455385f36b920de
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---
# CyberOps Vault — Obsidian Settings Reference

Opinionated baseline for this vault. Covers every setting category that matters.
Apply these before doing serious work — some defaults actively fight the agent pipeline.

---

## 1. Files & Links  (Settings → Files & Links)

| Setting | Value | Why |
|---|---|---|
| Default location for new notes | `00-Inbox` | Only affects Ctrl+N (human new-note button) — see note below |
| New link format | **Relative path** | Vault is portable; absolute paths break when moved |
| Use `[[Wikilinks]]` | **OFF** | Agents write `[text](../path.md)`; markdown links work everywhere including scripts |
| Automatically update internal links | ON | When you move a file, links stay valid |
| Detect all file extensions | ON | Shows `.py`, `.sh`, `.json` in file browser — useful for numbered scripts |
| Excluded files | `scripts/.hash_snapshots` | Hide hash snapshot dirs from indexing (noise) |

> **On "default location for new notes"**: This ONLY applies when you press Ctrl+N or click
> the new-note button in Obsidian's UI. It has zero effect on:
> - Agents (write directly to filesystem with explicit paths — `20-Entities/People/John-Doe.md`)
> - QuickAdd macros (each macro specifies its own destination folder)
> - Blueprint (assigns templates per folder; explicit destination)
>
> Agents routing their files to the right folder is controlled by the **vault folder map in
> their context prompt** (loaded from `00-META/AGENT-SYSTEM-ARCHITECTURE.md` via T1 tier),
> not by any Obsidian setting. If an agent puts something in the wrong place, the fix is
> updating the context, not the Obsidian setting.
>
> `00-Inbox` as default is only for your own quick-capture notes that you haven't categorized yet.

> **On wikilinks**: Turn them OFF so all links are portable markdown links with relative paths.
> Agents produce relative markdown links. Obsidian renders both — you lose nothing visually.
> If you want wikilinks for speed when typing, use QuickAdd to insert them,
> but keep the setting OFF so new links default to portable format.

### Attachment location
`Settings → Files & Links → Default location for new attachments`
Set to: `30-Evidence` — screenshots, PDFs, images from investigations land here automatically.

### Navigation properties (parent / sibling / child)

Hub notes use **YAML properties** with **quoted wikilinks** so Obsidian Properties stay clickable:

```yaml
parent: "[[VAULT-INDEX]]"
sibling: "[[00-SHARED/00-SHARED]]"
child: "[[HOW-SYNC-WORKS]]"
```

Convention and examples: **[[FRONTMATTER-WIKILINKS]]**.

---

## 2. Editor  (Settings → Editor)

| Setting | Value | Why |
|---|---|---|
| Default editing mode | **Source mode** | Agents write raw markdown; source mode shows exactly what they wrote |
| Spellcheck | OFF | IPs, domains, hashes, hex strings — all false positives |
| Auto-pair brackets | ON | Useful for frontmatter YAML and markdown |
| Fold heading | ON | Long investigation notes need folding |
| Fold indent | ON | Nested bullet folding for entity stubs |
| Readable line length | ON | Easier to read long reports |
| Show frontmatter | **ON** (source) / OFF (reading) | You need to see/edit frontmatter in source; reading view cleaner without it |
| Line numbers | ON | Helps when referencing agent output by line |
| Vim key bindings | your call | Only ON if you use vim; OFF otherwise |

---

## 3. Core Plugins — Enable These

| Plugin | Setting | Notes |
|---|---|---|
| **Templates** | ON | Folder: `Templates` — must match QuickAdd template path setting |
| **Backlinks** | ON | See what links to every entity/investigation |
| **Outgoing links** | ON | See all links in current note — good for entity stubs |
| **Graph view** | ON | Network visualization — configure below |
| **Tags** | ON | Tag pane for browsing by tag |
| **File recovery** | ON | Auto-snapshot every 5 min, keep 7 days — safety net |
| **Bookmarks** | ON | Pin: `Dashboards/Hypothesis-Tracker.md`, `00-Inbox/`, `01-Memories/agents/REVIEW-INBOX.md` |
| **Search** | ON | Essential |
| **Quick switcher** | ON | Cmd/Ctrl+O to jump to any file |
| **Page preview** | ON | Hover-preview wikilinks and markdown links |
| **Canvas** | ON | Useful for timeline and network layouts |
| **Daily notes** | OFF | Not part of this workflow — 60-Chronology has its own structure |
| **Slides** | OFF | Not needed |
| **Audio recorder** | OFF | Not needed |

---

## 4. Community Plugins — Install These

Install via Settings → Community plugins → Browse.

### Essential

**Dataview**
The most important plugin for this vault. Lets you query notes like a database.
- Enable JavaScript queries: ON
- Inline queries: ON
- Example use: `table status, priority from "00-Inbox" where type = "task"`

**QuickAdd**  (already configured — see `02-QUICKADD-SETUP.md`)
- Template folder: `Templates`
- All templates are plain `.md` files in `Templates/` — no Templater syntax
- QuickAdd macros handle date injection via `{{DATE}}`, `{{NAME}}`, `{{VALUE}}`

**Blueprint**  (already configured)
- Folder-level templates: assign a template per folder so new notes in that folder auto-populate
- Set `20-Entities/People/` → `Templates/T-STUB-person.md`
- Set `40-Intelligence/` → `Templates/T-PRODUCT.md`
- Set `30-Evidence/` → `Templates/T-PRODUCT-evidence.md`

**Metadata Menu**
Structured frontmatter editing. Adds dropdowns/pickers for typed fields.
- Set field types for: `status`, `priority`, `type`, `confidence`
- Maps to your entity and task frontmatter schemas

### Recommended

**Advanced Tables**  — Better pipe table editing (Tab to move between cells)

**Kanban**  — Drag-drop task board from any folder of `.md` files. Use on `00-Inbox/`.

**Calendar**  — Shows note counts by day. Good for seeing when agents were active.

**Obsidian Git**  — Auto-commit vault to git on schedule (useful if you add Git archival)

**Tag Wrangler**  — Rename/merge tags across entire vault at once

### Skip for now

- Excalidraw — heavy, not needed
- Kindle highlights — not relevant
- Obsidian Publish — not applicable

---

## 5. Graph View — Configure Filters

Open Graph View → click gear icon (top right of graph).

### Filters (hide these from graph — noise)
```
file.path: "scripts/"
file.path: "Templates/"
file.path: "Blueprints/"
file.path: ".hash_snapshots/"
file.path: "99-Archives/"
```

### Display
- Node size: **Links** (nodes with more connections = larger)
- Link thickness: medium
- Text fade threshold: 2.5
- Enable: **Show attachments** OFF (hides PDFs/images from graph)
- Enable: **Show orphans** OFF (shows only linked notes — cleaner investigation graph)

### Groups (color-code by folder)
Add these groups in order:
| Path query | Color | Label |
|---|---|---|
| `path: "10-Investigations"` | Red | Investigations |
| `path: "20-Entities/People"` | Orange | People |
| `path: "20-Entities/Organizations"` | Yellow | Orgs |
| `path: "20-Entities/IPs"` | Blue | IPs |
| `path: "20-Entities/Domains"` | Cyan | Domains |
| `path: "25-Networks"` | Purple | Networks |
| `path: "30-Evidence"` | Green | Evidence |
| `path: "00-Inbox"` | White | Inbox |

---

## 6. Python Scripts — Show or Hide?

**Recommendation: Show them (leave `scripts/` visible).**

Reasons:
- The `1a_`, `2b_`, `3a_` numbering makes the pipeline order obvious at a glance in the file browser
- You can click `.py` files — Obsidian shows source code with syntax highlighting (no editing, but readable)
- Useful to know at a glance which scripts exist without opening a terminal
- `.hash_snapshots/` dirs inside `scripts/` are the only noise — exclude those (see Files & Links above)

If you want scripts completely hidden from Obsidian's index and search:
- Add `scripts/` to `.obsidianignore` (create this file in vault root)
- They'll still be on disk and runnable from terminal — just invisible to Obsidian

---

## 7. Frontmatter Management

Every note in this vault uses YAML frontmatter. Rules:

**Always include in agent-generated notes:**
```yaml
---
type: task | entity | investigation | evidence | memory | report
status: pending | in-progress | done | archived
priority: HIGH | MED | LOW
created: YYYY-MM-DD
tags: []
---
```

**Metadata Menu field types to configure:**
| Field | Type | Values |
|---|---|---|
| `type` | Select | task, entity, investigation, evidence, memory, report |
| `status` | Select | pending, in-progress, done, archived, blocked |
| `priority` | Select | HIGH, MED, LOW |
| `confidence` | Select | HIGH, MED, LOW, UNVALIDATED |
| `created` | Date | YYYY-MM-DD |
| `tags` | Multi-text | free tags |

**Settings → Editor → Properties in document:** Set to **Visible** — always show frontmatter in editing view.

---

## 8. Search — Useful Saved Searches

In Search pane (Ctrl+Shift+F), save these as bookmarks:

| Search | What it finds |
|---|---|
| `path:00-Inbox tag:#task status:pending` | Open tasks |
| `path:20-Entities type:entity` | All entity stubs |
| `"- [ ]" path:REVIEW-INBOX` | Items awaiting human review |
| `path:03-Agents/hash-snapshots` | All hash snapshots (central dir) |
| `tag:#HIGH path:00-Inbox` | High-priority inbox items |

---

## 9. Hotkeys — Assign These

Settings → Hotkeys — search and assign:

| Action | Suggested hotkey |
|---|---|
| QuickAdd: Create task | Ctrl+Shift+T |
| QuickAdd: New entity stub | Ctrl+Shift+E |
| QuickAdd: Log evidence | Ctrl+Shift+V |
| Toggle graph view | Ctrl+Shift+G |
| Open Kanban board | Ctrl+Shift+K |
| Fold all headings | Ctrl+Shift+- |
| Toggle reading/editing mode | Ctrl+E |

---

## 10. Appearance

| Setting | Value |
|---|---|
| Theme | Minimal or AnuPpuccin (both clean for dense markdown) |
| Font size | 15–16px for body, 13px for UI |
| Line width | 700–750px (readable for long reports) |
| Interface font | System default or Inter |
| Monospace font | JetBrains Mono or Cascadia Code (for frontmatter/code blocks) |
| Show tab title bar | ON |
| Show status bar | ON |

---

## 11. The `.obsidianignore` File (Optional)

Create `CyberOps/.obsidianignore` to exclude from Obsidian's index entirely:

```
scripts/.hash_snapshots
.claude
**/.git
**/__pycache__
```

This keeps Obsidian's search and graph clean without moving any files.

---

## Quick-Start Checklist

- [ ] Files & Links: new notes → `00-Inbox`, links → relative path, wikilinks → OFF
- [ ] Editor: source mode default, spellcheck OFF, show properties ON
- [ ] Core plugins: Templates (folder: `Templates`), Backlinks, Graph, File recovery ON
- [ ] Community: install Dataview, Metadata Menu, Advanced Tables
- [ ] QuickAdd: template folder set to `Templates`, macros imported from package
- [ ] Graph: filter out `scripts/`, `Templates/`, `99-Archives/`; add color groups
- [ ] Metadata Menu: configure field types for `status`, `priority`, `type`, `confidence`
- [ ] Bookmark: `Dashboards/Hypothesis-Tracker.md`, `REVIEW-INBOX.md`, `00-Inbox/`
- [ ] Create `.obsidianignore` with `.hash_snapshots`, `.claude`, `__pycache__`
