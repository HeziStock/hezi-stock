"""
Fetch current stock prices and basic metrics using yfinance (no API key required).
Also fetches market movers (day gainers / day losers) for "what to enter" vs "what to exit" insights.
"""
import json
from pathlib import Path
from datetime import datetime
import yfinance as yf
import pandas as pd

# How many top gainers/losers to fetch from Yahoo screener
MOVERS_COUNT = 25


def load_config():
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def fetch_prices(symbols: list[str]) -> pd.DataFrame:
    """Fetch current price and previous close for given symbols."""
    rows = []
    for sym in symbols:
        try:
            ticker = yf.Ticker(sym)
            info = ticker.info
            hist = ticker.history(period="5d")
            current = float(info.get("currentPrice") or info.get("regularMarketPrice") or 0)
            if hist.empty:
                prev_close = current
            else:
                prev_close = float(hist["Close"].iloc[-2]) if len(hist) > 1 else float(hist["Close"].iloc[-1])
            change = current - prev_close
            pct = (change / prev_close * 100) if prev_close else 0
            rows.append({
                "symbol": sym,
                "name": info.get("shortName") or sym,
                "price": round(current, 2),
                "previous_close": round(prev_close, 2),
                "change": round(change, 2),
                "change_pct": round(pct, 2),
                "volume": int(info.get("volume") or 0),
                "market_cap": info.get("marketCap"),
                "fetched_at": datetime.now().isoformat(),
            })
        except Exception as e:
            rows.append({
                "symbol": sym,
                "name": sym,
                "price": None,
                "previous_close": None,
                "change": None,
                "change_pct": None,
                "volume": None,
                "market_cap": None,
                "error": str(e),
                "fetched_at": datetime.now().isoformat(),
            })
    return pd.DataFrame(rows)


def _parse_screener_quotes(quotes: list) -> list[dict]:
    """Turn yfinance screener 'quotes' into list of dicts like build_insights expects."""
    rows = []
    for q in quotes or []:
        sym = q.get("symbol") or q.get("ticker")
        if not sym:
            continue
        name = q.get("shortName") or q.get("longName") or q.get("displayName") or sym
        price = q.get("regularMarketPrice")
        pct = q.get("regularMarketChangePercent")
        if price is None and pct is not None:
            prev = q.get("regularMarketPreviousClose")
            if prev is not None:
                price = round(prev * (1 + pct / 100), 2)
        if price is None:
            price = 0
        rows.append({
            "symbol": sym,
            "name": name,
            "price": round(float(price), 2) if price is not None else None,
            "change_pct": round(float(pct), 2) if pct is not None else None,
            "volume": int(q.get("regularMarketVolume") or 0),
        })
    return rows


def fetch_market_movers(count: int = MOVERS_COUNT, retries: int = 3) -> tuple[list[dict], list[dict]]:
    """
    Fetch day gainers and day losers from Yahoo Finance screener (real market movers).
    Returns (gainers, losers). Retries up to retries times if no data.
    """
    gainers_list, losers_list = [], []
    for attempt in range(max(1, retries)):
        try:
            gainers_raw = yf.screen("day_gainers", count=count)
            quotes = gainers_raw.get("quotes") if isinstance(gainers_raw, dict) else []
            gainers_list = _parse_screener_quotes(quotes)
        except Exception:
            gainers_list = []
        try:
            losers_raw = yf.screen("day_losers", count=count)
            quotes = losers_raw.get("quotes") if isinstance(losers_raw, dict) else []
            losers_list = _parse_screener_quotes(quotes)
        except Exception:
            losers_list = []
        if (gainers_list or losers_list):
            break
    return (gainers_list or [], losers_list or [])


if __name__ == "__main__":
    config = load_config()
    df = fetch_prices(config["symbols"])
    print(df.to_string())
