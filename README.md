# PriceToCSV

A free tool for Canadian and US investors that downloads end-of-day adjusted
close prices from Yahoo Finance and exports them as a Quicken-compatible CSV file.

Built for investors who:
- Hold US and Canadian ETFs and stocks
- Use Quicken to track their portfolio
- Want to automate daily price updates instead of entering them manually

---

## Quick Start (Windows)

**[⬇ Get it on the Microsoft Store](https://apps.microsoft.com/detail/9N8QB9ZLPPTB)** — installs in seconds, no SmartScreen warning, auto-updates

Or download the **[latest ZIP release](https://gitlab.com/vdimitrov_73/pricetocsv/-/releases/permalink/latest)** — standalone `.exe`, no Python required

1. Launch `PriceToCSV.exe` (from Start menu or unzipped folder)
2. Edit `config.json` to add your ticker symbols
3. Double-click `PriceToCSV.exe` — use the menu or run with `--run`
4. Import the CSV into Quicken — or automate it with `ImportPrices.vbs` (see [QUICKEN_SETUP.md](QUICKEN_SETUP.md))

See [INSTALL.md](INSTALL.md) for all installation options.

---

## Download

**[⬇ Microsoft Store](https://apps.microsoft.com/detail/9N8QB9ZLPPTB)** — recommended, auto-updates

**[⬇ Latest ZIP release](https://gitlab.com/vdimitrov_73/pricetocsv/-/releases/permalink/latest)** — standalone `.exe`, no Python required

**Source:** [GitLab](https://gitlab.com/vdimitrov_73/pricetocsv) (primary) | [GitHub](https://github.com/Vdimitrov73/pricetocsv) (mirror)

> ZIP users — SmartScreen warning: click **More info** then **Run anyway**.

---

## Features

- Downloads end-of-day adjusted close prices from Yahoo Finance
- Supports US tickers (`VTI`, `TLT`, `AAPL`) and Canadian TSX tickers (`VUS.TO`, `XIC.TO`)
- Strips `.TO` suffix and maps forex symbols for clean Quicken output
- Fixed prices for some mutual funds (DYN6004, TDB8150, etc.)
- Historical date-range downloads
- Interactive menu or fully non-interactive CLI (`--run`)
- Scheduled automation support via Windows Task Scheduler
- Standard library only — no Python packages to install
- Output CSV row order: fixed prices → regular tickers → exchange rates

---

## Basic Usage

### Interactive menu

```
PriceToCSV.exe
```

or (Python users):

```
python PriceToCSV.py
```

### CLI (recommended for scheduled runs)

```
PriceToCSV.exe --run                                  Download today (config symbols)
PriceToCSV.exe --symbols VTI VXUS VUS.TO TLT          Download today (custom symbols)
PriceToCSV.exe --history 2025-01-01 2025-01-31        Historical date range
PriceToCSV.exe --symbols VTI --history 2026-01-01 2026-03-13
PriceToCSV.exe --config my_config.json --run          Custom config file
PriceToCSV.exe --help                                 Show all options
```

---

## How It Works

```
Yahoo Finance Chart API (adjusted close)
           │
           ▼
   config.json symbols
   + fixed_prices
   + symbol_aliases
           │
           ▼
   PriceToCSV.exe --run
           │
           ▼
   %LOCALAPPDATA%\PriceToCSV\prices_YYYYMMDD.csv
           │
           ▼
   Quicken: File → Import → Import Prices
   (or automated via ImportPrices.vbs — see QUICKEN_SETUP.md)
```

---

## Scheduling Daily Downloads

North American markets close at **4:00 PM ET**. Prices are final by ~4:15 PM ET.
Recommended scheduled run time: **4:20 PM ET**.

### Windows Task Scheduler

1. Open **Task Scheduler → Create Basic Task**
2. **Trigger:** Daily at 4:20 PM
3. **Action:** Start a program
   - Program/script: `C:\path\to\PriceToCSV.exe`
   - Arguments: `--run`
   - Start in: `C:\path\to\` *(folder containing `config.json`)*
4. Click **Finish**

After each run, import the new CSV from `%LOCALAPPDATA%\PriceToCSV\` into Quicken.
(or automated via ImportPrices.vbs — see QUICKEN_SETUP.md)

---

## Sample config.json

```json
{
  "symbols": ["MNT.TO", "CGL-C.TO", "VTI", "VXUS", "TLT", "VUS.TO", "CADEUR=X", "CADUSD=X"],
  "fixed_prices": {
    "DYN6000": 1.0,
    "DYN6004": 1.0,
    "TDB8150": 10.0
  },
  "symbol_aliases": {
    "CADEUR=X": "EUR",
    "CADUSD=X": "USD"
  }
}
```

| Key | Purpose |
|-----|---------|
| `symbols` | Tickers fetched from Yahoo Finance |
| `fixed_prices` | Mutual fund codes written at a fixed price, never fetched |
| `symbol_aliases` | Override any symbol's output name in the CSV |

Config search order:
1. Path given by `--config`
2. `config.json` in the current working directory
3. `%LOCALAPPDATA%\PriceToCSV\config.json`

---

## CSV Output

```
Symbol,Price,Date
DYN6000,1.0,03/14/2026
MNT,72.4,03/13/2026
VTI,326.13,03/13/2026
VUS,113.0,03/13/2026
EUR,0.6385,03/14/2026
USD,0.729,03/14/2026
```

| Mode | Output filename |
|------|----------------|
| Today | `prices_20260314.csv` |
| Historical | `prices_20260101_20260313.csv` |

Output directory: `%LOCALAPPDATA%\PriceToCSV\` (Windows)

---

## Quicken Import

For one-click automated import and currency update, see **[QUICKEN_SETUP.md](QUICKEN_SETUP.md)**.

Manual import:

1. **File → Import → Security Prices**
2. Select the CSV file → click **Import**

> **EUR / USD exchange rates:** Quicken's price import does not update currency
> exchange rates. Update them manually after each import:
> **Tools → Currency List** → double-click **USD** or **EUR** → enter the
> rate shown in the script output or CSV.
> (Automated via `ImportPrices.vbs` — see [QUICKEN_SETUP.md](QUICKEN_SETUP.md).)

---

## Ticker Format

| Market | Config symbol | CSV output |
|--------|--------------|------------|
| US stocks / ETFs | `VTI`, `TLT`, `AAPL` | `VTI`, `TLT`, `AAPL` |
| TSX (Canada) | `VUS.TO`, `XIC.TO`, `ZAG.TO` | `VUS`, `XIC`, `ZAG` |
| Forex (CAD base) | `CADEUR=X`, `CADUSD=X` | `EUR`, `USD` |
| Mutual funds (fixed) | `TDB8150`, `DYN6000` | `TDB8150`, `DYN6000` |

---

## File Reference

| File | Purpose |
|------|---------|
| `PriceToCSV.exe` | Standalone Windows executable — no Python required |
| `PriceToCSV.py` | Python source — run directly with Python 3.9+ |
| `ImportPrices.vbs` | Automates Quicken to import prices and update currencies |
| `config.json` | Your symbol list, fixed prices, and aliases |
| `setup.bat` | Python users: verifies Python install, shows run instructions |
| `README.FIRST.txt` | Quick start guide included in the ZIP bundle |
| `INSTALL.md` | Installation options and first-time setup |
| `QUICKEN_SETUP.md` | Quicken automation setup (ImportPrices.vbs + QUICKEN.INI) |
| `CHANGELOG.md` | Version history |

---

## Price Precision Note

Prices are stored as `round(price, 4)` — natural Python float representation
(e.g. `72.4`, `0.729`). Prices before a dividend ex-date will show more decimal
places than the Yahoo Finance History page (which rounds to 2) — both values are
correct. The extra precision reflects the dividend adjustment factor and is more
accurate for cost-basis calculations in Quicken.

---

## Data Source

Yahoo Finance Chart API v8 — adjusted close prices at `1d` interval.

```
https://query1.finance.yahoo.com/v8/finance/chart/{symbol}
```

---

## Contributing

1. [Open an issue](https://gitlab.com/vdimitrov_73/pricetocsv/-/issues) describing the problem or suggestion
2. Fork the repository on [GitLab](https://gitlab.com/vdimitrov_73/pricetocsv)
3. Create a branch: `git checkout -b fix/your-fix-name`
4. Make your changes and test them
5. Submit a merge request with a clear description of what changed and why

---

## Disclaimer

This tool is for personal convenience only. It is not financial advice.
Always verify imported prices against your brokerage statements.

---

## License

MIT License — see [LICENSE](LICENSE) for full text.
