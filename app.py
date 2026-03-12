"""
HEZI STOCK – HTTP portal.
Dashboard, run now, settings, and report list. Run: python app.py
"""
import csv
import io
import json
import logging
import os
import threading
from pathlib import Path
from datetime import datetime
from functools import wraps

import pandas as pd

# Suppress "development server" warning when running locally
logging.getLogger("werkzeug").setLevel(logging.ERROR)

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, Response, send_file

# Project root
ROOT = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(ROOT))

from stock_fetcher import load_config, fetch_prices, fetch_market_movers
from report_generator import (
    append_to_history,
    build_insights,
    build_insights_from_movers,
    movers_to_dataframe,
    write_insight_report,
)
from recommendation import research_and_recommend

__version__ = "1.0.0"

app = Flask(__name__, static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024
CONFIG_PATH = ROOT / "config.json"

# Secret key: prefer env, then config.json, then dev default
def _get_secret_key():
    key = os.environ.get("FLASK_SECRET_KEY")
    if key:
        return key
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f).get("portal_secret_key")
    except Exception:
        pass
    return "hezi-stock-dev-secret-change-in-production"
app.secret_key = _get_secret_key()


@app.context_processor
def inject_version():
    return {"version": __version__}


def _portal_password_required():
    """True if portal is password-protected and we're not on localhost."""
    try:
        cfg = load_cfg()
        pw = cfg.get("portal_password") or os.environ.get("HEZI_STOCK_PORTAL_PASSWORD")
        if not pw or not pw.strip():
            return False
        if request.remote_addr in ("127.0.0.1", "::1", None):
            return False
        return True
    except Exception:
        return False


def _check_portal_auth():
    if not _portal_password_required():
        return True
    if session.get("portal_authenticated"):
        return True
    auth = request.authorization
    pw = (load_cfg().get("portal_password") or os.environ.get("HEZI_STOCK_PORTAL_PASSWORD") or "").strip()
    if auth and pw and auth.password == pw:
        session["portal_authenticated"] = True
        return True
    return False


def require_portal_auth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not _check_portal_auth():
            if request.authorization:
                return Response("Invalid credentials", 401, {"WWW-Authenticate": "Basic realm=\"HEZI STOCK\""})
            return Response(
                "HEZI STOCK requires password when accessed from network.",
                401,
                {"WWW-Authenticate": "Basic realm=\"HEZI STOCK\""},
            )
        return f(*args, **kwargs)
    return wrapped


@app.errorhandler(500)
def handle_500(e):
    """Catch any unhandled 500 - show simple page to avoid redirect loop."""
    logging.exception("Unhandled 500: %s", e)
    return Response(
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Error</title></head><body style='font-family:sans-serif;padding:2rem;'>"
        "<h1>Something went wrong</h1><p>Check the <b>HEZI STOCK Server</b> window for the error message.</p>"
        "<p><a href='/app'>Back to dashboard</a> · <a href='/'>Home</a></p></body></html>",
        status=200,
        mimetype="text/html; charset=utf-8",
    )


@app.before_request
def require_auth_before_request():
    try:
        if request.path.startswith("/static/"):
            return None
        if _portal_password_required() and not _check_portal_auth():
            if request.authorization:
                return Response("Invalid credentials", 401, {"WWW-Authenticate": "Basic realm=\"HEZI STOCK\""})
            return Response(
                "HEZI STOCK requires password.",
                401,
                {"WWW-Authenticate": "Basic realm=\"HEZI STOCK\""},
            )
    except Exception:
        pass
    return None


def load_cfg():
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.warning("Failed to load config: %s", e)
        return {
            "use_market_movers": True,
            "schedule": {"morning_time": "09:00", "evening_time": "18:00"},
            "symbols": [],
            "report": {"output_dir": "reports"},
            "notifications": {"desktop": True, "sound": True},
        }


def save_cfg(config: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def get_reports_dir() -> Path:
    try:
        cfg = load_cfg()
        return ROOT / (cfg.get("report") or {}).get("output_dir", "reports")
    except Exception:
        return ROOT / "reports"


def get_latest_insight():
    """Load the most recent insight_*.json from reports."""
    try:
        reports_dir = get_reports_dir()
        if not reports_dir.exists():
            return None
        jsons = sorted(reports_dir.glob("insight_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not jsons:
            return None
        with open(jsons[0], encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.warning("get_latest_insight failed: %s", e)
        return None


def list_report_files():
    """List insight and history files for the Reports page."""
    reports_dir = get_reports_dir()
    if not reports_dir.exists():
        return [], []
    insights = []
    histories = []
    for p in sorted(reports_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if p.suffix == ".json" and p.name.startswith("insight_"):
            insights.append({"name": p.name, "path": p.name, "mtime": datetime.fromtimestamp(p.stat().st_mtime)})
        elif p.suffix == ".csv" and p.name.startswith("history_"):
            histories.append({"name": p.name, "path": p.name, "mtime": datetime.fromtimestamp(p.stat().st_mtime)})
    return insights[:20], histories[:20]


def run_fetch():
    """Perform one fetch cycle (used in background thread). Uses market movers by default."""
    try:
        cfg = load_cfg()
        use_market_movers = cfg.get("use_market_movers", True)
        if use_market_movers:
            gainers, losers = fetch_market_movers()
            if not gainers and not losers:
                return
            df = movers_to_dataframe(gainers, losers)
            append_to_history(df)
            recommendation = research_and_recommend(gainers)
            insights = build_insights_from_movers(gainers, losers, recommendation=recommendation)
        else:
            symbols = cfg.get("symbols") or []
            if not symbols:
                return
            df = fetch_prices(symbols)
            if df.empty or df["price"].isna().all():
                return
            append_to_history(df)
            insights = build_insights(df)
        write_insight_report(insights)
        if cfg.get("notifications", {}).get("desktop", True):
            try:
                from plyer import notification
                notification.notify(
                    title="HEZI STOCK – Insight ready",
                    message=insights.get("summary", "Report ready.")[:200],
                    app_name="HEZI STOCK",
                    timeout=10,
                )
            except Exception:
                pass
    except Exception as e:
        logging.exception("run_fetch failed (background): %s", e)


def _normalize_rec_list(insight):
    """Return a list of 0–10 recommendations from insight (handles old single-dict or list)."""
    if not insight or not isinstance(insight, dict):
        return []
    r = insight.get("recommendation")
    if not r:
        return []
    if isinstance(r, dict) and r.get("symbol"):
        return [r]
    if isinstance(r, list):
        return [x for x in r[:10] if isinstance(x, dict) and x.get("symbol")]
    return []


def _get_previous_rec_symbols():
    """Symbols from the second-most-recent insight (for 'New' badge)."""
    try:
        reports_dir = get_reports_dir()
        if not reports_dir.exists():
            return set()
        jsons = sorted(reports_dir.glob("insight_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if len(jsons) < 2:
            return set()
        with open(jsons[1], encoding="utf-8") as f:
            prev = json.load(f)
        out = set()
        r = prev.get("recommendation")
        if isinstance(r, dict) and r.get("symbol"):
            out.add(str(r["symbol"]).upper())
        elif isinstance(r, list):
            for x in r:
                if isinstance(x, dict) and x.get("symbol"):
                    out.add(str(x["symbol"]).upper())
        return out
    except Exception:
        return set()


@app.route("/")
def index():
    """Landing page (marketing)."""
    return render_template("landing.html")


@app.route("/app")
def dashboard():
    """Main app: dashboard with recommendations and run now."""
    try:
        insight = get_latest_insight()
        if isinstance(insight, dict):
            insight.setdefault("top_gainers", [])
            insight.setdefault("top_losers", [])
            insight.setdefault("summary", "")
        else:
            insight = None
        rec_list = _normalize_rec_list(insight) if insight else []
        last_report_time = None
        if insight and insight.get("generated_at"):
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(insight["generated_at"].replace("Z", "+00:00"))
                last_report_time = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                last_report_time = str(insight.get("generated_at", ""))[:16]
        previous_symbols = _get_previous_rec_symbols()
        return render_template(
            "index.html",
            insight=insight,
            rec_list=rec_list,
            last_report_time=last_report_time,
            previous_symbols=previous_symbols,
        )
    except Exception as e:
        logging.exception("Dashboard failed")
        try:
            flash("Error loading dashboard: " + str(e), "error")
            return render_template("index.html", insight=None, rec_list=[], last_report_time=None, previous_symbols=set())
        except Exception:
            return Response(
                "<h1>Error</h1><p>Dashboard failed. Check the server console for details.</p><a href='/app'>Try again</a>",
                status=500,
                mimetype="text/html",
            )


@app.route("/run", methods=["POST"])
def run_now():
    try:
        threading.Thread(target=run_fetch, daemon=True).start()
        flash("Updating report… The page will refresh automatically when the report is ready.")
        return redirect(url_for("dashboard", run_started=1))
    except Exception as e:
        logging.exception("Run now failed: %s", e)
    try:
        flash("Run now failed. Check the server window for the error.", "error")
    except Exception:
        pass
    return redirect(url_for("dashboard"))


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        try:
            raw = request.form.get("symbols", "").strip()
            symbols = []
            for part in raw.replace(",", " ").split():
                s = part.strip().upper()
                if s and s not in symbols:
                    symbols.append(s)
            use_movers = request.form.get("use_market_movers") == "on"
            if not use_movers and not symbols:
                flash("Add at least one symbol when not using market movers.", "error")
                return redirect(url_for("settings"))
            cfg = load_cfg()
            cfg["symbols"] = symbols
            cfg["use_market_movers"] = use_movers
            cfg.setdefault("schedule", {})["morning_time"] = request.form.get("morning_time", "09:00").strip() or "09:00"
            cfg.setdefault("schedule", {})["evening_time"] = request.form.get("evening_time", "18:00").strip() or "18:00"
            cfg.setdefault("notifications", {})["desktop"] = request.form.get("notify_desktop") == "on"
            cfg.setdefault("notifications", {})["sound"] = request.form.get("notify_sound") == "on"
            portal_pw = request.form.get("portal_password", "").strip()
            if portal_pw:
                cfg["portal_password"] = portal_pw
            save_cfg(cfg)
            flash("Settings saved.")
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(str(e), "error")
    cfg = load_cfg()
    return render_template("settings.html", config=cfg, version=__version__)


@app.route("/api/config/backup")
def config_backup():
    """Download config.json as backup."""
    return send_file(
        CONFIG_PATH,
        as_attachment=True,
        download_name="hezi_stock_config.json",
        mimetype="application/json",
    )


@app.route("/settings/restore", methods=["POST"])
def config_restore():
    """Restore config from uploaded JSON file."""
    try:
        f = request.files.get("config_file")
        if not f or not f.filename:
            flash("No file selected.", "error")
            return redirect(url_for("settings"))
        data = json.load(f)
        if not isinstance(data, dict):
            flash("Invalid config file.", "error")
            return redirect(url_for("settings"))
        save_cfg(data)
        flash("Config restored. Reload the page to see updated settings.")
        return redirect(url_for("settings"))
    except json.JSONDecodeError as e:
        flash("Invalid JSON: " + str(e), "error")
        return redirect(url_for("settings"))
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("settings"))


@app.route("/reports")
def reports():
    insights, histories = list_report_files()
    return render_template("reports.html", insights=insights, histories=histories, reports_dir=get_reports_dir().name)


@app.route("/reports/<path:filename>")
def report_file(filename):
    reports_dir = get_reports_dir()
    path = reports_dir / filename
    if not path.is_file() or path.parent != reports_dir.resolve():
        return "Not found", 404
    return send_file(path, as_attachment=True, download_name=path.name)


@app.route("/api/health")
def api_health():
    """Health check: returns 200 + version."""
    return jsonify({"ok": True, "version": __version__})


@app.route("/api/latest")
def api_latest():
    """JSON for latest insight (e.g. for polling after Run now)."""
    insight = get_latest_insight()
    if insight is None:
        return jsonify({"ok": False, "insight": None})
    return jsonify({"ok": True, "insight": insight})


@app.route("/api/export/recommendations.csv")
def export_recommendations_csv():
    """Download latest recommendations as CSV."""
    insight = get_latest_insight()
    rec_list = []
    if insight and insight.get("recommendation"):
        r = insight["recommendation"]
        if isinstance(r, dict) and r.get("symbol"):
            rec_list = [r]
        elif isinstance(r, list):
            rec_list = r[:10]
    if not rec_list:
        return "No recommendations to export", 404
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["#", "Symbol", "Name", "Rating", "Price", "Change %", "Reason", "Why enter now"])
    for i, rec in enumerate(rec_list, 1):
        w.writerow([
            i,
            rec.get("symbol", ""),
            rec.get("name", ""),
            rec.get("rating", ""),
            rec.get("price", ""),
            rec.get("change_pct", ""),
            (rec.get("reason") or "")[:200],
        (rec.get("why_enter_now") or rec.get("reason") or "")[:200],
    ])
    return send_file(
        io.BytesIO(out.getvalue().encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="hezi_stock_recommendations.csv",
    )


def _history_for_symbol(symbol: str, days: int = 14):
    """Read history CSVs and return last N days of (date, price, change_pct) for symbol."""
    reports_dir = get_reports_dir()
    if not reports_dir.exists():
        return [], [], []
    rows = []
    for p in sorted(reports_dir.glob("history_*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)[:days]:
        try:
            df = pd.read_csv(p)
            if "symbol" not in df.columns:
                continue
            sub = df[df["symbol"].astype(str).str.upper() == symbol.upper()]
            for _, r in sub.iterrows():
                date = r.get("fetched_at") or r.get("run_id", "")
                if isinstance(date, str) and "T" in date:
                    date = date.split("T")[0]
                elif isinstance(date, str) and len(date) >= 10:
                    date = date[:10]
                rows.append((date, r.get("price"), r.get("change_pct")))
        except Exception:
            continue
    if not rows:
        return [], [], []
    # Dedupe by date (keep last of day)
    by_date = {}
    for d, p, c in rows:
        by_date[d] = (p, c)
    dates = sorted(by_date.keys(), reverse=True)[:days]
    dates.reverse()
    prices = [by_date[d][0] for d in dates]
    changes = [by_date[d][1] for d in dates]
    return dates, prices, changes


@app.route("/api/chart/<symbol>")
def api_chart(symbol):
    """JSON: last N days of price/change for a symbol from history CSVs."""
    days = min(30, max(5, request.args.get("days", type=int) or 10))
    dates, prices, changes = _history_for_symbol(symbol, days=days)
    return jsonify({"ok": True, "symbol": symbol.upper(), "dates": dates, "prices": prices, "changes": changes})


@app.route("/chart")
def chart_page():
    """Simple chart: pick symbol, show last N days from history."""
    insight = get_latest_insight()
    symbols = []
    if insight:
        for r in insight.get("top_gainers", []) + insight.get("top_losers", []):
            s = (r.get("symbol") or "").strip()
            if s and s not in symbols:
                symbols.append(s)
        rec = insight.get("recommendation")
        if isinstance(rec, list):
            for r in rec:
                s = (r.get("symbol") or "").strip()
                if s and s not in symbols:
                    symbols.append(s)
        elif isinstance(rec, dict) and rec.get("symbol"):
            if rec["symbol"] not in symbols:
                symbols.append(rec["symbol"])
    return render_template("chart.html", symbols=symbols)


if __name__ == "__main__":
    get_reports_dir().mkdir(parents=True, exist_ok=True)
    print("HEZI STOCK portal: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
