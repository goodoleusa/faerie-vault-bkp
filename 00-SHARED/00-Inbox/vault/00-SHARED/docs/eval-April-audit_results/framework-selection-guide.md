---
type: research-brief
blueprint: "[[Blueprints/Research-Brief.blueprint]]"
agent_type: research-analyst
session_id: hustle-research-2026-04-01
doc_hash: sha256:pending
status: draft
created: 2026-04-01
topic: SMB Web Framework Selection + Automation Guide
verticals: [contractor, restaurant, pharmacy, lawyer]
---

# SMB Web Framework Selection Guide (2026)

> Decision tree for agency framework selection across four SMB verticals, plus automation, deployment, e-paper, and pharmacy backend guidance.

---

## Decision Tree — "My Client Is..."

### A Contractor (plumber, electrician, roofer, landscaper)
**Use: Astro + Cloudflare Pages**

- Goal: rank in local Google search, look professional, generate calls
- Astro ships zero JS by default — Lighthouse SEO 100 is achievable out of the box
- Clean static HTML = fast crawlability for Google Maps Pack inclusion
- Cloudflare Pages: unlimited bandwidth free, global CDN, pairs naturally with Astro post-acquisition (Jan 2026)
- CMS: Keystatic or Decap CMS (Git-based) so client can update services/prices
- Schema markup: LocalBusiness JSON-LD in Astro layout component
- Cost to client: $0/month hosting (Cloudflare Pages free)

**Stack:** Astro 5+ / Tailwind CSS / Cloudflare Pages / Keystatic CMS

---

### A Restaurant (sit-down, fast casual, food truck)
**Use: Next.js 15 + Stripe + Vercel (or Railway)**

- Goal: online ordering, menu browsing, reservations, gift cards
- Next.js Server Actions + Stripe Embedded Checkout (2026 best practice) — PCI compliance delegated to Stripe, card data never touches your server
- App Router with ISR (Incremental Static Regeneration) keeps menu pages fast while allowing dynamic specials
- Medusa or NextMerce for full headless e-commerce if needed
- OpenTable/Resy API or Tock for reservation integration
- Vercel is the native host for Next.js — but if budget is tight, Railway ($5/month) handles Next.js + Postgres together
- CMS: Sanity (free tier, excellent image handling for menu photos)

**Stack:** Next.js 15 / Stripe Embedded Checkout / Tailwind CSS / Sanity CMS / Vercel or Railway

**Cost to client:** $0 (Vercel free, personal-only) or $20/month (Vercel Pro) or $5-20/month (Railway)

---

### A Pharmacy (independent, compounding, specialty)
**Use: Astro (public) + SvelteKit (authenticated portal) + Turso or SQLite+Litestream**

Split architecture:
- **Public-facing site** (Astro): hours, services, staff, contact — zero patient data, Lighthouse 100, Cloudflare Pages free
- **Patient portal** (SvelteKit): prescription refill requests, medication status, secure messaging

**Why SvelteKit for the portal:**
- 1.6 KB runtime (vs React 42 KB) — fast on mobile for elderly patients
- Svelte 5 Runes = fine-grained reactivity without complexity
- WebSocket/SSE integration is idiomatic for real-time status updates

**Database choices (pick one):**

| Option | Cost | Notes |
|--------|------|-------|
| Turso (LibSQL) | Free tier (500 DBs) | Local-first, privacy-focused, no BAA |
| SQLite + Litestream | ~$0.02/month S3 | Self-hosted, maximum control, SQLCipher encryption |
| Neon (Serverless Postgres) | Free tier | BAA available on paid plans; relational integrity |

**Prescription refill workflow:**
1. Patient authenticates (Lucia auth — session cookie only, no PHI in token)
2. Patient selects medication from server-side-rendered profile
3. Refill request written to DB: `status=PENDING`, timestamped
4. Pharmacist dashboard shows PENDING queue (SSR — no PHI in client JS)
5. Pharmacist approves → SMS via Twilio → patient notified
6. Role separation enforced at DB level (user_id FK), not just UI

**Critical HIPAA-ish rules:**
- Every PHI access logged: user_id, action, timestamp, IP
- No patient data in JWT claims or localStorage
- Full encryption at rest (SQLCipher or Neon AES-256) + TLS in transit

**Stack:** Astro (public) + SvelteKit (portal) / Lucia Auth / Turso or SQLite+Litestream / Railway or Render (portal) / Cloudflare Pages (public)

---

### A Lawyer / Law Firm (solo, boutique, plaintiff's firm)
**Use: SvelteKit + Railway + Postgres**

- Goal: client portal with case status updates, document sharing, secure messaging, billing
- SvelteKit handles reactive case status boards cleanly — SSE for real-time case updates
- Role separation is critical: clients see only their matters (enforced at DB level)
- Document upload: Cloudflare R2 (S3-compatible, $0.015/GB) — presigned URLs, never expose storage directly
- E-signatures: DocuSeal (open source, self-hostable) or Docusign API
- Billing: Stripe Customer Portal for retainer payments and invoice management
- Brochure site (separate): Astro for SEO — "personal injury lawyer [city]" keywords

**Key features to build:**
- Case status timeline (SSE push from server when status changes)
- Secure document exchange (upload/download with audit log)
- Appointment scheduling (Cal.com open source, self-hostable)
- Client messaging (server-stored, not email — maintains privilege chain)

**Stack:** SvelteKit / Postgres (Railway) / Cloudflare R2 / DocuSeal / Cal.com / Stripe

---

## Framework Quick-Reference Table

| Framework | Best Vertical | SEO | Bundle | Real-Time | Dev Speed |
|-----------|---------------|-----|--------|-----------|-----------|
| Astro 5+ | Contractor, brochure | 10/10 | ~0 KB JS | No | High |
| Next.js 15 | Restaurant, e-commerce | 9/10 | ~85 KB | Moderate | High |
| SvelteKit | Pharmacy portal, lawyer portal | 8/10 | ~10 KB | Yes | Med-High |
| React/Vite | Internal tools, admin | 5/10 | ~120 KB | Yes | High |
| Angular | Enterprise law firm | 7/10 | ~200 KB | Yes | Low-Med |
| Nuxt 4 | Vue-team restaurants | 9/10 | ~70 KB | Moderate | High (Vue) |

---

## Automation Patterns for Template Systems

### Agency Onboarding Workflow (Recommended)

```
Intake Form (Tally.so)
  -> Webhook triggers create-client.js
  -> Clone vertical template repo (contractor/restaurant/pharmacy/lawyer)
  -> Token replacement: {{BUSINESS_NAME}}, {{PRIMARY_COLOR}}, {{PHONE}}
  -> gh CLI creates GitHub repo + Netlify/Cloudflare project
  -> Preview URL generated (<15 minutes from form submission)
  -> DNS instructions emailed to client
  -> CMS credentials sent (Keystatic or Sanity)
```

### Tool Selection by Scale

| Situation | Tool | Reason |
|-----------|------|--------|
| Single-project component generation | Plop | Stays in project, CI-friendly |
| Greenfield client site from scratch | Custom Node script | Full control, no deps |
| 5+ active client sites | Turborepo monorepo | Shared component lib, incremental builds |
| Angular-heavy portfolio | Nx | Stronger code generation for Angular |
| Non-technical clients needing CMS | WordPress + WP-CLI | Familiar to clients; automate via CLI |

### CMS Recommendations by Client Type

| Client Type | CMS | Why |
|-------------|-----|-----|
| Contractor (non-technical) | Keystatic | Git-based, no database, Astro-native |
| Restaurant (menu updates) | Sanity | Excellent image handling, free tier |
| Pharmacy (staff only) | Custom admin UI | HIPAA-ish: control access strictly |
| Lawyer (document-heavy) | Custom portal | No third-party CMS touching PHI |

---

## Deployment Platform Decision

### Cost-First Decision Tree

```
Is site purely static? (no API routes, no DB)
  YES -> Cloudflare Pages (unlimited bandwidth free, Astro-native)

Is site Next.js with API routes?
  YES + budget exists -> Vercel Pro ($20/user/month)
  YES + budget tight -> Railway ($5-20/month, runs DB alongside)

Is site SvelteKit portal (pharmacy/lawyer)?
  -> Railway (DB + app together, predictable pricing)

Need Docker/custom runtime?
  -> Render (health checks built-in, $7/month+)
```

### Platform Comparison

| Platform | Free Commercial | Bandwidth | Best For | Monitoring |
|----------|-----------------|-----------|----------|------------|
| Cloudflare Pages | Yes | Unlimited | Static + Astro | Built-in analytics |
| Netlify | Yes | 100 GB | JAMstack, SvelteKit | External (BetterUptime) |
| Vercel | No (personal only) | 100 GB | Next.js | External required |
| Railway | No | Usage-based | Full-stack + DB | Basic metrics |
| Render | Yes (static) | 100 GB | Backend services | Health checks built-in |

### Monitoring Setup (Required for Every Client)

UptimeRobot free tier: 50 monitors, 5-minute checks — sufficient for any SMB portfolio.
For SLA-sensitive clients (pharmacy, lawyer): BetterUptime free (3 monitors, status page).

---

## E-Paper + Responsive Design (Dual-Output Pipeline)

### When This Matters

Pharmacies with waiting room info tiles, contractor quote boards, restaurant menu boards — any deployment where a physical e-ink display shows the site's content.

### Build Pipeline

```
Design (full color CSS/Tailwind)
  -> Astro build with EPAPER=true flag
  -> Sharp image processor: contrast +20%, sharpen, Floyd-Steinberg dithering
  -> Output: /assets/web/ (standard) + /assets/epaper/ (1-bit or 4-bit)
  -> CSS Grid with fixed tile dimensions matching display resolution
```

### E-Paper Design Rules

| Rule | Why |
|------|-----|
| Black text on white only | No e-ink display renders mid-gray reliably |
| Minimum 18px/14pt text | Dithering blurs small text |
| No CSS transitions/animation | Refresh ghosting — even 75Hz Modos shows artifacts |
| Pre-dither images at build time | Never rely on browser for dithering |
| No gradients — flat fills only | Gradients become noise after 1-bit conversion |
| Fixed-pixel grid | Match display resolution (common: 800x600, 1024x758) |

### Dithering Method Selection

| Content Type | Method | Why |
|---|---|---|
| Photos | Floyd-Steinberg error diffusion | Best perceptual quality |
| Icons / UI | Bayer matrix (ordered) | Clean structured patterns |
| Text | No dithering | Preserve sharp edges |
| Color e-ink (Spectra 6) | Per-channel error diffusion | 6-color quantization |

### Sharp Implementation (build-time)

```js
import sharp from 'sharp';

async function ditherForEpaper(inputPath, outputPath) {
  await sharp(inputPath)
    .modulate({ brightness: 1.2 })
    .sharpen()
    .toColourspace('b-w')
    .toFile(outputPath, { dither: 1.0 }); // Floyd-Steinberg
}
```

---

## Key Findings Summary

1. **Astro + Cloudflare Pages** is the canonical pairing for static SMB sites post-Cloudflare acquisition (Jan 2026). Zero-JS default, Lighthouse 100 achievable, unlimited bandwidth free.

2. **Next.js 15 + Stripe Embedded Checkout** is the standard for restaurant/e-commerce in 2026 — Server Actions + React 19 make payment flows significantly simpler than prior approaches.

3. **SvelteKit** wins for authenticated portals (pharmacy, lawyer) — 1.6 KB runtime, idiomatic WebSocket/SSE, clean auth patterns. Not for public brochure pages.

4. **Split architecture** is the right pattern for pharmacy and law: Astro public site (SEO, zero patient data) + SvelteKit authenticated portal (PHI stays server-side).

5. **Turso or SQLite+Litestream** for independent pharmacy — local-first, privacy-first, near-zero cost. Use Neon (Serverless Postgres) when relational integrity or BAA is required.

6. **Agency automation**: Custom Node script + Plop + Turborepo (at scale). Tally.so intake -> webhook -> clone template -> token replace -> Cloudflare/Netlify deploy. Preview URL in <15 minutes.

7. **Monitoring**: UptimeRobot free (50 monitors) for standard SMB. BetterUptime free (status page) for pharmacy/lawyer who need client-visible SLA.

---

*Research conducted: 2026-04-01 | Agent: research-analyst | Sources: 14 web sources across all five goal domains*
