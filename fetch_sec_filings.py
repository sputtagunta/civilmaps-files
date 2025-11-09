#!/usr/bin/env python3
"""
Fetch SEC filings for Luminar Technologies (LAZR) from July 2022 to present.
"""

import os
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# SEC EDGAR API settings
SEC_API_BASE = "https://data.sec.gov"
COMPANY_TICKERS_URL = f"{SEC_API_BASE}/submissions/CIK0001758057.json"  # Luminar's CIK
HEADERS = {
    "User-Agent": "Civil Maps Repository research@civilmaps.com"
}

def get_luminar_filings():
    """Fetch Luminar's filing history from SEC EDGAR."""
    print("Fetching Luminar Technologies (LAZR) filings from SEC EDGAR...")

    response = requests.get(COMPANY_TICKERS_URL, headers=HEADERS)
    response.raise_for_status()

    data = response.json()
    return data

def filter_filings_by_date(filings_data, start_date="2022-07-01"):
    """Filter filings from July 2022 onwards."""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")

    recent_filings = filings_data.get("filings", {}).get("recent", {})

    if not recent_filings:
        print("No recent filings found")
        return []

    filtered = []

    # Get all arrays
    accession_numbers = recent_filings.get("accessionNumber", [])
    filing_dates = recent_filings.get("filingDate", [])
    forms = recent_filings.get("form", [])
    primary_docs = recent_filings.get("primaryDocument", [])

    for i in range(len(accession_numbers)):
        filing_date_str = filing_dates[i]
        filing_date = datetime.strptime(filing_date_str, "%Y-%m-%d")

        if filing_date >= start_dt:
            filtered.append({
                "accessionNumber": accession_numbers[i],
                "filingDate": filing_date_str,
                "form": forms[i],
                "primaryDocument": primary_docs[i]
            })

    return filtered

def download_filing(filing, output_dir):
    """Download a single SEC filing."""
    accession = filing["accessionNumber"].replace("-", "")
    primary_doc = filing["primaryDocument"]
    form_type = filing["form"]
    filing_date = filing["filingDate"]

    # Construct URL
    url = f"https://www.sec.gov/Archives/edgar/data/1758057/{accession}/{primary_doc}"

    # Create filename
    safe_form = form_type.replace("/", "-")
    filename = f"{filing_date}_{safe_form}_{primary_doc}"
    filepath = output_dir / filename

    print(f"Downloading: {form_type} from {filing_date}...")

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"  ✓ Saved to {filename}")
        return True
    except Exception as e:
        print(f"  ✗ Error downloading {filename}: {e}")
        return False

def main():
    output_dir = Path(__file__).parent / "Luminar_SEC_Filings"
    output_dir.mkdir(exist_ok=True)

    print(f"Output directory: {output_dir}")
    print()

    # Fetch filings data
    try:
        filings_data = get_luminar_filings()
    except Exception as e:
        print(f"Error fetching filings data: {e}")
        return

    # Filter filings from July 2022 onwards
    filtered_filings = filter_filings_by_date(filings_data, "2022-07-01")

    print(f"Found {len(filtered_filings)} filings from July 2022 to present")
    print()

    # Save metadata
    metadata = {
        "company": "Luminar Technologies Inc.",
        "ticker": "LAZR",
        "cik": "0001758057",
        "start_date": "2022-07-01",
        "fetch_date": datetime.now().strftime("%Y-%m-%d"),
        "total_filings": len(filtered_filings),
        "filings": filtered_filings
    }

    metadata_file = output_dir / "filings_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved metadata to {metadata_file}")
    print()

    # Download each filing
    success_count = 0
    for i, filing in enumerate(filtered_filings, 1):
        print(f"[{i}/{len(filtered_filings)}]", end=" ")
        if download_filing(filing, output_dir):
            success_count += 1

        # Rate limiting - SEC requests to be polite
        time.sleep(0.2)

    print()
    print(f"Download complete: {success_count}/{len(filtered_filings)} files downloaded successfully")

    # Create README
    readme_content = f"""# Luminar Technologies SEC Filings

This folder contains SEC filings for Luminar Technologies Inc. (NASDAQ: LAZR) from July 2022 to present.

## Company Information
- **Company Name**: Luminar Technologies Inc.
- **Ticker Symbol**: LAZR
- **CIK**: 0001758057
- **Filing Period**: July 2022 - {datetime.now().strftime("%B %Y")}

## Filings Count
Total filings: {len(filtered_filings)}

## Source
All documents are public filings obtained from the SEC EDGAR database:
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001758057

## File Naming Convention
Files are named: `YYYY-MM-DD_FORM-TYPE_original-filename.ext`

## Metadata
See `filings_metadata.json` for complete filing details including accession numbers and form types.
"""

    readme_file = output_dir / "README.md"
    with open(readme_file, 'w') as f:
        f.write(readme_content)

    print(f"Created README: {readme_file}")

if __name__ == '__main__':
    main()
