---
type: reference
status: live
created: 2026-04-27
updated: 2026-04-27
tags: [template, frontmatter, compass, graph-visualization, vault-schema]
parent: ./README.md
doc_hash: sha256:pending
hash_ts: pending
hash_method: body-sha256-v1
---

> **Breadcrumb:** faerie-vault > COMPASS-FRONTMATTER-TEMPLATE

# Compass Frontmatter Template for Graph Visualization

Use this template to author documents that integrate with:
- **Obsidian graph view** (colored links by compass bearing)
- **COC scripts** (forensic hash tracking + integrity)
- **Breadcrumbs plugin** (visual navigation via custom relationships)
- **Excalibrain plugin** (frontmatter ontology visualization)

---

## Complete Frontmatter Schema

```yaml
---
# REQUIRED: Document identity and type
type: [manifest|artifact|droplet|narrative|analysis]
status: [pending|in_progress|completed|blocked]
created: 2026-04-27T14:23:00Z
updated: 2026-04-27T14:23:00Z

# REQUIRED: Compass bearing (phase routing signal)
# N = unblock prerequisites, S = proceed, E = parallel work, W = retreat/reframe
compass_edge: [N|S|E|W]

# REQUIRED: Mission clustering (stigmergic investigation label)
investigation_label: investigation-name-slug

# OPTIONAL: Quality signals (for graph node coloring)
quality_score: 0.85  # 0.0-1.0: data/output confidence
belief_index: 0.92   # 0.0-1.0: manifest truthfulness (agent self-honesty)

# OPTIONAL: Agent origin and forensic linkage
agent: agent-name
task_id: task-123    # Matches forensics/manifests/*_{task_id}_*

# REQUIRED: Next task routing (stigmergic breadcrumb for agents)
next_task_queued: "description of what agent should do next"

# OPTIONAL: Compass relationship links (Breadcrumbs plugin)
# These create colored edges in graph view (N/S/E/W bearing directions)
north:: [[prerequisite-task-id]]   # Blue edge: what's blocking this
south:: [[downstream-task-id]]     # Green edge: what this unblocks
east:: [[parallel-task-id]]        # Yellow edge: parallel validators
west:: [[alternative-task-id]]     # Red edge: retreat/reframe options
discovery:: [[discovering-agent]]  # Purple dashed: who found this work

# REQUIRED: COC chain integrity (forensic audit trail)
doc_hash: sha256:pending
hash_ts: pending
hash_method: body-sha256-v1

# OPTIONAL: Vault topology (for parent/child hierarchy)
parent: ../path/to/parent.md
sibling: ../path/to/sibling.md
child: ../path/to/child-1.md
down: ../path/to/descendant.md
up: ../path/to/ancestor.md
same: ../path/to/same-cluster.md

# OPTIONAL: Tags and keywords
tags: [mission-label, priority-level, domain-tag]
---
```

---

## Field Descriptions

### Document Identity
- **type**: Categorizes document role (manifest = agent outcome, artifact = work product, droplet = reusable insight, narrative = session summary, analysis = research finding)
- **status**: Workflow state (pending = queued, in_progress = active, completed = done, blocked = halted awaiting unblock)
- **created/updated**: ISO8601 timestamps (set once at creation, updated only when content changes)

### Compass Bearing (Graph Visualization)
- **compass_edge**: Routing signal for upstream agents
  - **N (North)**: Prerequisites unblock this work; show dependencies
  - **S (South)**: This work unblocks downstream; proceed/complete signal
  - **E (East)**: Parallel work running; needs validation/peer review
  - **W (West)**: Retreat/reframe signal; problem found, need alternative approach
  
### Mission Clustering
- **investigation_label**: Slug name for mission (e.g., "vault-consolidation", "emergence-framework"). Agents with same label self-organize into coherent teams. Graph clusters nodes by label.

### Quality Signals (Graph Node Styling)
- **quality_score**: Agent confidence in output (0.0–1.0)
  - 0.85+: Bright green node (trusted)
  - 0.50–0.85: Yellow node (developing)
  - <0.50: Red node (recovery/exploration)
  - NULL: Purple node (unassessed)

- **belief_index**: Manifest truthfulness (0.0–1.0). High = agent admits uncertainty, low = agent overstating confidence. **Higher belief = better** (anti-gaming incentive).
  - 0.75+: Solid opacity (trusted)
  - 0.50–0.75: Medium opacity
  - <0.50: Faint opacity (uncertain)

### Forensic Linkage
- **agent**: Agent name/ID that created this document
- **task_id**: Unique task identifier; must match filename in `forensics/manifests/{YYYY-MM-DD}/*_{task_id}_*`
- **next_task_queued**: Narrative description of the next work to be done (agents read this to discover follow-on tasks)

### Graph Relationships (Breadcrumbs Plugin)
Create colored edges in Obsidian graph by linking with compass bearing prefixes:

```yaml
north:: [[uuid-or-title]]    # Blue link: prerequisite/blocker
south:: [[uuid-or-title]]    # Green link: unblocks downstream
east:: [[uuid-or-title]]     # Yellow link: parallel work
west:: [[uuid-or-title]]     # Red link: alternative/retreat
discovery:: [[agent-name]]   # Purple dashed: discovered by agent
```

These appear as colored edges in the graph, enabling visual compass navigation.

### COC Chain (Forensic Integrity)
- **doc_hash**: SHA256 hash of file body content. Set to `sha256:pending` at creation; filled by `stamp_doc_hash.py` hook. Breaking this indicates content was mutated post-creation.
- **hash_ts**: Timestamp when hash was calculated (ISO8601)
- **hash_method**: Hashing algorithm (always `body-sha256-v1`)

---

## Example: Manifest (Agent Outcome)

```yaml
---
type: manifest
status: completed
created: 2026-04-27T14:23:00Z
updated: 2026-04-27T15:10:00Z
compass_edge: S
investigation_label: vault-consolidation
quality_score: 0.89
belief_index: 0.91
agent: code-reviewer
task_id: vault-consolidation-001
next_task_queued: "Verify plugin configs were synced correctly to faerie-vault; test Obsidian graph with Breadcrumbs + Excalibrain"

north:: [[vault-consolidation-000]]
south:: [[vault-consolidation-002]]
east:: [[obsidian-config-verify]]
discovery:: [[faerie-vault-sync-agent]]

doc_hash: sha256:pending
hash_ts: pending
hash_method: body-sha256-v1

parent: ../Hive.md
tags: [vault, emergence, plugin-audit]
---

> **Breadcrumb:** Vault > Hive > Manifests > vault-consolidation-001

# Vault Consolidation: Plugin Audit & Config Sync

**Dashboard:** Removed obsidian42-brat phantom entry; verified 10 plugins; synced .obsidian configs to faerie-vault. Ready for graph visualization testing.

## What Was Done

1. Audited 19 community plugins in CT_VAULT
2. Identified obsidian42-brat as phantom (no plugin files)
3. Removed entry from community-plugins.json
4. Copied 7 essential configs + 10 plugin manifests to faerie-vault
5. Updated .gitignore to exclude node_modules in plugins

## Quality Assessment

- **Citation accuracy:** 1.0 (all findings verified)
- **Completeness:** All 10 working plugins accounted for
- **Cross-repo sync:** faerie-vault now has matching .obsidian configs

## Blockers Encountered

None. All recommendations from vault audit were implementable.

## Next: Test graph visualization

Template is ready. Need to:
- Activate compass-graph.css snippet
- Test Breadcrumbs + Excalibrain with sample manifests
- Verify graph link colors match compass bearings
```

---

## Example: Droplet (Reusable Insight)

```yaml
---
type: droplet
status: live
created: 2026-04-27T10:00:00Z
updated: 2026-04-27T10:00:00Z
compass_edge: E
investigation_label: emergence-framework
quality_score: 0.95
belief_index: 0.88
agent: research-analyst
task_id: droplet-reputation-system
next_task_queued: "Apply reputation system insight to agent scoring and task routing"

east:: [[agent-evolution-001]]
east:: [[agent-evolution-002]]

doc_hash: sha256:pending
hash_ts: pending
hash_method: body-sha256-v1

tags: [droplet, reputation, anti-gaming, incentive-design]
---

> **Breadcrumb:** Vault > Droplets > LIVE-2026-04-27

# Reputation System Flips Anti-Gaming Wisdom

**Essence:** Honest agents thrive; lying agents starve. Manifest truthfulness is measured and visible. Honesty is more profitable than hiding failure.

**Key insight:** Traditional perf systems reward high scores, punishing failure → agents hide failures. faerie2 inverts this: agents caught lying drop in score → get constrained to retraining → work starvation. Honest failure = fast recovery.

**Where to apply:** Agent dispatch, task routing, natural selection mechanics.
```

---

## Integration with Existing Scripts

### Linter Hook (Auto-Inject Frontmatter)
Existing `.obsidian/plugins/obsidian-linter/` config will:
- Enforce required fields (type, status, compass_edge, investigation_label)
- Auto-inject doc_hash: sha256:pending on new files
- Maintain consistent field order

### Hash Tracking (stamp_doc_hash.py)
Run after completion:
```bash
python3 ~/.claude/scripts/stamp_doc_hash.py --file path/to/document.md
```
This fills in `doc_hash`, `hash_ts`, and creates COC entry in `forensics/coc-entries/`.

### Graph Visualization Hook
Breadcrumbs plugin will auto-read `north::`, `south::`, `east::`, `west::`, `discovery::` prefixes and render as colored edges.

Excalibrain will auto-parse `quality_score`, `belief_index`, `investigation_label` frontmatter and render as node styling + clustering.

---

## Graph View Settings (Obsidian)

In Obsidian Settings > Graph:

```
Display:
  Arrows: ON (show bearing direction)
  Text: OFF (keep graph clean)
  
Physics:
  Repulsion: 80 (push compass directions apart)
  Attraction: 20 (pull same investigation_label together)
  Link distance: 40 (enough space for link colors to show)

Colors:
  Use CSS snippet: compass-graph.css
  Link colors auto-map from relationship type
  Node colors auto-map from quality_score
```

---

## Testing the Compass Graph

1. Create a few sample manifests with `compass_edge: N/S/E/W` and `investigation_label`
2. Add `north::|south::|east::|west::` links between them
3. Open graph view
4. Zoom in on a node
5. Look around: NORTH (blue) for blockers, SOUTH (green) for unblocks, EAST (yellow) for peers, WEST (red) for problems
6. You're inside the mission compass

---

**Template Status:** Live | Ready to use  
**Last Updated:** 2026-04-27  
**Integration:** Linter ✓ | Hash tracking ✓ | Graph ✓ | Breadcrumbs ✓ | Excalibrain ✓
