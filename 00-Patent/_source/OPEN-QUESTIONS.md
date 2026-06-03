# OPEN QUESTIONS
## Operator Must Answer Before USPTO Filing or Attorney Engagement

**Status:** Compiled from `charter.json` open_questions + discoveries during the polished-deliverables research pass.
**Date compiled:** 2026-05-23
**Agent:** research-analyst (expedition-w1)

---

### CRITICAL — Required Before USPTO Filing

These questions block the provisional filing. The provisional cannot be filed until they are answered.

**OQ-001: Co-inventor name and identity**
- What is the co-inventor's full legal name (as it will appear on the USPTO cover sheet)?
- What is their current mailing address (required on Form SB/16)?
- What is their citizenship / country of residence (required for USPTO filing)?
- Are there any ownership agreements between the two inventors regarding the patent rights (e.g., a co-inventor agreement specifying ownership split)?

**OQ-002: Lead inventor (first named inventor) information**
- Full legal name as it will appear on the USPTO cover sheet
- Current mailing address
- Citizenship / country of residence

**OQ-003: Entity status for fee calculation**
- Do BOTH inventors qualify for micro entity status?
  - Micro entity gross income qualification: as of 2025, maximum qualifying gross income is $251,190/year (confirmed from USPTO fee schedule search)
  - Micro entity filing limit: no more than 4 previous patent applications filed as inventor (provisional applications do not count toward this limit)
  - If either inventor does not qualify, the filing fee tier drops to small entity ($130) or regular ($325)
- Recommendation: confirm micro entity qualification with a patent attorney before filing

**OQ-004: Provisional patent title**
- The draft title in this specification is: "Autonomous Multi-Agent Orchestration System with Hierarchical Memory Promotion, Stigmergic Filesystem Coordination, Four-Layer Enforcement Stack, and Mechanical Quality Classification"
- USPTO recommends titles that are 2–7 words but this is a recommendation, not a requirement for provisionals
- Operator should confirm or adjust this title

---

### HIGH PRIORITY — Required Before ELA Execution

These questions block the ELA from being signed.

**OQ-005: Company entity legal name and state of incorporation**
- What is the full legal name of the company entity that will sign as Licensor?
- What state is it (or will it be) incorporated/formed in?
- If the company does not yet exist: the ELA Option A (company as exclusive sublicensee from inventors, then sublicenses to enterprise customer) requires a separate Exclusive License Agreement between the Inventors and the Company entity. The company must exist before this can be executed.

**OQ-006: ELA structure decision (Section 14 of ELA-DRAFT.md)**
- **Option A (recommended):** Inventors grant exclusive license to Company entity; Company sublicenses to Licensee. Provides liability shield but requires Exclusive License Agreement between Inventors and Company.
- **Option B (fallback):** Inventors license directly to Licensee. Simpler but exposes inventors personally.
- Which structure does the operator choose? Attorney should advise on tax and liability implications before selecting.

**OQ-007: First enterprise customer information**
- Customer legal name and state of formation (affects governing law selection and jurisdiction)
- Industry vertical (affects due-diligence affirmation scope and acceptable use provisions)
- Deal size class (affects fee schedule structure — flat fee vs. usage-based vs. revenue share)
- Timeline for contract signature (drives ELA finalization deadline)

**OQ-008: Governing law jurisdiction**
- The ELA and Assignment Agreement both have [STATE — OPEN QUESTION] placeholders.
- Most common choices for software companies: Delaware (company law alignment), California (where many enterprise customers are based), or the operator's home state.
- Attorney should advise based on company formation state and enterprise customer's jurisdiction.

**OQ-009: Dispute resolution mechanism**
- ELA Section 10.2 has a placeholder for arbitration provider (AAA or JAMS) and seat (city/state).
- Attorney should advise on which arbitration forum is appropriate for the deal size and customer type.

---

### MEDIUM PRIORITY — Required Before Non-Provisional Filing or Patent Attorney Engagement

**OQ-010: Patent attorney engagement**
- The provisional establishes the priority date. The 12-month clock to non-provisional conversion begins on the filing date.
- A registered patent attorney must: (a) review and refine the provisional specification; (b) draft formal independent and dependent claims for the non-provisional; (c) advise on claim scope vs. prior art; and (d) handle USPTO prosecution.
- Recommended timeline: engage attorney within 6 months of provisional filing, before the 12-month clock expires.
- Budget note: non-provisional patent prosecution typically costs $8,000–$20,000+ including attorney fees and USPTO fees. Provisional filing itself (DIY, no attorney) costs $65 (micro entity) + Form SB/16 + specification PDF.

**OQ-011: Prior art disclosure**
- Are the inventors aware of any prior art systems that describe similar techniques?
  - Stigmergic agent coordination systems (e.g., swarm intelligence papers, ACO — ant colony optimization systems)?
  - Hierarchical memory systems for AI agents (e.g., MemGPT, Reflexion, generative agents)?
  - Mechanical verdict classification systems in software engineering (e.g., mutation testing frameworks)?
  - Four-layer enforcement stacks in computer security (e.g., defense-in-depth frameworks)?
- Full prior art disclosure is required for USPTO examination. Inventors have a duty to disclose material prior art they are aware of.

**OQ-012: Jurisdiction strategy**
- US-only first (provisional + US non-provisional)?
- PCT international filing (covers 150+ countries, must file within 12 months of provisional)?
- Direct national phase in specific jurisdictions (EU, UK, China, Japan) without PCT?
- PCT route preserves maximum international options but adds significant cost ($5,000–$15,000+ for PCT filing, then national phase fees).
- Attorney should advise based on where the operator expects commercial activity.

---

### MEDIUM PRIORITY — Module Disposition Matrix

**OQ-013: Per-module OSS vs. proprietary disposition**
- The operator selected "core-engine-proprietary-rest-open" strategy.
- A concrete per-module decision matrix is needed to ensure the patent's novel-combination claim covers the IP boundary cleanly.
- Draft matrix (operator must confirm or revise):

| Module / Component | Proposed Disposition | Notes |
|---|---|---|
| `scripts/1a_manifest_writer.py` | Proprietary | Core memory promotion gate |
| `scripts/2d_frontier_scanner_indexed.py` | Proprietary | Core stigmergic coordination |
| `scripts/2a_spawn_pressure.py` | Proprietary | Core spawn formula |
| `scripts/shapes/_shapes_lib.py` | Proprietary | Core mechanical verdict classifier |
| `scripts/3f_membench_probes.py` | Proprietary | Core membench substrate |
| `scripts/3k_membench_scorer.py` | Proprietary | Core evaluation substrate |
| `forensics/schemas/formulas/*.formula.json` | Proprietary | Core formula definitions |
| `_meta/shapes.json` | Proprietary | Core shape registry |
| `.openhands/hooks/9x_hook-*.py` | Proprietary | Core reactive enforcement |
| `GOLD.md`, `NECTAR.md` (format/protocol) | Proprietary | Core memory protocol |
| `.agents/skills/*/SKILL.md` | Open source (OSS) | Community building |
| `.agents/skills/survey/SKILL.md` | Open source (OSS) | Community building |
| `AGENTS.md` (doctrine) | Open source (OSS) | Community building |
| Agent archetypes (NAVIGATOR, MAKER, etc.) | Open source (OSS) | Community building |
| Vault patterns, Obsidian structure | Open source (OSS) | Community building |

**OQ-014: forensic-coc-v2-rekor integration decision**
- The `forensic-coc-v2-rekor` charter covers a Merkle-tree + Sigstore Rekor witnessing architecture for the forensic chain-of-custody.
- Decision needed: (a) fold it into the current provisional as an additional claim area (requires adding Section 7 to the patent spec before filing); or (b) file a separate provisional for that architecture?
- The current provisional spec describes the SHA-256 hash chain (`forensics/coc.jsonl`) but does not claim the Rekor witnessing layer.
- Attorney should advise on whether combining or separating provides stronger protection.

---

### LOWER PRIORITY — For Later Planning

**OQ-015: share.note.sx encrypted note content**
- The operator referenced additional research at `https://share.note.sx/xyjlsmzd#yOf7fYmiC6qLhW4kHDi3uPpst9+YRt2pnEfWJ32FnTo`
- This note uses client-side encryption; the agent could not decrypt it in this session.
- Action: operator opens the URL in a browser, copies the decrypted content, and provides it for the next research pass.
- The decrypted content may contain additional patent claim language, ELA clauses, prior art references, or other material that should be incorporated into the polished deliverables.

**OQ-016: Multi-signature ed25519 notary key strategy**
- The `forensic-coc-v2-rekor` charter cross-references a notary key strategy for the company's overall identity.
- This may affect how the patent's forensic chain-of-custody claims are framed and how the company's IP ownership is established in a legally defensible way.
- No action required for the provisional filing, but should be resolved before the non-provisional.

**OQ-017: Post-assignment IP landscape**
- If the company is acquired or the IP is assigned (triggering the Assignment Agreement), what happens to:
  - Existing enterprise licensees under the ELA?
  - Open-source community users of the OSS modules?
  - Any employees or contractors who contributed to the system after the provisional filing?
- The Assignment Agreement draft (Y.2) transfers "all liabilities" to Assignee, but the scope of "liabilities" relative to existing ELA licensees should be confirmed with an attorney.

---

### NOTES FROM THE RESEARCH PASS

**On the LUMO hallucinated URL (OQ-018):**
- LUMO cited `https://www.uspto.gov/patents/apply/patent-eligibility` as the August 2025 USPTO guidance URL. This URL does not match the confirmed USPTO site structure. The correct resources are:
  - Canonical SME page: `https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility`
  - August 4, 2025 memo PDF: `https://www.uspto.gov/sites/default/files/documents/memo-101-20250804.pdf`
- The hallucinated URL has been corrected in BIBLIOGRAPHY-VERIFIED.md. Any attorney communications should use the corrected URLs.

**On LUMO's micro entity fee claim (OQ-019):**
- LUMO claimed micro entity fees of "$70-$150" and advised to "verify current rates." The verified current rate (from USPTO fee schedule, effective January 19, 2025, last revised May 1, 2026) is $65 for micro entity provisional filing. LUMO's range was slightly off; the current rate is $65.

**On patent numbers cited by LUMO (OQ-020):**
- LUMO cited Apple 7,469,381, Amazon 5,960,411, and Google PageRank as examples of provisional-originated patents.
- These patent numbers are in the public record.
- The "originated from provisional" claim was not independently verified in this session.
- Before citing these in any attorney communication or patent marketing material, verify via https://ppubs.uspto.gov/pubwebapp/ that the provisional origin claim is accurate for each patent.

