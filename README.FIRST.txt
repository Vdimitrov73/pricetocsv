============================================================
  PriceToCSV — Quick Start
============================================================

STEP 1 — Run the tool
---------------------
  python PriceToCSV.py
  or double-click PriceToCSV.exe on Windows

STEP 2 — Use the menu
----------------------
  1  Download prices (today)
  2  Download historical prices
  3  Edit symbol list
  Q  Quit

  Or skip the menu with CLI flags:

  python PriceToCSV.py --run
  python PriceToCSV.py --symbols VTI VXUS VUS.TO TLT
  python PriceToCSV.py --history 2025-01-01 2025-01-31
  python PriceToCSV.py --config my_config.json --run

STEP 3 — Find your CSV
-----------------------
  Windows  : %LOCALAPPDATA%\PriceToCSV\prices_YYYYMMDD.csv
  Linux    : ~/.local/share/PriceToCSV/prices_YYYYMMDD.csv
  macOS    : ~/.local/share/PriceToCSV/prices_YYYYMMDD.csv

STEP 4 — Import into Quicken
------------------------------
  File > Import > Security Prices
  Select the CSV file and click Import.

  CSV format:  Symbol, Price, Date (MM/DD/YYYY)

============================================================
  For full documentation see README.md
============================================================
