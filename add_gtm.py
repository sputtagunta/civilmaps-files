#!/usr/bin/env python3
"""
Add Google Tag Manager code to all HTML files.

This script automatically inserts GTM tracking code into the <head> and <body>
sections of all HTML files in the repository.
"""

import os
import re
from pathlib import Path

# GTM Head code (paste as high as possible in <head>)
GTM_HEAD = '''<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-MHFTDV8M');</script>
<!-- End Google Tag Manager -->
'''

# GTM Body code (paste immediately after <body>)
GTM_BODY = '''<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MHFTDV8M"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
'''

def add_gtm_to_file(file_path):
    """Add GTM code to a single HTML file."""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if GTM is already installed
        if 'GTM-MHFTDV8M' in content:
            print(f"  ⊘ Skipped: {file_path.name} (GTM already installed)")
            return False

        # Add GTM to <head>
        # Insert right after <head> tag
        head_pattern = r'(<head[^>]*>)'
        if re.search(head_pattern, content, re.IGNORECASE):
            content = re.sub(
                head_pattern,
                r'\1\n    ' + GTM_HEAD.replace('\n', '\n    '),
                content,
                count=1,
                flags=re.IGNORECASE
            )
        else:
            print(f"  ✗ Warning: No <head> tag found in {file_path.name}")
            return False

        # Add GTM to <body>
        # Insert right after <body> tag
        body_pattern = r'(<body[^>]*>)'
        if re.search(body_pattern, content, re.IGNORECASE):
            content = re.sub(
                body_pattern,
                r'\1\n    ' + GTM_BODY.replace('\n', '\n    '),
                content,
                count=1,
                flags=re.IGNORECASE
            )
        else:
            print(f"  ✗ Warning: No <body> tag found in {file_path.name}")
            return False

        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✓ Updated: {file_path.name}")
        return True

    except Exception as e:
        print(f"  ✗ Error processing {file_path.name}: {str(e)}")
        return False


def main():
    """Main function to add GTM to all HTML files."""

    base_dir = Path(__file__).parent

    print("=" * 60)
    print("Google Tag Manager Integration")
    print("=" * 60)
    print(f"GTM Container ID: GTM-MHFTDV8M")
    print(f"Base directory: {base_dir}")
    print("-" * 60)

    # Find all HTML files
    html_files = []

    # Root directory HTML files
    html_files.extend(base_dir.glob("*.html"))

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
        result = add_gtm_to_file(html_file)
        if result is True:
            updated += 1
        elif result is False and 'already installed' not in str(html_file):
            if 'Skipped' in str(html_file):
                skipped += 1
            else:
                failed += 1

    # Summary
    print()
    print("-" * 60)
    print("Integration complete!")
    print(f"  ✓ Updated: {updated}")
    print(f"  ⊘ Skipped: {skipped}")
    print(f"  ✗ Failed: {failed}")
    print(f"  Total: {len(html_files)}")
    print()
    print("Next steps:")
    print("  1. Review changes: git diff")
    print("  2. Commit: git add -A && git commit -m 'Add Google Tag Manager'")
    print("  3. Push: git push origin main")
    print("  4. Test: Visit your site and verify GTM is firing")


if __name__ == "__main__":
    main()
