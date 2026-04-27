---
date: 2026-03-22
type: extraction-report
source: Russian business registry (EGRUL/EGRIP) PDFs
status: unread
hypothesis: H4 (foreign handoff)
task_id: task-20260315-143950-2b9f
tags: []
doc_hash: sha256:be44edbf3969c2b321ea36d8251cb4c0ab98782657e2fd638407a66ffb10c587
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:36Z
hash_method: body-sha256-v1
---

# Russian "Starlink" Entity Extraction — Plain English Summary

## What We Found

Two Russian business registration documents were extracted and analyzed. They describe two separate entities both connected to the "Starlink" name:

### Entity 1: Filatov Dmitry Andreevich (Individual Entrepreneur)

- **Who**: Dmitry Filatov, Russian citizen, male
- **What**: Registered as a solo entrepreneur doing internet retail sales
- **When**: March 7, 2024
- **Where**: Krasnodar, Russia (southern Russia, near Black Sea)
- **Tax ID (INN)**: 232524834996 — the "23" prefix means Krasnodar region
- **Registration number**: OGRNIP 324237500095600
- **Business type**: Online retail + "other retail outside shops"

### Entity 2: OOO "Starlink" (LLC)

- **Who**: Company owned 100% by Mikhail Berezhinsky (General Director)
- **What**: Wholesale agent for timber and construction materials
- **When**: September 11, 2024
- **Where**: Moscow (Severnoe Butovo district, ul. Polyany 5A)
- **Company tax ID**: INN 9727085540
- **Berezhinsky's personal tax ID**: INN 231533996303 — also a "23" (Krasnodar) INN
- **Capital**: 178,000 rubles (~$2,000 USD) — minimum viable capital
- **Registration number**: OGRN 1247700608946

### Screenshots Show Many Russian "Starlinks"

A search of the Russian business registry for "Старлинк" (Starlink in Russian) returns 20+ companies across Russia registered between 2002-2025. The name is popular — likely inspired by SpaceX Starlink, though none appear connected to SpaceX.

## Why This Matters

### The Krasnodar Connection

Both Filatov and Berezhinsky have tax IDs issued in Krasnodar Krai (region code 23), even though Berezhinsky's company is in Moscow. Krasnodar keeps appearing in this investigation:

- **ERA Technopolis**: Russian military research campus near Krasnodar, near the Black Sea
- **"wecandevelopit"**: A Russian tech outfit with Krasnodar proximity found in earlier evidence
- **Radio station hacking**: Krasnodar radio stations were hacked with fake messages (Ukrainian hackers suspected)
- **Branch offices**: A Montenegro/Moscow/Krasnodar entity found in other evidence had a Krasnodar branch at 26 Odesskaya Street

### Shell Company Indicators

OOO Starlink has several hallmarks of a shell or front company:
- **Minimum capital** (~$2K) — the legal minimum for an LLC
- **Standard template charter** (Type 01) — no custom governance
- **Single owner who is also the director** — common in shell setups
- **Generic business codes** — timber/construction wholesale with no apparent infrastructure
- **Quick setup** — registered and fully operational within days

However, these same features describe thousands of legitimate small Russian businesses, so this is not conclusive.

## What We Didn't Find

- **No direct IP address overlap** with Baxet or Aeza networks — these are corporate registry documents, not technical infrastructure records
- **No name matches** between Filatov/Berezhinsky and known Aeza/Baxet directors
- **No hosting or telecom activity codes** — both entities have retail/wholesale codes, not IT/hosting

## Recommended Next Steps

1. **SPARK/Kontur lookup**: Search both INNs (231533996303, 232524834996) in Russian corporate databases for other company directorships — a pattern of shell companies would strengthen H4
2. **Address check**: Is the Moscow address (Severnoe Butovo, ul. Polyany 5A, str. 7) a mass-registration address?
3. **Aeza/Baxet director cross-reference**: Check known Aeza Group and Baxet Group principals against Krasnodar Krai registry
4. **Starlink Telecom (ЗАО)**: The older entity (OGRN 1027700046336, registered 2002) was an actual telecom company — does it have ASN/infrastructure overlap with Baxet?

## Assessment

**Hypothesis impact**: H4 (foreign data handoff) — **INCONCLUSIVE**. The Krasnodar geographic nexus is interesting but not probative. No direct technical infrastructure links found. These entities may be completely unrelated to the Aeza/Baxet hosting network, or they may be part of a broader shell company ecosystem that supports it. Further OSINT on the named individuals is needed.

---

*Source files: rawdata/Screenshots/Starlink/ (2 PDFs + 2 screenshots)*
*Full structured extraction: scripts/audit_results/russian_starlink_extraction_RUN008.json*
*COC: FSL-RUN008-STARLINK-EXTRACTION in .claude/forensics/audit-log.md*
