# PDF Redaction Tool

A Python script that permanently redacts (removes) specified terms from PDF files. It strips existing text layers, performs fresh OCR, then redacts terms by replacing them with permanent black boxes that cannot be removed.

## Features

- **Intelligent page detection**: Automatically distinguishes between native digital pages and scanned images
- **Selective OCR**: Only OCRs scanned pages, preserving accuracy of native text
- **Strips text layer from scans**: Ensures clean OCR for scanned content
- **Permanently redacts** all instances of specified terms
- **Black box coverage** that cannot be removed or revealed
- Case-insensitive search across all pages
- Interactive command-line interface
- Saves redacted PDF next to original with `_redacted` suffix

## Requirements

- Python 3.7 or higher
- Tesseract OCR (system package)
- Python libraries: PyMuPDF, pytesseract, Pillow

## Installation

### 1. Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Set up Python environment

Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment:
```bash
source venv/bin/activate
```

2. Run the script:
```bash
python redact_pdf.py
```

3. Follow the prompts:
   - Enter the path to your PDF file
   - Enter terms to redact (one per line)
   - Press Enter twice (two consecutive linefeeds) to finish entering terms
   - The script will process the PDF and save the redacted version

## Example

```
$ python redact_pdf.py
============================================================
PDF Redaction Tool
============================================================
Enter the path to the PDF file: ~/documents/sensitive.pdf

Enter terms to redact (one per line, press Enter twice to finish):
confidential
secret
proprietary


Terms to redact: confidential, secret, proprietary

Opening PDF: /Users/username/documents/sensitive.pdf

Analyzing PDF structure...
   Found 7 native digital page(s)
   Found 3 scanned page(s) requiring OCR

Step 1: Removing text layer from 3 scanned page(s)...
   Text layer removed from 3 page(s)

Step 2: Performing OCR on 3 scanned page(s)...
   OCR'ing page 2/10...
   OCR'ing page 5/10...
   OCR'ing page 8/10...
   OCR complete for 3 page(s)

Step 3: Searching for and redacting terms...
   Page 1: Found 'confidential' in 'CONFIDENTIAL'
   Page 1: Found 'confidential' in 'confidential'
   Page 3: Found 'secret' in 'secret'
   Page 5: Found 'proprietary' in 'proprietary'
   Page 5: Found 'proprietary' in 'Proprietary'
   Page 5: Found 'proprietary' in 'proprietary'

Applied 6 redaction(s) total.
Saving redacted PDF to: /Users/username/documents/sensitive_redacted.pdf

============================================================
Redaction complete!
Redacted PDF saved to: /Users/username/documents/sensitive_redacted.pdf
============================================================
```

## How It Works

The script intelligently processes mixed PDFs with both native and scanned content:

### Step 0: Intelligent Page Analysis
- Analyzes each page to detect if it's native digital content or a scanned image
- Uses heuristics: text quantity, image coverage, and page structure
- Native pages (print-to-PDF): Already have accurate text layers
- Scanned pages: Images that need OCR for text detection

### Step 1: Selective Text Layer Removal
- **Only strips text from scanned pages** (not native digital pages)
- Preserves existing accurate text on native pages
- Keeps all images and visual content intact
- Ensures clean slate for OCR on scanned content

### Step 2: Targeted OCR
- **Only OCRs pages identified as scans**
- Renders scanned pages as high-resolution images (300 DPI)
- Uses Tesseract OCR to detect all text
- Adds invisible text layer with accurate bounding boxes
- Native digital pages keep their original text layers

### Step 3: Universal Redaction
- Searches ALL pages (both native and OCR'd) for specified terms
- Case-insensitive matching across entire document
- Adds permanent redaction annotations with black fill
- Completely removes text (not just covered)
- Applies redactions that cannot be undone or revealed

## Important Notes

- **Intelligent processing**: Native digital pages keep their accurate text; only scans are re-OCR'd
- **Mixed document support**: Handles PDFs with both native and scanned pages
- **Preserves quality**: Native text pages maintain original accuracy
- **Redactions are permanent**: Original text is completely removed, not just covered
- **Original file preserved**: A new file is created; the source PDF is never modified
- **Case-insensitive matching**: Finds all variations of search terms across all pages
- **Black boxes are permanent**: Cannot be removed or made transparent
- **OCR accuracy**: Results depend on image quality and text clarity in scanned pages

## Troubleshooting

**"tesseract is not installed" error:**
- Make sure Tesseract OCR is installed on your system (see Installation section)
- Verify installation: `tesseract --version`

**Slow processing:**
- OCR is computationally intensive; large PDFs will take time
- Processing time depends on number of pages and image resolution
- Typical speed: 2-5 seconds per page

**OCR accuracy issues:**
- Ensure PDF contains clear, readable text
- Low-resolution scans may produce poor OCR results
- Try rescanning documents at higher DPI (300+ recommended)

## License

MIT
