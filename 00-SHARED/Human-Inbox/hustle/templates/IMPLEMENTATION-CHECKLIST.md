---
title: Implementation Checklist — RxReady Deployment
type: checklist
project: localweb
parent: [[00-SHARED/Human-Inbox/hustle/README]]
tags: #product-localweb #implementation
status: final
doc_hash: sha256:86700328c2c8ad22a237726b79a62bff7c116f4ff073c8b241921be3d638b464
created: 2026-04-01
hash_ts: 2026-04-01T16:12:28Z
hash_method: body-sha256-v1
---

# Implementation Checklist — RxReady Deployment

**Project:** [Client network name]
**Locations:** [Number of locations]
**Contract signed:** [Date]
**Target launch date:** [Date]
**LocalWeb operator:** [Your name]
**Client point of contact:** [Name + email]
**Client IT contact:** [Name + email]
**Client compliance contact:** [Name + email]

---

## WEEK 1 — Assets and Information Gathering

### Client Responsibilities (Client completes, notifies LocalWeb when done)

**Brand + visual**
- [ ] Logo file delivered (SVG or PNG 400px+)
- [ ] Brand color hex codes confirmed
- [ ] Typography or font names provided
- [ ] Brand standards document provided (if exists)

**Photography**
- [ ] Photos delivered for each location (or stock imagery approved)
- [ ] Staff photo consent obtained (if staff photos used)

**Copy and content**
- [ ] Pharmacy name(s) and DBA names confirmed
- [ ] Address, phone, hours per location confirmed
- [ ] Holiday/special hours schedule provided
- [ ] Custom messaging copy approved (tagline, any special notes)
- [ ] Languages confirmed (English only, or bilingual)

**Technical**
- [ ] Pharmacy management system identified
- [ ] API documentation provided (or API contact introduced)
- [ ] Sandbox environment access confirmed
- [ ] API endpoint URL (sandbox) provided
- [ ] Authentication credentials for sandbox provided
- [ ] IT administrator introduced to LocalWeb

**Compliance**
- [ ] Compliance officer introduced to LocalWeb
- [ ] Compliance officer has received data flow documentation
- [ ] Status strings reviewed and approved (see intake form Section 6)
- [ ] Privacy policy reviewed (attorney review, if needed)

**Admin access**
- [ ] Admin dashboard users listed (name + email for each)
- [ ] Preferred login method confirmed

---

## WEEK 2 — Site Build (LocalWeb Responsibilities)

**Template and branding**
- [ ] Template cloned for this client
- [ ] Brand colors applied to design system CSS variables
- [ ] Logo uploaded and sized correctly (header + favicon)
- [ ] Typography configured
- [ ] Stock photos or client photos uploaded and optimized (WebP, correct dimensions)

**Location pages**
- [ ] Location pages created for each location (URL slug: /[slug])
- [ ] Address, phone, hours populated per location
- [ ] Map embed configured (Leaflet, no Google API key needed)
- [ ] Any custom per-location messaging added

**Queue system**
- [ ] Cloudflare Worker created for this client
- [ ] API endpoint (sandbox) configured as encrypted secret
- [ ] Status code → display string mapping implemented
- [ ] Queue display component connected to Worker
- [ ] Prescription lookup form connected to Worker
- [ ] Rate limiting configured on Worker (prevent scraping)

**Delivery booking**
- [ ] Formspree endpoint created and tested
- [ ] Delivery booking form connected to Formspree
- [ ] Staff notification email(s) confirmed and tested
- [ ] Spam filter / honeypot field added to form

**Admin dashboard**
- [ ] Cloudflare KV namespace created for heatmap data
- [ ] Admin dashboard route configured at `/admin`
- [ ] Cloudflare Access (or password check) configured for admin route
- [ ] Heatmap component connected to KV data
- [ ] Admin credentials documented and stored securely

**Deployment to staging**
- [ ] Site built and deployed to staging URL (Cloudflare Pages preview)
- [ ] Staging URL shared with client
- [ ] Walkthrough video recorded and shared (10–15 min)
- [ ] All location URL paths tested
- [ ] HTTPS confirmed on all routes

---

## WEEK 3 — Testing and Compliance Review

### Client Testing Responsibilities

**Patient-facing**
- [ ] Queue display shows correct zone labels and times
- [ ] Prescription lookup tested with at least 10 Rx numbers (sandbox)
- [ ] All approved status strings display correctly
- [ ] Delivery booking form submits successfully
- [ ] Staff receives booking notification email within 60 seconds

**Admin dashboard**
- [ ] Admin can log in to dashboard
- [ ] Heatmap shows data for all locations
- [ ] Location labels are correct
- [ ] All admin users can access

**Mobile and cross-browser**
- [ ] Site tested on iOS Safari
- [ ] Site tested on Android Chrome
- [ ] Site tested on desktop Chrome, Firefox, Safari, Edge

### Compliance Review Responsibilities (Compliance Officer)

- [ ] Data flow diagram reviewed and acknowledged
- [ ] No PHI visible in any patient-facing lookup response
- [ ] Approved status strings confirmed (sign-off document attached)
- [ ] Privacy policy reviewed; any needed updates completed
- [ ] Data sharing review completed (with attorney if required)
- [ ] Staff training plan confirmed

### LocalWeb Testing Responsibilities

- [ ] Security scan of all forms (no XSS vulnerabilities)
- [ ] Worker injection testing (Rx number field tested with malicious input)
- [ ] Performance test: page load under 2 seconds on 4G mobile (Lighthouse score target: 90+)
- [ ] Accessibility check: WCAG 2.1 AA compliance confirmed
- [ ] SSL certificate valid and auto-renewing (Cloudflare manages this)
- [ ] Formspree rate limiting confirmed (prevents spam flood)
- [ ] Worker error handling confirmed (graceful failure if API is down)

---

## WEEK 4 — Launch

### Soft Launch (Days 1–3)

- [ ] Site moved from staging to production Cloudflare Pages project
- [ ] Production URL configured (Cloudflare Pages subdomain or custom domain)
- [ ] All staff-only testing completed
- [ ] Client provides written soft launch sign-off

### DNS and Custom Domain (if applicable)

- [ ] Custom domain added to Cloudflare Pages project
- [ ] DNS records updated (CNAME or A record pointing to Cloudflare)
- [ ] DNS propagation confirmed (24–48 hours)
- [ ] HTTPS certificate issued for custom domain

### Production API Switch

- [ ] Worker updated to use production API endpoint
- [ ] Production API credentials stored as encrypted Cloudflare secret
- [ ] Prescription lookup tested with 3 real Rx numbers (with client IT oversight)
- [ ] Queue display showing live data confirmed

### Deliverables to Client

- [ ] Live website URL(s) per location
- [ ] Admin dashboard URL + login credentials
- [ ] Cloudflare account credentials (client's own account, not shared with LocalWeb)
- [ ] Staff training video (30 min) sent to client
- [ ] PDF documentation: site structure, update process, incident response
- [ ] Worker source code (copy for client's records)
- [ ] Handoff package (all source files) uploaded to agreed location

### Client Sign-Off

- [ ] Client confirms site is live and performing correctly
- [ ] Client confirms receipt of all deliverables
- [ ] First monthly invoice scheduled for next billing cycle

---

## POST-LAUNCH — Ongoing Monitoring

**Month 1**
- [ ] Check-in call scheduled (30 min)
- [ ] Cloudflare analytics reviewed (traffic, errors, Worker invocations)
- [ ] Form submission routing confirmed still working

**Month 3**
- [ ] Quarterly Cloudflare security audit completed
- [ ] Heatmap data reviewed with client (demand patterns shared)
- [ ] SSL certificate expiry date confirmed (should be auto-renewing)
- [ ] API authentication still valid (rotate API key if expired)

**Ongoing**
- [ ] Monthly support hours tracked per client
- [ ] Change orders documented when hours exceeded
- [ ] Renewal reminder sent 60 days before contract end date
