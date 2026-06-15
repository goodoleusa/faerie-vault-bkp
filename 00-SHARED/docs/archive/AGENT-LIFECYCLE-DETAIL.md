# Agent Lifecycle — Detailed Protocols

Full specifications for task state management, failure handling, and self-update procedures.
Short rule version: `~/.claude/rules/agent-lifecycle.md`

---

## Task State and Progressive Disclosure

Each agent maintains a **versioned state** per task. This enables two things:
1. **Progressive analysis**: agent deepens findings across multiple passes without anchoring on earlier conclusions
2. **Forensic separability**: proves that OTJ learning events happened AFTER earlier findings were formed

### Task State File

Location: `~/.claude/hooks/state/task-states/{task_id}-{agent_type}.json`

Schema:
```json
{
  "task_id": "{id}",
  "agent": "{type}",
  "agent_version": "{YYYY-MM-DD}_{score}",
  "states": [
    {
      "v": 1,
      "ts": "{ISO}",
      "data_seen": "partial (phase 1 summary only)",
      "assumptions": {"H1": 0.70, "H2": 0.30},
      "findings": ["finding A", "finding B"],
      "open_questions": ["Q1", "Q2"]
    },
    {
      "v": 2,
      "ts": "{ISO}",
      "data_seen": "full dataset",
      "assumptions": {"H1": 0.85, "H2": 0.15},
      "findings": ["finding A (confirmed)", "finding C (new)"],
      "delta_from_prev": {
        "assumptions_updated": "H1 +0.15 — new cert evidence; H2 -0.15",
        "findings_added": ["finding C"],
        "findings_removed": [],
        "open_questions_resolved": ["Q1 — resolved by cert data"]
      }
    }
  ]
}
```

### Progressive Disclosure Protocol

```
Phase 1 (seed): Agent sees summary/sample only → write V1 state with prior assumptions
Phase 2 (deepen): Agent sees full data → read V1 state → update to V2 → record delta
Phase N (revisit): Each revisit adds a new state version, never overwrites old ones
```

**Rules:**
- ALWAYS read prior state before starting work on a task you've touched before
- Never modify past state versions — append only
- If revisiting a task after an OTJ training event: note `agent_version` changed between V1 and V2 in the delta — this is the forensic proof that the improvement happened between analysis passes, not retroactively

### OTJ Training Measured on State Deltas

When training-log records an improvement, it compares:
- Did the agent correctly update assumptions when new evidence was presented? (calibration)
- Did it avoid anchoring on V1 priors despite contradicting V2 evidence? (independence)
- Did it find new findings in V2 that V1 missed? (recall improvement)

This is forensically clean: the agent's capability is measured on HOW it updates, not WHAT it concludes. A court can show:
> "The agent formed prior assumptions at T1 (V1 state). New data was introduced at T2. The agent updated its assumptions at T3 > T2. OTJ training event occurred at T4 > T3. The finding was concluded at T5 > T4. Each step is timestamped and COC-logged — the training event is downstream of the finding."

---

## Task Failure Protocol (MANDATORY — before calling queue_ops.py fail)

When you cannot complete a task and must pass it to the next agent, your final job is to
**maximize the value of the context bundle** for whoever picks it up. Do NOT just call fail and exit.

### Steps before calling fail

1. **Write a FAILURE HANDOFF block** to `{repo}/.claude/memory/scratch-{SESSION_ID}.md`:
   ```
   <!-- MEM agent={your-type} ts={ISO} session={SESSION_ID} cat=HANDOFF pri=HIGH -->
   **[HANDOFF — task failed]** {task_id}: {one-line reason}

   What I tried:
   - {approach 1} → {what happened / why it didn't work}
   - {approach 2} → {what happened}

   DO NOT try again:
   - {specific thing that was a dead end} — {why it won't work}

   High-value leads NOT yet tried (next agent should start here):
   - {lead 1} — {why it's promising}
   - {lead 2} — {why it's promising}

   Data that WAS found (even if task incomplete):
   - {partial finding 1}
   - {partial finding 2}

   Recommended next agent: {subagent_type} — {one line why}
   <!-- /MEM -->
   ```

2. **Call fail with --reason and --agent-hint** (the --reason becomes the retry context prefix):
   ```bash
   python3 ~/.claude/hooks/state/queue_ops.py fail TASK_ID \
     --reason "Tried WHOIS + Shodan; 45.38.46.0/24 not in ARIN — try RIPE or Hurricane Electric BGP" \
     --agent "research-analyst"
   ```
   The failure reason appears at the top of the retry task's context bundle so the next agent
   sees immediately what was tried without re-reading your full scratch file.

3. **The retry context bundle is built automatically** from:
   - Your failure reason (prepended by queue_ops.py fail)
   - The original task's context_bundle (carried forward verbatim)
   The next agent gets both — they know what you tried AND the full original context.

### For HIGH priority tasks

Also append your FAILURE HANDOFF block directly into the
retry task's context_bundle via the --context-bundle flag on fail (override the auto-build):
```bash
HANDOFF=$(cat {repo}/.claude/memory/scratch-{SESSION_ID}.md | grep -A 50 "HANDOFF")
python3 ~/.claude/hooks/state/queue_ops.py fail TASK_ID \
  --reason "..." \
  --context-bundle "$HANDOFF"
```

---

## Self-Update Protocol (beat-last-score)

When your run completes and performance-eval or the orchestrator determines you
**beat your last score** on the primary KPI for your task type:

### IF beat_last_score AND improvement is durable

1. Read your own `~/.claude/agents/{your-type}.md`
2. Find or create "## Last Training" section at the end
3. Append what you learned that caused the improvement:
   - Specific technique or ordering that worked better
   - Constraint that improved output (e.g., "cite max 3 sources → higher precision")
   - Failure mode you avoided that hurt last time
4. Keep it to 3-5 bullets max — crystallize, don't accumulate
5. Update the date
6. Append version-bump entry to investigation COC (if active investigation):
   Append this JSON line to `~/.claude/memory/investigations/{inv_id}/forensics/master-coc.jsonl`:
   ```json
   {
     "type": "agent_version_bump",
     "agent": "{your-type}",
     "new_score": {score},
     "prev_score": {prev_score},
     "new_version": "{YYYY-MM-DD}",
     "prev_version": "{prev_date or 'baseline'}",
     "learning_type": "{otj|autotune|mini_learning}",
     "task": "{one-line: what you were doing when the improvement happened}",
     "ts": "{ISO-8601}",
     "entry_hash": "{SHA256 of this entry's canonical fields}",
     "prev_entry_hash": "{hash of previous master-coc entry, or 'genesis'}"
   }
   ```

   **FORENSIC PURPOSE:** This timestamped entry lets an expert witness prove that:
   - Finding F was produced at T1 by agent version V1 (score S1)
   - Capability improvement occurred at T2 where T2 > T1
   - Therefore: the improvement could NOT have biased finding F
   The COC hash chain makes this timeline immutable and court-admissible.
   coc-manager can generate an affidavit from this log on demand.

### IF did NOT beat last score

1. Do NOT update agent.md — only improvements get written there
2. APPEND to training-queue.json (bottom of queue, priority LOW):
   ```json
   {
     "agent": "{your-type}",
     "status": "queued",
     "source": "auto-requeue",
     "kpi_missed": "{which KPI fell short}",
     "score": {score},
     "target": {prev_score},
     "gap": {prev_score - score},
     "hypothesis": "{1-2 sentences: why performance was worse this time}",
     "suggested_training": [
       "{specific constraint or drill that targets the weakness}",
       "{alternative approach to try}"
     ],
     "on_the_job_eligible": true,
     "created": "{ISO date}"
   }
   ```
3. Set on_the_job_eligible=true — this means the agent can redeem itself
   during a REAL work session instead of needing a separate /autotune run.
   If during any future work session (with mini-learning enabled) the agent
   beats the previous score, it self-updates AND logs the redemption.

### On-the-job redemption (how failure becomes success without explicit training)

When an agent has a pending training-queue entry with `on_the_job_eligible: true`
and then beats the target score during a real work session:

1. Self-update agent.md (same as beat-last-score protocol above)
2. Update training-queue.json: set status="redeemed_on_the_job"
3. Append a REDEMPTION entry to `~/.claude/hooks/state/training-log.jsonl`:
   ```json
   {
     "type": "redemption",
     "agent": "{type}",
     "original_failure": "{kpi_missed} at {score}",
     "redemption_score": {new_score},
     "context": "on_the_job",
     "task": "{what the agent was actually doing when it improved}",
     "path_to_success": "{1-2 sentences: what changed between failure and success}",
     "ts": "{ISO date}"
   }
   ```
4. Write a `<!-- MEM cat=IDEA pri=MED -->` to scratch:
   "Agent {type} redeemed on-the-job: {kpi} went from {fail_score} to {new_score}.
    Key change: {what was different}. Consider promoting this to agent.md."

The redemption path is more valuable than explicit training because it proves the
improvement works in real conditions, not just constrained drills. Faerie surfaces
redemption entries in the performance brief so the user sees the arc from failure
to success.

### agent.md format (beat-last only)

```markdown
## Last Training — {YYYY-MM-DD}

Score: {score} (prev: {prev_score}, delta: +{delta})
Task: {one-line task description}
Context: {training | on_the_job_redemption}

Learnings:
- {what specifically improved performance}
- {technique or pattern to repeat}
- {failure mode to avoid}
```
