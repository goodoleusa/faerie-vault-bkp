---
created: 2026-04-12
tags:
  - faerie
  - mcp
  - zimaos
  - deployment
---

# ZimaOS MCP Deployment — Docker Config Fix

**Date:** 2026-04-12

## Problem

Docker on ZimaOS fails with:
```
mkdir /root/.docker: read-only file system
```

ZimaOS has a read-only root filesystem. Docker by default tries to write config to `/root/.docker`.

## Solution

Set `DOCKER_CONFIG` to a writable location (AppData):

```bash
export DOCKER_CONFIG=~/AppData/faerie-mcp/.docker
mkdir -p $DOCKER_CONFIG
docker compose up -d --build
```

**Persist in shell:**
```bash
echo 'export DOCKER_CONFIG=~/AppData/faerie-mcp/.docker' >> ~/.bashrc
```

## Key Paths

- **AppData:** `~/AppData/faerie-mcp` → `/DATA/.media/sda/AppData/faerie-mcp`
- **Docker config:** `~/.docker` (moved to AppData)
- **MCP ports:** 38080 (server), 38081 (token API)

## Status

✅ Deployed and running on ZimaBoard2