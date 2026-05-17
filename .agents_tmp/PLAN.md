# 1. OBJECTIVE

Create and implement three interconnected systems:

**A. PRISM Theme Integration**  
Integrate the existing pistachio/mermaid/light pastel + jewel tone + Obsidian palette as a proper PRISM-supported theme with natural CSS extensions for Obsidian Style Settings.

**B. Vault Crystallization System — The Real Honey**  
Build a self-crystallizing system where the most IMPORTANT outputs get preserved and made visible:
- **Larger synthesis docs** — comprehensive explanations of what metrics MEAN
- **Narrative docs** — story-driven explanations connecting the dots
- **Novel discoveries** — things never seen before
- **Publication-worthy insights** — equations, frameworks, reusable patterns
- **Visualizations** — mission graph views, agent insight maps, connection diagrams
- Moving forward: all high-value outputs auto-route through crystallization pathway

**C. Inbox Entry Point with Auto-Routing**  
Create a single "raw inbox" entry point that:
- Receives all unorganized/uncategorized files
- Auto-classifies them by document type and blueprint
- Prioritizes routing of synthesis/narrative/discovery docs to crystallization mission

# 2. CONTEXT SUMMARY

**Existing Theme Assets:**  
- `00-SHARED/Hive/Color/02-vaporwave-jewel.css` — Full theme with Mermaid styling, light/dark variants
- `00-SHARED/Hive/Color/theme-palette-lab.css` — Prism extension layer (investigation callouts, tags, kanban, dashboards)

**Existing Blueprints (from `/Blueprints/`):**
- `Crystallization-Candidate.blueprint` — Evaluation criteria for what becomes permanent (3+ sessions, cross-agent, human review, eval impact)
- `Task-Inbox.blueprint` — Task structure with `vault_path: "00-Inbox/tasks/"`
- `Dead-Drop.blueprint` — Async comms, routes to `00-Inbox/drops/`
- `Observer-Drop.blueprint` — Offline review with chain signature
- `Daily-Research.blueprint` — Daily research log structure

**Existing Inbox Structure:**  
- `00-SHARED/00-Inbox/vault/` — Main inbox with subfolders: `10-Examples/`, `20-Missions/` (swarm), `30-Dashboards/`, `40-Roster-Routing/`, `99-Vault-Meta/`

**Dependencies:**  
- Obsidian with Blueprints plugin, Templater plugin, Style Settings plugin  
- CLI hooks referenced (e.g., `drops.py`, `note_sign.py` in Dead-Drop)

# 3. APPROACH OVERVIEW

**A. PRISM Theme Integration:**  
1. Create `00-SHARED/Hive/Color/PRISM-theme.css` as the master theme import that combines both CSS files
2. Add Prism-compatible variable mappings so Style Settings can control all palette colors
3. Verify integration with existing Obsidian theme system

**B. Vault Crystallization System:**  
1. Create a "Crystallization **Mission**" (swarm staging) at `00-Inbox/mission-crystallization/` for evaluating candidates
2. Create automation that identifies potential crystallizable content (recurring patterns, cross-agent usage)
3. Build workflow: Discovery → Candidate → Gauntlet Review → Crystallized (HONEY.md or AGENTS.md)

**C. Auto-Routing Inbox:**  
1. Create `00-Inbox/00-Raw-Entry/` as the single entry point for all new files
2. Create routing rules based on frontmatter `type:` or filename patterns
3. Build a presend hook or automation that auto-classifies and routes files to their destinations

# 4. IMPLEMENTATION STEPS

## Phase A: PRISM Theme Integration (A1–A4)

### A1. Create Prism Custom Accent Snippet
- **Goal:** Integrate vaporwave jewel tones into Prism Theme via Style Settings custom accent
- **Method:** Create CSS snippet that overrides Prism accent variables with custom colors:
  - `--accent-hue`: 170 (shift from default for teal)
  - `--accent-saturation`: 65%
  - `--accent-custom-color`: #4ECDC4 (mermaid teal)
  - `--accent2-custom-color`: #6B3FA0 (purple)
  - `--accent3-custom-color`: #E85D75 (rose)
- **Reference:** Your existing `02-vaporwave-jewel.css` lines 1–14

### A2. Extend Prism Light Scheme (Pistachio Base)
- **Goal:** Leverage Prism's built-in "Pistachio" scheme with custom extensions
- **Method:** Create snippet extending `.theme-light` with your light pastel variables:
  - `--lab-page-bg`: #f5f7f2 (warm off-white)
  - `--lab-h1-color`: #2D1B69 (deep purple)
  - `--lab-h1-underline`: #4ECDC4 (teal)
  - `--lab-sidebar-bg`: #eef3eb (light pistachio)
- **Reference:** Your existing `02-vaporwave-jewel.css` lines 17–77

### A3. Extend Prism Dark Scheme (Pine/Jewel Base)
- **Goal:** Use Prism's "Pine" dark scheme and extend with jewel tones
- **Method:** Create snippet extending `.theme-dark`:
  - `--lab-page-bg`: #0F0B1A (near-black purple)
  - `--lab-h1-color`: #93C572 (pistachio titles)
  - `--lab-card-bg`: #1A1428 (dark purple card)
  - Jewel accents: teal #4ECDC4, purple #6B3FA0, rose #E85D75
- **Reference:** Your existing `02-vaporwave-jewel.css` lines 83–143

### A4. Add Mermaid Integration for Prism
- **Goal:** Make your existing Mermaid styling work with Prism
- **Method:** Combine with your `theme-palette-lab.css` Mermaid sections
- **Reference:** `theme-palette-lab.css` lines 255–376

---

## Phase B: Vault Crystallization System (B1–B5)

### B1. Create Crystallization Mission Folder
- **Goal:** Establish staging area for candidates awaiting evaluation (swarm staging, not a queue)
- **Method:** Create `00-SHARED/00-Inbox/mission-crystallization/`
- **Reference:** `Crystallization-Candidate.blueprint`

### B2. Create Crystallization Candidate Template
- **Goal:** Auto-generate candidate files from discovered patterns
- **Method:** Create Templater template based on Crystallization-Candidate blueprint
- **Reference:** `Blueprints/Crystallization-Candidate.blueprint`

### B2b. Prioritize High-Value Outputs for Crystallization
- **Goal:** Ensure synthesis/narrative/discovery docs route to crystallization, not lost in task completions
- **Method:** Add routing priority for document types that represent REAL honey:
  | If doc type is... | Priority | Route to... |
  |---|---|---|
  | synthesis | **HIGH** | `mission-crystallization/` |
  | narrative | **HIGH** | `mission-crystallization/` |
  | discovery | **HIGH** | `mission-crystallization/` |
  | insight | **HIGH** | `mission-crystallization/` |
  | equation | **HIGH** | `mission-crystallization/` |
  | visualization | **HIGH** | `mission-crystallization/` |
  | task | LOW | tasks/ |
- **Why:** Task completions are the vehicle — insights that help human THINK are the honey

### B3. Create "Gauntlet" Evaluation Automation
- **Goal:** Automated check for crystallization criteria
- **Method:** Create script that scans vault and checks:
  - Appeared in 3+ distinct sessions (check `created:` timestamps)
  - Cited by ≥2 distinct agent types (check `agent_author:` or similar)
  - Human review completed (check `confirmed on:` field)
- **Reference:** `Crystallization-Candidate.blueprint` lines 30–52

### B4. Define Crystallization Destinations — Where the Honey Lives
- **Goal:** Establish where the REAL high-value outputs go (not just task completions)
- **Method:** Create dedicated synthesis/narrative destinations:
  - `00-SHARED/HONEY-synthesis/` — Large synthesis docs explaining what metrics MEAN
  - `00-SHARED/HONEY-narratives/` — Story-driven explanation docs
  - `00-SHARED/HONEY-discoveries/` — Novel discoveries, publication-worthy insights
  - `00-SHARED/HONEY-visions/` — Visualizations: mission graphs, agent insight maps, connection diagrams
  - `00-SHARED/AGENTS.md` — Cross-agent techniques (reference)
- **Why:** Task completions aren't the honey — the insights that help humans THINK are

### B5. Create Self-Crystallizing Workflow (Moving Forward)
- **Goal:** Moving forward, vault auto-evaluates and promotes HIGH-VALUE outputs (synthesis, narratives, discoveries, visualizations)
- **Method:** Create presend hook that:
  1. When synthesis/narrative/discovery/insight/equation/visualization doc completes → auto-route to **mission-crystallization/**
  2. Evaluate for crystallization criteria (novelty, human value, reusability)
  3. Route to appropriate HONEY- destination (synthesis/narrative/discoveries/visions)
  4. Task completions → standard task routing (NOT crystallization priority)

---

## Phase C: Auto-Routing Inbox System (C1–C5)

### C1. Create Raw Entry Point Folder
- **Goal:** Single landing zone for all uncategorized files
- **Method:** Create `00-SHARED/00-Inbox/00-Raw-Entry/`
- **Reference:** Existing `00-Inbox/vault/` structure

### C2. Define Routing Rules Matrix — HIGH Priority for Honey
- **Goal:** Map document types to destinations, PRIORITIZING the REAL honey
- **Method:** Create routing table with priority levels:
  | If type is... | Priority | Route to... |
  |---|---|---|
  | **synthesis** | **HIGH** | `mission-crystallization/` → HONEY-synthesis/ |
  | **narrative** | **HIGH** | `mission-crystallization/` → HONEY-narratives/ |
  | **discovery** | **HIGH** | `mission-crystallization/` → HONEY-discoveries/ |
  | **insight** | **HIGH** | `mission-crystallization/` → HONEY-discoveries/ |
  | **visualization** | **HIGH** | `mission-crystallization/` → HONEY-visions/ |
  | task | LOW | `00-Inbox/tasks/` |
  | dead-drop | LOW | `00-Inbox/drops/` |
  | daily | LOW | `00-Inbox/vault/daily/` |
  | *unknown* | FALLBACK | `99-Vault-Meta/` (flag for human review) |

### C3. Create Routing Automation Script
- **Goal:** Auto-classify and move files from Raw-Entry
- **Method:** Build Python script or Obsidian automation:
```python
# Pseudocode:
for file in Raw_Entry:
    type = parse_frontmatter(file, "type")
    dest = routing_table.get(type, "99-Vault-Meta/")
    move(file, dest)
```
- **Reference:** Dead-Drop blueprint routing section

### C4. Create Fallback Handler
- **Goal:** Handle files that don't match any routing rule
- **Method:** Route to `00-Inbox/vault/99-Vault-Meta/` with flag for human review

### C5. Document Daily Output Workflow
- **Goal:** Ensure daily outputs route through the system
- **Method:** Document that agents should output to daily folder, which then feeds into `00-Raw-Entry/` for routing

# 5. TESTING AND VALIDATION

**Theme Validation:**
- [ ] Enable Prism Theme in Obsidian, select "Pistachio" (light) / "Pine" (dark)
- [ ] Enable custom CSS snippet, verify jewel accents appear
- [ ] Toggle light/dark mode, verify both palettes render correctly
- [ ] Test Mermaid diagrams render with jewel-toned shapes

**Crystallization Validation:**
- [ ] Create test **synthesis doc** in `mission-crystallization/`, verify it routes to HONEY-synthesis/
- [ ] Create test **narrative doc**, verify routes to HONEY-narratives/
- [ ] Create test **discovery/insight**, verify routes to HONEY-discoveries/
- [ ] Create test **visualization**, verify routes to HONEY-visions/
- [ ] Run gauntlet evaluation, verify it checks all criteria (not just task completion)
- [ ] Human approve test candidate, verify it promoted to correct HONEY- destination
- [ ] Verify self-crystallizing trigger fires on synthesis/narrative/discovery types (not task completions)

**Auto-Routing Validation:**
- [ ] Drop test file in 00-Raw-Entry/ with `type: task`
- [ ] Run routing automation, verify file moved to correct destination
- [ ] Drop file with unknown type, verify fallback to 99-Vault-Meta/
- [ ] Verify daily output folder integrates with routing
