#!/bin/bash
# PDF Redaction Tool - Run Script for macOS/Linux
# This script ensures everything is installed and runs the tool

set -e  # Exit on error

echo "============================================================"
echo "PDF Redaction Tool"
echo "============================================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed!"
    echo "  Please install Python 3.7 or higher from https://www.python.org"
    exit 1
fi

# Check Tesseract installation
if ! command -v tesseract &> /dev/null; then
    echo "⚠ Warning: Tesseract OCR is not installed!"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  Install with: brew install tesseract"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  Install with: sudo apt-get install tesseract-ocr"
    fi
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    echo ""
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python -c "import PyMuPDF, pytesseract, PIL" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
    echo ""
fi

# Run the script
echo "Starting PDF Redaction Tool..."
echo ""
python redact_pdf.py

# Deactivate virtual environment
deactivate
