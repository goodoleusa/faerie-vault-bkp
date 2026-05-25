---
type: readme
pseudosystem_folder: Forensics/waves
canonical_repo_path: "forensics/manifests/"
tags: [readme, waves, forensics, pseudosystem]
---

# Waves — Multi-Agent Dispatch Dossiers

> **Canonical manifests live in `forensics/manifests/<date>/` in the repo.**
> This folder contains dossiers for multi-agent dispatch waves — one note per major spawn event.
> A wave dossier collects all agents dispatched in one Queen liftoff, their outcomes, and what emerged.

---

## What Is a Wave?

A **wave** is one `/spawn` or Queen liftoff event — the Queen dispatches N agents in parallel (W1 LIFTOFF, W2 CRUISE, etc.), each writes a manifest, and the collective output advances one or more missions. The wave dossier is the post-mortem view:

- Which agents were dispatched?
- What did each accomplish (dashboard_lines)?
- What discovered_work emerged?
- Did the wave advance its charter's phase?
- What shapes moved (beneficial/harmful/neutral verdicts)?

## How to Add a Wave Dossier

1. After all agents in a wave have sealed their manifests
2. Blueprint → `Wave.blueprint` in Obsidian
3. Save to `Forensics/waves/{YYYY-MM-DD}-{wave-label}.md`
4. Fill in the agents table from the manifests in `Manifests/{YYYY-MM-DD}/`
5. Write the Emergence section (what wasn't in the brief but emerged)

## When Is a Wave Noteworthy?

Not every spawn needs a wave dossier. Consider adding one when:
- 4+ agents were dispatched in one wave
- The wave completed a charter phase or advanced multiple missions
- Significant discovered_work emerged (new bearing edges)
- A shape verdict was recorded (beneficial/harmful mutation)

---

*Part of the Vault Pseudosystem — see `PSEUDOSYSTEM-README.md` at vault root.*
