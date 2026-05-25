# Plugin Migration Guide — Faerie as Distributable Extension

**Date:** 2026-04-22  
**Status:** Future-ready (not yet needed, but migration is zero-cost)  
**Trigger:** When faerie reaches production stability + team wants version-locked releases  

---

## TL;DR: Why & When

**Current state (optimal now):** Faerie is a skill (`~/.claude/skills/faerie/`). Skills provide instant feedback, no reload needed, perfect for iteration.

**Future state (when ready):** Faerie becomes a plugin (`.claude-plugin/plugin.json` manifest). Plugins enable version control, semantic releases, marketplace distribution.

**Migration cost:** Zero breaking changes. Same code, new structure. One-time 1-hour refactoring.

**Triggers for migration:**
- Team wants version-locked releases (v1.0.0, v2.0.0)
- Multiple teams depend on faerie (want to share via marketplace)
- Need tight control over plugin dependencies (MCP servers, custom agents)
- Want to distribute via GitHub releases or Claude Code marketplace

**Triggers to stay as skill:**
- Solo use, personal projects
- Rapid iteration (don't want release cycles)
- Lightweight footprint preferred

---

## Hybrid Recommendation (Now + Future)

Keep skill for entry (`/faerie`), use plugin structure for internal distribution (team Git repos).

This gives you:
- **Now:** Instant iteration (skill, no reload needed)
- **Later:** Marketplace-ready (plugin structure, semantic versioning)
- **Always:** No breaking changes (same BODY.md logic)

---

## Migration Path (When Needed)

### Step 1: Create Plugin Manifest

Create `.claude-plugin/plugin.json` at the top of faerie2 repo:

```json
{
  "name": "faerie-orchestrator",
  "display_name": "Faerie Orchestrator",
  "description": "Multi-wave orchestration system for complex Claude tasks. Coordinates specialized agents, manages evaluation feedback, and routes work based on performance metrics.",
  "version": "2.0.0",
  "version_date": "2026-04-22",
  "author": {
    "name": "Persistech Research",
    "email": "research@persistech.ai"
  },
  "homepage": "https://github.com/persistech/faerie2",
  "repository": "https://github.com/persistech/faerie2",
  "license": "Apache-2.0",
  "claude_code_minimum_version": "1.15.0",
  
  "skills": [
    {
      "id": "faerie-main",
      "name": "faerie",
      "display_name": "Faerie Orchestrator",
      "path": "skills/faerie/SKILL.md"
    }
  ],
  
  "agents": [
    {
      "id": "workflow-orchestrator",
      "name": "workflow-orchestrator",
      "description": "Main orchestrator for faerie waves",
      "path": "agents/workflow-orchestrator.md"
    }
  ],
  
  "hooks": [
    {
      "type": "PreToolUse",
      "tool": "Agent",
      "script": "hooks/8x_faerie_gates.py"
    },
    {
      "type": "PostToolUse",
      "script": "hooks/8x_hook_runner.py"
    }
  ],
  
  "settings": {
    "piston_mode": {
      "type": "enum",
      "default": "balanced",
      "options": ["balanced", "momentum", "unblock", "deep"],
      "description": "Wave assignment strategy for queue analysis"
    },
    "model_routing": {
      "type": "boolean",
      "default": true,
      "description": "Enable multi-provider model routing (OpenRouter + Claude)"
    },
    "eval_isolation": {
      "type": "boolean",
      "default": true,
      "description": "Keep free model evals separate from Claude benchmarks"
    }
  },
  
  "dependencies": {
    "queue_ops": "~1.0.0",
    "eval_harness": "~2.0.0"
  },
  
  "keywords": [
    "orchestration",
    "agents",
    "evaluation",
    "cost-optimization",
    "multi-provider"
  ]
}
```

### Step 2: Move Files into Plugin Structure

```bash
# Current structure (skill-based)
~/.claude/skills/faerie/
  SKILL.md
  BODY.md

# Future structure (plugin-based)
faerie-plugin/
  .claude-plugin/
    plugin.json              ← manifest
  skills/
    faerie/
      SKILL.md               ← unchanged
      BODY.md                ← unchanged
  agents/
    workflow-orchestrator.md ← custom agent (if needed)
  hooks/
    8x_faerie_gates.py       ← pre-flight checks
    8x_hook_runner.py        ← hook dispatch
  scripts/
    piston_orchestrator.py
    9x_piston_model_router.py
    7x_spawn_template.py
    [etc.]
  docs/
    SPAWN-BUNDLE-F0-OPTIMIZATION.md
    OPENROUTER-INTEGRATION.md
    [etc.]
  templates/
    spawn-templates/         ← copy from ~/.claude/spawn-templates/
  README.md
  LICENSE
```

### Step 3: No Code Changes Required

The SKILL.md and BODY.md remain **identical**. Only the directory structure changes.

```bash
# Plugin version can be invoked as:
/faerie:faerie-orchestrator  # namespaced (plugin invocation)
# Or still as:
/faerie                       # if registered as primary skill
```

### Step 4: Version Management

Update `plugin.json` version on releases:

```bash
# Git workflow
git tag v2.0.0
git push origin v2.0.0

# Claude Code will detect version via plugin.json
# Users can /plugin install faerie-orchestrator@2.0.0
```

### Step 5: Marketplace Registration (Optional)

When ready to share:

1. **Create release notes** (changelog format):
   ```markdown
   # v2.0.0 — Multi-Provider Model Routing
   
   - Added OpenRouter integration for free model tiers
   - Implemented wave-specific model selection (W1→free, W2→Claude)
   - Isolated eval scores by model tier (no cross-contamination)
   - Added cost dashboard for faerie cycles
   ```

2. **Submit to marketplace:**
   - Visit Claude Code Marketplace
   - Sign in with GitHub
   - Create plugin listing (description, tags, logo)
   - Point to GitHub release URL
   - Marketplace auto-detects plugin.json

3. **Users install via:**
   ```
   /plugin install faerie-orchestrator
   # or specific version
   /plugin install faerie-orchestrator@2.0.0
   ```

---

## Backward Compatibility During Migration

### Phase 1: Skill + Plugin Co-Exist
Maintain both during transition:

```bash
~/.claude/skills/faerie/        # Original (skill-based)
faerie-plugin/                  # New (plugin-based)
```

Users can choose:
- `/faerie` → uses skill version
- `/faerie:faerie-orchestrator` → uses plugin version

### Phase 2: Plugin as Primary, Skill as Fallback
Move to plugin, keep skill as fallback:

```bash
~/.claude/skills/faerie/        # Deprecated, points to plugin
faerie-plugin/                  # Primary
```

### Phase 3: Plugin Only (Full Migration)
Remove skill, plugin is authoritative:

```bash
faerie-plugin/                  # Single source of truth
```

---

## Integration Points (What Changes)

| Component | Now (Skill) | After (Plugin) | Impact |
|---|---|---|---|
| **Entry point** | `/faerie` skill | `/faerie:faerie-orchestrator` plugin | Users may need to update shortcuts |
| **Config location** | `~/.claude/settings.json` | `plugin.json` settings section | Migrated automatically |
| **Hook registration** | `.claude/hooks/` manifest | Plugin hooks section | Cleaner, no manual registration |
| **Agent types** | `~/.claude/agents/` | `agents/` in plugin + `~/.claude/agents/` | Can combine sources |
| **Scripts** | Global ~/.claude/scripts/ | Plugin scripts/ + global | Plugin bundled = offline-capable |
| **Distribution** | Git clone or symlink | GitHub release or marketplace | Versioned, easier sharing |

---

## Settings Consolidation Example

**Before (skill-based, scattered):**
```
~/.claude/settings.json (some)
faerie2/.claude/spawn-boilerplate.md (some)
~/.claude/hooks/state/piston-checkpoint.json (some)
```

**After (plugin-based, unified):**
```
.claude-plugin/plugin.json (all declarative)
  ├─ settings section (piston_mode, model_routing)
  ├─ hooks section (event handlers)
  └─ agents section (custom agent types)
```

---

## Debugging During Migration

### Test plugin locally:
```bash
claude code --plugin-dir ./faerie-plugin/ /faerie
# Should behave identically to skill version
```

### Rollback if needed:
```bash
# Keep skill version in ~/.claude/skills/faerie/
# Just remove plugin from --plugin-dir
# /faerie continues to work from skill
```

---

## Timeline Estimate

| Phase | Effort | Timeline |
|---|---|---|
| 1. Create plugin.json manifest | 15 min | Week 1 |
| 2. Move files (no code changes) | 30 min | Week 1 |
| 3. Test locally with --plugin-dir | 30 min | Week 1 |
| 4. Maintain dual versions (skill + plugin) | 5 min/release | Ongoing |
| 5. Marketplace registration | 1 hour | When ready |
| **Total effort to market-ready** | **~2 hours** | **1–2 weeks** |

---

## Skill vs Plugin Checklist

**Stay as skill if:**
- [ ] Solo use, no sharing intent
- [ ] Rapid iteration (don't want release cycles)
- [ ] Lightweight preferred (no plugin overhead)

**Migrate to plugin if:**
- [ ] Team wants version-locked releases
- [ ] Multiple projects depend on faerie
- [ ] Want semantic versioning (v1.0.0, v2.0.0)
- [ ] Plan to share via marketplace eventually
- [ ] Need custom MCP servers or agents bundled

---

## References

- [Claude Code Plugin Architecture](https://code.claude.com/docs/plugins)
- [Semantic Versioning](https://semver.org/)
- [Claude Code Marketplace](https://claude.ai/plugins)
- Current faerie structure: `~/.claude/skills/faerie/SKILL.md`

---

**Status:** Migration plan ready, zero-cost path documented  
**Action:** Review when distribution becomes priority  
**Effort:** 1–2 hours one-time migration work
