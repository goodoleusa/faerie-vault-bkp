---
arch_id: ARCH-003
title: "Four-Bulkheads — Defense-in-Depth Cyber Stack for Forensic AI Systems"
status: canonical
created: 2026-05-23
authors: [goodoleusa, claude-opus-4-7]
mission_id: enterprise.patent.foundation
charter: enterprise-patent-foundation (Claim 8)
related_arch: [ARCH-001-STIGMERGIC-SPAWN-PROTOCOL, ARCH-002-LIFECYCLE-HOOKS-MATRIX]
related_skills: [four-bulkheads, four-shields, shape-registry, script-quarantine]
related_publications:
  - "FOR-SKEPTICS-zero-confabulation.md (Terry 2026 — forensic integrity measurement)"
  - "FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR.md (forensic chain v2)"
  - "STIGMERGY-FOR-AGENT-TEAMS.md (Terry 2026 — coordination substrate)"
  - "POTEMKIN-FAERIE-FIELD-REPORT.md (appearance-vs-reality)"
  - "SHAPE-REGISTRY-EVOLUTION-FIELD-REPORT.md (shape registry)"
tags: [architecture, cyber-defense, defense-in-depth, prompt-injection, forensic-integrity, bulkhead, court-discovery, reproducibility]
---

# 🌊 ARCH-003 — Four-Bulkheads: Defense-in-Depth Cyber Stack for Forensic AI Systems

> **What this doc is:** the canonical architecture document for swarmy's
> cyber-defense posture protecting the forensic record against adversarial
> input. Sister doctrine to ARCH-002 (lifecycle × hooks) and four-shields
> (discipline enforcement).
>
> **Why this exists:** the forensic record's value — reproducibility +
> court-discovery readiness — depends entirely on the integrity of every
> input that reaches it. Without defense-in-depth at the cyber layer,
> claims about that integrity are aspirational. With it, they are
> verifiable.

## The compartmentalization metaphor

Watertight bulkheads on a ship are independently-rated compartments that
prevent a single hull breach from sinking the vessel [1, 2]. The same
principle, applied to cyber defense, is the modern "defense in depth"
posture [3, 4]:

```
🏰 BULKHEAD 1: PERIMETER       — containerize internet access; egress allowlist
🧹 BULKHEAD 2: PURIFICATION    — sanitize inputs + outputs at the boundary
🩺 BULKHEAD 3: DETECTION       — real-time scanning + chain-integrity validation
🪞 BULKHEAD 4: QUARANTINE      — contain suspicious content; rollback; reputation
```

Each bulkhead is independently breachable. A breach at one is NOT the loss
of the forensic record — the next bulkhead holds. Together they make
adversarial input mathematically unable to reach `forensics/coc.jsonl`
without breaching all 4.

This complements four-shields (which protects against agent
discipline failure) by protecting against adversarial INPUT [5]. The
forensic chain v2 architecture [6, 7] provides the substrate that
four-bulkheads defends.

## Threat model

The forensic record is the system's load-bearing claim. Adversaries with
ability to inject content into the agent's input stream can target:

- **Prompt injection** — adversarial text in fetched content hijacks the
  agent's reasoning [8, 9]
- **Data poisoning** — malformed schemas/values that corrupt downstream
  computation [10, 11]
- **Source contamination** — repeated bad inputs from a source that lowers
  detection threshold over time [12]
- **Exfiltration** — agent tricked into writing secrets back into the
  forensic record [13]
- **Server-Side Request Forgery (SSRF)** — agent tricked into fetching
  internal-only resources or cloud metadata [14]
- **Confabulation by adversarial framing** — content engineered to look
  like authority but encode disinformation [15]

four-bulkheads is the architecture that defends against all of these
during agent internet access.

## The four bulkheads, in order

### 🏰 Bulkhead 1: PERIMETER — Containerized Internet Access

**Mechanism (cheapest layer, runs pre-execution):**
- Network namespace isolation per OH runtime container [16]
- Egress allowlist — agent's WebFetch/WebSearch can only resolve to
  domains on an explicit allowlist (e.g., GitHub, USPTO, NIST, IETF, official
  docs sites)
- Restricted DNS — DNS resolves only to allowlisted domains; everything
  else returns NXDOMAIN
- Egress audit logging — every WebFetch/WebSearch call writes a
  `network-egress` entry to `forensics/` with target URL + timestamp +
  agent_id

**Stops:** malicious URLs, unknown external APIs, exfiltration to
attacker-controlled domains, SSRF targets (cloud metadata, internal services)
[14, 17].

**Sample hook:** `.openhands/hooks/0x_hook-egress-allowlist.py`
(PreToolUse on WebFetch/WebSearch).

### 🧹 Bulkhead 2: PURIFICATION — Bidirectional Sanitization

**Ingress (content into agent):**
- Prompt-injection payload stripping per OWASP LLM01 patterns [8]
- HTML/Markdown sanitization (strip hidden text per the white-on-white
  attack pattern [18], CSS-rendered content, hidden inputs, embedded scripts)
- Encoding normalization — NFC unicode normalization per UAX #15 [19],
  strip BOM, reject mixed encodings
- Schema validation — if expected content type is JSON/YAML/CSV, validate
  before passing to agent
- Length caps to avoid context-flooding [20]

**Egress (agent writes to forensics):**
- Schema enforcement against `forensics/schemas/shape/` [7]
- Secret-leak detection (API key patterns, private key headers, password
  fields per common-credentials patterns [21])
- Sanitize agent-generated text destined for forensic record
- No-canonical-write rule — agents can only write to
  `forensics/ephemeral/`; promotion is hook-driven [ARCH-002]

**Stops:** prompt-injection payloads reaching agent reasoning,
schema-violating data poisoning, secret exfiltration, hidden-text attacks.

**Sample hooks:**
- `.openhands/hooks/2x_hook-input-sanitizer.py` (PostToolUse on WebFetch)
- `.openhands/hooks/2x_hook-output-sanitizer.py` (PreToolUse on Write/Edit
  to `forensics/`)

### 🩺 Bulkhead 3: DETECTION — Real-Time Poisoning Scanning

**Mechanism (runs continuously):**
- Anomaly detection on shape registry — if a shape's count moves outside
  its noise threshold AND the move correlates with recent ingress content,
  flag for review [SHAPE-REGISTRY-EVOLUTION]
- Hash chain validation on every COC append — verify `prev_entry_hash`
  continuity; any break = STOP write + alert [6, 22]
- Source reputation tracking — sources accumulate a reputation score;
  bad-content sources get downgraded; below-threshold sources rejected at
  Bulkhead 1
- Semantic anomaly detection — manifests that don't match expected
  mission_id grammar, completion_choice schema, or cluster_prefix parity
  get flagged (a manifest that LOOKS valid but content-poisons mission_id
  is a high-leverage attack)
- Cross-agent corroboration — when 2+ agents process the same source,
  their outputs are compared; divergence flags potential prompt-injection
  [MONKEYBRANCHING-2-AGENT-FIELD-REPORT]
- Honeypot fields in schemas — canary fields that should never appear in
  legitimate output; their presence indicates input poisoning [23]

**Stops:** sophisticated prompt-injection that survives sanitization,
slow-drift poisoning, cross-source contamination, stealth attacks
violating semantic invariants.

**Sample hooks:**
- `.openhands/hooks/3x_hook-poisoning-detector.py` (PostToolUse)
- `scripts/daily-cron/anomaly-scan.py` (periodic)

### 🪞 Bulkhead 4: QUARANTINE — Containment + Recovery

**Mechanism (last-resort containment + reputation feedback loop):**
- Quarantine zone — `scripts/quarantine/` (existing) extended with
  `quarantine/incoming/{YYYY-MM-DD}/`
- Pre-canonical staging — Bulkheads 1-3 mark content with confidence;
  below threshold → quarantine; above threshold → `forensics/ephemeral/`
- Git-based rollback — every flagged-but-promoted write has a rollback
  commit prepared; Bulkhead 3 detection triggers atomic rollback
- Reputation downgrade — sources accumulate negative reputation; over
  time, threshold drift makes future content harder to promote
- Forensic-replay sandbox — quarantined content can be re-run in a clean
  isolated sandbox for forensic analysis
- Quarantine COC — quarantine actions write to a separate chain
  (`forensics/quarantine-coc.jsonl`) so main chain stays clean
- Operator review queue — quarantined items appear in a review interface

**Stops:** poisoned content from spreading, false-positive damage, loss of
forensic evidence about the attack, slow attack escalation.

## Court-discovery + reproducibility implications

The forensic record is admissible-in-court only if its integrity is
defensible [22, 24]. four-bulkheads provides the defensibility:

- **Reproducibility** — every input that reached the forensic record passed
  all 4 bulkheads; the bulkhead logs are themselves forensic;
  deterministic replay possible from the bulkheads' acceptance decisions
  [FOR-SKEPTICS-zero-confabulation]
- **Chain-of-custody integrity** — Bulkhead 3's hash chain validation
  means any break in the COC is detected immediately, not after-the-fact
  [FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR]
- **Adversarial-input defense** — Bulkhead 1's egress allowlist means the
  witness (the agent) was only exposed to allowlisted information;
  cross-examination cannot impeach "what about that URL it saw"
- **Tamper evidence** — Bulkhead 4's quarantine + rollback leaves a
  forensic trail in the quarantine chain
- **Source provenance** — Bulkhead 3's reputation tracking means every
  assertion in the forensic record traces back to source URLs with known
  reputation history [POTEMKIN-FAERIE — appearance-vs-reality framing]

When asked in discovery "how do you know this forensic record wasn't
poisoned", the answer is: "show me the 4-bulkhead logs for that time
window; they enumerate every input that reached the agent + every output
that reached the forensic record."

## Why this is novel (patent claim 8 in the enterprise-patent-foundation expedition)

Each individual layer has prior art [3, 4, 8, 22]. The novelty lies in
the COMBINATION + the explicit forensic-integrity framing:

> Four-Bulkhead Cyber Defense Architecture for Forensically-Sound AI
> Systems — combining containerized network isolation, bidirectional
> content sanitization, real-time poisoning detection, and quarantine-
> based recovery to maintain a forensic record robust against adversarial
> prompt injection during agent internet access, where the bulkhead logs
> themselves form a defensible chain of custody supporting both
> reproducibility and court-discovery readiness claims.

Captured as Claim 8 in the `enterprise-patent-foundation` charter.

## Mapping to existing swarmy infrastructure

| Bulkhead | Existing | Gap |
|---|---|---|
| 🏰 Perimeter | None at egress layer | Need `.openhands/hooks/0x_hook-egress-allowlist.py` |
| 🧹 Purification | Partial — schemas at `forensics/schemas/shape/` provide structural validation | Need input sanitizer + secret-leak detector + prompt-injection pattern strip |
| 🩺 Detection | Partial — shape-registry mechanical verdict [SHAPE-REGISTRY-EVOLUTION] + COC hash chain [FORENSIC-COC-V2] | Need cross-agent corroboration + source reputation aggregator |
| 🪞 Quarantine | Partial — `scripts/quarantine/` exists + `script-quarantine` skill exists | Need ingress quarantine flow + quarantine-coc.jsonl + replay sandbox |

## Discovered work (to be wired into tactical charters)

1. (S) Author `.openhands/hooks/0x_hook-egress-allowlist.py` + an
   allowlist file at `.openhands/egress-allowlist.txt`
2. (S) Author `.openhands/hooks/2x_hook-input-sanitizer.py` + a
   prompt-injection pattern registry
3. (S) Author `.openhands/hooks/2x_hook-output-sanitizer.py` + a
   secret-leak detector
4. (S) Author `.openhands/hooks/3x_hook-poisoning-detector.py` +
   `scripts/daily-cron/anomaly-scan.py`
5. (S) Extend `scripts/quarantine/` with `incoming/{date}/` flow + a
   `forensics/quarantine-coc.jsonl` separate chain
6. (E) Source reputation aggregator at
   `scripts/source-reputation-aggregator.py` — feeds Bulkhead 1's
   allowlist decisions
7. (E) Forensic-replay sandbox at `scripts/quarantine/replay_sandbox.py`
8. (N) Schema-canary registry — `forensics/schemas/canary-fields.json`
   listing per-schema honeypot fields that should never appear in
   legitimate output
9. (W) Audit cron that confirms each bulkhead is firing correctly (no
   silent failures)
10. (S) Integrate into `enterprise-patent-foundation` polished
    deliverables (Claim 8 + corresponding Detailed Description sub-section)

## Integration target: SecureClaw

Operator stated 2026-05-23 that swarmy is already integrating **SecureClaw**.
This section records the integration intent + the per-bulkhead mapping
table; specific bulkhead-layer assignments await operator-provided context
on the SecureClaw capabilities being adopted.

| If SecureClaw provides … | Then it slots into … |
|---|---|
| Network filtering / egress policy / WAF | 🏰 Bulkhead 1 (Perimeter) |
| Content scanning / DLP / payload sanitization | 🧹 Bulkhead 2 (Purification) |
| Threat intel / behavioral anomaly / SIEM-style alerting | 🩺 Bulkhead 3 (Detection) |
| Incident response / quarantine workflows | 🪞 Bulkhead 4 (Quarantine) |

**Patent-novelty implication (Claim 8):** the four-bulkheads claim is a
COMBINATION claim. If SecureClaw provides one layer as a third-party
product, the combination is still novel, but the Detailed Description in
the provisional must attribute SecureClaw's contribution accurately to
avoid claiming prior art. Patent attorney review of this attribution is
explicit follow-up in the `enterprise-patent-foundation` charter.

**Operator follow-up required to complete this section:**

1. Brief description of what SecureClaw provides
2. Which bulkhead(s) it overlays
3. Integration surface (API, hosted service, on-prem agent)
4. Auth pattern (vendor-held vs customer-held, relative to the
   zero-knowledge architecture in the patent expedition)
5. Reference URL for citation

## Vancouver Bibliography

**Internal vault publications (load-bearing prior art for the swarmy-specific framing):**

[FOR-SKEPTICS-zero-confabulation] Terry J. For Skeptics: How Faerie's 0%
Confabulation Rate and 100% Manifest Truthfulness Are Actually Measured
[Internet]. Faerie Vault Publications; 2026 May 19 [cited 2026 May 23].
Available from: `$VAULT/80-Publications/FOR-SKEPTICS-zero-confabulation.md`

[FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR] Forensic COC v2 — Merkle Rollups +
Sigstore Rekor Anchoring [Internet]. Faerie Vault Publications; 2026 [cited
2026 May 23]. Available from: `$VAULT/80-Publications/FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR.md`

[FORENSIC-COC-V2-PHASE-1-KICKOFF] Forensic COC v2 Phase 1 Kickoff
[Internet]. Faerie Vault Publications; 2026 [cited 2026 May 23]. Available
from: `$VAULT/80-Publications/FORENSIC-COC-V2-PHASE-1-KICKOFF.md`

[STIGMERGY-FOR-AGENT-TEAMS] Terry J. Stigmergy as a Coordination Substrate
for AI Agent Teams [Internet]. Faerie Vault Publications; 2026 May 19 [cited
2026 May 23]. Available from: `$VAULT/80-Publications/STIGMERGY-FOR-AGENT-TEAMS.md`

[POTEMKIN-FAERIE] Potemkin Faerie — Field Report on an Ad-Hoc Stigmergic
System [Internet]. Faerie Vault Publications; 2026 May 19 [cited 2026 May
23]. Available from: `$VAULT/80-Publications/POTEMKIN-FAERIE-FIELD-REPORT.md`

[SHAPE-REGISTRY-EVOLUTION] Shape Registry Evolution — Field Report
[Internet]. Faerie Vault Publications; 2026 [cited 2026 May 23]. Available
from: `$VAULT/80-Publications/SHAPE-REGISTRY-EVOLUTION-FIELD-REPORT.md`

[MONKEYBRANCHING-2-AGENT-FIELD-REPORT] Monkeybranching 2-Agent Field
Report [Internet]. Faerie Vault Publications; 2026 [cited 2026 May 23].
Available from: `$VAULT/80-Publications/MONKEYBRANCHING-2-AGENT-FIELD-REPORT.md`

[ORCHESTRATOR-OBSERVATIONS] Orchestrator Observations [Internet]. Faerie
Vault Publications; 2026 [cited 2026 May 23]. Available from:
`$VAULT/80-Publications/ORCHESTRATOR-OBSERVATIONS.md`

[ARCH-002] ARCH-002 Swarmy OH Lifecycle × Hooks — Strategic Boundary
Matrix [Internet]. Faerie Vault Architecture; 2026 May 23 [cited 2026 May
23]. Available from: `$VAULT/00-SHARED/Architecture/ARCH-002-LIFECYCLE-HOOKS-MATRIX.md`

**External authoritative sources (each URL needs ⚠️ verification by the polished-deliverables agent's URL-check pass):**

1. ⚠️ International Maritime Organization. International Convention for
   the Safety of Life at Sea (SOLAS), Chapter II-1 — Construction,
   Subdivision and Stability (watertight bulkhead requirements) [Internet].
   IMO; 1974 [as amended; cited 2026 May 23]. Available from:
   `https://www.imo.org/en/About/Conventions/Pages/International-Convention-for-the-Safety-of-Life-at-Sea-(SOLAS),-1974.aspx`

2. ⚠️ Lloyd's Register. Watertight Subdivision Requirements for SOLAS
   Vessels [Internet]. Lloyd's; 2024 [cited 2026 May 23]. Available from:
   `https://www.lr.org/`

3. ⚠️ Cohen F. A Note on the Role of Deception in Information Protection
   (origin of "defense in depth" in cyber context). Communications of the
   ACM. 1998;41(2):91-102. Available from: `https://dl.acm.org/`

4. ⚠️ National Institute of Standards and Technology. NIST Special
   Publication 800-53 Rev. 5 — Security and Privacy Controls for
   Information Systems and Organizations [Internet]. NIST; 2020 Sep
   [cited 2026 May 23]. Available from:
   `https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final`

5. ⚠️ NIST. AI Risk Management Framework (AI RMF 1.0) [Internet]. NIST;
   2023 Jan [cited 2026 May 23]. Available from:
   `https://www.nist.gov/itl/ai-risk-management-framework`

6. — internal [FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR] (see above)

7. — internal `forensics/schemas/shape/*.schema.json` (this repo)

8. ⚠️ OWASP. OWASP Top 10 for LLM Applications 2025 — LLM01: Prompt
   Injection [Internet]. OWASP; 2025 [cited 2026 May 23]. Available
   from: `https://genai.owasp.org/llmrisk/llm01-prompt-injection/`

9. ⚠️ Greshake K, Abdelnabi S, Mishra S, Endres C, Holz T, Fritz M. Not
   What You've Signed Up For: Compromising Real-World LLM-Integrated
   Applications with Indirect Prompt Injection. arXiv preprint
   arXiv:2302.12173 [Internet]. 2023 Feb [cited 2026 May 23]. Available
   from: `https://arxiv.org/abs/2302.12173`

10. ⚠️ MITRE. ATLAS — Adversarial Threat Landscape for Artificial-
    Intelligence Systems [Internet]. MITRE; 2024 [cited 2026 May 23].
    Available from: `https://atlas.mitre.org/`

11. ⚠️ Carlini N et al. Poisoning Web-Scale Training Datasets is
    Practical. arXiv preprint arXiv:2302.10149 [Internet]. 2023 Feb
    [cited 2026 May 23]. Available from:
    `https://arxiv.org/abs/2302.10149`

12. ⚠️ Common Weakness Enumeration. CWE-1395: Dependency on Vulnerable
    Third-Party Component [Internet]. MITRE; 2024 [cited 2026 May 23].
    Available from: `https://cwe.mitre.org/`

13. ⚠️ OWASP. OWASP Top 10 for LLM — LLM06: Sensitive Information
    Disclosure [Internet]. OWASP; 2025 [cited 2026 May 23]. Available
    from: `https://genai.owasp.org/llmrisk/llm06-sensitive-information-disclosure/`

14. ⚠️ Common Weakness Enumeration. CWE-918: Server-Side Request Forgery
    (SSRF) [Internet]. MITRE; 2024 [cited 2026 May 23]. Available from:
    `https://cwe.mitre.org/data/definitions/918.html`

15. — internal [POTEMKIN-FAERIE] (see above)

16. ⚠️ Linux Kernel Documentation. namespaces(7) — overview of Linux
    namespaces [Internet]. The Linux Kernel Archives; 2024 [cited 2026
    May 23]. Available from:
    `https://man7.org/linux/man-pages/man7/namespaces.7.html`

17. ⚠️ Center for Internet Security. CIS Docker Benchmark [Internet].
    CIS; 2024 [cited 2026 May 23]. Available from:
    `https://www.cisecurity.org/benchmark/docker`

18. ⚠️ Hidden-Text and CSS-Rendering Attack Patterns — Common technique
    catalog. OWASP Web Security Testing Guide [Internet]. OWASP; 2024
    [cited 2026 May 23]. Available from: `https://owasp.org/www-project-web-security-testing-guide/`

19. ⚠️ Unicode Consortium. Unicode Standard Annex #15 — Unicode
    Normalization Forms [Internet]. Unicode Consortium; 2023 [cited 2026
    May 23]. Available from: `https://www.unicode.org/reports/tr15/`

20. ⚠️ OWASP. OWASP Top 10 for LLM — LLM04: Model Denial of Service
    [Internet]. OWASP; 2025 [cited 2026 May 23]. Available from:
    `https://genai.owasp.org/llmrisk/llm04-model-denial-of-service/`

21. ⚠️ TruffleHog (Detection Patterns for Leaked Credentials)
    [Internet]. Truffle Security; 2024 [cited 2026 May 23]. Available
    from: `https://github.com/trufflesecurity/trufflehog`

22. ⚠️ Federal Rules of Evidence, Rule 901 — Authenticating or
    Identifying Evidence [Internet]. United States Courts; 2024 [cited
    2026 May 23]. Available from:
    `https://www.law.cornell.edu/rules/fre/rule_901`

23. ⚠️ Spitzner L. The Honeynet Project — Know Your Enemy Whitepapers
    [Internet]. Honeynet Project; 2024 [cited 2026 May 23]. Available
    from: `https://www.honeynet.org/`

24. ⚠️ Federal Rules of Evidence, Rule 902(14) — Self-Authenticating
    Records from a Process or System [Internet]. United States Courts;
    2024 [cited 2026 May 23]. Available from:
    `https://www.law.cornell.edu/rules/fre/rule_902`

**Verification note:** External citations marked ⚠️ need WebFetch
verification by the `enterprise-patent-foundation` polished-deliverables
agent before being printed in any USPTO submission or ELA recital. The
verification pattern mirrors that doc's BIBLIOGRAPHY-VERIFIED.md
methodology.

---

**Last updated:** 2026-05-23 by goodoleusa + claude-opus-4-7 during the
precious-faerie-salvage / swarmy-on-OH-bootstrap / enterprise-patent-
foundation expedition sessions.

**Citation:** Use as `[ARCH-003]` in inline references or frontmatter.

**Verbatim mirror:** None yet — appending to `deploy/README.md` is OPTIONAL
(unlike ARCH-002 which has operational relevance for deploy operators,
ARCH-003 is more strategic doctrine + patent material; operator decides
whether to mirror).
