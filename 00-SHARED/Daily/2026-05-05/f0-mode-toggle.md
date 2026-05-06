# f(0) Mode Toggle — Easy Switching Between Passive & Active Constraint Enforcement

## Quick Toggle

### Via `/faerie` Skill (Recommended)
```bash
/faerie --f0-mode passive    # Measure only, don't enforce
/faerie --f0-mode active     # Enforce constraint (block if violated)
/faerie --f0-mode dry-run    # Check constraint, report, don't act
```

The `/faerie` skill updates `f0-config.json` automatically when you pass `--f0-mode`.

### Via Direct Config Edit
```bash
# Edit the config file
vim /mnt/d/0local/gitrepos/faerie2/.claude/f0-config.json

# Change: "f0_mode": "passive" → "f0_mode": "active"

# Then sync the setting
/faerie --f0-sync
```

### Via Command Line (One-Time Override)
```bash
# Pass --mode to constraint enforcer directly
python3 /mnt/d/0local/gitrepos/faerie2/.claude/scripts/9x_f0_constraint_enforcer.py \
  --total-budget 150000 \
  --presend-estimate 4500 \
  --mode active
```

---

## Modes Explained

### 1. `passive` (Default)
**Behavior:** Measure f(0) but don't block spawns.

**What happens:**
- Presend cost is checked against f(0) constraint
- If violated (presend > 5% of budget): log warning, proceed anyway
- Exit code: 0 (proceed) or 2 (warn)

**Use case:** Phase 1 baseline measurement. Understand current f(0) without changing behavior.

**Logs:** `forensics/metrics/f0-constraint-log.jsonl` (warnings recorded)

---

### 2. `active` (Enforced)
**Behavior:** Enforce f(0) ≤ 0.05 as hard constraint.

**What happens:**
- Presend cost is checked against f(0) constraint
- If violated: block spawn, recommend mitigation (reduce bundle OR parallelize)
- Exit code: 0 (proceed) or 1 (block)

**Use case:** Phase 3 cutover. Validate that constraint enforcement works. Test whether tight f(0) improves system behavior.

**Logs:** `forensics/metrics/f0-constraint-log.jsonl` (blocks recorded)

**Mitigation if blocked:**
1. Reduce bundle size (~{int(overage*1.2)} tokens)
2. Increase agent count (parallelize presend cost across agents)
3. Wait for next session (context may drop, easing pressure)

---

### 3. `dry-run` (Analysis Only)
**Behavior:** Check constraint without changing behavior.

**What happens:**
- Presend cost is checked against f(0) constraint
- Whether violated or not: exit code 2 (warn), no blocking
- Useful for analyzing constraint violations in retrospect

**Use case:** Debugging why constraint was violated. Understanding presend cost breakdown.

**Logs:** `forensics/metrics/f0-constraint-log.jsonl` ([DRY-RUN] entries)

---

## How to Measure the Impact of Mode Changes

### A/B Testing: Passive vs Active

**Setup:**
```
Week 1: passive mode (5 sessions)
  - Measure baseline f(0) without enforcement
  - Record: FFMx, coherence, agent quality

Week 2: active mode (5 sessions)
  - Same missions/goals, but constraint enforced
  - Record: FFMx, coherence, agent quality, blocked spawns

Compare:
  - Did active mode reduce f(0)? (should be yes)
  - Did it reduce FFMx? (should be no, or minimal impact)
  - Did quality/coherence improve or degrade? (measure)
  - How many spawns were blocked? (expect <10%)
```

### Metrics to Watch

**In passive mode:**
- Track f(0) trend: is it creeping up? Stable?
- Log presend overage: how many times would constraint be violated?

**In active mode:**
- Track blocked spawns: % that hit constraint
- Track mitigation success: when we reduce bundle, does next spawn fit?
- Compare FFMx to passive baseline: should be similar or better

**Both modes:**
- Monitor coherence (should stay ≥0.90)
- Monitor agent quality (should maintain or improve)
- Check discovery density (should stay 2.5-3.5)

---

## Implementation: How f(0) Mode is Wired

### Config File
**Location:** `/mnt/d/0local/gitrepos/faerie2/.claude/f0-config.json`

Current setting:
```json
{
  "f0_mode": "passive",
  "f0_target": 0.05,
  ...
}
```

### Enforcement Hook
**Script:** `9x_f0_constraint_enforcer.py`

**Called by:** PreSpawn hook in settings.json (to be wired)

**Behavior:**
1. Read f0_mode from config.json
2. Map config mode to enforcer mode:
   - `passive` → warn mode
   - `active` → enforce mode
   - `dry-run` → dry-run mode
3. Run constraint check
4. Exit with code: 0 (proceed), 1 (block), 2 (warn)

**Log location:** `forensics/metrics/f0-constraint-log.jsonl`

### `/faerie` Skill Integration
**Skill location:** `.claude/skills/faerie/SKILL.md`

When user invokes `/faerie --f0-mode active`:
1. Skill updates `f0-config.json` with new mode
2. Logs change to mode_history
3. Prints confirmation: "f(0) mode: passive → active"
4. Proceeds with session setup

---

## Recommendations for Phase 1, 2, 3

### Phase 1 (Immediate): Measurement
```
f0_mode = "passive"
Duration: 3-5 sessions
Goal: Establish baseline f(0), understand cost patterns
```

### Phase 2 (Sessions 4-8): Shadow Mode
```
f0_mode = "passive"  (still measuring)
Run context_pressure sigmoid in parallel (don't act on it)
Goal: Validate sigmoid predictions
```

### Phase 3 (Sessions 9-12): Cutover
```
f0_mode = "active"  (enforce constraint)
Duration: 4 sessions
Goal: Validate that enforcement works, measure impact on FFMx/coherence
```

### Phase 4 (Ongoing): Living
```
f0_mode = "passive" or "active" depending on findings
Monthly reassessment: is f(0) target still 0.05? Should it change?
Goal: Continuous improvement via measurement + feedback
```

---

## Troubleshooting

### Mode not changing?
1. Check config file is readable: `cat /mnt/d/0local/gitrepos/faerie2/.claude/f0-config.json`
2. Verify `f0_mode` field exists and is valid (passive|active|dry-run)
3. If using CLI override, pass `--mode` argument explicitly

### Spawns blocked unexpectedly (active mode)?
1. Check constraint log: `tail forensics/metrics/f0-constraint-log.jsonl`
2. Look for "CONSTRAINT_VIOLATED" entries
3. Check presend_estimate vs main_budget
4. Recommendation in log tells you whether to reduce bundle or parallelize

### Want to disable enforcement temporarily?
```bash
/faerie --f0-mode dry-run
# or
/faerie --f0-mode passive
```

Both allow spawns to proceed (mode=active is the only one that blocks).

---

## Config File Reference

**Location:** `/mnt/d/0local/gitrepos/faerie2/.claude/f0-config.json`

**Key fields:**
- `f0_mode`: Current mode (passive|active|dry-run)
- `f0_target`: Target constraint (default 0.05 = 5%)
- `current_settings`: When mode was last changed, why
- `mode_history`: Log of all mode changes (for audit trail)
- `constraint_enforcement_config`: Where hooks are wired

**To change mode:**
1. Edit `f0_mode` field
2. Update `current_settings.reason` to explain why
3. Optionally append to `mode_history` (or let /faerie do it)
4. Save
5. Run `/faerie --f0-sync` to confirm

---

## Quick Reference

| Mode | Behavior | Exit Code | Use Case |
|------|----------|-----------|----------|
| `passive` | Warn, proceed | 0 or 2 | Baseline measurement |
| `active` | Block if violated | 0 or 1 | Constraint enforcement testing |
| `dry-run` | Check, don't act | 2 | Analysis/debugging |

**How to toggle:**
- `/faerie --f0-mode <mode>` (recommended)
- Edit `f0-config.json` + `/faerie --f0-sync` (manual)
- `9x_f0_constraint_enforcer.py --mode <mode>` (direct, one-time)
