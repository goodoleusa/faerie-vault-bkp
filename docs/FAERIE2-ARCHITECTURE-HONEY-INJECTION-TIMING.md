# FAERIE2 Architecture: HONEY Injection at Spawn Time (Non-Negotiable Principle)

**Date:** 2026-04-29  
**Status:** CRITICAL ARCHITECTURAL PRINCIPLE  
**Applies to:** All bundle creation, all agent spawning, all context injection  

---

## Overview

FAERIE2 is an f(0) orchestration platform that minimizes main context burden through stigmergic coordination. A critical principle ensures context is fresh, bundles are discoverable, and subagents have zero orchestration dependencies:

**HONEY (crystallized knowledge) is injected at spawn time by main, NEVER at bundle creation time by subagents.**

This document explains why, how to implement it, enforcement mechanisms, and the full rationale.

---

## The Principle (Non-Negotiable)

### ❌ WRONG: HONEY Injected at Bundle Creation Time

```
Subagent discovers work
  ↓
/bundle skill (+ injects HONEY at bundle creation)
  ↓
Bundle created: {task_id, HONEY, NECTAR, ...} ← HEAVY, STALE
  ↓
Bundle sits in forensics/bundles/ for hours
  ↓
Main spawns agent with bundle (HONEY is stale by now)
  ↓
Agent receives outdated context
```

**Problems:**
1. **Token waste:** Bundles include HONEY for work never claimed
2. **Context rot:** HONEY created at T+10:00, used at T+11:00+ (stale facts, missed recent findings)
3. **Subagent complexity:** /bundle must read memory system (coupling, security concern)
4. **Bundle bloat:** Large JSON payloads slow discovery, sorting, filesystem operations
5. **Hard to discover:** Bundles aren't scannable; require full JSON parse per discovery

### ✅ RIGHT: HONEY Injected at Spawn Time by Main

```
Subagent discovers work
  ↓
/bundle skill (just facts: task_id, intent, priority, mission-label) ← THIN
  ↓
Bundle created: ~200 bytes of metadata
  ↓
Bundle sits in forensics/bundles/ (small, sortable, fast discovery)
  ↓
Main reads bundle + claims it
  ↓
Main injects HONEY + NECTAR at spawn time (FRESH context, right now)
  ↓
Agent receives: bundle + rich context assembled minutes ago
  ↓
Agent works with optimal signal
```

**Benefits:**
1. **Token efficiency:** Only claimed bundles pay HONEY cost
2. **Context freshness:** HONEY injected at spawn time (current, includes latest findings)
3. **Subagent autonomy:** /bundle has zero dependencies; calls no external systems
4. **Bundle discoverability:** Thin JSON, fast sorting, easy filesystem ops
5. **Centralized context control:** Main decides scope, freshness, filtering

---

## Why This Matters (Deep Rationale)

### Token Budget Impact

**Scenario:** 10 bundles created, 5 will be claimed within 2 hours, 5 will stale after 24 hours

**Cost if HONEY at bundle time:**
```
HONEY per bundle: ~1K tokens (full global + project crystallized facts)
  10 bundles × 1K = 10K tokens burned on creation
  Result: 5K tokens wasted (HONEY for bundles never claimed)
  Stale context: 1K tokens per claimed bundle (context rot)
  Total waste: ~5K tokens
```

**Cost if HONEY at spawn time:**
```
Bundle creation: ~50 tokens (just JSON validation + emit)
  10 bundles × 50 = 500 tokens
  HONEY injection at spawn: 5 bundles × 1K = 5K tokens
  Result: 0 wasted (only claimed bundles pay)
  Fresh context: HONEY current as of spawn time
  Total waste: 0 tokens
```

**Daily savings:** 5K–10K tokens × 365 days = $1.50–$3.00/day per active investigation

### Architectural Purity (Loose Coupling)

If `/bundle` touches HONEY:
- **Dependency:** /bundle needs CLAUDE_HOME + memory system access (couples to faerie infrastructure)
- **Coupling:** /bundle responsible for context freshness (temporal problem)
- **Fragility:** HONEY changes break /bundle (brittle contracts)
- **Complexity:** Subagents must understand scope filtering, HONEY schema
- **Security:** Who reads NECTAR/pollen? How are secrets protected?

If `/bundle` is dumb (just metadata):
- **Independence:** /bundle has zero external dependencies
- **Resilience:** HONEY changes don't touch /bundle
- **Simplicity:** /bundle just validates + emits JSON (testable, verifiable)
- **Security:** Subagents never read memory system
- **Correctness:** Main controls context quality + freshness

**Result:** Clean separation of concerns. Bundles are signal; HONEY injection is main's job.

### Context Freshness (Temporal Correctness)

Bundle created at 10:00 AM with HONEY snapshot:
```
HONEY at 10:00: "Latest evidence: IPs 1.2.3.0/24"
Bundle sits in forensics/bundles/ until 2:00 PM
Agent spawned at 2:00 PM reads bundle
Agent sees: "Latest evidence: IPs 1.2.3.0/24" (from 4 hours ago)
Meanwhile: NEW evidence found at 1:30 PM: "IPs 1.2.3.0/24 COMPROMISED"
Agent doesn't see the compromise → acts on stale info
```

Spawn-time injection:
```
Bundle created at 10:00: {task_id, intent}
Bundle sits in forensics/bundles/ until 2:00 PM
Agent spawned at 2:00 PM
Main injects HONEY + NECTAR at 2:00 PM (FRESH, includes 1:30 PM compromise)
Agent sees: "IPs COMPROMISED" (current info)
Agent acts on fresh facts
```

**Correctness requirement:** Context must be timely. Spawn-time injection guarantees freshness.

---

## Implementation Rules (Enforcement)

### What /bundle Does (Subagent-Side)

✅ **ALLOWED:**
- Validate schema (task_id, semantic_intent, priority, mission-label)
- Emit thin JSON to forensics/ephemeral/{task_id}/
- Promotion hook symlinks to forensics/bundles/{date}/
- Log to COC entry

❌ **FORBIDDEN:**
- Read HONEY or NECTAR files
- Inject any context
- Touch ~/.claude/ or global memory
- Assume HONEY presence
- Reference HONEY structure or schema

### What Main Does at Spawn Time (Main-Side)

✅ **ALWAYS DO:**
- Read bundle from forensics/bundles/{date}/
- Inject HONEY (scope-filtered by agent type/phase)
- Inject NECTAR (tail-50, mission-filtered)
- Inject project HONEY (repo-scoped facts)
- Inject recent manifests (prior findings, compass edges)
- Assemble final prompt with bundle + all context
- Call Agent(subagent_type=..., prompt=assembled_prompt)

❌ **NEVER DO:**
- Modify bundle JSON
- Cache bundle context (load fresh each spawn)
- Skip HONEY injection (mandatory)
- Assume bundle contains context (it shouldn't)

---

## Validation & Enforcement

### Validation Hook: Block HONEY in Bundles

Script: `scripts/0x_spawn_discipline_enforcer.py`

```python
def validate_bundle_creation(bundle_content):
    # Check: no HONEY references
    if "HONEY" in str(bundle_content) or "🍯" in str(bundle_content):
        raise ValueError("Bundle must not contain HONEY. Main injects at spawn time.")
    
    # Check: no context_injection field
    if "honey_scope" in bundle_content or "nectar" in bundle_content:
        raise ValueError("Bundle must be thin metadata only.")
    
    # Check: required fields present
    assert "task_id" in bundle_content
    assert "semantic_intent" in bundle_content
    assert "priority" in bundle_content
    # mission_label optional
```

**Result:** Bundles with HONEY fields are rejected. Violation logged to COC.

### Spawn Template: Enforce Context Injection

Script: `scripts/0x_spawn_template.py`

```python
def assemble_spawn_prompt(bundle_path, agent_type, scope="default"):
    bundle = load_bundle(bundle_path)
    
    # Inject context HERE (not in /bundle)
    honey = load_honey_scoped_by_agent(agent_type)
    nectar = load_nectar_tail_50(mission_label=bundle["mission_label"])
    manifests = load_recent_manifests_same_mission(bundle["mission_label"])
    
    # Assemble final prompt
    prompt = f"""
    ## HONEY (Crystallized Knowledge)
    {honey}
    
    ## NECTAR (Recent Findings)
    {nectar}
    
    ## Recent Manifests (Prior Work)
    {manifests}
    
    ## YOUR TASK
    Task ID: {bundle['task_id']}
    Intent: {bundle['semantic_intent']}
    Priority: {bundle['priority']}
    Mission: {bundle.get('mission_label', 'unassigned')}
    
    (Agent receives rich context assembled NOW)
    """
    
    return prompt
```

**Contract:** Every Agent() spawn MUST use `0x_spawn_template.py` output as prompt. Enforced by PreToolUse hook.

### COC Logging: Audit Violations

Every bundle creation logs: `"bundle_source: skill:bundle, honey_injected: false"`  
Every agent spawn logs: `"honey_injected: true, honey_scope: {agent_type}, nectar_lines: {N}"`

**If HONEY found in bundle:** Violation logged with full context (who, what, when, why).

---

## Common Mistakes (Anti-Patterns)

### Mistake 1: Injecting HONEY in /bundle

```python
# ❌ WRONG
def create_bundle(...):
    honey = load_honey()  # Anti-pattern!
    bundle = {
        "task_id": ...,
        "honey": honey  # ❌ WRONG
    }
    return bundle
```

**Why:** HONEY ages. Bundles sit unclaimed. Context is wasted.  
**Fix:** Remove HONEY from bundle. Main injects at spawn time.

### Mistake 2: Filtering HONEY at Bundle Time

```python
# ❌ WRONG
def create_bundle(phase=None):
    if phase:
        honey = load_honey_by_phase(phase)  # Anti-pattern!
```

**Why:** Subagent doesn't know phase. Main doesn't know when bundle is claimed. Filtering logic spread.  
**Fix:** Main decides filtering at spawn time based on agent type + task phase.

### Mistake 3: Caching Bundle Context

```python
# ❌ WRONG
BUNDLE_CACHE[task_id] = {
    "bundle": load_bundle(...),
    "honey": load_honey(...),  # Cache gets stale
}
# Use cached bundle hours later
```

**Why:** Cache doesn't expire. HONEY is outdated. Manifests missed.  
**Fix:** Always load fresh from disk at spawn time.

### Mistake 4: Agents Creating Their Own Bundles with HONEY

```python
# ❌ WRONG (agent spawning follow-up work)
def spawn_follow_up(...):
    honey = load_honey()
    bundle = {
        "task": ...,
        "honey": honey  # Anti-pattern!
    }
    Agent(prompt=bundle)  # ❌
```

**Why:** Agents shouldn't read HONEY. Cascades complexity.  
**Fix:** Agents create bundles with /bundle skill (thin metadata only). Main injects HONEY when claiming.

---

## Documentation Checklist (Enforcement)

This principle must appear in these locations:

- ✅ `faerie2/docs/ARCHITECTURE-HONEY-INJECTION-TIMING.md` (design doc)
- ✅ `faerie2/.claude/skills/bundle/BODY.md` (reminder section)
- ✅ `faerie2/scripts/0x_spawn_template.py` (docstring)
- ✅ `faerie2/settings.json` (hook comments)
- ✅ `faerie-vault/docs/FAERIE2-ARCHITECTURE-HONEY-INJECTION-TIMING.md` (this file)
- [ ] CT_VAULT design narrative (faerie2 architecture overview)
- [ ] FAERIE2 research paper / design doc
- [ ] Agent spawn protocol documentation (when agents themselves spawn follow-ups)

**Verification:** Grep for "HONEY injection" across all docs. Every design doc should reference this principle.

---

## Rationale: Why This Design Wins

| Aspect | If HONEY at Bundle Time | If HONEY at Spawn Time |
|--------|------------------------|-----------------------|
| **Token efficiency** | 5-10K wasted tokens/day (unclaimed bundles) | 0 wasted (only claimed bundles pay) |
| **Context freshness** | Stale (HONEY from hours ago) | Fresh (HONEY current as of spawn) |
| **Architectural coupling** | High (bundle depends on memory system) | Low (bundle is independent) |
| **Subagent complexity** | High (must read memory, understand scoping) | Low (just call /bundle, done) |
| **Bundle discoverability** | Hard (large JSON, slow sort) | Easy (thin metadata, fast filesystem ops) |
| **Context control** | Distributed (subagent + main) | Centralized (main only) |
| **Extensibility** | Brittle (HONEY changes break /bundle) | Robust (HONEY changes don't touch /bundle) |
| **Security** | Higher risk (subagents read memory) | Lower risk (main controls access) |
| **Failure modes** | Bundling fails → agent can't spawn | Injection fails → fallback to minimal context |

**Winner:** HONEY at spawn time. Clear dominance across all dimensions.

---

## Related Principles (Ecosystem)

This decision ties to:

1. **f(0) Principle:** Zero orchestration burden on main → thin bundles, fast discovery
2. **Subagent Autonomy:** Agents don't manage context → main does
3. **Stigmergy:** Bundles are pheromone trails (signal, not rich context)
4. **Mutation Discipline:** Changes to HONEY don't ripple through /bundle
5. **Compass Navigation:** Bundles carry mission_label; manifests carry compass edges
6. **Mission Self-Assembly:** Tasks cluster via mission_label; main's HONEY injection enriches context

---

## Sign-Off

**THIS IS A NON-NEGOTIABLE ARCHITECTURAL PRINCIPLE.**

Drift from this pattern is a mutation and must be caught + corrected via:

1. **Code Review:** Catch HONEY injection in /bundle or agent spawning
2. **Enforcement Hooks:** `8x_spawn_discipline_enforcer.py` blocks violating patterns
3. **Integration Tests:** Verify HONEY only appears at spawn time, never in bundles
4. **Documentation Audit:** Every design doc mentions principle; every spawn shows HONEY injection at spawn time

**If you find yourself about to move HONEY injection to bundle time:**

**STOP.** Ask yourself: "Why am I coupling subagents to the memory system? What complexity am I accepting?" Then read this document again.

**The answer is: Don't.** Keep bundles thin. Inject HONEY at spawn time. f(0) depends on it.

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-29  
**Status:** ENFORCED (mission-critical)
