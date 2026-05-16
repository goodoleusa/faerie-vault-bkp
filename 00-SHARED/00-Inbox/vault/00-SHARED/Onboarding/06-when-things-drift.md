---
type: guide
status: active
tags: [onboarding, debugging, troubleshooting, drift]
parent: Onboarding/INDEX
up: Onboarding/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:cb1c63dba5009332e5962cace9f147a28a3b10ffa50934baa2cd3750bb72f2be
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Onboarding](INDEX.md) · [⌂ Home](../../HOME.md)

# 06 — When Things Drift

Diagnosis and fix patterns for common failure modes.

---

## Diagnosis First

Before fixing anything:

```bash
python3 ~/.claude/scripts/9x_lean_query.py --get-all
```

This gives you the actual system state: context %, wave state, queue counts,
agents in flight. Use measured data — not assumptions.

---

## Common Failure Modes

### Queue stops draining

**Symptom:** `/run` claims nothing. Queue shows tasks but none execute.

**Diagnosis:**
```bash
python3 ~/.claude/scripts/9x_lean_query.py --get-queue
# Look for: all tasks have blockedBy set, or all claimed by stale sessions
```

**Fix — stale claims (claimed >2h ago):**
```bash
python3 ~/.claude/scripts/7x_queue_ops.py expire-stale-claims
```

**Fix — all tasks blocked:**
Find and complete the blocking task, or unblock manually:
```bash
python3 ~/.claude/scripts/7x_queue_ops.py unblock task-042
```

---

### Agent returns a partial manifest

**Symptom:** Dashboard shows `PARTIAL — still running in background`

**This is normal.** Partial is better than infinite wait. The agent
timed out but wrote what it had. Read `output_path` for partial findings.

If the partial output is enough: mark the task complete manually:
```bash
python3 ~/.claude/scripts/7x_queue_ops.py complete task-042
```

If not enough: requeue the task at the appropriate priority.

---

### Context grows too fast

**Symptom:** Context % hits 85%+ before W3 has run.

**Diagnosis:**
```bash
cat ~/.claude/hooks/state/piston-checkpoint.json
# Look for: context_pct, wave_state, deferred_reason
```

**Fix — manually trigger W3 before auto-compact:**
Run W3 synthesis agents with `run_in_background: true` now, before compact fires.

**Prevention:**
- Use `9x_lean_query.py --get-wave` after W2 to check context %
- If >70%: fire W3 immediately, do not wait

---

### Vault doc_hash showing as pending

**Symptom:** Vault documents have `doc_hash: sha256:pending` after agent run.

**Fix:**
```bash
python3 ~/.claude/scripts/stamp_doc_hash.py --file path/to/doc.md
```

**Prevention:** The spawn boilerplate includes stamp instructions.
If agents skip it, the hook catches it at session stop.

---

### piston-checkpoint.json shows stale wave state

**Symptom:** `/faerie` re-runs W1 agents that already completed.

**Diagnosis:**
```bash
cat ~/.claude/hooks/state/piston-checkpoint.json
# Look for: wave_state, last_updated
```

**Fix — update checkpoint manually:**
```bash
python3 ~/.claude/scripts/update_piston_checkpoint.py \
  --wave W2 --context-pct 45
```

---

### NECTAR tail-30 showing old findings

**Symptom:** Agents at startup report "no applicable NECTAR techniques" even
though prior sessions covered the same domain.

**Diagnosis:** `/handoff` may not have run at the end of prior sessions.
Pollen observations never promoted to NECTAR.

**Fix:**
```bash
python3 ~/.claude/scripts/9x_memory_bridge.py --promote-pollen --session <sid>
```

---

### Hook not firing (spawn contract violated)

**Symptom:** Agent spawns with direct prompt construction (not template).

**Diagnosis:**
```bash
cat ~/.claude/hooks/state/spawn-contract-violations.jsonl | tail -5
```

**Fix:**
Check that `8x_spawn_contract_enforcer.py` is registered in `settings.json`
under `hooks.PreToolUse`. If not, re-register.

---

## Equilibrium Audit

Run this when you suspect something structural is wrong:

```bash
python3 /mnt/d/0local/gitrepos/faerie2/scripts/9x_equilibrium_audit.py --check-scripts
```

Checks script tier declarations, missing REPLACES/METRIC fields, core vs sauce classification.

---

## Related

- [[04-reading-manifests]] — understanding manifest status for diagnosis
- [[05-using-the-queue]] — queue health and management
- [[../Architecture/piston-waves]] — piston state architecture
- [[../Glossary/terms]] — piston, wave, blocker, stale claim defined
