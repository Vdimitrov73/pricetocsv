# Changelog

All notable changes to PriceToCSV are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
