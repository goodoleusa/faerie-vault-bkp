# Task-Centric Droplet Architecture

**Adopted:** 2026-04-22  
**Status:** Production  
**TDDR baseline target:** ≥0.80 (Task Dependency Discovery Rate)

---

## Overview

Task-centric droplets are **pre-reasoning insights** that agents emit while working. They enable **stigmergic discovery**: when downstream agents (Task #40) autonomously discover and learn from upstream work (Task #39) without explicit handoffs or messages.

Every droplet is:
- **Task-linked** — discoverable by task ID (canonical anchor)
- **Agent-signed** — HMAC-SHA256 with persistent agent-type keys
- **Immutably audited** — hash-chained COC log in repo forensics
- **Dual-written** — repo canonical + vault mirror (for Obsidian viewing)

---

## Architecture

### Three Core Scripts

| Script | Role | Input | Output |
|--------|------|-------|--------|
| `9x_agent_key_manager.py` | Agent-type signing keys (persistent, evolutionary) | agent_type | key_id, public_key, signatures |
| `9x_task_droplet_writer.py` | Emit + write droplets to repo + vault | category, summary, pri, body | droplet files (4 paths), COC entry |
| `9x_task_droplet_discovery_bootstrap.py` | Discover upstream droplets at agent startup | task_id, upstream_task_ids | formatted markdown for injection |

### File Structure

```
Repository (canonical):
  faerie2/forensics/
    droplets/
      droplet-39.md           ← Task #39 droplet (canonical)
      droplet-40.md           ← Task #40 droplet (canonical)
      data-scientist-a1818e09.md  ← Agent-type secondary (canonical)
      code-reviewer-xyz789abc.md   ← Agent-type secondary (canonical)
      README.md               ← Architecture documentation
    droplet-coc-task-39.jsonl   ← COC log (create + read events)
    droplet-coc-task-40.jsonl   ← COC log (create + read events)

Vault (mirror, Obsidian-viewable):
  CyberOps-UNIFIED/00-SHARED/Droplets/
    droplet-39.md           ← Vault mirror
    droplet-40.md           ← Vault mirror
    data-scientist-a1818e09.md
    code-reviewer-xyz789abc.md

Keys (agent-type persistent identity):
  ~/.claude/keys/agents/
    data-scientist.json     ← Persistent key (evolves across versions, same key_id)
    code-reviewer.json
    workflow-orchestrator.json
    ... (one per agent type)
```

---

## Single Droplet Emission

When an agent emits a droplet, **one emit() call writes to all four locations atomically**:

```python
writer = TaskDropletWriter(
    agent_type="data-scientist",
    task_id="40",
    agent_run_id="ds-run-40-abc123",
    session_id="3b62c9df-ca37-..."
)

sig_event = writer.emit(
    category="HEADLINE",
    summary="Training queue redemption is more valuable than explicit training",
    pri="HIGH",
    body="Failure → queue entry → later beats target → self-update marked as redeemed (production proof)"
)
```

**Writes to:**
1. `/mnt/d/0local/gitrepos/faerie2/forensics/droplets/droplet-40.md` (canonical, repo)
2. `/mnt/d/0local/gitrepos/faerie2/forensics/droplets/data-scientist-a1818e09.md` (canonical, repo)
3. `$CT_VAULT/00-SHARED/Droplets/droplet-40.md` (mirror, vault)
4. `$CT_VAULT/00-SHARED/Droplets/data-scientist-a1818e09.md` (mirror, vault)

**COC logging:**
- Entry appended to `/mnt/d/0local/gitrepos/faerie2/forensics/droplet-coc-task-40.jsonl`
- Includes signature, payload hash, all 4 write destinations

---

## Discovery Path (Task Dependency Flow)

```
Task #40 spawns:
  ├─ STEP 1: Get upstream task IDs from faerie queue
  │   get_blocked_by(task_id=40) → [39]
  │
  ├─ STEP 2: Run discovery bootstrap at startup
  │   9x_task_droplet_discovery_bootstrap.py --task-id 40 --upstream-tasks "39"
  │
  ├─ STEP 3: Search for droplet-39.md
  │   Try: /mnt/d/0local/gitrepos/faerie2/forensics/droplets/droplet-39.md (canonical)
  │   Fallback: $CT_VAULT/00-SHARED/Droplets/droplet-39.md (vault mirror)
  │
  ├─ STEP 4: Parse & extract insights
  │   Read: category, priority, summary, agent_type, signature
  │
  ├─ STEP 5: Format for context injection
  │   Output: Markdown block "## SIBLING DISCOVERIES (Upstream Task Insights)"
  │
  ├─ STEP 6: Inject into agent context BEFORE task work
  │   Agent reads: "Task #39 discovered that training queue redemption is..."
  │
  └─ STEP 7: Agent signs the read event
      agent_key_manager.sign_droplet_read(source=39, discovering=40, ...)
      → COC entry logged to droplet-coc-task-40.jsonl
      → TDDR metric incremented (this agent discovered upstream)
```

---

## Key Continuity & Agent Evolution

Each agent type has **one persistent private key** stored at `~/.claude/keys/agents/{agent_type}.json`:

```json
{
  "key_id": "data-scientist-20260407",      ← Same ID proves evolution
  "agent_type": "data-scientist",
  "private_key": "a1b2c3d4e5f6...",         ← Secret, 256-bit
  "created_at": "2026-04-07T00:00:00Z",
  "versions": [                              ← Track agent versions using this key
    {"version": "1.0", "timestamp": "...", "description": "Initial key"},
    {"version": "1.1", "timestamp": "...", "description": "Bug fix in X"},
    {"version": "2.0", "timestamp": "...", "description": "Major redesign for H-PISTON"}
  ]
}
```

**Key semantics:**
- **Same `key_id` across versions:** Proves continuous agent evolution (v1→v1.1→v2), not a replacement
- **Different `key_id` (new agent):** Indicates fork, reset, or generational change
- **All signatures include `agent_key_id`:** Signature is tied to a specific key generation

---

## Forensic Integrity: Hash Chain

Every droplet event is logged immutably in `droplet-coc-task-{task_id}.jsonl` (append-only):

**Droplet creation (when written):**
```json
{
  "type": "droplet_created",
  "timestamp": "2026-04-22T04:15:00Z",
  "task_id": "40",
  "agent_type": "data-scientist",
  "agent_run_id": "ds-run-40-abc123",
  "agent_key_id": "data-scientist-20260407",
  "droplet_locations": {
    "canonical_task": "/mnt/d/0local/gitrepos/faerie2/forensics/droplets/droplet-40.md",
    "canonical_agent": "/mnt/d/0local/gitrepos/faerie2/forensics/droplets/data-scientist-a1818e09.md",
    "vault_task": "$CT_VAULT/00-SHARED/Droplets/droplet-40.md",
    "vault_agent": "$CT_VAULT/00-SHARED/Droplets/data-scientist-a1818e09.md"
  },
  "category": "HEADLINE",
  "summary": "Training queue redemption is more valuable than explicit training",
  "signature": "a1b2c3d4e5f6g7h8...",
  "payload_hash": "sha256:...",
  "session_id": "3b62c9df-ca37-..."
}
```

**Droplet read (when discovered by downstream task):**
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

**Proof of chain:** Created → Discovered → Used (source_task_id → discovering_task_id → insight_summary, all signed)

---

## Metrics

### TDDR (Task Dependency Discovery Rate)

**Definition:** Fraction of agents that autonomously discover upstream insights.

```
TDDR = (agents_discovering_upstream) / (total_agents_spawned)
Target: ≥0.80
```

**Measured:** At agent startup, `9x_task_droplet_discovery_bootstrap.py` records:
- `discovered_count` (>0 = contributed to TDDR)
- `discovery_latency_ms` (target ≤500ms per task)
- `tddr_contribution` (binary: 1 if discoveries>0, else 0)

**Logged:** `task-discovery-metrics-{SESSION_ID8}.jsonl` (for validation post-session)

---

## Spawn Protocol Integration

Every agent spawn prompt includes:

```markdown
## VAULT OUTPUT LOCATIONS
$VAULT_OUTPUT_FOLDER=/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED/ONBOARDING/2026-04-22-phase-3-eval/

Write all narrative findings to this folder. Use filenames like 01-TOPIC.md, 02-TOPIC.md.

## TASK DROPLET DISCOVERY (Agent Startup)
At startup, BEFORE main task work:

python3 ~/.claude/scripts/9x_task_droplet_discovery_bootstrap.py \
  --task-id "{task_id}" \
  --agent-type {agent_type} \
  --upstream-tasks "$UPSTREAM_TASK_IDS" \
  --inject-to-context

Output: Markdown "## SIBLING DISCOVERIES (Upstream Task Insights)" block.
Action: Prepend to your context, BEFORE reading the main task prompt.
Impact: You inherit upstream patterns; your read-event is signed + logged.
```

---

## Vault Sync

Vault droplets are automatically synced to `faerie2/ObsidianVault` via:
```bash
python3 scripts/9x_sync_obsidian_vault.py --execute
```

**Excluded (investigation-private, never synced):**
- `30-Evidence/`, `10-Investigations/`, `01-PROTECTED/`

**Included (synced):**
- `00-SHARED/Droplets/` (where droplets live)
- `00-SHARED/ONBOARDING/` (where narrative findings live)

Result: Obsidian vault reflects droplet architecture in real-time.

---

## Testing & Validation

**Run integration test:**
```bash
python3 ~/.claude/scripts/9x_droplet_architecture_test.py --mode full
```

**Modes:**
- `full`: All three phases (write, discover, read)
- `write-only`: Agent emits droplet
- `discover-only`: Downstream discovers upstream
- `read-only`: Reads are signed + logged

**Expected output:**
```
✓ Droplet emitted successfully
  Signature: a1b2c3d4e5f6...
  Agent key ID: data-scientist-20260407
  Timestamp: 2026-04-22T04:15:00Z
  ✓ Repo canonical: /mnt/d/0local/.../droplet-39.md
  ✓ Vault mirror: $CT_VAULT/.../droplet-39.md
  ✓ COC log: /mnt/d/0local/.../droplet-coc-task-39.jsonl

✓ Upstream droplets discovered and signed
  Droplets read: 1
  Task #39: Insights: 1
    First insight: Training queue redemption is more valuable...

✓ All tests passed! Droplet architecture is operational.
```

---

## Adoption Checklist (Per Session)

- [ ] Agents spawn with discovery bootstrap in prompt (calls 9x_task_droplet_discovery_bootstrap.py)
- [ ] Agents emit droplets using TaskDropletWriter.emit() (writes to 4 locations)
- [ ] COC logs exist: `/mnt/d/0local/gitrepos/faerie2/forensics/droplet-coc-task-*.jsonl`
- [ ] Vault sync runs: `python3 scripts/9x_sync_obsidian_vault.py` (after session)
- [ ] TDDR metric measured: `discovered_count > 0` recorded for each agent
- [ ] Spawn prompts include VAULT OUTPUT LOCATIONS (daily folder + droplets folder)
- [ ] Test passes: `python3 ~/.claude/scripts/9x_droplet_architecture_test.py --mode full`

---

## FAQ

### Q: Why repo + vault? Why not just vault?
**A:** Repo is git-tracked, immutable, and survives backup/restore. Vault is Obsidian-viewable but subject to sync delays + user edits. Dual-write ensures canonical record (repo) with convenient viewing (vault).

### Q: What if droplet-39.md doesn't exist in repo?
**A:** Fallback searches vault. If not found there either, discovery returns empty (Task #40 gets "None — first in task chain").

### Q: Can agents manually create droplet files?
**A:** No. Use TaskDropletWriter.emit() only. Manual files bypass signing + COC logging, breaking forensic chain.

### Q: How are keys rotated?
**A:** Not yet implemented. Current model: persistent key per agent-type, never expires. Future: add expiration + rotation policy.

### Q: What if an agent_key_id is compromised?
**A:** Create new key with different `key_id` (represents new agent identity). Old signatures remain valid but marked as "legacy key era" in COC. New signatures use new key.

### Q: How is TDDR calculated for a session?
**A:** Sum `tddr_contribution` from `task-discovery-metrics-{SESSION_ID8}.jsonl` (each agent returns binary 1 or 0). Divide by total agents spawned.

---

## Related Files

- **Architecture:** This document
- **Forensics:**  `/mnt/d/0local/gitrepos/faerie2/forensics/droplets/README.md`
- **Integration test:** `~/.claude/scripts/9x_droplet_architecture_test.py`
- **Agent key manager:** `~/.claude/scripts/9x_agent_key_manager.py`
- **Droplet writer:** `~/.claude/scripts/9x_task_droplet_writer.py`
- **Discovery bootstrap:** `~/.claude/scripts/9x_task_droplet_discovery_bootstrap.py`
- **Spawn boilerplate:** `~/.claude/rules/spawn-boilerplate.md` (VAULT OUTPUT LOCATIONS section)
- **Vault sync:** `scripts/9x_sync_obsidian_vault.py`

---

**Next step:** Integrate into Phase 4 agent spawns (SPAWN-BOILERPLATE injection) and validate TDDR baseline.
