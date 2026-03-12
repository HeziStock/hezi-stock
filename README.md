# HEZI STOCK

**Market insights** — what to consider entering vs exiting. Runs twice daily, saves structured reports, and notifies you when the insight is ready. No API key required (uses Yahoo Finance).

## What it does

- **Fetches** market movers (day gainers & losers) or your custom symbol list from Yahoo Finance.
- **Recommends** up to 10 stocks with a 1–10 rating and “why enter now” (momentum, volume, analysts).
- **Saves** history (CSV) and insight reports (JSON + TXT) in the `reports` folder.
- **Notifies** you with a desktop notification when the report is ready.
- **Web portal** — Dashboard, Run now, Settings, Reports. Optional **desktop GUI** and **single-click launcher**.

## Quick start

### 1. Install Python

Install from [python.org](https://www.python.org/downloads/) and check **“Add Python to PATH”**.

### 2. Install dependencies

In the project folder:

```bash
pip install -r requirements.txt
```

### 3. Run with one click

Double-click **`Start HEZI STOCK.bat`**.

- A window titled “HEZI STOCK Server” opens (keep it open while using the portal).
- Your browser opens automatically at **http://127.0.0.1:5000**.
- To stop: close the “HEZI STOCK Server” window.

No need to open PowerShell or type any commands.

### 4. Alternative: run from terminal

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Distribution (giving the app to others)

1. **Copy the whole project folder** (all files: `app.py`, `gui.py`, `templates`, `config.json`, `Start HEZI STOCK.bat`, etc.).
2. On the other PC: install **Python** and run **`pip install -r requirements.txt`** once in that folder.
3. Tell the user to double-click **`Start HEZI STOCK.bat`** to start the server and open the portal.

Optional: build a single **.exe** with PyInstaller (see [Building a single EXE](#building-a-single-exe) below).

## Portal

- **Dashboard** — Latest summary, entry recommendations (up to 10 with rating), “Run now” button, gainers/losers tables. Page auto-refreshes when a new report is ready.
- **Settings** — Data source (market movers vs custom symbols), symbols list, morning/evening times, notifications. Saved to `config.json`.
- **Reports** — List and download insight (JSON/TXT) and history (CSV) files.

The server listens on `0.0.0.0:5000`, so you can open it from another device on your network (e.g. `http://YOUR_PC_IP:5000`). Use **Settings** in the portal to set an optional **password** when sharing on a network. For access over the internet, run the app behind a reverse proxy (e.g. nginx) with **HTTPS** and keep the portal password enabled.

## Desktop GUI

```bash
python gui.py
```

Dashboard, “Update now”, top 10 recommendations, gainers/losers, open reports folder, and Settings (symbols, schedule, notifications).

## Run once (test)

```bash
python run_once.py
```

You get a console summary, desktop notification, and new files in `reports`.

## Automatic runs (twice a day)

See **[TASK_SCHEDULER_GUIDE.md](TASK_SCHEDULER_GUIDE.md)** for:

- **Option A** — Windows Task Scheduler (PowerShell script `setup_tasks.ps1`).
- **Option B** — Manual Task Scheduler setup.
- **Option C** — Built-in scheduler (`python run_scheduler.py`; window must stay open).

Times are set in `config.json` under `schedule.morning_time` and `schedule.evening_time`.

## Output files

- **`reports/history_YYYY-MM-DD.csv`** — Rows per symbol per run (price, change %, volume, etc.).
- **`reports/insight_*.json`** — Structured summary: recommendations, top_gainers, top_losers, summary text.
- **`reports/insight_*.txt`** — Same summary in plain text.

## Configuration

Edit **`config.json`**:

- **`use_market_movers`** — `true` = use day gainers/losers; `false` = use only `symbols` list.
- **`symbols`** — Tickers when not using market movers (e.g. `["AAPL", "MSFT"]`).
- **`schedule.morning_time`** / **`evening_time`** — e.g. `"09:00"`, `"18:00"`.
- **`notifications.desktop`** / **`sound`** — Desktop notification and sound when report is ready.
- **`portal_password`** (optional) — If set, the web portal requires this password (when not on localhost).
- **`alerts`** (optional) — List of `{ "symbol": "AAPL", "above": true, "price": 150 }` to get a notification when price crosses the threshold.

## Building a single EXE

To build a standalone executable (no Python installed on target PC):

1. Install PyInstaller: `pip install pyinstaller`
2. Run from the project folder:
   ```bash
   pyinstaller build_hezi_stock.spec
   ```
   Or use the one-line command in **BUILD_EXE.md** if you prefer not to use a spec file.

The output will be in `dist/`. Run the generated `.exe`; it starts the server. The user can then open **http://127.0.0.1:5000** in a browser (or you can bundle a batch file that runs the exe and opens the URL).

See **BUILD_EXE.md** for detailed steps and options.

## Version

HEZI STOCK version is shown in the portal footer. Check **`app.py`** for `__version__`.
