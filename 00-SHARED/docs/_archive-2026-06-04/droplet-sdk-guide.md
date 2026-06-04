---
type: reference-guide
status: active
created: 2026-04-22
tags: [droplets, sdk, task-centric, stigmergy]
parent: 00-SHARED
doc_hash: pending
hash_ts: pending
hash_method: body-sha256-v1
---

# TaskDropletWriter SDK Guide — Complete Reference

> [↑ 00-SHARED](../) · [→ Droplets](./Droplets/)

## What Are Droplets?

**Droplets are pre-reasoning insights** — the moment inspiration strikes, before your brain filters it through logic. They're meant to **cross-pollinate across agents and tasks**.

Examples of droplet moments:
- You notice connection between two unrelated domains
- An assumption just flipped ("Wait, I had this backwards...")
- A technique just worked and you can't fully explain why yet
- A gut feeling says something is wrong/right but you don't know why
- Context is about to auto-compact and a thought will evaporate

The signal is: **hesitation, surprise, or excitement**. Write that raw moment.

---

## Why Use the SDK (Not Manual Files)?

Droplets require cryptographic attribution + audit trail:

| Requirement | Manual File | TaskDropletWriter SDK |
|---|---|---|
| **Agent-type persistent key** | Must manage yourself (error-prone) | Automatic (one key per agent type) |
| **HMAC-SHA256 signature** | Not captured | Signed at creation + read time |
| **COC logging** | Not tracked | Appended to `droplet-coc-task-*.jsonl` (immutable) |
| **Dual-write (repo + vault)** | Must do manually (sync issues) | Atomic, single emit() call |
| **Attribution** | Unclear who wrote it | agent_key_id + timestamp + session |
| **Forensic chain** | Broken | Unbroken: creation → discovery → usage |

**Manual droplets = forensic liability.** Use the SDK.

---

## Installation & Import

The TaskDropletWriter is part of the faerie infrastructure (pre-installed).

```python
from task_droplet_writer import TaskDropletWriter
```

If import fails:
```bash
python3 ~/.claude/scripts/9x_task_droplet_writer.py --help
# (Verify script exists and is executable)
```

---

## Basic Usage (Minimal)

```python
from task_droplet_writer import TaskDropletWriter

# Initialize (called once per agent run)
writer = TaskDropletWriter(
    agent_type="data-scientist",           # Your agent type
    task_id="40",                          # Injected at spawn (from $TASK_ID env var)
    agent_run_id="ds-run-40-abc123",       # From AGENT-RUN-ID section of spawn boilerplate
    session_id="3b62c9df-ca37-..."         # From $CLAUDE_SESSION_ID env var
)

# Emit a droplet (call multiple times per session, up to 5 times ideal)
sig = writer.emit(
    category="HEADLINE",
    summary="Training queue redemption is more valuable than explicit training",
    pri="HIGH"
)

print(f"✓ Droplet emitted: {sig['signature'][:32]}...")
```

**Output files (written automatically):**
- Canonical (repo): `/mnt/d/0local/gitrepos/faerie2/forensics/droplets/droplet-40_data-scientist-a1818e09_2026-04-22_3b62c9df.md`
- Secondary (repo): `/mnt/d/0local/gitrepos/faerie2/forensics/droplets/data-scientist-a1818e09_2026-04-22_3b62c9df.md`
- Vault mirror: `$CT_VAULT/00-SHARED/Droplets/droplet-40_data-scientist-a1818e09_2026-04-22_3b62c9df.md`
- COC audit: `/mnt/d/0local/gitrepos/faerie2/forensics/droplet-coc-task-40.jsonl` (append)

---

## Full Constructor

```python
writer = TaskDropletWriter(
    agent_type: str,                    # Required: "data-scientist", "code-reviewer", etc.
    task_id: str,                       # Required: task ID (e.g., "40")
    agent_run_id: str,                  # Required: from AGENT-RUN-ID section above
    session_id: str,                    # Required: $CLAUDE_SESSION_ID env var
    vault_root: Optional[str] = None,   # Optional: $CT_VAULT root (auto-detected if None)
    repo_root: Optional[str] = None     # Optional: repo root (auto-detected if None)
)
```

---

## emit() — Full Signature

```python
sig_event = writer.emit(
    category: str,                      # Required: category (see types below)
    summary: str,                       # Required: 1-sentence insight (unfiltered)
    pri: str = "MED",                   # Optional: priority (HIGH, MED, LOW)
    body: Optional[str] = None          # Optional: additional context (2-5 sentences)
)
```

**Returns:** Signature event (dict) with fields:
```python
{
    "event": "droplet_create",
    "task_id": "40",
    "agent_type": "data-scientist",
    "agent_key_id": "data-scientist-20260407",
    "agent_public_key": "a1b2c3d4e5f6...",
    "category": "HEADLINE",
    "summary": "...",
    "timestamp": "2026-04-22T04:15:00Z",
    "signature": "a1b2c3d4e5f6g7h8i9j0k1l2...",
    "payload_hash": "sha256:..."
}
```

---

## Categories (Types of Droplets)

### High-Value Types (Prioritize Writing)

| Category | When to use | Example |
|---|---|---|
| **HEADLINE** | "Whoa, I had this backwards" / surprising finding | "Training queue redemption is more valuable than explicit training because it proves improvement works in production" |
| **CONNECTION** | Two unrelated ideas suddenly link | "Context debt + spawn boilerplate timing + training-queue all need the same 'canonical binding moment' fix" |
| **FIRST_IMPRESSION** | Gut feeling before reasoning | "Something about this feels backwards but I don't know why yet" |
| **TECHNIQUE** | Pattern that just worked | "Index-first reads cut context by 98%. Pointer search → read those files → analyze." |

### Supporting Types

| Category | When to use | Example |
|---|---|---|
| **OBSERVATION** | Something noticed, may be relevant later | "Training queue has been dark 36 days" |
| **HYPOTHESIS** | Untested theory | "Batch spawn might scale better than sequential" |
| **IDEA** | Improvement thought | "Could we use the training queue pattern for droplet routing?" |

---

## Priority Levels

```python
pri="HIGH"   # Anomaly, critical pattern, blocking issue (promote immediately)
pri="MED"    # Standard droplet (most cases)
pri="LOW"    # Nice-to-know, contextual
```

---

## Example: Writing Multiple Droplets

```python
writer = TaskDropletWriter(
    agent_type="evidence-curator",
    task_id="45",
    agent_run_id="ec-run-45-xyz",
    session_id="3b62c9df-ca37-..."
)

# Droplet 1: Connection
writer.emit(
    category="CONNECTION",
    summary="Gap analysis + tier-1 cutoff both need per-item confidence scoring (same pattern)",
    pri="MED"
)

# Droplet 2: Technique
writer.emit(
    category="TECHNIQUE",
    summary="Metadata-first search cuts files scanned by 95%. Search {name, type, source} then read only matching files.",
    pri="MED"
)

# Droplet 3: First Impression (pre-reasoning)
writer.emit(
    category="FIRST_IMPRESSION",
    summary="Intuition says tier-2 threshold is too low but I haven't run stats yet",
    pri="LOW"
)

# Droplet 4: Headline (surprising finding)
writer.emit(
    category="HEADLINE",
    summary="Only 1 of 15 smoking-gun items survived peer review. Confidence gap is real.",
    pri="HIGH",
    body="Need to revisit tier-1 definition. Quality > quantity."
)
```

**Ideal range:** 2-5 droplets per agent run (minimum 1, mandatory).

---

## Droplet Format (On Disk)

What the SDK writes to disk:

```markdown
### 2026-04-22T04:15:00Z — data-scientist
**cat:** HEADLINE | **pri:** HIGH
**task_id:** 40 | **agent_type:** data-scientist | **agent_run_id:** ds-run-40-abc123
**signature:** a1b2c3d4e5f6... (see COC for full)

Training queue redemption is more valuable than explicit training because it 
proves improvement works in production.

**Body:** Failure → queue entry → later beats target → self-update marked as 
redeemed_on_the_job → logged as redemption (more valuable than explicit training 
because it's real-work validated).

**coc_entry:** droplet-coc-task-40.jsonl

---
```

---

## Filename Convention (Durable, Cross-Location)

**Pattern (identical in repo + vault):**
```
droplet-{task_id}_{agent_type}-{agent_id}_{YYYY-MM-DD}_{session_id8}.md
```

**Example:**
```
droplet-40_data-scientist-a1818e09_2026-04-22_3b62c9df.md
```

**Breakdown:**
- `droplet-40` — Task ID (primary searchable key for stigmergy)
- `_data-scientist-a1818e09` — Agent type + first 8 chars of session ID (who wrote it)
- `_2026-04-22` — Date (timeline tracking)
- `_3b62c9df` — Session ID first 8 chars (session context)

**Why this pattern?**
- Task ID first: makes task-dependency discovery via grep trivial (`grep -r "droplet-40"`)
- All IDs included: attribution is complete (agent type, session, date)
- Identical everywhere: repo canonical + vault mirror use same filename (no sync confusion)
- Extensible: can add domain prefix later if multi-investigation growth demands it

---

## Locations (Dual-Write, Atomic)

**One emit() call writes to four paths (identical filename pattern everywhere):**

### Canonical (System of Record, git-tracked)
```
/mnt/d/0local/gitrepos/faerie2/forensics/droplets/
  droplet-40_data-scientist-a1818e09_2026-04-22_3b62c9df.md          (task-linked)
  data-scientist-a1818e09_2026-04-22_3b62c9df.md                     (agent-linked)
```

### Vault Mirror (Obsidian-viewable, synced)
```
$CT_VAULT/00-SHARED/Droplets/
  droplet-40_data-scientist-a1818e09_2026-04-22_3b62c9df.md          (task-linked)
  data-scientist-a1818e09_2026-04-22_3b62c9df.md                     (agent-linked)
```

### COC Audit Log (Immutable, repo forensics)
```
/mnt/d/0local/gitrepos/faerie2/forensics/
  droplet-coc-task-40.jsonl                                          (append-only)
```

**All four paths written atomically** in a single `emit()` call. If any path fails, exception is raised (no partial writes).

---

## COC Entries (Audit Trail)

**At creation (droplet_created event):**
```json
{
  "type": "droplet_created",
  "timestamp": "2026-04-22T04:15:00Z",
  "task_id": "40",
  "agent_type": "data-scientist",
  "agent_run_id": "ds-run-40-abc123",
  "agent_key_id": "data-scientist-20260407",
  "droplet_locations": {
    "canonical_task": "/mnt/d/0local/.../droplet-40_data-scientist-a1818e09_2026-04-22_3b62c9df.md",
    "canonical_agent": "/mnt/d/0local/.../data-scientist-a1818e09_2026-04-22_3b62c9df.md",
    "vault_task": "$CT_VAULT/.../droplet-40_data-scientist-a1818e09_2026-04-22_3b62c9df.md",
    "vault_agent": "$CT_VAULT/.../data-scientist-a1818e09_2026-04-22_3b62c9df.md"
  },
  "category": "HEADLINE",
  "summary": "Training queue redemption is more valuable...",
  "signature": "a1b2c3d4e5f6...",
  "payload_hash": "sha256:...",
  "session_id": "3b62c9df-ca37-..."
}
```

**At discovery/read (droplet_read event):**
```json
{
  "type": "droplet_read",
  "timestamp": "2026-04-22T04:22:00Z",
  "source_task_id": "40",
  "discovering_task_id": "41",
  "discovering_agent_type": "code-reviewer",
  "discovering_agent_run_id": "cr-run-41-xyz789",
  "discovering_key_id": "code-reviewer-20260407",
  "signature": "x9y8z7w6v5u4...",
  "payload_hash": "sha256:...",
  "insight_summary": "Training queue redemption is more valuable..."
}
```

**Proof of chain:** creation → discovery → usage, all signed + timestamped.

---

## Agent Key Manager (Persistent Identity)

Each agent type has **one persistent private key**:

```
~/.claude/keys/agents/
  data-scientist.json
  code-reviewer.json
  workflow-orchestrator.json
  ... (one per agent type)
```

**Key contents:**
```json
{
  "key_id": "data-scientist-20260407",
  "agent_type": "data-scientist",
  "private_key": "a1b2c3d4e5f6...",  (256-bit, secret)
  "created_at": "2026-04-07T00:00:00Z",
  "versions": [
    {"version": "1.0", "timestamp": "...", "description": "Initial key"},
    {"version": "1.1", "timestamp": "...", "description": "Bug fix in X"},
    {"version": "2.0", "timestamp": "...", "description": "Major redesign for H-PISTON"}
  ]
}
```

**Key semantics:**
- **Same `key_id` across versions:** Proves agent evolution (v1→v1.1→v2), not a replacement
- **Different `key_id`:** Indicates new agent identity (fork, reset, generational change)
- **All signatures include `agent_key_id`:** Tied to specific key generation for audit trail

---

## Testing Your Droplets

Run integration test:
```bash
python3 ~/.claude/scripts/9x_droplet_architecture_test.py --mode full
```

Expected output:
```
✓ Droplet emitted successfully
  Signature: a1b2c3d4e5f6...
  Agent key ID: data-scientist-20260407
  Timestamp: 2026-04-22T04:15:00Z
  ✓ Repo canonical: /mnt/d/0local/.../droplet-40_data-scientist-a1818e09_2026-04-22_3b62c9df.md
  ✓ Vault mirror: $CT_VAULT/.../droplet-40_data-scientist-a1818e09_2026-04-22_3b62c9df.md
  ✓ COC log: /mnt/d/0local/.../droplet-coc-task-40.jsonl

✓ Upstream droplets discovered and signed
  Droplets read: 1
  Task #40 → Task #39: Insights: 1
    First insight: Training queue redemption is more valuable...

✓ All tests passed! Droplet architecture is operational.
```

---

## Common Patterns

### Pattern 1: Droplet Immediately When Thought Forms

```python
# (In your main work loop)
writer = TaskDropletWriter(...)

# Middle of analysis, idea hits
writer.emit(
    category="IDEA",
    summary="Could tier-1 cutoff use Bayesian credibility intervals instead of threshold?",
    pri="LOW"
)

# Continue work (droplet already captured, won't evaporate)
```

### Pattern 2: Pre-Compress Emergency Capture

```python
# (Context ~90% full, about to hit auto-compact)
# Capture raw insights before context crush

writer.emit(
    category="HEADLINE",
    summary="Silent failure pattern: 3 agents completed but no manifest",
    pri="HIGH"
)

writer.emit(
    category="FIRST_IMPRESSION",
    summary="Spawn boilerplate timing feels backwards (agent discovers better path during work, not at spawn)",
    pri="MED"
)

# Auto-compact fires; insights are already persisted
```

### Pattern 3: End-of-Run Synthesis (Post-Work Reflection)

```python
# (Main work complete, time to reflect)

# What worked?
writer.emit(
    category="TECHNIQUE",
    summary="Metadata-first indexing reduced file scans by 95%",
    pri="HIGH"
)

# What was harder than expected?
writer.emit(
    category="OBSERVATION",
    summary="Peer review rejected 87% of findings; confidence definition needs review",
    pri="MED"
)

# What assumption flipped?
writer.emit(
    category="HEADLINE",
    summary="Low sample size (N=15) is acceptable if quality score is >4.0 and signed by 2+ agents",
    pri="HIGH"
)
```

---

## Error Handling

If emit() fails (file write, signing error, etc.):

```python
try:
    writer.emit(category="HEADLINE", summary="...", pri="HIGH")
except Exception as e:
    print(f"WARNING: Droplet write failed: {e}")
    # Log to pollen as fallback
    print("<!-- MEM cat=DROPLET pri=HIGH -->")
    print("Droplet (write failed): ...")
    print("<!-- /MEM -->")
```

**Fallback:** If vault unreachable, droplets can be appended to pollen-{SESSION_ID}.md as MEM blocks. Memory-keeper promotes to NECTAR at /handoff (less durable than SDK, but safe fallback).

---

## Next: Upstream Discovery

Once you emit droplets, downstream tasks discover them via:
```bash
python3 ~/.claude/scripts/9x_task_droplet_discovery_bootstrap.py \
  --task-id 41 \
  --agent-type code-reviewer \
  --upstream-tasks "40" \
  --inject-to-context
```

This discovers your droplet-40_* file, parses it, signs the read event, and injects "## SIBLING DISCOVERIES" into downstream agent context.

See: `docs/task-droplet-architecture.md` (discovery path section)

---

**Status:** SDK production-ready  
**Metrics:** TDDR (Task Dependency Discovery Rate), signature coverage, discovery latency  
**Next:** Integrate into Phase 4 agent spawns for full stigmergic loop
