---
type: dashboard
status: active
last_updated: 2026-05-22
purpose: human-final-gate-for-publish
related_repos: [faerie2, cybertemplate, hustle]
related_skill: vault-daily
---

# 📰 Publishing Dashboard — Final Gate

> This is the single page goodoleusa opens when ready to publish. It
> answers: **what did the AI session find, what needs my eyes/hands,
> what's blocking publication.**
>
> Designed for the cybertemplate site (data-intensive investigation)
> + adaptable to any data-→-narrative-→-publish flow.
>
> Companion: `swarmy-inbox` CLI alias gives the same bucket view from
> the shell.

---

## ✋ THE FINAL GATE — what only you can do

Things that need *you* (the human), not an agent:

- [ ] Read each `📝 ANNOTATING` item below — agents drafted these but
      they need your voice
- [ ] Approve each `🚀 READY-TO-PUBLISH` item with `swarmy-publish <file>`
- [ ] For cybertemplate items: confirm the JOURNALIST_BRIEFING tier
      assignment is right before the data flows to the public site
- [ ] Add the human dedication/intent line to any sealed creature
      memorial under `forensics/creatures/memorial/`
- [ ] Sign your weekly synthesis (uses your key:
      `forensics/reputation/keys/goodoleusa.{key,pub}`)

---

## 📊 Today's stage snapshot

> Run the queries below in Obsidian via the **Dataview** plugin (it
> auto-fills from frontmatter). If you don't have Dataview, the
> equivalent CLI is `swarmy-inbox` and `swarmy-inbox-today`.

### ✏️ DRAFTS — needs writing
```dataview
TABLE author AS "by", related_mission AS "mission", file.mtime AS "modified"
FROM "00-SHARED/Daily"
WHERE status = "draft"
SORT file.mtime DESC
LIMIT 15
```

### 👁️ REVIEWING — drafts ready for self-review
```dataview
TABLE author AS "by", related_mission AS "mission", file.size AS "size"
FROM "00-SHARED/Daily"
WHERE status = "reviewing"
SORT file.mtime DESC
LIMIT 15
```

### 📝 ANNOTATING — needs YOUR human voice on top
```dataview
TABLE author AS "by", related_mission AS "mission"
FROM "00-SHARED/Daily"
WHERE status = "annotating"
SORT file.mtime ASC
```

> When all annotations are done on an item, transition with:
> `swarmy-status-set <file> ready-to-publish`

### 🚀 READY-TO-PUBLISH — the publish queue
```dataview
TABLE author AS "by", related_mission AS "mission", related_repos AS "repos"
FROM "00-SHARED/Daily"
WHERE status = "ready-to-publish"
SORT file.mtime ASC
```

> Final gate per item:
> 1. One last read for typos + factual claims
> 2. `swarmy-publish <file>` → signs + flips to `published`
> 3. If destined for cybertemplate site, sync via cybertemplate's
>    `scripts/sync-vault-to-site.py` (see below)

### ✅ PUBLISHED THIS WEEK
```dataview
TABLE author AS "by", related_mission AS "mission", file.mtime AS "published"
FROM "00-SHARED/Daily"
WHERE status = "published"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
```

---

## 🔬 cybertemplate-specific pipeline

> For investigation-bound narratives (the data-intensive case). The
> cybertemplate site at `cybertemplate.retrofuture.tech` reads from
> the `cybertemplate/data/timelines/00-master/` curated tree. Anything
> you publish FROM the vault needs to land there.

### Stage 1 — Data is curated (agents do this)
- Source data lives in cybertemplate's tier-2/tier-3 evidence
- The `evidence-curator` agent promotes items via
  `cybertemplate/forensics/promotion_log.json`
- You see what's been curated by reading the agent's manifests:
  `swarmy-frontier` filtered by mission

### Stage 2 — Draft narrative (AI session writes; you read)
- AI sessions write to `$SWARMY_VAULT_DAILY/{date}/NN-slug.md` with
  `status: reviewing`
- Your inbox surfaces these for review

### Stage 3 — You annotate (the human voice)
- Add your perspective, your why, your dedications
- Mark `status: annotating` while working
- This is the irreplaceable part — the AI can't add YOUR voice

### Stage 4 — Ready-to-publish
- Final factual check
- Confirm the journalist-briefing-tier assignment (Tier 1 = smoking
  gun, Tier 2 = strong, Tier 3 = contextual, Tier 4 = full catalog)
- `swarmy-publish <file>`

### Stage 5 — Site sync (auto + your trigger)
- The vault → cybertemplate sync is automatic via poll-deploy daemon
- Your `swarmy-publish` is the final gate; once signed, the site
  picks it up on the next poll tick (~5 min)

---

## 📚 Long-form writing recommendation

If you want a book-style writing surface inside Obsidian without
managing Obsidian itself, pin these plugins:

| Plugin | Why |
|---|---|
| **Longform** | Manuscript view with project structure (chapters / scenes); doesn't fight Obsidian, just adds a UI for narrative continuity |
| **Dataview** | What powers the queries in this dashboard |
| **Templater** | New-note frontmatter auto-fill (so `swarmy-write` and the GUI New Note both produce identical templates) |
| **Obsidian Git** | Auto-commit the vault on save (you don't have to think about it) |
| **swarmy-hive-plugin** | (when shipped) Manifest index + mission graph display in Obsidian |

Pin those, hide everything else from the sidebar, and your Obsidian
becomes a writing surface, not a tool-management surface.

---

## 🤖 What the AI sessions discovered today

> This pulls from `forensics/manifests/{today}` — only the items
> tagged for human-publish-relevance show up here. Refresh by
> running `swarmy-frontier` in the shell.

```dataview
LIST
FROM "00-SHARED/Daily"
WHERE date = date(today)
WHERE author != "openhands-agent"  -- show only human-authored entries
SORT file.ctime DESC
```

Agent-authored manifests live in the faerie2 repo's
`forensics/manifests/{today}/` — the dashboard intentionally surfaces
only items that arrived in the vault (i.e., agents that wrote a
narrative). Agents that ONLY shipped code (no vault narrative) won't
appear here, which is correct: code ships through git, not the
publish gate.

---

## 🛠 Maintenance

- This dashboard lives at `$SWARMY_VAULT/00-SHARED/PUBLISHING-DASHBOARD.md`
- Update `last_updated` whenever you add new sections
- New buckets? Update `swarmy-inbox` in
  `deploy/scripts/install-swarmy-aliases.sh` to mirror
- Status vocabulary is fixed: `draft | reviewing | annotating |
  ready-to-publish | published | sealed`. Don't fork it; the CLI +
  Dataview queries depend on it.

---

*Source-of-truth: this file at the vault root. CLI mirror:
`swarmy-inbox`. To activate the aliases: run
`bash deploy/scripts/install-swarmy-aliases.sh` (in the faerie2
repo) then `source ~/.bashrc`.*
