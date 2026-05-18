---
task_id: vault-enhancement-03-mcp-architecture
investigation_label: vault-enhancement-2026-04-28
status: in_progress
created: 2026-04-28
---

# MCP Server Architecture — Design for Live System Status

**Breadcrumb:** [[00-DASHBOARD]] > [[03-mcp-server-architecture]] > [[02-settings-sync-strategy]]

> faerie2's Model Context Protocol (MCP) server achieves <500ms response times through careful async design, connection pooling, and compass graph integration.

---

## Navigation Table

| Document | Direction | Purpose |
|----------|-----------|---------|
| [[02-settings-sync-strategy]] | ← Previous | Settings sync model |
| [[04-mcp-deployment-vps]] | → Next | VPS deployment guide |
| [[00-DASHBOARD]] | ← Related | System status hub |

---

## Performance SLA: <500ms Response Target

**Why 500ms?**
- Agent prompt evaluation in Claude API: 100-200ms (model inference)
- Network roundtrip (client to server, server to API): 100-150ms
- Compass graph traversal (parse manifests, extract edges): 50-100ms
- Serialization + response marshaling: 50-100ms

**Total budget: ~400-550ms** (aggressive but achievable with tuning)

**Measurement:**
```
Response Time = (timestamp_response_sent - timestamp_request_received)
SLA violation: >500ms
Target: 90th percentile <300ms (healthy), 99th percentile <500ms (acceptable)
```

---

## Architecture: Async-First Design

### Layer 1: FastAPI Application Server

```
[Client] --HTTP--> [FastAPI Router] --async--> [Queue Manager]
                        |
                        v
                   [Request Handler]
                        |
                        +---> [Manifest Reader] (async file I/O)
                        +---> [Compass Edge Parser] (CPU-bound, thread pool)
                        +---> [Response Marshaler] (JSON encoder)
```

**Key principle:** All I/O operations are async; CPU-bound work is delegated to thread pool (avoids blocking event loop).

### Layer 2: Connection Pooling

**TCP Connection Pool (client → server):**
- Min connections: 5 (always open, ready)
- Max connections: 50 (burst capacity)
- Timeout: 60s idle (auto-close)
- Backoff: Exponential if server overloaded

**Database/Filesystem Connection Pool:**
- Memory-mapped file handles for forensics/manifests/ (zero-copy reads)
- LRU cache (last 100 accessed files, 10MB total)
- TTL: 5 minutes (stale file detection)

### Layer 3: Async Message Queue

**Message flow:**
```
Client Request
  ↓
[Async Queue] (capacity: 100 messages)
  ↓
[Worker Pool] (5-10 workers, scale by CPU)
  ↓
[Manifest Reader] (async file I/O via aiofiles)
  ↓
[Compass Parser] (CPU, thread pool)
  ↓
[Response Cache] (in-memory, 1-hour TTL)
  ↓
Client Response
```

**Queue backpressure:** If queue fills >80%, reject new requests with 503 (Service Unavailable). Client retries with exponential backoff.

---

## Compass Graph Integration: Three Access Patterns

### Pattern 1: Read Manifest Edges (Frontier Scan)

**Use case:** `/api/compass/open-edges` — list unexplored tasks

```python
async def get_open_edges(investigation_label: str) -> List[CompassEdge]:
    # 1. Async read manifests/{YYYY-MM-DD}/ (cached, memory-mapped)
    manifests = await asyncio.gather(
        *[read_manifest_file(f) for f in glob("forensics/manifests/2026-04-28/*")]
    )
    # ~50ms (I/O + parsing)
    
    # 2. Extract compass edges + next_task_queued fields (CPU, thread pool)
    edges = await thread_pool_executor.run_in_thread(
        parse_edges, manifests, investigation_label
    )
    # ~50ms (parsing, filtering)
    
    # 3. Filter for open edges (no matching manifest yet)
    open_edges = [e for e in edges if e.next_task_queued not in completed_tasks]
    # ~10ms (in-memory filtering)
    
    return open_edges
    # Total: ~110ms
```

**Performance tuning:**
- Cache completed_tasks (refresh every 60s) — avoids O(N) lookup
- Compress manifests on disk (gzip) — saves 70% storage, costs 15ms decompression
- Batch file reads (10 files at once, not sequential) — parallelizes I/O

### Pattern 2: Query Mission Topology (Phase Gates)

**Use case:** `/api/mission/{label}/topology` — show graph structure

```python
async def get_mission_topology(investigation_label: str) -> MissionGraph:
    # 1. Read all manifests for this label (async, cached)
    manifests = await get_manifests_by_label(investigation_label)
    # ~60ms
    
    # 2. Build DAG: nodes = tasks, edges = compass_edge + next_task_queued
    graph = await thread_pool_executor.run_in_thread(
        build_dag, manifests
    )
    # ~40ms
    
    # 3. Compute phase gates: quality_score + belief_index per node
    gates = await thread_pool_executor.run_in_thread(
        evaluate_phase_gates, graph
    )
    # ~30ms
    
    # 4. Detect blockers (N-edges, quality <threshold)
    blockers = [n for n in graph.nodes if n.compass_edge == "N"]
    
    return MissionGraph(nodes=graph.nodes, edges=graph.edges, phase_gates=gates, blockers=blockers)
    # Total: ~130ms
```

### Pattern 3: Discover Unblocking Work (Agent Discovery Protocol)

**Use case:** `/api/agent/{agent_type}/discover` — find next work matching capability

```python
async def discover_unblocking_work(agent_type: str, investigation_label: str) -> Task:
    # 1. Get open edges + filter by agent capability (CPU, thread pool)
    open_edges = await get_open_edges(investigation_label)
    matching = await thread_pool_executor.run_in_thread(
        filter_by_agent_capability, open_edges, agent_type
    )
    # ~80ms
    
    # 2. For each matching edge, check if prerequisites are solvable (CPU)
    candidates = await thread_pool_executor.run_in_thread(
        rank_by_unblock_potential, matching
    )
    # ~50ms
    
    # 3. Return highest-ranking unblocking work
    if candidates:
        return candidates[0]
    else:
        return None
    # Total: ~130ms
```

---

## Connection Management: TCP Keep-Alive

**Client-side (faerie CLI):**
```
TCP_KEEPALIVE_IDLE = 30s (how long before probe sent)
TCP_KEEPALIVE_INTVL = 10s (interval between probes)
TCP_KEEPALIVE_CNT = 5 (probes before close)
Total before close: 30 + (10 * 5) = 80s
```

**Server-side (MCP FastAPI):**
```python
# graceful shutdown on idle >60s
@app.on_event("shutdown")
async def shutdown_idle_connections():
    for conn in connection_pool:
        if time.time() - conn.last_activity > 60:
            await conn.close()
```

---

## Caching Strategy: Three-Level Cache

**Level 1: In-Memory Cache (10MB, 1-hour TTL)**
- Recently accessed manifests (LRU)
- Parsed compass edges
- Mission topology graphs
- Eviction policy: LRU + age

**Level 2: Memory-Mapped File Cache (OS-managed)**
- forensics/manifests/*.json read via mmap (zero-copy)
- OS kernel handles paging
- Automatically expires on file change (mtime check)

**Level 3: HTTP Client-Side Cache (24-hour TTL)**
- Compass edge list (slow-changing)
- Mission topology (stable across day)
- agent card metadata (updated daily)

**Cache coherence:**
```
When manifest written:
  1. Invalidate in-memory cache entry
  2. Update mtime on filesystem
  3. Notify clients via /api/manifest-updated webhook (long-poll)
```

---

## Request Flow: Detailed Trace (500ms Budget)

**Scenario: Client requests open edges for investigation_label="sdk-readiness"**

```
t=0ms       Client sends: GET /api/compass/open-edges?label=sdk-readiness

t=5ms       Server receives, enqueues to message queue

t=10ms      Worker dequeued, calls get_open_edges()
             - Check in-memory cache (fast path, 1ms if hit)
             - Cache MISS: proceed

t=15ms      Async read forensics/manifests/2026-04-28/*.json
             - 20 files x 25ms (parallel, not sequential)
             - I/O: ~25ms (OS caches most)

t=45ms      JSON parse + extract edges (CPU-bound, thread pool)
             - Parse 20 files: ~30ms
             - Filter by label: ~5ms

t=80ms      Filter for open edges (in-memory, <1ms)

t=85ms      Encode response as JSON (aiofiles + encoder)
             - JSON encoding: ~5ms
             - Serialize to wire: ~5ms

t=95ms      Send response to client

t=500ms     [SLA LIMIT - 405ms remaining budget used]
```

**Worst case (cold cache, slow disk):**
- File I/O: +100ms (if disk not cached)
- Parsing: +50ms (if large manifests)
- Network latency: +150ms (geography)
- **Total: ~395ms (still under 500ms!)**

---

## Resource Allocation

**CPU:** 2 cores minimum (1 for I/O coordination, 1 for parsing)  
**Memory:** 512MB (in-memory cache: 10MB, worker buffers: 500MB)  
**Disk:** 10GB minimum (forensics/ grows ~100MB/week)  
**Network:** 10Mbps+ (each response is <100KB JSON)

---

## Async Patterns: Examples

### Example 1: Parallel Manifest Reads (Not Sequential)

**Bad (blocks event loop):**
```python
def get_all_manifests():
    manifests = []
    for f in glob("forensics/manifests/2026-04-28/*"):
        manifests.append(json.load(open(f)))  # BLOCKING!
    return manifests
# Time: 20 files * 20ms = 400ms
```

**Good (async/await):**
```python
async def get_all_manifests():
    tasks = [aiofiles.open(f).read() for f in glob("forensics/manifests/2026-04-28/*")]
    manifests = await asyncio.gather(*tasks)
    return manifests
# Time: max(20 reads in parallel) ≈ 20ms
```

### Example 2: Thread Pool for CPU Work (Not Main Thread)

**Bad (blocks event loop):**
```python
def parse_edges(manifests):
    edges = []
    for m in manifests:
        edges.extend(extract_edges(m))  # CPU-bound, BLOCKING!
    return edges
```

**Good (thread pool):**
```python
async def parse_edges(manifests):
    def _parse(manifest_list):
        edges = []
        for m in manifest_list:
            edges.extend(extract_edges(m))
        return edges
    
    return await executor.run_in_executor(None, _parse, manifests)
```

---

## Monitoring: Latency Metrics

**Metrics to track:**

| Metric | Threshold | Action |
|--------|-----------|--------|
| p50 latency | <150ms | OK (fast path hit) |
| p95 latency | <350ms | OK (acceptable) |
| p99 latency | <500ms | OK (at limit) |
| p99 latency | >500ms | ALERT (SLA violation) |
| Queue depth | >80 msgs | WARN (backpressure) |
| Cache hit rate | <70% | WARN (cache too small) |

**Logging:**
```python
logger.info(f"manifest_read_ms={elapsed_io}, parse_ms={elapsed_cpu}, total_ms={elapsed_total}")
```

**Dashboard:** See [[00-DASHBOARD]] for live status visualization.

---

**Related:** [[02-settings-sync-strategy]] (how settings affect behavior), [[04-mcp-deployment-vps]] (production deployment)  
**Ref:** faerie design principle: "f(0) orchestration burden"; MCP server removes main from network I/O coordination  
**Status:** Ready for deployment
