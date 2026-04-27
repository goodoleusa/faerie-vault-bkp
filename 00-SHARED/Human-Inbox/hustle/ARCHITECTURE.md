---
title: LocalWeb Studio — Architecture & Operations
type: architecture
status: draft
project: localweb
parent: [[00-SHARED/Hive/01-ARCHITECTURE.md]]
children: []
tags: [product-localweb, architecture, operations]
doc_hash: sha256:pending
created: 2026-04-01
blueprint: "[[Blueprints/Research-Brief.blueprint]]"
agent_type: research-analyst
session_id: localweb-arch-001
promotion_state: awaiting-annotation
---

# LocalWeb Studio — Architecture & Operations

## Executive Summary

LocalWeb Studio is a solo-operator web design and hosting business built around six vertical-specific static site templates, three service tiers, and a single genuine technical differentiator: the RxReady pharmacy queuing system. The architecture is deliberately minimal — Astro builds to static HTML, Cloudflare Pages serves it, Formspree handles forms, and Cloudflare Workers provide the only thin backend surface (scoped to RxReady). Every tool choice prioritizes portability and zero vendor lock-in. The business model is template amortization: 8–12 hours to build a vertical template once, 2–4 hours to customize per client, with full margin recovery by client #3 in each vertical.

This document maps the full operational and technical architecture: how a prospect becomes a client, how the six templates relate to each other and their markets, how the tech stack interconnects, how money flows, and how a solo operator stays under capacity at 35 active clients.

**Source:** `/mnt/d/0LOCAL/gitrepos/hustle/business-plan-localweb.md`

---

## Diagram 1 — Client Service Flow

How a prospect moves from first contact to live site and into ongoing retention.

```mermaid
flowchart TD
    A([Prospect\nDiscovery]) --> B{Outreach\nChannel}
    B --> |Chamber/BNI| C[Networking Event]
    B --> |Google Search| D[Cold Outreach\nPostcard + QR]
    B --> |Referral| E[Existing Client\n$100 Credit]
    B --> |Audit Lead| F[Free Website Audit\n24hr PDF delivery]

    C --> G[Sales Conversation]
    D --> G
    E --> G
    F --> G

    G --> H{Tier\nSelection}
    H --> |Starter\n$799 setup + $79/mo| I[5-page static site\n3-4 day delivery]
    H --> |Growth\n$1,499 setup + $129/mo| J[10 pages + vertical features\n4-7 day delivery]
    H --> |Full-Service\n$2,499+ setup + $199/mo| K[Full template + integrations\n7-10 day delivery]

    I --> L[Intake Form\nAsset Collection]
    J --> L
    K --> L

    L --> M[Template Clone\n15 min]
    M --> N[Brand Config\n30 min]
    N --> O[Image Swap + Optimize\n60 min]
    O --> P[Content Population\n90 min]
    P --> Q[Forms + Maps Config\n60 min]
    Q --> R[Cloudflare Deploy\nSSL Auto-provision\n30 min]
    R --> S[QA Checklist\nMobile/PageSpeed/404\n60 min]
    S --> T[Client Review Call\n+ Tweaks 60 min]
    T --> U([LIVE SITE\n~7.5 hrs total])

    U --> V[Ongoing Retainer]
    V --> W[Monthly 1hr Maintenance\nAnalytics + Updates]
    W --> X{Change\nRequest?}
    X --> |Included\nText/hours/images| W
    X --> |Billable $95/hr\nNew pages/features| Y[Change Order\nSign-off]
    Y --> W

    V --> Z{Churn\nRisk?}
    Z --> |Offboarding| AA[Hosting Handoff\n$299 fee\nRepo + DNS transfer]
    Z --> |Watch-only\n$49/mo| AB[Monitoring Tier]
```

The critical constraint is the intake form — the site cannot start until all assets are in hand. The 7.5-hour build target assumes complete asset delivery. Delays in client asset collection are the primary schedule risk, not the technical work.

---

## Diagram 2 — Template Ecosystem

All six vertical templates, their key differentiators, and pricing anchors.

```mermaid
graph TB
    subgraph TEMPLATES["Template Product Line"]
        direction TB

        FC["FoundationCraft\nConstruction / Contracting\n---\nBefore/after lightbox gallery\nLeaflet service area map\nQuote request form\nGoogle Reviews embed\nLicense/insurance trust badges\n---\nStarter $799 / Growth $1,299\n3-4 day delivery"]

        TT["TableTurn\nRestaurant / Bar\n---\nInline HTML menu (SEO-indexed)\nHoliday hours display\nOpenTable/Resy embed\nStatic JSON events calendar\nInstagram oEmbed feed\n---\nGrowth $1,499 / Full $2,199\n4-5 day delivery"]

        RX["RxReady\nPharmacy\n---\nPrescription status lookup widget\nReal-time queue wait + heatmap\nDelivery booking form\nMulti-location chain finder\nInsurance accepted list\n---\nFull $3,499-$4,999\n$249-$399/mo retainer\n7-10 day delivery"]

        ZR["ZoneRunner\nDelivery Service\n---\nLive order status page\nLeaflet zone coverage map\nDemand heatmap visualization\nService booking form\nFAQ accordion\n---\nGrowth $1,799 / Full $2,799\n5-7 day delivery"]

        CC["CounselClear\nSmall Legal Firm\n---\nPractice area pages (SEO intent)\nAttorney bio pages\nCalendly/Cal.com booking embed\nWCAG 2.1 AA compliant by default\nTrust-signal design language\nCase results summary\n---\nGrowth $1,499 / Full $2,299\n4-5 day delivery"]

        DM["DistrictMap\nBusiness Association\n---\nInteractive member story map\nCard grid with category filter\nMembership tier + benefits table\nStatic JSON event listings\nSponsor logo wall\nFormspree newsletter signup\n---\nFull $2,999-$3,999\n$179/mo retainer\n6-8 day delivery"]
    end

    subgraph SHARED["Shared Foundation (All Templates)"]
        direction LR
        S1[Astro 4.x build]
        S2[Cloudflare Pages hosting]
        S3[Formspree contact form]
        S4[Cloudflare DNS + SSL]
        S5[Cloudflare Web Analytics]
        S6[Mobile-responsive layout]
        S7[95+ PageSpeed target]
    end

    FC & TT & RX & ZR & CC & DM --> SHARED

    RX -.->|"DIFFERENTIATOR\nCloudflare Workers + KV\nSupabase for chains"| BACKEND["Thin Backend\n(RxReady only)"]
```

Every template shares the same deployment pipeline. RxReady is the only template with a backend surface — and that backend is scoped to a single Cloudflare Worker, not a server. The interactive map templates (FoundationCraft, ZoneRunner, DistrictMap) all use Leaflet.js with no API key billing risk.

---

## Diagram 3 — Tech Stack Relationships

How all tools interact across the build, serve, and integrate layers.

```mermaid
graph LR
    subgraph BUILD["Build Layer"]
        A1[GitHub Repo\nclient branch per client] --> A2[Astro 4.x\nor 11ty for Starter]
        A2 --> A3[Static HTML/CSS/JS\npre-built at deploy time]
    end

    subgraph SERVE["Serve Layer"]
        A3 --> B1[Cloudflare Pages\nGit-based auto-deploy\nFree tier]
        B1 --> B2[Global CDN\n<200ms load\nenterprise uptime]
        B1 --> B3[Cloudflare DNS\nFree, DDoS protected\nProxied by default]
        B3 --> B4[SSL Auto-provision\nLet's Encrypt via CF]
    end

    subgraph FORMS["Form Layer"]
        B2 --> C1[Formspree\nForm endpoint\nFree tier]
        C1 --> C2[Client Email\nNotification]
    end

    subgraph MAPS["Map Layer"]
        B2 --> D1[Leaflet.js\nOpen source\nNo API key]
        D1 --> D2[Location Data\nHardcoded JSON\nor client-supplied CSV]
    end

    subgraph BOOKING["Booking Layer"]
        B2 --> E1[Cal.com\nor Calendly\nEmbed]
        E1 --> E2[Client Calendar\nNotification]
    end

    subgraph ANALYTICS["Analytics Layer"]
        B2 --> F1[Cloudflare Web Analytics\nPrivacy-preserving\nNo cookies\nNo GDPR friction]
    end

    subgraph BACKEND["Backend Layer — RxReady Only"]
        B2 --> G1[Cloudflare Worker\nStateless edge function\nScales to zero]
        G1 --> G2[Cloudflare KV\nQueue state per location\nFast reads]
        G1 --> G3[Supabase\nPostgres — chain-wide state\nPrescription cache TTL 4hr]
        G1 --> G4[Pharmacy Internal API\nWebhook or direct call\nStatus passthrough only]
        G4 -.->|"PHI boundary\nOperator's system only"| G5[(Pharmacy\nPHI Repository\nNOT on our infra)]
    end

    subgraph DELIVERY["Delivery Form — RxReady Only"]
        B2 --> H1[Formspree\nor Netlify Forms]
        H1 --> H2[Pharmacy Notification\nEmail / SMS via Twilio\nor Slack webhook]
    end
```

The PHI boundary is the most important architecture constraint: the Cloudflare Worker is a passthrough proxy to the pharmacy's own system. No patient data lands in LocalWeb infrastructure. The Worker returns only status strings — the pharmacy's existing system remains the sole PHI repository.

---

## Diagram 4 — RxReady Deep Dive

Data flow, PHI isolation, and the queue visualization system.

```mermaid
flowchart TD
    subgraph PATIENT["Patient-Facing Frontend\n(Static CDN — Cloudflare Pages)"]
        P1[Patient enters\nRx number + DOB] --> P2[fetch to CF Worker\nevery 60s polling]
        P3[Heatmap display\nHour-of-day SVG/Canvas\nGreen-Amber-Red gradient] --> P4[Queue wait display\ncurrent slots + avg wait]
        P5[Delivery booking form\nName + address + Rx + window] --> P6[Formspree endpoint]
    end

    subgraph WORKER["Cloudflare Worker\n(Edge — No Persistent Server)"]
        W1[Status Lookup\nEndpoint] --> W2{Route}
        W2 --> |Rx lookup| W3[Proxy to Pharmacy API\npassthrough only]
        W2 --> |Queue read| W4[Read KV: location+date\nslots_remaining\navg_wait_mins\ndemand_level]
        W2 --> |Heatmap data| W5[Aggregate KV history\n30-day rolling window\nhourly demand averages]
        W6[Admin Endpoint\nPassword-protected URL] --> W7[Write queue state to KV\npharmacist-triggered]
        W6 --> W8[Write queue state to Supabase\nchain-wide sync]
    end

    subgraph STORAGE["Storage Layer"]
        KV[(Cloudflare KV\nlocation+date keys\nfast local reads\nper-location ops)]
        SB[(Supabase\nPostgres\nlocations table\nqueue_state table\nrx_status_cache 4hr TTL\ndelivery_bookings)]
    end

    subgraph PHARMACY["Pharmacy Systems\n(Operator-Controlled — PHI Lives Here)"]
        PA[Pharmacy Internal API\nor webhook endpoint]
        PHI[(PHI Repository\nFull Rx records\nPatient data\nNOT on our infra)]
        PA --- PHI
    end

    subgraph NOTIFICATIONS["Notification Layer"]
        NF[Formspree captures\ndelivery booking]
        NF --> N1[Client Email]
        NF --> N2[SMS via Twilio webhook]
        NF --> N3[Slack webhook]
    end

    P2 --> W1
    W3 --> PA
    W3 -.->|"Returns ONLY:\nReady / Processing /\nInsurance pending /\nRequires consultation"| P2
    W4 --> KV
    W5 --> KV
    W7 --> KV
    W8 --> SB
    P5 --> NF

    subgraph PHI_BOUNDARY["PHI Isolation Rules"]
        direction LR
        R1["No Rx numbers stored in KV"]
        R2["No DOBs stored anywhere"]
        R3["Status strings only returned"]
        R4["Rx number hashed in cache key\nnot stored plaintext"]
        R5["No analytics on RxReady pages"]
        R6["Operator provides API endpoint\nOperator owns PHI compliance"]
    end
```

The heatmap is driven by historical KV aggregates — not live tracking of individual patients. It shows "Wednesday 2pm is typically busy" derived from aggregate demand levels, not individual prescription records. The admin endpoint is a URL-path-protected page within the same Astro site, not a separate app, keeping deployment simple.

---

## Diagram 5 — Revenue Model

How setup fees, retainers, and add-ons compound across client counts.

```mermaid
graph TB
    subgraph REVENUE_STREAMS["Revenue Streams"]
        S1["Setup Fees\nOne-time\nStarter $799\nGrowth $1,499\nFull $2,499+\nRxReady $3,499-$4,999"]
        S2["Monthly Retainers\nRecurring\nStarter $79/mo\nGrowth $129/mo\nFull $199/mo\nRxReady $249-$399/mo"]
        S3["Add-On Services\nBillable separately\nSEO audit $299\nGBP setup $149\nPhoto coord $199\nContent refresh $99\nADA audit $399\nChange requests $95/hr"]
    end

    subgraph TEMPLATE_AMORTIZATION["Template Build Economics"]
        T1["Build cost: 8-12hrs @ implied rate\nCustomize per client: 2-4hrs\nBreak-even: Client #3\nPure margin: Client #10+"]
        T1 --> T2["6 templates x 10-20 clients each\n= 60-120 lifetime template sales"]
    end

    subgraph SCENARIOS["Monthly Recurring Revenue Scenarios"]
        direction LR
        SC1["$3K/mo Scenario\n20 Starter @ $79 = $1,580\n5 Growth @ $129 = $645\n+ ~$1,000 setup avg\n= ~$3,225/mo"]
        SC2["$6K/mo Scenario\n15 Starter @ $79 = $1,185\n15 Growth @ $129 = $1,935\n5 Full @ $199 = $995\n+ ~$1,500 setup avg\n= ~$6,040/mo"]
        SC3["$10K/mo Scenario\n10 Growth @ $129 = $1,290\n15 Full @ $199 = $2,985\n2 RxReady @ $324 avg = $648\n+ add-ons ~$2,000\n= ~$9,525/mo"]
    end

    subgraph OVERHEAD["Fixed Overhead"]
        O1["Software/tools: $100/mo\nBusiness insurance: $100/mo\nMarketing/misc: $100/mo\nTotal: ~$300/mo\nBreak-even: 4 Starter clients"]
    end

    subgraph MARGINS["Margin by Tier (Steady State)"]
        direction LR
        M1["Starter $79/mo\n~1hr maintenance\nMargin after time cost: ~$65/mo"]
        M2["Growth $129/mo\n~1hr maintenance\nMargin after time cost: ~$115/mo"]
        M3["Full $199/mo\n~1hr maintenance\nMargin after time cost: ~$180/mo"]
        M4["RxReady $324/mo avg\n~1.5hr maintenance\nMargin after time cost: ~$285/mo"]
    end

    S1 & S2 & S3 --> SCENARIOS
    TEMPLATE_AMORTIZATION --> SC3
    OVERHEAD --> SC1
```

RxReady is the margin engine. Five pharmacy clients at $324/mo average equals $1,620 MRR — equivalent to 20+ Starter clients. The $10K/mo scenario requires only 27 total clients (10 Growth + 15 Full + 2 RxReady) versus the 35-client capacity ceiling, leaving headroom for new builds. Setup fees are excluded from steady-state margin because they are non-recurring, but they are critical in months 1-12 to fund the template build cost.

---

## Diagram 6 — Operational Workflow

How a solo operator allocates time across onboarding, ongoing maintenance, and capacity ceiling.

```mermaid
flowchart LR
    subgraph WEEK1["Week 1 — New Client Onboarding\nTarget: 8 hrs operator time"]
        W1A[Intake form sent\nAssets collected] --> W1B[Day 1-2: Template clone\nBrand config\n45 min]
        W1B --> W1C[Day 2-3: Content + images\nForms + maps\n3.5 hrs]
        W1C --> W1D[Day 3: Deploy\nQA\n1.5 hrs]
        W1D --> W1E[Day 4-5: Client review\nTweaks\n1 hr]
        W1E --> W1F([LIVE\n~7.5 hrs total])
    end

    subgraph MONTHLY["Ongoing Monthly — Per Client\nTarget: 1 hr or less"]
        M1[Cloudflare analytics\n10 min] --> M2[Uptime check\nautomated alert]
        M2 --> M3[Content update requests\nup to 30 min included]
        M3 --> M4{Quarterly?}
        M4 --> |Yes| M5[PageSpeed audit\nBroken link check\n20 min extra]
        M4 --> |No| M6([Done for month])
        M5 --> M6
    end

    subgraph CAPACITY["Monthly Capacity — 35 Client Ceiling"]
        C1["Maintenance: 35 clients x 1hr = 35hrs"] --> C2["New builds: 2/mo x 8hrs = 16hrs"]
        C2 --> C3["Sales + admin: ~20hrs"]
        C3 --> C4([~71 hrs/mo\nHire contractor at 28-30 clients])
    end

    subgraph YEAR1["Year 1 Milestones"]
        Y1["Mo 1-2: 3 clients\nDemo sites built\nChamber joined"] --> Y2["Mo 3-4: 8 clients\nReferral program live\nSBDC relationship"]
        Y2 --> Y3["Mo 5-6: 15 clients\nFirst RxReady\nFull template line"]
        Y3 --> Y4["Mo 7-9: 22 clients\n$3K+ MRR\nFirst contractor consideration"]
        Y4 --> Y5["Mo 10-12: 28-30 clients\n$5K+ MRR\nSystematic referral pipeline"]
    end
```

The capacity math: 35 clients x 1hr maintenance + 2 builds x 8hrs + 20hrs admin = 71 hours/month, which is above a sustainable solo pace. The hire trigger should be at 28-30 active clients, not at the stated 35-client ceiling, to protect build time — which is the primary new revenue generator.

---

## Implementation Notes for Developers

Concrete steps and configuration touchpoints when cloning a template for a new client.

### Astro Configuration Checklist (Per Client Clone)

**1. Config file — `src/config/site.yml` (or equivalent config object)**

```yaml
# Replace these on every clone:
business:
  name: "Client Business Name"
  phone: "+1-555-000-0000"
  email: "contact@client.com"
  address: "123 Main St, City, ST 00000"
  hours:
    mon_fri: "9am - 6pm"
    saturday: "10am - 4pm"
    sunday: "Closed"
  social:
    instagram: "https://instagram.com/clienthandle"
    facebook: "https://facebook.com/clientpage"

brand:
  primary_color: "#2B4C7E"      # client hex
  secondary_color: "#F4A261"    # client hex
  font_heading: "Montserrat"    # or client-specified
  font_body: "Open Sans"

cloudflare:
  analytics_token: "REPLACE_WITH_CLIENT_TOKEN"

formspree:
  endpoint: "https://formspree.io/f/REPLACE_WITH_CLIENT_ID"
```

**2. Cloudflare Pages — per client setup**
- Create new Pages project from GitHub branch (not fork)
- Set custom domain in Pages dashboard — Cloudflare handles SSL automatically
- Analytics: enable Cloudflare Web Analytics per site, copy token to config
- Workers (RxReady only): deploy Worker via `wrangler deploy`, bind KV namespace

**3. Formspree — per client setup**
- Create new form in Formspree dashboard
- Copy endpoint URL to config
- Set notification email to client's email address
- Enable reCAPTCHA on contact forms

**4. Leaflet.js maps (FoundationCraft, ZoneRunner, DistrictMap)**
- Set `MAP_CENTER: [lat, lng]` and `MAP_ZOOM: 11` in config
- Service area polygons: edit `src/data/service-area.geojson`
- Member pins (DistrictMap): edit `src/data/members.json` — one object per member with `lat`, `lng`, `name`, `category`, `description`, `url`

**5. Image optimization workflow**
- All images processed through Squoosh before commit
- Target: AVIF at 75% quality for hero images, WebP at 80% for gallery
- Max file size: 200KB per image, 80KB for thumbnails
- Use Astro's `<Image>` component — handles srcset automatically

**6. RxReady-specific Cloudflare Worker config**
- `wrangler.toml`: bind KV namespace as `QUEUE_STATE`
- Set environment variables: `PHARMACY_API_URL`, `PHARMACY_API_KEY`, `ADMIN_SECRET` (via Cloudflare dashboard, not in code)
- `ADMIN_SECRET` gates the admin endpoint — use a random 32-char string, share only with pharmacy staff
- Supabase (chain clients): set `SUPABASE_URL` and `SUPABASE_ANON_KEY` as Worker environment variables

**7. QA checklist before client review call**
- [ ] PageSpeed Insights score >= 95 mobile, >= 98 desktop
- [ ] Mobile layout check at 375px, 430px, 768px breakpoints
- [ ] All form submissions tested (check Formspree dashboard)
- [ ] Map loads and pins/polygons render correctly
- [ ] No 404s in browser console
- [ ] SSL active on custom domain (Cloudflare dashboard shows "Active")
- [ ] Business hours accurate
- [ ] Phone number and email links clickable on mobile (tel: and mailto: protocols)

### Template Customization Time Estimates

| Task | Estimate | Notes |
|---|---|---|
| Clone repo + create client branch | 15 min | `git checkout -b client-name` |
| Brand config (colors, fonts, info) | 30 min | Single config file |
| Image swap + Squoosh optimization | 60 min | 5-10 hero/gallery images |
| Content population | 90 min | Copy, menu, services, hours |
| Forms + maps config | 60 min | Formspree endpoint + coordinates |
| Cloudflare Pages deploy + DNS | 30 min | Git push triggers auto-deploy |
| QA checklist | 60 min | PageSpeed + mobile + forms |
| Client review tweaks | 60 min | Minor copy/image adjustments |
| **Total** | **~7.5 hrs** | Target: under 8 hrs |

### Hosting Handoff Protocol

When a client leaves or wants ownership:

1. Transfer GitHub repo to client's GitHub account (Settings > Transfer)
2. Client creates their own Cloudflare Pages account and imports repo
3. Update DNS A/CNAME records to point to client's Pages deployment
4. Export Formspree forms to client's account (Formspree supports this)
5. Record a 30-minute Loom walkthrough covering how to update the site
6. Invoice $299 offboarding fee + final month's retainer
7. Offer $49/mo "watch-only" monitoring if client wants continued oversight

---

*LocalWeb Studio Architecture — Generated 2026-04-01 from business-plan-localweb.md*
*Status: draft — update to final after human review*
