---
type: operational-guide
status: active
created: 2026-04-29
tags: [deployment, zimaboard, operations, mcp-server, troubleshooting]
companion: "faerie2/docs/40-ZIMABOARD-DOCKER-SETUP.md"
---

# ZimaBoard Deployment — Operational Guide

**What is this?** Day-to-day operational manual for running faerie2 on ZimaBoard. Access patterns, monitoring, common issues, and recovery procedures.

**Setup?** See `faerie2/docs/40-ZIMABOARD-DOCKER-SETUP.md` (repo doc) for initial installation and Docker configuration.

**Audience:** Operators, researchers, ZimaBoard caretakers.

**Last Updated:** 2026-04-29  
**Status:** Active (v1.0)

---

## Quick Reference — Common Tasks

### Access MCP Server from Local Machine

**One-time setup (after initial deploy):**
```bash
# Create persistent SSH tunnel (runs in background)
ssh -fNL 7778:localhost:7778 user@zimaboard.local

# Verify tunnel is open
lsof -i :7778  # Should show ssh process
```

**Then:** All Claude Code commands work as if MCP server is local.

### Spawn New Investigation

```bash
# Via Claude Code (locally)
/spawn "investigation description" --investigation-label kebab-case-name

# Or via curl (if CLI unavailable)
curl -X POST http://localhost:7778/api/spawn \
  -H "Content-Type: application/json" \
  -d '{
    "investigation_label": "my-investigation",
    "wave": 1,
    "max_parallel": 2
  }'
```

### Check Agent Status

```bash
# SSH into ZimaBoard
ssh user@zimaboard.local

# View running containers
docker-compose -f /data/faerie2-deployment/docker-compose.yml ps

# View logs
docker-compose -f /data/faerie2-deployment/docker-compose.yml logs -f --tail 50

# Check if agents are working
docker-compose exec faerie2-core \
  ls -lat /forensics/manifests/$(date +%Y-%m-%d) | head -5
```

### Update Secrets (HONEY, NECTAR, Agent Cards)

```bash
# SSH into ZimaBoard
ssh user@zimaboard.local

# Update HONEY (crystallized facts)
cp /path/to/HONEY.md /data/faerie2-secrets/HONEY.md

# Update NECTAR (recent findings)
cp /path/to/NECTAR.md /data/faerie2-secrets/NECTAR.md

# Restart container to apply changes
docker-compose -f /data/faerie2-deployment/docker-compose.yml restart faerie2-core

# Verify changes were applied
docker-compose exec faerie2-core cat /secrets/HONEY.md | head -20
```

---

## Daily Operations

### Morning Check

```bash
# 1. Verify container is running
ssh user@zimaboard.local
docker-compose -f /data/faerie2-deployment/docker-compose.yml ps

# 2. Check disk space (forensics partition)
df -h /data/faerie2-forensics  # Should have >5GB free

# 3. Check recent manifests (signs of activity)
ls -lat /data/faerie2-forensics/manifests/$(date +%Y-%m-%d) | head -5

# 4. Check error logs
docker-compose logs faerie2-core 2>&1 | grep -i error | tail -10

# If everything is green: ready to spawn investigations
```

### Monitor Active Work

```bash
# Watch manifests as they're written (near real-time)
watch -n 2 "ls -lat /data/faerie2-forensics/manifests/$(date +%Y-%m-%d) | head -10"

# Or: tail container logs
docker-compose logs -f faerie2-core

# Count active agents (from recent manifests)
ls /data/faerie2-forensics/manifests/$(date +%Y-%m-%d) | wc -l
```

### Investigate Agent Output

```bash
# Read most recent manifest (agent outcome)
MANIFEST=$(ls -t /data/faerie2-forensics/manifests/$(date +%Y-%m-%d)/* | head -1)
cat "$MANIFEST" | jq '.'  # Pretty-print JSON

# Extract key fields
jq '.task_id, .dashboard_line, .compass_edge' "$MANIFEST"

# Find manifests for specific task
grep -r "task-123" /data/faerie2-forensics/manifests/$(date +%Y-%m-%d) | head -3

# Find high-quality work (quality_score > 0.75)
grep -r "quality_score" /data/faerie2-forensics/manifests/$(date +%Y-%m-%d) \
  | grep "0\.[89]\|1\.0" | head -5
```

### Clean Up Logs (Prevent Disk Bloat)

```bash
# Check log size
du -sh /data/faerie2-logs

# Docker automatically rotates (json-file driver, max 100MB per log)
# But if manual cleanup needed:
docker-compose logs --no-log-prefix > /tmp/export.log
# Then container logs are cleared on next restart
```

---

## Monitoring & Metrics

### Resource Usage

```bash
# Real-time container stats
docker stats faerie2-core --no-stream

# Expected ranges (ZimaBoard):
# CPU: 5-20% (idle), 40-80% (active agents)
# Memory: 800MB-1.5GB (relative to 4GB ZimaBoard limit)
# Net I/O: 1-10MB/s (agent API calls)

# If consistently high:
# - Scale down: reduce max_parallel in docker-compose.yml
# - Scale up: add more ZimaBoard resources (unlikely on 216-Poe)
```

### Forensics Growth

```bash
# Total forensics size
du -sh /data/faerie2-forensics

# By type
du -sh /data/faerie2-forensics/manifests
du -sh /data/faerie2-forensics/artifacts
du -sh /data/faerie2-forensics/coc-entries

# By date (oldest first)
du -sh /data/faerie2-forensics/manifests/* | sort -h

# Cleanup old investigations (after archival to B2/external storage)
# Example: remove investigations older than 30 days
find /data/faerie2-forensics -name "2026-03*" -type d | head -3  # Preview
find /data/faerie2-forensics -name "2026-03*" -type d -exec rm -rf {} \;  # Execute
```

### Mission Status at a Glance

```bash
# How many investigations are active?
ls /data/faerie2-forensics/manifests/ | wc -l

# How many manifests today?
ls /data/faerie2-forensics/manifests/$(date +%Y-%m-%d)/* 2>/dev/null | wc -l

# Which investigation has the most work?
for dir in /data/faerie2-forensics/manifests/*/; do
  count=$(grep -r "investigation_label" "$dir" 2>/dev/null | cut -d: -f2 | sort | uniq -c | head -1 | awk '{print $1}')
  label=$(grep -r "investigation_label" "$dir" 2>/dev/null | cut -d: -f2 | sort | uniq -c | head -1 | awk '{$1=""; print $0}' | xargs)
  echo "$count $label"
done | sort -rn
```

---

## Troubleshooting

### Container Won't Start

**Symptoms:** `docker-compose up -d` shows error or container exits immediately.

```bash
# 1. Check error message
docker-compose logs faerie2-core --tail 50

# 2. Common causes:
#    a) Port 7778 in use
lsof -i :7778  # Kill if needed: kill -9 <PID>

#    b) Disk full
df -h /data  # Should have >5GB free

#    c) Secrets not found
ls -la /data/faerie2-secrets  # Should have HONEY.md, NECTAR.md, keys/

#    d) Bad .env file
cat /data/faerie2-deployment/.env.production | grep -i error

# 3. Fix and restart
docker-compose down
docker-compose up -d
sleep 5
docker-compose logs faerie2-core
```

### MCP Server Not Responding

**Symptoms:** `curl http://localhost:7778/health` times out or returns 503.

```bash
# 1. Check container is running
docker-compose ps faerie2-core  # Should show "Up"

# 2. Check MCP server inside container
docker-compose exec faerie2-core curl http://localhost:7778/health

# 3. If still failing, check logs
docker-compose logs faerie2-core | grep -i "mcp\|server" | tail -20

# 4. Restart MCP server only (without restarting container)
docker-compose exec -d faerie2-core \
  python3 -m faerie2.mcp.server --port 7778 --log-level DEBUG

# 5. Verify restart worked
sleep 3
docker-compose exec faerie2-core curl http://localhost:7778/health
```

### Agents Not Running / No Manifests Written

**Symptoms:** No new manifests in `/forensics/manifests/{YYYY-MM-DD}/` despite spawning.

```bash
# 1. Check if container is healthy
docker-compose exec faerie2-core echo "Container alive"

# 2. Check if ANTHROPIC_API_KEY is set
docker-compose exec faerie2-core env | grep -i anthropic

# 3. Check if forensics directory is writable
docker-compose exec faerie2-core touch /forensics/test.txt && rm /forensics/test.txt

# 4. Check agent permissions
docker-compose exec faerie2-core ls -la /forensics/ephemeral/

# 5. Manually test agent spawn (inside container)
docker-compose exec faerie2-core \
  python3 scripts/0x_spawn.py \
    --agent-type stigmergy-scout \
    --investigation-label test-investigation \
    --bundle-path forensics/bundles/2026-04-29/test-bundle.json

# 6. If still failing, check logs
docker-compose logs faerie2-core | grep -i "error\|fail\|spawn" | tail -20
```

### SSH Tunnel Drops (Connection Resets)

**Symptoms:** `curl http://localhost:7778/` works initially, then stops working after a while.

```bash
# 1. Check if tunnel is still alive
lsof -i :7778
# If no process shown, tunnel died

# 2. Reconnect tunnel
ssh -fNL 7778:localhost:7778 user@zimaboard.local

# 3. Verify it's open
sleep 2
curl -I http://localhost:7778/health

# 4. For persistent tunnel (survives terminal close):
# Add to ~/.ssh/config on local machine:
Host zimaboard.local
  HostName zimaboard.local
  User user
  LocalForward 7778 localhost:7778
  ServerAliveInterval 60
  ServerAliveCountMax 3

# Then: ssh zimaboard.local (tunnel auto-opens)
```

### Redis Cache Issues

**Symptoms:** Errors mentioning Redis connection in container logs.

```bash
# 1. Check if redis container is running
docker-compose ps redis  # Should show "Up"

# 2. Check redis health inside container
docker-compose exec faerie2-core redis-cli -h redis ping
# Should return: PONG

# 3. If redis is down, restart it
docker-compose restart redis

# 4. Verify redis is accessible from faerie2-core
docker-compose exec faerie2-core \
  python3 -c "import redis; r = redis.Redis(host='redis'); print(r.ping())"
# Should return: True

# 5. If persistent issues, clear cache
docker-compose exec redis redis-cli FLUSHALL
docker-compose restart redis
```

### Running Out of Disk Space

**Symptoms:** `docker-compose up` fails with "No space left on device"

```bash
# 1. Check disk usage
df -h /data

# 2. Identify largest directories
du -sh /data/faerie2-* | sort -rh

# 3. Archive old investigations (before deleting)
ARCHIVE_DATE="2026-04-15"  # Cutoff: delete investigations older than this
tar czf /mnt/external-backup/forensics-$ARCHIVE_DATE.tar.gz \
  /data/faerie2-forensics/manifests/$ARCHIVE_DATE \
  /data/faerie2-forensics/artifacts/$ARCHIVE_DATE \
  /data/faerie2-forensics/coc-entries/$ARCHIVE_DATE

# 4. Verify archive is readable
tar tzf /mnt/external-backup/forensics-$ARCHIVE_DATE.tar.gz | head -10

# 5. Delete archived investigation
rm -rf /data/faerie2-forensics/manifests/$ARCHIVE_DATE
rm -rf /data/faerie2-forensics/artifacts/$ARCHIVE_DATE
rm -rf /data/faerie2-forensics/coc-entries/$ARCHIVE_DATE

# 6. Verify space is freed
df -h /data  # Should show more free space

# 7. Optional: send archive to B2 (if B2 account configured)
b2 authorize-account "$BACKBLAZE_ACCOUNT_ID" "$BACKBLAZE_API_KEY"
b2 upload-file "faerie-eval" /mnt/external-backup/forensics-$ARCHIVE_DATE.tar.gz
```

### Updating faerie2 Code

**Symptoms:** New features not available, or old bugs still present.

```bash
# 1. Stop container
docker-compose down

# 2. Pull latest code
cd /data/faerie2-deployment
git pull origin main

# 3. Rebuild image (includes latest code)
docker-compose build --no-cache faerie2-core

# 4. Restart container (forensics + secrets persist)
docker-compose up -d

# 5. Verify new code is running
docker-compose exec faerie2-core \
  python3 scripts/0x_spawn.py --version

# 6. Check logs for startup messages
docker-compose logs --tail 50
```

---

## Backup & Recovery

### Automated Backup to B2 (Cloud WORM)

faerie2 includes a background script that streams forensics artifacts to Backblaze B2 (Write-Once-Read-Many, immutable backup). Ensure credentials are in `.env`:

```bash
# In /data/faerie2-deployment/.env.production, add:
B2_ACCOUNT_ID=xxx
B2_API_KEY=xxx
B2_BUCKET_NAME=faerie-eval

# Restart container
docker-compose restart faerie2-core

# Verify uploads are happening
docker-compose logs faerie2-core | grep -i "b2\|backup" | tail -10
```

### Manual Forensics Backup

```bash
# Export full forensics directory
tar czf /mnt/backup/forensics-$(date +%Y-%m-%d).tar.gz \
  /data/faerie2-forensics

# Verify tarball integrity
tar tzf /mnt/backup/forensics-$(date +%Y-%m-%d).tar.gz | wc -l

# Copy to external storage (USB drive, NAS, etc.)
rsync -av /mnt/backup/ /mnt/nas-backup/
```

### Recovery from Backup

```bash
# If forensics directory is corrupted:

# 1. Stop container
docker-compose down

# 2. Restore from backup
rm -rf /data/faerie2-forensics
tar xzf /mnt/backup/forensics-2026-04-20.tar.gz -C /data/

# 3. Verify restoration
ls -la /data/faerie2-forensics/manifests/

# 4. Restart container
docker-compose up -d

# 5. Verify agents can read manifests
docker-compose exec faerie2-core \
  ls /forensics/manifests/2026-04-20 | wc -l
```

---

## Accessing Forensics Remotely

### Via SCP (Copy Files to Local Machine)

```bash
# Copy recent manifests
scp -r user@zimaboard.local:/data/faerie2-forensics/manifests/$(date +%Y-%m-%d) \
  ./manifests-today

# Copy specific artifacts
scp user@zimaboard.local:/data/faerie2-forensics/artifacts/2026-04-29/* \
  ./artifacts/
```

### Via SSH Port Forward (Read-Only Access)

```bash
# Forward forensics directory via SFTP
ssh -fNL 2222:zimaboard.local:22 user@zimaboard.local

# Mount via SSHFS (macOS/Linux)
sshfs -p 2222 user@127.0.0.1:/data/faerie2-forensics ./zimaboard-forensics

# Browse locally
ls -la zimaboard-forensics/manifests/
cat zimaboard-forensics/manifests/2026-04-29/manifest.json | jq '.'

# Unmount when done
umount ./zimaboard-forensics
```

---

## Performance Tuning

### Increasing Parallelism (More Agents)

```bash
# Edit docker-compose.yml command section:
# Change:
# --max-parallel 2

# To:
# --max-parallel 4

# Then restart:
docker-compose down
docker-compose up -d

# Monitor memory usage (should stay under 2GB)
docker stats faerie2-core --no-stream
```

### Reducing Memory Usage (If Container Crashes)

```bash
# Decrease allocated RAM in docker-compose.yml:
# Change deploy.resources.limits.memory from 2G to 1.5G

# Restart:
docker-compose down
docker-compose up -d

# Verify it starts cleanly
docker-compose logs faerie2-core
```

### Speeding Up Agent Spawning

```bash
# Use lighter model for W1 (triage phase):
# In docker-compose.yml, ensure:
# --model haiku  (cheap, fast)

# For W2/W3, use sonnet:
# --model sonnet  (slower, smarter)

# Check model usage in manifests:
grep -r "model" /data/faerie2-forensics/manifests/$(date +%Y-%m-%d) | head -5
```

---

## Periodic Maintenance

### Weekly

```bash
# Check disk usage
df -h /data/faerie2-forensics

# Archive logs (if not auto-rotated)
docker-compose logs > /tmp/faerie2-weekly-$(date +%Y-%m-%d).log

# Verify recent manifests are being written
ls -l /data/faerie2-forensics/manifests/$(date +%Y-%m-%d) | tail -5
```

### Monthly

```bash
# Update HONEY and NECTAR from vault
cp /vault-path/HONEY.md /data/faerie2-secrets/HONEY.md
cp /vault-path/NECTAR.md /data/faerie2-secrets/NECTAR.md
docker-compose restart faerie2-core

# Backup forensics to external storage
tar czf /mnt/backup/forensics-monthly-$(date +%Y-%m).tar.gz \
  /data/faerie2-forensics

# Prune old investigations (>60 days old)
find /data/faerie2-forensics -type d -name "2026-0[12]-*" -exec rm -rf {} \;

# Check container version
docker-compose exec faerie2-core python3 scripts/0x_spawn.py --version
```

### Quarterly

```bash
# Full system audit
docker system df  # Image/container/volume usage

# Rebuild image (clears unused layers)
docker-compose build --no-cache faerie2-core

# Export evaluation report
docker-compose exec faerie2-core python3 scripts/9x_metrics_lightweight.py \
  --output /forensics/eval-quarterly-$(date +%Y-Q%q).json

# Archive full quarter's forensics
QUARTER=$(date +%Y-Q%q)
tar czf /mnt/backup/forensics-$QUARTER.tar.gz /data/faerie2-forensics
```

---

## Contact & Support

**Setup issues?** See `faerie2/docs/40-ZIMABOARD-DOCKER-SETUP.md` for initial configuration.

**Architecture questions?** See `faerie2/docs/12-ARCHITECTURE.md` for design principles.

**Emergency recovery?** Restore from backup (see Backup & Recovery section above).

---

## Glossary (Quick Reference)

| Term | Meaning |
|------|---------|
| **Manifest** | Agent outcome record (what work was done, next task) |
| **Forensics** | Immutable record of all agent work (artifacts, manifests, audit logs) |
| **MCP Server** | Claude's Model Context Protocol server; runs on ZimaBoard, accessed via SSH tunnel |
| **Investigation Label** | Kebab-case identifier grouping related work (e.g., treasury-cert-ip-origins) |
| **W1/W2/W3** | Wave tiers: W1 (LIFTOFF, many agents), W2 (CRUISE, focused), W3 (INSERTION, synthesis) |
| **Dashboard Line** | ≤80 char summary of agent outcome (displayed on terminal) |
| **Compass Edge** | N/S/E/W routing signal indicating next phase (North=unblock, South=proceed, etc.) |
| **HONEY** | Crystallized universal facts (immutable reference layer) |
| **NECTAR** | Recent HIGH/CRITICAL findings (mutable, refreshed per session) |

---

**Last Updated:** 2026-04-29 | **Version:** 1.0 | **Status:** Production
