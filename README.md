# Solfice (Civil Maps) Whistleblower Repository

> Public evidence, timelines, and analysis to examine the 2022 sale of Solfice Research, Inc. (d/b/a Civil Maps) assets (“Project Condor”) and related governance, disclosure, and voting issues. This repo is designed for verifiability, not virality.

---

## What this repo is

* A public, append-only archive of documents and structured notes that help the public, investigators, and journalists understand what happened, when, and who approved it.
* A changelog-driven record of exhibits and facts with cryptographic hashes so anyone can independently verify integrity.
* A living index that maps evidence to specific questions: vote math (§271), notice/consent (§228), conflicts (§144), selective disclosure, consideration waterfall, compensation/inducements, and IP/title chain.

## What this repo is **not**

* Not a place to dox, harass, or post personal data.
* Not rumor aggregation. Every claim must tie to a document, a sworn statement, or a verifiable public record.
* Not legal advice.

---

## Repository structure

```
/README.md                 — You are here
/CLAIMS/                   — Each claim in one file: facts, sources, status, open questions
/TIMELINES/                — Chronologies (board actions, consents, money flows, filings)
/EXHIBITS/                 — Primary docs (PDFs) + .sha256 checksums
/BRIEFS/                   — Public court filings and sworn affidavits
/ANALYSIS/                 — Valuation/waterfall models, vote math, scenario trees
/SEC/                      — Tip IDs (redacted), public 8-K/10-Q cites, chronology of contacts
/MEDIA/                    — Press statements, Q&A, fact sheets
/TOOLS/                    — Scripts for hashing, PDF text extraction, and redaction
```

### Key exhibit index (mapped to common questions)

* **Board & Stockholder Consents** → vote authorization, conflicts disclosures, §144 cleansing, §228 process.
* **Omnibus Amendment to Notes** → allocation of consideration, priority vs. common, contingent/holdback mechanics.
* **Release/Severance Agreements** → compensation timing/amounts near the vote/closing; potential inducements.
* **IP Assignment + Plan of Liquidation** → title chain, what actually transferred, dissolution/survival windows.
* **Disclosure Schedules / Waterfall** → who got what, when, and under which conditions.

> Each file in `/EXHIBITS` has a matching `.sha256` and a short “why this matters” note in `/CLAIMS`.

---

## Quick start

1. **Verify integrity**

   ```bash
   shasum -a 256 EXHIBITS/**/* | diff - CHECKSUMS.sha256
   ```
2. **Browse the story**

   * Start with `TIMELINES/00_master.md`.
   * Then read `CLAIMS/*.md`—each links back to exhibits and docket cites.
3. **Replicate the math**

   * Open `ANALYSIS/waterfall.xlsx` or `ANALYSIS/waterfall.ipynb` and rerun the scenarios.
4. **Track changes**

   * Every PR must update the relevant timeline and claim files and include hashes for any new exhibits.

---

## Contribution guide (public-interest safe-harbor)

* **Evidence-first:** Attach or cite a primary source. If you can’t attach it, provide a stable public link and capture a hash of what you saw.
* **Redact responsibly:** Remove SSNs, home addresses, bank numbers, signatures that aren’t already public; keep timestamps, signatory names/titles, and amounts.
* **Provenance note:** For each new file, add a 3-line block at top:

  ```
  Source: <how obtained or public link>
  First seen: YYYY-MM-DD
  Hash (SHA256): <hash>
  ```
* **Neutral verbs, specific nouns:** “Board executed X” > “They secretly did X.” Let documents do the talking.
* **Cross-reference:** Update `TIMELINES` and at least one `CLAIMS` file with links to the new exhibit.

Submit via PR. Use the template in `.github/PULL_REQUEST_TEMPLATE.md`.

---

## Responsible publication policy

* No private medical, financial account numbers, passwords, or minors’ data.
* No doxxing or targeted harassment. Issues/comments violating this will be removed and reported.
* If you’re a current/former employee with constraints, use your counsel and applicable whistleblower protections before contributing.

---

## Verification & reproducibility

* **Hashes:** All PDFs/CSVs carry SHA-256 checksums; releases include a signed `CHECKSUMS.sha256`.
* **Deterministic scripts:** `/TOOLS` contains small, auditable Python/CLI utilities for hashing, diffing, and text extraction.
* **Evidence map:** `CLAIMS/_index.md` shows claim ⇄ exhibit links and confidence levels (High/Med/Low).

---

## Maintainers & contact

* Open an issue with “Fact Check” tag for corrections.
* Secure contact: `keys/maintainers.asc` (PGP).
* Press: see `MEDIA/press_kit.md`.

---

## License

* **Documents & analysis:** CC BY 4.0
* **Code in /TOOLS:** MIT

---

## Why this exists

Markets and courts rely on uniform, material disclosure to all voting holders. Concentrating the primary paperwork, vote math, consideration allocations, and compensation timing in one verifiable place helps everyone—shareholders, regulators, and future founders—see the same record and draw their own conclusions.

> If you mirror this repo, please preserve the directory structure and `CHECKSUMS.sha256` so hashes continue to match.
