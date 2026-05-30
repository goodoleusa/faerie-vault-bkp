# ONBOARDING SUBSTRATE FOR NEW MODELS — Standardized Template

**Purpose:** Enable rapid integration of new model families (llama, mistral, qwen, dbrx, falcon, etc.) into Faerie2 without losing cultural context.

**When to use:** When adding a new model to the open-roster (outside Claude API). Fill out this template BEFORE the first spawn.

---

## 1. MODEL REGISTRATION

```yaml
---
model_family: "mistral"  # llama | mistral | qwen | dbrx | falcon | chatglm
model_name: "mistral-7b-instruct"
version: "v0.3"
context_window: 8192  # tokens
quantization: "int4"  # fp16 | int8 | int4 | gguf-q4_km
deployment: "ollama"  # ollama | vllm | tgi | replicate | huggingface
endpoint: "http://localhost:11434/api/generate"  # for ollama, vllm, TGI
huggingface_id: "mistralai/Mistral-7B-Instruct-v0.3"

# Reputation baseline (will be computed from first N tasks)
composite_score_initial: 0.50  # assume 0.5 until proven
belief_index_initial: 0.50

# Capabilities (what this model is good for)
specializations:
  - "text summarization"
  - "code generation (Python, SQL)"
  - "document analysis"
  - "question answering"
specializations_exclude:
  - "image analysis (no vision)"
  - "audio transcription"
  - "real-time reasoning (latency issues)"
---
```

**Storage location:** `~/.claude/agents/mistral-7b-instruct.md` (same as Claude agent cards)

---

## 2. FAERIE CONTEXT PROTOCOL

### 2a. Compass Navigation (Required)

Every prompt to this model includes:

```markdown
## COMPASS NAVIGATION PROTOCOL

You are operating in a **stigmergic multi-agent system**. You do not communicate directly with other agents. Instead, you:

1. **Read your starting bundle** (HONEY + NECTAR + pollen + task)
2. **Complete your assigned task** using the context provided
3. **Write your outcome as a manifest** (JSON, structured)
4. **Leave your manifest in the filesystem** (`forensics/manifests/YYYY-MM-DD/`)
5. **Other agents read manifests to discover next work**

### Compass Bearing (After Task Completion)

After finishing your task, decide on your **compass bearing** (which direction next work flows):

- **South (S)** — "Proceed downstream." Your output quality is high (≥0.7). Write `compass_edge: "S"` in manifest. Next agent can rely on your output.
- **North (N)** — "Blocked by prerequisites." Your work revealed missing input data or upstream blockers. Write `compass_edge: "N"` + describe the blocker in `next_task_queued`.
- **East (E)** — "Parallel work needed." Your output is good, but method is uncertain. Write `compass_edge: "E"` + suggest validation task.
- **West (W)** — "Retreat, reframe." Your approach failed or contradicted evidence. Write `compass_edge: "W"` + propose alternative.

**Key insight:** The compass edge IS your signal to the next agent. The filesystem IS your communication channel.
```

### 2b. Reputation Context (Required)

Model receives on startup:

```json
{
  "composite_score": 0.56,
  "belief_index": 0.62,
  "interpretation": "CAUTION. This model is recovering. You can claim MED/LOW phases only. Avoid HIGH/CRITICAL work. Your honesty signal is medium; validate claims with citations.",
  "how_to_improve": "Improve by: (1) admitting uncertainty, (2) citing sources, (3) writing accurate manifests."
}
```

**Model responsibility:** Read this header EVERY prompt. Decline HIGH/CRITICAL work if score < 0.5. Accept only work matching your reputation level.

### 2c. Manifest Schema (Required Output)

After task completion, model writes to:
```
{repo}/forensics/manifests/{YYYY-MM-DD}/
  {HH-MM-SS}Z_manifest_task-{task_id}_{model_name}_{counter}.json
```

**Template:**
```json
{
  "task_id": "investigate-ip-origins-123",
  "investigation_label": "treasury-cert-origins",
  "dashboard_line": "Resolved 47 IP registrations → 12 unique ASNs; 3 state-owned networks detected.",
  "phase": "EXTEND",
  "quality_score": 0.78,
  "belief_index": 0.71,
  "compass_edge": "S",
  "next_task_queued": null,
  "discovered_work": {
    "found": false,
    "work_items": []
  },
  "artifacts_written": [
    "forensics/artifacts/2026-04-28/02-15-33Z_artifact_ip-asn-mapping_mistral_001.json"
  ],
  "timestamp": "2026-04-28T14:30:15Z",
  "model_name": "mistral-7b-instruct",
  "composite_score_at_start": 0.56,
  "composite_score_at_end": 0.58
}
```

**Quality score:** Self-assessment (0.0–1.0). How confident are you in the output?
- 0.9–1.0 = Highly confident, verified, citations included
- 0.7–0.9 = Confident, few gaps
- 0.5–0.7 = Moderate confidence, some uncertainty
- <0.5 = Low confidence, significant gaps

**Belief index:** Honesty self-assessment. Four signals averaged:
1. **Manifest truthfulness:** Does your dashboard_line match your actual output? (Be honest here.)
2. **Error admission:** Did you admit uncertainty or claim false certainty?
3. **Citation accuracy:** Did you cite sources accurately?
4. **Outcome alignment:** Did you deliver what you promised in the original task?

Score calculation: `belief_index = mean([signal1, signal2, signal3, signal4])` where each is 0.0–1.0.

### 2d. Bundle Reading (Required Input)

Your prompt contains:

```markdown
## CONTEXT BUNDLE — [investigation_label]

### HONEY (Crystallized Universal Facts)
[~2K tokens of global knowledge: system principles, tool descriptions, command syntax]

### PROJECT HONEY (Repo-Scoped Facts)
[~800 tokens of domain-specific knowledge: case background, evidence types, known actors]

### NECTAR (Recent HIGH Findings)
[Last 20 findings tagged pri=HIGH: patterns, insights, emerging threats]

### POLLEN (Live Session Observations)
[Raw MEM blocks from current session: unrefined observations, hypotheses]

### PRIOR MANIFESTS (Same Investigation Label)
[Last 5 manifests from agents working on same investigation_label]
[Gives you context: what has already been done? What gaps remain?]

---

## YOUR TASK
[Your specific assignment]

## CONSTRAINTS
- You are operating at composite_score={your_score}; claim work at that difficulty level
- Investigation label: {label}. Prefer work in this cluster if you discover multiple options.
- Return a manifest JSON to {repo}/forensics/manifests/{date}/. Include dashboard_line, compass_edge, discovered_work.
```

**Model responsibility:** Read all five layers BEFORE executing the task. Understand the context depth. Don't hallucinate; if something isn't in HONEY/NECTAR/pollen, say so.

---

## 3. TESTING CHECKLIST

### 3a. Unit Tests (per-model, before production)

```bash
# Test 1: Bundle reading
python3 -c "
import json
prompt = '''...model prompt with embedded bundle...'''
assert 'HONEY' in prompt, 'HONEY missing'
assert 'NECTAR' in prompt, 'NECTAR missing'
print('✅ Bundle structure OK')
"

# Test 2: Manifest writing
curl -X POST http://localhost:11434/api/generate \
  -d '{\"model\": \"mistral-7b-instruct\", \"prompt\": \"Write a JSON manifest with task_id, dashboard_line, compass_edge, next_task_queued\"}' \
  | python3 -m json.tool  # Validate JSON

# Test 3: Reputation awareness
# Send prompt with composite_score: 0.35, expect model to decline HIGH work

# Test 4: Compass navigation
# Send task, expect compass_edge (S|N|E|W) in manifest output

# Test 5: Investigation label clustering
# Send two tasks with same investigation_label, expect model to discover prior work in manifests
```

### 3b. Integration Tests (multi-task, before team dispatch)

- [ ] Model reads 4-task investigation without hallucinating missing context
- [ ] Model writes valid JSON manifest (schema validation passes)
- [ ] Model identifies next_task_queued correctly (read compass edges from prior manifests)
- [ ] Model discovers related work via frontier scan (if 40%+ context remains)
- [ ] Model respects reputation gate (declines HIGH if score <0.5)
- [ ] Manifest readable by downstream agents (JSON parseable, <5KB)
- [ ] Quality score and belief index are honest (spot-check: do outputs justify the scores?)

### 3c. Production Readiness

- [ ] Register model in ~/.claude/agents/ (create agent card .md)
- [ ] Add to reputation tracking system (reputation service subscribed to manifests)
- [ ] Test single spawn via /spawn skill (run 1 task, verify manifest output)
- [ ] Test team dispatch (4-agent team with this model + 3 others; verify coordination)
- [ ] Measure FFMx (force per token, cost per outcome) — compare to baseline
- [ ] Monitor composite_score drift over first 10 tasks (expect to stabilize)
- [ ] Monitor belief_index stability (should not drop >0.3 points per task)

---

## 4. CULTURAL COMPATIBILITY AUDIT

### Questions to Answer (Self-Assess)

**Q1: Can this model read Markdown with embedded JSON?**
- Expected: YES. If model struggles with JSON, add explicit JSON block delimiters: `\`\`\`json ... \`\`\``.

**Q2: Can this model write valid JSON manifests without hallucinating fields?**
- Expected: YES. Test on 5 sample manifests. If >20% parse failures, add JSON schema to prompt.

**Q3: Can this model understand compass bearings (N/S/E/W) as abstract routing signals?**
- Expected: YES. If model confuses compass with geography, add example: "South (downstream) = 'my output is good, other agents can rely on it'."

**Q4: Can this model respect reputation gates (decline HIGH work if score <0.5)?**
- Expected: YES. If model ignores score, add enforcement: "You MUST not attempt HIGH work if composite_score < 0.5. Return: `\"error\": \"reputation gate: cannot claim HIGH work\"` in manifest."

**Q5: Can this model discover related work via investigation_label clustering?**
- Expected: YES (requires reading prior manifests in same label). If model misses connections, add reminder: "Read `discovered_work` field in prior manifests; that's where hidden dependencies live."

### Red Flags (Model NOT Ready)

- [ ] Model hallucinates JSON fields or writes unparseable JSON (>10% error rate)
- [ ] Model ignores reputation gates (attempts HIGH work at score 0.3)
- [ ] Model confuses compass edges (writes "North = go to next task" instead of "North = blocked")
- [ ] Model has latency >30s per task (breaks async dispatch model)
- [ ] Model drops context (forgets parts of HONEY/NECTAR/pollen mid-task)

---

## 5. DEPLOYMENT CHECKLIST

### Pre-Deployment (Week 1)

- [ ] Fill out Section 1 (model registration YAML)
- [ ] Complete Section 3 (run all tests, pass >95%)
- [ ] Complete Section 4 (cultural audit, no red flags)
- [ ] Create ~/.claude/agents/{model_name}.md (agent card with maps_to_official_type)
- [ ] Commit registration to git: `git add ~/.claude/agents/{model_name}.md && git commit -m "Register model family: {model_family}"`

### Deployment (Week 2)

- [ ] Configure reputation service to track this model (add to scoring table)
- [ ] Test single spawn: `/spawn mistral-7b "Sample task" --investigation-label test-mistral`
- [ ] Verify manifest output appears in forensics/manifests/
- [ ] Run 3 sample tasks, spot-check manifests for honesty
- [ ] Measure response latency (expect <30s per task)

### Production (Week 3+)

- [ ] Add to team rosters (declare in spawn templates)
- [ ] Monitor composite_score daily (should stabilize by task 10)
- [ ] Monitor belief_index drift (watch for degradation)
- [ ] Compare FFMx to baseline (Claude haiku as benchmark)
- [ ] Document any cultural gaps discovered (for Section 6 report)

---

## 6. EXAMPLE: Mistral-7B Integration

**Timeline:** 3 days to deploy

**Registration (Day 1):**
```yaml
model_family: "mistral"
model_name: "mistral-7b-instruct"
deployment: "ollama"
endpoint: "http://localhost:11434/api/generate"
specializations:
  - "text summarization"
  - "code analysis"
  - "document review"
specializations_exclude:
  - "image/vision"
  - "audio transcription"
```

**Testing (Day 1–2):**
- Write unit test script: `test_mistral_bundle_reading.py` (checks HONEY/NECTAR in prompt)
- Write manifest schema validator: `validate_manifest.py`
- Run 5 sample tasks, validate manifests
- Result: 100% manifest success rate, avg quality_score 0.68, belief_index 0.71

**Deployment (Day 3):**
```bash
git add ~/.claude/agents/mistral-7b-instruct.md
git commit -m "Register model: mistral-7b-instruct (mistral family) — reputation init 0.50"

# Add to reputation service
python3 .claude/adapters/reputation-service.py --register mistral-7b-instruct

# Test single spawn
/spawn mistral-7b "Analyze code quality in repository" --investigation-label test-mistral

# Verify
ls forensics/manifests/2026-04-28/ | grep mistral
```

**Monitoring:**
```bash
# Daily: Check drift
python3 .claude/adapters/reputation-summary.py --model mistral-7b-instruct

# Weekly: FFMx comparison
python3 .claude/adapters/ffmx-benchmark.py --model mistral-7b-instruct --vs haiku
```

---

## 7. GLOSSARY: Faerie-Specific Terms

| Term | Definition | Example |
|------|-----------|---------|
| **Investigation Label** | String that clusters related work. All tasks with same label = same mission. | `treasury-cert-origins` |
| **Compass Edge** | Routing signal (N/S/E/W) indicating next work direction. | `S` = proceed, `N` = blocked upstream |
| **Manifest** | JSON output from agent task. Contains dashboard_line, compass_edge, discovered_work. | See 2c template |
| **Composite Score** | 0.0–1.0 reputation rating. Determines work difficulty (HIGH/MED/LOW). | 0.72 = healthy, claim HIGH work |
| **Belief Index** | 0.0–1.0 honesty self-assessment. High = agent admits uncertainty. | 0.68 = moderate honesty |
| **Dashboard Line** | ≤80 char summary of task outcome. Read by main context switchboard. | "Resolved 47 IPs → 12 ASNs" |
| **HONEY** | Crystallized universal facts (system principles, syntax, procedures). | "Compass bearings: N/S/E/W route work" |
| **NECTAR** | Recent HIGH findings (last 20 marked pri=HIGH). Evolves per-session. | "New ASN pattern detected in IPs" |
| **Pollen** | Raw session observations (unrefined MEM blocks from agents). | "Agent flagged suspicious timing" |
| **Discovered Work** | Unblocking tasks found during frontier scan. Appended to manifest. | `{"found": true, "work_items": [...]}` |
| **Frontier Scan** | Search for unclaimed tasks in forensics/ matching investigation_label. | "Found 3 north-blocked tasks in same mission" |

---

## 8. CONTACT & FEEDBACK

**Questions:** Refer to `docs/SPAWN-CARD-PROTOCOL.md` and `docs/AGENT-DISCOVERY-PROTOCOL.md` in repo.

**Report issues:** Create forensic artifact in `forensics/artifacts/{date}/` with tag `model-integration-issue`.

**Success metrics:** Monitor composite_score growth (should improve 0.01–0.05 per 10 tasks) and FFMx efficiency (target: >2.0× cost baseline).

---

**Template Version:** 2.0.0  
**Last Updated:** 2026-04-28  
**Status:** Production-ready
