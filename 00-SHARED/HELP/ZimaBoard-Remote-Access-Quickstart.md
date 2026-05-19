# ZimaBoard Remote Access — Collaborator Quickstart

**Goal:** Get SSH + ztnet access to the investigation ZimaBoard from anywhere.

---

## Step 1 — Install ZeroTier

Download and install ZeroTier from **zerotier.com/download**

- Windows: install the desktop app (tray icon)
- Mac: same, install the app
- Linux: `curl -s https://install.zerotier.com | sudo bash`

---

## Step 2 — Join the Network

**Network ID:** `f3797ba7a81e998e` (swarmy)

**Windows/Mac:**
1. Click ZeroTier tray icon (bottom-right corner)
2. Click **"Join New Network"**
3. Paste: `f3797ba7a81e998e`
4. Click Join

**Linux/WSL:**
```bash
sudo zerotier-cli join f3797ba7a81e998e
```

---

## Step 3 — Wait for Authorization

Your device will show as **pending** until the admin approves it.

Tell the admin your request is in. Once approved, you'll get a `10.10.233.x` IP.

**Verify you're connected (Windows PowerShell):**
```powershell
ping 10.10.233.8
```
Should get replies. If no reply, you're not authorized yet.

---

## Step 4 — SSH to ZimaBoard

```bash
ssh casaos@10.10.233.8
```

Password: (ask admin)

If you're on WSL, this works directly — WSL inherits the Windows ZeroTier connection.

---

## Step 5 — Access Services

Once on the ZeroTier network, access via browser or SSH:

| Service | URL |
|---------|-----|
| ztnet (ZeroTier manager) | http://10.10.233.8:3050 |
| ZimaOS dashboard | http://10.10.233.8 |
| SSH | ssh casaos@10.10.233.8 |

---

## Troubleshooting

**Ping fails / can't connect:**
- Check ZeroTier tray — are you showing as connected?
- Ask admin to verify you're authorized in the Members list
- Try `sudo zerotier-cli listnetworks` (Linux) — should show status OK

**SSH refused:**
- ZimaBoard might need your SSH key added
- Try `ssh -o StrictHostKeyChecking=no casaos@10.10.233.8`

**Got kicked off the network:**
- Authorization can expire or be revoked — ask admin to re-authorize

---

## Admin: Authorizing New Members

1. Go to **my.zerotier.com**
2. Open network `f3797ba7a81e998e`
3. Scroll to **Members**
4. Check the box next to the new device to authorize it
5. Optionally assign a name so you know who's who

---
**Network:** `f3797ba7a81e998e` (swarmy)  
**ZimaBoard ZeroTier IP:** `10.10.233.8`  
**Last Updated:** 2026-04-08  
**Status:** ✅ Verified — ping 10.10.233.8 confirmed reachable (27-141ms) from Windows over ZeroTier
