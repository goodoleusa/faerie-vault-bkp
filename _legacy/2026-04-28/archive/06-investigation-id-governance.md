---
type: governance
status: archived
created: 2026-04-28
archived_date: 2026-04-30
archived_reason: "Consolidated into Vault Governance Master (01-forensic-governance.md)"
superseded_by: 01-forensic-governance.md
canonical_url: "/2026-04-28/01-forensic-governance.md#investigation-id-governance"
tags: [investigation-id, governance, archived]
compass_edge: W
investigation_label: vault-crystallization-audit
---

# 📍 Investigation ID Governance — Earned Status, Not Arbitrary

**ARCHIVED:** This document has been consolidated into [[01-forensic-governance.md]]. See that document for the current, authoritative version.

**Breadcrumb:** [[00-DASHBOARD]] > [[01-forensic-governance]] > Investigation ID Governance section

---

# 📍 Investigation ID Governance — Earned Status, Not Arbitrary

**Breadcrumb:** [[00-DASHBOARD]] > [[06-investigation-id-governance]]

> Investigation IDs are **earned through validation and selection pressure**, not assigned arbitrarily. Work progresses from unaffiliated → candidate → validated → investigation member.

---

## The Problem: Arbitrary Investigation Affiliation

**Current behavior (drift risk):**
```
Agent writes manifest
  └─ investigation_label: "random-label-i-picked"
     └─ Gets clustered immediately
     └─ No validation that this belongs with similar work
     └─ Noise accumulates (spurious clusters)
```

**Result:** Mission graph polluted with labels that don't represent real work coherence.

---

## Solution: Earned Investigation IDs

### Stage 1: Unaffiliated Work (No investigation_label)

```
Agent completes task
  ├─ Manifest written without investigation_label (or investigation_label: "uncategorized")
  ├─ Artifacts in forensics/artifacts/2026-04-28/
  ├─ Status: "candidate" (not yet validated)
  └─ Discoverable via frontier scan, but not clustered
```

**Who:** Any agent doing exploratory work, research, tooling, utilities.

### Stage 2: Candidate for Investigation

```
Agent discovers work belongs to a larger mission
  ├─ Reads manifests from past 24h via frontier scan
  ├─ Finds similar work (same domain, same compass edges)
  ├─ Updates manifest with investigation_label: "domain-description"
  ├─ Documents evidence: "Found 3 prior manifests with same theme"
  └─ Mark as: "candidate — awaiting validation"
```

**Mechanism:** Agent initiative + honest frontier scan.

### Stage 3: Validation (Selection Pressure)

```
Main (or synthesizer agent) reviews open investigations
  ├─ Reads: candidate investigation_labels with <5 manifests
  ├─ Evaluates: Does this cluster represent real coherence?
  │   ├─ Similar compass edges? ✓
  │   ├─ Shared preconditions/blockers? ✓
  │   ├─ Agent types are complementary? ✓
  │   └─ Manifests link properly (N/S/E/W bearings)? ✓
  ├─ Decision: VALIDATE or REJECT
  ├─ If VALIDATE: mark investigation_label as "active"
  ├─ If REJECT: rename to "abandoned-REASON" or merge into parent
  └─ Update forensics/investigations-registry.json (COC-tracked)
```

**Criteria:** Coherence > activity. 3 manifests + clear theme = valid investigation.

### Stage 4: Active Investigation

```
investigation_label: "treasury-certificate-origins" (validated)
  ├─ Status: active
  ├─ Timestamp validated: 2026-04-25T10:30Z
  ├─ Manifests: 12 (and counting)
  ├─ Compass edges: N(2), S(8), E(2), W(0)
  ├─ Agents participating: 4
  ├─ Next tasks queued: 3 (ready to claim)
  └─ Blocker chain: treasury-cert-ip-origins → certificate-validation → dns-pivot
```

**Status:** Full participation in mission graph. /run --missions clusters by this label.

---

## Cross-Repo Mission Graph Visibility

### The Architecture

```
Mission Graph = Union of all repos' forensics/manifests/
  ├─ faerie-vault/forensics/manifests/
  │   └─ Past work, long-running investigations
  ├─ faerie2/forensics/manifests/
  │   └─ Current production work
  ├─ CT_VAULT/.../forensics/ (if created)
  │   └─ Concurrent investigations
  └─ Any future repo with forensics/ folder
      └─ Auto-discovered at startup
```

### Discovery Protocol

**Query Phase (Main):**
```bash
# List all investigations across ALL repos
python3 0x_mission_graph.py --query investigations --cross-repo

# Result:
# Active:
#   - treasury-cert-origins (faerie-vault, 12 manifests)
#   - sdk-readiness-mcp-deployment (faerie2, 3 manifests)
#   - vault-enhancement-2026-04-28 (CT_VAULT, 2 manifests)
# Candidates (awaiting validation):
#   - audio-ingest-free-models (faerie2, 1 manifest)
```

### Implementation: Federated Index

```python
class MissionGraphAggregator:
    def __init__(self):
        self.repos = [
            Path("/mnt/d/0local/gitrepos/faerie-vault"),
            Path("/mnt/d/0local/gitrepos/faerie2"),
            Path("/mnt/d/0LOCAL/CT_VAULT"),
            # Auto-discover from env: ADDITIONAL_FORENSICS_ROOTS
        ]
    
    def discover_investigations(self, status="active"):
        """Find all investigations across all repos, filter by status."""
        investigations = {}
        
        for repo in self.repos:
            manifests_dir = repo / "forensics" / "manifests"
            if not manifests_dir.exists():
                continue
            
            for manifest_file in manifests_dir.rglob("*.json"):
                m = json.loads(manifest_file.read_text())
                label = m.get("investigation_label", "uncategorized")
                
                if label not in investigations:
                    investigations[label] = {
                        "status": "candidate",  # default
                        "manifests": [],
                        "repos": []
                    }
                
                investigations[label]["manifests"].append(m)
                if repo not in investigations[label]["repos"]:
                    investigations[label]["repos"].append(str(repo))
        
        # Load validation registry (COC-tracked)
        registry = self._load_investigations_registry()
        for label, status in registry.items():
            if label in investigations:
                investigations[label]["status"] = status
        
        return {
            label: data for label, data in investigations.items()
            if data["status"] == status
        }
```

---

## Validation Registry (forensics/investigations-registry.json)

**Location:** Each repo has its own + aggregator reads all.

```json
{
  "treasury-cert-origins": {
    "status": "active",
    "validated_at": "2026-04-25T10:30:00Z",
    "validated_by": "main",
    "validation_criteria": {
      "coherence_score": 0.92,
      "manifest_count": 12,
      "compass_edges_present": ["N", "S", "E"],
      "agent_diversity": 4
    },
    "parent_investigation": null,
    "notes": "Tracking certificate origin discovery via DNS pivots"
  },
  "audio-ingest-free-models": {
    "status": "candidate",
    "manifests": 1,
    "validation_notes": "Awaiting 2+ more manifests to form coherent cluster"
  },
  "abandoned-old-project": {
    "status": "abandoned",
    "reason": "Merged into treasury-cert-origins",
    "merged_into": "treasury-cert-origins",
    "abandoned_at": "2026-04-24T15:00:00Z"
  }
}
```

**COC:** Edits logged via 0x_coc_writer.py. Immutable audit trail.

---

## Workflow: Unaffiliated → Earned Investigation

### Day 1: Agent Does Exploratory Work

```
Agent (researcher) starts investigation into certificate origins
  └─ Writes manifest: investigation_label: null (or "uncategorized")
     └─ forensics/manifests/2026-04-25/10-30-00Z_manifest_task-101_researcher_001.json
```

### Day 2: Agent Discovers Pattern

```
Agent (researcher) scans frontier, finds 2 more related manifests
  └─ Updates investigation_label: "treasury-cert-origins"
  └─ Documents evidence in dashboard_line:
     "Found coherent cluster: 3 manifests, shared DNS pivot precondition"
  └─ Manifest written with new label
```

### Day 3: Main Validates

```
Main reads mission graph:
  ├─ Sees "treasury-cert-origins" with 3 manifests
  ├─ Checks: same compass edges? agents complementary? coherence clear?
  ├─ Validates via investigation registry
  ├─ Stakes investigation: status="active"
  └─ /run --missions now discovers treasury-cert-origins as claimable
```

### Day 4+: Investigation Lives

```
Agents read manifests → see treasury-cert-origins is active
  ├─ Frontier scan prioritizes next_task_queued with matching label
  ├─ New agents join investigation autonomously (stigmergy)
  ├─ Investigation evolves, new preconditions discovered
  └─ Remains "active" as long as open edges exist
```

---

## Multi-Repo Coherence Example

**Investigation spans repos:**

```
treasury-cert-origins (ACTIVE, 12 manifests)
  ├─ faerie-vault (6 manifests)
  │   ├─ Initial discovery (2026-04-20)
  │   ├─ DNS pivoting (2026-04-22)
  │   └─ Blocker: certificate validation (N edge)
  │
  ├─ faerie2 (4 manifests)
  │   ├─ Picked up from frontier scan (2026-04-24)
  │   ├─ IP origin mapping (2026-04-25)
  │   └─ Certificate chain analysis (2026-04-26)
  │
  └─ CT_VAULT (2 manifests)
      ├─ Cross-validation from parallel team (2026-04-26)
      └─ Next: geographic distribution analysis (queued)

Query: 0x_mission_graph.py --query investigations --cross-repo
Result: treasury-cert-origins ACTIVE across 3 repos, 12 total manifests, 4 compass edges open
```

**Result:** Single coherent mission, physically distributed, discovered and managed by distributed agents.

---

## Earned vs. Arbitrary: The Difference

| Aspect | Arbitrary (Bad) | Earned (Good) |
|--------|-----------------|---------------|
| **Assignment** | "I'll call this 'my-project'" | Agent + frontier scan discovers pattern |
| **Validation** | None | Main validates coherence + registers |
| **Preconditions** | Assumed | Explicit (agent documents evidence) |
| **Blocker clarity** | Unclear | Compass edges (N/S/E/W) show dependencies |
| **Cross-repo visibility** | Fragmented | Mission graph sees all repos |
| **Agent discovery** | Manual routing | Autonomous via investigation_label + frontier scan |

---

## Implementation Roadmap

**Phase 1 (This Sprint):**
- ✅ Investigation registry schema (forensics/investigations-registry.json)
- ✅ Validation criteria (coherence_score, manifest_count, agent_diversity)
- ✅ Candidate → active workflow

**Phase 2 (Next Sprint):**
- 🚀 Cross-repo aggregator (0x_mission_graph.py --cross-repo)
- 🚀 Federated index (read all repos at startup)
- 🚀 ADDITIONAL_FORENSICS_ROOTS env var for discovery

**Phase 3 (Future):**
- 🔮 Investigation merge logic (consolidate spurious clusters)
- 🔮 Reputation impact (agents with high discovery accuracy get to propose new investigations)
- 🔮 Investigation graduation (candidate → active → mature → archive)

---

**Related:** [[00-DASHBOARD]], [[mcp-server-architecture]]  
**Ref:** faerie design: "Stigmergy-only" — no central queue, investigations emerge from local signals  
**Status:** Pending implementation in 0x_mission_graph.py

