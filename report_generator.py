"""
Generate structured reports: CSV history and a summary insight report.
"""
import json
from pathlib import Path
from datetime import datetime
import pandas as pd


def load_config():
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def ensure_output_dir() -> Path:
    config = load_config()
    out = Path(__file__).parent / config["report"]["output_dir"]
    out.mkdir(parents=True, exist_ok=True)
    return out


def movers_to_dataframe(gainers: list[dict], losers: list[dict]) -> pd.DataFrame:
    """Build a DataFrame from gainers + losers for history CSV (same columns as fetch_prices)."""
    rows = []
    for r in (gainers or []) + (losers or []):
        rows.append({
            "symbol": r.get("symbol"),
            "name": r.get("name") or r.get("symbol"),
            "price": r.get("price"),
            "previous_close": r.get("price"),  # screener doesn't always give prev close
            "change_pct": r.get("change_pct"),
            "volume": r.get("volume", 0),
            "fetched_at": datetime.now().isoformat(),
        })
    return pd.DataFrame(rows)


def append_to_history(df: pd.DataFrame) -> Path:
    """Append current snapshot to daily history CSV (one row per symbol per run)."""
    out_dir = ensure_output_dir()
    ts = datetime.now()
    date_str = ts.strftime("%Y-%m-%d")
    run_id = ts.strftime("%Y%m%d_%H%M%S")
    file_path = out_dir / f"history_{date_str}.csv"
    df = df.copy()
    df["run_id"] = run_id
    df["session"] = "morning" if ts.hour < 12 else "evening"
    if file_path.exists():
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, index=False)
    return file_path


def build_insights(df: pd.DataFrame) -> dict:
    """Build a small insight summary from the current snapshot (fixed symbol list)."""
    valid = df.dropna(subset=["price", "change_pct"])
    if valid.empty:
        return {"error": "No valid data", "top_gainers": [], "top_losers": [], "summary": ""}
    sorted_df = valid.sort_values("change_pct", ascending=False)
    top_gainers = sorted_df.head(5)[["symbol", "name", "price", "change_pct"]].to_dict("records")
    top_losers = sorted_df.tail(5)[["symbol", "name", "price", "change_pct"]].to_dict("records")
    avg_change = valid["change_pct"].mean()
    summary = (
        f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M')}. "
        f"Tracked {len(valid)} stocks. "
        f"Avg daily change: {avg_change:.2f}%. "
        f"Top gainer: {top_gainers[0]['symbol']} ({top_gainers[0]['change_pct']:.2f}%). "
        f"Biggest drop: {top_losers[-1]['symbol']} ({top_losers[-1]['change_pct']:.2f}%)."
    )
    return {
        "generated_at": datetime.now().isoformat(),
        "symbols_tracked": len(valid),
        "average_change_pct": round(float(avg_change), 2),
        "top_gainers": top_gainers,
        "top_losers": top_losers,
        "summary": summary,
    }


def build_insights_from_movers(gainers: list[dict], losers: list[dict], top_n: int = 15, recommendation: list[dict] | dict | None = None) -> dict:
    """
    Build insight report from market movers (day gainers / day losers).
    recommendation = list from recommendation.research_and_recommend() (at least 5 with rating & why_enter_now).
    """
    top_gainers = [{"symbol": r["symbol"], "name": r.get("name") or r["symbol"], "price": r.get("price"), "change_pct": r.get("change_pct")} for r in (gainers or [])[:top_n]]
    top_losers = [{"symbol": r["symbol"], "name": r.get("name") or r["symbol"], "price": r.get("price"), "change_pct": r.get("change_pct")} for r in (losers or [])[:top_n]]
    g1 = top_gainers[0] if top_gainers else {}
    l1 = top_losers[0] if top_losers else {}
    g_pct = g1.get("change_pct")
    l_pct = l1.get("change_pct")
    g_str = f"{g_pct:.2f}%" if g_pct is not None else "—"
    l_str = f"{l_pct:.2f}%" if l_pct is not None else "—"
    rec_list = recommendation if isinstance(recommendation, list) else ([recommendation] if recommendation and recommendation.get("symbol") else [])
    lines = [
        f"• Session: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"• Market movers: {len(gainers or [])} gainers, {len(losers or [])} losers",
    ]
    if rec_list:
        lines.append("• 10 stocks most worth entering now (rating 1–10):")
        for r in rec_list[:10]:
            lines.append(f"  · {r.get('symbol', '—')} ({r.get('rating', '?')}/10)")
    lines.append(f"• Consider entering (top gainer): {g1.get('symbol', '—')} ({g_str})")
    lines.append(f"• Consider exiting / watch (top loser): {l1.get('symbol', '—')} ({l_str})")
    summary = "\n".join(lines)
    out = {
        "generated_at": datetime.now().isoformat(),
        "source": "market_movers",
        "symbols_tracked": len(gainers or []) + len(losers or []),
        "top_gainers": top_gainers,
        "top_losers": top_losers,
        "summary": summary,
    }
    if rec_list:
        out["recommendation"] = rec_list
    return out


def write_insight_report(insights: dict) -> Path:
    """Write insight report as JSON and a short text summary."""
    out_dir = ensure_output_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = out_dir / f"insight_{ts}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(insights, f, indent=2)
    txt_path = out_dir / f"insight_{ts}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(insights.get("summary", "No summary.") + "\n\n")
        rec_list = insights.get("recommendation")
        if isinstance(rec_list, dict):
            rec_list = [rec_list] if rec_list.get("symbol") else []
        if rec_list:
            f.write("--- 10 STOCKS MOST WORTH ENTERING NOW (rating 10 = strongest pick) ---\n\n")
            for i, rec in enumerate(rec_list[:10], 1):
                f.write(f"{i}. {rec.get('symbol')} — {rec.get('name', '')}  |  Rating: {rec.get('rating', '?')}/10\n")
                f.write(f"   Reason: {rec.get('reason', '')}\n")
                f.write(f"   Why enter now: {rec.get('why_enter_now', '')}\n")
                if rec.get("price") is not None:
                    pct = rec.get("change_pct")
                    f.write(f"   Price: ${rec['price']:.2f}" + (f" ({pct:+.2f}% today)\n" if pct is not None else "\n"))
                f.write("\n")
            f.write("(Not investment advice. Do your own research and use your broker.)\n\n")
            f.write("--- מניות להערכה שיכולות להמשיך לחזק מחר (לפי המחקר של היום) ---\n")
            f.write("On the basis of today's momentum, volume and analyst ratings, these are our top picks that could show follow-through in the next session (estimate only, not a prediction):\n\n")
            for i, rec in enumerate(rec_list[:10], 1):
                f.write(f"  {i}. {rec.get('symbol')} — {rec.get('name', '')} (דירוג {rec.get('rating', '?')}/10)\n")
                f.write(f"     {rec.get('why_enter_now', rec.get('reason', ''))}\n")
                f.write(f"     להערכתנו: פוטנציאל להמשך חיזוק מחר על בסיס הנתונים של היום.\n\n")
            f.write("(זו הערכה על בסיס מחקר, לא תחזית. השוק יכול לנוע בכיוון אחר.)\n\n")
        f.write("Consider entering (top gainers):\n")
        for r in insights.get("top_gainers", []):
            pct = r.get("change_pct")
            f.write(f"  {r.get('symbol')} {r.get('name', '')}: {pct}%\n")
        f.write("Consider exiting / watch (top losers):\n")
        for r in insights.get("top_losers", []):
            pct = r.get("change_pct")
            f.write(f"  {r.get('symbol')} {r.get('name', '')}: {pct}%\n")
    return json_path
