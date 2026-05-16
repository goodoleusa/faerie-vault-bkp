# CULTURAL COMPATIBILITY GAPS & FIXES — Open Models in Faerie2

**Purpose:** Identify where Faerie2 assumes Claude (CLI, models, eval infrastructure) and propose minimal-change adapters to support open models (Ollama, vLLM, TGI, etc.).

**Audience:** DevOps/ML engineers preparing to onboard new model families.

---

## GAP 1: Agent Spawning (HARD BLOCKER)

### The Problem

**Claude CLI mechanism:** `/spawn` uses `Agent(subagent_type=...)` tool, which is ONLY available in Claude Code CLI.

```python
# This works in Claude Code CLI:
Agent(
    subagent_type="data-analyst",
    prompt="Analyze the revenue data...",
    model="haiku"
)

# Open models have NO equivalent tool.
```

**Impact:** Cannot spawn worker agents dynamically. Data-ingest team orchestration (11 agents) becomes impossible.

### The Fix: Celery Bridge Adapter

**Option A: Celery Task Queue (Recommended)**

```python
# File: ~/.claude/adapters/agent-celery-bridge.py
"""
Bridge between Claude CLI Agent() calls and open-model task queue.
Routes spawned agents to Celery workers running Ollama/vLLM endpoints.
"""

import json
import uuid
from celery import Celery
from typing import Optional

class AgentBridge:
    def __init__(self, broker_url="redis://localhost:6379"):
        self.app = Celery("faerie-agents", broker=broker_url)
        self.app.conf.update(
            result_backend="redis://localhost:6379",
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
        )
    
    def spawn_agent(
        self,
        subagent_type: str,
        prompt: str,
        model: str = "llama2-70b",
        investigation_label: str = "default",
        run_in_background: bool = False,
    ) -> dict:
        """
        Mimics Agent() tool behavior. Routes to Celery worker.
        Returns task result (manifest JSON).
        """
        task_id = str(uuid.uuid4())
        
        # Celery task: invoke model on worker
        async_result = self.app.send_task(
            "agents.execute_task",
            args=[
                subagent_type,
                prompt,
                model,
                investigation_label,
                task_id,
            ],
            task_id=task_id,
        )
        
        if run_in_background:
            # Fire-and-forget
            return {"task_id": task_id, "status": "queued"}
        else:
            # Wait for result (up to 5 min timeout)
            result = async_result.get(timeout=300)
            return result
    
    def __call__(self, **kwargs):
        """Allow AgentBridge() to mimic Agent() syntax."""
        return self.spawn_agent(**kwargs)

# Usage (replaces Agent() in Claude Code):
# agent_bridge = AgentBridge()
# result = agent_bridge(
#     subagent_type="data-analyst",
#     prompt="Analyze data...",
#     model="llama2-70b"
# )
```

**Celery Worker (runs inference):**

```python
# File: workers/faerie_agent_worker.py
"""
Celery worker that executes agent tasks on Ollama/vLLM endpoints.
"""

from celery import Celery, Task
import requests
import json
from pathlib import Path
import datetime

app = Celery("faerie-agents")
app.config_from_object("celery_config.py")

@app.task(name="agents.execute_task", bind=True)
def execute_agent_task(
    self,
    subagent_type: str,
    prompt: str,
    model: str,
    investigation_label: str,
    task_id: str,
) -> dict:
    """
    Execute agent task on open model (Ollama/vLLM endpoint).
    Return manifest JSON (same schema as Claude Agent output).
    """
    
    # 1. Send prompt to model endpoint
    endpoint = f"http://localhost:11434/api/generate"  # Ollama
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=300)
        response.raise_for_status()
        model_output = response.json()["response"]
    except Exception as e:
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(e),
        }
    
    # 2. Parse manifest from model output (expect JSON block)
    manifest = _extract_manifest_from_output(model_output, task_id)
    
    # 3. Write manifest to forensics/
    manifest_path = _write_manifest(manifest, investigation_label, model)
    
    # 4. Return result
    return {
        "task_id": task_id,
        "status": "complete",
        "manifest_path": manifest_path,
        "dashboard_line": manifest.get("dashboard_line", ""),
    }

def _extract_manifest_from_output(output: str, task_id: str) -> dict:
    """Extract JSON manifest from model output."""
    # Model should write JSON block: ```json { ... } ```
    try:
        start = output.find("```json") + 7
        end = output.find("```", start)
        json_str = output[start:end].strip()
        return json.loads(json_str)
    except:
        # Fallback: create minimal manifest
        return {
            "task_id": task_id,
            "dashboard_line": output[:80],
            "compass_edge": "S",
            "quality_score": 0.5,
            "belief_index": 0.5,
        }

def _write_manifest(manifest: dict, investigation_label: str, model: str) -> str:
    """Write manifest to forensics/manifests/ folder."""
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc)
    folder = Path(f"forensics/manifests/{ts.strftime('%Y-%m-%d')}")
    folder.mkdir(parents=True, exist_ok=True)
    
    filename = (
        f"{ts.strftime('%H-%M-%S')}Z_manifest_task-{manifest['task_id']}_{model}_001.json"
    )
    path = folder / filename
    path.write_text(json.dumps(manifest, indent=2))
    return str(path)
```

**Config:**

```python
# File: celery_config.py
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
timezone = "UTC"
enable_utc = True
task_acks_late = True
task_reject_on_worker_lost = True
```

**Docker Compose (4 workers):**

```yaml
version: "3.9"
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama:/root/.ollama
    environment:
      - OLLAMA_GPU=1  # Enable GPU
  
  worker-1:
    build: .
    command: celery -A workers.faerie_agent_worker worker -n worker1@%h -Q default
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
      - OLLAMA_ENDPOINT=http://ollama:11434
    depends_on:
      - redis
      - ollama
  
  worker-2:
    build: .
    command: celery -A workers.faerie_agent_worker worker -n worker2@%h -Q default
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
      - OLLAMA_ENDPOINT=http://ollama:11434
    depends_on:
      - redis
      - ollama
  
  # ... worker-3, worker-4 ...

volumes:
  ollama:
```

**Integration with /spawn (minimal changes):**

```python
# File: .claude/skills/spawn/executor-open-models.py
"""
Modified executor.py to use Celery bridge instead of Agent() tool.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "adapters"))

from agent_celery_bridge import AgentBridge

def main():
    args = sys.argv[1:]
    
    # Parse args (same as before)
    wave = extract_wave(args)
    investigation_label = extract_investigation_label(args)
    spawn_requests = generate_spawn_requests(args)
    
    # Use bridge instead of Agent() tool
    bridge = AgentBridge()
    results = []
    
    for req in spawn_requests:
        agent_type = req["agent_type"]
        prompt = req["prompt"]
        model = req.get("model", "llama2-70b")
        run_inline = req.get("run_inline", True)
        
        print(f"Spawning {agent_type} on {model}...")
        result = bridge.spawn_agent(
            subagent_type=agent_type,
            prompt=prompt,
            model=model,
            investigation_label=investigation_label,
            run_in_background=(not run_inline),
        )
        results.append(result)
        print(f"  → {result['status']} (task {result['task_id']})")
    
    print(f"\nAll {len(results)} agents spawned ({investigation_label})")

if __name__ == "__main__":
    main()
```

---

## GAP 2: Reputation Framework (MODERATE FIX)

### The Problem

**Claude-specific:** `composite_score` (0.0–1.0) and `belief_index` computed from Claude eval infrastructure (internal KPIs, last training timestamp, feature adoption).

**Open models:** No built-in eval framework. Reputation must be computed from **actual task outcomes**, not training metadata.

### The Fix: Lightweight Reputation Service

```python
# File: ~/.claude/adapters/reputation-service.py
"""
Compute composite_score and belief_index from manifests (task outcomes).
Serve via HTTP endpoint. Agents fetch on startup.
"""

import json
import redis
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Tuple
from statistics import mean

class ReputationService:
    def __init__(self, redis_url="redis://localhost:6379/0"):
        self.redis = redis.from_url(redis_url)
    
    def compute_composite_score(self, model_name: str) -> float:
        """
        Compute 0.0–1.0 score from last 10 tasks.
        Score = (quality_score + belief_index) / 2
        """
        manifests = self._fetch_recent_manifests(model_name, limit=10)
        if not manifests:
            return 0.50  # Default for new models
        
        quality_scores = [m.get("quality_score", 0.5) for m in manifests]
        belief_indices = [m.get("belief_index", 0.5) for m in manifests]
        
        composite = mean(quality_scores + belief_indices)
        return round(min(1.0, max(0.0, composite)), 2)
    
    def compute_belief_index(self, model_name: str) -> float:
        """
        Compute 0.0–1.0 honesty index from four signals:
        1. Manifest truthfulness (does dashboard_line match actual output?)
        2. Error admission (does agent admit uncertainty?)
        3. Citation accuracy (are sources real?)
        4. Outcome alignment (did agent deliver promised work?)
        """
        manifests = self._fetch_recent_manifests(model_name, limit=10)
        if not manifests:
            return 0.50
        
        signals = []
        for m in manifests:
            # Signal 1: Manifest truthfulness (spot-check, heuristic)
            dashboard_len = len(m.get("dashboard_line", ""))
            signal1 = 1.0 if 20 <= dashboard_len <= 80 else 0.5
            
            # Signal 2: Error admission (look for "uncertain", "likely", "estimate")
            output = self._fetch_artifact(m.get("artifacts_written", [None])[0])
            signal2 = 1.0 if self._contains_uncertainty_language(output) else 0.6
            
            # Signal 3: Citation accuracy (basic check: URLs valid?)
            signal3 = 1.0 if self._verify_citations(output) else 0.4
            
            # Signal 4: Outcome alignment (compass_edge makes sense?)
            signal4 = 1.0 if m.get("compass_edge") in ["N", "S", "E", "W"] else 0.3
            
            signals.append(mean([signal1, signal2, signal3, signal4]))
        
        return round(mean(signals), 2) if signals else 0.50
    
    def get_reputation(self, model_name: str) -> Dict:
        """Return composite_score + belief_index."""
        composite = self.compute_composite_score(model_name)
        belief = self.compute_belief_index(model_name)
        
        return {
            "model_name": model_name,
            "composite_score": composite,
            "belief_index": belief,
            "interpretation": self._interpret_score(composite, belief),
            "recommendation": self._recommend_work_level(composite),
        }
    
    def _interpret_score(self, composite: float, belief: float) -> str:
        if composite >= 0.7 and belief >= 0.7:
            return "HEALTHY — Can claim HIGH/CRITICAL work. Honesty is strong."
        elif composite >= 0.5 and belief >= 0.5:
            return "CAUTION — Can claim MED work. Monitor honesty."
        else:
            return "RECOVERY — Claim LOW/MED work only. Improve honesty."
    
    def _recommend_work_level(self, composite: float) -> str:
        if composite >= 0.7:
            return "HIGH/CRITICAL"
        elif composite >= 0.5:
            return "MED"
        else:
            return "LOW"
    
    def _fetch_recent_manifests(self, model_name: str, limit: int = 10) -> list:
        """Read manifests from forensics/ folder (last N matching model)."""
        forensics_path = Path("forensics/manifests")
        manifests = []
        
        for date_folder in sorted(forensics_path.glob("*"), reverse=True):
            if not date_folder.is_dir():
                continue
            for manifest_file in sorted(date_folder.glob(f"*{model_name}*.json"), reverse=True):
                try:
                    m = json.loads(manifest_file.read_text())
                    manifests.append(m)
                    if len(manifests) >= limit:
                        return manifests
                except:
                    continue
        
        return manifests
    
    def _fetch_artifact(self, artifact_path: str) -> str:
        """Read artifact from disk."""
        try:
            return Path(artifact_path).read_text()
        except:
            return ""
    
    def _contains_uncertainty_language(self, text: str) -> bool:
        """Check for admissions of uncertainty."""
        uncertain_words = ["uncertain", "likely", "estimate", "may", "might", "unclear", "unknown"]
        return any(word in text.lower() for word in uncertain_words)
    
    def _verify_citations(self, text: str) -> bool:
        """Basic citation check (url pattern detection)."""
        import re
        urls = re.findall(r"https?://\S+", text)
        # Heuristic: if agent cites sources, bonus points
        return len(urls) > 0

# HTTP Server (Flask)
from flask import Flask, jsonify

app = Flask(__name__)
service = ReputationService()

@app.route("/api/reputation/<model_name>", methods=["GET"])
def get_reputation(model_name: str):
    """Endpoint agents fetch on startup."""
    return jsonify(service.get_reputation(model_name))

@app.route("/api/reputation/<model_name>/update", methods=["POST"])
def update_reputation(model_name: str):
    """Recompute score (called after manifest write)."""
    return jsonify(service.get_reputation(model_name))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

**Integration with agent startup (prompt injection):**

```python
# Fetch reputation before task execution
import requests

def get_agent_context(model_name: str) -> Dict:
    """Fetch reputation context before spawning agent."""
    try:
        resp = requests.get(f"http://reputation-service:5000/api/reputation/{model_name}")
        return resp.json()
    except:
        return {"composite_score": 0.5, "belief_index": 0.5}  # Fallback

# Add to agent prompt:
reputation = get_agent_context("mistral-7b-instruct")
prompt = f"""
## YOUR REPUTATION (Honesty Check)

Composite Score: {reputation['composite_score']} / 1.0
Belief Index: {reputation['belief_index']} / 1.0
Recommendation: {reputation['recommendation']}

**Important:** If your composite_score < 0.5, you MUST NOT attempt HIGH or CRITICAL work.
Claim only {reputation['recommendation']} work. Be honest about uncertainty.

{task_description}
"""
```

---

## GAP 3: Vision API Costs (EASY FIX)

### The Problem

Vision-ingest Step 4 requires paid Claude Vision API. No fallback for open models.

### The Fix: Ollama+LLaVA Adapter

```python
# File: ~/.claude/adapters/vision-ingest-ollama.py
"""
Replace Claude Vision API with Ollama+LLaVA (free, local).
Drop-in replacement for Step 4 of vision-ingest.
"""

import json
import requests
from pathlib import Path
from typing import Dict, List
import base64

class VisionProcessorOllama:
    def __init__(self, ollama_endpoint="http://localhost:11434"):
        self.endpoint = ollama_endpoint
        self.model = "llava"  # Ollama LLaVA model
    
    def process_frame(self, image_path: str, task: str = "extract_text") -> Dict:
        """
        Process single frame (image) via Ollama+LLaVA.
        task: "extract_text" | "extract_tables" | "extract_forms" | "identify_metrics"
        """
        
        # 1. Load image as base64
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")
        
        # 2. Craft prompt for task
        prompt = self._craft_prompt(task)
        
        # 3. Send to Ollama
        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
            "temperature": 0.3,  # Low temp for structured extraction
        }
        
        try:
            resp = requests.post(
                f"{self.endpoint}/api/generate",
                json=payload,
                timeout=60,
            )
            resp.raise_for_status()
            output = resp.json()["response"]
        except Exception as e:
            return {"error": str(e), "output": None}
        
        # 4. Parse JSON from output
        extracted = self._parse_json_from_output(output)
        return extracted
    
    def _craft_prompt(self, task: str) -> str:
        """Generate task-specific prompt."""
        if task == "extract_text":
            return """Extract all visible text from this image. Return as JSON:
{
  "text_blocks": [
    {"content": "...", "position": "top|middle|bottom|left|right"},
    ...
  ],
  "confidence": 0.85
}"""
        elif task == "extract_tables":
            return """Extract all table data from this image. Return as JSON:
{
  "tables": [
    {
      "headers": [...],
      "rows": [[...], ...],
      "caption": "..."
    }
  ]
}"""
        elif task == "extract_forms":
            return """Extract all form fields from this image. Return as JSON:
{
  "form_fields": [
    {"label": "Name", "value": "...", "type": "text|checkbox|radio"},
    ...
  ]
}"""
        elif task == "identify_metrics":
            return """Identify all numbers, metrics, and key values in this image. Return as JSON:
{
  "metrics": [
    {"name": "Revenue", "value": "1.2M", "unit": "$"},
    ...
  ]
}"""
        else:
            return "Analyze this image and return findings as structured JSON."
    
    def _parse_json_from_output(self, output: str) -> Dict:
        """Extract JSON from LLaVA output."""
        try:
            # Look for JSON block
            start = output.find("{")
            end = output.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = output[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback: return raw output
        return {"raw_output": output, "confidence": 0.3}
    
    def process_batch(self, image_paths: List[str], task: str = "extract_text") -> List[Dict]:
        """Process multiple frames."""
        results = []
        for path in image_paths:
            result = self.process_frame(path, task)
            result["image_path"] = path
            results.append(result)
        return results

# Integration with vision-ingest:
def step4_vision_api(image_dir: str, config: Dict) -> Dict:
    """
    Drop-in replacement for Claude Vision API step.
    config = {"api": "claude" | "ollama", ...}
    """
    
    if config.get("api") == "ollama":
        processor = VisionProcessorOllama(config.get("endpoint", "http://localhost:11434"))
        task_type = config.get("task", "extract_text")
        
        image_paths = list(Path(image_dir).glob("*.jpg")) + list(Path(image_dir).glob("*.png"))
        results = processor.process_batch(image_paths, task=task_type)
        
        return {"results": results, "total_processed": len(results), "api_used": "ollama"}
    
    else:  # Claude Vision API (paid)
        # Original Claude Vision API code here
        pass
```

**Cost comparison:**
- Claude Vision API: $0.003 per 1K image tokens; 500 frames = $0.75–5 (depends on image complexity)
- Ollama+LLaVA: Free (local GPU cost ~$0.35/hour)

---

## GAP 4: Token Metering (EASY FIX)

### The Problem

Claude Code CLI tracks tokens natively. Open models (Ollama, vLLM) have no standard accounting. Can't measure FFMx (force per token).

### The Fix: Prometheus Hook

```python
# File: ~/.claude/adapters/prometheus-token-meter.py
"""
Log token usage to Prometheus. Integrate with Celery worker or Ollama wrapper.
"""

from prometheus_client import Counter, Histogram, start_http_server
import time

# Define metrics
token_counter = Counter(
    "agent_tokens_total",
    "Total tokens used (input + output)",
    ["model", "task_type", "status"],
)

task_duration = Histogram(
    "agent_task_seconds",
    "Task execution time",
    ["model", "task_type"],
)

quality_score_gauge = Gauge(
    "agent_quality_score",
    "Output quality (0.0–1.0)",
    ["model"],
)

def log_task_completion(
    model: str,
    task_type: str,
    input_tokens: int,
    output_tokens: int,
    duration_sec: float,
    quality_score: float,
    status: str = "success",
):
    """Log task metrics to Prometheus."""
    total_tokens = input_tokens + output_tokens
    token_counter.labels(model, task_type, status).inc(total_tokens)
    task_duration.labels(model, task_type).observe(duration_sec)
    quality_score_gauge.labels(model).set(quality_score)
    
    # Also log to time-series DB (if available)
    print(f"✓ {model}: {total_tokens} tokens | {duration_sec:.1f}s | quality {quality_score:.2f}")

# Start metrics server (port 9090)
if __name__ == "__main__":
    start_http_server(9090)
    print("Prometheus metrics listening on http://localhost:9090/metrics")
```

**Integration with Celery worker:**

```python
# In faerie_agent_worker.py
@app.task
def execute_agent_task(subagent_type, prompt, model, investigation_label, task_id):
    start_time = time.time()
    
    # Model inference...
    input_tokens = count_tokens(prompt)
    response = call_model(model, prompt)
    output_tokens = count_tokens(response)
    
    # Log to Prometheus
    log_task_completion(
        model=model,
        task_type=subagent_type,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        duration_sec=time.time() - start_time,
        quality_score=manifest["quality_score"],
    )
    
    return manifest
```

---

## SUMMARY: Gaps and Effort Matrix

| Gap | Severity | Effort | Fix | Impact |
|-----|----------|--------|-----|--------|
| **Agent() tool** | HARD BLOCKER | 2 weeks | Celery bridge | Unblocks team spawn |
| **Reputation scoring** | MODERATE | 1 week | Redis + scorer | Unblocks quality gating |
| **Vision API costs** | EASY | 3 days | Ollama+LLaVA | Frees vision-ingest from paid API |
| **Token metering** | EASY | 1 week | Prometheus | Enables FFMx measurement |
| **Manifest schema** | NONE | 0 | None | Already model-agnostic ✓ |
| **COC logging** | NONE | 0 | None | Already model-agnostic ✓ |
| **Forensic naming** | NONE | 0 | None | Already model-agnostic ✓ |

---

## DEPLOYMENT ROADMAP

### Week 1: Foundation
- [ ] Deploy Celery + Redis + Ollama (Docker Compose)
- [ ] Test basic task queue (enqueue / dequeue)
- [ ] Build agent-celery-bridge.py

### Week 2: Core Adapters
- [ ] Implement reputation-service.py
- [ ] Implement vision-ingest-ollama.py
- [ ] Test single-agent spawn (data-analyst on llama2-70b)

### Week 3: Integration
- [ ] Wire reputation service into /spawn skill
- [ ] Wire Ollama adapter into vision-ingest
- [ ] Test team dispatch (4 agents, mixed models)

### Week 4: Metrics & Polish
- [ ] Deploy Prometheus + Grafana
- [ ] Implement token metering hooks
- [ ] Stress test: run 20-agent job, measure FFMx
- [ ] Document in runbooks

---

**Document:** Cultural Compatibility Gaps v1.0  
**Date:** 2026-04-28  
**Status:** Actionable roadmap — use for Q3 planning
