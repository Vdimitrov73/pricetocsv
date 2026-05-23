# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PriceToCSV is a Python tool for Canadian and US investors that downloads end-of-day adjusted close prices from Yahoo Finance and exports them as Quicken-compatible CSV files. It supports both US tickers (`VTI`, `TLT`, `AAPL`) and Canadian TSX tickers (`VUS.TO`, `XIC.TO`) with automatic symbol conversion.

## Development Environment

- **Language**: Python 3.9+
- **Dependencies**: Standard library only (no external packages)
- **Main script**: `PriceToCSV.py`
- **Configuration**: `config.json`

## Common Development Tasks

### Running the Application
```bash
# Interactive menu (Python)
python PriceToCSV.py

# Download today's prices (non-interactive)
python PriceToCSV.py --run

# Custom symbols
python PriceToCSV.py --symbols VTI VXUS VUS.TO

# Historical data
python PriceToCSV.py --history 2025-01-01 2025-01-31

# Custom config file
python PriceToCSV.py --config my_config.json --run
```

### Testing
```bash
# Run the main application with test config
python PriceToCSV.py --config test_config.json --run

# Test symbol conversion logic
python -c "from PriceToCSV import display_name; print(display_name('VUS.TO', {}))"
```

### Code Structure
- **`PriceToCSV.py`**: Main application with CLI interface and Yahoo Finance integration
- **`config.json`**: Symbol list, fixed prices, and symbol aliases
- **`data_dir()`**: Handles Windows data directory for MSIX/frozen executables
- **`fetch_prices()`**: Yahoo Finance API integration
- **`display_name()`**: Symbol conversion for Quicken compatibility

### Key Functions
- `run_download()`: Main download orchestration
- `fetch_prices()`: Yahoo Finance API calls
- `display_name()`: Symbol name conversion
- `load_config()`/`save_config()`: Configuration management

### Adding New Features
1. Update `PriceToCSV.py` with new functionality
2. Add corresponding CLI arguments in `main()`
3. Update `README.md` with usage examples
4. Test with both interactive and CLI modes

### Symbol Management
- **US tickers**: Use symbols like `VTI`, `TLT`, `AAPL`
- **TSX tickers**: Use symbols like `VUS.TO`, `XIC.TO` (auto-converts to `VUS`, `XIC`)
- **Forex**: Use symbols like `CADEUR=X`, `CADUSD=X` (auto-converts to `EUR`, `USD`)
- **Fixed prices**: Add mutual funds to `fixed_prices` dictionary

### Configuration
- **Symbol aliases**: Map forex symbols to display names
- **Fixed prices**: Set static prices for mutual funds
- **Search order**: Custom config → current directory → data directory

### Output Format
- CSV format: `Symbol,Price,Date`
- Precision: 4 decimal places for prices
- Date format: `MM/DD/YYYY`
- Output directory: `%LOCALAPPDATA%\PriceToCSV\` (Windows)

### Windows Integration
- **MSIX/frozen**: Uses Windows known folder API for data directory
- **Console visibility**: Auto-hides console for non-interactive mode
- **Task scheduling**: Recommended for daily downloads at 4:20 PM ET

### Yahoo Finance API
- **Endpoint**: `https://query1.finance.yahoo.com/v8/finance/chart/{symbol}`
- **Parameters**: `interval=1d`, `period1`, `period2`, `events=adjclose`
- **Rate limiting**: Handle HTTP errors gracefully
- **Data**: Adjusted close prices only

## Architecture Notes

- **Single-file design**: All functionality in one Python script
- **Standard library only**: No external dependencies for portability
- **Config-driven**: All user settings in JSON configuration
- **Cross-platform**: Works on Windows, macOS, Linux (with Python)
- **Windows-focused**: MSIX support and Task Scheduler integration

## Testing Strategy

- **Unit tests**: Test individual functions (symbol conversion, config loading)
- **Integration tests**: Test full download flow with mock API responses
- **CLI tests**: Test command-line argument parsing and behavior
- **Configuration tests**: Test config file loading and validation

## Deployment Notes

- **Standalone executable**: Built with PyInstaller for Windows
- **Microsoft Store**: Auto-updates and no SmartScreen warnings
- **ZIP release**: Standalone `.exe` with no Python required
- **Python version**: Compatible with Python 3.9+

## Common Issues

- **Rate limiting**: Yahoo Finance may return HTTP 429
- **Symbol not found**: Verify ticker symbols are valid
- **Date range**: Historical data limited by Yahoo Finance availability
- **Windows permissions**: Ensure write access to data directory

## Performance Considerations

- **API calls**: One per symbol, cached results for same day
- **Memory usage**: Minimal, processes one symbol at a time
- **File I/O**: Efficient CSV writing with buffering
- **Network**: Timeouts and retries for robustness

## CI/CD and Releases
- **GitLab CI** (`.gitlab-ci.yml`): builds EXE and creates GitLab release on `vX.X.X` tags
- **GitHub Actions** (`build_exe.yml`): mirrors via GitLab push mirror, triggers on same tags
- **Tagging**: `git tag vX.X.X && git push origin vX.X.X` triggers both pipelines
- **`version.txt`**: PyInstaller version file, patched automatically by CI from the tag

## VBScript Integration
- **`ImportPrices.vbs`**: automates Quicken price and currency import via SendKeys
- Requires Quicken 2007–2013, launched via custom Quicken toolbar button
- Setup instructions in `QUICKEN_SETUP.md`