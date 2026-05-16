# faerie-magic Cheatsheet — Quick Reference

> **TL;DR:**
> - `/faerie` = session start (always first). `/handoff` = session end.
> - `/run` = claim and execute next queued task. `/queue` = show queue.
> - Key agents: `memory-keeper` (end-of-session), `data-engineer` (ETL), `evidence-curator` (tiering).
> - Status footer format: `[{stage} T{N} | {alert} | ctx ~{K}K | cache HIT/MISS | ${cost}/turn | headroom:{H}K]`


## Session Lifecycle Commands

| Command | When | What it does |
|---------|------|-------------|
| `/faerie` | Session start (always) | Roundup + learn + fill template + queue or /new |
| `/new` | Start a sprint | Reads queue, spawns team, launches session |
| `/new [paste template]` | Start from filled template | Skips queue, parses template directly |
| `/handoff` | Mid-session context save | Bundles context for next session without ending |
| `/done` | Sprint complete | Memory-keeper + queue update + HONEY/NECTAR sync |
| `/sprint` | Queue management | View/add/reorder sprint queue |
| `/roster` | View agents | Who's running, what they own |
| `/collab` | Multi-agent coordination | Sync state across concurrent sessions |
| `/swap` | Replace session lead | Hand off orchestration mid-session |

---

## Queue Operations (queue_ops.py)

```bash
# Add a task (minimal)
python hooks/state/queue_ops.py add \
  --goal "Verify B2 backup integrity" \
  --priority HIGH

# Add a task (rich — recommended)
python hooks/state/queue_ops.py add \
  --goal "Verify B2 backup integrity" \
  --priority HIGH \
  --project cybertemplate \
  --source security-auditor

# Claim next available task
python hooks/state/queue_ops.py claim --session $SESSION_ID

# Claim up to 3 tasks from same project (depth mode — default)
python hooks/state/queue_ops.py claim --session $SESSION_ID --mode depth --max 3

# Claim highest-priority across all projects (breadth mode)
python hooks/state/queue_ops.py claim --session $SESSION_ID --mode breadth

# Mark complete
python hooks/state/queue_ops.py complete sprint-20260315-014

# Mark failed (triggers re-queue with enriched context)
python hooks/state/queue_ops.py fail sprint-20260315-014

# List queue
python hooks/state/queue_ops.py list
```

### Rich queue entry fields

```json
{
  "id": "sprint-YYYYMMDD-NNN",
  "priority": "HIGH | MED | LOW",
  "task_type": "session_sprint | data_ingest | launch_phase | generic",
  "goal_one_line": "One sentence: what to do",
  "hypothesis": "What we believe is true that this task will test",
  "seeking": "What evidence would confirm or refute the hypothesis",
  "why_now": "Why this is the right next task",
  "recommended_agent": "agent-type-name",
  "success_path": "What to do when the task succeeds",
  "failure_path": "What to do when the task fails",
  "project": "repo-name",
  "on_the_job_eligible": true,
  "filled_template_path": "~/.claude/hooks/state/sprint-queue/sprint-NNN.md"
}
```

---

## Agent Failure Protocol

**Before calling `fail` on a task, the agent MUST write:**

```markdown
<!-- MEM agent=X ts=ISO8601 session=Y cat=HANDOFF pri=HIGH -->
**[HANDOFF]** Task sprint-NNN failed — B2 hash verify incomplete

What was attempted: Ran hash_guardian.py against 4,410 files. Completed 2,847 before timeout.
Why it failed: 10-minute timeout on WSL — large file set needs chunked approach.
Partial work salvageable: hash_manifest_partial_RUN014.json covers files A-L (alphabetical).
What next attempt should do: Start from M onward; use --chunk flag with --resume hash_manifest_partial_RUN014.json.
Key files: forensic/hash_manifest_partial_RUN014.json, forensic/forensic-script-log.md (FSL-014 open)

Files: forensic/hash_manifest_partial_RUN014.json
Next: Re-queue with --resume flag; spawn security-auditor with chunked approach
<!-- /MEM -->
```

Then update the queue entry's `hypothesis` with what was learned, and set `on_the_job_eligible: true`.

---

## Memory Write Routing

| What you observed | Where it goes |
|-------------------|---------------|
| Working note, in-progress observation | `{repo}/.claude/memory/scratch-{SESSION_ID}.md` |
| HIGH priority flag needing human review | Also → `~/.claude/memory/REVIEW-INBOX.md` |
| Durable project fact | Faerie crystallizes → `{repo}/.claude/memory/HONEY.md` |
| Cross-project preference or machine fact | Faerie crystallizes → `~/.claude/memory/HONEY.md` |
| Validated finding | Memory-keeper promotes → `~/.claude/memory/KNOWLEDGE-BASE.md` |
| Cross-session connection | Tag `cat=CONNECTION` — auto-promoted to global REVIEW-INBOX |

### Memory entry format

```
<!-- MEM agent={name} ts={ISO8601} session={id} cat={CATEGORY} pri={PRIORITY} -->
**[{CATEGORY}]** {one-line summary under 100 chars}

{2-10 lines of context, evidence, file references}

Files: {comma-separated paths, or "none"}
Next: {recommended action, or "none"}
<!-- /MEM -->
```

**Categories:** `OBSERVATION` `FLAG` `IDEA` `PAIN` `DECISION` `HANDOFF` `HEADLINE` `CONNECTION` `THREAD`

**Priorities:** `HIGH` `MED` `LOW`

`HEADLINE`, `CONNECTION`, `THREAD` auto-promote to REVIEW-INBOX at session end.

---

## Hypothesis Tracking Fields

Every hypothesis-bearing task should carry these fields (in queue entry or session template):

| Field | Purpose | Example |
|-------|---------|---------|
| `hypothesis` | What we believe | "Some files were silently modified during the overwrite incident" |
| `seeking` | Evidence that confirms or refutes | "Hash mismatches between genesis manifest and current files" |
| `smoking_gun` | Specific artifact that would prove it | "A file whose sha256 differs from hash_manifest_genesis_RUN004.json" |
| `why_now` | Why test this hypothesis now | "Genesis manifest just recovered from git; window to verify is open" |
| `confidence` | Bayesian estimate (0.0–1.0) | `0.3` (prior to testing) |
| `confirmed_by` | Evidence that confirmed it | "FSL-014: 3 hash mismatches found in evidence set F-G" |
| `refuted_by` | Evidence that refuted it | `null` |
| `follow_up` | Next question if confirmed | "Identify when the modification occurred and by what process" |

---

## Agent Self-Update Protocol

Agents update their own `.md` file only when they **beat their previous score** on the primary KPI:

```markdown
## Last Training — YYYY-MM-DD

Score: 0.91 (prev: 0.84, delta: +0.07)
Task: evidence tiering — 4,410 files, 3 tiers
Context: on_the_job_redemption

Learnings:
- Cite tier decisions with specific hash + timestamp, not just filename
- Run consistency check before finalizing: any tier-1 without a FSL entry is an error
- 3-pass approach (scan → draft → verify) outperforms 1-pass scoring
```

If the agent did NOT beat its score: append to `hooks/state/training-queue.json` with `on_the_job_eligible: true`. Do not update the agent file.

---

## Three-File Memory Hierarchy

```
~/.claude/memory/HONEY.md        ← Crystallized wisdom (cross-project, ≤200 lines)
{repo}/.claude/memory/HONEY.md   ← Project crystallized facts
~/.claude/memory/REVIEW-INBOX.md ← Human review queue
~/.claude/memory/KNOWLEDGE-BASE.md ← Validated findings
{repo}/.claude/memory/scratch-{SESSION_ID}.md ← Working notes (session-scoped)
```

**Rule:** Never write project state to global HONEY.md. Never write cross-project preferences to project HONEY.md. Never write investigation data to the auto-memory folder (`.claude/projects/*/memory/` — that's an index, not a store).

---

## Token Budget Quick Reference

| Session turn | Stage | Action |
|-------------|-------|--------|
| T1 | Spawn | Spawn all specialists NOW — they get fresh 200K windows |
| T2–7 | Orbit | Agents working; parent session stays lean |
| T8–10 | Consolidate | Integrate agent returns |
| T11–13 | Commit | `git add -A && git commit && git push` |
| T14+ | Descent | Auto-compact fires automatically — keep working |

**Model routing:**
- Bulk/classification: **Haiku** ($1/1M — 3× cheaper)
- Code/review/agents: **Sonnet** (default)
- Architecture/security: **Opus** (only when depth matters)

**Footer format (every response):**
```
[ctx ~NK/200K | cache HIT ✓ | turn N | ~$X this turn | saved ~$X | session ~$X]
```
