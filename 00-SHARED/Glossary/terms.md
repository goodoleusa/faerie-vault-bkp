---
type: reference
status: active
tags: [glossary, terms, definitions, A-Z]
parent: Glossary/INDEX
up: Glossary/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:81b3fd9548cecdeda9e03ec3dc9c9a3ed1ba47e9493563918ff4e80b2f7d37ea
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

> [↑ Glossary](INDEX.md) · [⌂ Home](../../HOME.md)

# Terms — A to Z

---

## A

**AGENT-RUN-ID**
Immutable forensic anchor generated at agent startup. Links an agent run to its
eval score, COC entries, and training update. Format: `ar-{date}-{hash8}`.
See: [[../Architecture/spawn-contract]]

**altimeter**
The context fill % reading used to gate wave launches. Faerie reads `context_pct`
from `piston-checkpoint.json`. Not a clock — wave timing is pressure-based.

**anti-gaming bundle model**
The architectural guarantee that agents cannot see their baseline score before running.
The parent embeds only the public discovery.json inline. Private card (Last Training,
baseline, KPIs) is never in the agent's reachable scope.

---

## B

**baseline (eval)**
The Last Training score for an agent type. Set after a scored eval run. The next run
is measured against this baseline. Beating it triggers training update.

**blockedBy**
A queue field declaring task dependencies. A task with `blockedBy: ["T1"]` cannot be
claimed until T1 reaches `status: final`.

**bundle**
Crystallized context passed to an agent at spawn time. Contains role, task, vault
output location, manifest contract, and boilerplate sections. Rendered by
`7x_spawn_template.py`. ≤50 tokens to produce (deterministic, no LLM).

---

## C

**cascading summarization**
The pattern where main reads only `dashboard_line` (≤80 chars) from each agent.
Deeper synthesis spawns a synthesizer that also returns a `dashboard_line`. Main
context cost stays constant regardless of agent count. See: [[../Hive/the-five-principles]]

**chain-of-custody (COC)**
Hash-chained forensic audit trail. Every agent run appends one entry to `forensics/coc.jsonl`.
Each entry includes `prev_entry_hash` and `entry_hash`. Altering any entry invalidates the chain.

**claim**
The atomic act of an agent taking ownership of a task from the sprint queue.
Uses rename-based atomic claiming (`{task}.task.md` → `{task}.claimed.md`).

**cold start**
A session where >8h has passed since the last faerie cycle. Triggers emergency handoff
and cross-project registry scan before wave launch.

**context_pct**
Current context window fill percentage. Read from `piston-checkpoint.json`.
Key thresholds: 70% (W3 should start), 85% (compact queued), 93.5% (auto-compact fires).

---

## D

**dashboard_line**
≤80 character summary of what an agent produced. The primary signal main reads from
an agent manifest. Format (value · diagnosis · signal):
`"12 endpoints documented; 2 auth gaps flagged; ready-for-security-review"`

**droplet**
An inspired insight written before reasoning filters it. Cross-domain connections,
surprises, gut signals. Written to `Droplets/LIVE-{date}.md`. Discoverable by future
agents at task boundaries. See: [[../Skills-Reference/droplet]]

---

## E

**equilibrium**
The system-wide guardrail ensuring every durable file has a token budget.
Checked by `python3 {repo}/scripts/9x_equilibrium_audit.py --check-scripts`.

**eval**
Automated quality scoring of agent output against `done_looks_like` criteria.
Produces a score 0-1. Compared against agent's `baseline` (Last Training).
Run by `auto_eval.py` after each task completion.

---

## F

**f(0)**
The north star: orchestration burden on main context approaches zero. Number of
agents spawned and returned is not constrained by main context. Achieved by the five
principles working together. See: [[../Hive/the-five-principles]]

**faerie cycle**
One orchestration unit: `/faerie` → waves → `/handoff`. May span multiple CLI sessions.
Distinct from a CLI run (one `claude` process invocation).

**faerie-brief.json**
Cold-start session brief. Gated by `8x_faerie_brief_gatekeeper.py` — skipped on
warm start to prevent redundant context reads.

**finding_hash**
SHA256 hash of the primary output file. Included in manifest to prove integrity.

---

## H

**handoff**
The faerie cycle end operation. Promotes pollen → NECTAR, syncs vault, updates
piston checkpoint. See: [[../Skills-Reference/handoff]]

**HONEY.md**
Crystallized knowledge. Dense. Hard-won. ≤5K tokens. Mutates only via `/crystallize`
with human approval. Two tiers: global (`~/.claude/HONEY.md`) and project
(`{repo}/.claude/HONEY.md`). See: [[../Architecture/memory-topology]]

**hook**
A Claude Code PreToolUse or PostToolUse handler. Examples:
- `8x_spawn_contract_enforcer.py` — blocks direct prompt construction
- `8x_faerie_brief_gatekeeper.py` — gates warm-start brief reads
- Session_stop_hook — fires at CLI exit

---

## M

**manifest**
JSON file an agent writes on completion. Lives at
`{repo}/forensics/manifests/{TS}_{type}_{task-id}_{agent-id}_{sid8}.json`.
Contains dashboard_line, output_path, status, hash fields.
See: [[../Onboarding/04-reading-manifests]]

**manifest_hash**
SHA256 of the manifest JSON (excluding the hash field itself). Included for integrity.

**membench**
Memory benchmark. Measures 8 metrics: Retention, Continuity, Work Efficiency, Overhead,
Confabulation Rate. Baseline (2026-04-16): Retention 88 · Continuity 100 · WorkEff 15x · Overhead 2.8% · Confab 0%.

**MEM block**
Structured observation format written to pollen. Parsed by memory tooling.
Categories: OBSERVATION, FLAG, IDEA, PAIN, DECISION, HANDOFF, HEADLINE, CONNECTION, THREAD.

**monkeybranching**
When an agent chains directly to the next task without returning to faerie.
Requires: context >30K remaining, next task in-domain, next task unblocked.

---

## N

**NECTAR.md**
Validated findings. Append-only forever. Never edited. Never compressed.
Located at `~/.claude/NECTAR.md`. See: [[../Architecture/memory-topology]]

---

## P

**piston**
The wave-based orchestration engine. Named for the rocket physics metaphor.
Manages wave sequencing, agent assignment, and context pressure gating.

**piston-checkpoint.json**
Canonical state file for piston: `context_pct`, `wave_state`, `agents_in_flight`,
`deferred_reason`. Located at `~/.claude/hooks/state/piston-checkpoint.json`.

**pollen**
Ephemeral session notes. Written as MEM blocks to `pollen-{SID}.md`.
Promoted to NECTAR at `/handoff`. See: [[../Architecture/memory-topology]]

**proof-in-place**
mth00076: The compliance proof must live on a stronger substrate than the system it proves.
See: [[../Hive/proof-in-place]]

---

## S

**SESSION_ID8**
First 8 characters of `CLAUDE_SESSION_ID`. Used in manifest filenames for
cross-session isolation (prevents overwrite between sessions).

**spawn contract**
Rule #7: Every Agent() spawn must be rendered via `7x_spawn_template.py --bundle`.
Enforced by `8x_spawn_contract_enforcer.py` PreToolUse hook.
See: [[../Architecture/spawn-contract]]

**sprint**
All work toward a phase milestone. May span multiple faerie cycles.

**sprint queue**
The ordered backlog of pending tasks. Lives at
`~/.claude/hooks/state/sprint-queue.json`. Shaped by `/queue`, consumed by `/run`.

**stigmergy**
Coordination through environmental marks. Agents write to the filesystem;
other agents discover what was written. No messages, no polling, no relay overhead.
See: [[../Hive/stigmergic-recursion]]

---

## T

**task_id**
Unique identifier for a queue task. Embedded in filenames and manifests.
Discovery: `grep -r "_{task_id}_" forensics/` finds all predecessor work for zero context cost.

**template**
Deterministic spawn prompt renderer. Produces full agent context from ≤50 token input.
Listed via `7x_spawn_template.py list`. See: [[../Architecture/spawn-contract]]

---

## V

**VANILLA baseline**
Unassisted performance measurement. Run `/vanilla` after a hard task to measure
what main session would produce without agents. Used to compute f(0) delta.

**vault**
The Obsidian-format documentation system. Derivative artifacts (styled, human-readable).
Not the canonical system of record — that is `forensics/`. This vault (`faerie2/vault/`)
is the learn-faerie playground.

---

## W

**warm start**
A session within 8h of the last faerie cycle. faerie-brief.json is skipped.
Only `piston-checkpoint.json` is read for orientation.

**wave**
A set of agents dispatched in the same time tier. W1 (45s, fast), W2 (180s, medium),
W3 (600s, deep synthesis). Gated by context pressure, not clock.

**WORM**
Write Once Read Many. B2 bucket with compliance-mode lock. Used for immutable
backup of forensics/. Admin cannot bypass the lock.

---

## Related

- [[../Hive/the-five-principles]] — principles reference most of these terms
- [[../Architecture/memory-topology]] — HONEY/NECTAR/pollen in depth
- [[../Architecture/forensic-integrity]] — COC and hash chain in depth
