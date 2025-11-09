#!/usr/bin/env python3
"""
Extract filing timestamps from PDF documents in the 220 Case folder.
"""

import os
import re
import json
from pathlib import Path

try:
    import pypdf
    PDF_LIBRARY = 'pypdf'
except ImportError:
    try:
        import PyPDF2
        PDF_LIBRARY = 'PyPDF2'
    except ImportError:
        print("Error: No PDF library found. Please install pypdf or PyPDF2")
        print("Run: pip3 install pypdf")
        exit(1)

def extract_first_page_text(pdf_path):
    """Extract text from the first page of a PDF."""
    try:
        if PDF_LIBRARY == 'pypdf':
            reader = pypdf.PdfReader(pdf_path)
            if len(reader.pages) > 0:
                return reader.pages[0].extract_text()
        else:  # PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfFileReader(file)
                if reader.numPages > 0:
                    return reader.getPage(0).extract_text()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None
    return None

def parse_filing_timestamp(text):
    """Parse filing timestamp from PDF text."""
    if not text:
        return None

    # Pattern 1: EFiled: Dec 13 2024 04:19PM EST
    pattern1 = r'EFiled:\s+([A-Za-z]+\s+\d{1,2}\s+\d{4}\s+\d{1,2}:\d{2}[AP]M\s+[A-Z]{3})'
    match = re.search(pattern1, text, re.IGNORECASE)
    if match:
        return match.group(1)

    # Pattern 2: Filed: Month DD, YYYY
    pattern2 = r'Filed:\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})'
    match = re.search(pattern2, text, re.IGNORECASE)
    if match:
        return match.group(1)

    # Pattern 3: Date filed or similar
    pattern3 = r'Date\s+[Ff]iled:\s+([A-Za-z]+\s+\d{1,2},?\s+\d{4})'
    match = re.search(pattern3, text, re.IGNORECASE)
    if match:
        return match.group(1)

    return None

def process_pdfs(base_dir):
    """Process all PDFs and extract timestamps."""
    timeline_data = []
    case_dir = Path(base_dir) / "220 Case"

    if not case_dir.exists():
        print(f"Error: {case_dir} not found")
        return timeline_data

    # Walk through all subdirectories
    for root, dirs, files in os.walk(case_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = Path(root) / file
                relative_path = pdf_path.relative_to(base_dir)

                print(f"Processing: {relative_path}")

                # Extract first page text
                text = extract_first_page_text(pdf_path)

                # Parse timestamp
                timestamp = parse_filing_timestamp(text)

                # Store result
                timeline_data.append({
                    'path': str(relative_path),
                    'filename': file,
                    'folder': Path(root).name,
                    'timestamp': timestamp if timestamp else 'Not found'
                })

                if timestamp:
                    print(f"  Found timestamp: {timestamp}")
                else:
                    print(f"  No timestamp found")

    return timeline_data

def main():
    base_dir = Path(__file__).parent
    print(f"Scanning PDFs in: {base_dir / '220 Case'}")
    print()

    timeline_data = process_pdfs(base_dir)

    # Sort by folder and filename
    timeline_data.sort(key=lambda x: (x['folder'], x['filename']))

    # Save to JSON file
    output_file = base_dir / 'js' / 'timeline.json'
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(timeline_data, f, indent=2)

    print()
    print(f"Extracted timestamps from {len(timeline_data)} PDFs")
    print(f"Results saved to: {output_file}")

    # Create timeline.js
    js_content = f"""// Timeline data for Civil Maps case documents
// Auto-generated from PDF filing timestamps

const TIMELINE_DATA = {json.dumps(timeline_data, indent=2)};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {{
  module.exports = TIMELINE_DATA;
}}
"""

    js_file = base_dir / 'js' / 'timeline.js'
    with open(js_file, 'w') as f:
        f.write(js_content)

    print(f"JavaScript file created: {js_file}")

if __name__ == '__main__':
    main()
