---
type: governance
status: archived
created: 2026-04-28
archived_date: 2026-04-30
archived_reason: "Consolidated into Vault Governance Master (01-forensic-governance.md)"
superseded_by: 01-forensic-governance.md
canonical_url: "/2026-04-28/01-forensic-governance.md#work-hierarchy-codex"
tags: [work-hierarchy, governance, archived]
compass_edge: W
investigation_label: vault-crystallization-audit
---

# 🗂️ Work Hierarchy Codex — Precise Language & Anti-Mission-Creep

**ARCHIVED:** This document has been consolidated into [[01-forensic-governance.md]]. See that document for the current, authoritative version.

**Breadcrumb:** [[00-DASHBOARD]] > [[01-forensic-governance]] > Work Hierarchy Codex section

---

# 🗂️ Work Hierarchy Codex — Precise Language & Anti-Mission-Creep

**Breadcrumb:** [[00-DASHBOARD]] > [[07-work-hierarchy-codex]]

> **Purpose:** Single source of truth for all terminology. Prevents drift, mission creep, and amnesia. Every decision, dispatch, and manifest references this codex.

---

## ⚙️ MISSION GRAPH = The Whole System

The **mission graph** is NOT a queue. It is a **directed acyclic graph (DAG) of work units**, physically encoded in filesystem artifacts (`forensics/{type}/{date}/`), navigated via compass bearings (N/S/E/W), and clustered by `investigation_label`.

**Key property:** Mission graph is STATIC + DYNAMIC.
- **Static:** Manifests + artifacts in `forensics/` (immutable, survives session end)
- **Dynamic:** `next_task` edges point to future work (discovered by agents via frontier scans, written as next-bearing field)

**Visual:** X-axis = time (task sequence); Y-axis = investigation_label (clustering); Z-axis = compass bearing (direction). No linear queue. Pure graph navigation.

---

## 📊 Hierarchy of Work Products (Root to Leaf)

**All work outputs fit into this precise hierarchy. Nothing exists outside it.**

```
┌─────────────────────────────────────────────────────────┐
│ 🎯 MISSION (Investigation Label Cluster)               │
│    Highest level: all work sharing investigation_label  │
│    Example: "treasury-cert-ip-origins" spans 12 tasks   │
│    Status: Candidate → Validated → Active               │
│    Stored in: investigations-registry.json (COC-tracked)│
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
   ┌─────────────┐   ┌──────────────┐
   │ 📋 PHASE    │   │ 🔗 BLOCKER   │
   │ (N/S/E/W)   │   │ CHAIN (deps) │
   └────────────┘   └──────────────┘
        │
        ▼
   ┌─────────────────────────────────────────┐
   │ 📌 TASK (Task ID)                       │
   │ Single unit of work for one agent       │
   │ Deliverable: manifest + artifacts       │
   │ Stored in: forensics/manifests/{date}/  │
   └────────────┬────────────────────────────┘
        │       │
        ▼       ▼
    ┌────┐  ┌────────────┐
    │📝  │  │ 📦 BUNDLE  │
    │MAN.│  │ (input ctx)│
    └────┘  └────────────┘
        │
        ▼
   ┌─────────────────────────────────────────┐
   │ 🔨 STEP (Agent Action)                  │
   │ Atomic unit within task execution       │
   │ Example: "read manifest", "filter data",│
   │ "spawn follow-up agent"                 │
   │ Stored in: manifest.steps[]             │
   └────────────┬────────────────────────────┘
        │
        ▼
   ┌──────────────────────────┐
   │ 📄 ARTIFACT (Work Output)│
   │ Leaf product: analysis,  │
   │ code, findings, report   │
   │ Stored in:               │
   │ forensics/artifacts/date/│
   └──────────────────────────┘
```

---

## 🎯 MISSION — Investigation Label + Coherence

**Definition:** A mission is a VALIDATED, CLUSTERED set of tasks sharing a single `investigation_label` and meeting coherence criteria.

**Properties:**
- `investigation_label` (string) — narrative theme, immutable once validated
- `status` (enum) — one of: candidate, validated, active, abandoned, merged
- `validation_timestamp` (ISO 8601) — when main validated coherence
- `validated_by` (agent ID) — who made validation decision
- `coherence_score` (float 0.0–1.0) — entropy-based focus metric
- `manifest_count` (int) — how many task manifests in this mission
- `compass_edges_present` (list) — which bearings exist (N/S/E/W)
- `agent_types` (list) — which agent types contributed
- `parent_investigation` (string|null) — if merged into another mission, link to parent

**Example:**
```json
{
  "investigation_label": "treasury-cert-ip-origins",
  "status": "active",
  "validated_at": "2026-04-25T10:30:00Z",
  "validated_by": "main",
  "coherence_score": 0.92,
  "manifest_count": 12,
  "compass_edges_present": ["N", "S", "E"],
  "agent_types": ["researcher", "data-analyst", "code-reviewer", "ai-engineer"],
  "parent_investigation": null
}
```

**Stored in:** `forensics/investigations-registry.json` (one per repo, aggregated by cross-repo scanner)

**Validation Criteria (Selection Pressure):**
- ✅ ≥3 manifests sharing same label
- ✅ Coherence score ≥0.70 (not fragmented)
- ✅ Agent types are complementary (not all the same type)
- ✅ Compass edges form connected chain (N→S or E→W paths exist)
- ❌ Reject: <3 manifests, coherence <0.70, single agent type only, no paths

---

## 📋 PHASE — Compass Bearing + Time Sequence

**Definition:** A phase is a DIRECTIONAL + TEMPORAL UNIT in a mission. It is ONE STEP along the compass (one bearing: N, S, E, or W) that UNBLOCKS downstream work or resolves a BLOCKER.

**NOT:** Phases are NOT sequential stages (SEED → DEEPEN → EXTEND → FULL). That is a QUALITY GATE metric, separate concept.

**Core property:** Each phase has a CLEAR BEARING that moves the mission forward:

| Bearing | Meaning | Example | Next Phase |
|---------|---------|---------|-----------|
| **⬆️ N (North)** | Unblock prerequisites | "Discover IP origins via DNS pivot" | S (when data found) |
| **⬇️ S (South)** | Proceed / Advance | "Analyze cert chain with found IPs" | Done (or E for validation) |
| **➡️ E (East)** | Parallel investigation | "Cross-validate via secondary source" | S (merge results) |
| **⬅️ W (West)** | Retreat / Reframe | "Approach failed, try new hypothesis" | N or E (new direction) |

**Example Phase Sequence (One Mission):**
```
Mission: treasury-cert-ip-origins
├─ Phase 1 (N): "Discover certificate origin via WHOIS/DNS"
│   └─ Tasks: whois-lookup, dns-pivot, ip-registry-scan
│   └─ Status: Complete, found 3 IP ranges
│   └─ Next bearing: S (proceed to analysis)
│
├─ Phase 2 (S): "Analyze geographic distribution of IPs"
│   └─ Tasks: geoloc-analysis, isp-mapping, infrastructure-map
│   └─ Status: In progress, 70% complete
│   └─ Next bearing: E (parallel: validate via third source)
│
└─ Phase 3 (E): "Cross-validate findings with BGP routing data"
    └─ Tasks: bgp-validation, routing-audit
    └─ Status: Queued
    └─ Next bearing: S (merge into final report)
```

**Key constraint:** Each PHASE emits ONE MANIFEST with ONE bearing. Phase is NOT a task; it is a DIRECTION + one or more TASKS that together move that direction.

**Stored in:** Manifest field `compass_edge` (bearing) + `phase_label` (human description)

---

## 📌 TASK — Atomic Unit of Work (Task ID)

**Definition:** A task is a SINGLE UNIT OF WORK assigned to ONE AGENT. It has one `task_id`, one `dashboard_line`, one `next_task` bearing.

**Properties:**
- `task_id` (string) — unique identifier, format: `{mission_label}-{sequential_number}` or UUID
- `investigation_label` (string) — which mission does this task belong to?
- `agent_type` (string) — who executes this? (researcher, code-reviewer, etc.)
- `status` (enum) — pending, in_progress, completed, blocked, abandoned
- `created_at` (ISO 8601) — when was task created?
- `started_at` (ISO 8601|null) — when did agent start?
- `completed_at` (ISO 8601|null) — when did agent finish?
- `dashboard_line` (string ≤80 chars) — one-line summary of outcome
- `compass_edge` (enum N|S|E|W) — which direction did this task move?
- `next_task` (task_id|null) — what task unblocks downstream?
- `artifacts` (list) — filenames of work products generated

**Example:**
```json
{
  "task_id": "treasury-cert-ip-origins-001",
  "investigation_label": "treasury-cert-ip-origins",
  "agent_type": "researcher",
  "status": "completed",
  "created_at": "2026-04-25T09:00:00Z",
  "started_at": "2026-04-25T09:15:00Z",
  "completed_at": "2026-04-25T10:30:00Z",
  "dashboard_line": "Found 12 WHOIS entries; 3 IP ranges identified; DNS pivots queued",
  "compass_edge": "S",
  "next_task": "treasury-cert-ip-origins-002",
  "artifacts": [
    "forensics/artifacts/2026-04-25/10-30-00Z_whois_dump.json",
    "forensics/artifacts/2026-04-25/10-30-01Z_ip_ranges.csv"
  ]
}
```

**Stored in:** `forensics/manifests/{date}/{task_id}_manifest.json`

---

## 🔗 BLOCKER CHAIN — Prerequisites & Dependencies

**Definition:** A blocker chain is a DEPENDENCY GRAPH within a mission. Task B is BLOCKED by task A if B's input data depends on A's output.

**Compass encoding:**
- **North edge (A→B):** A is blocked by B (B must complete first)
- **Inverted:** B has "next_task": A_id

**Example Chain:**
```
Task 1 (N edge): "Discover IP origins via DNS"
  └─ next_task: Task 2

Task 2 (S edge): "Validate IPs via BGP routing"
  └─ next_task: Task 3

Task 3 (S edge): "Generate final report"
  └─ next_task: null (end of chain)
```

**Enforcement:** `/run --missions` reads `next_task` field and claims tasks in dependency order. Never claims Task 2 until Task 1 manifest exists.

---

## 📦 BUNDLE — Execution Context Package

**Definition:** A bundle is the INPUT DATA given to an agent at spawn time. It contains all context the agent needs: global facts (HONEY), recent findings (NECTAR), current observations (pollen), task description, and investigation background.

**Structure:**
```json
{
  "task_id": "treasury-cert-ip-origins-001",
  "investigation_label": "treasury-cert-ip-origins",
  "mission_context": {
    "phase": "unblock prerequisites",
    "compass_edge": "N",
    "blocker": "Need IP origin data before analysis can proceed"
  },
  "honey": "{ ...1K universal facts... }",
  "nectar": "{ ...recent HIGH findings... }",
  "pollen": "{ ...live session observations... }",
  "task_goal": "Discover origin IPs of treasury certificate via WHOIS/DNS pivots",
  "agent_type": "researcher",
  "constraints": [
    "Complete within 15 min",
    "Output must be CSV or JSON, not narrative",
    "Must cite sources (WHOIS registrar, DNS timestamp)"
  ]
}
```

**Stored in:** `forensics/bundles/{date}/{task_id}_bundle.json`

---

## 🔨 STEP — Atomic Agent Action

**Definition:** A step is ONE DISCRETE ACTION within a task. Examples: "read manifest", "query database", "generate report", "spawn follow-up agent".

**Not stored separately.** Steps are LOGGED IN-FLIGHT in the manifest's `steps[]` array:

```json
{
  "task_id": "treasury-cert-ip-origins-001",
  "steps": [
    {
      "seq": 1,
      "action": "read_frontier_scans",
      "duration_ms": 150,
      "result": "found 3 prior DNS pivot tasks"
    },
    {
      "seq": 2,
      "action": "execute_whois_query",
      "duration_ms": 3200,
      "result": "12 WHOIS records retrieved"
    },
    {
      "seq": 3,
      "action": "write_manifest",
      "duration_ms": 50,
      "result": "manifest written to forensics/manifests/2026-04-25/"
    },
    {
      "seq": 4,
      "action": "frontier_scan_discovery",
      "duration_ms": 200,
      "result": "discovered downstream task: BGP validation queued"
    }
  ]
}
```

**Governance:** Steps are IMMUTABLE once written (part of forensic record). They provide complete execution trace for debugging + auditing.

---

## 📄 ARTIFACT — Work Product (Leaf Output)

**Definition:** An artifact is a CONCRETE DELIVERABLE generated by a step. It is the final output of work: analysis document, CSV data, code file, report, etc.

**Properties:**
- **Path:** `forensics/artifacts/{date}/{timestamp}_{task_id}_{agent_type}_{counter}.{ext}`
- **Immutable:** Written once, never modified
- **Signed:** Ed25519 signature in COC entry (chain-of-custody)
- **Referenced:** Linked from manifest's `artifacts[]` field
- **Court-ready:** Complete lineage: path shows date + task + agent + counter

**Examples:**
```
forensics/artifacts/2026-04-25/
  09-30-00Z_treasury-cert-ip-origins-001_researcher_001.json     (WHOIS data)
  09-31-00Z_treasury-cert-ip-origins-001_researcher_002.csv      (IP ranges)
  10-15-00Z_treasury-cert-ip-origins-002_analyst_001.md          (analysis report)
```

**Never in `.claude/` folder.** Always in `forensics/artifacts/` (system of record).

---

## 🗺️ LINEAR X-AXIS: Task Sequence (Temporal + Dependency Order)

The mission graph's **linear projection** (time-axis view) shows tasks in **execution order** (dependency-sorted):

```
Time ──────────────────────────────────────────────────────►

Task 1 (N): Discover IPs
  └─ Output: ip_ranges.csv
  └─ Duration: 15 min
  └─ next_task: Task 2

    Task 2 (S): Validate via BGP
      └─ Input: Task 1's ip_ranges.csv
      └─ Output: bgp_validation.json
      └─ Duration: 8 min
      └─ next_task: Task 3

        Task 3 (S): Generate report
          └─ Input: Task 2's bgp_validation.json
          └─ Output: final_report.md
          └─ Duration: 5 min
          └─ next_task: null (done)

Total: 28 min wall time (sequential)
       3 tasks | 1 mission | compass path: N→S→S
```

**Key insight:** Linear X-axis is NOT the "real" shape. Real shape is DAG (parallel E edges, W retreats, etc.). X-axis is just one projection for human consumption.

---

## 🔬 QUALITY GATES — Separate from Phases (NOT a phase)

**⚠️ CRITICAL DISTINCTION:**

Quality gates (SEED 0.50, DEEPEN 0.70, EXTEND 0.80, FULL 0.85) are **EVALUATION THRESHOLDS**, not phases.

- **Phase:** Compass direction (N/S/E/W) — WHERE you are going in the mission
- **Quality gate:** Score threshold (0.50–0.85) — HOW GOOD the output is

**They are ORTHOGONAL:**
- Task can be at phase N (unblock) AND quality SEED (early)
- Task can be at phase S (proceed) AND quality FULL (mature)
- Quality gates inform WHETHER to proceed past the phase (not the phase itself)

**Example:**
```
Task: Discover IPs via WHOIS
├─ Phase: N (North, unblock prerequisite)
├─ Quality gate: SEED (0.50 threshold)
├─ Actual quality: 0.65 (passes SEED, borderline DEEPEN)
└─ Decision: Proceed to next phase (S) because quality ≥ 0.50
```

---

## ⚖️ TWO TASK CLASSES — Subject Matter vs. System Dynamics

**CRITICAL DISTINCTION:** Not all tasks are equal. Some tasks are SUBJECT MATTER (domain-specific investigation work). Others are SYSTEM DYNAMICS (infrastructure, orchestration, tooling).

### Subject Matter Tasks (Domain-Specific Missions)
**Definition:** Tasks that directly advance an investigation_label mission.

**Examples:**
- "Discover IP origins via WHOIS" (treasury-cert-ip-origins mission)
- "Analyze geographic distribution of IPs" (same mission)
- "Validate via BGP routing" (same mission)

**Properties:**
- Belong to investigation_label (required)
- Generate domain artifacts (analysis, findings, data)
- Compass edges chart the MISSION progression (N→S→E)
- Stored in: `forensics/manifests/`, `forensics/artifacts/`
- Status: Candidate → Validated → Active (via investigations-registry.json)

### System Dynamics Tasks (Infrastructure & Orchestration)
**Definition:** Tasks that BUILD or MAINTAIN the mission graph infrastructure itself.

**Examples:**
- "Implement cross-repo mission graph aggregator" (sys-mission-graph-aggregator)
- "Create investigations-registry.json validation workflow" (sys-registry-validation)
- "Implement sync-settings.py for settings drift detection" (sys-settings-sync)
- "Write forensic COC signing hooks" (sys-forensic-integrity)

**Properties:**
- investigation_label format: `sys-{subsystem}` (explicit "system dynamics" prefix)
- Do NOT chart compass edges (they're not part of domain missions)
- Generate infrastructure artifacts (code, configs, hooks)
- Stored in: `forensics/manifests/`, `.claude/scripts/`, `.claude/hooks/`
- **CRITICAL:** System dynamics work is ABOUT the mission graph, not OF the mission graph

**Key rule:** System dynamics tasks are **FOUNDATIONAL, not discovery**. They enable subject matter work. Do not let system dynamics tasks proliferate. Only create sys- tasks when they unblock multiple subject matter missions or fix critical infrastructure.

---

## 📖 CODEX REFERENCE (Always Cite This)

When discussing work structure, use this hierarchy:

1. **🎯 Mission** (investigation_label + coherence + status) — cluster of related work
2. **📋 Phase** (N/S/E/W bearing) — directional unit within mission
3. **📌 Task** (task_id) — atomic work for one agent
   - **Subject matter:** investigation_label without `sys-` prefix (treasury-cert-ip-origins, sdk-readiness-mcp, etc.)
   - **System dynamics:** investigation_label with `sys-` prefix (sys-mission-graph-aggregator, sys-registry-validation, etc.)
4. **📦 Bundle** (task context) — input data package
5. **🔨 Step** (discrete action) — atomic agent operation
6. **📄 Artifact** (work product) — concrete output

**Example sentence:** "Mission treasury-cert-ip-origins (subject matter) has 3 phases (N→S→E). Phase 2 (S) consists of task 002, which spawned a code-reviewer to generate a validation artifact. Meanwhile, sys-mission-graph-aggregator (system dynamics) unblocks this work by enabling cross-repo manifest discovery."

**Anti-pattern:** "Let me do phase 2" (wrong—phases are NOT actions, they are DIRECTIONS). Correct: "Let me work on phase 2's task-002."

---

## 🛡️ Anti-Mission-Creep Enforcement

**Mission Creep Risk:** Tasks drift from investigation_label, phases lose bearing, no one knows what the mission is anymore.

**Enforcement Points:**
1. ✅ **Pre-spawn:** Manifest MUST include `investigation_label` (required field, not optional)
2. ✅ **Pre-validation:** Investigation must have ≥3 tasks before validation (prevents single-task "missions")
3. ✅ **Per-manifest:** `compass_edge` MUST be one of N/S/E/W (not freeform)
4. ✅ **Drift detection:** If task's `investigation_label` changes, COC entry logs the change + reason
5. ✅ **Validation gate:** Only validated missions appear in `/run --missions` discovery

**Result:** Mission creep is visible. Drift is logged. Amnesia is prevented because EVERY task's lineage is in forensics/.

---

## 📚 References

- `06-investigation-id-governance.md` — Investigation lifecycle (candidate → active)
- `CLAUDE.md mth00101` — Compass Navigation Protocol
- `forensics/investigations-registry.json` — COC-tracked mission registry
- `forensics/manifests/{date}/` — All task outcomes

---

**Last Updated:** 2026-04-28 14:22 UTC  
**Related:** [[06-investigation-id-governance]], [[00-DASHBOARD]]  
**Status:** CANONICAL — all system references must cite this codex
