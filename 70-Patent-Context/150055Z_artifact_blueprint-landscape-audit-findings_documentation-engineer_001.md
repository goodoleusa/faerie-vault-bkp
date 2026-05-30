---
type: findings
status: draft
created: 2026-04-28T15:00:55Z
investigation_label: vault-blueprints-standardization
phase: SEED
---

# Blueprint Landscape Audit — Phase 1 Findings Summary

## Task Status

| Aspect | Status |
|--------|--------|
| **Original Task** | `BLOCKED` |
| **Blockers** | Path inaccessibility (CT_VAULT/Blueprints/ not accessible) |
| **Reframe Applied** | YES — Phase 1 path discovery completed instead |
| **Full Audit Ready** | Awaiting CT_VAULT path accessibility |

---

## What We Learned

### 1. Blueprints ARE Used in Faerie Architecture

✓ **Confirmed:**
- Blueprints plugin (v0.6.0) is configured and active
- Templater plugin active (provides Nunjucks support)
- README explicitly documents blueprint usage in setup (line 920)
- QuickAdd provides blueprint-driven note creation

### 2. Architecture is Separated: Code ≠ Content

✓ **Discovered:**
- **faerie-vault** = Template/reference repository (this repo)
  - Contains: `.obsidian/` config, scripts, CLAUDE.md, setup docs
  - Does NOT contain: vault content folders (00-SHARED/, 20-Entities/, Blueprints/)
  
- **CT_VAULT** = Instantiated Obsidian vault instance
  - Contains: Actual vault content + blueprints
  - Location: `/mnt/d/0LOCAL/CT_VAULT/` (currently inaccessible)

### 3. Expected Blueprint Categories

Inferred from README and vault structure documentation:
- **Entity blueprints**: Person, Organization, Network, IP, Domain
- **Evidence blueprints**: File, Document, Finding, Photo
- **Analysis blueprints**: Task, Report, Intelligence, Analysis
- **Utility blueprints**: Droplet (insight capsule), Template, Configuration

### 4. Blueprint Technology Stack

| Component | Purpose |
|-----------|---------|
| **Blueprint plugin** | Core templating system |
| **Templater** | Nunjucks syntax (`{{ var }}`, `{% if %}`, `{% for %}`) |
| **Dataview** | Frontmatter queries for template selection |
| **QuickAdd** | Keyboard shortcuts + macro system for instantiation |

### 5. Common Variable Patterns

Likely to be inconsistent across blueprints:
- Timestamp: `{{ timestamp }}` vs `{{ created_at }}` vs `{{ date }}`
- Author: `{{ author }}` vs `{{ agent_type }}`
- Content: `{{ content }}` vs `{{ body }}`
- Type: `{{ type }}` vs `{{ doc_type }}`
- Status: `{{ status }}` vs `{{ state }}`

---

## What Blocked the Original Task

**Root Cause:** Path `/mnt/d/0LOCAL/CT_VAULT/` is not accessible from faerie-vault context

**Diagnostic Evidence:**
- faerie-vault is at `/mnt/d/0local/gitrepos/` (lowercase 0local)
- CT_VAULT referenced at `/mnt/d/0LOCAL/` (uppercase 0LOCAL)
- Path case difference suggests different filesystem mounts
- Swarmy is designed for air-gapped collaboration → vault likely on different machine

**Why It Matters:**
- Cannot list `/mnt/d/0LOCAL/CT_VAULT/Blueprints/` directory
- Cannot discover `.blueprint` files
- Cannot analyze blueprint completeness, drift, or usage
- Cannot validate Nunjucks syntax

---

## What Phase 2 Would Deliver (Once Path is Accessible)

### Blueprint Inventory
```
Blueprints discovered: X total
├─ Stubs (frontmatter only): Y
├─ Partial (some sections): Z
└─ Full (complete templates): W

Completeness breakdown:
  - Stubs (0-20 lines): Y items
  - Partial (20-60 lines): Z items
  - Full (60+ lines): W items
```

### Drift Analysis
```
Variable inconsistencies found: N
├─ Timestamp format variants: timestamp, created_at, date, …
├─ Author field variants: author, agent_type, creator, …
├─ Status field variants: status, state, workflow, …
└─ Custom section patterns: Inconsistent use of {% section %} vs # Markdown

Drift severity: HIGH | MEDIUM | LOW
```

### Usage Analysis
```
Blueprints referenced in vault: M total
Blueprints with 0 references (orphaned): O
  - Likely candidates for consolidation or removal

Most-used blueprints:
  1. Entity-Person (used 45 times)
  2. Task (used 32 times)
  3. Evidence (used 28 times)
  …
```

### Near-Duplicates
```
Blueprint pairs with >80% similarity: P
├─ Pair 1: Entity-Person.blueprint ↔ Entity-User.blueprint (87% match)
├─ Pair 2: Task.blueprint ↔ Task-Audit.blueprint (85% match)
└─ Recommendation: Consolidate; keep newer, deprecate older
```

### Nunjucks Validation
```
Blueprints checked: X
├─ Valid syntax: X - Q items
├─ Parsing errors: Q items
│  └─ Unclosed tags: R items
│  └─ Broken filters: S items
└─ Validation quality: (X - Q) / X = T%
```

---

## Why This Matters

**Impact on Vault Quality:**
- If blueprints drift, new notes will be inconsistent
- Orphaned blueprints clutter the system
- Near-duplicates confuse users creating stubs
- Nunjucks errors break note instantiation

**Impact on Agent Operations:**
- Inconsistent variable names break agent parsing
- Agents reading blueprints will see conflicting schemas
- Cannot reliably extract frontmatter fields
- Investigation_label field may be inconsistent

**Impact on Templates:**
- QuickAdd macros may not work with all blueprints
- Dataview queries may fail on inconsistent frontmatter
- Make.md clustering may not recognize related blueprints

---

## Path Resolution Checklist

To enable Phase 2, confirm:

- [ ] CT_VAULT location is documented in faerie-vault setup
- [ ] Mount point or symlink exists at `/mnt/d/0LOCAL/CT_VAULT/`
- [ ] Blueprints directory exists: `/mnt/d/0LOCAL/CT_VAULT/Blueprints/`
- [ ] At least 3 `.blueprint` files discoverable
- [ ] Read access confirmed (test with `ls -la`)

---

## Next Steps

**Immediate (now):**
- This Phase 1 report documents findings and blocks
- Awaiting path resolution from infrastructure team

**When CT_VAULT is accessible:**
1. Run Phase 2 full blueprint landscape audit
2. Deliver inventory of all blueprints with completeness ratings
3. Map drift patterns and consolidation candidates
4. Flag orphans and near-duplicates
5. Validate Nunjucks syntax across all templates

**Output:**
- Comprehensive blueprint-landscape.json inventory
- Drift analysis with severity ratings
- Consolidation recommendations
- Variable standardization guide
- Nunjucks validation report

---

## Files Generated

- **Manifest:** `forensics/manifests/2026-04-28/150035Z_manifest_blueprint-landscape-audit_documentation-engineer_001.json`
- **Phase 1 Report:** `forensics/artifacts/2026-04-28/150045Z_artifact_blueprint-landscape-audit-phase1_documentation-engineer_001.md`
- **This Summary:** `forensics/artifacts/2026-04-28/150055Z_artifact_blueprint-landscape-audit-findings_documentation-engineer_001.md`

---

**Status:** Phase 1 Complete  
**Blocker:** Path accessibility (external to agent control)  
**Phase 2 Trigger:** CT_VAULT/Blueprints/ accessibility confirmed  
**Updated:** 2026-04-28 15:00:55Z
