@echo off
REM PDF Redaction Tool - Run Script for Windows
REM This script ensures everything is installed and runs the tool

echo ============================================================
echo PDF Redaction Tool
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python is not installed or not in PATH!
    echo   Please install Python 3.7 or higher from https://www.python.org
    pause
    exit /b 1
)

REM Check Tesseract installation
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ! Warning: Tesseract OCR is not installed or not in PATH!
    echo.
    echo   Download and install from:
    echo   https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    set /p CONTINUE="Continue anyway? (Y/N): "
    if /i not "%CONTINUE%"=="Y" exit /b 1
    echo.
)

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Setting up virtual environment...
    python -m venv venv
    echo + Virtual environment created
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import PyMuPDF, pytesseract, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    python -m pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
    echo + Dependencies installed
    echo.
)

REM Run the script
echo Starting PDF Redaction Tool...
echo.
python redact_pdf.py

REM Deactivate virtual environment
call deactivate
