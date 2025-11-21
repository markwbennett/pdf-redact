@echo off
REM PDF Redaction Tool - Installation Script for Windows
REM This script automates the setup process

echo ============================================================
echo PDF Redaction Tool - Installation Script
echo ============================================================
echo.

REM Check Python installation
echo Step 1: Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python is not installed or not in PATH!
    echo   Please install Python 3.7 or higher from https://www.python.org
    echo   Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo + Found: %PYTHON_VERSION%
echo.

REM Check Tesseract installation
echo Step 2: Checking Tesseract OCR installation...
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Tesseract OCR is not installed or not in PATH!
    echo.
    echo   Download and install from:
    echo   https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo   After installation, add Tesseract to your PATH or
    echo   install it to the default location: C:\Program Files\Tesseract-OCR
    echo.
    set /p CONTINUE="Would you like to continue anyway? (Y/N): "
    if /i not "%CONTINUE%"=="Y" exit /b 1
) else (
    for /f "tokens=*" %%i in ('tesseract --version 2^>^&1 ^| findstr /C:"tesseract"') do set TESSERACT_VERSION=%%i
    echo + Found: %TESSERACT_VERSION%
)
echo.

REM Create virtual environment
echo Step 3: Creating Python virtual environment...
if exist "venv\" (
    echo   Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo + Virtual environment created
)
echo.

REM Install dependencies
echo Step 4: Installing Python dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
echo + Dependencies installed:
echo   - PyMuPDF (PDF processing^)
echo   - pytesseract (OCR integration^)
echo   - Pillow (Image processing^)
echo.

REM Success message
echo ============================================================
echo + Installation complete!
echo ============================================================
echo.
echo To use the tool:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Run the script:
echo      python redact_pdf.py
echo.
echo   3. When finished, deactivate:
echo      deactivate
echo.
pause
