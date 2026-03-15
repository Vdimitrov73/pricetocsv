# PriceToCSV

Download end-of-day **adjusted close prices** from Yahoo Finance and export
them as a **Quicken-compatible CSV** file.

- ✅ Standard library only — zero dependencies
- ✅ US and Canadian tickers (`VTI`, `VUS.TO`, `XIC.TO`, …)
- ✅ Fixed prices for mutual funds
- ✅ Interactive menu **or** CLI flags
- ✅ Historical date-range downloads
- ✅ Windows `.exe` via GitLab CI

---

## Quick Start

```bash
python PriceToCSV.py            # interactive menu
python PriceToCSV.py --run      # non-interactive, uses config.json
```

---

## CLI Reference

| Flag | Description |
|------|-------------|
| `--run` | Download today's prices (config symbols, non-interactive) |
| `--symbols SYM …` | Override symbol list |
| `--history START END` | Historical range `YYYY-MM-DD YYYY-MM-DD` |
| `--config FILE` | Use a custom `config.json` |
| `--version` | Print version and exit |

### Examples

```bash
# Today's prices for config symbols
python PriceToCSV.py --run

# Today's prices, custom symbols (US + Canadian)
python PriceToCSV.py --symbols VTI VXUS TLT VUS.TO XIC.TO

# Historical download for config symbols
python PriceToCSV.py --history 2025-01-01 2025-01-31

# Historical download for specific symbols
python PriceToCSV.py --symbols VTI VXUS --history 2025-01-01 2025-01-31

# Use a different config file
python PriceToCSV.py --config ~/my_portfolio.json --run
```

---

## config.json

```json
{
  "symbols": ["VTI", "VXUS", "TLT", "VUS.TO", "XIC.TO", "CADEUR=X", "CADUSD=X"],
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

- **`symbols`** — tickers downloaded from Yahoo Finance - .TO suffix stripped
- **`fixed_prices`** — mutual fund codes always written at the given price
- **`symbol_aliases`** — override any symbol's output name.

Config search order:
1. Path given by `--config`
2. `config.json` in the current working directory
3. Platform data directory (see [INSTALL.md](INSTALL.md))

---

## CSV Output

```
Symbol,Price,Date
VTI,278.4321,03/14/2026
VXUS,57.1100,03/14/2026
VUS.TO,101.2500,03/14/2026
TDB8150,10.0000,03/14/2026
```

**File naming:**

| Mode | Filename |
|------|----------|
| Today | `prices_20260314.csv` |
| Historical | `prices_20250101_20250131.csv` |

**Output directory:**

| Platform | Path |
|----------|------|
| Windows  | `%LOCALAPPDATA%\PriceToCSV\` |
| Linux / macOS | `~/.local/share/PriceToCSV/` |

---

## Interactive Menu

```
──────────────────────────────────────────────────────
  PriceToCSV  v1.1.0
──────────────────────────────────────────────────────
  Symbols : VTI, VXUS, TLT, VUS.TO, XIC.TO
  Fixed   : DYN6000, DYN6004, TDB8150
  Output  : /home/vlad/.local/share/PriceToCSV
──────────────────────────────────────────────────────
  1  Download prices (today)
  2  Download historical prices
  3  Edit symbol list
  Q  Quit
──────────────────────────────────────────────────────
```

---

## Ticker Format

| Market | Example |
|--------|---------|
| US stocks / ETFs | `VTI`, `TLT`, `AAPL` |
| TSX (Canada) | `VUS.TO`, `XIC.TO`, `ZAG.TO` |
| Mutual funds (fixed) | `TDB8150`, `DYN6000` |

---

## Data Source

Yahoo Finance Chart API v8
```
https://query1.finance.yahoo.com/v8/finance/chart/{symbol}
```
Returns adjusted close prices at daily (`1d`) interval.

---

## Building the Windows .exe

```bash
pip install pyinstaller
pyinstaller --onefile --name PriceToCSV PriceToCSV.py
# Output: dist/PriceToCSV.exe
```

The GitLab CI pipeline (`.gitlab-ci.yml`) automates this on every push
to `main` or on tagged releases, requiring a registered Windows runner.

---

## License

MIT
