# Changelog

All notable changes to PriceToCSV are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] — 2026-03-14

### Fixed
- Price formatting now matches natural Python float representation
  (`72.4` instead of `72.4000`, `0.729` instead of `0.7290`)
- Removed trailing zeros that do not affect Quicken import precision

### Changed
- CSV row order is now: **fixed prices → regular tickers → forex/exchange rates**
- Symbol display names in CSV output:
  - `.TO` suffix stripped  (`VUS.TO` → `VUS`, `MNT.TO` → `MNT`)
  - Forex symbols mapped to currency code (`CADEUR=X` → `EUR`, `CADUSD=X` → `USD`)
- Menu "Symbols" line now shows a compact summary (`VTI, VXUS, TLT, IEF, AVUV  (+16 more)`)
  instead of wrapping the full list across the screen
- Saving symbols in option 3 now confirms count (`✓  Saved 21 symbol(s).`)
- `symbol_aliases` added to `config.json` for custom ticker → display name mappings

### Added
- `symbol_aliases` config key to override any symbol's output name

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
