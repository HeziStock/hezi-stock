"""
Run one full cycle: fetch stocks, write history + insight report, show notification.
Use this with Windows Task Scheduler for morning and evening runs.
"""
import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from stock_fetcher import load_config, fetch_prices, fetch_market_movers
from report_generator import (
    append_to_history,
    build_insights,
    build_insights_from_movers,
    movers_to_dataframe,
    write_insight_report,
)
from recommendation import research_and_recommend


def notify_desktop(title: str, message: str, sound: bool = True):
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name="HEZI STOCK",
            timeout=10,
        )
    except Exception as e:
        print(f"Notification failed: {e}")


def main():
    config = load_config()
    do_notify = config.get("notifications", {}).get("desktop", True)
    sound = config.get("notifications", {}).get("sound", True)
    use_market_movers = config.get("use_market_movers", True)

    if use_market_movers:
        # Real market movers: what to consider entering (gainers) vs exiting (losers)
        print("Fetching market movers (day gainers & losers)...")
        gainers, losers = fetch_market_movers()
        if not gainers and not losers:
            msg = "Market movers run failed: no data received."
            print(msg)
            if do_notify:
                notify_desktop("HEZI STOCK – Error", msg, sound)
            return 1
        df = movers_to_dataframe(gainers, losers)
        append_to_history(df)
        recommendation = research_and_recommend(gainers)
        insights = build_insights_from_movers(gainers, losers, recommendation=recommendation)
    else:
        # Fixed symbol list (legacy)
        symbols = config.get("symbols") or []
        if not symbols:
            msg = "No symbols in config. Add symbols in Settings or set use_market_movers to true."
            print(msg)
            if do_notify:
                notify_desktop("HEZI STOCK – Error", msg, sound)
            return 1
        print("Fetching stock prices...")
        df = fetch_prices(symbols)
        if df.empty or df["price"].isna().all():
            msg = "Stock run failed: no data received."
            print(msg)
            if do_notify:
                notify_desktop("HEZI STOCK – Error", msg, sound)
            return 1
        append_to_history(df)
        insights = build_insights(df)

    report_path = write_insight_report(insights)
    summary = insights.get("summary", "Report ready.")
    print(summary)
    print(f"Report saved: {report_path}")
    if do_notify:
        notify_desktop("HEZI STOCK – Insight ready", summary[:200], sound)

    # Optional: price alerts
    price_map = {}
    for r in (insights.get("top_gainers") or []) + (insights.get("top_losers") or []):
        s = r.get("symbol")
        if s and r.get("price") is not None:
            price_map[str(s).upper()] = float(r["price"])
    for alert in config.get("alerts") or []:
        symbol = (alert.get("symbol") or "").strip().upper()
        if not symbol:
            continue
        threshold = alert.get("price")
        above = alert.get("above", True)
        try:
            threshold = float(threshold)
        except (TypeError, ValueError):
            continue
        current = price_map.get(symbol)
        if current is None:
            continue
        if above and current >= threshold:
            notify_desktop("HEZI STOCK – Alert", f"{symbol} reached ${threshold:.2f} (current ${current:.2f})", sound)
        elif not above and current <= threshold:
            notify_desktop("HEZI STOCK – Alert", f"{symbol} fell to ${threshold:.2f} (current ${current:.2f})", sound)

    return 0


if __name__ == "__main__":
    sys.exit(main())
