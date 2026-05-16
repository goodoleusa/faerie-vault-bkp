---
type: publication
status: draft
title: Faerie2 Living Formula System — Architecture & Feedback Loops
mission: mission-formula-driven-pacing
tags: [formula-system, f0-constraint, living-formulas, pacing, ffmx, operational-math]
created: 2026-05-05
updated: 2026-05-05
doc_hash: "sha256:pending"
parent: "[[../80-Publications]]"
---

# Faerie2 Living Formula System

**North Star:** f(0) context burden ratio ≤ 5% (measured + enforced via constraint equation)

## 1. System Architecture: From Discrete Waves to Continuous Pacing

### OLD: Discrete Wave Thresholds
```mermaid
graph TD
    A["Context Fill %"] -->|≤70%| B["W1 LIFTOFF<br/>6 agents"]
    A -->|71-80%| C["W2 CRUISE<br/>4 agents"]
    A -->|81-87%| D["W3 INSERTION<br/>1 background"]
    A -->|≥93%| E["RED ALERT<br/>Compact now"]
    
    B --> F["Discrete jumps<br/>at thresholds"]
    C --> F
    D --> F
    
    style F fill:#ffcccc,stroke:#cc0000
    style A fill:#e1f5ff,stroke:#0277bd
```

**Problem:** Discontinuities at threshold boundaries. Human decides "is it time for W2?"

### NEW: Continuous Context Pressure Sigmoid
```mermaid
graph TD
    A["Context Fill %"] --> B["Context Pressure<br/>p(c) = 1/(1+e^(-k·(c-c_mid)))"]
    B --> C["Spawn Pressure Score<br/>0 to 1"]
    C -->|p=0.1| D["Low Pressure<br/>Conservative spawn"]
    C -->|p=0.5| E["Mid Pressure<br/>Normal spawn"]
    C -->|p=0.9| F["High Pressure<br/>Aggressive spawn"]
    D --> G["Formula decides<br/>No human stage gates"]
    E --> G
    F --> G
    
    style G fill:#ccffcc,stroke:#00cc00
    style C fill:#fff9c4,stroke:#f57f17
```

**Advantage:** Smooth curve, formula-driven, no discrete jumps. Main doesn't ask "when is W2?"—formula answers.

---

## 2. f(0) as Active Constraint: The Forcing Equation

### Measurement (Passive) vs Constraint (Active)

```
PASSIVE (Old):
  Measure f(0) each session
  Hope it's ≤5%
  Adjust next session if too high
  
ACTIVE (New):
  CONSTRAINT: f(0) ≤ 0.05 (hard limit)
  DERIVED: main_budget = total_budget × 0.05
  DECISION: Before spawn, check presend cost ≤ main_budget
  FEEDBACK: If presend > budget, compress bundle or parallelize
```

### The Forcing Equation

```
Given:
  B = total_session_tokens (e.g., 150,000)
  f(0)_target = 0.05 (5%)
  presend_estimate = estimated orchestration cost

Constraint:
  f(0) = main_tokens / B ≤ 0.05
  
Rearranged (enforcement):
  main_tokens ≤ B × 0.05
  main_tokens ≤ 150,000 × 0.05
  main_tokens ≤ 7,500

Decision Gate:
  IF presend_estimate ≤ 7,500:
    spawn normally
  ELSE:
    reduce bundle size OR increase agent_count
    re-estimate, check again
```

### f(0) Enforcement Loop (Mermaid)

```mermaid
graph TD
    A["Session Start<br/>Budget = B tokens"] --> B["Calculate Main Budget<br/>main_budget = B × 0.05"]
    B --> C["Estimate Presend Cost<br/>presend_estimate"]
    C --> D{{"presend<br/>≤<br/>main_budget?"}}
    
    D -->|YES| E["✓ Proceed with Spawn"]
    D -->|NO| F["Compress Bundle<br/>or<br/>Add Parallelism"]
    
    F --> G["Re-estimate Presend"]
    G --> D
    
    E --> H["Log: presend, main_budget,<br/>actual f(0) post-session"]
    H --> I["Weekly Feedback Loop<br/>Adjust formula parameters"]
    
    style D fill:#fff176,stroke:#f57f17
    style I fill:#a5d6a7,stroke:#388e3c
```

---

## 3. Compression Ratio Dominates FFMx: The Logarithmic Lever

```mermaid
graph LR
    A["FFMx Multiplier"] -->|"70% contribution"| B["Compression Ratio<br/>ln(M₀/Mf)"]
    A -->|"20% contribution"| C["Agent Quality"]
    A -->|"10% contribution"| D["Emergence Health"]
    
    B -->|"e.g., 2× compression<br/>adds ln2=0.69"| E["Compression is<br/>the dominant lever"]
    C --> F["Diminishing returns<br/>on quality improvement"]
    D --> F
    
    E --> G["Engineering focus:<br/>Reduce token burn<br/>not just agent skill"]
    
    style B fill:#ffccbc,stroke:#d84315
    style G fill:#e1bee7,stroke:#7b1fa2
```

---

## 4. Living Formula Feedback Loops

### Weekly f(0) Adjustment Loop

```mermaid
graph TD
    A["Session Data<br/>Last 7 days"] --> B["Calculate f(0) avg<br/>main_tokens / total_tokens"]
    B --> C{{"f(0)<br/>in bounds?"}}
    
    C -->|"f(0) < 0.02"| D["Can afford deeper<br/>main reasoning<br/>increase bundle layers"]
    C -->|"0.02 ≤ f(0) ≤ 0.05"| E["✓ Optimal<br/>maintain current<br/>bundle mixture"]
    C -->|"0.05 < f(0) < 0.08"| F["Borderline high<br/>tighten bundle weights"]
    C -->|"f(0) ≥ 0.08"| G["Too high<br/>add agent parallelism<br/>reduce presend"]
    
    D --> H["Update bundle_mixture_weights<br/>formula parameters"]
    F --> H
    G --> H
    
    H --> I["Next Session:<br/>Use updated weights"]
    I --> A
    
    style C fill:#fff9c4,stroke:#f57f17
    style H fill:#c8e6c9,stroke:#2e7d32
```

### Monthly Context Pressure Sigmoid Refit

```mermaid
graph TD
    A["30-day context_pressure_log<br/>500+ spawn decision points"] --> B["Extract:<br/>context_fill%, p(c)_predicted,<br/>actual_spawn_decision"]
    
    B --> C["Fit sigmoid curve<br/>to observed data<br/>find best c_mid, k"]
    
    C --> D{{"Fitted sigmoid<br/>matches observed<br/>?80%"}}
    
    D -->|"YES"| E["✓ Sigmoid params stable<br/>use fitted c_mid, k"]
    D -->|"NO"| F["Adjust c_mid or k<br/>re-fit until convergence"]
    
    F --> C
    E --> G["Log parameters<br/>to forensics/metrics/"]
    G --> H["Next month:<br/>Use updated sigmoid"]
    
    style D fill:#fff176,stroke:#f57f17
```

---

## 5. Mission Coherence: Team Focus Metric

```
Entropy-based focus score:

coherence = 1 - H(labels) / H_max

Where:
  H(labels) = Shannon entropy of investigation_labels in discovered_work[]
  H_max = log₂(num_unique_labels)

Interpretation:
  coherence ≈ 1.0  →  Team laser-focused on 1-2 missions
  coherence ≈ 0.5  →  Team scattered across many missions
  coherence < 0.75 →  ⚠ Mission drift detected
```

### Coherence Monitoring

```mermaid
graph TD
    A["All manifests<br/>this wave"] --> B["Extract investigation_label<br/>from each manifest"]
    B --> C["Count label frequencies<br/>compute Shannon entropy H"]
    C --> D["Calculate coherence<br/>1 - H/H_max"]
    
    D --> E{{"coherence<br/>score?"}}
    
    E -->|"≥0.90"| F["✓ Laser Focus<br/>team tightly aligned"]
    E -->|"0.75-0.90"| G["✓ Good Focus<br/>1-2 main missions"]
    E -->|"<0.75"| H["⚠ Drift Detected<br/>too many parallel missions"]
    
    H --> I["Signal main:<br/>consider consolidating scope"]
    
    style E fill:#fff9c4,stroke:#f57f17
    style I fill:#ffccbc,stroke:#d84315
```

---

## 6. Reputation Decay: Meritocratic Agent Selection

```
Prevent permanent caste system: decay old scores, enable comebacks

score_aged(t) = score₀ / (1 + λ·days)

Where:
  score₀ = initial reputation score
  λ = decay constant (0.1 per day by default)
  days = time since agent's last spawn
  
At λ=0.1:
  Day 0: score₀ (100%)
  Day 7: score₀ / 1.7 ≈ 59% (half-life)
  Day 30: score₀ / 4 = 25% (fully reset to baseline)
```

### Decay Curve (Excalidraw-style)

```
Reputation Score vs Time

100% |●
     |  ╲
 75% |    ╲
     |      ╲
 50% |        ●─────← Half-life: ~7 days
     |          ╲
 25% |            ╲___●
     |
  0%  ├─────┬─────┬─────┬─────┐
     0      7     14    21    30  days

λ = 0.1 (decay per day)

Logic:
  - Top agent from last month slowly decays
  - New agent with good score rises quickly
  - System meritocratic, not monopolistic
```

---

## 7. Discovery Density: Signal Quality per Manifest

```
discovered_work_density = Σ entries in discovered_work[] / num_manifests

Current baseline: 2.8 entries/manifest
Target: 3.5 entries/manifest

Interpretation:
  density < 2.0 →  Agent bundles too constrained; not discovering enough
  density 2.5-3.5 →  ✓ Healthy discovery rate
  density > 5.0 →  May be over-discovering (signal noise, false positives)
```

### Density Feedback

```mermaid
graph TD
    A["End of wave<br/>Count discovered_work[] entries"] --> B["density = total_entries / num_manifests"]
    
    B --> C{{"density<br/>in bounds?"}}
    
    C -->|"< 2.0"| D["Bundle too constrained<br/>add frontier scan depth<br/>reduce task specificity"]
    C -->|"2.5-3.5"| E["✓ Healthy<br/>maintain current bundle<br/>formula working well"]
    C -->|"> 5.0"| F["Over-discovering<br/>focus bundles more<br/>reduce scope expansion"]
    
    D --> G["Adjust bundle mixture<br/>weights formula"]
    F --> G
    G --> H["Next wave:<br/>Use tuned formula"]
    
    style C fill:#fff9c4,stroke:#f57f17
```

---

## 8. Complete Feedback Loop: From Measurement to Living Formula

```mermaid
graph TD
    A["Session Executes<br/>Agents spawn & work"] --> B["Measurement Hooks Capture:<br/>f(0), context_pressure,<br/>coherence, density,<br/>reputation decay"]
    
    B --> C["Data flows to<br/>forensics/metrics/"]
    
    C -->|"Daily"| D["f(0) tracker<br/>context_pressure_log<br/>coherence scores"]
    C -->|"Weekly"| E["Aggregate & analyze<br/>formulas tracking sheet"]
    C -->|"Monthly"| F["Refit sigmoid,<br/>adjust weights,<br/>publish formula report"]
    
    E --> G{{"Formula<br/>performing<br/>well?"}}
    
    G -->|"YES"| H["Log to HONEY.md<br/>formula is proven"]
    G -->|"NO"| I["Propose parameter tweaks<br/>run shadow mode"]
    
    I --> J["Test new formula<br/>for 5 sessions"]
    J --> K{{"Better<br/>outcomes?"}}
    K -->|"YES"| H
    K -->|"NO"| L["Revert to prior formula<br/>try different approach"]
    
    H --> M["Next Session:<br/>Use refined formula"]
    M --> A
    
    style A fill:#e1f5ff,stroke:#0277bd
    style M fill:#c8e6c9,stroke:#2e7d32
    style I fill:#fff9c4,stroke:#f57f17
```

---

## Summary: F(0) Constraint + Living Formulas

| Aspect | Old Approach | New Approach |
|--------|--------------|--------------|
| **f(0)** | Measured passively | Enforced as constraint (≤5%) |
| **Wave Timing** | Discrete thresholds (W1/W2/W3) | Continuous sigmoid formula |
| **Pacing Decision** | Human judgment ("is it W2 time?") | Formula query (p(c) score) |
| **Agent Quality** | Static rankings | Decaying reputation (meritocratic) |
| **Team Focus** | Gut feeling | Measured coherence (entropy-based) |
| **Feedback** | One-time fixes | Living loops (weekly + monthly) |
| **Formulas** | Static parameters | Refit monthly on data |

**Result:** Main doesn't manage waves—formulas do. Main focuses on mission intent, formulas handle pacing.

---

**Next Actions:**
1. ✓ Wire measurement hooks (9x_f0_tracker.py, 9x_context_pressure_logger.py)
2. ✓ Implement f(0) constraint enforcement
3. ✓ Run Phase 1 (measurement: 3-5 sessions)
4. → Phase 2 (sigmoid shadow mode: sessions 4-8)
5. → Phase 3 (cutover: replace wave gates with formula)
