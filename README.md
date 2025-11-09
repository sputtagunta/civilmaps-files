# Civil Maps §220 Books & Records Case Repository

> Public archive of court filings and materials from the Delaware Court of Chancery §220 books and records action concerning Solfice Research, Inc. (d/b/a Civil Maps). This repository provides transparent access to case documents, organized chronologically for independent review and verification.

---

## What this repo is

* A public archive of court documents from the Delaware Court of Chancery §220 books and records case
* An organized collection of verified complaint, affidavits, briefs, and correspondence filed in the action
* A resource for stockholders, journalists, and the public to access and review case materials independently
* A chronological record of the progression of the §220 litigation

## What this repo is **not**

* Not a place to dox, harass, or post personal data
* Not rumor aggregation—only court filings and public records are included
* Not legal advice or legal representation
* Not a substitute for official court records available through the Delaware Court of Chancery

---

## Repository structure

```
/README.md                                              — You are here
/220 Case/                                              — Delaware §220 books & records action materials
  /VERIFIED COMPLAINT/                                  — Initial complaint and supporting documents
  /AFFIDAVIT OF SERVICE/                                — Service documents and exhibits A-O
  /ANUJ AFFIDAVIT - STOCKHOLDER STATUS/                 — Stockholder standing affidavit
  /SRAVAN AFFIDAVIT - SUPPORT FOR PLAINTIFF'S ANSWERING BRIEF/  — Supporting affidavit
  /SRAVAN AFFIDAVIT IN SUPPORT OF PLAINTIFF/            — Additional supporting affidavit
  /PLAINTIFF - OPPOSITION BRIEF/                        — Opposition to motion to dismiss
  /PLAINTIFF FIRST OPPOSITION BRIEF/                    — First opposition brief
  /DEFENDANT MOTION TO DISMISS/                         — Defendant's motion and supporting docs
  /DEFENDANT REPLY BRIEF/                               — Defendant's reply brief
  /MEET_AND_CONFER_LETTER/                              — Joint status reports and correspondence
```

### Key document index (organized by folder)

* **VERIFIED COMPLAINT** → Initial §220 demand and basis for books & records inspection
* **AFFIDAVIT OF SERVICE** → Exhibits A-O documenting service and supporting evidence
* **PLAINTIFF AFFIDAVITS** → Stockholder standing and factual support for claims
* **OPPOSITION BRIEFS** → Arguments against defendant's motion to dismiss
* **DEFENDANT BRIEFS** → Motion to dismiss and reply brief with supporting affidavits
* **CORRESPONDENCE** → Meet and confer letters and joint status reports

> Documents are organized chronologically within each folder to track the progression of the §220 action.

---

## Quick start

1. **Review the case progression**

   * Start with `220 Case/VERIFIED COMPLAINT/` to understand the initial §220 demand
   * Review plaintiff and defendant briefs chronologically
   * Check `220 Case/AFFIDAVIT OF SERVICE/` for supporting exhibits A-O

2. **Verify document integrity**

   * Each folder may contain `.sha256` checksums for verification
   * Check file metadata and timestamps for authenticity

3. **Track case developments**

   * New filings will be added to the `220 Case/` folder as they become available
   * Every PR must include the document date and docket information

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
* **Cross-reference:** Place documents in the appropriate `220 Case/` subfolder and update this README if adding new case materials.

Submit via PR. Use the template in `.github/PULL_REQUEST_TEMPLATE.md`.

---

## Responsible publication policy

* No private medical, financial account numbers, passwords, or minors’ data.
* No doxxing or targeted harassment. Issues/comments violating this will be removed and reported.
* If you’re a current/former employee with constraints, use your counsel and applicable whistleblower protections before contributing.

---

## Verification & reproducibility

* **Hashes:** PDFs may carry SHA-256 checksums for verification; consider adding `CHECKSUMS.sha256` to folders.
* **Court dockets:** All documents should reference Delaware Court of Chancery docket numbers for independent verification.
* **Public records:** Case filings can be independently verified through Delaware's public court records system.

---

## Maintainers & contact

* Open an issue with “Fact Check” tag for corrections.
* Secure contact: `keys/maintainers.asc` (PGP).
* Press: see `MEDIA/press_kit.md`.

---

## License

* **Court documents:** Public court records; no copyright claimed on official filings
* **Repository organization & documentation:** CC BY 4.0
* **Any scripts in /TOOLS (if added):** MIT

---

## Why this exists

Delaware §220 provides stockholders a statutory right to inspect books and records when they demonstrate a proper purpose. This repository consolidates court filings, affidavits, and related materials from the ongoing §220 action in a publicly accessible format. By making these documents readily available, shareholders, investigators, journalists, and the public can independently review the arguments, evidence, and progression of the case.

Transparency in corporate governance matters. This repo serves as a centralized, verifiable archive of the legal proceedings seeking access to Civil Maps' books and records.

> If you mirror this repo, please preserve the directory structure and document metadata so the record remains intact.
