#!/bin/bash
#
# Convert all HTML files in sections/ directory to PDF
#
# This script tries multiple conversion methods in order of preference:
# 1. weasyprint (best for styled HTML)
# 2. pyppeteer (headless Chrome, good for complex layouts)
# 3. wkhtmltopdf (fallback if installed on system)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTIONS_DIR="${SCRIPT_DIR}/sections"
PDF_OUTPUT_DIR="${SCRIPT_DIR}/sections_pdf"

echo "================================================================"
echo "HTML to PDF Converter"
echo "================================================================"
echo ""

# Check if sections directory exists
if [ ! -d "$SECTIONS_DIR" ]; then
    echo "Error: sections/ directory not found"
    exit 1
fi

# Count HTML files
HTML_COUNT=$(find "$SECTIONS_DIR" -maxdepth 1 -name "*.html" | wc -l | tr -d ' ')
echo "Found $HTML_COUNT HTML file(s) to convert"
echo ""

# Method 1: Try weasyprint
if python3 -c "import weasyprint" 2>/dev/null; then
    echo "Using weasyprint for conversion..."
    python3 "${SCRIPT_DIR}/convert_sections_to_pdf.py"
    exit 0
fi

# Method 2: Try pyppeteer
if python3 -c "import pyppeteer" 2>/dev/null; then
    echo "Using pyppeteer (Chromium) for conversion..."
    python3 "${SCRIPT_DIR}/convert_sections_to_pdf_chromium.py"
    exit 0
fi

# Method 3: Try wkhtmltopdf (if installed on system)
if command -v wkhtmltopdf &> /dev/null; then
    echo "Using wkhtmltopdf for conversion..."

    # Create output directory
    mkdir -p "$PDF_OUTPUT_DIR"

    # Convert each HTML file
    for html_file in "$SECTIONS_DIR"/*.html; do
        if [ -f "$html_file" ]; then
            filename=$(basename "$html_file" .html)
            pdf_file="${PDF_OUTPUT_DIR}/${filename}.pdf"

            echo "Converting: ${filename}.html -> ${filename}.pdf"
            wkhtmltopdf \
                --enable-local-file-access \
                --print-media-type \
                --margin-top 25mm \
                --margin-right 25mm \
                --margin-bottom 25mm \
                --margin-left 25mm \
                "$html_file" \
                "$pdf_file" 2>/dev/null

            if [ -f "$pdf_file" ]; then
                size=$(du -h "$pdf_file" | cut -f1)
                echo "  ✓ Success: ${filename}.pdf ($size)"
            else
                echo "  ✗ Failed: ${filename}.pdf"
            fi
            echo ""
        fi
    done

    echo "================================================================"
    echo "Conversion complete!"
    echo "PDF files saved to: $PDF_OUTPUT_DIR"
    exit 0
fi

# No conversion tool available
echo "Error: No PDF conversion tool found."
echo ""
echo "Please install one of the following:"
echo ""
echo "  1. weasyprint (recommended):"
echo "     pip install weasyprint"
echo ""
echo "  2. pyppeteer (Chromium-based):"
echo "     pip install pyppeteer"
echo ""
echo "  3. wkhtmltopdf (system package):"
echo "     macOS: brew install wkhtmltopdf"
echo "     Ubuntu: sudo apt-get install wkhtmltopdf"
echo ""
exit 1
