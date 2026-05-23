# Changelog

All notable changes to PriceToCSV are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.2.6] — 2026-05-23

### Fixed
- fetch_prices(): added symbol mismatch check against meta.symbol to prevent
  wrong prices from reaching Quicken on redirected/delisted tickers
- fetch_prices(): added timestamp/adjclose array parity check for silent data loss
- _get_json(): exponential backoff retry (1s, 2s) on HTTP 429/502/503/504

## [1.2.5] — 2026-03-19

### Added
- Windows package published to the **Microsoft Store** (MSIX, auto-updates, no SmartScreen)
- `ImportPrices.vbs`: automates Quicken to import today's prices and update
  EUR/USD currency exchange rates with one click
- `QUICKEN_SETUP.md`: full setup guide for QUICKEN.INI configuration,
  toolbar button, and daily usage (replaces `QUICKEN_UPDATE.md`)

### Changed
- `INSTALL.md`: Microsoft Store added as Option A (recommended install method)
- `README.md`: MS Store link added to Download and Quick Start sections;
  Quicken import section now references `ImportPrices.vbs` and `QUICKEN_SETUP.md`
- `README.FIRST.txt`: STEP 1 updated for MS Store users; STEP 4 updated to
  reflect automated import via `ImportPrices.vbs`

---

## [1.2.0] — 2026-03-15

### Changed
- `--help` / `--version` epilog now shows `PriceToCSV.exe` examples first,
  with `python PriceToCSV.py` listed as the Python-user alternative
- README.md fully rewritten: download links, flow diagram, scheduling guide,
  file reference table, contributing section — modelled on t3_compute

### Added
- `README.FIRST.txt`: STEP 5 — Windows Task Scheduler setup (4:20 PM ET daily)
- `README.FIRST.txt`: NOTE explaining EUR/USD exchange rates must be updated
  manually in Quicken via Tools → Currency List
- `README.md`: Scheduling section, Quicken import note, price precision note,
  disclaimer, contributing guide, GitLab/GitHub source links

---

## [1.1.2] — 2026-03-14

### Fixed
- `.gitlab-ci.yml`: removed venv activation steps (not needed — standard library only)
- `.gitlab-ci.yml`: replaced `echo >` with `Set-Content`/`Add-Content -Encoding utf8`
  to guarantee UTF-8 dotenv output for the release stage

---

## [1.1.1] — 2026-03-14

### Fixed
- `.gitlab-ci.yml`: corrected runner tag from `windows` to `saas-windows-medium-amd64`
- `.gitlab-ci.yml`: added `release` stage matching t3_compute pipeline structure

---

## [1.1.0] — 2026-03-14

### Fixed
- Price formatting now uses natural Python float representation
  (`72.4` not `72.4000`, `0.729` not `0.7290`)

### Changed
- CSV row order: **fixed prices → regular tickers → forex/exchange rates**
- Symbol output names: `.TO` suffix stripped, forex mapped to currency code
  (`CADEUR=X` → `EUR`, `CADUSD=X` → `USD`)
- Menu "Symbols" line shows compact summary when more than 5 symbols configured
- Saving symbols confirms count (`✓  Saved 21 symbol(s).`)

### Added
- `symbol_aliases` config key for custom ticker → display name mappings

---

## [1.0.0] — 2026-03-14

### Added
- Interactive menu: download today, download historical, edit symbols, quit
- `--run`, `--symbols`, `--history`, `--config`, `--version` CLI flags
- Adjusted close price fetch via Yahoo Finance Chart API v8
- US tickers, Canadian `.TO` tickers, and forex `=X` pairs
- Fixed-price support for mutual funds
- Quicken-compatible CSV: `Symbol, Price, Date (MM/DD/YYYY)`
- Platform-aware output directory (Windows `%LOCALAPPDATA%`, Linux/macOS `~/.local/share`)
- Standard library only — no third-party dependencies
- GitLab CI pipeline for Windows .exe via PyInstaller
- `.github/workflows/build_exe.yml` for GitHub Actions mirror release

---
