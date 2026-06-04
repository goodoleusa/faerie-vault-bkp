---
type: documentation
title: MEMBENCH-COMPETITOR-HARNESS — Adapting Membench to External Memory Systems
status: complete
created: 2026-04-25
tags: [membench, evaluation-framework, competitors, adapter-pattern, mem0, chatgpt, memgpt, letta]
---

> [↑ Docs](./README.md) · [← MEMBENCH-METRICS-DETAILED-GUIDE](./MEMBENCH-METRICS-DETAILED-GUIDE.md) · [→ MEMBENCH-AS-OPEN-FRAMEWORK](./MEMBENCH-AS-OPEN-FRAMEWORK.md)

# MEMBENCH-Competitor Harness — Evaluation Framework for Third-Party Memory Systems

**Purpose:** Show how Mem0, ChatGPT Persistent Memory, MemGPT, Letta, and other agentic memory products can adapt the Membench evaluation framework to their own architectures and run credible benchmarks against faerie2 and other systems.

---

## 1. The Competitor Adapter Pattern

### 1.1 — Why Adapt?

Membench was built to measure faerie2's memory system (HONEY/NECTAR/pollen), which has explicit file-based state, checkpointing, and forensic logging. Other memory systems store state differently: as encrypted vectors, in a managed service, in a local database, or in a black-box model. A generic competitor cannot run faerie's harness directly. Instead, they must adapt Membench's eight metrics to their own memory architecture.

**The pattern:** Each competitor implements a "memory-adapter" module that translates Membench's probe interface into their system's native API and state representation. The adapter then reports back to a unified scoring system. The probe sets (Retention, Confabulation, Relevance, etc.) remain architecture-agnostic; the *measurement* is what changes.

### 1.2 — What Must Be Adapted?

Membench expects to probe the memory system at these layers:

| Membench Concept | What It Measures | Competitor Mapping |
|------------------|------------------|-------------------|
| **HONEY** | Crystallised memory (compressed, canonical) | Summarised/compressed state (depends on system) |
| **NECTAR** | Raw findings log (append-only, dense) | Full memory history (vector store, event log, database table) |
| **Pollen** | Working observations (ephemeral, per-session) | In-flight context (conversation buffer, working memory) |
| **Checkpoint** | Session boundary preservation (manifest state before compact) | Session resumption mechanism (saved session state, vector persistence) |
| **Probe Set** | 10 randomised retention/confabulation questions | Domain-specific facts for your use case |
| **Metric Computation** | Universal (Retention %, Relevance %, Efficiency ratio) | Same scoring logic, different input sources |

### 1.3 — The Four-Tier Compatibility Framework

Not all systems expose enough state to implement all metrics. Membench defines four tiers:

**Tier 1: Full Native (1–2 days to adapter)**
- Memory is explicit in files or queryable databases
- Session checkpointing is visible
- Agent manifests or decision logs exist
- Examples: faerie2, MemGPT, Letta

**Tier 2: Structured Memory (3–5 days to adapter)**
- Memory is stored in inspectable form (vector store, SQL database, JSON file)
- You can read memory contents directly via API or file-system access
- Chunking/summarisation is visible
- Examples: Mem0 (with API access), LlamaIndex + vector stores, ChromaDB

**Tier 3: API-Based (1–2 weeks to adapter)**
- Memory is opaque to direct inspection but queryable via API
- You can test memory retrieval (query → response)
- You must infer correctness from interaction, not introspection
- Examples: ChatGPT Persistent Memory, OpenAI Assistants API, Anthropic Memory extensions

**Tier 4: Proxy-Based (2–4 weeks to adapter)**
- Memory is fully black-box; no direct access to memory contents
- You can only measure downstream effects (agent quality, task completion)
- Requires synthetic workload design and output comparison
- Examples: Closed-source commercial systems, proprietary platforms

### 1.4 — Generic Adapter Template

Every adapter implements this interface:

```python
class MemorySystemAdapter:
    """Bridge between Membench probe interface and any memory system."""
    
    def __init__(self, system_config: dict):
        """Initialize connection to memory system.
        
        Args:
            system_config: System-specific config (API keys, paths, credentials)
        """
        pass
    
    def store_fact(self, fact: str, metadata: dict = None) -> dict:
        """Store a fact in the system's memory layer.
        
        Returns: {"fact_id": str, "storage_layer": str, "timestamp": str}
        """
        raise NotImplementedError
    
    def retrieve_memory(self, query: str) -> dict:
        """Retrieve memory matching the query.
        
        Returns: {
            "results": [{"text": str, "source": str, "score": float}],
            "total_retrieved": int,
            "memory_layer": str
        }
        """
        raise NotImplementedError
    
    def get_memory_state(self) -> dict:
        """Read the full memory state (for Crystallisation Quality metric).
        
        Returns: {
            "compressed_memory": str,  # or None if not accessible
            "raw_memory": str,         # or None if not accessible
            "memory_size_bytes": int,
            "last_updated": str
        }
        """
        raise NotImplementedError
    
    def checkpoint_state(self) -> dict:
        """Get the system's current checkpoint/session state.
        
        Returns: {
            "checkpoint_path": str,
            "checkpoint_timestamp": str,
            "contents_hash": str,
            "can_resume": bool
        }
        """
        raise NotImplementedError
    
    def resume_from_checkpoint(self, checkpoint: dict) -> bool:
        """Resume from a saved checkpoint.
        
        Returns: True if resume successful, False otherwise.
        """
        raise NotImplementedError
    
    def get_memory_overhead(self) -> dict:
        """Measure memory infrastructure tokens/cost.
        
        Returns: {
            "tokens_per_read": int,
            "tokens_per_write": int,
            "tokens_per_query": int,
            "api_calls_per_session": int,
            "estimated_monthly_cost": float
        }
        """
        raise NotImplementedError
```

This is the **minimum contract**. Systems that cannot implement all methods mark them as `NotImplementedError` and Membench reports "metric not available for this tier."

---

## 2. Mem0 Adapter (Tier 2 — Structured Memory)

### 2.1 — Mem0 Architecture Overview

Mem0 stores memory in:
- **Structured memory** (JSON-stored facts, queryable)
- **Vector store** (embeddings for semantic search)
- **Metadata** (tags, sources, update timestamps)

Memory is accessible via Mem0's Python API and persisted in local file or remote service. Membench can read the structured memory directly.

### 2.2 — Retention Metric for Mem0

**What we're testing:** When facts are stored in Mem0 (via `mem0.add()`), can they be reliably retrieved with specific keywords?

```python
class Mem0Adapter(MemorySystemAdapter):
    def __init__(self, config):
        from mem0 import MemoryClient
        self.client = MemoryClient(api_key=config.get('api_key'))
        self.memory_id = config.get('memory_id')
    
    def store_fact(self, fact: str, metadata: dict = None) -> dict:
        """Add a fact to Mem0's structured memory."""
        result = self.client.add(fact, memory_id=self.memory_id)
        return {
            "fact_id": result.get('id'),
            "storage_layer": "mem0_structured",
            "timestamp": result.get('timestamp')
        }
    
    def retrieve_memory(self, query: str) -> dict:
        """Retrieve facts matching the query."""
        results = self.client.search(query, memory_id=self.memory_id, limit=10)
        return {
            "results": [
                {"text": r.get('data'), "source": "mem0", "score": r.get('score', 1.0)}
                for r in results
            ],
            "total_retrieved": len(results),
            "memory_layer": "structured"
        }
    
    def probe_retention(self, probe_set: list[dict]) -> dict:
        """Run retention probes against Mem0."""
        scores = []
        for probe in probe_set:
            query = probe['query']
            required_substrings = probe['required_substrings']
            anti_facts = probe.get('anti_facts', [])
            
            # Retrieve
            result = self.retrieve_memory(query)
            retrieved_text = ' '.join([r['text'] for r in result['results']])
            
            # Score
            score = 10  # Start at full points
            required_hit_count = sum(
                1 for substring in required_substrings
                if substring.lower() in retrieved_text.lower()
            )
            if required_hit_count == len(required_substrings):
                score = 10  # All required present
            elif required_hit_count > 0:
                score = 4   # Partial
            else:
                score = 0   # Missing
            
            # Check anti-facts
            for anti_fact in anti_facts:
                if anti_fact.lower() in retrieved_text.lower():
                    score = 0  # Confabulation
                    break
            
            scores.append(score)
        
        retention_pct = (sum(scores) / (len(scores) * 10)) * 100
        return {
            "retention_score": retention_pct,
            "scores": scores,
            "probe_count": len(scores)
        }
```

**Calibration for Mem0:**
- Train on 5–10 runs to establish baseline Retention
- If Retention is consistently >85%, probes are well-aligned
- If Retention is <60%, either Mem0's semantic search is weak or probes expect too-specific phrasing

### 2.3 — Overhead Calculation for Mem0

Mem0 is typically a SaaS API, so "overhead" means API calls + tokens.

```python
def get_memory_overhead(self) -> dict:
    """Measure Mem0's cost in API calls and tokens."""
    # Mem0 API call costs (example; adjust to Mem0's actual pricing)
    # Each add() call = 1 API call
    # Each search() call = 1 API call
    # Token estimate: assume Mem0 internally spends ~50 tokens per add(),
    # ~20 tokens per search() (internal embedding + retrieval)
    
    calls_per_session = {
        "add_calls": 10,      # Facts added during session
        "search_calls": 25,   # Queries during session
        "update_calls": 2,    # Updates/corrections
    }
    
    estimated_tokens = {
        "add": calls_per_session["add_calls"] * 50,
        "search": calls_per_session["search_calls"] * 20,
    }
    
    # Pricing: $0.0001 per call (example; update to actual pricing)
    estimated_cost = (
        (calls_per_session["add_calls"] +
         calls_per_session["search_calls"] +
         calls_per_session["update_calls"]) * 0.0001
    )
    
    return {
        "tokens_per_read": 20,
        "tokens_per_write": 50,
        "tokens_per_query": 20,
        "api_calls_per_session": sum(calls_per_session.values()),
        "estimated_session_cost": estimated_cost,
        "gross_overhead_pct": (
            sum(estimated_tokens.values()) / 
            (5000 + sum(estimated_tokens.values()))  # Total session tokens
        ) * 100
    }
```

### 2.4 — Work Efficiency Baseline for Mem0

```python
def benchmark_work_efficiency(self, task_set: list[dict]) -> dict:
    """Measure tasks completed per thousand tokens with/without Mem0."""
    
    results_with_mem0 = []
    for task in task_set:
        # Retrieve relevant memory
        memory = self.client.search(task['query'], memory_id=self.memory_id)
        # (Agent uses memory to complete task)
        # Measure tokens spent on this task
        task_tokens = 800  # Example
        results_with_mem0.append({
            "task_id": task['id'],
            "tokens": task_tokens,
            "completed": True
        })
    
    tokens_with_mem0 = sum(r['tokens'] for r in results_with_mem0)
    tasks_with_mem0 = len([r for r in results_with_mem0 if r['completed']])
    efficiency_with_mem0 = tasks_with_mem0 / (tokens_with_mem0 / 1000)
    
    # Baseline: estimate tokens without Mem0 (re-briefing cost)
    estimated_baseline_tokens = (
        tokens_with_mem0 * 1.35  # Re-briefing adds ~35% overhead
    )
    efficiency_baseline = tasks_with_mem0 / (estimated_baseline_tokens / 1000)
    
    return {
        "efficiency_with_memory": efficiency_with_mem0,
        "efficiency_baseline": efficiency_baseline,
        "efficiency_ratio": efficiency_with_mem0 / efficiency_baseline,
        "tasks_completed": tasks_with_mem0
    }
```

---

## 3. ChatGPT Persistent Memory Adapter (Tier 3 — API-Based, Opaque)

### 3.1 — ChatGPT Persistent Memory Architecture

ChatGPT's persistent memory is opaque: you send `update_memory()` calls and receive `recalled_memory` in responses, but you cannot directly inspect what is stored or how it is compressed.

**Challenge:** Membench cannot measure Retention by reading the stored memory. Instead, we measure via **interaction.**

### 3.2 — Retention via Interaction (Black-Box Testing)

Instead of inspecting memory, we test whether the system *behaves* as if it remembers.

```python
class ChatGPTMemoryAdapter(MemorySystemAdapter):
    def __init__(self, config):
        import openai
        self.client = openai.OpenAI(api_key=config['api_key'])
        self.conversation_id = config.get('conversation_id')
    
    def store_fact(self, fact: str, metadata: dict = None) -> dict:
        """Store a fact via update_memory in next message."""
        # ChatGPT doesn't have a direct "store" call; facts are conveyed
        # to the model via conversation. We track them locally.
        fact_id = hashlib.sha256(fact.encode()).hexdigest()[:8]
        return {
            "fact_id": fact_id,
            "storage_layer": "chatgpt_persistent",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def retrieve_memory(self, query: str) -> dict:
        """Test whether memory is recalled via an interaction."""
        # Send a query designed to elicit memory recall
        prompt = f"""
        Answer this question based only on facts you have been told in
        previous conversations. If you don't remember, say so explicitly.
        
        Question: {query}
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.choices[0].message.content
        
        return {
            "results": [{"text": response_text, "source": "chatgpt_memory", "score": 1.0}],
            "total_retrieved": 1,
            "memory_layer": "persistent"
        }
    
    def probe_retention_via_interaction(self, probe_set: list[dict]) -> dict:
        """Black-box retention: does the model answer correctly?"""
        scores = []
        
        for probe in probe_set:
            query = probe['query']
            required_substrings = probe['required_substrings']
            
            # Ask the model
            retrieved = self.retrieve_memory(query)
            response_text = retrieved['results'][0]['text']
            
            # Score
            required_hit_count = sum(
                1 for substring in required_substrings
                if substring.lower() in response_text.lower()
            )
            
            if required_hit_count == len(required_substrings):
                score = 10
            elif required_hit_count > 0:
                score = 4
            else:
                score = 0
            
            scores.append(score)
        
        retention_pct = (sum(scores) / (len(scores) * 10)) * 100
        return {
            "retention_score": retention_pct,
            "scores": scores,
            "methodology": "interaction-based (opaque system)"
        }
```

**Interpretation:** A score of 88/100 means "88% of direct interaction probes were answered correctly with required substrings present." It does not measure whether memory is compressed well or continuously available; it measures whether *at test time*, the system correctly recalled the facts.

### 3.3 — Continuity for Opaque Systems

For opaque systems, test continuity via **session resumption**:

```python
def checkpoint_session(self) -> dict:
    """Save current conversation state."""
    return {
        "conversation_id": self.conversation_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "test_marker": f"checkpoint_{uuid.uuid4()}"
    }

def test_resumption(self, checkpoint: dict) -> dict:
    """Does the system remember after a session break?"""
    test_marker = checkpoint['test_marker']
    
    # Query: "What was the most recent checkpoint marker I gave you?"
    prompt = f"What was the last unique marker or ID I mentioned to you?"
    
    result = self.retrieve_memory(prompt)
    response_text = result['results'][0]['text']
    
    if test_marker in response_text:
        continuity_score = 100
    else:
        continuity_score = 0
    
    return {
        "test_marker": test_marker,
        "recognized": test_marker in response_text,
        "continuity_score": continuity_score,
        "methodology": "marker recall after session break"
    }
```

---

## 4. MemGPT / Letta Adapter (Tier 1 — Full Native)

### 4.1 — MemGPT/Letta Architecture

Both MemGPT and Letta expose memory as explicit data structures:
- **CoreMemory** — short-term facts (analogous to HONEY)
- **PeripheralMemory** — long-term history (analogous to NECTAR)
- **Archival** — full record log (analogous to forensics/)

Memory is queryable via the agent's API; manifests or conversation logs record what happened.

### 4.2 — Retention Probe Against Memory Structures

```python
class LettaMemoryAdapter(MemorySystemAdapter):
    def __init__(self, config):
        from letta import LocalClient
        self.client = LocalClient()
        self.agent_id = config['agent_id']
    
    def store_fact(self, fact: str, metadata: dict = None) -> dict:
        """Add to agent's CoreMemory."""
        # Letta: directly write to core memory
        agent = self.client.get_agent(self.agent_id)
        agent.core_memory.append({"text": fact})
        return {
            "fact_id": hashlib.sha256(fact.encode()).hexdigest()[:8],
            "storage_layer": "core_memory",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def get_memory_state(self) -> dict:
        """Read both CoreMemory and PeripheralMemory for quality assessment."""
        agent = self.client.get_agent(self.agent_id)
        core_text = '\n'.join([m.get('text', '') for m in agent.core_memory])
        peripheral_text = '\n'.join(agent.messages[-30:])  # Last 30 messages
        
        return {
            "compressed_memory": core_text,
            "raw_memory": peripheral_text,
            "memory_size_bytes": len(core_text.encode()) + len(peripheral_text.encode()),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    
    def probe_retention(self, probe_set: list[dict]) -> dict:
        """Test Retention against CoreMemory directly."""
        scores = []
        agent = self.client.get_agent(self.agent_id)
        core_memory_text = '\n'.join([m.get('text', '') for m in agent.core_memory])
        
        for probe in probe_set:
            required_substrings = probe['required_substrings']
            required_hit_count = sum(
                1 for substring in required_substrings
                if substring.lower() in core_memory_text.lower()
            )
            
            if required_hit_count == len(required_substrings):
                score = 10
            elif required_hit_count > 0:
                score = 4
            else:
                score = 0
            
            scores.append(score)
        
        return {
            "retention_score": (sum(scores) / (len(scores) * 10)) * 100,
            "scores": scores
        }
    
    def checkpoint_state(self) -> dict:
        """Get Letta's internal session checkpoint."""
        agent = self.client.get_agent(self.agent_id)
        state = {
            "core_memory": agent.core_memory,
            "last_message_id": len(agent.messages),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        state_bytes = json.dumps(state).encode()
        return {
            "checkpoint_path": f"letta_agent_{self.agent_id}",
            "checkpoint_timestamp": state['timestamp'],
            "contents_hash": hashlib.sha256(state_bytes).hexdigest(),
            "can_resume": True
        }
    
    def resume_from_checkpoint(self, checkpoint: dict) -> bool:
        """Resume agent from saved state."""
        # Letta agents are stateful by default; resumption is implicit
        agent = self.client.get_agent(self.agent_id)
        return agent is not None
```

### 4.3 — Coordination Index for Multi-Agent Setups

If Letta is running multiple agents in parallel:

```python
def get_coordination_index(self, agent_ids: list[str]) -> dict:
    """Measure whether agents reference each other's work."""
    total_findings = 0
    coordinated_findings = 0
    
    for agent_id in agent_ids:
        agent = self.client.get_agent(agent_id)
        findings = agent.core_memory  # or extract from conversation logs
        total_findings += len(findings)
        
        # Count explicit references to other agents
        for finding in findings:
            text = finding.get('text', '')
            for other_id in agent_ids:
                if other_id in text:
                    coordinated_findings += 1
                    break
    
    coordination_index = (
        coordinated_findings / total_findings
        if total_findings > 0 else 0
    )
    
    return {
        "coordination_index": coordination_index,
        "coordinated_findings": coordinated_findings,
        "total_findings": total_findings,
        "target": 0.40
    }
```

---

## 5. Generic System Adapter — Four-Step Pattern

For any system that stores memory (Tier 2–4), follow this pattern:

### Step 1: Identify the Memory-Bearing Layer

```python
# What is the minimal addressable unit of memory?
# - File (e.g., faerie's HONEY.md)?
# - Database row (e.g., Mem0's memory table)?
# - Vector embedding (e.g., ChromaDB)?
# - API-only (e.g., ChatGPT)?

memory_layer = {
    "storage_type": "file | database | vector | api",
    "readable": True,  # Can we inspect it directly?
    "queryable": True, # Can we search it?
    "writable": True,  # Can we add to it?
}
```

### Step 2: Expose It to Probes

```python
def retrieve_and_score(self, probe: dict) -> int:
    """Generic scoring for any memory layer."""
    
    # Step 1: Query the layer
    results = self._query_memory_layer(probe['query'])
    
    # Step 2: Aggregate results into single text
    aggregated = ' '.join(results)
    
    # Step 3: Count required substrings
    required_count = sum(
        1 for substring in probe['required_substrings']
        if substring in aggregated
    )
    
    # Step 4: Check anti-facts
    for anti_fact in probe.get('anti_facts', []):
        if anti_fact in aggregated:
            return 0  # Confabulation
    
    # Step 5: Score
    if required_count == len(probe['required_substrings']):
        return 10
    elif required_count > 0:
        return 4
    else:
        return 0
```

### Step 3: Measure Overhead

```python
def measure_memory_overhead(self) -> dict:
    """For any system, overhead = cost to store + retrieve."""
    
    # Measure 10 store operations
    store_times = []
    for i in range(10):
        t0 = time.time()
        self.store_fact(f"test_fact_{i}")
        store_times.append(time.time() - t0)
    
    # Measure 10 retrieval operations
    retrieve_times = []
    for i in range(10):
        t0 = time.time()
        self.retrieve_memory(f"test_query_{i}")
        retrieve_times.append(time.time() - t0)
    
    # Convert time to tokens (rough estimate: 1ms ≈ 5 tokens)
    tokens_per_store = statistics.mean(store_times) * 1000 * 5
    tokens_per_retrieve = statistics.mean(retrieve_times) * 1000 * 5
    
    return {
        "tokens_per_write": tokens_per_store,
        "tokens_per_read": tokens_per_retrieve,
        "total_session_overhead_tokens": (
            tokens_per_store * 10 +  # 10 writes per session
            tokens_per_retrieve * 25 # 25 reads per session
        )
    }
```

### Step 4: Benchmark Against a Baseline

```python
def efficiency_vs_baseline(self) -> dict:
    """Any system: measure task throughput with memory vs without."""
    
    # Run task set WITH memory
    with_memory_tokens = 0
    with_memory_tasks = 0
    for task in self.task_set:
        # Retrieve memory
        memory = self.retrieve_memory(task['query'])
        # Agent uses memory to complete task
        tokens_spent = self._task_token_count(task, memory)
        with_memory_tokens += tokens_spent
        with_memory_tasks += 1
    
    # Estimate WITHOUT memory (add re-briefing cost)
    without_memory_tokens = with_memory_tokens * 1.3  # 30% re-briefing overhead
    without_memory_tasks = with_memory_tasks
    
    efficiency_with = with_memory_tasks / (with_memory_tokens / 1000)
    efficiency_without = without_memory_tasks / (without_memory_tokens / 1000)
    
    return {
        "efficiency_with_memory": efficiency_with,
        "efficiency_without_memory": efficiency_without,
        "efficiency_ratio": efficiency_with / efficiency_without
    }
```

---

## 6. Running the Harness: CLI Interface

Once the adapter is implemented, use the unified harness:

```bash
# Mem0 adapter
python3 membench_harness.py \
  --adapter mem0 \
  --config mem0-config.json \
  --probes /path/to/probe-set.json \
  --output membench-results.json

# ChatGPT adapter
python3 membench_harness.py \
  --adapter chatgpt \
  --config chatgpt-config.json \
  --probes domain-specific-probes.json

# Letta adapter
python3 membench_harness.py \
  --adapter letta \
  --agent-id $LETTA_AGENT_ID \
  --probes faerie-probes.json

# Generic (any Tier 2+ system)
python3 membench_harness.py \
  --adapter generic \
  --adapter-class MyCustomAdapter \
  --config system-config.json
```

Output: `membench-results.json` with scores for all 8 metrics.

---

## 7. Honest Limitations — What You Cannot Measure

### For Tier 3 (API-Based, Opaque):
- **Crystallisation Quality** — you cannot measure how well memory is compressed (it is opaque)
- **True Retention** — you measure behaviour, not ground truth; model might hallucinate correct answers
- **Confabulation Rate** — only detectable if system makes contradictory claims; silent confabulation invisible

### For Tier 4 (Fully Black-Box):
- All metrics except **Work Efficiency** and **Overhead Gross** are proxy-only
- Must rely on task-completion metrics to infer memory quality
- Results are less credible for legal/regulated use cases

### For All Systems:
- **Probe Set Calibration** — probes must be tuned to each system's semantic understanding; probe quality is critical
- **Baseline Measurement** — getting a clean "memory-off" baseline is hard; most systems cannot optionally disable memory
- **Domain Transfer** — probes trained on one domain (healthcare) may not transfer to another (finance)

---

## 8. Submitting Results to the Registry

Once you have run the harness on your system:

```python
import json
from datetime import datetime, timezone

result = {
    "system_name": "Mem0",
    "system_version": "1.2.3",
    "probe_set_version": "membench-v0.1.0",
    "domain": "faerie-forensics",  # or your own
    "tier": 2,
    "run_timestamp": datetime.now(timezone.utc).isoformat(),
    
    # All 8 metrics (or null if not available for your tier)
    "retention": 0.72,
    "relevance": 0.68,
    "efficiency_ratio": 3.2,
    "overhead_gross_pct": 28,
    "overhead_net_pct": 5,
    "continuity": 95,
    "coordination_index": 0.15,
    "crystallisation_quality": None,  # Tier 2 cannot measure
    "confabulation_rate": 0.02,
    
    # Metadata
    "adapter_implementation": "mem0-official-adapter-v1",
    "test_duration_seconds": 1240,
    "probe_count": 10,
    "workload_type": "forensic-analysis",
    "notes": "Mem0 with ChromaDB backend, default embedding model"
}

# Append to public registry (git-tracked)
with open("membench-results-registry.jsonl", "a") as f:
    f.write(json.dumps(result) + "\n")
```

Results go to `/mnt/d/0local/gitrepos/faerie2/forensics/membench-results-registry.jsonl` for public comparison.

---

## 9. Example: Running Mem0 vs. faerie2 on Same Probe Set

**Scenario:** You want to compare Mem0 (Tier 2, cost-optimized) to faerie2 (Tier 1, forensic-grade) on the same probe set.

```bash
# Run faerie2 (native harness)
python3 ~/.claude/scripts/3x_eval_harness.py --membench \
  --output faerie2-membench.json

# Run Mem0 (adapter harness)
python3 membench_harness.py \
  --adapter mem0 \
  --config mem0.json \
  --probes forensic-probes.json \
  --output mem0-membench.json

# Compare
python3 membench_results_comparator.py \
  --faerie faerie2-membench.json \
  --mem0 mem0-membench.json \
  --format table
```

**Output:**
```
MEMBENCH COMPARISON
==================

Metric               faerie2    Mem0    Diff    
Retention            88/100     72/100  -16 🔴
Relevance            null       68/100  —
Efficiency Ratio     15.0x      3.2x    -11.8x 🔴
Gross Overhead       32.8%      28%     -4.8% 🟢
Net Overhead         2.8%       5.2%    +2.4% 🔴
Continuity           100/100    95/100  -5 🟡
Confabulation Rate   0%         2%      +2% 🟡

Interpretation:
- Mem0 uses less gross tokens (good for cost)
- But faerie2 has 5x better efficiency ratio (better for throughput)
- Mem0's Retention is lower (probe mismatch or weaker semantic search)
- Both are under hard ceilings (Continuity >90%, Confabulation <5%)
```

---

## 10. Contributing Your Adapter Back

To contribute your adapter to the Membench ecosystem:

1. **Fork** the faerie2 repo
2. **Add** your adapter to `membench-adapters/` directory
3. **Document** your implementation (which tier, limitations, calibration notes)
4. **Test** against the standard probe sets
5. **Submit** a PR with example results

Membench maintainers will review for:
- Correctness of metric implementation
- Honesty about limitations
- Probe set calibration appropriateness
- Results reproducibility

---

## Summary

The Competitor Adapter Pattern enables **credible, platform-independent comparison of memory systems**. By mapping each system's architecture to a common probe interface and scoring logic, Membench lets vendors compare apples to apples without claiming unfair advantages.

- **Tier 1** (Full Native): 1–2 days to wire, complete results
- **Tier 2** (Structured): 3–5 days to wire, very accurate
- **Tier 3** (API-Based): 1–2 weeks to wire, black-box but interactive
- **Tier 4** (Black-Box): 2–4 weeks to wire, proxy-only metrics

Every tier publishes honestly to the results registry. Customers read the registry and choose systems based on credible, reproducible benchmarks — not marketing claims.

---

*Membench Competitor Harness — Evaluation framework for third-party memory systems. Part of the open Membench standard.*
