"""
PriceToCSV v1.2.2
Download end-of-day adjusted close prices from Yahoo Finance.
Produces Quicken-compatible CSV:  Symbol, Price, Date
Standard library only — no external dependencies.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import shutil
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

VERSION   = "1.2.2"
APP_NAME  = "PriceToCSV"
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"
_HEADERS  = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


# ── Paths ─────────────────────────────────────────────────────────────────────

def data_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    else:
        base = Path.home() / ".local" / "share"
    d = base / APP_NAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def exe_dir() -> Path:
    """Directory containing the running exe or script.
    Handles PyInstaller bundles (frozen) and plain Python execution.
    Used to locate the bundled config.json when installed via MSIX.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent   # dist/PriceToCSV.exe or MSIX install dir
    return Path(__file__).parent             # script directory when running via Python


def resolve_config(override: str | None) -> Path:
    if override:
        return Path(override)
    # 1. config.json in current working directory (standalone / Python usage)
    local = Path("config.json")
    if local.exists():
        return local
    # 2. Persistent user config in data directory
    data_path = data_dir() / "config.json"
    if data_path.exists():
        return data_path
    # 3. First run when installed via MSIX: seed from bundled config next to exe
    bundled = exe_dir() / "config.json"
    if bundled.exists() and bundled.resolve() != local.resolve():
        shutil.copy2(bundled, data_path)
    return data_path


# ── Config ────────────────────────────────────────────────────────────────────

_DEFAULT_CFG: dict = {
    "symbols": [],
    "fixed_prices": {},
    "symbol_aliases": {
        "CADEUR=X": "EUR",
        "CADUSD=X": "USD"
    }
}


def load_config(path: Path) -> dict:
    if not path.exists():
        return dict(_DEFAULT_CFG)
    try:
        with path.open(encoding="utf-8") as f:
            cfg = json.load(f)
        cfg.setdefault("symbols", [])
        cfg.setdefault("fixed_prices", {})
        cfg.setdefault("symbol_aliases", _DEFAULT_CFG["symbol_aliases"])
        return cfg
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[WARN] Cannot read config ({exc}); using defaults.")
        return dict(_DEFAULT_CFG)


def save_config(cfg: dict, path: Path) -> None:
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except OSError as exc:
        print(f"[WARN] Cannot save config: {exc}")


# ── Symbol helpers ────────────────────────────────────────────────────────────

def display_name(symbol: str, aliases: dict) -> str:
    """
    Convert internal ticker to Quicken-friendly output name:
      CADEUR=X  →  EUR   (via alias or auto: last 3 chars before =X)
      VUS.TO    →  VUS   (strip .TO suffix)
      VTI       →  VTI   (unchanged)
    """
    if symbol in aliases:
        return aliases[symbol]
    if symbol.endswith(".TO"):
        return symbol[:-3]
    if symbol.endswith("=X") and len(symbol) >= 5:
        return symbol[-5:-2]          # e.g. CADEUR=X → EUR
    return symbol


def is_forex(symbol: str) -> bool:
    return symbol.endswith("=X")


# ── Yahoo Finance ─────────────────────────────────────────────────────────────

def _get_json(url: str) -> dict | None:
    req = urllib.request.Request(url, headers=_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code} — symbol not found or rate-limited")
    except urllib.error.URLError as exc:
        print(f"Network error: {exc.reason}")
    except Exception as exc:
        print(f"Unexpected error: {exc}")
    return None


def fetch_prices(symbol: str, period1: int, period2: int) -> list[tuple[str, float]]:
    """Return list of (MM/DD/YYYY, price) for adjusted close."""
    url = (
        f"{YAHOO_URL}{symbol}"
        f"?interval=1d&period1={period1}&period2={period2}&events=adjclose"
    )
    data = _get_json(url)
    if data is None:
        return []
    try:
        result     = data["chart"]["result"][0]
        timestamps = result.get("timestamp", [])
        adj_close  = result["indicators"]["adjclose"][0]["adjclose"]
    except (KeyError, IndexError, TypeError):
        print("Unexpected API response structure")
        return []

    rows: list[tuple[str, float]] = []
    for ts, price in zip(timestamps, adj_close):
        if price is None:
            continue
        date_str = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%m/%d/%Y")
        rows.append((date_str, round(price, 4)))
    return rows


# ── Download orchestration ────────────────────────────────────────────────────

def _to_ts(date_str: str) -> int:
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())


def _fetch_sym(sym: str, p1: int, p2: int, historical: bool) -> list[tuple[str, float]] | None:
    """Fetch prices for one symbol; returns None on failure."""
    print(f"  {sym:<16}", end=" ", flush=True)
    prices = fetch_prices(sym, p1, p2)
    if not prices:
        print("— no data retrieved")
        return None
    if historical:
        print(f"{len(prices)} record(s)")
        return prices
    else:
        date_str, price = prices[-1]
        print(f"{price}  ({date_str})")
        return [prices[-1]]


def run_download(
    cfg:     dict,
    symbols: list[str] | None = None,
    start:   str | None       = None,
    end:     str | None       = None,
    out_dir: Path | None      = None,
) -> Path | None:

    out_dir  = out_dir or data_dir()
    active   = [s.upper() for s in (symbols or cfg.get("symbols", []))]
    fixed    = {k.upper(): v for k, v in cfg.get("fixed_prices", {}).items()}
    aliases  = {k.upper(): v for k, v in cfg.get("symbol_aliases", {}).items()}

    if not active and not fixed:
        print("[WARN] No symbols configured. Use option 3 in the menu or --symbols.")
        return None

    # Partition into regular tickers vs forex
    regular = [s for s in active if not is_forex(s)]
    forex   = [s for s in active if is_forex(s)]

    historical = bool(start and end)
    today_str  = datetime.today().strftime("%m/%d/%Y")

    if historical:
        p1    = _to_ts(start)
        p2    = _to_ts(end) + 86399
        label = f"{start.replace('-','')}_{end.replace('-','')}"
        print(f"Downloading historical prices  ({start} → {end})")
    else:
        now   = int(time.time())
        p1    = now - 86400 * 7
        p2    = now
        label = datetime.today().strftime("%Y%m%d")
        print(f"Downloading end-of-day prices  ({datetime.today().strftime('%Y-%m-%d')})")

    # ── Section 1: Fixed prices ───────────────────────────────────────────────
    fixed_rows: list[tuple] = []
    for sym, price in fixed.items():
        out_sym = display_name(sym, aliases)
        print(f"  {sym:<16} {round(price,4)}  (fixed)")
        fixed_rows.append((out_sym, round(price, 4), today_str))

    # ── Section 2: Regular tickers ────────────────────────────────────────────
    regular_rows: list[tuple] = []
    for sym in regular:
        if sym in fixed:
            continue
        result = _fetch_sym(sym, p1, p2, historical)
        if result is None:
            continue
        out_sym = display_name(sym, aliases)
        for date_str, price in result:
            regular_rows.append((out_sym, round(price, 4), date_str))

    # ── Section 3: Forex / exchange rates ─────────────────────────────────────
    forex_rows: list[tuple] = []
    for sym in forex:
        result = _fetch_sym(sym, p1, p2, historical)
        if result is None:
            continue
        out_sym = display_name(sym, aliases)
        for date_str, price in result:
            forex_rows.append((out_sym, round(price, 4), date_str))

    rows = fixed_rows + regular_rows + forex_rows

    if not rows:
        print("[WARN] No data to write.")
        return None

    csv_path = out_dir / f"prices_{label}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Symbol", "Price", "Date"])
        writer.writerows(rows)

    print(f"  ✓  {len(rows)} row(s) written → {csv_path}")
    return csv_path


# ── Menu helpers ──────────────────────────────────────────────────────────────

_SEP_W = 54
_SEP   = "─" * _SEP_W


def _sym_summary(syms: list[str], max_show: int = 5) -> str:
    """Compact one-line summary — show first N symbols then (+X more)."""
    if not syms:
        return "(none)"
    if len(syms) <= max_show:
        return ", ".join(syms)
    shown = ", ".join(syms[:max_show])
    return f"{shown}  (+{len(syms) - max_show} more)"


# ── Interactive menu ──────────────────────────────────────────────────────────

def menu(cfg: dict, cfg_path: Path) -> None:
    out = data_dir()

    while True:
        syms  = cfg.get("symbols", [])
        fixed = cfg.get("fixed_prices", {})

        print(f"{_SEP}")
        print(f"  PriceToCSV  v{VERSION}")
        print(_SEP)
        print(f"  Symbols : {_sym_summary(syms)}")
        print(f"  Fixed   : {', '.join(fixed) or '(none)'}")
        print(f"  Output  : {out}")
        print(_SEP)
        print("  1  Download prices (today)")
        print("  2  Download historical prices")
        print("  3  Edit symbol list")
        print("  Q  Quit")
        print(_SEP)

        choice = input("  Select: ").strip().upper()

        if choice == "1":
            run_download(cfg, out_dir=out)

        elif choice == "2":
            print()
            start = input("  Start date (YYYY-MM-DD): ").strip()
            end   = input("  End date   (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(start, "%Y-%m-%d")
                datetime.strptime(end,   "%Y-%m-%d")
            except ValueError:
                print("  [ERROR] Invalid date. Use YYYY-MM-DD.")
                continue
            if start > end:
                print("  [ERROR] Start date must be before end date.")
                continue
            run_download(cfg, start=start, end=end, out_dir=out)

        elif choice == "3":
            print(f"  Current symbols ({len(syms)}): {_sym_summary(syms, max_show=8)}")
            raw = input("  New list (comma-separated, blank to cancel): ").strip()
            if raw:
                cfg["symbols"] = [s.strip().upper() for s in raw.split(",") if s.strip()]
                save_config(cfg, cfg_path)
                print(f"  ✓  Saved {len(cfg['symbols'])} symbol(s).")

        elif choice == "Q":
            print("  Goodbye!")
            break

        else:
            print("  Invalid option. Enter 1, 2, 3 or Q.")


# ── CLI entry point ───────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        prog="PriceToCSV",
        description=(
            "Download end-of-day adjusted close prices from Yahoo Finance "
            "and export as Quicken-compatible CSV (Symbol, Price, Date)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python PriceToCSV.py                              Interactive menu
  python PriceToCSV.py --run                        Download today (config symbols)
  python PriceToCSV.py --symbols VTI VXUS VUS.TO   Download today (custom symbols)
  python PriceToCSV.py --history 2025-01-01 2025-01-31
  python PriceToCSV.py --symbols VTI --history 2025-01-01 2025-01-31
  python PriceToCSV.py --config my_config.json --run
        """,
    )
    ap.add_argument("--run",     action="store_true",
                    help="Non-interactive: download today's prices using config symbols")
    ap.add_argument("--symbols", nargs="+", metavar="SYMBOL",
                    help="Override ticker list (e.g. VTI VXUS VUS.TO)")
    ap.add_argument("--history", nargs=2, metavar=("START", "END"),
                    help="Historical range in YYYY-MM-DD format")
    ap.add_argument("--config",  metavar="FILE",
                    help="Path to a custom config.json")
    ap.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    args = ap.parse_args()

    cfg_path = resolve_config(args.config)
    cfg      = load_config(cfg_path)

    symbols  = [s.upper() for s in args.symbols] if args.symbols else None
    start    = args.history[0] if args.history else None
    end      = args.history[1] if args.history else None

    for label, val in [("--history START", start), ("--history END", end)]:
        if val:
            try:
                datetime.strptime(val, "%Y-%m-%d")
            except ValueError:
                ap.error(f"{label} must be YYYY-MM-DD, got: {val!r}")

    if args.run or args.symbols or args.history:
        run_download(cfg, symbols=symbols, start=start, end=end)
    else:
        menu(cfg, cfg_path)


if __name__ == "__main__":
    main()
