---
created: 2026-03-28
updated: 2026-03-28
type: system-design
status: active
tags: [hive, architecture, system-design, piston-model, memory, forensics, modularity]
aliases: [Piston Model, Hive Frame, System Map]
parent:
  - "[[_system-root]]"
doc_hash: sha256:345149544289835041bdb22c84532d849b98939ec6842dd9f1b0241fba49ac52
hash_ts: 2026-03-29T16:10:27Z
hash_method: body-sha256-v1
---

# Hive Frame — System Architecture

> **Start here:** [[SYSTEM-GUIDE]] for a full clickable learning guide.

## Related Docs

### Deep Dives (by diagram section)

| Diagram | Deep-dive doc | Pseudosystem component |
|---------|--------------|----------------------|
| Piston engine | [[PISTON-MODEL-DESIGN]] | [[session-lifecycle]] |
| Session lifecycle | [[faerie-start]] / [[handoff-end]] | [[emergency-handoff]] |
| Memory architecture | [[13-MEMORY-FLOW-ARCHITECTURE]] | [[memory-layer]] / [[honey-seed]] / [[nectar-narrative]] |
| faerie's role | [[11-FAERIE-IMPACT-AB]] | [[faerie-start]] / [[subagent-spawning]] |
| Three independent systems | [[system-state-files-guide]] | [[state-engine]] / [[context-budget]] |
| Forensics isolation | [[HOW-ANNOTATION-COC-WORKS]] | [[forensic-layer]] / [[coc-hash-chain]] |
| Data flow | [[PIPELINE-DESIGN]] | [[agent-outbox]] / [[vault-layer]] |
| Modular sauce | [[15-MODULAR-SECRET-SAUCE]] | — |

### Related Design Narratives

```dataview
LIST
FROM "00-SHARED/Hive"
WHERE (type = "system-design" OR type = "design-narrative" OR type = "narrative")
  AND file.name != this.file.name
SORT default(updated, created) DESC
LIMIT 10
```

### Component Notes Referenced

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Component",
  component_type AS "Type"
FROM "00-SHARED/Hive/pseudosystem"
WHERE contains(["session-lifecycle", "memory-layer", "honey-seed", "nectar-narrative", "forensic-layer", "coc-hash-chain", "faerie-start", "handoff-end", "agent-layer", "subagent-spawning", "state-engine", "context-budget", "equilibrium", "crystallization", "sprint-queue", "vault-layer", "agent-outbox"], file.name)
SORT component_type ASC, file.name ASC
```

---

## The Piston: Session Engine

```mermaid
graph TD
    subgraph PISTON["🔧 PISTON ENGINE"]
        direction TB
        W1["Wave 1: FAST: ~45s return</br>Explore, security-auditor</br>admin-sync, token-optimizer"]
        W2["Wave 2: MEDIUM</br>~3min return</br>python-pro, data-engineer</br>evidence-analyst, knowledge-synth"]
        W3["Wave 3: DEEP</br>~10min return</br>data-scientist, research-analyst</br>evidence-curator"]

        W1 -->|"fast returns → relaunch"| W1
        W1 -->|"~30s delay"| W2
        W2 -->|"~90s delay"| W3
        W3 -->|"results → queue new cycle"| W1
    end

    style W1 fill:#4a9eff,color:#fff
    style W2 fill:#f5a623,color:#fff
    style W3 fill:#d0021b,color:#fff
    style PISTON fill:#1a1a2e,color:#fff
```

## Session Lifecycle

```mermaid
graph LR
    subgraph SESSION["Session Lifecycle"]
        F["/faerie</br>START"] --> WORK["Work Phase</br>Piston running"]
        WORK --> H["/handoff</br>END"]
        WORK -.->|"mid-session"| C["/crystallize"]
        C -.-> WORK
    end

    subgraph COMPACT["Auto-Compact"]
        AC["Context full"] --> PRE["pre_compact_hook</br>writes checkpoint"]
        PRE --> SQUISH["Compact fires</br>Context summarized"]
        SQUISH --> RESUME["surfacing_scheduler</br>resume"]
        RESUME -->|"skip done waves</br>launch next"| WORK
    end

    style F fill:#7b68ee,color:#fff
    style H fill:#e74c3c,color:#fff
    style C fill:#2ecc71,color:#fff
    style AC fill:#95a5a6,color:#fff
    style RESUME fill:#4a9eff,color:#fff
```

## Memory Architecture: Separate Systems

```mermaid
graph TB
    subgraph WORKING["Working Memory (per-session)"]
        SCRATCH["scratch-{SID}.md</br>Raw observations</br>MEM blocks"]
    end

    subgraph DURABLE["Durable Memory (survives sessions)"]
        HONEY["HONEY.md</br>Preferences & methods</br>Earned through time"]
        NECTAR["NECTAR.md</br>Validated findings</br>Append-only, never compress"]
        REVIEW["REVIEW-INBOX.md</br>HIGH flags for human</br>Append-only"]
    end

    subgraph FORENSIC["Forensic Record (repo-root, agent-blind)"]
        COC["forensic-coc.jsonl</br>Hash-chained COC"]
        MANIFEST["hash_manifest*.json</br>Evidence integrity"]
        BRIEFS["session-briefs/</br>Per-session snapshots"]
    end

    SCRATCH -->|"membot promotes"| NECTAR
    SCRATCH -->|"HIGH flags"| REVIEW
    NECTAR -->|"crystallization</br>(multi-mind forging)"| HONEY
    SCRATCH -->|"auto-append</br>(hook, write-only)"| COC

    style WORKING fill:#2d3436,color:#fff
    style DURABLE fill:#0c3c26,color:#fff
    style FORENSIC fill:#4a0000,color:#fff
    style HONEY fill:#f1c40f,color:#000
    style NECTAR fill:#e67e22,color:#fff
    style REVIEW fill:#e74c3c,color:#fff
    style COC fill:#7f0000,color:#fff
```

## faerie's Role: Orchestrator, Not Worker

```mermaid
graph TB
    subgraph FAERIE["faerie: Parent Session"]
        ORIENT["1. Orient</br>Read handoff/brief/HONEY"]
        PLAN["2. Plan</br>surfacing_scheduler piston"]
        LAUNCH["3. Launch</br>Agent tool × N"]
        CONDUCT["4. Conduct **Process returns**</br>Relaunch fast agents"]
        SYNTH["5. Synthesize</br>**Connect findings**</br>Update hypotheses"]
    end

    subgraph AGENTS["Subagents (200K each)"]
        A1["evidence-analyst"]
        A2["python-pro"]
        A3["data-scientist"]
        A4["membot"]
    end

    subgraph QUEUE["Queue System"]
        QF["sprint-queue.json"]
        QA["queue-archive/"]
        KB["Kanban board</br>(Obsidian sync)"]
    end

    ORIENT --> PLAN --> LAUNCH
    LAUNCH --> A1 & A2 & A3 & A4
    A1 & A2 & A3 -->|"returns"| CONDUCT
    A4 -->|"memory work"| CONDUCT
    CONDUCT --> SYNTH
    CONDUCT -->|"relaunch"| LAUNCH
    QF --> LAUNCH
    SYNTH -->|"auto-queue follow-ups"| QF
    QF <-->|"bidirectional sync"| KB

    style FAERIE fill:#2c1654,color:#fff
    style AGENTS fill:#1a3a5c,color:#fff
    style QUEUE fill:#1a3c1a,color:#fff
```

## Three Independent Systems

```mermaid
graph LR
    subgraph PHASES["Context Phases"]
        CP["context_phase.py"]
        CP --> LIFT["LIFTOFF</br>0-30%"]
        CP --> ORB["ORBIT</br>30-70%"]
        CP --> DEO["DEORBIT</br>70-85%"]
        CP --> REE["REENTRY</br>85%+"]
    end

    subgraph SURFACING["Surfacing Scheduler"]
        SS["surfacing_scheduler.py"]
        SS --> PLAN2["Wave planning"]
        SS --> CAL["Self-calibration"]
        SS --> RESUME2["Post-compact resume"]
    end

    subgraph METRICS["Session Metrics"]
        SM["session_metrics.py"]
        SM --> KPI["7 hash-chained KPIs"]
        SM --> TREND["Trend reports"]
    end

    KPI -->|"calibration</br>feedback loop"| CAL

    style PHASES fill:#34495e,color:#fff
    style SURFACING fill:#2c3e50,color:#fff
    style METRICS fill:#1a252f,color:#fff
```

## Forensics Isolation Architecture

```mermaid
graph TB
    subgraph REPOS["Investigation Repos"]
        CT["cybertemplate/forensics/</br>COC, manifests, session briefs"]
        DAE["data-analysis-engine/forensics/</br>Analysis logs, genesis ledger"]
        F2["faerie2/forensics/</br>(future)"]
    end

    subgraph GLOBAL["Global Forensics"]
        GF["~/.claude/memory/forensics/</br>Annotation receipts</br>Vault manifests"]
    end

    subgraph DENY["Agent Access"]
        R["Read: DENIED</br>(settings.json deny rules)"]
        W["Write: APPEND ONLY</br>(via forensic_coc.py hook)"]
    end

    CT & DAE & F2 --> R
    CT & DAE & F2 --> W

    AGG["Cross-repo aggregation:</br>find */forensics/ -type f"]

    style REPOS fill:#4a0000,color:#fff
    style GLOBAL fill:#4a0000,color:#fff
    style DENY fill:#2d3436,color:#fff
    style R fill:#c0392b,color:#fff
    style W fill:#27ae60,color:#fff
```

## Data Flow: End to End

```mermaid
graph LR
    USER["Human"] -->|"/faerie"| SESSION["Session"]
    SESSION -->|"piston waves"| AGENTS2["Agents"]
    AGENTS2 -->|"findings"| SCRATCH2["Scratch"]
    SCRATCH2 -->|"membot"| NECTAR2["NECTAR"]
    NECTAR2 -->|"crystallize"| HONEY2["HONEY"]
    AGENTS2 -->|"auto-append"| FORENSICS2["Forensics</br>(agent-blind)"]
    SESSION -->|"queue_vault_sync"| OBSIDIAN["Obsidian Vault</br>(human interface)"]
    OBSIDIAN -->|"drag-drop</br>kanban reorder"| SESSION
    USER -->|"annotations"| OBSIDIAN
    SESSION -->|"/handoff"| BRIEF["faerie-brief.json"]
    BRIEF -->|"next /faerie"| SESSION

    style USER fill:#8e44ad,color:#fff
    style SESSION fill:#2c1654,color:#fff
    style AGENTS2 fill:#1a3a5c,color:#fff
    style SCRATCH2 fill:#2d3436,color:#fff
    style NECTAR2 fill:#e67e22,color:#fff
    style HONEY2 fill:#f1c40f,color:#000
    style FORENSICS2 fill:#4a0000,color:#fff
    style OBSIDIAN fill:#6c3483,color:#fff
    style BRIEF fill:#2980b9,color:#fff
```

## Modular Secret Sauce: Paid Feature Architecture

The system supports two build modes: **full** (all features) and **open** (sauce modules removed).
Proprietary modules enhance specific pain points. Remove them and the core still works — just simpler.

```mermaid
graph TB
    subgraph CORE["CORE (always present, fully functional)"]
        direction TB
        SS["surfacing_scheduler.py</br>Job classification</br>Flat batch launches</br>Self-calibration"]
        PCH["pre_compact_hook.py</br>Drain HIGH blocks</br>Droplets snapshot</br>Brief update"]
        QS["queue_ops.py</br>Sprint task queue</br>Atomic claim/complete"]
        MEM["Memory routing</br>HONEY/NECTAR/scratch</br>REVIEW-INBOX"]
        COC2["forensic_coc.py</br>Hash-chained COC</br>Agent-blind logging"]
        AGT["Agent spawning</br>20+ specialized types</br>Fresh 200K each"]
    end

    subgraph SAUCE["SECRET SAUCE (removable __removable__=True)"]
        direction TB
        PI["piston.py</br>Phased wave engine</br>fast/medium/deep rhythm</br>Checkpoint + resume"]
        ON["overnight_synthesis.py</br>Batch Opus analysis</br>Cross-cutting insight"]
        CP2["crystallize_premium.py</br>Advanced integration</br>Multi-mind forging"]
        TL["training_loop.py</br>Agent self-improvement</br>Deployment scoring"]
    end

    SS -->|"try: from piston import plan"| PI
    PCH -->|"try: from piston import checkpoint"| PI
    SS -.->|"ImportError → flat batch"| SS

    style CORE fill:#1a3a5c,color:#fff
    style SAUCE fill:#4a0e0e,color:#fff
    style PI fill:#d4a017,color:#000
    style ON fill:#d4a017,color:#000
    style CP2 fill:#d4a017,color:#000
    style TL fill:#d4a017,color:#000
    style SS fill:#2c5f8a,color:#fff
    style PCH fill:#2c5f8a,color:#fff
```

### How It Works

```mermaid
sequenceDiagram
    participant C as Consumer<br/>(surfacing_scheduler)
    participant P as piston.py<br/>(sauce module)
    participant F as Flat Fallback<br/>(built-in)

    Note over C: try: from piston import plan
    alt piston.py exists (full build)
        C->>P: plan(pending_tasks)
        P-->>C: {model: "piston", waves: [...]}
        Note over C: Three-speed rhythm
    else piston.py removed (open build)
        C->>F: plan_launch_batch(pending_tasks)
        F-->>C: {model: "flat_fallback", batch: [...]}
        Note over C: All agents at once, still works
    end
```

### Pain Points Each Sauce Module Addresses

```mermaid
graph LR
    subgraph PAIN["Pain Points in Agent Orchestration"]
        P1["Agent returns</br>cluster at compact</br>threshold"]
        P2["Context wasted on</br>redundant re-reads</br>after compact"]
        P3["No memory of what</br>worked across</br>100+ sessions"]
        P4["Deep insights lost</br>when context compacts</br>at peak richness"]
    end

    subgraph FIX["Sauce Scripts (paid tier)"]
        F1["piston.py</br>Timed waves prevent</br>return clustering"]
        F2["piston.checkpoint()</br>Resume from exact</br>wave position"]
        F3["training_loop.py</br>Agent self-scoring</br>across deployments"]
        F4["overnight_synthesis.py</br>Batch Opus processes</br>overnight, ready at dawn"]
    end

    P1 --> F1
    P2 --> F2
    P3 --> F3
    P4 --> F4

    style PAIN fill:#5c1a1a,color:#fff
    style FIX fill:#1a3a1a,color:#fff
    style F1 fill:#d4a017,color:#000
    style F2 fill:#d4a017,color:#000
    style F3 fill:#d4a017,color:#000
    style F4 fill:#d4a017,color:#000
```

### Removal Protocol

```bash
# Find all sauce modules
grep -rl '__removable__' ~/.claude/scripts/

# Remove before interview
rm ~/.claude/scripts/piston.py
rm ~/.claude/scripts/overnight_synthesis.py
rm ~/.claude/scripts/crystallize_premium.py
rm ~/.claude/scripts/training_loop.py

# Verify: everything still works
python3 ~/.claude/scripts/surfacing_scheduler.py plan   # flat_fallback model
python3 ~/.claude/scripts/surfacing_scheduler.py resume  # "no_piston_module" status
echo '{}' | python3 ~/.claude/hooks/pre_compact_hook.py  # steps 1-4 work, step 5 skipped
```

## Key Separations

| System | What it is | What it is NOT |
|---|---|---|
| **faerie** | Session orchestrator (read → launch → conduct) | Not a worker — never does task work inline |
| **HONEY** | Sacred preferences/methods earned through time | Not a scratchpad — entries are crystallized, not appended |
| **NECTAR** | Append-only validated findings | Not compressible — forensic truth record |
| **Forensics** | Agent-blind COC at repo root | Not in .claude/ — agents can't read it |
| **Vault** | Human-readable interface / message bus | Not canonical storage — repos are canonical |
| **Queue** | Sprint task list with COC on transitions | Not ephemeral — completed tasks are evidence |
| **Piston** | Three-speed agent wave rhythm (sauce) | Not a scheduler — it's a rhythm (fast/medium/deep/cycle) |
| **Crystallization** | Multi-mind knowledge forging (agents + human + time) | Not compression — integration makes text richer, not shorter |
| **Sauce modules** | `__removable__` scripts enhancing pain points | Not load-bearing — core works without them |


## Blueprint Registry

Agent output types have canonical schema definitions in `Hive/blueprints/`.
Each blueprint specifies required frontmatter, section structure, validation rules,
and links to an example output. Reference via `blueprint: blueprint_{type}` in frontmatter.

### Active Blueprints

| Blueprint | Type | Output Dir | Example |
|-----------|------|------------|---------|
| [[blueprints/blueprint_finding\|blueprint_finding]] | finding | Agent-Outbox/findings/ | (see blueprint) |
| [[blueprints/blueprint_analysis\|blueprint_analysis]] | analysis | Agent-Outbox/analysis/ | (see blueprint) |
| [[blueprints/blueprint_evidence\|blueprint_evidence]] | evidence | Agent-Outbox/evidence/ | (see blueprint) |
| [[blueprints/blueprint_report\|blueprint_report]] | report | Agent-Outbox/reports/ | (see blueprint) |
| [[blueprints/blueprint_brief\|blueprint_brief]] | brief | Session-Briefs/ | (see blueprint) |
| [[blueprints/blueprint_agent_evolution\|blueprint_agent_evolution]] | agent-evolution | Agent-Outbox/agent-evolution/ | [[Agent-Outbox/agent-evolution/example-agent-evolution\|example]] |
| [[blueprints/blueprint_droplet\|blueprint_droplet]] | droplet | Dashboards/Droplets/ | [[Agent-Outbox/droplets/example-droplet-LIVE\|example]] |
| [[blueprints/blueprint_dashboard\|blueprint_dashboard]] | dashboard | Dashboards/ | [[Agent-Outbox/dashboards/example-dashboard\|example]] |
| [[blueprints/blueprint_session_manifest\|blueprint_session_manifest]] | session-manifest | Dashboards/session-briefs/ | [[Dashboards/session-briefs/example-session-manifest\|example]] |
| [[blueprints/blueprint_design_insight\|blueprint_design_insight]] | design-narrative | Hive/ | [[18-blueprint-system-design\|18 — Blueprint System]] |

### How to Use a Blueprint

When writing an agent output file, set `blueprint: blueprint_{type}` in frontmatter.
Read the blueprint file to get required fields and sections. The blueprint is the
single source of truth for that output type — not VAULT-SCHEMA.md (which remains the
canonical universal spec but is too large to consult at write time).

For spawn prompts, include:
```
Blueprint for this output type: 00-SHARED/Hive/blueprints/blueprint_{type}.md
Read it before writing your output file.
```

See [[18-blueprint-system-design]] for the ADR explaining why this system was created.
