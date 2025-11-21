#!/usr/bin/env python3
"""
PDF Redaction Script
Redacts specified terms from a PDF by removing text and adding permanent black boxes.
"""

import fitz  # PyMuPDF
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


def redact_pdf(pdf_path, terms):
    """
    Redact all instances of specified terms from the PDF.

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

    total_redactions = 0

    # Iterate through each page
    for page_num in range(len(doc)):
        page = doc[page_num]

        # Search for each term and mark for redaction
        for term in terms:
            # Search for the term (case-insensitive by default)
            text_instances = page.search_for(term)

            if text_instances:
                print(f"Page {page_num + 1}: Found {len(text_instances)} instance(s) of '{term}'")
                total_redactions += len(text_instances)

                # Add redaction annotation for each instance
                for inst in text_instances:
                    # Create a redaction annotation
                    annot = page.add_redact_annot(inst, fill=(0, 0, 0))  # Black fill

        # Apply all redactions on this page
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

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
