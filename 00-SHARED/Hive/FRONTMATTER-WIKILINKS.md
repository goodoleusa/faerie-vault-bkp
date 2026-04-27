---
type: meta
tags:
  - meta
  - obsidian
  - yaml
  - navigation
updated: 2026-03-23
parent:
  - "[[00-README]]"
sibling:
  - "[[05-OBSIDIAN-SETTINGS]]"
child:
  - "[[00-SHARED/00-SHARED]]"
doc_hash: sha256:785c876c2c665a0f4173ad562841a545a1325ad14d9351a340921a5cb981ece5
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:26Z
hash_method: body-sha256-v1
---

# Frontmatter — parent, sibling, child (wikilinks)

Use **YAML properties** so Obsidian can show them in **Properties** and resolve **clickable** links. Always **wrap each wikilink in double quotes** so `:` and spaces inside `[[...]]` do not break YAML.

## Pattern

```yaml
---
parent: "[[Path/To/Parent-Note]]"
sibling: "[[Path/To/Related-Note]]"
child: "[[Path/To/One-Child]]"
---
```

**One wikilink per line** (each value is a single quoted string).

## Several children

Use a **list** (still one `[[link]]` per line):

```yaml
---
children:
  - "[[First Child Note]]"
  - "[[Second Child Note]]"
---
```

## Naming

- Prefer **paths** when titles collide: `[[00-SHARED/HOW-SYNC-WORKS]]` not just `[[HOW-SYNC-WORKS]]` if another note shares the same display name.
- File is `HOW-SYNC-WORKS.md` → wikilink `[[HOW-SYNC-WORKS]]` or `[[00-SHARED/HOW-SYNC-WORKS]]` for clarity.

## Relationship to body links

Body text can use markdown or wikilinks. **Navigation hubs** (`parent` / `sibling` / `child`) stay in frontmatter so Dataview and the Properties panel stay consistent.

See also: **[[05-OBSIDIAN-SETTINGS]]** (Files & Links) for vault-wide link defaults.

For **human ↔ agent async** on the same note (YAML + readable body + response sections), see **[[12-ASYNC-HUMAN-AGENT-BRIDGE]]**. That doc also defines **faerie-aligned** optional keys (`memory_lane`, `promotion_state`, `queue_task_id`, `bundle_ref`, …) for queues, NECTAR/HONEY routing, and bundles.
