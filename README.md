# PDF Redaction Tool

A Python script that permanently redacts (removes) specified terms from PDF files by replacing them with black boxes that cannot be removed.

## Features

- Searches for and redacts all instances of specified terms
- Permanently removes OCR text and replaces with black boxes
- Case-insensitive search
- Interactive command-line interface
- Saves redacted PDF next to original with `_redacted` suffix

## Requirements

- Python 3.7 or higher
- PyMuPDF (fitz) library

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
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
Page 1: Found 2 instance(s) of 'confidential'
Page 3: Found 1 instance(s) of 'secret'
Page 5: Found 3 instance(s) of 'proprietary'

Applied 6 redaction(s) total.
Saving redacted PDF to: /Users/username/documents/sensitive_redacted.pdf

============================================================
Redaction complete!
Redacted PDF saved to: /Users/username/documents/sensitive_redacted.pdf
============================================================
```

## How It Works

The script uses PyMuPDF to:
1. Open and parse the PDF file
2. Search each page for the specified terms
3. Add redaction annotations with black fill color
4. Apply the redactions permanently (text is removed, not just covered)
5. Save the result with optimized compression

## Important Notes

- Redactions are **permanent** - the original text is completely removed from the PDF
- The original PDF file is not modified - a new file is created
- The script performs case-insensitive matching by default
- Only searchable text can be redacted (text in images requires OCR first)

## License

MIT
