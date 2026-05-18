---
task_id: vault-enhancement-04-vps-deployment
investigation_label: vault-enhancement-2026-04-28
status: in_progress
created: 2026-04-28
---

# MCP Deployment on VPS — Production Guide

**Breadcrumb:** [[00-DASHBOARD]] > [[04-mcp-deployment-vps]] > [[03-mcp-server-architecture]]

> Deploy faerie2 MCP server on DigitalOcean, Linode, or equivalent VPS with nginx reverse proxy, systemd management, and full monitoring.

---

## Navigation Table

| Document | Direction | Purpose |
|----------|-----------|---------|
| [[03-mcp-server-architecture]] | ← Previous | Server design + performance tuning |
| [[05-mcp-deployment-zimaboard]] | → Next | Alternative: Personal hardware deployment |
| [[00-DASHBOARD]] | ← Related | System status hub |

---

## Prerequisites

### VPS Requirements

**Provider:** DigitalOcean Droplet, Linode, AWS Lightsail, or equivalent  
**OS:** Ubuntu 22.04 LTS (Jammy)  
**Instance Type:** 2vCPU, 4GB RAM, 100GB SSD (~$20-30/month)  
**Network:** Public IPv4 + IPv6, port 443 open

**Verify OS:**
```bash
uname -a
# Linux vps.example.com 5.15.0-84-generic #93-Ubuntu SMP x86_64 GNU/Linux

lsb_release -a
# Ubuntu 22.04.2 LTS
```

### SSH Access & Security

**SSH key setup (on local machine):**
```bash
ssh-keygen -t ed25519 -f ~/.ssh/faerie-vps -C "faerie@vps"
# Don't set passphrase (systemd needs auto-access)

ssh-copy-id -i ~/.ssh/faerie-vps.pub root@{VPS_IP}
```

**SSH config (~/.ssh/config):**
```
Host faerie-vps
    HostName {VPS_IP}
    User root
    IdentityFile ~/.ssh/faerie-vps
    StrictHostKeyChecking accept-new
```

**Test access:**
```bash
ssh faerie-vps "echo 'SSH OK'"
```

---

## Step 1: Initial VPS Setup

### 1.1 Update System

```bash
ssh faerie-vps << 'EOF'
apt update && apt upgrade -y
apt install -y python3.11 python3-pip python3-venv \
              nginx curl wget git htop net-tools

# Verify Python
python3 --version
# Python 3.11.x
EOF
```

### 1.2 Create Application User

```bash
ssh faerie-vps << 'EOF'
# Create faerie user (non-root, safer)
useradd -m -s /bin/bash -G sudo faerie
echo "faerie ALL=(ALL) NOPASSWD: /usr/sbin/systemctl" >> /etc/sudoers.d/faerie

# Copy SSH key to faerie user
mkdir -p /home/faerie/.ssh
cp /root/.ssh/authorized_keys /home/faerie/.ssh/
chown -R faerie:faerie /home/faerie/.ssh
chmod 700 /home/faerie/.ssh
chmod 600 /home/faerie/.ssh/authorized_keys

# Verify
su - faerie -c "echo 'User OK'"
EOF
```

### 1.3 Clone faerie2 Repository

```bash
ssh faerie-vps << 'EOF'
cd /opt
git clone https://github.com/goodoleusa/faerie-vault.git

# Create symlink for easy access
ln -s /opt/faerie-vault /opt/faerie

# Setup Python environment
cd /opt/faerie
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt 2>/dev/null || pip install fastapi uvicorn aiofiles pydantic

# Verify
python3 -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"
EOF
```

---

## Step 2: Configure nginx Reverse Proxy

### 2.1 Create nginx Configuration

```bash
ssh faerie-vps << 'EOF'
cat > /etc/nginx/sites-available/faerie << 'NGINX'
upstream faerie_backend {
    # FastAPI uvicorn running on localhost:8000
    server 127.0.0.1:8000;
    keepalive 64;
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=health_limit:10m rate=1000r/s;

server {
    listen 80;
    listen [::]:80;
    server_name _;

    # Redirect HTTP → HTTPS
    location / {
        return 301 https://$host$request_uri;
    }

    # Let's Encrypt ACME challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name {VPS_HOSTNAME};  # Replace with your domain

    # SSL certificates (see Step 3)
    ssl_certificate /etc/letsencrypt/live/{VPS_HOSTNAME}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{VPS_HOSTNAME}/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/{VPS_HOSTNAME}/chain.pem;

    # SSL tuning
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/faerie_access.log;
    error_log /var/log/nginx/faerie_error.log warn;

    # Gzip compression
    gzip on;
    gzip_types application/json text/plain text/css application/javascript;
    gzip_vary on;
    gzip_min_length 1024;

    # Root location
    location / {
        limit_req zone=api_limit burst=10 nodelay;
        proxy_pass http://faerie_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_request_buffering off;
        proxy_read_timeout 300s;
        proxy_connect_timeout 10s;
    }

    # Health check endpoint (higher rate limit)
    location /health {
        limit_req zone=health_limit burst=100 nodelay;
        proxy_pass http://faerie_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        access_log off;
    }

    # Metrics endpoint (restricted)
    location /metrics {
        allow 127.0.0.1;
        allow 10.0.0.0/8;
        deny all;
        proxy_pass http://faerie_backend;
    }
}
NGINX

# Enable site
ln -sf /etc/nginx/sites-available/faerie /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
EOF
```

### 2.2 Install SSL Certificate (Let's Encrypt)

```bash
ssh faerie-vps << 'EOF'
apt install -y certbot python3-certbot-nginx

# Obtain certificate (replace {VPS_HOSTNAME} with your domain)
certbot certonly --nginx -d {VPS_HOSTNAME} --agree-tos --register-unsafely-without-email

# Auto-renew (cron job)
echo "0 3 * * * certbot renew --quiet --deploy-hook 'systemctl reload nginx'" | crontab -

# Verify
ls -la /etc/letsencrypt/live/{VPS_HOSTNAME}/
EOF
```

---

## Step 3: Configure systemd Service

### 3.1 Create systemd Service File

```bash
ssh faerie-vps << 'EOF'
cat > /etc/systemd/system/faerie.service << 'SYSTEMD'
[Unit]
Description=faerie2 MCP Server
After=network.target
Wants=network-online.target

[Service]
Type=notify
User=faerie
WorkingDirectory=/opt/faerie
Environment="PATH=/opt/faerie/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/opt/faerie/venv/bin/uvicorn faerie:app \
    --host 127.0.0.1 \
    --port 8000 \
    --workers 4 \
    --loop uvloop \
    --log-level info

# Auto-restart on failure
Restart=always
RestartSec=5
StartLimitBurst=3
StartLimitIntervalSec=60

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

# Process isolation
PrivateTmp=yes
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/faerie/forensics /var/log/faerie

# Health check
HealthCheck=process
HealthCheckInterval=10s

[Install]
WantedBy=multi-user.target
SYSTEMD

# Enable service
systemctl daemon-reload
systemctl enable faerie.service
systemctl start faerie.service

# Verify
systemctl status faerie
EOF
```

### 3.2 Verify Service is Running

```bash
ssh faerie-vps << 'EOF'
# Check service status
systemctl status faerie --no-pager

# Check if listening on port 8000
ss -tlnp | grep 8000

# Check recent logs
journalctl -u faerie -n 20 --no-pager
EOF
```

---

## Step 4: Health Checks & Monitoring

### 4.1 Add Health Check Endpoint

**In faerie.py (MCP server code):**
```python
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/ready")
async def readiness_check():
    # Check if forensics/ is accessible
    try:
        import os
        os.access("forensics/manifests", os.R_OK)
        return {"ready": True}
    except Exception as e:
        return {"ready": False, "error": str(e)}
```

### 4.2 Local Health Check

```bash
ssh faerie-vps << 'EOF'
# Test health endpoint
curl -s http://127.0.0.1:8000/health | jq .
# {"status": "healthy", "timestamp": "2026-04-28T10:15:02.123456", "version": "1.0.0"}

# Test through nginx (HTTPS)
curl -s https://faerie.example.com/health | jq .
EOF
```

### 4.3 Monitor Logs

```bash
ssh faerie-vps << 'EOF'
# Follow service logs
journalctl -u faerie -f

# Check nginx logs
tail -f /var/log/nginx/faerie_access.log
tail -f /var/log/nginx/faerie_error.log
EOF
```

---

## Step 5: Performance Tuning

### 5.1 System Limits

```bash
ssh faerie-vps << 'EOF'
# Increase file descriptors
cat >> /etc/security/limits.conf << 'LIMITS'
faerie soft nofile 65536
faerie hard nofile 65536
faerie soft nproc 4096
faerie hard nproc 4096
LIMITS

# Apply (may need relogin)
sysctl -p
EOF
```

### 5.2 TCP Tuning

```bash
ssh faerie-vps << 'EOF'
cat >> /etc/sysctl.conf << 'SYSCTL'
# TCP performance
net.core.somaxconn = 65536
net.ipv4.tcp_max_syn_backlog = 65536
net.ipv4.ip_local_port_range = 1024 65535
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30

# Buffer tuning
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
SYSCTL

sysctl -p
EOF
```

---

## Troubleshooting

### Issue: "Connection refused" on port 8000

**Diagnosis:**
```bash
ssh faerie-vps 'ss -tlnp | grep 8000'
# If no output, service not listening
```

**Fix:**
```bash
ssh faerie-vps << 'EOF'
# Check service status
systemctl status faerie

# View error logs
journalctl -u faerie -n 50

# Restart service
systemctl restart faerie
systemctl status faerie
EOF
```

### Issue: "504 Bad Gateway" from nginx

**Diagnosis:**
```bash
ssh faerie-vps 'tail -20 /var/log/nginx/faerie_error.log'
# "upstream timed out"
```

**Fix:**
1. Check if backend is slow: `curl http://127.0.0.1:8000/health`
2. Increase proxy_read_timeout in nginx (see Step 2.1)
3. Increase uvicorn workers: `--workers 8`
4. Restart nginx: `systemctl restart nginx`

### Issue: "SSL certificate error"

**Diagnosis:**
```bash
ssh faerie-vps 'certbot certificates'
```

**Fix:**
```bash
ssh faerie-vps << 'EOF'
# Renew certificate early
certbot renew --force-renewal

# Reload nginx
systemctl reload nginx

# Test
curl -I https://faerie.example.com
# HTTP/2 200
EOF
```

---

## Maintenance

### Weekly Checklist

```bash
# Check service status
systemctl status faerie

# Check disk usage
df -h /opt/faerie

# Check certificate expiry
certbot certificates

# Monitor logs for errors
journalctl -u faerie --since "1 week ago" | grep ERROR | tail -10
```

### Monthly Tasks

```bash
# Update packages
apt update && apt upgrade -y

# Prune old forensics (>30 days)
find /opt/faerie/forensics -mtime +30 -delete

# Backup forensics to B2
aws s3 sync /opt/faerie/forensics s3://faerie-backup/forensics/
```

---

**Related:** [[03-mcp-server-architecture]] (server design), [[05-mcp-deployment-zimaboard]] (alternative deployment)  
**Ref:** faerie design principle: "Artifacts-in-forensics"; backup strategy is critical  
**Status:** Ready for production deployment
