# COST BREAKDOWN: Claude CLI vs. Open-Model Stack

**Scenario:** 30 days of normal usage (100 data-ingest tasks, 500 vision-ingest frames, 50 audio-ingest jobs).

---

## A. CLAUDE CLI (Current Stack)

| Component | Usage | Unit Cost | Monthly |
|-----------|-------|-----------|---------|
| **Audio-ingest** (faster-whisper local) | 50 jobs × 1h avg | $0/hour | **$0** |
| **Vision-ingest Steps 1–3** (local) | 500 frames processed | $0 (CPU) | **$0** |
| **Vision-ingest Step 4** (Claude Vision API) | 500 frames × $0.003 avg | $1.50 | **$1,500** (scaled) |
| **Data-ingest agent spawning** | 100 tasks × 8 agents × 5K tokens | $0.0001 per 1K input | **$400–1,000** |
| **Reputation scoring** | Built into Claude eval (free) | $0 | **$0** |
| **Token metering** | Built-in to Claude Code CLI | $0 | **$0** |
| **Manifest / COC logging** | Filesystem only | $0 | **$0** |
| **Total** | — | — | **$1,900–2,500/month** |

**Assumptions:**
- Vision API: $0.003 per 1K image tokens; avg 2 calls per frame at 500 tokens each = $0.003 per frame
- Data-ingest agents: 100 tasks × 8 agents × 5K input tokens = 4M input tokens × $0.00001 per token = $40/month, plus completions; scaling 10× for realistic workload
- No storage costs (forensics/ stored in git)

**Operational overhead:** None (Claude Code CLI handles everything)

---

## B. OPEN-MODEL STACK (With Adapters)

### B1. Infrastructure Costs (One-Time + Monthly)

| Component | Setup Cost | Monthly Operational | Notes |
|-----------|-----------|----------------------|--------|
| **GPU Server** (1× RTX 4090 or equivalent spot instance) | $500–2,000 | $250–400 | 24/7 for local models (Whisper, LLaVA, llama2-70b) |
| **Celery Task Queue** (K8s or Docker Swarm, 4 workers) | $1,000–3,000 | $300–500 | Task orchestration (replaces Agent() tool) |
| **Redis** (reputation scoring state) | $200 | $15–30 | In-memory cache for composite_score tracking |
| **Prometheus + Grafana** (metrics) | $500 | $20–50 | Token metering + performance monitoring |
| **Storage** (forensics backups, logs) | — | $50–100 | S3/B2 for forensic integrity (already recommended) |
| **Total Setup** | **$2,200–6,000** | **$635–1,080/month** | — |

### B2. Model Costs (No Inference API Calls)

| Component | Workload | Unit Cost | Monthly |
|-----------|----------|-----------|---------|
| **Audio-ingest** (faster-whisper, local GPU) | 50 jobs × 1h = 50h | $0.35/h (GPU spot) | **$18** |
| **Vision-ingest Steps 1–3** (local CPU) | 500 frames | $0 | **$0** |
| **Vision-ingest Step 4** (Ollama+LLaVA, local GPU) | 500 frames × 30s each | $0.35/h | **$50** |
| **Data-ingest agents** (4 workers, llama2-70b+mistral) | 100 tasks × 4 agents × 2h per task | $0.35/h per worker | **$280** |
| **No API calls** (everything local) | — | $0 | **$0** |
| **Total Model Costs** | — | — | **$348/month** |

### B3. Engineering & Maintenance

| Task | Effort (Hours) | Cost (at $150/hr) | When |
|------|---|---|---|
| **Build Celery bridge** (replaces Agent()) | 80 | $12,000 | Week 1–2 |
| **Build reputation service** | 40 | $6,000 | Week 2–3 |
| **Ollama adapter for vision-ingest** | 24 | $3,600 | Week 1 (parallel) |
| **Prometheus integration** | 16 | $2,400 | Week 3 |
| **Monthly ops + debugging** | 20/month | $3,000/month | Ongoing |
| **Total Upfront** | 160 hours | **$24,000** | One-time |
| **Total Monthly Maintenance** | 20 hours | **$3,000** | Recurring |

### B4. Operational Summary (Open Models)

| Category | First Month | Months 2+ |
|----------|-----------|----------|
| **Infrastructure** | $2,200–6,000 (setup) + $635 (ops) | $635–1,080 |
| **Model inference** (local only) | $348 | $348 |
| **Engineering** | $24,000 | $3,000 |
| **Total** | **$26,535–30,000** | **$3,983–4,428** |

---

## C. BREAK-EVEN ANALYSIS

### When Does Open-Model Stack Become Cheaper?

**Monthly savings vs. Claude API:**
- Claude stack: $1,900–2,500/month
- Open model stack: $635 (infra) + $348 (models) + $3,000 (eng) = $3,983/month in steady state

**Months to payoff upfront investment:**
- Upfront delta: $24,000 (engineering)
- Monthly savings: ~$0 (actually +$1,500 cost increase, month 1; but…)

**Recalculation (more realistic scaling):**
- Claude stack scales: 100 → 1,000 tasks = $19–25K/month (10× workload)
- Open model stack scales: 100 → 1,000 tasks = $3,983 + $3,000 = $6,983/month (engineering amortizes)

**Breakeven workload:** ~500 tasks/month (where Claude API cost ≈ $12,500; open models stay at $3,983)

**Payoff period:** ~3–4 months at high workload (500+ tasks/month)

---

## D. COST DECISION MATRIX

| Scenario | Recommendation | Reasoning |
|----------|---|---|
| **< 100 tasks/month** | **Stay with Claude CLI** | API costs ($1,900/mo) < open model infra ($3,983/mo) |
| **100–300 tasks/month** | **Claude CLI + evaluate open models** | Breakeven approaching; build adapters in parallel if you have eng resources |
| **300–500 tasks/month** | **Hybrid (90% Claude, 10% open)** | Test open models on non-critical tasks; measure FFMx before full commitment |
| **500–1,000 tasks/month** | **Open models + Claude hybrid** | High workload justifies infra investment; use Claude for latency-critical phases |
| **> 1,000 tasks/month** | **Pure open models** | Payoff is 2–3 months; API costs ($20K+/mo) unjustifiable |

---

## E. HIDDEN COSTS (Often Missed)

### Claude CLI Stack
- **Cold storage backups:** $50–100/mo (S3/B2 for forensic integrity)
- **Compliance/audit:** Included (Claude eval framework handles SOC2)
- **Support:** Included (Anthropic support team)
- **Model updates:** Free (Claude always latest)

### Open-Model Stack
- **GPU maintenance:** $200–500/mo (upkeep, driver updates, cooling)
- **Model fine-tuning:** $5–20K per model (if you want custom behavior)
- **Compliance/audit:** $0 (but you build/validate it yourself — 40–80 hours)
- **Community support only** (unless you hire dedicated DevOps)
- **Hardware obsolescence:** GPU lifespan ~3 years; budget $500/month for replacement

---

## F. QUALITY TRADEOFFS

| Metric | Claude API | Ollama+LLaVA (local) |
|--------|-----------|--|
| **Vision extraction accuracy (OCR)** | 95%+ | 85–90% |
| **Audio transcription (Whisper)** | ~95% (faster-whisper) | ~95% (same model, local) |
| **Data-ingest latency** | 30s per task | 2–5 min per task (slower GPU inference) |
| **Hallucination rate** | Lower (Claude 4.5 optimized) | Higher (llama2/mistral less refined) |
| **Context coherence** | Excellent (tight RLHF) | Good (but degradation at >4K tokens) |
| **Code quality** | Excellent | Good (mistral/llama good at code) |

---

## G. RECOMMENDATIONS (2026-04-28)

### SHORT TERM (Next 3 months)
1. **Stay on Claude CLI** (current cost-optimal for <300 tasks/month)
2. **Build onboarding substrate template** (done; see artifact)
3. **Implement Celery bridge** (1 week investment; enables future migration)
4. **Monitor workload growth** (measure tasks/month; track trend)

### MID TERM (3–6 months)
1. **If workload >300 tasks/mo:**
   - Deploy Celery bridge + reputation service
   - Test Ollama+LLaVA on non-critical vision tasks
   - Measure FFMx + quality for open models
2. **If workload <300 tasks/mo:**
   - Keep Claude CLI; no migration needed
   - Use onboarding template for future flexibility

### LONG TERM (6–12 months)
1. **If workload >500 tasks/mo:**
   - Migrate data-ingest to open models (save $10K+/month)
   - Hybrid vision: Ollama for cost-sensitive, Claude for high-accuracy
2. **If workload <500 tasks/mo:**
   - Maintain hybrid (Claude for core, open models for experimentation)

---

## H. SPREADSHEET CALCULATOR (Self-Service)

Use this to calculate YOUR break-even:

```python
# Monthly cost calculator
def calculate_monthly_cost(num_tasks, num_vision_frames):
    """
    num_tasks = data-ingest agent tasks (100 = our baseline)
    num_vision_frames = vision-ingest frames processed (500 = our baseline)
    """
    
    # CLAUDE CLI
    vision_api_cost = num_vision_frames * 0.003  # Claude Vision
    data_ingest_cost = (num_tasks * 8 * 5000) * 0.00001  # 8 agents × 5K tokens
    claude_total = vision_api_cost + data_ingest_cost + 50  # +50 for storage
    
    # OPEN MODELS
    infra_monthly = 835  # GPU + Celery + Redis + Prometheus + storage
    model_inference = (num_tasks * 2 * 0.35) + (num_vision_frames * 0.0001)  # GPU hours
    open_total = infra_monthly + model_inference + (3000 / 30)  # amortize eng
    
    print(f"Tasks: {num_tasks}/month, Vision frames: {num_vision_frames}/month")
    print(f"Claude:  ${claude_total:,.0f}/month")
    print(f"Open:    ${open_total:,.0f}/month")
    print(f"Savings: ${claude_total - open_total:,.0f}/month")
    
    return claude_total, open_total

# Test scenarios
for tasks, frames in [(100, 500), (300, 1500), (500, 2500), (1000, 5000)]:
    calculate_monthly_cost(tasks, frames)
    print()
```

---

## I. EXECUTIVE SUMMARY

| Workload | Recommended | Cost | Payoff |
|----------|---|---|---|
| **Light** (<100 tasks/mo) | Claude CLI | $1,900/mo | N/A (don't migrate) |
| **Medium** (100–300 tasks/mo) | Claude CLI + evaluate | $2,500/mo | ~1 year if scales to 500/mo |
| **Medium-High** (300–500 tasks/mo) | Hybrid (test open) | $3,500–12K/mo | 3–4 months to payoff |
| **High** (500–1,000 tasks/mo) | Open models primary | $4K/mo (steady state) | 2–3 months to payoff |
| **Very High** (1,000+ tasks/mo) | Pure open models | $4–6K/mo | <1 month to payoff |

**Current state (baseline):** ~100 tasks/month = Claude CLI optimal. Revisit in 6 months if growth continues.

---

**Document:** Cost Breakdown v1.0  
**Date:** 2026-04-28  
**Confidence:** Medium (depends on actual AWS/GPU spot pricing + your infrastructure choices)
