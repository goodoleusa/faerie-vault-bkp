# EVAL-FLOW — End-to-End Training & Score Pipeline

How an agent's self-reported training event becomes a hash-chained, court-admissible score
that gates tier promotion — with zero agent ability to see its own prior scores before running.

---

## The Flow at a Glance

```
agent run (blind)
      ↓ writes append-only to own card
##  Training Log                                     (agent card, PUBLIC append)
      ↓ drained at /handoff by membot
vault_agent_evolution_sync.py                        (aggregator — membot-only)
      ├──▶ hooks/state/eval-history.jsonl            (hash-chained canonical)
      ├──▶ $CT_VAULT/03-Agents/training-events/*.md  (vault mirror, human-readable)
      └──▶ ## Last Training  on agent card            (PRIVATE — parent-only, hidden from next run)
      ↓
tier promotion gate
      (evalbot scores only, sustain ≥0.90 × 3 consecutive runs → tier up, baseline resets)
```

Two kinds of entries feed `eval-history.jsonl` — both share the same hash chain:
1. Agent training events (from `vault_agent_evolution_sync.py`).
2. System-eval composite snapshots (from `eval_harness.py` — the 7-dimension MBS run).

---

## Step 1 — Agent writes its own Training Log (blind)

During or immediately after a run, if the agent beat its target or discovered a durable
technique, it appends one entry to `## Training Log` on its own card:

```
### 2026-04-20T14:02:33Z | deployment H1 editorial summary | score=0.96 | prev=0.94 | delta=+0.02 | source=self
- Lead with alarming fact first (actor/action/timeline), evidence second
- Under-write within budget (299/500 tokens frees 40% for polish)
- Walk every claim before submit — 100% citation rate is measurable and achievable
```

Rules:
- Append-only. Never edit an existing entry. Never rewrite the section.
- `source=self` for OTJ self-assessment. `source=evalbot` for independent scoring.
- Bullets are durable learnings only — no case data, no entity names (court-admissibility rule).
- The agent does **not** read `## Last Training` (parent-only; anti-gaming — see `rules/agents.md` §2).

The bundle model (`rules/agents.md` §2) means the sub-agent never sees its own card
artifact. The parent injects the PUBLIC discovery JSON inline into the spawn prompt, and
the agent returns the Training Log entry as part of its manifest. A follow-up `Edit` by
the parent appends it to the card. (Implementation in-flight — until the bundle model is
universal, some agents still self-append during the run.)

---

## Step 2 — Membot drains at /handoff

At faerie cycle end (`/handoff`), the membot invokes:

```bash
python3 scripts/eval/vault_agent_evolution_sync.py
# optional: --dry-run to preview  |  --backfill to seed from ## Last Training sections
```

For each agent card, the aggregator:

1. **Parses new `## Training Log` entries** — anything with `timestamp >
   last_aggregation_ts` from `hooks/state/eval-aggregation-state.json`.
2. **Builds a canonical JSONL record** with agent, timestamp, scores, delta, source,
   training_type, context, learnings, aggregated_at.
3. **Hash-chains it** — `entry_hash = sha256((prev_hash || "genesis") + sorted_json(entry))`.
4. **Appends to `hooks/state/eval-history.jsonl`** (immutable, one object per line).
5. **Writes a vault mirror** to `$CT_VAULT/03-Agents/training-events/{agent}-{slug}.md`
   with frontmatter + body; stamped by `stamp_doc_hash.py` on next vault sweep.
6. **Updates `## Last Training`** on the agent card with the newest aggregate. This
   section is parent-facing only; the anti-gaming bundle model keeps it out of the
   next run's context.
7. **Advances the state cursor** in `eval-aggregation-state.json` to `{latest_ts,
   latest_entry_hash}`.

Idempotent by construction — rerun-safe.

---

## Step 3 — Tier promotion gate

Reads `hooks/state/eval-history.jsonl`. Only `source: evalbot` entries are authoritative.

- Sustain **≥0.90 across 3 consecutive evalbot runs** → agent tiers up. Baseline resets at the
  new tier; card's `Tier:` line updates in the `## Last Training` section.
- `source: self` entries are directional — they feed training-queue redemption tracking, never
  tier promotion.
- Evalbot itself never reads its own prior scores (anti-bias); it reads the agent's work
  product and scores it against the rubric.

Tier rubrics:
- **Tier 1** — standard tasks. Baseline evalbot score.
- **Tier 2** — harder test cases, stricter citation requirements, cross-session consistency.
- **Tier 3** — novel problems, synthesis across domains.
- **Tier 4** — research-lead, open-ended multi-phase work.

See `rules/agents.md` §4 "Self-Update & Scoring Protocol" for the full rubric.

---

## Step 4 — Training-queue redemption (parallel track)

When an agent did **not** beat its last score, it appends to `training-queue.json` with
`on_the_job_eligible: true`. If that agent later beats its target during real work:

1. Self-update `## Training Log` (source=self).
2. Set the queue entry's `status = "redeemed_on_the_job"`.
3. Append a REDEMPTION record to `hooks/state/training-log.jsonl`.

The aggregator picks up the `## Training Log` entry on the next /handoff, the event flows
into `eval-history.jsonl`, and the redemption is court-admissible.

---

## Schemas

Full JSON schemas live in `hooks/state/schemas/`:

- `training-queue.schema.json`
- `eval-history.schema.json`
- `training-log.schema.json`
- `eval-aggregation-state.schema.json`

---

## The `/eval` command suite

Entry point for researcher-invoked evals (see `commands/eval.md`):

| Command | Purpose |
|---|---|
| `/eval baseline {agent}` | Establish zero-point reference. source=evalbot, hash-chained. |
| `/eval run {agent} --task {id}` | One-shot scored eval. Updates card only if beat baseline. |
| `/eval train {agent} --on-job [--n N]` | Enables MINI_LEARNING for next N spawns. |
| `/eval compare --a {r1} --b {r2}` | A/B diff from eval-history.jsonl. Pre-registered hypotheses. |
| `/eval compare --agent {a} --runs last-{N}` | Cohort stats, same anti-HARKing discipline. |
| `/eval repeat [--seed S]` | Replay last config from eval-config-history.jsonl. |

Every invocation appends to `eval-config-history.jsonl` and emits a COC v2 manifest
under `hooks/state/eval-{subcmd}-{SID8}-{AID16}.json`.

---

## Path resolution — how the scripts find their state

Both `eval_harness.py` and `vault_agent_evolution_sync.py` resolve their config root in
priority order:

1. `FAERIE2_HOME` environment variable — faerie2 standalone install root (preferred).
2. `CLAUDE_HOME` environment variable — global Claude CLI home (legacy + dogfood).
3. `~/.claude` — platform default.

This keeps faerie2 standalone self-contained: ship it with a `FAERIE2_HOME` export in
the install shim and everything reads/writes inside the standalone install tree.

---

## See also

- `rules/agents.md` §2 (anti-gaming / bundle model) · §4 (scoring authority, tier graduation)
- `agents/evalbot.md` — evalbot card (independent scorer protocol)
- `agents/membot.md` — membot card (Training Log Collection section)
- `commands/eval.md` — /eval command surface
- `scripts/eval/eval_harness.py` — 7-dimension composite scorer
- `scripts/eval/vault_agent_evolution_sync.py` — membot aggregator
