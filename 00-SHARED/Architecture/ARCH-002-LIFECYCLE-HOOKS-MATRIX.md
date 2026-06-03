---
arch_id: ARCH-002
title: Swarmy OH Lifecycle × Hooks — Strategic Boundary Matrix
status: canonical
created: 2026-05-23
authors: [goodoleusa, claude-opus-4-7]
mission_id: hooks.lean.wire
charter: swarmy-oh-runtime-bootstrap
related_arch: [ARCH-001-STIGMERGIC-SPAWN-PROTOCOL]
related_skills: [four-shields, forage, spawn, shape-registry]
tags: [architecture, hooks, openhands, four-shields, lifecycle, swarmy]
---

# 🐝 Swarmy OH Lifecycle × Hooks — Strategic Boundary Matrix

> **What hooks SHOULD fire at each lifecycle boundary in the swarmy-on-OH runtime, mapped to four-shields enforcement, kept lean.**

This doc answers the question: *given the swarmy doctrine and the OpenHands runtime model, where in the session lifecycle should a hook fire, what utility does it serve, and which of the four shields (🛡🧠⛓🪞) does it close?*

It is the **strategic counterpart** to four-shields' "how" — four-shields tells you what shield to use for any given discipline; this matrix tells you where in the lifecycle each hook lives.

---

## The session shape

```
┌──────────────────────────────────────────────────────────────────────────┐
│              session start              session end                       │
│  ┌──────┐    ↓                          ↑      ┌────────┐               │
│  │ user │ → PromptSubmit → … turns … → SessionEnd → digest               │
│  └──────┘                                                                 │
│              ┌──── per turn ────┐                                          │
│              │ PreToolUse →     │                                          │
│              │   tool runs →    │                                          │
│              │ PostToolUse      │                                          │
│              └──────────────────┘                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

Within a turn there are two sub-lifecycles that swarmy adds:

```
        per-spawn                  per-manifest-write
   ┌─────────────────┐         ┌────────────────────────┐
   │  PreSpawn →     │         │  Write to ephemeral →  │
   │   Agent() →     │         │  PostToolUse:          │
   │  PostSpawn      │         │   promote-to-canonical │
   └─────────────────┘         │   + COC append         │
                               │   + shape track        │
                               │   + B2 WORM upload     │
                               └────────────────────────┘
```

---

## The matrix — boundaries × hooks × shields

| Boundary | Hook utility | Shield | Why strategic |
|---|---|---|---|
| **🌅 Session start** (no real hook — skills auto-load) | `forage` skill (always-on) + AGENTS.md jump-start glossary injection | 🧠 | Every agent inherits the rhythm + doctrine without operator pings |
| **📥 UserPromptSubmit** | Turn counter; piston wave-stage detector (W1/W2/W3 by ctx pressure) | 🪞 | Tells the spawn-pressure curve what wave we're in |
| **🔒 PreToolUse (any)** | COC pre-write hash capture (`hash_before`) | 🛡 | Foundation of the immutable forensic chain |
| **🛑 PreToolUse (Bash)** | Loop guard — block `cat`/`tail`/`grep` polling | ⛓ | Prevents the "let me check on the agent" anti-pattern from `CLAUDE.md` |
| **📋 PreToolUse (Write/Edit to `forensics/charters/`)** | Charter shape lint + cluster_prefix fence + signing requirement | 🛡 + ⛓ | Charters can't be born malformed |
| **📋 PreToolUse (Write to `forensics/ephemeral/**/*__manifest__*.json`)** | Manifest filename schema (v2 type-marker + w3w + kebab + agent) | 🛡 | Filename IS the index — corrupting it breaks frontier scan |
| **📋 PreToolUse (Write to canonical `forensics/manifests/`, `forensics/coc.jsonl`)** | **DENY** — agents only write to `ephemeral/`; promotion is hook-only | ⛓ | Write-protection architecture (canonical = symlinks, never agent-typed) |
| **✍️ PostToolUse (any)** | COC entry append (`hash_after` + `prev_entry_hash` chain + ed25519 sign) | 🛡 + ⛓ | Closes the hash chain on every action |
| **✍️ PostToolUse (Write to `forensics/ephemeral/`)** | Promote-by-symlink to canonical + type-infer from filename | 🛡 | Single source of truth (no duplicates); agents stay unaware |
| **✍️ PostToolUse (manifest seal)** | (a) Shape tracking — re-count + classify mechanical verdict; (b) B2 WORM upload queue; (c) reputation event from `completion_choice` | 🪞 | The 3-shot recovery layer per manifest |
| **🚀 PreSpawn (`spawn.py` emits directive)** | Mission validation (non-empty, w3w shape, `cluster_prefix=3`, `manifest_output_path` conforms); WAVE_LIMITS check; skip-recursive-spawn check; KNOWN_AGENT_TYPES gate | 🛡 + ⛓ | The spawn discipline enforcer (what `9x_spawn_protocol_enforcer.py` did before it was lost) |
| **🚀 PostSpawn (Agent() invoked)** | Roster update + `spawn-influence-{date}.json` write + `genotype-fitness-{date}.json` write + wave-counter update | 🪞 | Feeds spawn-pressure feedback loop — the genetic-algorithm closure (Lane A's lost f(0) emergence engine) |
| **🌙 SessionEnd** | Session digest + token audit summary + NECTAR crystallize candidate + HONEY review queue | 🪞 | The handoff payload |
| **⏰ Periodic (cron)** | (a) Shape audit re-counts all detectors; (b) Reputation aggregator; (c) Charter debloat-overdue scan; (d) Vault auto-index; (e) Cross-repo alignment shape compute | 🪞 | The slow-loop immune memory |
| **🌿 Pre-commit (git hook)** | Filename lint + charter shape + manifest signing | ⛓ | Last-mile defense before content leaves the repo |

---

## The cheaper-earlier law

```
🛡 STRUCTURAL  — prevent: the wrong thing CAN'T be expressed     $
🧠 COGNITIVE   — remind:  skill/microagent fires before action  $$
⛓ REACTIVE    — block:   hook rejects at the OS boundary       $$$
🪞 RECOVERY    — catch:   periodic audit + reputation scoring   $$$$
```

A discipline at one shield is brittle. The four together = swarmy survives drift.

**Recovery audits should be the rare catch, not the primary defense.** If you find yourself adding a 🪞 hook to compensate for a missing 🛡 hook, redesign — 🛡 is cheaper and earlier.

---

## The lean keeper list (4-shields covered, no bloat — 11 hooks)

**🛡 Structural (3 hooks):**
- `pre_bundle_validator` (PreSpawn) — ensure bundle has `mission_id`, `cluster_prefix`, `manifest_output_path`; recursive-spawn detection; WAVE_LIMITS
- `charter_shape_lint` (PreToolUse Write to `forensics/charters/`) — encoded by `_charter_lib.py` writer + hook
- `manifest_filename_enforce` (PreToolUse Write to `forensics/ephemeral/`) — v2 filename grammar

**⛓ Reactive (3 hooks):**
- `loop_guard` (PreToolUse Bash) — block agent polling
- `canonical_write_deny` (PreToolUse Write to `forensics/manifests/`, `coc.jsonl`) — agents only touch ephemeral
- `coc_chain_append` (PostToolUse any) — hash chain + ed25519 sign

**🪞 Recovery (5 hooks):**
- `roster_update` (PostSpawn) — feeds spawn-pressure feedback (HIGH VALUE — restores evolve↔spawn loop)
- `shape_tracking` (PostToolUse manifest) — re-count + mechanical verdict classification
- `session_digest` (SessionEnd) — handoff payload
- `token_auditor` (SessionEnd + periodic) — cost discipline
- `b2_worm_uploader` (PostToolUse manifest) — immutable cloud backup

**🧠 cognitive shield is NOT a hook** — it's the always-loaded skill set (`forage`, `four-shields`, `mission`, `charter`, `spawn`, `shape-registry`). Skills are 🧠's vessel; hooks are 🛡⛓🪞's vessel.

---

## Stub → real-impl mapping (the salvage)

Top-level `hooks/` contains 10 **permissive stubs** (each says `"""Permissive stub — original hook script missing"""` — they fire no real logic). The stub names are clues to what got lost:

| Stub | Should fire at | Shield | Recover? |
|---|---|---|---|
| `0x_pre_agent_bundle_validator.py` | PreSpawn — validate bundle before `Agent()` | 🛡 | ✅ YES — gap in current |
| `4x_forensic_coc.py` | PostToolUse — COC append | 🛡 | ⚠️ Check if `.openhands/hooks/` covers (likely yes via `coc_chain_append`) |
| `8x_state_write_coc_enforcer.py` | PreToolUse Write to canonical paths | ⛓ | ✅ YES — DENY rule for canonical writes (`canonical_write_deny`) |
| `8x_roster_update.py` | PostSpawn — roster + spawn-pressure feedback | 🪞 | ✅ YES — feeds the LOST evolve↔spawn loop |
| `8x_user_prompt_turn_counter.py` | UserPromptSubmit | 🪞 | ✅ YES — drives piston stage detection |
| `8x_vault_auto_index.py` | Periodic cron OR PostToolUse on vault writes | 🪞 | ✅ YES — vault canonicity |
| `9x_reputation_tracker.py` | PostToolUse (manifest seal) — reputation event from `completion_choice` | 🪞 | ✅ YES — wraps `scripts/5g_reputation_tracker.py` if it exists |
| `9x_session_digest.py` | SessionEnd | 🪞 | ✅ YES — handoff payload |
| `9x_token_auditor.py` | SessionEnd + periodic | 🪞 | ✅ YES — cost discipline |
| `agent_tracker.py` | PostSpawn — duplicate of `roster_update`? | 🪞 | Merge with `roster_update`; one canonical |

Top-level `hooks/` is preserved verbatim at `scripts/_recovery/2026-05-23-precious-faerie/from-repo-hooks/` for forensic provenance. The real implementations live in `.openhands/hooks/` (the OH-native location).

---

## Highest-leverage gap to close NOW

`roster_update` (PostSpawn) — the missing piece that closes the evolve↔spawn feedback loop Lane A of the precious-faerie-salvage team identified. Without it, the queen drives spawn decisions manually instead of letting the genetic-algorithm closure work.

Once `roster_update` lands, the next `spawn.py` invocation reads `forensics/eval/genotype-fitness-{date}.json` and adjusts the sigmoid midpoint via `_adjust_pressure_from_evolve()` (recovery vault path: `scripts/_recovery/2026-05-23-precious-faerie/from-backup-repo/skills/faerie/spawn.py` L323-361 — the canonical implementation).

---

## How to add a new hook (lifecycle-first design)

1. **Identify the boundary** from the matrix above. If your need doesn't fit one, the matrix is wrong — fix the matrix before adding the hook.
2. **Identify the shield**. If your hook would be 🪞 to compensate for a missing 🛡, redesign upstream — 🛡 is always cheaper.
3. **Cite the existing skill or schema** the hook enforces. A hook without a sibling skill (🧠) or schema (🛡) is doing whack-a-mole, not enforcement.
4. **Use the existing canonical writers** (`1a_manifest_writer.py`, `_charter_lib.py`, `0a_coc-core.py`) instead of re-implementing — they already enforce structurally.
5. **Add to `.openhands/hooks.json`** with the right `PreToolUse` / `PostToolUse` matcher.
6. **Add a `--self-test` flag** that exercises reject + accept cases.
7. **Register the hook in this matrix.** If you add a hook that doesn't appear here, the matrix is stale — update it.

---

## Anti-patterns

- **🪞 as primary defense.** "We'll catch it in the audit" = the discipline is failing upstream and you're paying maximum cost. Move it to 🛡.
- **One hook does many things.** A hook should fire at ONE boundary and serve ONE shield. If your hook touches PreSpawn AND PostToolUse AND cron, it's three hooks.
- **Hook validates without a sibling skill.** Means agents will hit the hook surprised; add the 🧠 layer (skill) that warns them BEFORE they hit the ⛓ layer (hook).
- **Stubs without retirement_ts.** A `"""Permissive stub — original hook script missing"""` should EITHER be replaced OR moved to `.archive/` with a documented retirement. Letting stubs sit live is worst-of-both — looks like the hook works, but doesn't.
- **Hooks at the same shield layer.** Four reactive hooks doing 80% the same thing = expensive + duplicates. The shields must span the time-cost gradient.

---

## See also

- `.agents/skills/four-shields/SKILL.md` — the cheaper-earlier law + how to wire a new discipline at four shields
- `.agents/skills/spawn/SKILL.md` — the spawn-discipline language hooks enforce
- `.agents/skills/shape-registry/SKILL.md` — inline reflex; many hooks UPDATE shape state
- `scripts/_recovery/2026-05-23-precious-faerie/SCRIPTS-FEATURE-MATRIX.md` — what got lost and how to cannibalize it
- `forensics/charters/active/2026-05-23Z__charter__swarmy-oh-runtime-bootstrap__goodoleusa.json` — the active charter scoping this work

---

**Last updated:** 2026-05-23 by goodoleusa + claude-opus-4-7 during the precious-faerie-salvage / swarmy-on-OH-bootstrap session.
