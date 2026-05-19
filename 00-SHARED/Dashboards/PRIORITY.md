---
type: researcher-priority
updated: 2026-03-26
sync_to_honey: true
tags: [priority, north-star, researcher-instruction]
doc_hash: sha256:b7767129f7189c06d779d16d2bcc513c0bd62cf6e2607fc63f65c78b4e36e267
hash_ts: 2026-03-29T16:10:50Z
hash_method: body-sha256-v1
---

# Researcher North Star

> This file is your current #1 instruction to the agent system.
> Edit it freely — vault_narrative_sync.py will inject it into HONEY.md at session start.
> Agents see it first. It overrides queue priorities.

---

## Current Priority

**Verify ORNL + LLNL certs on Baxet IPs before any nuclear-triple claims go public.**

The ORNL cert on Baxet IP is `CN=BlurbStudio.cr` (self-signed, NOT ornl.gov). The nuclear-triple framing needs LLNL verification (45.130.147.179) before it can be used in any published claim. Do not route any agent toward nuclear-triple narrative work until this verification gap is closed.

---

## Context

- LANL cert: confirmed (194.58.46.116) — solid
- ORNL hostname: confirmed on Baxet IP, but cert is BlurbStudio.cr self-signed — NOT ornl.gov
- LLNL: 45.130.147.179 — unverified pending Shodan archive access

**Queued task:** `task-20260323-140411-5a6f` — ORNL cert via CT logs + LLNL verification

---

## Previous Priorities

*(moved here when superseded)*

---

*Synced to `~/.claude/memory/HONEY.md` on session start · Edit freely in Obsidian*
