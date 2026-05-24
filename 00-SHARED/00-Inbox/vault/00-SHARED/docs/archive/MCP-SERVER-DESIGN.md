# faerie MCP Server — Design & Deployment

**Status:** ✅ Deployed on ZimaBoard (ZimaOS)  
**Repo:** `vps-mcp/` in faerie repo  
**Target:** Claude Code CLI + Desktop App integration

---

## ⚠️ Deprecation Notice (2026-04-12)

The following tools from the original design are **NOT YET IMPLEMENTED**:

| Deprecated Tool | Reason |
|-----------------|--------|
| `queue.claim` | → Use `faerie_run` |
| `queue.complete` | → Use `faerie_queue_add` |
| `queue.fail` | Not implemented |
| `queue.list` | → Use `faerie_queue_list` |
| `memory.read` | Not implemented |
| `memory.append` | Not implemented |
| `eval.status` | Not implemented |
| `eval.run` | Not implemented |
| `agent.spawn` | Not implemented |
| `agent.roster` | Not implemented |

---

## ✅ Active Tools (v0.5.0)

Deployed on ZimaOS at `http://<zima-ip>:38080/mcp`

### Free Tier (50 req/day)

| Tool | Description |
|------|-------------|
| `faerie_status` | System health + queue summary |
| `faerie_queue_list` | List pending tasks with filters |
| `faerie_dashboard` | Structured dashboard data |

### Pro Tier (unlimited)

| Tool | Description |
|------|-------------|
| `faerie_run` | Claim and start next queued task |
| `faerie_queue_add` | Add task to sprint queue |
| `faerie_decide` | Process "1y 2n 3q" decisions |

---

## Getting a Token

```bash
# On ZimaOS
curl -X POST http://localhost:38081/tokens/free \
  -H "Content-Type: application/json" \
  -d '{"email": "you@email.com"}'

# Check token status
curl http://localhost:38081/tokens/<token>/status
```

---

## Configuration

In `mcp.json`:

```json
{
  "mcpServers": {
    "faerie": {
      "url": "http://<zima-ip>:38080/mcp",
      "headers": {
        "Authorization": "Bearer <token>"
      }
    }
  }
}
```

---

## Deployment

### ZimaOS (Recommended)

See: `vps-mcp/ZIMAOS-DEPLOY.md`

```bash
# SSH into ZimaBoard
ssh casaos@zimaos.local

# Setup
cd ~/AppData/faerie-mcp
export DOCKER_CONFIG=~/AppData/faerie-mcp/.docker
docker compose up -d
```

### Local Development

```bash
cd vps-mcp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Terminal 1: MCP server
python server.py

# Terminal 2: Token API
python token_api.py
```

---

## Adding New Tools

Edit `server.py` and add to `PRO_ONLY_TOOLS` in `auth.py`:

```python
@mcp.tool()
async def faerie_my_tool(ctx: Context, param: str) -> dict[str, Any]:
    """Description. TIER: pro"""
    _check_auth(ctx, "faerie_my_tool")
    # ... implementation
    return {"ok": True}
```

---

*Updated: 2026-04-12*