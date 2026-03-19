# Installation Guide

## Option A — Microsoft Store (recommended)

1. Search for **PriceToCSV** in the [Microsoft Store](https://apps.microsoft.com/detail/9N8QB9ZLPPTB)
   or click the link to install directly
2. Click **Get** — no SmartScreen warning, auto-updates automatically
3. Launch from the Start menu
4. On first run, edit `config.json` to add your symbols

---

## Option B — Windows Executable (ZIP, no Python required)

1. Download `PriceToCSV_vX.Y.Z.zip` from the
   [latest release](https://gitlab.com/vdimitrov_73/pricetocsv/-/releases/permalink/latest)
2. Unzip anywhere (e.g. `C:\Tools\PriceToCSV\`)
3. Edit `config.json` to add your symbols
4. Double-click `PriceToCSV.exe` — or run from the command line:

```
PriceToCSV.exe --run
PriceToCSV.exe --help
```

> SmartScreen warning: click **More info** then **Run anyway**.

---

## Option C — Run from Source (Python 3.9+)

```bash
# 1. Clone the repository
git clone https://gitlab.com/vdimitrov_73/pricetocsv.git
cd pricetocsv

# 2. Verify Python version (must be 3.9+)
python --version

# 3. Run directly — no pip install needed
python PriceToCSV.py
python PriceToCSV.py --run
python PriceToCSV.py --help
```

No virtual environment or package installation required.
The script uses only the Python standard library.

---

## Option D — Build the .exe Yourself

```bash
pip install pyinstaller
pyinstaller --onefile --name PriceToCSV PriceToCSV.py
# Output: dist/PriceToCSV.exe
```

Or run `setup.bat` — it verifies your Python install and shows run instructions.

The GitLab CI pipeline (`.gitlab-ci.yml`) automates this on every `vX.Y.Z` tag push.

---

## Output Location

| Platform | Path |
|----------|------|
| Windows  | `%LOCALAPPDATA%\PriceToCSV\` |
| Linux    | `~/.local/share/PriceToCSV/`  |
| macOS    | `~/.local/share/PriceToCSV/`  |

If a `config.json` exists in the **current working directory**,
it takes priority over the one in the data directory.

---

## Quicken Import

For fully automated price import and currency update, set up `ImportPrices.vbs`.
See **[QUICKEN_SETUP.md](QUICKEN_SETUP.md)** for step-by-step instructions.

Manual import:

1. Open Quicken → Investing **File → Import → Import Prices**
2. Select the generated CSV file
3. Click **Import**

The CSV format (`Symbol, Price, Date MM/DD/YYYY`) is compatible with
Quicken Home & Business (2007–2013, Windows).

> **EUR / USD exchange rates** are not updated by the price import.
> Update them manually: **Tools → Currency List** →
> double-click the currency → enter the rate from the CSV.
> (This is automated by `ImportPrices.vbs` — see [QUICKEN_SETUP.md](QUICKEN_SETUP.md).)

---

## Scheduling Daily Downloads

See the **Scheduling** section in [README.md](README.md) for
Windows Task Scheduler setup instructions.

Recommended run time: **4:20 PM ET** (markets close 4:00 PM, prices final ~4:15 PM).
