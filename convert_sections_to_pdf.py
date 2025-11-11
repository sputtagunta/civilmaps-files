#!/usr/bin/env python3
"""
Convert HTML files in sections/ directory to PDF format.

This script uses weasyprint to convert HTML files to PDF while preserving
styling, fonts, and layout. Each HTML file in the sections/ directory will
be converted to a corresponding PDF file.

Requirements:
    pip install weasyprint

Usage:
    python convert_sections_to_pdf.py
"""

import os
import sys
from pathlib import Path

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError:
    print("Error: weasyprint is not installed.")
    print("Please install it with: pip install weasyprint")
    sys.exit(1)


def convert_html_to_pdf(html_path, pdf_path):
    """
    Convert a single HTML file to PDF.

    Args:
        html_path: Path to input HTML file
        pdf_path: Path to output PDF file

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Converting: {html_path.name} -> {pdf_path.name}")

        # Configure fonts for better rendering
        font_config = FontConfiguration()

        # Load HTML and convert to PDF
        html = HTML(filename=str(html_path))

        # Optional: Add custom CSS for PDF output
        pdf_css = CSS(string='''
            @page {
                size: Letter landscape;
                margin: 1in;
            }
            body {
                font-size: 11pt;
            }
        ''', font_config=font_config)

        # Generate PDF
        html.write_pdf(
            str(pdf_path),
            stylesheets=[pdf_css],
            font_config=font_config
        )

        print(f"  ✓ Success: {pdf_path.name} ({pdf_path.stat().st_size // 1024} KB)")
        return True

    except Exception as e:
        print(f"  ✗ Error converting {html_path.name}: {str(e)}")
        return False


def main():
    """Main function to convert all HTML files in sections/ to PDF."""

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
        if convert_html_to_pdf(html_file, pdf_file):
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


if __name__ == "__main__":
    main()
