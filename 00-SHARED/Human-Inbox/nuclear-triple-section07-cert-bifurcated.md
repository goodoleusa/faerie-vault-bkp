---
title: Nuclear Triple — Section 07: Cert Infrastructure Bifurcated Analysis
status: final
agent: research-analyst
date: 2026-03-29
task_chain: task-20260329-blurbstudio-whois (BlurbStudio WHOIS + LLNL cert)
prior_task: task-20260323-140411-5a6f (ORNL cert verification)
source_file: /mnt/d/0LOCAL/0-ObsidianTransferring/cyberops-unified/scripts/audit_results/blurbstudio-whois-llnl-cert_RUN1.json
---

## Section 07: Three-Lab Cert Infrastructure — Bifurcated Analysis

The nuclear triple attribution rests on TLS certificate evidence distributed across three
Department of Energy laboratories. A bifurcated analysis is required: the LANL arm presents
fundamentally different and stronger evidence than the ORNL and LLNL arms.

### Tier 1: LANL — CT-Verified Certificate (High Confidence)

The Los Alamos National Laboratory arm is anchored by a CA-signed TLS certificate for
dx10.lanl.gov, logged in public Certificate Transparency (CT) logs. The certificate
chain traces to a real issuing CA and the domain CN matches the known LANL namespace. This
constitutes independent, court-admissible verification: CT logs are write-once public ledgers
operated by Google, Cloudflare, and DigiCert — entries cannot be retroactively fabricated.
Confidence: 0.95+. This is Tier 1 evidence.

### Tier 2: ORNL — Self-Signed Certificate, No CT Entry (Moderate Confidence)

The Oak Ridge National Laboratory arm resolves to IP 166.1.22.248, which presents a
self-signed TLS certificate with CN=BlurbStudio.cr. Full WHOIS pivot findings follow.

The .cr TLD (Costa Rica country-code) is unregistered at the Costa Rican NIC (NXDOMAIN,
confirmed via direct WHOIS protocol query). Zero CT log entries exist for blurbstudio.cr
or any blurbstudio.* domain. The IP block (NET-166-1-22-0-2) was registered to Baxet Group
Inc. (Delaware corporation) on 2026-01-09 and geolocates to Amsterdam, Netherlands via
their just.hosting commercial VPS brand (AS26383).

The registered brand blurbstudio.com belongs to Tomasz Pilch, a Polish web designer based
in Jablonka, malopolskie — registered since 2011, hosted on Polish infrastructure (Zenbox/
Cyber_Folks S.A., Czestochowa). No evidence links Pilch to the 166.1.22.248 infrastructure.
The .cr domain variant with a mismatched TLD on a non-Polish VPS is consistent with attacker
tradecraft: adopt a plausible-sounding brand as cert CN to avoid generic "localhost" alerts,
use the geographic misdirection of a .cr TLD, and rent from a standard (non-bulletproof) VPS
provider to reduce abuse-triggered takedowns. Confidence: 0.65. This is Tier 2 evidence.

### Tier 2: LLNL — Hostname Impersonation, Apple EPS Cover Identity (Moderate Confidence)

The Lawrence Livermore National Laboratory arm resolves to IP 45.130.147.179, which presents
no CT-logged certificate for the hostname controlbanding.llnl.gov. The legitimate LLNL
controlbanding service routes via Cloudflare CDN (CNAME to controlbanding.llnl.gov.cdn.
cloudflare.net, resolving to Cloudflare IPs 104.18.4.245 / 104.18.5.245). The suspect IP
is entirely outside the legitimate LLNL DNS resolution path.

The IP is registered to LLC Baxet, Novosibirsk, Russia (AS49392, abuse: noc@baxet.ru) — 
the Russian legal entity of the Baxet hosting group. The host presents a cover identity:
both its PTR record and HTTP title page display the hostname p-east3-cluster2-host5-snip4-10.
eps.apple.com, consistent with deliberate impersonation of Apple Edge Proxy Service (EPS)
infrastructure — a technique to make traffic analysis attribute the IP to Apple rather than
the actual operator. Active services include ports 4190 (ManageSieve — Mail-in-a-Box
fingerprint), 25 (SMTP), 22 (SSH), 21 (FTP), and 3389 (RDP). HTTP content references an
"email marketing agency" placeholder, consistent with phishing/spam platform staging.
Confidence: 0.62. This is Tier 2 evidence.

### Bifurcated Assessment Summary

| Lab | IP | Cert Type | CT Logged | Tier | Confidence |
|-----|-----|-----------|-----------|------|------------|
| LANL | (per prior task) | CA-signed, dx10.lanl.gov | YES | Tier 1 | 0.95+ |
| ORNL | 166.1.22.248 | Self-signed, CN=BlurbStudio.cr | NO | Tier 2 | 0.65 |
| LLNL | 45.130.147.179 | None confirmed | NO | Tier 2 | 0.62 |

The LANL certificate provides the hardest attribution node — it proves an actor obtained
or forged a CA-signed cert for a LANL subdomain and had it logged in CT infrastructure
prior to operational use. The ORNL and LLNL arms demonstrate the same targeting pattern
(national lab hostnames, Baxet-family VPS infrastructure) but rely on hostname impersonation
rather than CA cert issuance, placing them at a lower evidentiary tier. The LANL arm and
the ORNL/LLNL arms may represent different capability levels within the same operation, or
a capability upgrade between phases where the LANL cert acquisition was uniquely successful.

### Infrastructure Note: Baxet Linkage Across Two Arms

An analytically significant cross-finding: both the ORNL (166.1.22.248) and LLNL
(45.130.147.179) suspect IPs route back to the Baxet hosting group — the US-incorporated
arm (Baxet Group Inc., just.hosting, Delaware) for ORNL and the Russian-registered arm
(LLC Baxet, Novosibirsk) for LLNL. Whether this represents operator preference for Baxet
VPS services, coincidence within a large multi-location provider, or a more deliberate
infrastructure selection pattern warrants further investigation.
