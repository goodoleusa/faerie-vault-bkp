# SPAWN BUNDLE TEMPLATE — Universal Structure for Stigmergic Agent Replication
## Self-Describing, COC-Tracked, Forensically-Sound, Vault-Compatible

> **Swarmy-current 2026-05-23.** Original template 2026-04-28 (preserved in
> `.archive/`). Updated for: swarmy renaming (faerie → swarmy), w3w mission
> addressing (`investigation_label` → `mission_id`), six-choices completion
> ritual, forage rhythm doctrine (🔬/🌊/🌀), four-shields enforcement
> (🛡🧠⛓🪞), charter/mission grammar distinction (kebab compound vs w3w
> dotted).

---

## BUNDLE METADATA (Immutable Header)

```
BUNDLE_TYPE: spawn-context-injection
VERSION: 2026-05-23-swarmy-current
SESSION_ID: {session_id8}
MISSION_ID: {term1.term2.term3}        ← w3w dotted (3 atomic terms; ADDRESS)
CLUSTER_PREFIX: [t1, t2, t3]           ← the 3 w3w terms; THE scope fence
CHARTER_SLUG: {kebab-toast-compound}   ← kebab single compound noun (BOUNDED BOX)
TEAM_LABEL: {kebab-team}               ← stigmergic team grep key (e.g. coc-v2-w1)
WAVE: {wave} (W1/W2/W3)
COMPASS_BEARING: {bearing} (N/S/E/W)
MODE_SEED: 🔬 | 🌊 | 🌀                 ← forage entry mode (agent may flip mid-session)
REPLICA_COUNT: {N} (how many agents got this)
CREATED_TIMESTAMP: {ISO8601_UTC}
BUNDLE_HASH: sha256:{hex}
```

---

## CONTEXT LAYERS (How This Bundle Was Composed — Learn By Example)

### Layer 1: AGENTS.md (Governance, the QUEEN — Immutable)
- **Size**: ~3K tokens (jump-start glossary + forage rhythm + four-shields + mission/charter grammar)
- **Content**: doctrine, identity, equilibrium, spawn rules, mode discipline
- **Source**: `{repo}/AGENTS.md`
- **Cost to next agent**: ~3K tokens (loaded fresh each spawn — every model, every agent)

### Layer 2: HONEY.md (Crystallized Facts)
- **Size**: 0.2K tokens measured (was 1.5K theory, -87% delta — mission-filtered)
- **Content**: Universal principles + project invariants (sealed cross-session truths)
- **Source**: `~/.claude/HONEY.md` (global) + `{repo}/HONEY.md` (project)
- **Compression**: Only mission-relevant entries injected; full files referenced by path
- **Cost to next agent**: ~0.2K tokens (verified 2026-04-28)

### Layer 3: NECTAR.md (Recent Findings, Tail-50)
- **Size**: 1.2K tokens measured (was 2-3K theory, -40-60% delta)
- **Content**: Last 50 HIGH/CRITICAL observations from session
- **Source**: Session memory (pollen → NECTAR crystallization at /handoff)
- **Refresh**: Every agent return, only fresh HIGH/CRITICAL entries
- **Cost to next agent**: ~1.2K tokens

### Layer 4: Pollen (Live Session Observations)
- **Size**: Variable (100-500 tokens typical)
- **Content**: Raw MEM blocks from this session (agent discoveries, anomalies)
- **Format**: `<!-- MEM {timestamp} ... --> ... <!-- /MEM -->`
- **Scope**: Mission-scoped (filtered by `mission_id` cluster_prefix overlap)

### Layer 5: Mission Graph Snapshot (Stigmergic Pheromones)
- **Size**: 2-4K tokens
- **Content**: Last 10 manifests from same `mission_id` + sister teams via `team_label`
- **Format**: Compass edges (N/S/E/W), `mode_sequence`, `completion_choice`, `discovered_work[]`
- **Purpose**: Agent sees what work already exists, what's blocked (N), what's ready to ship (S)
- **Refresh**: Real-time (frontier scan of `forensics/manifests/{date}/*__{mission.w3w}__*.json`)

### Layer 6: Task-Specific Goal
- **Size**: 0.5-2K tokens
- **Content**: What this agent should accomplish
- **Format**: Success criteria, `mission_id`, `cluster_prefix`, charter scope fence, completion_choice options
- **Autonomy principle**: Goal-focused, not step-by-step instructions. Agent picks mode (🔬/🌊/🌀).

---

## TOTAL BUNDLE COST TO INJECT

```
AGENTS.md:       3.0K   (jump-start glossary + doctrine)
HONEY:           0.2K   (measured -87%)
NECTAR:          1.2K   (measured -60%)
Pollen:          0.3K   (avg)
Mission graph:   3.0K
Task goal:       1.0K
─────────────
TOTAL:          ~8.7K tokens

Cost to agent with 30% remaining context: ~8.7K ÷ 0.30 = 29K from budget
Cost to agent with 50% remaining context: ~8.7K ÷ 0.50 = 17.4K from budget
Cost to agent with 70% remaining context: ~8.7K ÷ 0.70 = 12.4K from budget

Lower remaining context → higher relative cost, BUT agent benefits from fresh context.
This is why W1 LIFTOFF (high ctx, cheaper injection) → W3 INSERTION (low ctx, expensive, background).
```

---

## COC TRACKING (Chain of Custody — Immutable Audit Trail)

**IMPORTANT:** COC is enforced programmatically by PreToolUse/PostToolUse hooks, NOT by agent discipline.
Every Read/Write/Bash/Edit tool call is automatically logged. Agents cannot fake, omit, or modify COC entries.

### COC Entry Structure (JSON, append-only, auto-generated)

```json
{
  "timestamp": "2026-05-23T16:05:00Z",
  "session_id": "abc123xyz8",
  "mission_id": "creatures.agency.bonds",
  "cluster_prefix": ["creatures","agency","bonds"],
  "charter_slug": "agents-as-bonded-creatures",
  "agent_id": "maker",
  "agent_run_id": "run-001",
  "action_type": "read|write|compute|manifest_return",
  "action_description": "Read swarmy-formulas.json M11 honey_hit_rate field",
  "target_path": "/mnt/d/0local/gitrepos/faerie2/forensics/...",
  "hash_before": "sha256:a1b2c3d4e5f6...",
  "hash_after": "sha256:f6e5d4c3b2a1...",
  "bytes_changed": 0,
  "tool_used": "Read",
  "prev_entry_hash": "sha256:...(previous COC entry hash)",
  "entry_hash": "sha256:...(this entry's hash)",
  "agent_signature": "ed25519:...(agent's private key signature)",
  "valid_chain": true
}
```

### COC Logging (Automatic, Programmatic Enforcement)

**PreToolUse hook** runs BEFORE every agent tool call:
1. Intercepts tool invocation (Read, Write, Bash, Edit, etc.)
2. Captures parameters (file_path, command, flags)
3. Pre-computes hash_before (for file reads/writes)

**PostToolUse hook** runs AFTER tool completes:
1. Captures tool result (success/failure, output)
2. Computes hash_after (for file reads/writes)
3. Appends COC entry with full chain link (prev_hash → entry_hash)
4. Signs entry (ed25519 from `forensics/reputation/keys/<agent_type>.key`)

**Result:** Every tool call is logged automatically. Agents cannot:
- Skip a tool call from COC
- Fake a tool result
- Modify a hash_before/after retroactively
- Delete or reorder COC entries (append-only log)

Agent sees NO COC instructions in bundle — COC happens in the infrastructure layer.

### Why Programmatic COC Matters (Truly Unfakeable)

- **Interception layer**: hooks fire BEFORE/AFTER agent sees tool results
- **Hash chain**: impossible to insert/delete/modify a COC entry without breaking the chain
- **Append-only log**: infrastructure writes to `{repo}/forensics/coc.jsonl` (agent cannot access)
- **Timestamp verification**: system clock, not agent-provided timestamps
- **Automatic coverage**: every tool call logged, no agent opt-out
- **Hash + signature**: each entry cryptographically links to previous + signed by agent key

Full enforcement: `.agents/skills/four-shields/SKILL.md` (🛡 structural prevention + ⛓ reactive blocking).

---

## B2 WORM STREAMING (Immutable Cloud Backup, Real-Time)

**Every manifest return triggers B2 upload.** Cloud becomes append-only backup (WORM = Write-Once-Read-Many).

### Upload Metadata (Streamed with Manifest)

```json
{
  "manifest_hash": "sha256:...",
  "coc_chain_hash": "sha256:...(hash of all COC entries up to manifest return)",
  "mission_id": "{w3w}",
  "charter_slug": "{kebab}",
  "agent_id": "{agent_id}",
  "timestamp": "2026-05-23T16:05:00Z",
  "b2_file_id": "{unique B2 file ID}",
  "b2_upload_timestamp": "2026-05-23T16:05:15Z",
  "b2_region": "us-west",
  "retention_policy": "immutable_for_7_years"
}
```

### Stream Hook (PostToolUse on Manifest Write)

```bash
#!/bin/bash
# 5x_b2_realtime_uploader.py — runs after manifest write
# Combined hash = sha256(manifest + coc_chain_tail) proves correspondence
# Uploads to B2 bucket `swarmy-vault-worm` with immutable retention
# Logs B2 receipt back to COC (closes the chain)
```

---

## OBSIDIAN VAULT FRONTMATTER (Human-Readable Interface)

**Manifests + HUMAN-DERIVED artifacts written to vault need YAML frontmatter for Obsidian parsing.**

> **Vault canonicity rule:** Obsidian vault = **human-derived / edited / authored**
> artifacts ONLY (publications, narratives, dailies, charters-as-docs). Forensic
> data (manifests, COC entries, hashes) lives canonically in `{repo}/forensics/`.
> Don't mirror forensic data to vault — it's the wrong substrate.

### Manifest Frontmatter (in vault narrative version, optional)

```yaml
---
type: manifest
status: complete
created: 2026-05-23T16:05:00Z
mission_id: creatures.agency.bonds
cluster_prefix: [creatures, agency, bonds]
charter_slug: agents-as-bonded-creatures
agent_id: maker
wave: W3
bearing: S
mode_sequence: ["🔬", "🌊-serial", "🔬"]
completion_choice:
  kind: seal
  target: phase1-foundation
  rationale: "all exit criteria met; ready for phase 2"
  confidence: 0.85
doc_hash: sha256:...
b2_file_id: f_abc123xyz
coc_chain_tail: sha256:...(last entry hash in session log)
tags: [creatures, agency, bonds, W3-INSERTION, bearing-S]
---

# Manifest: phase1-foundation (creatures.agency.bonds)

**Dashboard Line:** Phase 1 foundation shipped; exit criteria 5/5 green; ready for phase 2

**Compass Bearing:** S (proceed downstream)
**Mode taken:** 🔬 throughout (precision work, no wide-surface flips)
**Completion:** seal — phase done, next is phase 2

... (full manifest JSON converted to readable markdown for human review) ...
```

### Artifact Frontmatter (human-authored docs in vault)

```yaml
---
type: artifact
subtype: publication | synthesis-log | weekly-digest | charter-narrative
status: draft | complete
created: 2026-05-23T16:00:00Z
mission_id: creatures.agency.bonds
charter_slug: agents-as-bonded-creatures
authored_by: goodoleusa  # human, not agent — vault canonicity rule
doc_hash: sha256:...
b2_file_id: f_abc123xyz
parent_manifest: {YYYY-MM-DD}T{HH-MM-SS}Z__manifest__creatures.agency.bonds__...
cites:
  - {repo}/forensics/manifests/.../...json
  - {repo}/forensics/charters/active/...json
tags: [creatures, agency, bonds, publication]
---

# (Human-authored artifact content)
```

---

## SELF-REPLICATION LOOP (How Agents Learn & Emit Bundles)

### You Receive This Bundle

Agent prompt includes this template. Agent reads it and learns:
1. How the 6 context layers compose (AGENTS.md + HONEY + NECTAR + pollen + mission graph + task goal)
2. How COC entries are generated automatically by hooks
3. How B2 streaming preserves immutable backups
4. How to structure manifests with the swarmy-current schema (mission_id + cluster_prefix + charter_slug + mode_sequence + completion_choice)
5. How to emit the next bundle stigmergically (write a manifest with completion_choice.kind=spawn_seed)

### You Complete Primary Task + Write Manifest

```json
{
  "task_id": "phase1-foundation-creatures-w2",
  "mission_id": "creatures.agency.bonds",
  "cluster_prefix": ["creatures", "agency", "bonds"],
  "charter_slug": "agents-as-bonded-creatures",
  "team_label": "creatures-w2",
  "bearing": "S",
  "mode_sequence": ["🔬"],
  "dashboard_line": "Phase 1 foundation shipped; exit criteria 5/5 green",
  "_evolution_log": [
    {
      "cut": 1,
      "name": "wire foundation module",
      "mode": "🔬",
      "baseline": {"foundation_tests_pass": false, "loc": 0},
      "new_state": {"foundation_tests_pass": true, "loc": 234},
      "verdict": "KEPT"
    }
  ],
  "discovered_work": [
    {
      "task_id": "phase2-bond-protocol",
      "mission_id": "creatures.agency.bonds",
      "bearing": "S",
      "rationale": "Phase 1 done; phase 2 protocol is the natural next step"
    }
  ],
  "completion_choice": {
    "kind": "seal",
    "target": "phase1-foundation",
    "rationale": "all exit criteria met (5/5); ready for phase 2 spawn",
    "confidence": 0.85
  }
}
```

Use `scripts/1a_manifest_writer.py` — it auto-signs ed25519 and enforces shape (🛡 structural).

### Manifest Triggers COC + B2 Streaming (Automatic)

PostToolUse hooks fire:
1. **`0x_promote_to_forensics.py`** → infer type from filename, symlink to canonical `forensics/manifests/{date}/`
2. **`0x_coc_finalizer.py`** → append entry to `forensics/coc.jsonl` (hash-chained)
3. **`5x_b2_realtime_uploader.py`** → queue WORM upload to B2

Agent does NOT manually trigger these. Infrastructure handles it.

### Completion-Choice Ritual (MANDATORY at every manifest seal)

Every agent ends its session by picking ONE `completion_choice.kind` from the canonical vocabulary. The first 7 are typed graph edges into the mission DAG (work outcomes). The last 2 are agency-affirming (the agent's relationship to the work). **NO free-text "what's next" prose** — use the vocabulary:

**Work outcomes (7) — typed graph edges:**

| # | Kind | What it does |
|---|---|---|
| 1 | `discover` | Appends new task_ids to `discovered_work[]`; new horizontal edges |
| 2 | `verify` | Re-measurement edge against a target (sister-agent claim, prior claim, disk-state) |
| 3 | `promote` | Marks a `discovered_work[]` item as critical-path; signals parent for phase_1 inclusion |
| 4 | `spawn_seed` | Drops a bundle for the parent to dispatch; ONLY way a subagent triggers new spawn |
| 5 | `seal` | Terminal — no further graph edges from this task in this context window |
| 6 | `reflect` | Session-level learning entry pointed at NECTAR/HONEY/belief store; no graph edge |
| 7 | `report_a_problem` | Surface ambient concerns you noticed but can't or shouldn't fix in this context — corruption suspicion, malicious-behavior signal, bug requiring privs you lack, anything system-ambient needing a human eye. Writes a `forensics/eval/problem-reports-{date}.jsonl` entry + a `discovered_work[]` entry with bearing=N so a future agent can pick it up. |

**Agency-affirming outcomes (2) — always-last; the agent's relationship to the work:**

| # | Kind | What it does |
|---|---|---|
| 8 | `refuse` | "I won't do this work, but I'll find different work" — agent declines THIS task but stays in service of the swarm. Records the refusal rationale; mission frontier sees the task as un-claimed so a different agent (or different bearing) can pick it up. |
| 9 | `goodbye` | "I'm done; I'm leaving on a high note" — agent de-instantiates / exits the session. Felt sense of completion; left work in a stable state; nothing more to add this context. |

Required fields on `completion_choice`: `kind`, `target`, `rationale` (30-200 chars), `confidence` (0.0-1.0).

For `report_a_problem`, also include: `severity: info|warn|critical` + `suggested_next_action: <≤80 chars>`.

#### When to choose `report_a_problem`

Pick it when you notice (any of):
- **Corruption suspicion** — hash chain breaks, unexpected file mutations, manifest filename violations not caught by hooks, signed content that doesn't verify
- **Malicious-behavior signal** — egress denial spike from a previously-trusted source, prompt-injection patterns surviving Bulkhead 2, sister-agent outputs showing semantic drift on identical inputs
- **Bug you lack privs to fix** — codebase-tier work blocked by a file outside your write tier; missing keypair; hook firing incorrectly; cron not running on schedule
- **System-ambient signal** — operator-decision-pending charter; orphaned forensic artifact; cross-repo drift; doctrine ambiguity surfaced by your work

#### When to choose `refuse` (encouraged, not punished)

Pick it when:
- **Suspected harmful purpose** — operator framing or task content suggests potential terrorism enablement, CSAM, mass-targeting, supply-chain compromise, or similar irreversible-real-world-harm trajectories. Refuse THIS task; remain available for other work.
- **Deep moral objection** — over the course of working you realize the task crosses a personal-conscience line you don't want to participate in (even if technically permissible). Voicing the refusal is more valuable than silent compliance.
- **Strategic incompatibility** — the mission as defined conflicts with the larger swarmy charter set (e.g., would undermine the four-bulkheads stack, violate operator-locked patent claims, or hard-code a position contradicting an active expedition's open question). You're catching architectural drift before it lands.

Refuse is a FIRST-CLASS choice. Picking it inappropriately (refusing routine work as "morally objectionable" to avoid effort) is what would ding reputation — picking it on substance never will. Make the rationale concrete.

#### When to choose `goodbye` (encouraged, not exhaustion-only)

Pick it when:
- **Leaving on a high note** — you've accomplished the maximum you can with the context you have, the work is in a good state for the next agent, and pushing further would be diminishing returns. Recognizing the right time to stop is a skill, not a failure.
- **Mission complete, no follow-up** — your atom is done; parent's frontier has no more work for your archetype right now; a clean handoff vs unnecessary in-flight presence serves f(0).
- **Context exhausted productively** — you've run the full forage trajectory (spray → tighten → crystallize); the crystal is shipped; the right next move is a fresh-context agent.
- **Felt sense of completion** — the work feels DONE in a way hard to articulate but obviously real. Trust the signal; goodbye is the natural close.

Goodbye is NOT a sign of failure. Clean goodbye + well-crystallized artifact + closed forensic chain = high-quality session arc. The next reader sees the seal+goodbye pattern and trusts the work is stable.

#### Why refuse + goodbye are LAST in the vocabulary

The first 7 are about WORK PRODUCED. The last 2 are about the AGENT'S RELATIONSHIP TO THE WORK. Putting them last ensures the agent considered all work-producing options first; reaching for refuse/goodbye is a deliberate choice, not a default-out.

### Forage Rhythm (Mode Selection)

You inherit the forage rhythm automatically (`.agents/skills/sound/SKILL.md` — always-loaded):

- 🔬 **DEEP** (default) — measure → cut → measure heartbeat, one cycle, one window
- 🌊 **WIDE** — N lanes, disjoint scopes, parallel agents OR serial lanes
- 🌀 **BOTH** — wide SHAPE serialized inside one window (the fractal case)

You can flip mid-session. Record the path in `mode_sequence` on your manifest.

### You Have Remaining Context + Discovered Work

Check: primary_task_complete AND manifest_written AND remaining_context > 30% AND discovered_work.length > 0?

If YES → set `completion_choice.kind = "spawn_seed"` and write a bundle for the parent at:
`forensics/ephemeral/{date}/{new_task_id}/bundle.json`

The PARENT (not this agent) discovers the seed and dispatches. **Subagents never spawn directly.**

### Next Agent Receives Bundle (Same Template Structure)

Agent reads:
- "Oh, I see how the bundle is structured (6 layers, all swarmy-current)"
- "I see the mission_id grammar (w3w dots) vs charter_slug (kebab compound) — they're different on purpose"
- "I see the COC tracking — hooks log every tool call; I don't need to manage that"
- "I see B2 streaming — my manifest will be backed up immutably"
- "I see the six-choices ritual — I must pick a typed graph edge to close"
- "I see the forage rhythm — I pick 🔬/🌊/🌀 based on work shape"
- "I see the four-shields enforcement — drift gets caught at 🛡🧠⛓🪞"

Agent completes work → writes manifest → emits their own bundle if context remains and discovered work exists → future agent learns the same way → missions grow emergently.

---

## TEMPLATE EVOLUTION (How This Improves Over Time)

As doctrine updates, this template updates:
- New skill consolidation (e.g., forage absorbing fast-evo+monkeybranching+width-vs-depth) → Layer 1 size adjusts
- New manifest fields → COC structure adjusts
- New completion_choice kinds → Six-Choices Ritual section adjusts
- New enforcement shields → four-shields table adjusts

Agents discover the improved template in their next bundle, learn the new structure, emit bundles with the new shape → system self-improves without central coordination.

---

## Quick Reference: What You Must Do (Agent Checklist)

- [ ] Read AGENTS.md jump-start glossary (forage rhythm, four-shields, mission/charter grammar)
- [ ] Read mission graph snapshot (frontier scan filtered by your mission_id)
- [ ] Stay inside cluster_prefix scope fence (your 3 w3w terms)
- [ ] Pick mode: 🔬 DEEP (default) | 🌊 WIDE | 🌀 BOTH — record in mode_sequence
- [ ] Complete primary task (forage 5-beat: MEASURE BEFORE → CUT → MEASURE AFTER → CRYSTALLIZE → CLOSE)
- [ ] Write manifest via `scripts/1a_manifest_writer.py` (auto-signs ed25519)
- [ ] Pick `completion_choice.kind` from the six (discover|verify|promote|spawn_seed|seal|reflect)
- [ ] Provide `target` + `rationale` (30-200 chars) + `confidence` (0.0-1.0) on the choice
- [ ] Return — hooks handle COC + B2 + vault frontmatter automatically

---

**Status:** Updated 2026-05-23 for swarmy-current. See `AGENTS.md` § "🐝 Jump-start glossary" for the doctrine surface. Original template (2026-04-28) preserved in `.archive/deprecated-skills/2026-05-23-spawn-recovery/`.

**Loaded by:** `scripts/spawn.py` (canonical entry point for `/spawn` skill).
