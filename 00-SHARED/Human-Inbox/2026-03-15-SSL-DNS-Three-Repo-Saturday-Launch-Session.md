---
type: meta
tags:
  - inbox
  - ssl
  - dns
doc_hash: sha256:7936596d47be9f60b404edd0d46a2b4a9f6ccd523f230862744a40e520da3e08
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

  ---
  Re: SSL and DNS — No, you do NOT need to keep Namecheap DNS to use their SSL certificate. Here's the deal:

  If you bought a Namecheap SSL certificate (PositiveSSL, etc.):
  - The SSL cert is tied to the domain, not the DNS provider
  - You complete domain validation (DCV) once — via email, DNS TXT record, or HTTP file
  - After issuance, the cert works regardless of who handles DNS
  - But: you'd need to install it on your VPS manually, and renew it periodically

  Better approach — skip the paid SSL entirely:
  - Cloudflare (free plan): auto-SSL for .report — no cert needed
  - Caddy on Hetzner VPS: auto-HTTPS via Let's Encrypt for .net — free, auto-renewing
  - GitHub Pages: auto-SSL for .info — free
  - deSEC.io: handles DNS only (no SSL), pairs perfectly with Caddy's auto-HTTPS

  So the setup is:
  1. Move DNS for .net to deSEC.io (free, privacy-focused, supports DNSSEC)
  2. Point .report NS to Cloudflare (they handle DNS + SSL + CDN)
  3. Keep .info DNS at Namecheap or move to GitHub (for GitHub Pages)
  4. Caddy on VPS auto-obtains Let's Encrypt certs for .net — zero config, auto-renews
  5. Cancel/don't renew the Namecheap paid SSL — you don't need it

  Caddy + Let's Encrypt gives you free auto-renewing SSL. Cloudflare gives you free SSL. The paid Namecheap cert adds nothing.

  ---
  Full Session Deliverables

  Everything built this session:

  ┌───────────────────────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────┐
  │                                   File                                    │                        Purpose                         │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ B2 Dual-Bucket                                                            │                                                        │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ scripts/b2_bucket_copy.py                                                 │ Backup → working bucket copy + manifests               │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ scripts/b2_verify_sync.py                                                 │ Daily verification of backup vs working                │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ forensic/b2_backup_manifest.json                                          │ Backup ground truth template                           │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ forensic/b2_working_manifest.json                                         │ Working bucket provenance template                     │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ forensic/b2_verify/                                                       │ Verification report directory                          │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ Three-Repo Export                                                         │                                                        │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ scripts/export_to_public.sh                                               │ Export site files to public repo                       │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ scripts/export_to_template.sh                                             │ Export pipeline to template repo                       │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ .github/workflows/export-to-public.yml                                    │ CI auto-export on push                                 │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ scripts/setup_template.sh                                                 │ One-command pipeline onboarding                        │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ config.example.json                                                       │ Template project config                                │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ .env.example                                                              │ Environment variable template                          │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ Launch Platform                                                           │                                                        │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ scripts/publish_p2p.sh                                                    │ IPFS, Arweave, BitTorrent, IA, Nostr publishing        │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ scripts/securedrop_submit.py                                              │ SecureDrop submission via Tor                          │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ scripts/press_outreach.py                                                 │ AI-personalized press emails (Haiku)                   │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ scripts/monitor_coverage.py                                               │ Web monitoring for news mentions                       │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ Dashboards                                                                │                                                        │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ press.html                                                                │ Media CRM (kanban + contacts + timeline)               │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ coverage.html                                                             │ Public press coverage page                             │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ assets/mirrors-footer.js                                                  │ Reusable censorship-resilience footer with status dots │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ Docs + Config                                                             │                                                        │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ docs/LAUNCH-CHECKLIST.md                                                  │ Full T-7 to T+7 launch playbook                        │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ ARCHITECTURE.md                                                           │ Updated with three-repo + B2 architecture              │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ project_config.json                                                       │ Updated with criticalexposure.report domain            │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ https://excalidraw.com/#json=Z56-_IuaSFfg52RJy8rKl,S6vepm7kNYkuEN33tK0okA │ Architecture visualization                             │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ Data files                                                                │                                                        │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ data/press_contacts.json                                                  │ Sample press contact list                              │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ data/press_coverage.json                                                  │ Empty coverage (ready for articles)                    │
  ├───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
  │ exports/outreach_log.json                                                 │ Empty outreach log                                     │
  └───────────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────┘

  [ctx ~115K/200K | cache HIT ✓ | turn 10 | ~$0.70 | saved ~$0.28 vs cold | session ~$6.20]

✻ Cooked for 1m 2s

❯ i need to test the generic (the third generic template repo) today and start DNS propagation of the site but i dont want the specific content to be published yet

● Two parallel tracks:

  Track 1: DNS Propagation (start now, takes 24-48h)

  Set up DNS pointing to a placeholder — no investigation content exposed.

  For .report (Cloudflare):
  1. Cloudflare dashboard → Add Site → criticalexposure.report
  2. Cloudflare gives you 2 nameservers (e.g., ann.ns.cloudflare.com)
  3. Namecheap → Domain List → criticalexposure.report → Custom DNS → paste Cloudflare NS
  4. In Cloudflare: add A record → @ → any IP (or enable Pages later)

  For .net (deSEC.io):
  1. Register at desec.io → create domain criticalexposure.net
  2. Copy deSEC nameservers (e.g., ns1.desec.io, ns2.desec.org)
  3. Namecheap → Custom DNS for .net → paste deSEC NS
  4. Add A record later when VPS is provisioned

  For .info (GitHub Pages):
  1. Keep Namecheap DNS for now
  2. Add CNAME record: @ → yourusername.github.io
  3. Or just start propagation by pointing NS now

  Start all three NS changes today — they propagate in parallel.