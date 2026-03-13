"""
Entry recommendations: research top gainers and recommend 5+ stocks to consider buying.
Each recommendation includes: symbol, name, reason, why_enter_now, rating 1–10, and a global_review (sector, analysts, news, metrics).
"""
import yfinance as yf

# How many top gainers to research
TOP_CANDIDATES = 20
# How many to recommend (at least 10)
MIN_RECOMMENDATIONS = 10

# Analyst recommendation key → score (higher = better for buying)
ANALYST_SCORE = {
    "strong_buy": 30,
    "buy": 25,
    "outperform": 22,
    "hold": 10,
    "underperform": 0,
    "sell": -10,
    "strong_sell": -20,
}


def _get_analyst_score(info: dict) -> tuple[float, str]:
    """Extract analyst score and label from ticker.info."""
    key = (info.get("recommendationKey") or "").lower().replace(" ", "_")
    label = info.get("averageAnalystRating") or key or "—"
    return (ANALYST_SCORE.get(key, 10), str(label))


def _get_volume_ratio(info: dict) -> float:
    """Volume today / average volume. Above 1 = more interest than usual."""
    vol = info.get("volume") or info.get("regularMarketVolume") or 0
    avg = info.get("averageVolume") or info.get("averageDailyVolume3Month") or 1
    if not avg or avg <= 0:
        return 1.0
    return (vol or 0) / avg


def _get_market_cap(info: dict) -> float:
    """Market cap in billions."""
    cap = info.get("marketCap") or 0
    return (cap or 0) / 1e9


def _score_to_rating(score: float, min_s: float, max_s: float) -> int:
    """Convert total_score to rating 1–10 (10 = best)."""
    if max_s <= min_s:
        return 5
    return max(1, min(10, round(1 + 9 * (score - min_s) / (max_s - min_s))))


def _build_why_enter_now(item: dict) -> str:
    """Short sentence: why enter this stock right now (based on research)."""
    parts = []
    pct = item.get("change_pct")
    if pct is not None:
        parts.append(f"strong momentum today (+{pct:.1f}%)")
    vr = item.get("volume_ratio")
    if vr is not None and vr > 1:
        parts.append(f"volume {vr:.1f}x average (elevated interest)")
    al = item.get("analyst_label")
    if al and al != "—":
        parts.append(f"analysts: {al}")
    if not parts:
        return "Top gainer in today's screen; consider further research in your broker."
    return " — ".join(parts) + ". Opportunity to enter on strength."


def _get_news_headlines(ticker, max_items: int = 3) -> list[str]:
    """Fetch recent news headlines for the ticker (from Yahoo Finance)."""
    try:
        news = getattr(ticker, "news", None)
        if not news:
            return []
        headlines = []
        for n in (news or [])[:max_items]:
            title = n.get("title") if isinstance(n, dict) else getattr(n, "title", None)
            if title and isinstance(title, str) and title.strip():
                headlines.append(title.strip()[:120])
        return headlines
    except Exception:
        return []


def _build_global_review(info: dict, news_headlines: list[str], change_pct: float | None, volume_ratio: float | None) -> str:
    """
    Build a short global review for the stock: sector, analysts, valuation, volume, and recent news.
    So the user has a broader picture before deciding to enter.
    """
    lines = []
    sector = info.get("sector") or info.get("industry")
    industry = info.get("industry") if not sector else None
    if sector:
        lines.append(f"Sector: {sector}." + (f" Industry: {industry}." if industry and industry != sector else ""))
    rec = (info.get("recommendationKey") or "").strip()
    target = info.get("targetMeanPrice") or info.get("targetMedianPrice")
    if rec:
        line = f"Analysts: {rec}."
        if target is not None:
            try:
                line += f" Target price ~${float(target):.1f}."
            except (TypeError, ValueError):
                pass
        lines.append(line)
    pe = info.get("trailingPE") or info.get("forwardPE")
    if pe is not None:
        try:
            lines.append(f"P/E: {float(pe):.1f}.")
        except (TypeError, ValueError):
            pass
    cap = info.get("marketCap")
    if cap is not None and cap >= 1e9:
        lines.append(f"Market cap: ${cap / 1e9:.1f}B.")
    if volume_ratio is not None and volume_ratio > 0:
        lines.append(f"Volume today: {volume_ratio:.1f}x average.")
    if change_pct is not None:
        lines.append(f"Today: {change_pct:+.1f}%.")
    if news_headlines:
        lines.append("Recent: " + news_headlines[0] + (" | " + news_headlines[1] if len(news_headlines) > 1 else ""))
    return " ".join(lines) if lines else "Data from Yahoo Finance. Check your broker for full research."


def research_and_recommend(
    gainers: list[dict],
    max_candidates: int = TOP_CANDIDATES,
    min_count: int = MIN_RECOMMENDATIONS,
    exclude_symbols: list[str] | None = None,
) -> list[dict]:
    """
    Research top gainers and return at least 5 entry recommendations.
    Each dict: symbol, name, price, change_pct, reason, why_enter_now, rating (1–10), volume_ratio, analyst_label, market_cap_b.
    exclude_symbols: symbols to never recommend (e.g. ["NVDA"] to hide from Top 10).
    """
    if not gainers:
        return []
    excluded = {str(s).strip().upper() for s in (exclude_symbols or []) if s}
    candidates = [g for g in gainers[:max_candidates] if (g.get("symbol") or "").upper() not in excluded]
    scored = []
    for g in candidates:
        sym = g.get("symbol")
        if not sym or (excluded and str(sym).upper() in excluded):
            continue
        try:
            t = yf.Ticker(sym)
            info = t.info
            change_pct = g.get("change_pct") or 0
            volume_ratio = _get_volume_ratio(info)
            analyst_score, analyst_label = _get_analyst_score(info)
            cap_b = _get_market_cap(info)
            if cap_b < 0.3:
                continue
            news_headlines = _get_news_headlines(t)
            global_review = _build_global_review(info, news_headlines, g.get("change_pct"), volume_ratio)
            momentum_pts = min(40, max(0, (change_pct or 0) * 2))
            vol_pts = min(30, volume_ratio * 15)
            total = momentum_pts + vol_pts + analyst_score
            scored.append({
                "symbol": sym,
                "name": info.get("shortName") or info.get("longName") or g.get("name") or sym,
                "price": g.get("price") or info.get("currentPrice") or info.get("regularMarketPrice"),
                "change_pct": change_pct,
                "volume_ratio": round(volume_ratio, 2),
                "analyst_label": analyst_label,
                "market_cap_b": round(cap_b, 2),
                "total_score": round(total, 1),
                "momentum_pts": round(momentum_pts, 1),
                "vol_pts": round(vol_pts, 1),
                "analyst_pts": analyst_score,
                "global_review": global_review,
            })
        except Exception:
            scored.append({
                "symbol": sym,
                "name": g.get("name") or sym,
                "price": g.get("price"),
                "change_pct": g.get("change_pct"),
                "volume_ratio": None,
                "analyst_label": "—",
                "market_cap_b": None,
                "total_score": (g.get("change_pct") or 0) * 2,
                "momentum_pts": (g.get("change_pct") or 0) * 2,
                "vol_pts": 0,
                "analyst_pts": 0,
                "global_review": "Data from Yahoo Finance. Run again for full review.",
            })

    # Sort by total_score descending; take top 10 (at least min_count)
    scored.sort(key=lambda x: x["total_score"], reverse=True)
    top = list(scored[:10])
    # If we have fewer than min_count, pad with raw gainers (momentum only)
    used_syms = {x["symbol"] for x in top}
    need = min_count - len(top)
    if need > 0:
        for g in candidates:
            if g.get("symbol") in used_syms:
                continue
            top.append({
                "symbol": g.get("symbol"),
                "name": g.get("name") or g.get("symbol"),
                "price": g.get("price"),
                "change_pct": g.get("change_pct"),
                "volume_ratio": None,
                "analyst_label": "—",
                "market_cap_b": None,
                "total_score": (g.get("change_pct") or 0) * 2,
                "momentum_pts": (g.get("change_pct") or 0) * 2,
                "vol_pts": 0,
                "analyst_pts": 0,
                "global_review": "Data from Yahoo Finance. Run again for full review.",
            })
            used_syms.add(g.get("symbol"))
            need -= 1
            if need <= 0:
                break
    if not top:
        for g in candidates[:min_count]:
            top.append({
                "symbol": g.get("symbol"),
                "name": g.get("name") or g.get("symbol"),
                "price": g.get("price"),
                "change_pct": g.get("change_pct"),
                "volume_ratio": None,
                "analyst_label": "—",
                "market_cap_b": None,
                "total_score": (g.get("change_pct") or 0) * 2,
                "momentum_pts": (g.get("change_pct") or 0) * 2,
                "vol_pts": 0,
                "analyst_pts": 0,
                "global_review": "Data from Yahoo Finance. Run again for full review.",
            })

    smin = min(x["total_score"] for x in top) if top else 0
    smax = max(x["total_score"] for x in top) if top else 1
    result = []
    for item in top:
        reason_parts = []
        reason_parts.append(f"momentum +{item.get('change_pct', 0):.1f}%")
        if item.get("volume_ratio"):
            reason_parts.append(f"volume {item['volume_ratio']:.1f}x avg")
        if item.get("analyst_label") and item.get("analyst_label") != "—":
            reason_parts.append(f"analyst: {item['analyst_label']}")
        if item.get("market_cap_b"):
            reason_parts.append(f"cap ${item['market_cap_b']:.1f}B")
        reason = " · ".join(reason_parts)
        rating = _score_to_rating(item["total_score"], smin, smax)
        why_enter_now = _build_why_enter_now(item)
        result.append({
            "symbol": item["symbol"],
            "name": item["name"],
            "price": item.get("price"),
            "change_pct": item.get("change_pct"),
            "reason": reason,
            "why_enter_now": why_enter_now,
            "rating": rating,
            "volume_ratio": item.get("volume_ratio"),
            "analyst_label": item.get("analyst_label"),
            "market_cap_b": item.get("market_cap_b"),
            "total_score": item.get("total_score"),
            "global_review": item.get("global_review") or "Data from Yahoo Finance. Check your broker for full research.",
        })
    return result
