@echo off
echo Retool Automation - Survey Reward Tool
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install --upgrade pip
pip install pyautogui colorama

REM Run the script
if "%1"=="" (
    python retool_automation.py
) else (
    python retool_automation.py %*
)

pause