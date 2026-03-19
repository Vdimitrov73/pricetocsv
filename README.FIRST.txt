============================================================
  PriceToCSV — Quick Start
============================================================

STEP 1 — Get the tool
---------------------
  Microsoft Store (recommended — auto-updates, no warnings):
    Search for PriceToCSV in the Microsoft Store, then
    launch it from the Start menu.

  ZIP release:
    Double-click PriceToCSV.exe   (no Python required)
    or: python PriceToCSV.py      (if you have Python 3.9+)

STEP 2 — Use the menu
----------------------
  1  Download prices (today)
  2  Download historical prices
  3  Edit symbol list
  Q  Quit

  Or skip the menu entirely (ideal for scheduled runs):

  PriceToCSV.exe --run
  PriceToCSV.exe --symbols VTI VXUS VUS.TO TLT
  PriceToCSV.exe --history 2025-01-01 2025-01-31

STEP 3 — Find your CSV
-----------------------
  Windows  : %LOCALAPPDATA%\PriceToCSV\prices_YYYYMMDD.csv

STEP 4 — Import into Quicken
-----------------------------
  AUTOMATED (recommended):
    Use ImportPrices.vbs for one-click import + currency update.
    See QUICKEN_SETUP.md for setup instructions.

  MANUAL:
    File > Import > Import Prices
    Select the CSV file and click Import.

    CSV format:  Symbol, Price, Date (MM/DD/YYYY)

    NOTE: EUR and USD exchange rates in the CSV are NOT imported
    by Quicken's price import. Update them manually:
    Tools > Currency List > double-click USD or EUR > enter rate.

STEP 5 — Schedule daily downloads (optional)
---------------------------------------------
  Recommended run time: 4:20 PM ET (North American markets
  close at 4:00 PM ET — prices are final by ~4:15 PM ET).

  Windows Task Scheduler:
  1. Open Task Scheduler > Create Basic Task
  2. Trigger: Daily at 4:20 PM
  3. Action: Start a program
     Program : C:\path\to\PriceToCSV.exe
     Arguments: --run
     Start in : C:\path\to\   (folder with config.json)
  4. Click Finish

  MS Store users: PriceToCSV is installed system-wide.
  Use the full path shown in Task Scheduler when browsing
  for the executable.

============================================================
  For full documentation see README.md
  For Quicken automation see QUICKEN_SETUP.md
============================================================
