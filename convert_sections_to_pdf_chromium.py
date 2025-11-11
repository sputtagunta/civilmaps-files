#!/usr/bin/env python3
"""
Convert HTML files in sections/ directory to PDF format using Chromium/Chrome.

This script uses pyppeteer (headless Chrome) to convert HTML files to PDF,
which provides excellent rendering quality and handles complex CSS/JavaScript.

Requirements:
    pip install pyppeteer

Usage:
    python convert_sections_to_pdf_chromium.py
"""

import asyncio
import os
import sys
from pathlib import Path

try:
    from pyppeteer import launch
except ImportError:
    print("Error: pyppeteer is not installed.")
    print("Please install it with: pip install pyppeteer")
    sys.exit(1)


async def convert_html_to_pdf_async(html_path, pdf_path):
    """
    Convert a single HTML file to PDF using headless Chrome.

    Args:
        html_path: Path to input HTML file
        pdf_path: Path to output PDF file

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Converting: {html_path.name} -> {pdf_path.name}")

        # Launch headless browser
        browser = await launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        page = await browser.newPage()

        # Load HTML file
        file_url = f"file://{html_path.resolve()}"
        await page.goto(file_url, {'waitUntil': 'networkidle0'})

        # Generate PDF with options
        await page.pdf({
            'path': str(pdf_path),
            'format': 'Letter',
            'landscape': True,
            'printBackground': True,
            'margin': {
                'top': '1in',
                'right': '1in',
                'bottom': '1in',
                'left': '1in'
            }
        })

        await browser.close()

        print(f"  ✓ Success: {pdf_path.name} ({pdf_path.stat().st_size // 1024} KB)")
        return True

    except Exception as e:
        print(f"  ✗ Error converting {html_path.name}: {str(e)}")
        return False


async def main_async():
    """Main async function to convert all HTML files in sections/ to PDF."""

    # Get the base directory (where script is located)
    base_dir = Path(__file__).parent.resolve()
    sections_dir = base_dir / "sections"

    # Create output directory for PDFs
    pdf_output_dir = base_dir / "sections_pdf"
    pdf_output_dir.mkdir(exist_ok=True)

    print(f"Base directory: {base_dir}")
    print(f"Sections directory: {sections_dir}")
    print(f"PDF output directory: {pdf_output_dir}")
    print("-" * 60)

    # Check if sections directory exists
    if not sections_dir.exists():
        print(f"Error: Sections directory not found at {sections_dir}")
        sys.exit(1)

    # Find all HTML files in sections directory
    html_files = list(sections_dir.glob("*.html"))

    if not html_files:
        print(f"No HTML files found in {sections_dir}")
        sys.exit(0)

    print(f"Found {len(html_files)} HTML file(s) to convert\n")

    # Convert each HTML file to PDF
    successful = 0
    failed = 0

    for html_file in sorted(html_files):
        # Create corresponding PDF filename
        pdf_file = pdf_output_dir / f"{html_file.stem}.pdf"

        # Convert
        if await convert_html_to_pdf_async(html_file, pdf_file):
            successful += 1
        else:
            failed += 1

        print()  # Blank line between files

    # Summary
    print("-" * 60)
    print(f"Conversion complete!")
    print(f"  ✓ Successful: {successful}")
    print(f"  ✗ Failed: {failed}")
    print(f"  Total: {len(html_files)}")
    print(f"\nPDF files saved to: {pdf_output_dir}")


def main():
    """Wrapper to run async main function."""
    asyncio.get_event_loop().run_until_complete(main_async())


if __name__ == "__main__":
    main()
