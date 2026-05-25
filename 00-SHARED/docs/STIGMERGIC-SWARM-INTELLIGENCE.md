# Stigmergic Swarm Intelligence — Faerie2 Coordination Substrate

**Status:** documentation reference | **Tier:** 30-memory | **Cites:** sys00033 (task_id join), sys00031 (stigmergy-only), mth00074 (rocket physics), CLAUDE.md principles | **Supersedes:** none | **Last updated:** 2026-04-24

---

## Executive Summary

Faerie2 coordinates parallel agent work without SendMessage or centralized synchronization. Instead, agents cooperate through **stigmergy** — indirect coordination via persistent filesystem state that any downstream agent can query at zero context cost. This document explains the substrate, mechanisms, and design intent.

**Core insight:** filesystem becomes the API; agents coordinate by reading and writing task state in a queryable, hash-chained form. No back-channel messaging. No polling. No orchestration ceremony in the main session.

---

## What Is Stigmergy?

Stigmergy is a coordination mechanism observed in insect colonies (ants, termites) where individuals modify their shared environment and respond to those modifications without direct communication. A pheromone trail is a chemical signal left in the environment; ants follow it, deposit their own pheromone, reinforce the trail. Termites build pillars by sensing (not communicating) what sibling termites built; each adds a brick on top of sensed structure. No instruction, no messenger, no foreman.

**Applied to agents:**
- Agents write **persistent task state** (manifest files, droplets, queue claims)
- Downstream agents **read that state** without asking ("what did your predecessor find?")
- The filesystem IS the shared environment; paths encode meaning

**Why this matters for f(0):**
- **Zero message-send overhead** — no `SendMessage` RPC, no queue depth, no back-channel congestion
- **Zero coordination latency** — agents act immediately on written state, not after waiting for a reply
- **Zero context burn in main** — orchestration is implicit in the filename/path structure, not an async puzzle main must solve
- **Scalability to arbitrary N** — one thousand agents with independent read/write zones don't require one thousand callback handlers in main

---

## Core Stigmergic Primitives in Faerie2

### 1. Task_ID as Universal Join Key (sys00033)

Every artifact names its task via filename pattern:
```
{timestamp}_{product-type}_{task_id}_{agent_signature}_{session_id8}.{ext}
```

**New agent spawning for task_id=306b runs:**
```bash
grep -r "_306b_" forensics/
```

**Result:** discovers all predecessor work — droplets, manifests, COC entries, vault outputs, agent-runs — instantly, with zero context cost. Filesystem becomes a queryable index.

**Why it works:**
- Task_id is deterministic (assigned by queue)
- Filename is immutable (forensic artifact)
- Grep is filesystem-native (no API, no authentication, no latency)
- Zero Claude inference needed

### 2. Manifest Status Progression (in-progress → draft → final)

Agents write manifests with evolving status:

```json
{
  "task_id": "306b",
  "status": "in-progress",
  "checkpoint_name": "started",
  "progress_pct": 0,
  "ts": "2026-04-24T00:15:30Z",
  "agent_run_id": "ae2e1d4f..."
}
```

Later, same manifest, status=draft:
```json
{
  "task_id": "306b",
  "status": "draft",
  "checkpoint_name": "analysis_complete",
  "progress_pct": 75,
  "findings": {... deeper output ...},
  "ts": "2026-04-24T00:17:45Z"
}
```

Finally, status=final:
```json
{
  "task_id": "306b",
  "status": "final",
  "dashboard_line": "authored 2K-word STIGMERGIC doc; verified; next: review gate",
  "output_path": "/vault/.../doc.md",
  "ts": "2026-04-24T00:19:22Z"
}
```

**Sibling agents (or faerie main) read the same file path repeatedly.** Early reads see draft; later reads see final. No callback needed. Decoupled pace.

**Why this works:**
- File writes are atomic in most filesystems
- Status field is scannable (one-liner grep)
- Sibling doesn't need to poll; reads happen naturally at task boundaries
- Timestamp allows causal ordering without a central clock

### 3. Faerie-Queue BlockedBy Dependency Chains

Sprint queue stores task objects with optional `blockedBy: [task_id1, task_id2]`. Faerie scheduler reads the queue summary:
```json
{
  "task_306b": {
    "status": "queued",
    "blockedBy": ["task_306a"],
    "priority": "MED"
  }
}
```

Faerie sees task_306b is blocked; doesn't dispatch it. When task_306a writes manifest with status=final, faerie's next wave reads the queue again and sees `blockedBy: []` — task_306b is now unblocked and eligible.

**Why it works:**
- Dependency graph is explicit in the queue, not hidden in agent logic
- No back-channel messaging required; the queue update is the signal
- Faerie reads the queue once per wave; O(queue_size) not O(agents²)

### 4. Vault Droplets as Real-Time Insights

Agents write **droplets** (short insights) to a shared vault file the moment inspiration strikes, before full reasoning finishes:

```
# 2026-04-24T00:18:15Z — Connection: Task_id pattern can query predecessor work

Realized that task_id in filename enables zero-cost predecessor discovery. If new agent needs to know 
what a prior agent found, `grep -r "_{task_id}_" forensics/` is instant. This inverts the coordination model 
from "agents ask main for context" to "agents grep the filesystem for their own context."

File: forensics/manifests/..., droplets/LIVE-2026-04-24.md
```

Droplets are written immediately (anti-evaporation), not after full synthesis. Other agents can read droplets to cross-pollinate ideas without waiting for the originating agent to finish.

**Why it works:**
- Capture reasoning WHILE it's forming, not after it's polished
- Shared vault is passive; no coordination overhead
- Other agents read asynchronously; original agent doesn't block

### 5. Stigmergy Registry — Shared Task Lists with Atomic Claims

When multiple agents need to divide work (e.g., a team with 3 lane leads), they share a task list:

```
~/.claude/tasks/{team_name}/
  001-ingestion.task.md      (unclaimed)
  002-schema-mapping.task.md (unclaimed)
  003-anomaly-detection.task.md (unclaimed)
```

Each agent atomically claims a task via rename:
```bash
mv ~/.claude/tasks/w2-investigate/002-schema-mapping.task.md \
   ~/.claude/tasks/w2-investigate/002-schema-mapping.claimed.md
```

If rename succeeds, this agent owns the task. If another agent's rename races ahead, this agent sees the `.claimed.md` and picks the next unclaimed task. **Single-writer-wins** without a lock server.

**Why it works:**
- Filesystem rename is atomic (one syscall)
- No coordination layer needed; the filesystem IS the layer
- Supports arbitrary number of competing agents
- Failure recovery is implicit (unclaimed files exist if agent crashed before completion)

---

## Design Intent: Why Stigmergy Over SendMessage?

### 1. Orchestration Burden on Main ≈ 0 (f(0))

If agents send messages to main asking "what should I do next?" or "did your sibling finish?", main must:
- Receive N messages per wave
- Synthesize context from each
- Route decisions
- Send replies

**Cost:** O(N) main-session inference, 15-25K tokens per agent bootstrap, back-channel latency.

With stigmergy, main spawns agents, reads one FINAL manifest per wave, proceeds. Agents find context and coordinate via the filesystem.

**Cost:** O(1) main work, zero message-round-trip latency, agents act immediately on written state.

### 2. Cache Efficiency — Hit the 5-Minute Token TTL

Faerie's W1 (first-stage liftoff) spawns agents in parallel. If agents immediately start reading ancestor context via SendMessage, each message is a separate API call and burns the 5-minute cache window. If agents read from git or local forensics files instead, the cache is preserved across the whole wave.

**Concrete:** 50 agents in W1, 5 messages per agent to ask for context = 250 API calls. 250 calls × ~20-30 seconds per round-trip = agents are idle waiting for replies while the 5-minute window expires. With filesystem reads, all 50 agents hit local disk and start working immediately.

### 3. Resilience to Agent Churn

If an agent crashes before sending a reply to a sibling, the sibling blocks forever (deadlock). Filesystem state doesn't have this problem — manifest files are immutable evidence; if an agent crashes, its partial manifest still exists and downstream agents can inspect it (and decide to retry, escalate, or route around the problem).

### 4. Replay and Audit

Every artifact written to the filesystem is permanent and queryable. If a mistake happens, the full audit trail exists: what agent wrote what when, in what order, with what hash. SendMessage logs can be rotated or lost. Filesystem artifacts, especially when git-tracked and hash-chained, are durable evidence.

---

## Stigmergy Patterns in Practice

### Pattern 1: Pre-Computation Summary (mth00083)

Large state files grow unboundedly. Instead of faerie parsing the full file, a script computes a summary atomically:

```
sprint-queue.json (1MB, 500 tasks)
  ↓ (atomic write)
sprint-queue-summary.json (200 bytes, top 3 unclaimed + count)
```

Faerie reads ONLY the summary. If the summary is stale, it triggers a rebuild (which re-parses the full file and re-writes the summary). This inverts read-time cost from O(queue_size) to O(1).

**Why it works:** Pre-computation happens at write-time (cheap); read-time is cached (near-free). The full file is an audit log (immutable); the summary is the API.

### Pattern 2: Cascading Summarization (mth00074)

Main reads ONLY `dashboard_line` (≤80 chars) from each agent. Full output goes to forensics. If main needs deeper synthesis: spawn a synthesizer agent that reads N predecessor manifests and returns its own dashboard_line.

Result: unbounded agent count with bounded main context. Synthesis happens in subagent, not main.

### Pattern 3: Hash-Chained COC (Chain of Custody)

Every forensic artifact records the hash of the prior artifact:
```json
{
  "ts": "2026-04-24T00:19:22Z",
  "agent_run_id": "ae2e1d4f",
  "file_hash": "sha256:abc123...",
  "prior_entry_hash": "sha256:def456...",
  "entry_hash": "sha256:ghi789..."
}
```

The chain is immutable: if someone tampers with an entry, the hash of the next entry no longer matches. The full chain becomes a cryptographic proof of integrity. Combined with B2 WORM bucket compliance-mode retention (mth00076), the chain is tamper-evident beyond admin compromise.

---

## Anti-Patterns: What Stigmergy Is NOT

### 1. Not a Message Queue

Stigmergy has no queue depth, no enqueue/dequeue semantics, no consumer groups. Agents write once; any agent reads anytime. It's a shared filesystem, not a broker.

### 2. Not Eventual Consistency

Filesystem state is strongly consistent (POSIX semantics on local disk). A file written by agent A is immediately visible to agent B reading from the same disk. No "eventual" delay.

### 3. Not Polling

Agents don't loop checking "is the file written yet?" — they assume upstream agents have finished (enforced by queue dependencies) and read the manifest immediately.

### 4. Not Broadcast / Publish-Subscribe

There's no subscriber registry, no pub/sub broker, no topic namespace. Agents read specific file paths they know about (task_id-based grep, team-member manifest path, shared task list location). Direct reads, not subscriptions.

---

## Fault Tolerance & Recovery

### Partial Manifests

If an agent crashes mid-execution, its manifest (status=in-progress) remains on disk. Downstream agents see it and can:
- Wait (assume retry will happen)
- Escalate (route to exception handler)
- Work around (assume the partial output and continue)

**No silent failure:** the crash is visible in the manifest state.

### Stale Droplets

A droplet written before the originating agent finished thinking is stale (reasoning continued but droplet was fixed at write-time). Downstream agents treat droplets as hints, not truth. If a droplet contradicts the final manifest, the manifest wins (it's the authoritative artifact).

### Orphaned Tasks in Queue

If a task is claimed but never completed, the `.claimed.md` file remains. Faerie can detect orphaned claims (task hasn't progressed in 5+ minutes) and re-queue it.

---

## Scaling Properties

**Agent count:** 1 to 1000+ agents per wave have no impact on main-session cost; each agent read/writes independent files. The O(1) invariant holds.

**Task count:** 1 to 100K+ tasks in sprint-queue.json; faerie reads only the pre-computed summary (200 bytes), not the full file. O(1) read.

**Message traffic:** Zero; all coordination is filesystem-native. No network, no broker.

**Latency:** Manifest reads are disk-latency (milliseconds), not API-round-trip (seconds). Agents start working immediately.

---

## Conclusion

Stigmergy inverts the coordination model from "agents ask main" to "agents cooperate via shared state." The filesystem becomes the API, task_id becomes the join key, and fsync + hash-chaining become the proofs.

This design enables **f(0):** orchestration burden on main ≈ 0, unbounded agent scaling, and guaranteed audit trails. No SendMessage, no polling, no callback handlers. Just durable, queryable, cryptographically-proven state.

---

## References

| Reference | Cite |
|-----------|------|
| Task_id as join key | sys00033 |
| Stigmergy-only principle | sys00031 |
| Cascading summarization | mth00074 |
| Pre-computation at write-time | mth00083 |
| Proof-in-place discipline | mth00076 |
| Main-inference heuristic | mth00086 |
| Faerie2 architecture spec | CLAUDE.md |

---

**Document ID:** 30-stigmergic-swarm | **Author:** general-purpose agent | **Session:** 2026-04-24 W1 | **Next:** faerie routing decision
