# Installation Guide

## Option A — Run from Source (all platforms)

### Requirements
- Python 3.9 or newer
- Internet access

### Steps
```bash
# 1. Clone the repository
git clone https://gitlab.com/<your-group>/PriceToCSV.git
cd PriceToCSV

# 2. (Optional) verify Python version
python --version        # must be 3.9+

# 3. Run directly — no pip install needed
python PriceToCSV.py
```

No virtual environment or package installation is required.
The script uses only the Python standard library.

---

## Option B — Windows Executable (.exe)

Download `PriceToCSV.zip` from the latest GitLab CI artifact
(or the Releases page), unzip it, and double-click `PriceToCSV.exe`.

---

## Option C — Build the .exe Yourself

### Requirements
- Python 3.9+
- PyInstaller (`pip install pyinstaller`)

### Steps
```bash
pip install pyinstaller
pyinstaller --onefile --name PriceToCSV PriceToCSV.py
```

The executable is created at `dist/PriceToCSV.exe` (Windows)
or `dist/PriceToCSV` (Linux/macOS).

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

1. Open Quicken → **File → Import → Security Prices**
2. Select the generated CSV file
3. Click **Import**

The CSV format (`Symbol, Price, Date`) is compatible with
Quicken for Windows and Quicken for Mac.
