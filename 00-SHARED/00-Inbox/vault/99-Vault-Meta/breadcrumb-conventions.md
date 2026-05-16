---
type: reference
status: active
tags: [meta, breadcrumb, navigation, conventions]
parent: 99-Vault-Meta/INDEX
up: 99-Vault-Meta/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:5a010fbc59d0d9065bdbbabe01c073142d3d2be7ff2f0063933268c45e42d026
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Vault-Meta](INDEX.md) · [⌂ Home](../../HOME.md)

# Breadcrumb Conventions

Navigation conventions used throughout this vault.

---

## Breadcrumb Format

Every document begins with a breadcrumb line:

```markdown
> [↑ Parent Section](../parent-section/INDEX.md) · [⌂ Home](../../HOME.md)
```

- `↑` — one level up in the hierarchy
- `⌂` — back to HOME.md (always present)
- Relative paths — always relative to current file location

---

## Frontmatter Fields

Every document includes these frontmatter fields:

```yaml
---
type: narrative|reference|guide|index|example|dashboard
status: active|draft|deprecated
tags: [relevant, tags]
parent: Section/INDEX             ← logical parent (not path)
up: Section/INDEX                 ← same as parent (Obsidian convention)
child: [SubSection/INDEX]         ← only if has children (optional)
created: YYYY-MM-DD
updated: YYYY-MM-DD
doc_hash: sha256:pending          ← replaced by stamp script
---
```

---

## Document Types

| Type | Use |
|------|-----|
| `entry-point` | HOME.md only |
| `index` | Every INDEX.md — section hub |
| `narrative` | Hive design narratives |
| `reference` | Technical quick-refs |
| `guide` | Step-by-step onboarding |
| `example` | Worked session examples |
| `dashboard` | System state narratives |

---

## Wiki-Link Format

Internal links use Obsidian wiki-link format:

```markdown
[[FileName]]               ← links to FileName.md in same directory
[[SubDir/FileName]]        ← links to SubDir/FileName.md
[[../SiblingDir/INDEX]]    ← links up then into sibling directory
```

Every document should have:
- At least 2 outbound links (Related section)
- At least 1 inbound link (referenced by parent INDEX or a sibling)

---

## Related Section

Every document ends with a Related section:

```markdown
## Related

- [[sibling-doc]] — brief description
- [[../OtherSection/INDEX]] — brief description
- [[../Glossary/terms]] — definitions for terms used here
```

---

## Related

- [[doc-stamping]] — how doc_hash works
- [[../HOME]] — vault entry point
