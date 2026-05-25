---
type: charter
status: sealed
charter_id: pair-coding-completion-and-dry-cleanup
semantic_mission: swarmy-pair-coding-completion
cluster_prefix: []
phase: "COMPLETE-6-of-6"
author: goodoleusa
created: 2026-05-25
canonical_repo_path: "forensics/charters/active/2026-05-25Z__charter__pair-coding-completion-and-dry-cleanup__goodoleusa.json"
filename_base: "2026-05-25Z__charter__pair-coding-completion-and-dry-cleanup__goodoleusa"
tags: [charter, pseudosystem]
blueprint: "[[Charter.blueprint]]"
---

# Charter — pair-coding-completion-and-dry-cleanup

> **Vault pseudosystem mirror** — canonical source: `forensics/charters/active/2026-05-25Z__charter__pair-coding-completion-and-dry-cleanup__goodoleusa.json`
> Status: **sealed** | Phase: **COMPLETE-6-of-6** | Mission: `[[swarmy-pair-coding-completion]]`

---

## Thesis

The 2026-05-24 wave shipped the Pair Session foundation (PairSessionLayout + Caddy block + shared-
conv-relay in flight). This charter completes Path 3 (Cuts B/C/D/E) so two users can actually pair-
code with shared canvas state + ghost cursors + SPA history routing, AND cleans up the doctrinal
cruft the velocity wave accumulated (DRY violations, missing skill loading, dead components, naming
drift). The cleanup is as important as the new features — without it, the next velocity wave starts
from a

## Phases

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| phase_1 | Complete Path 3 pair-coding (Cuts B + C + D) | 6 | sealed |
| phase_2 | Skills auto-load into chat Conversation | 3 | sealed |
| phase_3 | DRY cleanups (the velocity-wave debt) | 4 | sealed |
| phase_4 | GH bridges round-trip (mission-graph ↔ Projects, charter ↔ m | 5 | sealed |
| phase_5 | Backend events for stigmergic field (close the mock-data gap | 3 | sealed |
| phase_6 | Production hardening + DNS + deploy automation | 4 | sealed |

## Operator Pain Points

- Friend can't join my conversation live — they see same VISUAL layout via shared URL but separate chat data (Cut F backen
- Friend drags a card on canvas, I don't see it — RecursiveCanvas is localStorage-per-browser (Cut C)
- Live cursors missing — PresenceBar shows WHO is here, not WHERE — Figma-style co-presence needs Cut B
- Direct-navigate to swarmy.retrofuture.tech/pair?session_id=X likely 404s — Vite SPA needs Caddy try_files (Cut D)
- Chat LLM doesn't know about /faerie /spawn /forage etc. — 32 SKILL.md files not auto-loaded into Conversation context (c

## Non-Goals

- Cut E (Codespaces integration) — too far out for this charter; revisit in hustle-portfolio-f0-demo phase
- Mobile responsive PairSessionLayout — desktop-first; mobile later
- Voice/video chat in pair sessions — out of scope (use Zoom/Discord)
- CRDT for canvas (last-write-wins is fine for v1; CRDT if collision rate proves problematic)
- Public unauthenticated pair sessions — invite-list only (security boundary)

## Related Charters

- 2026-05-23Z__charter__hive-pair-coding-foundation (Phase 6 in progress; this cha
- 2026-05-24Z__charter__recursive-canvas-visual-design-substrate (the canvas subst
- 2026-05-24Z__charter__forensic-coc-v2-rekor (sigstore signatures; orthogonal but
- 2026-05-24Z__charter__multi-tenancy-and-free-tier-scoping (auth/tier scaffolding

---

*To jump to canonical JSON: open `forensics/charters/active/2026-05-25Z__charter__pair-coding-completion-and-dry-cleanup__goodoleusa.json` in repo. Vault note is navigation-only — do not edit to change charter state.*
