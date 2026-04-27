---
title: Implementation Roadmap — 4 Weeks to Live
type: guide
project: localweb
parent: [[00-SHARED/Human-Inbox/hustle/README]]
tags: #product-localweb #narrative #implementation
status: final
doc_hash: sha256:40102e029825da8a06cf03b92c1777fc3f3b9eeabefb2e00a388260c6e6a605d
created: 2026-04-01
hash_ts: 2026-04-01T16:07:00Z
hash_method: body-sha256-v1
---

# Implementation Roadmap — 4 Weeks from Contract to Live

This document explains exactly what happens between signing a contract with LocalWeb Studio and your first patient using the RxReady site. Responsibilities are clearly split.

---

## Timeline Overview

```
Week 1: Assets + Information Gathering
Week 2: Site Build + Queue System Setup
Week 3: Testing + Compliance Review
Week 4: Soft Launch → Refine → Public Launch
```

---

## Week 1 — Your Responsibilities (Assets Gathering)

LocalWeb sends you a structured intake form (see [[templates/CLIENT-INTAKE-FORM]]) within 24 hours of contract signing. You have one week to return it.

**Brand assets**
- Logo files (SVG or PNG at minimum 400px wide)
- Brand color hex codes
- Any custom fonts or typography guidelines
- Optional: existing brand standards document

**Photography**
- Up to 10 photos per location (exterior storefront, interior, staff if approved)
- Acceptable formats: JPEG, PNG, HEIC — phone camera quality is fine
- If you have no photos, we can use a curated set of licensed stock images at no extra charge

**Copy and content**
- Pharmacy name(s) and any DBA names
- Physical addresses for all locations
- Hours of operation (including holiday variations)
- Phone numbers and primary contact email per location
- Any custom messaging ("Family pharmacy since 1987," "Bilingual staff available")
- Approved prescription status strings (we provide a default list; you approve or edit)

**Technical**
- Your pharmacy management system's API endpoint URL
- Authentication method (API key, OAuth, or basic auth — we support all three)
- A sandbox/test environment for us to verify connectivity before touching live data
- Contact details for your IT administrator in case we need troubleshooting help

**Compliance**
- Name and email of your compliance officer or legal contact
- Confirmation of which compliance review they will conduct (see [[00-SHARED/Human-Inbox/hustle/06-COMPLIANCE-BOUNDARIES]])

---

## Week 2 — LocalWeb Responsibilities (Site Build)

Once we have your assets:

1. **Clone and configure the RxReady template** — apply your brand colors, logo, typography
2. **Build location pages** — each location gets a dedicated URL path with its own queue display
3. **Configure the Cloudflare Worker** — connect to your API endpoint, map status codes to display strings, set authentication headers
4. **Set up the admin dashboard** — create your network's heatmap view, configure location labels
5. **Formspree integration** — delivery booking forms route to your designated staff email
6. **Deploy to staging environment** — a private URL where only you and your team can see the site

You receive a staging URL at the end of Week 2 with a brief walkthrough video (10–15 min) showing what was built and how to navigate the admin dashboard.

---

## Week 3 — Testing and Compliance Review

**Your testing responsibilities:**
- [ ] Verify each location's queue data is displaying correctly
- [ ] Test prescription lookup with at least 10 Rx numbers (using your sandbox environment)
- [ ] Confirm status strings match your approved list
- [ ] Test the delivery booking form end-to-end (submit → confirm staff email received)
- [ ] Review admin dashboard for accuracy
- [ ] Compliance officer review (see checklist below)

**Compliance officer review items:**
- [ ] Confirm no PHI is visible in the patient-facing lookup
- [ ] Confirm data sharing agreement is reviewed (LocalWeb provides a template)
- [ ] Confirm privacy policy update is needed or not (most networks need a one-line addition)
- [ ] Sign off on status strings approved for display
- [ ] Confirm staff training plan

**LocalWeb testing responsibilities:**
- Security scan of all forms and API connections
- Performance testing (target: under 2 seconds page load on mobile)
- Cross-browser testing (Chrome, Safari, Firefox, Edge — desktop and mobile)
- Accessibility check (WCAG 2.1 AA minimum)

**If issues are found in Week 3:** We resolve them before moving to Week 4. This week has a built-in buffer.

---

## Week 4 — Launch

**Soft launch (staff-only access):**
- Site goes live at a non-publicized URL
- All staff test the patient-facing experience
- Any final feedback incorporated
- Typically 2–3 business days

**Public launch:**
- DNS pointed to live site (takes 24–48 hours to fully propagate)
- Staff training video shared (30-minute walkthrough of admin dashboard and queue management)
- You receive:
  - Live website URL(s) per location
  - Admin dashboard login credentials
  - Cloudflare account access (you get your own Cloudflare login, not shared with LocalWeb)
  - PDF documentation: site structure, update process, what to do if something breaks

---

## Ongoing After Launch

| Month | Activity |
|---|---|
| Month 1 | Check-in call (30 min) — is the queue system performing as expected? |
| Months 2–3 | Heatmap review — we share observations on your demand patterns |
| Month 3 | Quarterly Cloudflare security audit |
| Ongoing | Up to 1 hr/month of content updates included in retainer |

---

## What Happens If You're Not Ready in Week 1

Life happens. If assets aren't ready in Week 1:

- Timeline shifts by the number of days delayed — everything else stays the same
- We work with whatever you have and flag gaps (e.g., "we'll use stock photos until yours arrive")
- If delay is more than 2 weeks, we may need to reschedule the project slot

This is not punitive — it's project management reality. The earlier you complete the intake, the sooner you go live.

---

*Next: [[00-SHARED/Human-Inbox/hustle/05-PRICING-PLAYBOOK]] — full pricing model and ROI analysis*
