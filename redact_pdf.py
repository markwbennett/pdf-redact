#!/usr/bin/env python3
"""
PDF Redaction Script
Removes existing text layer, performs OCR, then redacts specified terms
by removing text and adding permanent black boxes.
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import sys


def get_pdf_path():
    """Prompt user for PDF path and validate it exists."""
    while True:
        pdf_path = input("Enter the path to the PDF file: ").strip()

        # Handle quoted paths
        if pdf_path.startswith('"') and pdf_path.endswith('"'):
            pdf_path = pdf_path[1:-1]
        elif pdf_path.startswith("'") and pdf_path.endswith("'"):
            pdf_path = pdf_path[1:-1]

        # Expand user home directory
        pdf_path = os.path.expanduser(pdf_path)

        if os.path.isfile(pdf_path) and pdf_path.lower().endswith('.pdf'):
            return pdf_path
        else:
            print(f"Error: '{pdf_path}' is not a valid PDF file. Please try again.")


def get_redaction_terms():
    """Prompt user for terms to redact (two consecutive linefeeds ends input)."""
    print("\nEnter terms to redact (one per line, press Enter twice to finish):")
    terms = []
    empty_line_count = 0

    while True:
        line = input()

        if line.strip() == "":
            empty_line_count += 1
            if empty_line_count >= 2:
                break
        else:
            empty_line_count = 0
            terms.append(line.strip())

    return [term for term in terms if term]  # Remove any empty strings


def detect_page_type(page):
    """
    Detect if a page is native digital content or a scanned image.

    Args:
        page: PyMuPDF page object

    Returns:
        'native' if page has native text content, 'scanned' if it's an image/scan
    """
    # Get text content and images on the page
    text = page.get_text().strip()
    images = page.get_images()

    # Get page dimensions
    page_rect = page.rect
    page_area = page_rect.width * page_rect.height

    # Calculate total area covered by images
    image_area = 0
    for img_info in images:
        try:
            img_rect = page.get_image_bbox(img_info[7])  # img_info[7] is xref
            if img_rect:
                image_area += img_rect.width * img_rect.height
        except:
            pass

    # Heuristics for detection:
    # 1. If page has substantial text (>100 chars) and images cover <50% of page -> native
    # 2. If page has little/no text (<50 chars) and large images (>80% coverage) -> scanned
    # 3. If images cover most of the page (>80%) -> likely scanned

    image_coverage = image_area / page_area if page_area > 0 else 0

    if len(text) > 100 and image_coverage < 0.5:
        return 'native'
    elif len(text) < 50 and image_coverage > 0.8:
        return 'scanned'
    elif image_coverage > 0.8:
        return 'scanned'
    elif len(text) > 50:
        return 'native'
    else:
        # Default to scanned if unclear - safer to OCR than to miss text
        return 'scanned'


def strip_text_layer(doc, page_numbers):
    """
    Remove all existing text from specified pages of the PDF, keeping only images/graphics.

    Args:
        doc: PyMuPDF document object
        page_numbers: List of page numbers to strip text from
    """
    if not page_numbers:
        print("\nStep 1: No pages need text layer removal (all native digital content)")
        return

    print(f"\nStep 1: Removing text layer from {len(page_numbers)} scanned page(s)...")

    for page_num in page_numbers:
        page = doc[page_num]

        # Get all text blocks and redact them (removes text completely)
        text_dict = page.get_text("dict")
        blocks = text_dict.get("blocks", [])

        for block in blocks:
            if block.get("type") == 0:  # Text block
                bbox = fitz.Rect(block["bbox"])
                # We're not adding a fill color here - just removing the text
                page.add_redact_annot(bbox)

        # Apply redactions to remove text but keep images
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    print(f"   Text layer removed from {len(page_numbers)} page(s)")


def ocr_page(page, dpi=300):
    """
    Perform OCR on a PDF page and return text with bounding boxes.

    Args:
        page: PyMuPDF page object
        dpi: Resolution for rendering page as image

    Returns:
        List of tuples (text, bbox) for each word found
    """
    # Render page to image
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)

    # Convert to PIL Image
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))

    # Perform OCR with bounding box data
    ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    # Extract words and their bounding boxes
    words_with_boxes = []
    n_boxes = len(ocr_data['text'])

    for i in range(n_boxes):
        text = ocr_data['text'][i].strip()
        if text:  # Skip empty strings
            # Convert image coordinates to PDF coordinates
            x0 = ocr_data['left'][i] * 72 / dpi
            y0 = ocr_data['top'][i] * 72 / dpi
            x1 = (ocr_data['left'][i] + ocr_data['width'][i]) * 72 / dpi
            y1 = (ocr_data['top'][i] + ocr_data['height'][i]) * 72 / dpi

            bbox = fitz.Rect(x0, y0, x1, y1)
            words_with_boxes.append((text, bbox))

    return words_with_boxes


def add_ocr_text_layer(doc, page_numbers):
    """
    Add OCR'd text as an invisible text layer to specified pages of the PDF.

    Args:
        doc: PyMuPDF document object
        page_numbers: List of page numbers to OCR

    Returns:
        Dictionary mapping page numbers to list of (text, bbox) tuples
    """
    if not page_numbers:
        print("\nStep 2: No pages need OCR (all native digital content)")
        return {}

    print(f"\nStep 2: Performing OCR on {len(page_numbers)} scanned page(s)...")

    page_ocr_data = {}

    for page_num in page_numbers:
        page = doc[page_num]
        print(f"   OCR'ing page {page_num + 1}/{len(doc)}...")

        # Get OCR data for this page
        words_with_boxes = ocr_page(page)
        page_ocr_data[page_num] = words_with_boxes

        # Add invisible text layer
        for text, bbox in words_with_boxes:
            # Insert text at the correct position with zero opacity (invisible)
            page.insert_text(
                bbox.tl,  # Top-left point
                text,
                fontsize=bbox.height * 0.8,  # Approximate font size
                color=(0, 0, 0),
                render_mode=3  # Invisible text (neither fill nor stroke)
            )

    print(f"   OCR complete for {len(page_numbers)} page(s)")
    return page_ocr_data


def redact_terms(doc, page_ocr_data, terms):
    """
    Search for terms in OCR'd text and redact them.

    Args:
        doc: PyMuPDF document object
        page_ocr_data: Dictionary of OCR data from add_ocr_text_layer
        terms: List of terms to redact

    Returns:
        Number of redactions made
    """
    print("\nStep 3: Searching for and redacting terms...")

    total_redactions = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        ocr_words = page_ocr_data.get(page_num, [])

        # Search for each term
        for term in terms:
            term_lower = term.lower()

            # Search through OCR'd words for matches (case-insensitive)
            for text, bbox in ocr_words:
                if term_lower in text.lower():
                    print(f"   Page {page_num + 1}: Found '{term}' in '{text}'")
                    # Add redaction annotation with black fill
                    page.add_redact_annot(bbox, fill=(0, 0, 0))
                    total_redactions += 1

        # Apply all redactions on this page
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    return total_redactions


def redact_pdf(pdf_path, terms):
    """
    Intelligently process PDF: OCR only scanned pages, then redact specified terms.

    Args:
        pdf_path: Path to the source PDF file
        terms: List of terms to redact

    Returns:
        Path to the redacted PDF file
    """
    if not terms:
        print("No terms provided. Exiting without redaction.")
        return None

    print(f"\nOpening PDF: {pdf_path}")
    doc = fitz.open(pdf_path)

    # Step 0: Analyze pages to determine which need OCR
    print("\nAnalyzing PDF structure...")
    scanned_pages = []
    native_pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_type = detect_page_type(page)

        if page_type == 'scanned':
            scanned_pages.append(page_num)
        else:
            native_pages.append(page_num)

    print(f"   Found {len(native_pages)} native digital page(s)")
    print(f"   Found {len(scanned_pages)} scanned page(s) requiring OCR")

    # Step 1: Remove existing text layer from scanned pages only
    strip_text_layer(doc, scanned_pages)

    # Step 2: Perform OCR only on scanned pages
    page_ocr_data = add_ocr_text_layer(doc, scanned_pages)

    # Step 3: Search and redact terms (on all pages)
    total_redactions = redact_terms(doc, page_ocr_data, terms)

    # Generate output filename
    base_name, ext = os.path.splitext(pdf_path)
    output_path = f"{base_name}_redacted{ext}"

    # Save the redacted PDF
    print(f"\nApplied {total_redactions} redaction(s) total.")
    print(f"Saving redacted PDF to: {output_path}")
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

    return output_path


def main():
    """Main script execution."""
    print("=" * 60)
    print("PDF Redaction Tool")
    print("=" * 60)

    # Get PDF path
    pdf_path = get_pdf_path()

    # Get terms to redact
    terms = get_redaction_terms()

    if not terms:
        print("\nNo terms entered. Exiting.")
        sys.exit(0)

    print(f"\nTerms to redact: {', '.join(terms)}")

    # Perform redaction
    output_path = redact_pdf(pdf_path, terms)

    if output_path:
        print(f"\n{'=' * 60}")
        print("Redaction complete!")
        print(f"Redacted PDF saved to: {output_path}")
        print(f"{'=' * 60}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
