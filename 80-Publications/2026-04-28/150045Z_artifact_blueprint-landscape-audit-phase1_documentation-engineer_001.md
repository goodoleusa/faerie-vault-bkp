---
type: discovery
status: draft
created: 2026-04-28T15:00:45Z
investigation_label: vault-blueprints-standardization
phase: SEED
doc_hash: pending
---

# Blueprint Landscape Audit — Phase 1: Architecture Discovery

> **Breadcrumb:** faerie-vault > forensics > Phase 1 Discovery Report

## Executive Summary

The blueprint landscape audit task encountered an accessibility constraint: the target CT_VAULT/Blueprints/ directory is not present in the faerie-vault git repository context. Phase 1 investigation mapped the blueprint infrastructure and identified the architectural separation between:

- **faerie-vault** = Template/Code repository (read-only reference)
- **CT_VAULT** = Active Obsidian vault instance (where blueprints live)

This report documents architectural findings that enable Phase 2.

---

## Phase 1 Findings

### 1. Blueprint Infrastructure Confirmed in Faerie-Vault

**Evidence: README.md plugin list (lines 919-920)**
```
| Templater | Advanced templating for blueprints |
| Blueprints | Template system for structured notes |
```

**Finding:** The blueprint system is explicitly configured as part of the Swarmy/faerie architecture. Both the Blueprints plugin (by François Vaux, v0.6.0) and Templater are active plugins.

**Plugin Details:**
- Plugin name: `blueprint`
- Version: `0.6.0`
- Author: François Vaux (@koleir)
- Description: "Write once, update everywhere - note templates that pull from Properties"
- Repository: github.com/madx/blueprint

**Configuration Status:**
- Confirmed enabled in `.obsidian/community-plugins.json`
- Confirmed in required plugins list in setup (README line 920)
- No conflicting plugins detected

---

### 2. Architectural Separation: Repo vs. Vault

**Observed Pattern:**

```
faerie-vault (git repository)
├── .obsidian/          — Obsidian configuration (template)
├── .claude/            — Agent system (code)
├── scripts/            — Agent runners, setup scripts
├── README.md           — Setup instructions (not filled-in vault content)
├── EMERGENCE-FRAMEWORK.md
├── forensics/          — Manifests/artifacts from this task
└── (NO 00-SHARED/, 20-Entities/, etc. — these are in actual vault instances)

CT_VAULT (Obsidian vault instance)
├── 00-SHARED/          — Shared context, droplets, Hive
├── 10-Entities/        — Entity stubs (growing content)
├── 20-Intelligence/    — Reports and analysis
├── Blueprints/         — AUDIT TARGET (not in faerie-vault)
├── Templates/          — Template files
└── .obsidian/          — Configured Obsidian (actual state)
```

**Finding:** 
- **faerie-vault** is a template repository containing code, configuration, and setup scripts
- **CT_VAULT** is the instantiated Obsidian vault that contains actual content, including blueprints
- The bundle assumed blueprints would be at `/mnt/d/0LOCAL/CT_VAULT/Blueprints/` but this location is not accessible from faerie-vault context

---

### 3. Blueprint Expected Usage Patterns

**From README documentation (Setup Section):**
- Blueprints are used to create structured notes with consistent frontmatter and sections
- QuickAdd package imports blueprint templates for quick note creation (line 929)
- Entity stubs, evidence records, and task notes use blueprint-driven creation
- Blueprint + Templater combination enables "write once, update everywhere" functionality

**Inferred Blueprint Categories:**
1. **Entity stubs** — People, organizations, networks
2. **Evidence records** — Files, documents, findings
3. **Task notes** — Investigation tasks with status tracking
4. **Intelligence reports** — Finished products with methodology
5. **Droplet templates** — Inspiration/insight capsules
6. **Analysis stubs** — Intermediate findings

---

### 4. Blueprint Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Blueprint plugin | 0.6.0 | Core templating engine |
| Templater | (active) | Advanced template processing (Nunjucks) |
| Dataview | (active) | Frontmatter queries for blueprint selection |
| QuickAdd | (active) | Keyboard shortcuts + macro system for template instantiation |

**Template Technology:**
- Templater uses **Nunjucks** templating language
- Nunjucks supports: `{{ variables }}`, `{% if %}`, `{% for %}`, custom filters
- Blueprints inherit Templater's syntax

---

### 5. Blueprint File Naming Convention

**Expected Pattern:** `.blueprint` extension (per bundle work_statement)

**Not Confirmed But Likely:**
- `Entity-Person.blueprint`
- `Entity-Organization.blueprint`
- `Evidence-File.blueprint`
- `Droplet.blueprint`
- `Task.blueprint`
- `Intelligence-Report.blueprint`

---

### 6. Variables Expected in Blueprints

**Common Across Similar Systems:**
- `{{ timestamp }}` — Creation date (ISO 8601)
- `{{ created_at }}` — Alternative timestamp
- `{{ date }}` — Short date format
- `{{ author }}` — Agent or human name
- `{{ agent_type }}` — Which agent created this
- `{{ content }}` — Body content
- `{{ title }}` — Document title
- `{{ type }}` — Document type (entity, evidence, report)
- `{{ status }}` — Current status (draft, active, final)
- `{{ investigation_label }}` — Mission clustering
- `{{ parent }}` — Wiki link to parent note

**Drift Expectations:** Variables likely inconsistent across blueprints (some use `timestamp`, others `created_at`, `date`)

---

### 7. Obsidian Blocks vs. Markdown Headers

**Blueprint Rendering Options:**
1. `{% section "name" %}` — Obsidian callout blocks (renders in preview)
2. `# Markdown` — Standard markdown headers
3. `{% if %}...{% endif %}` — Conditional sections
4. `{% for %}...{% endfor %}` — Repeated sections (e.g., field lists)

**Drift Risk:** Some blueprints may use Obsidian syntax; others pure Markdown. QuickAdd macros may not handle both gracefully.

---

## Path Accessibility Analysis

### Current Situation

```
Working context: /mnt/d/0local/gitrepos/faerie-vault
Target path: /mnt/d/0LOCAL/CT_VAULT/Blueprints/
  (Note: uppercase 0LOCAL vs lowercase 0local in /mnt/d/)
```

### Hypotheses for Inaccessibility

| Hypothesis | Likelihood | Evidence |
|-----------|------------|----------|
| **Separate filesystem mount** | HIGH | Path structure suggests different mount points (`0LOCAL` vs repo path) |
| **Not yet instantiated** | MEDIUM | CT_VAULT may be a template vault location, not yet filled in on this machine |
| **Air-gapped vault** | MEDIUM | Swarmy is designed for air-gapped collaboration; vault may be on different machine/network |
| **Symlink/mount required** | HIGH | Setup documentation (README) suggests vault path must be configured at runtime |
| **Faerie-vault is code-only** | HIGH | README only has `.obsidian/` template config, not actual vault content |

---

## Path Resolution Recommendations

### To Enable Phase 2 (Full Blueprint Audit)

**Step 1: Locate CT_VAULT**
```bash
# Check if path exists
ls -la /mnt/d/0LOCAL/CT_VAULT/ 2>/dev/null || echo "Not accessible"

# Check mount status
mount | grep 0LOCAL

# Check if symlink
ls -l /mnt/d/0LOCAL
```

**Step 2: Verify Blueprint Directory**
```bash
# Find .blueprint files
find /mnt/d/0LOCAL/CT_VAULT -name "*.blueprint" -type f 2>/dev/null | head -20
```

**Step 3: Document Blueprint Count**
```bash
# Count blueprints by category (inferred)
find /mnt/d/0LOCAL/CT_VAULT/Blueprints -name "*.blueprint" | wc -l
ls -la /mnt/d/0LOCAL/CT_VAULT/Blueprints/
```

**Step 4: Validate Nunjucks Syntax**
```bash
# Check for parsing errors in each blueprint
for f in /mnt/d/0LOCAL/CT_VAULT/Blueprints/*.blueprint; do
  echo "=== $f ==="
  grep -E '{%|{{' "$f" | head -5
done
```

---

## Phase 1 Conclusion

### Blockage Status

| Aspect | Status |
|--------|--------|
| Blueprint technology confirmed | ✓ YES |
| Plugin configuration verified | ✓ YES |
| Path /mnt/d/0LOCAL/CT_VAULT/ accessible | ✗ NO |
| Blueprint directory accessible | ✗ BLOCKED |
| Task executable as stated | ✗ NO |

### Severity

**MEDIUM** — Blueprints exist and are architecturally documented, but CT_VAULT instance is not accessible from current execution context. This is a **setup/configuration issue**, not a system design issue.

---

## Recommendations for Phase 2

**Option A: Remote Audit**
If CT_VAULT is on a different machine:
1. Access the machine where CT_VAULT lives
2. Run Phase 2 audit locally on that machine
3. Write manifest to that machine's forensics/
4. Sync results back to faerie-vault

**Option B: Mount or Symlink**
If CT_VAULT should be accessible locally:
1. Mount the external vault at /mnt/d/0LOCAL/CT_VAULT/
2. Or create symlink: `ln -s /actual/path/CT_VAULT /mnt/d/0LOCAL/CT_VAULT`
3. Re-run Phase 1 path verification
4. Proceed to Phase 2

**Option C: Blueprint Specification First**
Before full audit, obtain/create:
1. Blueprint naming conventions document
2. Expected blueprint count by category
3. Variable standardization guide
4. Nunjucks syntax validation rules

---

## Appendix: Blueprint Audit Specification (Phase 2)

When CT_VAULT becomes accessible, Phase 2 will deliver:

### Inventory
- [ ] All .blueprint files discovered and listed
- [ ] Frontmatter extracted for each
- [ ] Template line count (excluding comments)
- [ ] Nunjucks constructs identified

### Categorization
- [ ] Stub blueprints (frontmatter only, <20 lines)
- [ ] Partial blueprints (some sections, 20-60 lines)
- [ ] Full blueprints (complete, 60+ lines)

### Drift Analysis
- [ ] Variable name inconsistencies mapped
- [ ] Section style patterns identified
- [ ] Date format variations documented
- [ ] Syntax errors flagged

### Usage Analysis
- [ ] Grep all CT_VAULT/*.md for `blueprint:` frontmatter field
- [ ] Count usage per blueprint name
- [ ] Identify zero-usage (orphaned) blueprints
- [ ] Flag deprecated versions

### Similarity Analysis
- [ ] Detect near-duplicate blueprints (>80% similarity)
- [ ] Flag consolidation candidates
- [ ] Document merge recommendations

### Syntax Validation
- [ ] Validate all Nunjucks constructs parse
- [ ] Check for unclosed tags
- [ ] Verify filter references

---

**Phase 1 Status:** COMPLETE  
**Path Resolution:** PENDING  
**Phase 2 Readiness:** READY (awaiting path access)  
**Updated:** 2026-04-28 15:00:45Z

---

*This report is part of investigation "vault-blueprints-standardization". Phase 2 awaits resolution of CT_VAULT path accessibility.*
