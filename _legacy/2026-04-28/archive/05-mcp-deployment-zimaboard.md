---
type: mcp-deployment-strategy
status: archived
created: 2026-04-28
archived_date: 2026-04-30
archived_reason: "Consolidated into MCP Deployment Strategy (02-settings-sync-strategy.md)"
superseded_by: 02-settings-sync-strategy.md
canonical_url: "/2026-04-28/02-settings-sync-strategy.md#mcp-deployment-zimaboard"
tags: [mcp-deployment-zimaboard, archived]
compass_edge: W
investigation_label: vault-enhancement-2026-04-28
---

# MCP Deployment on ZimaBoard — Personal Hardware Guide

**ARCHIVED:** This document has been consolidated into [[02-settings-sync-strategy.md]]. See that document for the current, authoritative version.

**Breadcrumb:** [[00-DASHBOARD]] > [[02-settings-sync-strategy]] > MCP Deployment ZimaBoard section

---

**Breadcrumb:** [[00-DASHBOARD]] > [[05-mcp-deployment-zimaboard]] > [[04-mcp-deployment-vps]]

> Run faerie2 MCP server on personal hardware (ZimaBoard with ZimaOS) for private, self-hosted deployment with full autonomy.

---

## Navigation Table

| Document | Direction | Purpose |
|----------|-----------|---------|
| [[04-mcp-deployment-vps]] | ← Previous | VPS deployment (cloud alternative) |
| [[03-mcp-server-architecture]] | ← Related | Server design + performance tuning |
| [[00-DASHBOARD]] | ← Related | System status hub |

---

## Why ZimaBoard + ZimaOS?

**ZimaBoard benefits:**
- **Small form factor:** 5"x5" board, fits in pocket, <10W power
- **Fanless design:** Silent, reliable, no moving parts
- **Full Linux:** Runs ZimaOS (Debian-based), full docker support
- **Storage:** PCIe NVMe slot (up to 4TB)
- **Networking:** Gigabit ethernet + optional WiFi module
- **Cost:** ~$200 hardware vs. $20-30/month for VPS (payback in 7 months)

---

## Prerequisites

### Hardware Setup

**ZimaBoard specs:**
- CPU: ARM-based or x86 (check model)
- RAM: 4GB minimum, 8GB recommended
- Storage: 128GB SSD minimum (NVMe M.2 slot)
- Power: USB-C 5V adapter (included)
- Networking: Gigabit ethernet (USB-C to RJ45 dongle if needed)

**Networking:**
- Wired ethernet preferred (low latency)
- Local network: 192.168.x.x (configure static IP)
- Port forwarding: 443 from router to ZimaBoard:443 (for HTTPS)
- Domain: Use DynDNS or static IP + custom domain

### ZimaOS Installation

**Download ZimaOS:**
1. Visit https://zimaos.com/download
2. Download ISO image for your ZimaBoard variant
3. Write to USB stick: `dd if=zimaos.iso of=/dev/sdX bs=4M`

**Boot & Install:**
1. Insert USB stick, power on ZimaBoard
2. Follow BIOS → Boot from USB
3. ZimaOS installer will guide through setup
4. Choose: Install to NVMe SSD

**Verify installation:**
```bash
# Log in via console or SSH
ssh root@zima.local

# Check OS
cat /etc/os-release
# ZimaOS version ...

# Check NVMe storage
lsblk
# nvme0n1 (M.2 SSD)
```

---

## Step 1: Initial ZimaOS Setup

### 1.1 Network Configuration

```bash
ssh root@zima.local << 'EOF'
# Assign static IP (replace with your network)
ip addr show  # Current IP
ip addr add 192.168.1.100/24 dev eth0
ip route add default via 192.168.1.1

# Make permanent: edit /etc/network/interfaces
cat > /etc/network/interfaces << 'NET'
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
NET

# Restart networking
systemctl restart networking

# Verify
ping 8.8.8.8  # Should work
EOF
```

### 1.2 Update System & Install Docker

```bash
ssh root@zima.local << 'EOF'
apt update && apt upgrade -y
apt install -y docker.io docker-compose curl git htop

# Add docker group
usermod -aG docker root

# Verify Docker
docker --version
docker run hello-world
EOF
```

### 1.3 Clone faerie2 Repository

```bash
ssh root@zima.local << 'EOF'
cd /opt
git clone https://github.com/goodoleusa/faerie-vault.git
ln -s /opt/faerie-vault /opt/faerie

# Verify
ls -la /opt/faerie
EOF
```

---

## Step 2: Create Docker Container

### 2.1 Write Dockerfile

```bash
ssh root@zima.local << 'EOF'
cat > /opt/faerie/Dockerfile << 'DOCKER'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    git curl htop \
    && rm -rf /var/lib/apt/lists/*

# Copy faerie code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi uvicorn aiofiles pydantic \
    uvloop httptools

# Create non-root user
RUN useradd -m -u 1000 faerie
RUN chown -R faerie:faerie /app

USER faerie

# Health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "faerie:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
DOCKER

# Build image
docker build -t faerie:latest /opt/faerie
docker images
EOF
```

### 2.2 Write docker-compose.yml

```bash
ssh root@zima.local << 'EOF'
cat > /opt/faerie/docker-compose.yml << 'COMPOSE'
version: '3.9'

services:
  faerie:
    image: faerie:latest
    container_name: faerie-mcp
    restart: always
    ports:
      - "127.0.0.1:8000:8000"
    volumes:
      - /opt/faerie/forensics:/app/forensics
      - /opt/faerie/.claude:/app/.claude
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=info
    health_check:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 5s
    # Resource limits for ZimaBoard (limited RAM/CPU)
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G

  nginx:
    image: nginx:alpine
    container_name: faerie-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /opt/faerie/nginx.conf:/etc/nginx/nginx.conf:ro
      - /opt/faerie/ssl:/etc/nginx/ssl:ro
      - /opt/faerie/certbot:/var/www/certbot:ro
    depends_on:
      - faerie

  certbot:
    image: certbot/certbot:latest
    container_name: faerie-certbot
    restart: always
    volumes:
      - /opt/faerie/certbot:/var/www/certbot
      - /opt/faerie/ssl:/etc/letsencrypt
    command: certonly --webroot --webroot-path=/var/www/certbot --agree-tos -d zima.example.com

volumes:
  forensics:
  ssl:
COMPOSE

# Verify syntax
docker-compose -f /opt/faerie/docker-compose.yml config
EOF
```

### 2.3 Configure nginx for Docker

```bash
ssh root@zima.local << 'EOF'
cat > /opt/faerie/nginx.conf << 'NGINX'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    gzip on;

    upstream faerie {
        server faerie:8000;
    }

    server {
        listen 80;
        server_name _;
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl http2;
        server_name zima.example.com;  # Replace with your domain

        ssl_certificate /etc/letsencrypt/live/zima.example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/zima.example.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        location / {
            proxy_pass http://faerie;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            access_log off;
            proxy_pass http://faerie/health;
        }
    }
}
NGINX
EOF
```

---

## Step 3: Start Docker Containers

### 3.1 Launch Containers

```bash
ssh root@zima.local << 'EOF'
cd /opt/faerie

# Start services
docker-compose up -d

# Verify running
docker-compose ps
# CONTAINER ID   IMAGE        STATUS
# xxx            faerie       Up X seconds (healthy)
# yyy            nginx        Up X seconds

# Check logs
docker-compose logs faerie
docker-compose logs nginx
EOF
```

### 3.2 Test Health Endpoint

```bash
ssh root@zima.local << 'EOF'
# Local test (before HTTPS setup)
curl -s http://127.0.0.1:8000/health | jq .
# {"status": "healthy", "timestamp": "...", "version": "1.0.0"}

# Through nginx
curl -s http://127.0.0.1/health | jq .
EOF
```

---

## Step 4: Configure HTTPS & Domain

### 4.1 DynDNS Setup (if using home internet)

**Option A: Use DynDNS provider (e.g., No-IP)**
```bash
ssh root@zima.local << 'EOF'
# Install noip client
apt install -y noip2

# Configure (answer prompts with your No-IP account)
noip2 -c /etc/noip2.conf

# Start service
systemctl start noip2
systemctl enable noip2
EOF
```

**Option B: Static IP + Custom Domain**
```
1. Get static public IP from ISP (or use cloud DNS provider)
2. Register domain (example.com)
3. Point A record to your public IP
4. Configure port forwarding on router:
   - Router WAN Port 443 → ZimaBoard LAN 192.168.1.100:443
   - Router WAN Port 80 → ZimaBoard LAN 192.168.1.100:80
```

### 4.2 Obtain SSL Certificate

```bash
ssh root@zima.local << 'EOF'
docker exec faerie-certbot certbot certonly --webroot \
    --webroot-path=/var/www/certbot \
    --email your@email.com \
    -d zima.example.com \
    --agree-tos \
    --non-interactive

# Verify certificate
docker exec faerie-certbot certbot certificates

# Reload nginx
docker exec faerie-nginx nginx -s reload
EOF
```

---

## Step 5: Auto-Restart & Monitoring

### 5.1 Enable Auto-Start on Power Loss

```bash
ssh root@zima.local << 'EOF'
# Enable docker autostart
systemctl enable docker

# Create systemd service for docker-compose
cat > /etc/systemd/system/faerie-docker.service << 'SYSTEMD'
[Unit]
Description=faerie Docker Compose Service
After=docker.service
Requires=docker.service

[Service]
Type=simple
WorkingDirectory=/opt/faerie
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose down
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SYSTEMD

systemctl daemon-reload
systemctl enable faerie-docker.service
systemctl start faerie-docker.service
EOF
```

### 5.2 Monitor Container Health

```bash
ssh root@zima.local << 'EOF'
# Check status
docker-compose ps

# Real-time logs
docker-compose logs -f faerie

# Resource usage (CPU, Memory)
docker stats faerie-mcp

# If container stops, restart automatically (already configured with restart: always)
EOF
```

---

## Step 6: Backups & Maintenance

### 6.1 Automated Backup to Cloud

```bash
ssh root@zima.local << 'EOF'
# Install rclone (cloud sync)
curl https://rclone.org/install.sh | bash

# Configure B2 backend
rclone config

# Backup forensics/ daily at 2 AM
cat > /opt/faerie/backup-cron.sh << 'BACKUP'
#!/bin/bash
# Daily backup of forensics/ to B2
rclone sync /opt/faerie/forensics b2:faerie-backup/forensics --delete-excluded
BACKUP

chmod +x /opt/faerie/backup-cron.sh

# Add to crontab
echo "0 2 * * * /opt/faerie/backup-cron.sh" | crontab -
EOF
```

### 6.2 Monthly Maintenance

```bash
ssh root@zima.local << 'EOF'
# Prune old forensics (>30 days)
find /opt/faerie/forensics -mtime +30 -delete

# Update docker images
docker-compose pull
docker-compose up -d
docker image prune -f

# Check disk usage
df -h /opt/faerie
du -sh /opt/faerie/*
EOF
```

---

## Troubleshooting

### Issue: "Container keeps restarting"

**Diagnosis:**
```bash
ssh root@zima.local 'docker-compose logs faerie | tail -50'
```

**Common causes:**
- Memory limit exceeded: Increase memory in docker-compose.yml
- Port already in use: Check `docker ps` and stop conflicting container
- Dependency not ready: Check if faerie code has syntax errors

### Issue: "HTTPS certificate fails to renew"

**Fix:**
```bash
ssh root@zima.local << 'EOF'
# Manual renewal
docker exec faerie-certbot certbot renew --force-renewal

# Reload nginx
docker exec faerie-nginx nginx -s reload

# Check certificate status
docker exec faerie-certbot certbot certificates
EOF
```

### Issue: "High latency from remote (>1 second)"

**Diagnosis:**
- Network bandwidth: Check router CPU/throughput
- ZimaBoard CPU limited: Monitor `docker stats`
- DNS lookup slow: Test with IP address directly

**Fix:**
1. Increase ZimaBoard worker count (docker-compose limits to 4)
2. Monitor network load (other devices using bandwidth?)
3. Use local DNS or Google DNS (8.8.8.8)

---

## Cost Analysis

| Aspect | VPS | ZimaBoard |
|--------|-----|-----------|
| **Hardware** | N/A | $200 (one-time) |
| **Monthly** | $20-30 | $0 (electricity only, ~$2/month) |
| **12-month cost** | $240-360 | $200 + $24 = $224 |
| **Payback** | N/A | 7-8 months |
| **Control** | Limited | Full |
| **Reliability** | Provider SLA | Your responsibility |

**Recommendation:** ZimaBoard for long-term (>12 months), VPS for short-term prototyping.

---

**Related:** [[04-mcp-deployment-vps]] (VPS alternative), [[03-mcp-server-architecture]] (server design)  
**Ref:** faerie design principle: "Artifacts-in-forensics"; backup to cloud is critical for long-term durability  
**Status:** Ready for personal deployment
