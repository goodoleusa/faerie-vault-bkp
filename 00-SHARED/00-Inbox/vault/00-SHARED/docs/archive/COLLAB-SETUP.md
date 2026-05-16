# Faerie Collaboration — Cloud Setup

**Goal:** Host a secure, remote-accessible AI coding session for you and your friend.

---

## Quick Start: Use Existing OpenHands

Your ZimaBoard already runs OpenHands:

| Service | URL | Auth |
|---------|-----|------|
| OpenHands | http://192.168.0.11:13333 | None (local only) |
| Faerie MCP | http://192.168.0.11:38080/mcp | Token |

---

## Secure Remote Access (with auth)

### nginx-proxy-manager (recommended)

1. **Login**: `http://192.168.0.11:81`

2. **Create Access List** (do this first):
   - Go to **Access Lists** → **New Access List**
   - Name: `Friends`
   - Type: `Basic Auth`
   - Add usernames/passwords for you + friend
   - Click **Save**

3. **Create Proxy Host #1 — OpenHands**:
   - Domain names: `faeriemcp.duckdns.org`
   - Forward: `192.168.0.11:13333`
   - Access List: `Friends`
   - Click **Save**

4. **Create Proxy Host #2 — Faerie MCP**:
   - Domain names: `api.faeriemcp.duckdns.org`
   - Forward: `192.168.0.11:38080`
   - Access List: `Friends`
   - Click **Save**

5. **Open Firewall** in ZimaOS → Network → Firewall:

| Port | Protocol | Source |
|------|----------|--------|
| 80 | TCP | Anywhere |
| 443 | TCP | Anywhere |

---

### Final URLs

| Service | Remote URL |
|---------|------------|
| OpenHands (collab) | `http://faeriemcp.duckdns.org` |
| Faerie MCP | `http://api.faeriemcp.duckdns.org/mcp` |

### MCP Configuration

```json
{
  "mcpServers": {
    "faerie": {
      "url": "http://api.faeriemcp.duckdns.org/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

Friend logs in once via browser → gets OpenHands. Your local Claude uses MCP URL with token.

---

## Sharing with Friend

Give them:
- Your public URL (from DuckDNS or Cloudflare Access)
- Their username/password

They open the URL, login, and you both get:
- Full OpenHands terminal
- AI coding assistant (Claude)
- Your faerie MCP tools

---

## Port Checklist

In ZimaOS → Network → Firewall:

| Port | Service |
|------|---------|
| 13333 | OpenHands |
| 38080 | Faerie MCP |
| 38081 | Token API |

---

*Updated: 2026-04-12*