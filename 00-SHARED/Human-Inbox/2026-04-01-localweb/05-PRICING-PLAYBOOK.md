---
title: Pricing Playbook — LocalWeb Studio for Pharmacy Networks
type: playbook
project: localweb
parent: [[00-SHARED/Human-Inbox/2026-04-01-localweb/README]]
tags: #product-localweb #narrative #sales-ready
status: final
doc_hash: sha256:db63abcc404c195e162eec0b41719e5f825f35e0c14a72184b99c3d3bae9de26
created: 2026-04-01
hash_ts: 2026-04-01T16:07:45Z
hash_method: body-sha256-v1
---

# Pricing Playbook

This document covers everything financial: pricing tiers, what's included, ROI talking points, and contract terms. Use it internally when modeling deals, or share the relevant sections with a prospect.

---

## Pricing Tiers

### Single Location

| Item | Cost |
|---|---|
| Setup fee | $1,500 |
| Monthly retainer | $129–$199/mo |

Setup fee range depends on: photography needs (none vs. extensive stock sourcing), number of custom status strings, API complexity.

Retainer range: $129/mo for basic queue + status lookup only; $199/mo adds delivery booking and admin heatmap.

### 2–5 Locations (Franchise Bundle)

| Item | Cost |
|---|---|
| Setup fee | $2,500–$4,000 |
| Monthly retainer | $179–$249/mo |

Locations share a single Cloudflare account and a unified admin dashboard. Each location has its own URL path and queue display. Setup fee scales with location count and API integration complexity.

At this tier, a shared Cloudflare KV namespace stores cross-location heatmap data — enabling the network-level demand analytics that make RxReady compelling for franchise operators.

### 6+ Locations (Enterprise Franchise)

| Item | Cost |
|---|---|
| Setup fee | $5,000+ (scoped per engagement) |
| Monthly retainer | Custom — typically $299–$499/mo |

Enterprise engagements include: dedicated Cloudflare account setup, custom SLA (99.9% uptime guarantee in writing), expanded support hours, optional staff training sessions per location, and quarterly business review calls.

---

## What Every Tier Includes

- Static site hosting on Cloudflare Pages (global CDN)
- RxReady queue display + prescription status lookup
- Delivery booking form with staff email notification
- Admin heatmap dashboard
- Up to 1 hour/month of content updates
- Quarterly Cloudflare security audit
- Bug fix coverage (if something breaks, we fix it)
- Full source file access (your code, always)

---

## What Costs Extra

| Item | Rate |
|---|---|
| Additional support hours (over 1 hr/mo) | $95/hr (change order required) |
| Custom integrations beyond standard API endpoint | Scoped per project; minimum $500 |
| Photography coordination or sourcing | $150–$300 per engagement |
| Custom feature development (e.g., appointment booking, loyalty module) | Scoped; minimum $800 |
| Additional staff training sessions (beyond 30-min video) | $150/session |
| Emergency support (outside business hours) | $150/hr — enterprise tier only |

---

## ROI Model

### The Call Reduction Math

A pharmacy handling 400 daily prescriptions might receive 50–80 inbound status calls per day. At 2.5 minutes per call, that's 125–200 minutes of staff time daily — roughly 2–3.5 FTE-equivalent hours.

At even a 15% reduction (conservative, based on Mesa Verde results): **18–30 minutes of staff time recovered per day, per location.**

For a 3-location network, that's 54–90 minutes per day network-wide. At a pharmacy technician wage of $18–22/hr, that's $29–$49.50 recovered per day, or **$10,500–$18,000 per year in recovered labor capacity.**

Monthly retainer at the 3-location tier: $179–$249. Annual cost: ~$2,900.

**Payback period: under 90 days at conservative estimates.**

### The Competitive Differentiation Value

This one is harder to quantify but real:

- "We have a live queue website" is a meaningful differentiator vs. independent pharmacies
- Patients share the queue URL — organic word of mouth with no marketing spend
- Corporate accounts and assisted living facilities value the status lookup for their coordinators
- Insurance case managers increasingly refer patients to pharmacies with digital self-service

### The Data Value

The admin heatmap gives you demand data you have never had before:

- Which hours have the longest waits? (Staff accordingly)
- Which locations are consistently understaffed on Monday mornings?
- How did a flu shot promotion affect walk-in volume?
- Is the new location's growth on track?

This intelligence has operational value beyond the website itself.

---

## Contract Terms

### Standard Terms

- **Contract length:** 12 months or 24 months (24-month gets 10% discount on setup fee)
- **Billing:** Monthly retainer due by the 5th of each month; setup fee due 50% at contract signing, 50% at launch
- **Payment methods:** ACH bank transfer, check, or credit card (card adds 2.9% processing fee)

### Termination

- **Early termination:** 90 days written notice, or payment of one month's retainer as early termination fee (whichever is less)
- **Hosting handoff:** Available at any time, at no extra charge. We transfer the Cloudflare account and provide all source files within 5 business days of request.
- **After termination:** Site remains live until the Cloudflare account transfer is complete. We don't pull the plug on a live pharmacy website.

### Scope Changes

- Any change that requires more than 1 hour of work triggers a written change order
- You approve the estimate before we start — no surprise invoices
- Change orders are billed at $95/hr with a 2-hour minimum

---

## Negotiation Notes (Internal — Don't Share)

These are talking points for negotiating with a prospect:

- **"Can we do a pilot with one location first?"** — Yes. Single location at standard pricing. If they expand to 3+ within 6 months, apply a retroactive bundle discount to the setup fee (credit toward next invoice).
- **"Can you lower the monthly fee?"** — Rarely worth discounting retainer. Better lever: extend setup fee payment terms (3 months instead of 50/50). Recurring revenue matters more than upfront.
- **"We want a Service Level Agreement."** — Available at Enterprise tier. Standard tier has best-effort SLA (99% historical Cloudflare uptime); put that in writing if they need documentation for procurement.
- **"Who else have you done this for?"** — Reference the Mesa Verde example. If pressed for a live reference, note that reference calls are available for enterprise contracts.

---

*Related: [[00-SHARED/Human-Inbox/2026-04-01-localweb/06-COMPLIANCE-BOUNDARIES]] — what's covered vs. what's the pharmacy's responsibility*
