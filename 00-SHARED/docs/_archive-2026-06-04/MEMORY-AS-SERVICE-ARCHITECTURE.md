---
type: architecture
status: active
created: 2026-04-21
tags: [memory-service, architecture, saas]
up: README.md
prev: MODEL-ROUTING.md
next: SPAWN-BOILERPLATE-INJECTION-ARCHITECTURE.md
---

> [↑ Readme](README.md) · [← Model Routing](MODEL-ROUTING.md) · [→ Spawn Boilerplate Injection Architecture](SPAWN-BOILERPLATE-INJECTION-ARCHITECTURE.md) · [⌂ Home](../README.md)

# Memory Architecture as Hosted Service

Transform faerie from a local .claude orchestration system into a production-grade **memory service platform** that any agent (Claude Code, Agent SDK, third-party) can integrate with.

## Current State: Local Setup

```
~/.claude/                    (local filesystem)
├── HONEY.md                  (crystallized knowledge)
├── NECTAR.md                 (append-only findings log)
├── memory/
│   ├── REVIEW-QUEUE.json     (HIGH flags, atomic)
│   ├── forensics/            (COC logs, immutable)
└── hooks/
    └── state/                (wave manifests, stigmergy)

{repo}/.claude/
├── HONEY.md                  (project-specific facts)
└── memory/
    └── pollen-{SID}.md       (session working notes)

Vault (Obsidian)
├── 00-SHARED/ONBOARDING/     (daily session output)
├── Droplets/                 (anti-evaporation insights)
└── 01-Memories/agents/       (trained agent cards)
```

**Limitations:**
- Single-machine (WSL-bound)
- Filesystem-dependent (no cloud sync)
- Manual Obsidian sync (Syncthing = eventually consistent)
- No multi-tenant isolation
- No API access for third-party agents
- No persistent training record (only local agent cards)
- Forensic COC chain is local-only (S3 backup is manual)

---

## Target State: Hosted Service

```
                    Claude Code CLI                  Agent SDK (Python/TS)      Third-party Agents
                          │                                  │                           │
                          └──────────────────────────────────┼───────────────────────────┘
                                                             │
                                          ┌──────────────────▼──────────────────┐
                                          │     Memory Service API (REST)      │
                                          │  (Anthropic-hosted or self-hosted)  │
                                          └──────────────────┬──────────────────┘
                                                             │
                    ┌────────────────────────────────────────┼────────────────────────────────────┐
                    │                                        │                                    │
         ┌──────────▼────────────┐         ┌────────────────▼──────────────┐      ┌──────────────▼─────────┐
         │  Memory Core Service  │         │   Forensic COC Service       │      │  Vector / Embeddings  │
         │  (HONEY/NECTAR/Pollen)│         │   (Hash Chain Authority)     │      │  (Semantic Search)    │
         └──────────┬────────────┘         └────────────┬──────────────────┘      └──────────┬─────────────┘
                    │                                    │                                    │
         ┌──────────▼────────────────────────────────────▼────────────────────────────────────▼──────────┐
         │                    Persistent Data Layer (PostgreSQL + S3)                                    │
         ├─────────────────────────────────────────────────────────────────────────────────────────────┤
         │ • Documents (HONEY, NECTAR, pollen)     • Training records (agent cards, OTJ redemptions)   │
         │ • Forensic logs (COC chain, hash manifest)                                                   │
         │ • Session state (wave results, manifests)                                                    │
         │ • Vault sync (Obsidian ↔ Backend)       • Vector embeddings (for semantic search)          │
         │ • Multi-tenant isolation (by org/user)                                                       │
         └────────────────────────────────┬───────────────────────────────────────────────────────────┘
                                          │
         ┌────────────────────────────────▼───────────────────────────────────┐
         │           Sync & Integration Layer                                  │
         ├──────────────────────────────────────────────────────────────────────┤
         │ • Vault mirror (Obsidian → Backend via webhook)                     │
         │ • S3/B2 backup (immutable archive of forensic logs)                 │
         │ • CLI bridge (claude-docs skill ↔ backend memory API)              │
         │ • SDK integrations (Python, TypeScript, Go clients)                 │
         └──────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Memory Service API (REST + gRPC)

**Purpose:** Expose memory operations over HTTP/gRPC so agents don't need filesystem access.

#### Endpoints

```
# Read memory (GET)
GET /v1/users/{org_id}/memory/honey
GET /v1/users/{org_id}/memory/nectar?last_n=30
GET /v1/users/{org_id}/memory/review-queue
GET /v1/users/{org_id}/droplets?date=2026-04-21&category=HEADLINE

# Write memory (POST/PUT)
POST /v1/users/{org_id}/memory/pollen
  { "session_id": "...", "mem_block": {...} }

PUT /v1/users/{org_id}/memory/honey/entry/{key}
  { "content": "...", "section": "principles" }

POST /v1/users/{org_id}/memory/high-flag
  { "id": "...", "content": "...", "priority": "HIGH" }

# Forensic operations (append-only)
POST /v1/users/{org_id}/forensics/append
  { "event": "agent_run", "hash_before": "...", "hash_after": "..." }

GET /v1/users/{org_id}/forensics/coc-chain?since=hash_id

# Context bundle (for spawning agents)
GET /v1/users/{org_id}/context/bundle?session_id=...&agent_type=...
  Returns: { honey, nectar_tail_30, review_hot, agent_card }

# Training & scoring
POST /v1/users/{org_id}/agents/{agent_type}/training
  { "score": 0.92, "technique": "...", "baseline": 0.90 }

GET /v1/users/{org_id}/agents/{agent_type}/card
  Returns: Full agent card (public + private sections)
```

#### Authentication

- **API Key** (for backend services)
- **OAuth2** (for SaaS user accounts)
- **Service Account** (for Agent SDK integration)

#### Rate Limiting

- Standard: 100 req/sec per user
- Pro: 1000 req/sec per user
- Enterprise: custom

---

### 2. Data Model (PostgreSQL Schema)

```sql
-- Multi-tenant namespace
CREATE TABLE organizations (
  id UUID PRIMARY KEY,
  name TEXT,
  created_at TIMESTAMP,
  tier VARCHAR(10)  -- free, pro, enterprise
);

-- Users within org
CREATE TABLE users (
  id UUID PRIMARY KEY,
  org_id UUID REFERENCES organizations,
  name TEXT,
  email TEXT,
  created_at TIMESTAMP
);

-- Core memory documents
CREATE TABLE memory_documents (
  id UUID PRIMARY KEY,
  org_id UUID REFERENCES organizations,
  user_id UUID REFERENCES users,
  doc_type VARCHAR(50),  -- honey | nectar | pollen | agent_card
  content TEXT,
  section VARCHAR(100),  -- for HONEY: principles, memory-hierarchy, flow
  hash_sha256 TEXT,      -- content hash for COC chain
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  version INT            -- for concurrency control
);

-- Session memory (pollen)
CREATE TABLE pollen_entries (
  id UUID PRIMARY KEY,
  session_id VARCHAR(50),
  agent_type VARCHAR(50),
  mem_block JSONB,       -- { category, priority, content, files }
  created_at TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- Sessions
CREATE TABLE sessions (
  id VARCHAR(50) PRIMARY KEY,
  org_id UUID,
  user_id UUID,
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  status VARCHAR(20),    -- in-progress | completed | failed
  manifest JSONB         -- final manifest from session end
);

-- Agent training & scoring
CREATE TABLE agent_training_records (
  id UUID PRIMARY KEY,
  org_id UUID,
  agent_type VARCHAR(50),
  score FLOAT,
  baseline FLOAT,
  technique TEXT,        -- what improved the score
  source VARCHAR(20),    -- self | evalbot | otj_redemption
  created_at TIMESTAMP
);

-- Forensic COC chain
CREATE TABLE forensic_entries (
  id UUID PRIMARY KEY,
  org_id UUID,
  event_type VARCHAR(50),  -- agent_run | memory_write | hash_update
  hash_before TEXT,
  hash_after TEXT,
  prev_entry_id UUID REFERENCES forensic_entries(id),  -- chain link
  operator VARCHAR(50),   -- agent_type or user_name
  metadata JSONB,
  created_at TIMESTAMP,
  signed_by TEXT         -- PGP signature if required
);

-- Droplets (anti-evaporation)
CREATE TABLE droplets (
  id UUID PRIMARY KEY,
  org_id UUID,
  agent_type VARCHAR(50),
  agent_id VARCHAR(8),
  category VARCHAR(50),  -- OBSERVATION | CONNECTION | HEADLINE
  priority VARCHAR(10),  -- HIGH | MED | LOW
  content TEXT,
  file_path TEXT,        -- where written in vault
  created_at TIMESTAMP
);

-- Vault sync state
CREATE TABLE vault_sync (
  id UUID PRIMARY KEY,
  org_id UUID,
  file_path TEXT,
  local_hash TEXT,       -- Obsidian side
  backend_hash TEXT,     -- Service side
  last_sync TIMESTAMP,
  sync_direction VARCHAR(10),  -- local_to_backend | backend_to_local
  conflict_resolution VARCHAR(50)  -- last_write_wins | merge | manual
);

-- API audit log
CREATE TABLE api_audit_log (
  id UUID PRIMARY KEY,
  org_id UUID,
  user_id UUID,
  endpoint TEXT,
  method VARCHAR(10),
  status_code INT,
  request_hash TEXT,
  response_hash TEXT,
  created_at TIMESTAMP
);
```

---

### 3. Core Service: Memory Manager

```python
# pseudocode — actual implementation uses FastAPI + SQLAlchemy

class MemoryService:
    """Unified interface to all memory operations."""
    
    async def get_honey(self, org_id: str) -> str:
        """Fetch HONEY.md for context loading."""
        return await db.query(
            "SELECT content FROM memory_documents "
            "WHERE org_id = ? AND doc_type = 'honey' "
            "ORDER BY updated_at DESC LIMIT 1",
            org_id
        )
    
    async def get_nectar_tail(self, org_id: str, n: int = 30) -> List[str]:
        """Fetch last N entries from NECTAR (append-only)."""
        return await db.query(
            "SELECT content FROM memory_documents "
            "WHERE org_id = ? AND doc_type = 'nectar' "
            "ORDER BY created_at DESC LIMIT ?",
            org_id, n
        )
    
    async def write_pollen(
        self, 
        org_id: str, 
        session_id: str, 
        mem_block: dict
    ) -> None:
        """Append MEM block to session pollen."""
        await db.insert("pollen_entries", {
            "session_id": session_id,
            "org_id": org_id,
            "mem_block": mem_block,
            "created_at": now()
        })
    
    async def promote_pollen_to_nectar(
        self, 
        org_id: str, 
        session_id: str
    ) -> None:
        """At /handoff: promote session pollen → NECTAR."""
        pollen = await db.query(
            "SELECT mem_block FROM pollen_entries WHERE session_id = ?",
            session_id
        )
        
        # Append all HIGH-priority entries to NECTAR
        for block in pollen:
            if block["priority"] == "HIGH" or block["cat"] == "HEADLINE":
                await db.insert("memory_documents", {
                    "org_id": org_id,
                    "doc_type": "nectar",
                    "content": block,
                    "hash_sha256": sha256(block)
                })
    
    async def append_forensic_entry(
        self,
        org_id: str,
        event_type: str,
        hash_before: str,
        hash_after: str,
        operator: str
    ) -> None:
        """Hash-chained append to forensic log."""
        prev_entry = await db.query(
            "SELECT id, hash_after FROM forensic_entries "
            "WHERE org_id = ? ORDER BY created_at DESC LIMIT 1",
            org_id
        )
        
        entry = {
            "org_id": org_id,
            "event_type": event_type,
            "hash_before": hash_before,
            "hash_after": hash_after,
            "prev_entry_id": prev_entry[0]["id"] if prev_entry else None,
            "operator": operator,
            "created_at": now()
        }
        
        # Verify chain: prev.hash_after == entry.hash_before (optional, can be warn-only)
        if prev_entry and prev_entry[0]["hash_after"] != hash_before:
            log_warning(f"Forensic chain gap detected for {org_id}")
        
        await db.insert("forensic_entries", entry)
    
    async def get_context_bundle(
        self,
        org_id: str,
        agent_type: str,
        session_id: str
    ) -> dict:
        """Build context bundle for agent spawn.
        
        This is what faerie currently injects inline.
        Now it's generated server-side, reducing client burden.
        """
        honey = await self.get_honey(org_id)
        nectar_tail = await self.get_nectar_tail(org_id, n=30)
        review_hot = await self.get_review_queue_hot(org_id)
        
        # Fetch agent card (PRIVATE section hidden from subagent)
        agent_discovery = await db.query(
            "SELECT content FROM memory_documents "
            "WHERE org_id = ? AND doc_type = 'agent_discovery' "
            "AND metadata->>'agent_type' = ? "
            "ORDER BY updated_at DESC LIMIT 1",
            org_id, agent_type
        )
        
        return {
            "session_id": session_id,
            "agent_type": agent_type,
            "honey": honey,
            "nectar_tail_30": nectar_tail,
            "review_hot": review_hot,
            "agent_discovery": agent_discovery,  # PUBLIC only
            "generated_at": now()
        }
    
    async def record_agent_training(
        self,
        org_id: str,
        agent_type: str,
        score: float,
        baseline: float,
        technique: str,
        source: str  # "self" | "evalbot" | "otj_redemption"
    ) -> None:
        """Record agent training outcome (OTJ or eval)."""
        await db.insert("agent_training_records", {
            "org_id": org_id,
            "agent_type": agent_type,
            "score": score,
            "baseline": baseline,
            "technique": technique,
            "source": source,
            "created_at": now()
        })
        
        # Update agent card with last training
        if score > baseline:
            await db.update("memory_documents", 
                where={"org_id": org_id, "doc_type": "agent_card", 
                       "metadata->>'agent_type'": agent_type},
                values={
                    "content": {...updated card...},
                    "hash_sha256": sha256({...updated card...})
                }
            )
```

---

### 4. Vault Sync Service

Keep Obsidian vault in sync with backend (one source of truth: backend, vault = read-only replica).

```python
class VaultSyncService:
    """Two-way sync between Obsidian vault and backend memory."""
    
    async def webhook_on_vault_change(
        self,
        org_id: str,
        file_path: str,
        file_hash: str,
        operation: str  # created | modified | deleted
    ) -> None:
        """Called when Obsidian syncs file via Syncthing."""
        
        backend_hash = await db.query(
            "SELECT backend_hash FROM vault_sync "
            "WHERE org_id = ? AND file_path = ?",
            org_id, file_path
        )
        
        if operation == "modified":
            if file_hash == backend_hash:
                # No change, skip
                return
            
            # File changed locally — read new content
            content = await read_vault_file(file_path)
            
            # Determine which memory doc this is (HONEY, NECTAR, pollen, etc.)
            doc_type = classify_vault_file(file_path)
            
            # Update backend
            await db.update("memory_documents",
                where={"org_id": org_id, "doc_type": doc_type},
                values={"content": content, "hash_sha256": sha256(content)}
            )
            
            # Record sync event
            await db.update("vault_sync",
                where={"org_id": org_id, "file_path": file_path},
                values={
                    "local_hash": file_hash,
                    "backend_hash": sha256(content),
                    "last_sync": now(),
                    "sync_direction": "local_to_backend"
                }
            )
    
    async def push_backend_to_vault(
        self,
        org_id: str,
        doc_type: str
    ) -> None:
        """Periodically push backend changes back to vault.
        
        Triggered by:
        - /handoff (pollen → NECTAR promotion)
        - Agent training record (update agent card)
        - COC entry appended (update forensic manifest)
        """
        
        # Fetch latest doc from backend
        content = await db.query(
            "SELECT content, hash_sha256 FROM memory_documents "
            "WHERE org_id = ? AND doc_type = ? "
            "ORDER BY updated_at DESC LIMIT 1",
            org_id, doc_type
        )
        
        # Map to vault file path
        vault_path = map_doc_to_vault_path(doc_type)
        
        # Write to vault
        await write_vault_file(vault_path, content)
        
        # Update sync state
        await db.update("vault_sync",
            where={"org_id": org_id, "file_path": vault_path},
            values={
                "backend_hash": content["hash_sha256"],
                "last_sync": now(),
                "sync_direction": "backend_to_local"
            }
        )
```

---

### 5. Forensic COC Service (Immutable Authority)

```python
class ForensicCOCService:
    """Maintain hash-chained forensic log as system of record."""
    
    async def verify_chain(self, org_id: str) -> dict:
        """Verify COC chain integrity (no gaps, correct hash linking)."""
        entries = await db.query(
            "SELECT id, hash_before, hash_after, prev_entry_id FROM forensic_entries "
            "WHERE org_id = ? ORDER BY created_at ASC",
            org_id
        )
        
        gaps = []
        prev = None
        
        for entry in entries:
            if prev and prev["hash_after"] != entry["hash_before"]:
                gaps.append({
                    "prev_id": prev["id"],
                    "entry_id": entry["id"],
                    "gap": f"{prev['hash_after']} != {entry['hash_before']}"
                })
            prev = entry
        
        return {
            "org_id": org_id,
            "total_entries": len(entries),
            "chain_intact": len(gaps) == 0,
            "gaps": gaps,
            "verified_at": now()
        }
    
    async def export_coc_chain(
        self,
        org_id: str,
        start_hash: str = None
    ) -> str:
        """Export COC chain as signed document for audit/legal."""
        
        query = "SELECT * FROM forensic_entries WHERE org_id = ? "
        params = [org_id]
        
        if start_hash:
            query += "AND hash_before >= ? "
            params.append(start_hash)
        
        entries = await db.query(query + "ORDER BY created_at ASC", *params)
        
        # Format as JSON-L (one entry per line, immutable)
        coc_doc = "\n".join(json.dumps(e) for e in entries)
        
        # Sign with PGP if org requires it
        if await org_requires_pgp_signature(org_id):
            coc_doc = await pgp_sign(coc_doc, org_id)
        
        return coc_doc
```

---

### 6. Client SDKs

#### Python SDK

```python
from faerie_memory import MemoryClient

client = MemoryClient(
    api_key="sk_...",
    org_id="org_123",
    base_url="https://memory.faerie.ai"  # or self-hosted
)

# Read memory at agent startup
honey = await client.get_honey()
nectar = await client.get_nectar_tail(n=30)
review_hot = await client.get_review_queue_hot()

# Write session observations
await client.write_pollen(
    session_id="sess_abc123",
    mem_block={
        "category": "OBSERVATION",
        "priority": "HIGH",
        "content": "Found bug in auth.py",
        "files": ["src/auth.py:42"]
    }
)

# At /handoff: promote pollen → NECTAR
await client.promote_pollen_to_nectar(session_id="sess_abc123")

# Record training
await client.record_training(
    agent_type="code-reviewer",
    score=0.92,
    baseline=0.90,
    technique="added security check for SQL injection",
    source="otj_redemption"  # on-the-job learning
)

# Fetch context bundle for spawning agent
bundle = await client.get_context_bundle(
    agent_type="security-auditor",
    session_id="sess_xyz"
)
```

#### TypeScript SDK

```typescript
import { MemoryClient } from "@faerie/memory-sdk";

const client = new MemoryClient({
  apiKey: "sk_...",
  orgId: "org_123",
  baseUrl: "https://memory.faerie.ai"
});

// Same API, Promise-based
const honey = await client.getHoney();
const nectar = await client.getNectarTail({ n: 30 });

await client.writePollen({
  sessionId: "sess_abc123",
  memBlock: {
    category: "HEADLINE",
    priority: "HIGH",
    content: "Security vulnerability discovered",
    files: ["src/payment.ts:105"]
  }
});
```

---

## Deployment Topology

### Option 1: Anthropic-Hosted (SaaS)

```
User's Claude Code CLI / Agent SDK
        ↓
  api.faerie.claude.com  (Anthropic-hosted)
        ↓
  ┌─────────────────────┐
  │ PostgreSQL (RDS)    │  Multi-tenant database
  │ S3 (forensic logs)  │  Immutable archive
  │ Vector DB (Pinecone)│  Semantic search
  └─────────────────────┘
        ↓
  Vault Mirror (Syncthing)
        ↓
  User's Obsidian Vault (Read-only replica)
```

**Pricing:**
- Free: 5K memory entries/month, 1 org, 1 user
- Pro: 100K entries/month, 3 orgs, 10 users per org — $29/mo
- Enterprise: Custom, dedicated instance, compliance support

### Option 2: Self-Hosted (Open Source)

```
User's Claude Code CLI / Agent SDK
        ↓
  docker-compose up  (faerie-memory-service)
        ↓
  Local PostgreSQL + S3-compatible storage
        ↓
  User's Obsidian Vault (Local sync)
```

**Included:**
- Docker Compose setup
- PostgreSQL schema + migrations
- Python/TypeScript SDKs
- CLI bridge integration
- S3/MinIO configuration

---

## Integration Points

### 1. Claude Code CLI Bridge

```
User: /claude-docs "Can I spawn agents?"

CLI:
  1. Check local .claude/HONEY.md (existing behavior)
  2. If query hits memory service: fetch latest from API
  3. If network unavailable: fallback to local cache
  
Result: Seamless — user doesn't know if they're reading local or backend
```

### 2. Agent SDK Integration

```python
from claude_agent_sdk import query
from faerie_memory import MemoryClient

async def main():
    memory = MemoryClient(api_key="...", org_id="...")
    
    # Fetch context bundle
    bundle = await memory.get_context_bundle(
        agent_type="my-agent",
        session_id="sess_123"
    )
    
    # Query Claude with memory context
    async for message in query(
        prompt="Your task here",
        context_bundle=bundle  # ← NEW: memory service as context source
    ):
        if message.type == "complete":
            # Write observations back
            await memory.write_pollen(
                session_id="sess_123",
                mem_block=message.observations
            )
```

### 3. Third-Party Agent Integration

```
Any agent (Anthropic, third-party, custom):
  1. Fetch API key from environment
  2. Call Memory Service API (REST)
  3. No SDK required — just HTTP
  
Example:
  curl -H "Authorization: Bearer sk_..." \
    https://memory.faerie.ai/v1/users/org_123/memory/honey
```

---

## Migration Path: Local → Hosted

### Phase 1: Launch Local Backend (Week 1-2)
- Spin up PostgreSQL locally
- Implement MemoryService
- Write data migration from ~/.claude → DB

### Phase 2: Deploy SaaS (Week 3-4)
- Host on cloud (AWS RDS + Lambda, or containerized on GCP/Azure)
- Implement API
- Release Python + TypeScript SDKs

### Phase 3: Vault Sync (Week 5-6)
- Two-way sync between backend + Obsidian
- Conflict resolution logic
- Webhook integration with Syncthing

### Phase 4: Third-Party Integrations (Week 7-8)
- Agent SDK integration
- Anthropic partnership (if applicable)
- Open-source release

---

## Strategic Value

### For Individual Developers
- Persistent training (never lose improvements)
- Multi-device access (Claude on Mac + Windows + Web)
- AI-native reasoning (semantic search over all your learnings)

### For Teams
- Shared memory across agents
- Audit trail (forensic COC)
- Cross-org knowledge (with permission)

### For Anthropic (Potential Partnership)
- **New product category:** Memory infrastructure for AI agents
- **Upsell:** Free tier → Pro ($29/mo) → Enterprise (custom)
- **Moat:** No competitor is solving agentic memory well
- **Network effect:** More agents using same memory service = better insights for all

---

## Next Steps

1. **Read official Claude docs:** `/claude-docs` skill now available
2. **Design phase:** Whiteboard API schema + data model ✓ (this doc)
3. **Proof of concept:** Migrate local ~/.claude to PostgreSQL
4. **MVP:** Deploy locally, test CLI + Agent SDK integration
5. **SaaS launch:** Containerize, deploy to cloud, build SDKs
6. **Scale:** Multi-tenant, pricing tiers, integrations

---

**Questions to explore:**
- Should we host this ourselves or partner with Anthropic?
- Open-source or closed-source?
- Pricing model: per-agent, per-session, storage-based, or freemium?
- Multi-tenant isolation: namespace-based (simple) or row-level security (complex)?
- Forensic COC: Local only or integrate with legal/compliance services?

**This is the bridge between faerie (orchestration) and the agent platform of the future.**
