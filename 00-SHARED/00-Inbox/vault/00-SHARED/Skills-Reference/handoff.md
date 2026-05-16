---
type: reference
status: active
tags: [skill, handoff, session, memory, promotion]
parent: Skills-Reference/INDEX
up: Skills-Reference/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:f0613b1e6405f71e016c8538bfabd862c33c95c8260eeaf5b7bc76caec123d3b
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Skills-Reference](INDEX.md) · [⌂ Home](../../HOME.md)

# /handoff — Session Closer

Closes the faerie cycle. Promotes session memory, syncs vault, updates piston.

---

## Invocation

```
/handoff
```

---

## What It Does

```
1. Write HANDOFF MEM block to pollen
2. Spawn memory-keeper (promotes pollen → NECTAR)
3. Sync vault with agent outputs
4. Update piston-checkpoint.json for next session
5. Build master COC (hash-chained audit trail)
```

---

## Memory Promotion Flow

```
pollen-{SID}.md (session notes)
    ↓  /handoff
NECTAR.md (validated findings, append-only)
    ↓  /crystallize (human choice)
HONEY.md (crystallized knowledge, ≤5K tokens)
```

HIGH-priority pollen entries (pri=HIGH) are promoted immediately at /handoff.
Other entries are reviewed by memory-keeper for NECTAR eligibility.

---

## What Happens Without /handoff

Session observations stay in pollen. At next session start, pollen is not
automatically read. The observations effectively evaporate.

Always run `/handoff` before closing Claude Code.

---

## Not Memory Promotion

`session_stop_hook.py` fires at CLI exit — this is NOT memory promotion.
Memory promotion is `/handoff`'s job specifically.
The stop hook handles: piston checkpoint, COC finalization, W3 completion collection.

---

## Related

- [[crystallize]] — /crystallize for deeper memory integration
- [[../Architecture/memory-topology]] — full memory architecture
- [[../Onboarding/01-first-session]] — where /handoff fits in the session flow
- [[../Glossary/terms]] — pollen, NECTAR, handoff defined
