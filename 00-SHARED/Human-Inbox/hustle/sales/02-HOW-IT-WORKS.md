---
title: How LocalWeb Works — Operations Overview
type: guide
project: localweb
parent: [[00-SHARED/Human-Inbox/hustle/README]]
tags: #product-localweb #narrative #implementation
status: final
doc_hash: sha256:aac564af4786341dd9d88cc3a0b3e72efe9016a0b178d62e0d53b6294fa6e1fc
created: 2026-04-01
hash_ts: 2026-04-01T16:05:53Z
hash_method: body-sha256-v1
---

# How LocalWeb Works

This document explains how LocalWeb Studio operates day-to-day — written for non-technical readers. No jargon. If you want to understand what you're actually buying, start here.

---

## The Delivery Model

LocalWeb Studio works from **pre-built, customizable templates**. This is the same model used by the best solo agencies — not because it's easier, but because it lets us deliver faster without sacrificing quality.

Here's what that means in practice:

- The core site structure (navigation, color system, mobile layout, forms) is pre-tested and production-ready before your project starts
- Your customization layer (brand colors, logo, copy, photos, location data, queue integration) goes on top
- Total operator time to configure and deploy a new location: under 8 hours

Traditional agencies rebuild from scratch for every client. LocalWeb amortizes that foundation cost across all clients — and passes the savings to you in faster delivery and lower setup fees.

---

## The Technology Stack (Plain English)

You don't need to understand this deeply, but you should know what you're running on:

| Component | What It Is | Why We Use It |
|---|---|---|
| **Astro** | The site builder | Generates pure HTML/CSS/JS — no database, no server required |
| **Cloudflare Pages** | Where the site lives | Global CDN, 99.99% uptime, free tier covers most sites |
| **Cloudflare Workers** | The queue logic | Serverless code that talks to your pharmacy API; runs at the edge |
| **Formspree** | Form submissions | Handles contact forms and delivery booking without a backend |
| **Leaflet** | Maps | Open-source map library — no Google API key, no per-request charges |

**The key principle: no database on the site itself.** All patient-facing data is read from your pharmacy system in real time and displayed momentarily. Nothing is stored. The site is just HTML and a thin API connection.

---

## What "Week 1 Onboarding" Looks Like

When you sign a contract, you receive a structured intake checklist (see [[templates/CLIENT-INTAKE-FORM]]). Here's what we need from you in the first week:

- **Brand assets:** Logo (SVG preferred), brand colors (hex codes), any fonts you use
- **Photography:** Up to 10 images per location (exterior, interior, staff — we can work with phone photos)
- **Copy:** Pharmacy name, address, hours, phone, any custom messaging ("Family-owned since 1987")
- **API details:** The endpoint URL and authentication method for your pharmacy management system's queue/status API
- **Compliance contact:** Name and email of your internal compliance officer or legal contact

That's it. LocalWeb handles the rest.

---

## The Build Phase

Weeks 2–3 are ours. Here's what happens:

1. Clone the RxReady template to your network's configuration
2. Apply brand colors, logo, and copy
3. Configure the Cloudflare Worker with your API endpoint
4. Set up location routing (each pharmacy gets its own URL path: `/westside`, `/downtown`, etc.)
5. Build the admin heatmap dashboard (password-protected, one login for all locations)
6. Internal testing with your compliance officer before anything goes public

---

## Monthly Support

After launch, your monthly retainer includes:

- **Up to 1 hour of updates** per month: text changes, hour updates, image swaps, minor layout requests
- **Cloudflare monitoring:** We watch your site's performance and uptime metrics quarterly
- **Bug fixes:** If something breaks, we fix it — no extra charge
- **Form submission review:** We confirm Formspree routes are working after any infrastructure changes

If you need more than 1 hour in a given month, we send a change order first. Standard rate: $95/hr. You approve before we start.

---

## No Vendor Lock-In

The output of LocalWeb's work is standard HTML, CSS, and JavaScript — plus Cloudflare configuration files. If you ever want to move to a different host, a different vendor, or manage it yourself:

- All source files are yours
- Cloudflare account transfer takes about 30 minutes
- The Worker code is documented so any developer can maintain it
- We provide a "handoff package" on request at no extra charge

You're not locked in. We earn your continued business by being the best option, not by making it painful to leave.

---

## Summary

| What we do | Timeline |
|---|---|
| Intake and asset collection | Week 1 |
| Site build + queue setup | Week 2 |
| Testing + compliance review | Week 3 |
| Soft launch → public launch | Week 4 |
| Ongoing support + monitoring | Monthly |

Next: [[00-SHARED/Human-Inbox/hustle/03-RXREADY-DEEP-DIVE]] — the full story on how RxReady works.
