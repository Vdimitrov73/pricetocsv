# Quicken 2009 — Automated Price & Currency Update

This document explains how to configure Quicken 2009 to automatically import
end-of-day security prices and update currency exchange rates using
`PriceToCSV` and `ImportPrices.vbs`.

Tested on Quicken Home & Business 2009 (Windows). Expected to work on
Quicken 2007–2013 for Windows with possible adjustments to keyboard shortcuts.
Not compatible with Quicken 2014 or later.

## How It Works

1. **`PriceToCSV`** downloads end-of-day prices from Yahoo Finance and writes
   a Quicken-compatible CSV file (`prices_YYYYMMDD.csv`) to
   `%LOCALAPPDATA%\PriceToCSV\`.
2. **`ImportPrices.vbs`** automates Quicken to import the CSV and update
   currency exchange rates via the built-in One Step Update feature.
3. A custom **toolbar button** in Quicken launches `ImportPrices.vbs` with one
   click.

---

## Prerequisites

- Quicken Home & Business 2009 (Windows)
- `PriceToCSV` installed — via the [Microsoft Store](https://apps.microsoft.com/detail/9N8QB9ZLPPTB)
  (recommended) or the [ZIP release](https://gitlab.com/vdimitrov_73/pricetocsv/-/releases/permalink/latest)
- `PriceToCSV` configured with your symbols (see `README.md`)
- `ImportPrices.vbs` (this repo) placed in `Documents\PriceToCSV\`

---

## Step 1 — Configure QUICKEN.INI

Find the file at:

```
C:\ProgramData\Intuit\Quicken\Config\QUICKEN.INI
```

> ⚠️ Close Quicken before editing this file.

### a) Enable the custom toolbar button

Find the `AddApps` line and append `;QFL`:

```ini
AddApps=;QHI;QFL
```

### b) Enable currency rate download

The original Intuit currency server is defunct. Find this line:

```ini
CurrencyRateDownload=http://www.intuit.de/currency/data_de.txt
```

Add the following line **directly below** it:

```ini
CurrencyRateDownload2005=http://redirect.reckon.com.au/reckonaccounts_2013_au/currencydownloading
```

This points Quicken to a working Reckon Accounts server that provides 150+
currency exchange rates in a compatible format.

### c) Register the ImportPrices script

Add this section at the **bottom** of `QUICKEN.INI`:

```ini
[QFL]
ExeName=C:\Users\Administrator\Documents\PriceToCSV\ImportPrices.vbs
MenuString=Import Prices
IntuitID=1023
InformExec=FALSE
```

> ⚠️ Replace `Administrator` with your actual Windows username.

---

## Step 2 — Add the Toolbar Button

1. Start Quicken
2. Go to **Edit → Customize Toolbar**
3. Check **Show all choices**
4. Find **Quicken Family Lawyer** in the list → click **Add**
5. Click **Edit Icon** and rename it to `Import Prices`

---

## Step 3 — Daily Usage

### Run PriceToCSV first

Launch `PriceToCSV` (from the Start menu if installed via MS Store, or
double-click `PriceToCSV.exe` from the ZIP) and use option 1, or run it
non-interactively:

```
PriceToCSV.exe --run
```

This creates:

```
%LOCALAPPDATA%\PriceToCSV\prices_YYYYMMDD.csv
```

You can automate this with Windows Task Scheduler to run after market close.
See the **Scheduling** section in [README.md](README.md).

### Then click Import Prices in Quicken

Click the **Import Prices** toolbar button. The script will automatically:

1. Navigate to **Investing → Portfolio** (required for the Import menu to be available)
2. Import today's security prices from `prices_YYYYMMDD.csv`
3. Dismiss the "Successfully Imported X prices" confirmation
4. Open the Currency List (`Ctrl+Q`)
5. Trigger **Update Rates → One Step Update → Update Now!**
6. Download 36+ currency exchange rates from the Reckon server
7. Close all dialogs

> The full process takes approximately 20–25 seconds.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| "Today's prices file not found" | PriceToCSV not run yet today | Run `PriceToCSV --run` first |
| Import Prices menu item greyed out | Not on Investing tab | Script handles this automatically via `Ctrl+U` |
| Wrong number of prices imported | Symbol not in `config.json` | Add it via PriceToCSV menu option 3 |
| Currency update fails | No internet connection | Check connectivity; rates update separately from prices |
| Script clicks wrong thing | Quicken was slow to respond | Increase the relevant `WScript.Sleep` value in `ImportPrices.vbs` |

---

## Files in This Repo

| File | Description |
|---|---|
| `PriceToCSV.exe` | Downloads prices from Yahoo Finance, writes CSV (also on MS Store) |
| `ImportPrices.vbs` | Automates Quicken to import prices and update currencies |
| `config.json` | Your ticker symbols and aliases (created on first run) |
| `README.md` | PriceToCSV setup and usage |
| `QUICKEN_SETUP.md` | This file |
