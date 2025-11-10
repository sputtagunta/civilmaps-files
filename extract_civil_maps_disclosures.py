#!/usr/bin/env python3
"""
Extract Civil Maps disclosures from Luminar SEC filings
"""
import os
import re
from pathlib import Path

def clean_html(text):
    """Remove HTML tags and clean up text"""
    # Remove script and style elements
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_context(text, search_term, context_size=1000):
    """Extract context around search term"""
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    matches = []

    for match in pattern.finditer(text):
        start = max(0, match.start() - context_size)
        end = min(len(text), match.end() + context_size)
        context = text[start:end]
        matches.append(context)

    return matches

def search_file(filepath):
    """Search a single file for Civil Maps mentions"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Clean HTML
        cleaned = clean_html(content)

        # Search for Civil Maps or Solfice
        civil_maps_matches = extract_context(cleaned, 'Civil Maps', 2000)
        solfice_matches = extract_context(cleaned, 'Solfice', 2000)

        all_matches = civil_maps_matches + solfice_matches

        if all_matches:
            filename = os.path.basename(filepath)
            # Parse filename for date and form type
            parts = filename.split('_')
            date = parts[0] if len(parts) > 0 else 'Unknown'
            form_type = parts[1] if len(parts) > 1 else 'Unknown'

            return {
                'filename': filename,
                'date': date,
                'form_type': form_type,
                'matches': all_matches
            }
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

    return None

def main():
    sec_filings_dir = Path('/Users/ubuntu/workbench/civilmaps-files/Luminar_SEC_Filings')

    # Files that grep found with Civil Maps mentions
    target_files = [
        '2022-08-09_10-Q_lazr-20220630.htm',
        '2022-11-04_10-Q_lazr-20220930.htm',
        '2023-02-28_10-K_lazr-20221231.htm',
        '2023-05-10_10-Q_lazr-20230331.htm',
        '2023-08-08_10-Q_lazr-20230630.htm',
        '2023-11-09_10-Q_lazr-20230930.htm',
        '2024-02-28_10-K_lazr-20231231.htm',
        '2024-05-10_10-Q_lazr-20240331.htm',
        '2024-08-08_10-Q_lazr-20240630.htm',
        '2024-11-18_10-Q_lazr-20240930.htm',
        '2025-03-28_10-K_lazr-20241231.htm',
        '2025-05-20_10-Q_lazr-20250331.htm',
        '2025-08-13_10-Q_lazr-20250630.htm'
    ]

    results = []

    for filename in target_files:
        filepath = sec_filings_dir / filename
        if filepath.exists():
            print(f"Processing {filename}...")
            result = search_file(filepath)
            if result:
                results.append(result)

    # Print results
    print("\n" + "="*80)
    print("CIVIL MAPS DISCLOSURES IN LUMINAR SEC FILINGS")
    print("="*80 + "\n")

    for result in results:
        print(f"\n{'='*80}")
        print(f"FILE: {result['filename']}")
        print(f"DATE: {result['date']}")
        print(f"FORM TYPE: {result['form_type']}")
        print(f"{'='*80}\n")

        for i, match in enumerate(result['matches'][:3], 1):  # Limit to first 3 matches per file
            print(f"DISCLOSURE #{i}:")
            print("-" * 80)
            # Clean up the match text
            cleaned_match = ' '.join(match.split())
            # Limit length
            if len(cleaned_match) > 1500:
                cleaned_match = cleaned_match[:1500] + "..."
            print(cleaned_match)
            print("\n")

if __name__ == '__main__':
    main()
