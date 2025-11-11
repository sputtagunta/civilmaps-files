#!/usr/bin/env python3
"""
Replace Google Tag Manager with Google Analytics gtag.js across all HTML files.
"""

import os
import re
from pathlib import Path

# New Google Analytics code
NEW_GTAG = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RXJC476TYC"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-RXJC476TYC');
</script>'''

def replace_gtag_in_file(file_path):
    """Replace GTM code with new gtag in a single HTML file."""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file has GTM code
        if 'GTM-MHFTDV8M' not in content and 'googletagmanager.com' not in content:
            print(f"  ⊘ Skipped: {file_path.name} (No GTM code found)")
            return False

        original_content = content

        # Remove GTM head code (including surrounding whitespace and newlines)
        gtm_head_pattern = r'\s*<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->\s*\n?\s*'
        content = re.sub(gtm_head_pattern, '', content, flags=re.DOTALL)

        # Remove GTM noscript body code (including surrounding whitespace and newlines)
        gtm_body_pattern = r'\s*<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->\s*\n?\s*'
        content = re.sub(gtm_body_pattern, '', content, flags=re.DOTALL)

        # Insert new gtag right after <head> tag
        head_pattern = r'(<head[^>]*>)'
        if re.search(head_pattern, content, re.IGNORECASE):
            content = re.sub(
                head_pattern,
                r'\1\n    ' + NEW_GTAG.replace('\n', '\n    ') + '\n    ',
                content,
                count=1,
                flags=re.IGNORECASE
            )
        else:
            print(f"  ✗ Warning: No <head> tag found in {file_path.name}")
            return False

        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Updated: {file_path.name}")
            return True
        else:
            print(f"  ⊘ No changes: {file_path.name}")
            return False

    except Exception as e:
        print(f"  ✗ Error processing {file_path.name}: {str(e)}")
        return False


def main():
    """Main function to replace gtag in all HTML files."""

    base_dir = Path(__file__).parent

    print("=" * 60)
    print("Google Analytics Migration (GTM → gtag.js)")
    print("=" * 60)
    print(f"New tracking ID: G-RXJC476TYC")
    print(f"Base directory: {base_dir}")
    print("-" * 60)

    # Find all HTML files
    html_files = []

    # Root directory HTML files (exclude google verification file)
    for file in base_dir.glob("*.html"):
        if not file.name.startswith('google'):
            html_files.append(file)

    # Sections directory HTML files
    sections_dir = base_dir / "sections"
    if sections_dir.exists():
        html_files.extend(sections_dir.glob("*.html"))

    if not html_files:
        print("No HTML files found.")
        return

    print(f"Found {len(html_files)} HTML file(s)\n")

    updated = 0
    skipped = 0
    failed = 0

    for html_file in sorted(html_files):
        result = replace_gtag_in_file(html_file)
        if result is True:
            updated += 1
        elif result is False:
            skipped += 1
        else:
            failed += 1

    # Summary
    print()
    print("-" * 60)
    print("Migration complete!")
    print(f"  ✓ Updated: {updated}")
    print(f"  ⊘ Skipped: {skipped}")
    print(f"  ✗ Failed: {failed}")
    print(f"  Total: {len(html_files)}")
    print()
    print("Changes made:")
    print("  - Removed: Google Tag Manager (GTM-MHFTDV8M)")
    print("  - Removed: GTM noscript fallback")
    print("  - Added: Google Analytics gtag.js (G-RXJC476TYC)")
    print()
    print("Next steps:")
    print("  1. Review changes: git diff")
    print("  2. Commit: git add -A && git commit -m 'Replace GTM with Google Analytics gtag.js'")
    print("  3. Push: git push origin main")
    print("  4. Verify: Visit site and check Analytics Real-Time reports")


if __name__ == "__main__":
    main()
