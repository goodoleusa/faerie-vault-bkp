# AGENT-CARD-REPUTATION-SCHEMA.md

**Task:** task-20260425-133355-9d39  
**Author:** python-pro  
**Date:** 2026-04-25  

---

## Overview

Agent cards (`~/.claude/agents/{type}.md`) are extended with a fourth section,
`## REPUTATION`, which acts as the authoritative reputation ledger for each
agent type. No parallel registry exists — the card IS the ledger.

Cards are already loaded at spawn time, so reputation values auto-inherit into
every new session without additional lookup cost.

---

## Card Section Layout

```
## Identity          ← existing (YAML frontmatter + description)
## BASELINE          ← existing (locked; eval-only writes)
## Last Training     ← existing (append-only; agent self-writes after runs)
## REPUTATION        ← NEW (auto-managed; do not hand-edit)
```

---

## REPUTATION Section Schema

```markdown
## REPUTATION (auto-managed; do not hand-edit)

- manifest_truthfulness_score: 0.85
  # Rolling 30-day average derived from adversarial manifest reviews.
  # Each review contributes: +1 (verified true claim) or -1 (caught lie),
  # decay-weighted by exp(-days_since_review / 30).
  # Default for new agents: 0.85.

- mutation_verification_pass_rate: 0.85
  # Fraction of files_written claims in manifests that were verified present
  # after the agent run completed. Scored by reputation tracker hook.
  # Default for new agents: 0.85.

- caught_lying:
    count: 0
    last_session_id: null
    decay_factor: 1.0
  # count       — cumulative verified lies (never decrements; only decay matters).
  # last_session_id — session_id8 of most recent caught-lie event.
  # decay_factor — exp(-days_since_last_lie / 14); recomputed at every card update.
  #                1.0 when count == 0 (no lies ever recorded).

- adversarial_auditor_score: 0.85
  # When THIS agent acts as auditor of another agent's manifest:
  # fraction of its "catch" calls subsequently confirmed valid by eval harness.
  # Default for new agents: 0.85.

- routing_weight: 1.0
  # Composite score used by 7x_spawn_template.py route_task_by_content():
  #
  #   routing_weight = max(
  #       DEMOTION_FLOOR,                         # 0.1
  #       base × (1 + truthfulness − caught_lying.decay_factor × 0.5)
  #   )
  #
  # where base = 1.0 for new agents.
  #
  # Thresholds (7x_spawn_template.py constants):
  #   DEMOTION_THRESHOLD  = 0.5   → reroute to stigmergy-scout (classification mode)
  #   PROMOTION_THRESHOLD = 0.85  → eligible for autonomous multi-file complex tasks
  #
  # Default for new agents: 1.0.

- last_updated: "2026-04-25T13:33:55Z"
  # ISO 8601 UTC timestamp of most recent automated update.

- signed_by: "ed25519:<base64-signature>"
  # Ed25519 signature over the canonical JSON representation of all REPUTATION
  # fields (excluding signed_by itself). Key: ~/.claude/agents/{type}.key.
  # Computed by 9x_reputation_tracker.py via 9x_agent_sign.py helpers.
  # Value "ed25519:init" indicates the initial default block (not yet event-derived).
```

---

## Routing Weight Formula (detail)

```
truthfulness = manifest_truthfulness_score           # 0.0 – 1.0
lying_penalty = caught_lying.decay_factor × 0.5     # 0.0 – 0.5
raw = 1.0 × (1 + truthfulness − lying_penalty)
routing_weight = max(0.1, min(2.0, raw))
```

New-agent defaults → `1.0 × (1 + 0.85 − 1.0 × 0.5)` = **1.35**, capped at 1.0
(base is implicitly clamped so weight starts at 1.0 for pristine agents).

Practical ceiling: 1.0 base × (1 + 1.0 truthfulness − 0 lying) = 2.0 (perfect agent).

---

## Thresholds

| Constant              | Value | Effect                                                      |
|-----------------------|-------|-------------------------------------------------------------|
| `DEMOTION_FLOOR`      | 0.1   | Absolute minimum routing weight                             |
| `DEMOTION_THRESHOLD`  | 0.5   | Below → rerouted to `stigmergy-scout` (classification mode) |
| `PROMOTION_THRESHOLD` | 0.85  | Above → eligible for autonomous multi-file task execution   |

---

## Update Lifecycle

```
manifest written by agent
    └─► PostToolUse hook 9x_reputation_tracker.py fires
            └─► appends event to ~/.claude/hooks/state/reputation-events.jsonl
                    └─► every 10 events: batch processor runs
                            └─► recomputes REPUTATION block per affected agent
                            └─► atomic tmp+rename write to ~/.claude/agents/{type}.md
                            └─► Ed25519 sign via 9x_agent_sign.py helpers
                            └─► COC entry via 4x_coc_writer.py
```

---

## Backward Compatibility

Cards without a `## REPUTATION` section are treated as having all default values
(`truthfulness=0.85`, `routing_weight=1.0`). The init script
(`scripts/9x_init_reputation.py`) back-fills existing cards idempotently.

---

## File Ownership

| File                                              | Writer                       |
|---------------------------------------------------|------------------------------|
| `~/.claude/agents/{type}.md` (REPUTATION block)  | `9x_reputation_tracker.py`   |
| `~/.claude/hooks/state/reputation-events.jsonl`  | `9x_reputation_tracker.py`   |
| `forensics/coc.jsonl`                             | `4x_coc_writer.py` (via hook)|

Human and agents MUST NOT hand-edit `## REPUTATION` blocks. Violations are
detected by `8x_deny_rule_validator.py` path patterns.
