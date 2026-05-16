---
type: index
status: active
tags: [index, droplets, insights, auto-populated]
parent: 00-SHARED/INDEX
up: 00-SHARED/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:1d49a8932d40313b16c341f682e1e075ba0fbd94b4ca897ec7772bb426e9e4ab
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

> [↑ 00-SHARED](../INDEX.md) · [⌂ Home](../../HOME.md)

# Droplets

Agent-written insights, auto-populated during sessions.

**This folder is auto-populated.** Do not manually create entries here.

Agents write droplets during sessions to:
`$CT_VAULT/00-SHARED/Droplets/LIVE-{YYYY-MM-DD}.md`

Forensic droplet records live in:
`{repo}/forensics/droplets/`

---

## What Droplets Are

Droplets are inspired thoughts written before reasoning filters them:
- Cross-domain connections
- Surprises (assumption flipped)
- Gut signals (friction mid-explanation)
- Patterns that appear across silos

They are NOT:
- Technical findings (those are pollen)
- Summaries of what was read (use pollen)
- Process logs (use pollen MEM blocks)

---

## High-Priority Droplets

HIGH priority droplets are promoted to NECTAR at `/handoff`. They become
part of the persistent validated findings corpus — discoverable by future
agents at task boundaries.

---

## When Files Appear Here

Droplet files appear in this folder when agents run sessions and write
insights. Each file is named `LIVE-{YYYY-MM-DD}.md` and contains
timestamped, categorized insight blocks.

---

## Related

- [[../Skills-Reference/droplet]] — /droplet skill reference
- [[../Hive/stigmergic-recursion]] — how droplets are discovered
- [[../Glossary/terms]] — droplet defined
