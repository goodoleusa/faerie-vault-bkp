# Streaming & Citation Discipline — Quality Standards

**Quick summary:** Agents must emit findings in real-time (streaming) and cite every source. This enables cross-session visibility, quality scoring, and trustworthy multi-agent chains.

---

## Why This Matters

| Problem | Solution | Impact |
|---------|----------|--------|
| Quality scoring only 11% accurate | Mandatory source citations | Enable 100% citation_accuracy_rate |
| Other sessions can't see agent progress | Real-time streaming to manifests | Enable cross-session discovery |
| No audit trail of decisions | Stream + MEM blocks at each step | Enable forensic verification |
| Findings can't be evaluated by eval-harness | Citation data in streams | Enable evalbot measurement |

---

## Rule 1: Streaming (MANDATORY)

**Every agent MUST emit findings in real-time** using `memory_bridge.py --stream`.

### Protocol

```bash
python3 /mnt/d/0LOCAL/.claude/scripts/memory_bridge.py \
  --stream --task {TASK_ID} --agent {AGENT_TYPE} \
  --emit {finding|droplet|decision|progress|summary} "{message}"
```

### Cadence

- **Minimum:** 5-20 entries per run
- **Timing:** Emit immediately after discovery (before filtering or reasoning)
- **Spacing:** Roughly every 15-30 seconds during active work
- **Bad patterns:**
  - 1 entry/run = understreaming (agent not sharing)
  - 100+ entries/run = overstreaming (summarize more)

### Emit Types

| Type | When | Example |
|------|------|---------|
| `finding` | Confirmed discovery with source | `[PRISMA-5.0] Owner identified in admin DB` |
| `droplet` | Intuition, pattern, connection | `This pattern reminds me of supply-chain compromise` |
| `decision` | Choice made with rationale | `Chose evidence-curator for tiering due to citation depth` |
| `progress` | Phase boundary reached | `Phase 1 complete: ingested 50K records` |
| `summary` | Final synthesis | `8 findings, 5 Tier-1, 0.95 confidence` |

### Fallback (if stream fails)

Write MEM blocks to `{repo}/.claude/memory/scratch-{SESSION_ID}.md`:
```
<!-- MEM agent=you ts={ISO} cat=FINDING pri=MED -->
**[FINDING]** [PRISMA-5.0] Owner identified in admin DB
{details}
<!-- /MEM -->
```

---

## Rule 2: Citation Discipline (MANDATORY)

**Every finding MUST cite its source.** Current baseline: 11% citation rate. Target: 100%.

### Citation Format

```
[source-id] Claim about what you found

Examples:
[PRISMA-MUSKOX-5.0] Edward Coristine (GitHub ID 76141700) appears in admin DB
[STAT-GOV-CERT-INFLECTION-019, p=6.54e-101] Cert traffic inflection confirmed
[RD-1017279346] NLRB whistleblower disclosed this access pattern
[wave2-python-pro-task-005-result.json] Prior agent confirmed ownership link
[HONEY.md sys00019] This follows the evolutionary selection pressure principle
```

### What Counts as Valid Source

- **File path + line:** `~file.md:42`
- **Database/extraction run:** `[PRISMA-RUN-name + score]`
- **Prior agent manifest:** `[wave-X-agent-type-result.json]`
- **NECTAR/HONEY entry:** `[HONEY.md sys00019]`
- **External document:** `[NPR article, 2025-01-20]`, `[LinkedIn post, @handle]`
- **Statistical result:** `[STAT-ID, p=value]`
- **Vault finding:** `[vault-path/finding-name.md]`

### In Streaming

```bash
python3 /mnt/d/0LOCAL/.claude/scripts/memory_bridge.py \
  --stream --task {TASK_ID} --agent {AGENT_TYPE} \
  --emit finding "[PRISMA-MUSKOX-5.0] Edward Coristine ownership confirmed"
```

### In Manifests

Include citation tallies:

```json
{
  "findings": 8,
  "citations_required": 8,
  "citations_provided": 8,
  "citation_accuracy_rate": 1.0,
  "sources_used": ["PRISMA-MUSKOX", "STAT-GOV-CERT", "NPR", "RD-1017279346"],
  "missing_citations": []
}
```

---

## Integration Checklist

Before returning your result manifest, verify:

- [ ] Streamed 5-20 findings via `memory_bridge.py --stream`
- [ ] Emitted AFTER discovery (not after filtering)
- [ ] Every finding has inline `[source-id]` citation
- [ ] Every citation references valid source (file:line, run-id, etc.)
- [ ] Manifest includes `citation_accuracy_rate: 1.0` (goal)
- [ ] MEM blocks written to scratch (fallback if stream fails)
- [ ] Manifest path is correct (canonical or fallback)

---

## Why This Works

### Streaming enables discovery
- Other agents see your findings in real-time
- Multi-agent chains can start work before all dependencies finish
- Cross-session visibility (Session B can read Session A's streams)

### Citations enable evaluation
- Evalbot can measure citation_accuracy_rate
- Findings can be verified (others can trace source)
- Chain of reasoning is auditable

### Together they enable scale
- Multi-session coordination: visible + trustworthy
- Quality scoring: measurable + fair
- Cross-investigation learning: reusable + verified

---

## Examples

### Bad (low quality)

```
Agent finding (no stream, no citation):
  "The data shows a pattern"
  
Manifest citation_accuracy: 0.0
(Evalbot can't score this — unknown source)
```

### Good (high quality)

```
Agent streams:
  memory_bridge.py --stream --task 001 --agent evidence-curator \
    --emit finding "[PRISMA-MUSKOX-5.0, conf=4.8/5.0] 29 VMs wiped at 2025-02-18T19:18:41"

Manifest reports:
  {
    "findings": 4,
    "citations_provided": 4,
    "citation_accuracy_rate": 1.0,
    "sources_used": ["PRISMA-MUSKOX", "STAT-H-RATIO-014", "HONEY.md sys00019"]
  }

(Evalbot can verify every claim, measure quality with confidence)
```

---

## Reference

- **SPAWN-BOILERPLATE.md** §3 (Streaming) — Full protocol in spawn prompts
- **SPAWN-BOILERPLATE.md** §3b (Citations) — Detailed citation discipline
- **memory_bridge.py** — Streaming implementation (`~/.claude/scripts/`)
- **ARCHITECTURE.md** §14 — Multi-session visibility (streaming enables it)
- **eval_harness.py** — Citation accuracy scoring (evalbot measures this)

---

**Last updated:** 2026-04-07  
**Status:** Rolling out immediately (affects all new spawns)  
**Target:** 100% citation rate by 2026-04-15
