# HTML to PDF Conversion Scripts

This directory contains scripts to convert all HTML files in the `sections/` directory to PDF format.

## Quick Start

### Option 1: Automatic (Recommended)

Run the shell script which will automatically detect and use the best available conversion tool:

```bash
./convert_to_pdf.sh
```

### Option 2: Manual (Choose Your Tool)

#### Using weasyprint (Best quality, preserves styling)

```bash
# Install weasyprint
pip install weasyprint

# Run conversion
python3 convert_sections_to_pdf.py
```

#### Using pyppeteer (Chromium-based, handles JavaScript)

```bash
# Install pyppeteer
pip install pyppeteer

# Run conversion
python3 convert_sections_to_pdf_chromium.py
```

## Output

All PDF files will be saved to: `sections_pdf/`

Each HTML file in `sections/` will be converted to a corresponding PDF:
- `sections/civil-maps-company.html` → `sections_pdf/civil-maps-company.pdf`
- `sections/luminar-technologies.html` → `sections_pdf/luminar-technologies.pdf`
- etc.

## Installation Instructions

### macOS

#### weasyprint (Recommended)
```bash
# Using pip
pip install weasyprint

# Or using Homebrew + pip
brew install python3 cairo pango gdk-pixbuf libffi
pip3 install weasyprint
```

#### pyppeteer
```bash
pip install pyppeteer
```

#### wkhtmltopdf (Fallback)
```bash
brew install wkhtmltopdf
```

### Ubuntu/Debian Linux

#### weasyprint
```bash
sudo apt-get install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
pip3 install weasyprint
```

#### pyppeteer
```bash
sudo apt-get install python3-pip
pip3 install pyppeteer
```

#### wkhtmltopdf
```bash
sudo apt-get install wkhtmltopdf
```

### Windows

#### weasyprint
```bash
pip install weasyprint
```

#### pyppeteer
```bash
pip install pyppeteer
```

## Conversion Features

### weasyprint
- ✅ Excellent CSS support
- ✅ Preserves fonts and styling
- ✅ Good for styled documents
- ✅ Handles custom fonts
- ❌ No JavaScript support

### pyppeteer
- ✅ Full Chrome rendering engine
- ✅ JavaScript support
- ✅ Complex layout support
- ✅ Excellent web font support
- ⚠️ Requires Chromium download (~170MB first run)

### wkhtmltopdf
- ✅ System-level tool
- ✅ No Python dependencies
- ✅ Fast conversion
- ⚠️ Limited CSS3 support
- ❌ Older rendering engine

## Troubleshooting

### "No PDF conversion tool found"
Install one of the tools listed above. weasyprint is recommended for best results.

### "Module not found" error
Make sure you've installed the Python package:
```bash
pip3 install weasyprint
# or
pip3 install pyppeteer
```

### Fonts not rendering correctly
weasyprint requires system fonts. On macOS, Google Fonts should work automatically.
For custom fonts, ensure they're installed at the system level.

### PDF is too large
The generated PDFs include embedded fonts and images. To reduce size:
- Optimize images in HTML before conversion
- Use web-safe fonts instead of custom fonts
- Enable PDF compression (automatic in most tools)

### Chromium download fails (pyppeteer)
First run of pyppeteer downloads Chromium (~170MB). If it fails:
```bash
# Manually install Chromium
pyppeteer-install

# Or use local Chrome
python3 -c "from pyppeteer import launch; launch(executablePath='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')"
```

## Script Details

### convert_to_pdf.sh
- Automatic tool detection
- Tries multiple methods in order
- Provides helpful error messages
- Cross-platform compatible

### convert_sections_to_pdf.py
- Uses weasyprint
- Best for styled documents
- Configurable page size and margins
- Font configuration support

### convert_sections_to_pdf_chromium.py
- Uses pyppeteer (headless Chrome)
- Best for complex layouts
- JavaScript support
- Async conversion for better performance

## Customization

### Changing Page Size

Edit the PDF generation options in the script:

**weasyprint:**
```python
pdf_css = CSS(string='''
    @page {
        size: Letter;  # Change to A4, Legal, etc.
        margin: 1in;
    }
''')
```

**pyppeteer:**
```python
await page.pdf({
    'format': 'Letter',  # Change to A4, Legal, etc.
    'margin': {
        'top': '1in',
        'right': '1in',
        'bottom': '1in',
        'left': '1in'
    }
})
```

### Adjusting Margins

Modify the margin values in the scripts as shown above.

### Custom Styling for PDF

Add custom CSS specifically for PDF output in the scripts.

## Use Cases

### SEC Filing Submission
Convert HTML documentation to PDF for regulatory submissions.

### Court Document Submission
Generate PDF versions of web-based evidence for court filings.

### Archival
Create permanent PDF archives of HTML documentation.

### Printing
Generate printer-friendly PDFs with proper page breaks.

## Output Quality

All converters aim for:
- Letter size (8.5" x 11") pages
- 1 inch margins
- Preserved colors and styling
- Embedded fonts
- Clickable hyperlinks
- Proper page breaks

## License

These scripts are provided as-is for use with the Civil Maps documentation repository.

## Support

For issues with the conversion scripts, check:
1. Tool is properly installed (`pip list` or `which wkhtmltopdf`)
2. Input HTML files exist in `sections/` directory
3. Write permissions for `sections_pdf/` directory
4. System has sufficient disk space for PDFs

---

Last updated: November 11, 2025
