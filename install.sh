#!/bin/bash
# PDF Redaction Tool - Installation Script for macOS/Linux
# This script automates the setup process

set -e  # Exit on error

echo "============================================================"
echo "PDF Redaction Tool - Installation Script"
echo "============================================================"
echo ""

# Check Python installation
echo "Step 1: Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
else
    echo "✗ Python 3 is not installed!"
    echo "  Please install Python 3.7 or higher from https://www.python.org"
    exit 1
fi
echo ""

# Check Tesseract installation
echo "Step 2: Checking Tesseract OCR installation..."
if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version | head -n 1)
    echo "✓ Found: $TESSERACT_VERSION"
else
    echo "✗ Tesseract OCR is not installed!"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  Install with: brew install tesseract"
        echo "  (If you don't have Homebrew: https://brew.sh)"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  Install with: sudo apt-get install tesseract-ocr"
    fi
    echo ""
    read -p "Would you like to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo ""

# Create virtual environment
echo "Step 3: Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "  Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate and install dependencies
echo "Step 4: Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✓ Dependencies installed:"
echo "  - PyMuPDF (PDF processing)"
echo "  - pytesseract (OCR integration)"
echo "  - Pillow (Image processing)"
echo ""

# Success message
echo "============================================================"
echo "✓ Installation complete!"
echo "============================================================"
echo ""
echo "To use the tool:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the script:"
echo "     python redact_pdf.py"
echo ""
echo "  3. When finished, deactivate:"
echo "     deactivate"
echo ""
