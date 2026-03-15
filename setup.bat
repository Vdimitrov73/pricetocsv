@echo off
title PriceToCSV Setup
echo ============================================================
echo   PriceToCSV -- Python Setup
echo ============================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found.
    echo         Install Python 3.9+ from https://python.org
    echo         Make sure to tick "Add Python to PATH" during install.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo [OK] %%i found.
echo [OK] No extra packages required -- standard library only.
echo.
echo ── How to run ──────────────────────────────────────────────
echo   python PriceToCSV.py              (interactive menu)
echo   python PriceToCSV.py --run        (non-interactive)
echo   python PriceToCSV.py --help       (all options)
echo ────────────────────────────────────────────────────────────
echo.
pause
