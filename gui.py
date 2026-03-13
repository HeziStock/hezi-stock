"""
HEZI STOCK – desktop GUI.
Professional, user-friendly interface for market insights.
"""
import json
import sys
import threading
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd

# Project root on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from stock_fetcher import load_config, fetch_prices, fetch_market_movers, fetch_extended_movers
from report_generator import (
    append_to_history,
    build_insights,
    build_insights_from_movers,
    movers_to_dataframe,
    write_insight_report,
)
from recommendation import research_and_recommend

CONFIG_PATH = Path(__file__).parent / "config.json"
APP_NAME = "HEZI STOCK"
TAGLINE = "Market insights · What to enter, what to exit"


def load_cfg():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_cfg(config: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


class StockTrackerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME}  —  {TAGLINE}")
        self.root.minsize(840, 640)
        self.root.geometry("980x700")
        self.root.configure(bg="#e8ecf1")

        self._colors = {
            "bg": "#e8ecf1",
            "card_bg": "#ffffff",
            "header_bg": "#0f172a",
            "header_fg": "#ffffff",
            "header_tagline": "#94a3b8",
            "accent": "#4a9eff",
            "accent_hover": "#2563eb",
            "gain": "#059669",
            "loss": "#dc2626",
            "muted": "#64748b",
            "text": "#1e293b",
            "border": "#e2e8f0",
        }
        self._style()
        self._build_ui()
        self._load_settings_into_ui()
        self.last_insight = None
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _style(self):
        style = ttk.Style()
        if self.root.tk.call("tk", "windowingsystem") == "win32":
            style.theme_use("vista")
        # Primary button
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(20, 12),
        )
        style.map("Accent.TButton", background=[("active", self._colors["accent_hover"])])
        # Card / frame
        style.configure(
            "Card.TFrame",
            background=self._colors["card_bg"],
        )
        style.configure(
            "Card.TLabelframe",
            background=self._colors["card_bg"],
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=self._colors["card_bg"],
            foreground=self._colors["text"],
            font=("Segoe UI", 10, "bold"),
        )
        # Treeview
        style.configure(
            "Custom.Treeview",
            font=("Segoe UI", 10),
            rowheight=28,
            fieldbackground=self._colors["card_bg"],
        )
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 10, "bold"), foreground=self._colors["muted"])
        style.map("Custom.Treeview", background=[("selected", "#dbeafe")])

    def _build_ui(self):
        main = tk.Frame(self.root, bg=self._colors["bg"], padx=20, pady=16)
        main.pack(fill=tk.BOTH, expand=True)

        # ----- Header -----
        header = tk.Frame(main, bg=self._colors["header_bg"], height=76, pady=18, padx=24)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header,
            text=APP_NAME,
            bg=self._colors["header_bg"],
            fg=self._colors["header_fg"],
            font=("Segoe UI", 22, "bold"),
        ).pack(side=tk.LEFT)
        tk.Label(
            header,
            text=f"  ·  {TAGLINE}",
            bg=self._colors["header_bg"],
            fg=self._colors["header_tagline"],
            font=("Segoe UI", 11),
        ).pack(side=tk.LEFT)

        # ----- Toolbar -----
        toolbar = tk.Frame(main, bg=self._colors["bg"], pady=14)
        toolbar.pack(fill=tk.X)
        self.run_btn = ttk.Button(
            toolbar,
            text="  ⟳  Update now",
            command=self._run_now,
            style="Accent.TButton",
        )
        self.run_btn.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar, text="Open reports folder", command=self._open_reports).pack(side=tk.LEFT, padx=(0, 16))
        self.status_var = tk.StringVar(value="Ready. Click \"Update now\" to load market movers.")
        status_lbl = tk.Label(
            toolbar,
            textvariable=self.status_var,
            bg=self._colors["bg"],
            fg=self._colors["muted"],
            font=("Segoe UI", 10),
        )
        status_lbl.pack(side=tk.LEFT, padx=(8, 0))

        # ----- Notebook -----
        nb = ttk.Notebook(main)
        nb.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        # --- Dashboard ---
        dash = tk.Frame(nb, bg=self._colors["bg"], padx=4, pady=8)
        nb.add(dash, text="  Dashboard  ")

        # Summary card
        sum_card = ttk.LabelFrame(dash, text="Latest insight", style="Card.TLabelframe", padding=14)
        sum_card.pack(fill=tk.X, pady=(0, 14))
        self.summary_text = scrolledtext.ScrolledText(
            sum_card,
            height=3,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=8,
            pady=8,
        )
        self.summary_text.pack(fill=tk.X)
        self.summary_text.insert(tk.END, "Click \"Update now\" to fetch the latest market movers and see what to consider entering or exiting.")
        self.summary_text.config(state=tk.DISABLED)

        # Top 5 recommendations (research-based)
        rec_card = ttk.LabelFrame(dash, text="Top 10 entry recommendations (10 = most recommended)", style="Card.TLabelframe", padding=12)
        rec_card.pack(fill=tk.X, pady=(0, 12))
        self.rec_text = scrolledtext.ScrolledText(
            rec_card,
            height=14,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
        )
        self.rec_text.pack(fill=tk.X)
        self.rec_text.insert(tk.END, "Run \"Update now\" to get 5 stock recommendations with rating 1–10 and why to enter now.")
        self.rec_text.config(state=tk.DISABLED)

        # Two columns: Gainers | Losers
        tables_row = tk.Frame(dash, bg=self._colors["bg"])
        tables_row.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        lf_gain = ttk.LabelFrame(tables_row, text="Consider entering (top gainers)", style="Card.TLabelframe", padding=10)
        lf_gain.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        self.gainers_tree = self._make_tree(lf_gain, ("Symbol", "Name", "Price", "Change %"), style_name="Custom.Treeview")

        lf_lose = ttk.LabelFrame(tables_row, text="Consider exiting / watch (top losers)", style="Card.TLabelframe", padding=10)
        lf_lose.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))
        self.losers_tree = self._make_tree(lf_lose, ("Symbol", "Name", "Price", "Change %"), style_name="Custom.Treeview")

        # Full snapshot
        all_frame = ttk.LabelFrame(dash, text="Full snapshot", style="Card.TLabelframe", padding=10)
        all_frame.pack(fill=tk.BOTH, expand=True)
        self.all_tree = self._make_tree(all_frame, ("Symbol", "Name", "Price", "Prev close", "Change %", "Volume"), style_name="Custom.Treeview")

        # --- Settings ---
        sett = tk.Frame(nb, bg=self._colors["bg"], padx=4, pady=12)
        nb.add(sett, text="  Settings  ")

        # Data source
        source_frame = ttk.LabelFrame(sett, text="Data source", style="Card.TLabelframe", padding=12)
        source_frame.pack(fill=tk.X, pady=(0, 12))
        self.use_movers_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            source_frame,
            text="Use market movers (recommended) — day gainers & losers from the market",
            variable=self.use_movers_var,
        ).pack(anchor=tk.W)
        ttk.Label(source_frame, text="If unchecked, only your custom symbol list below is used.").pack(anchor=tk.W)

        # Symbols
        sym_frame = ttk.LabelFrame(sett, text="Custom symbols (when not using market movers)", style="Card.TLabelframe", padding=12)
        sym_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        self.symbols_text = scrolledtext.ScrolledText(sym_frame, height=5, wrap=tk.WORD, font=("Consolas", 10))
        self.symbols_text.pack(fill=tk.BOTH, expand=True)
        ttk.Label(sym_frame, text="One symbol per line or comma-separated (e.g. AAPL, MSFT)").pack(anchor=tk.W)

        # Schedule
        sched_frame = ttk.LabelFrame(sett, text="Daily schedule", style="Card.TLabelframe", padding=12)
        sched_frame.pack(fill=tk.X, pady=(0, 12))
        row = ttk.Frame(sched_frame)
        row.pack(fill=tk.X)
        ttk.Label(row, text="Morning run:").pack(side=tk.LEFT, padx=(0, 8))
        self.morning_var = tk.StringVar(value="09:00")
        ttk.Entry(row, textvariable=self.morning_var, width=10).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(row, text="Evening run:").pack(side=tk.LEFT, padx=(0, 8))
        self.evening_var = tk.StringVar(value="18:00")
        ttk.Entry(row, textvariable=self.evening_var, width=10).pack(side=tk.LEFT)

        # Notifications
        notif_frame = ttk.LabelFrame(sett, text="Notifications", style="Card.TLabelframe", padding=12)
        notif_frame.pack(fill=tk.X, pady=(0, 12))
        self.notify_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(notif_frame, text="Show desktop notification when report is ready", variable=self.notify_var).pack(anchor=tk.W)
        self.sound_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(notif_frame, text="Play sound with notification", variable=self.sound_var).pack(anchor=tk.W)

        save_btn = ttk.Button(sett, text="Save settings", command=self._save_settings)
        save_btn.pack(pady=(8, 0))

    def _make_tree(self, parent, columns, style_name="Custom.Treeview"):
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(container, columns=columns, show="headings", height=6, selectmode="browse", style=style_name)
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=84, stretch=True)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb = ttk.Scrollbar(container, orient=tk.VERTICAL, command=tree.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=sb.set)
        return tree

    def _load_settings_into_ui(self):
        try:
            cfg = load_cfg()
            self.symbols_text.delete("1.0", tk.END)
            self.symbols_text.insert(tk.END, "\n".join(cfg.get("symbols", [])))
            self.use_movers_var.set(cfg.get("use_market_movers", True))
            self.morning_var.set(cfg.get("schedule", {}).get("morning_time", "09:00"))
            self.evening_var.set(cfg.get("schedule", {}).get("evening_time", "18:00"))
            self.notify_var.set(cfg.get("notifications", {}).get("desktop", True))
            self.sound_var.set(cfg.get("notifications", {}).get("sound", True))
        except Exception as e:
            messagebox.showwarning("Settings", f"Could not load config: {e}")

    def _save_settings(self):
        try:
            raw = self.symbols_text.get("1.0", tk.END).strip()
            symbols = []
            for part in raw.replace(",", " ").split():
                s = part.strip().upper()
                if s and s not in symbols:
                    symbols.append(s)
            use_movers = self.use_movers_var.get()
            if not use_movers and not symbols:
                messagebox.showwarning("Settings", "Add at least one symbol when not using market movers.")
                return
            cfg = load_cfg()
            cfg["symbols"] = symbols
            cfg["use_market_movers"] = use_movers
            cfg.setdefault("schedule", {})["morning_time"] = self.morning_var.get().strip() or "09:00"
            cfg.setdefault("schedule", {})["evening_time"] = self.evening_var.get().strip() or "18:00"
            cfg.setdefault("notifications", {})["desktop"] = self.notify_var.get()
            cfg.setdefault("notifications", {})["sound"] = self.sound_var.get()
            save_cfg(cfg)
            messagebox.showinfo("Settings", "Settings saved. Next run will use your preferences.")
        except Exception as e:
            messagebox.showerror("Settings", str(e))

    def _run_now(self):
        self.run_btn.config(state=tk.DISABLED)
        self.status_var.set("Updating… Please wait.")

        def work():
            try:
                cfg = load_cfg()
                use_market_movers = cfg.get("use_market_movers", True)
                if use_market_movers:
                    gainers, losers, entry_candidates = fetch_extended_movers()
                    df = movers_to_dataframe(gainers, losers)
                    recommendation = research_and_recommend(entry_candidates, max_candidates=50)
                    insights = build_insights_from_movers(gainers, losers, recommendation=recommendation)
                else:
                    symbols = cfg.get("symbols") or []
                    df = fetch_prices(symbols)
                    insights = build_insights(df)
                self.root.after(0, lambda: self._on_fetch_done(df, cfg, insights))
            except Exception as e:
                self.root.after(0, lambda: self._on_fetch_error(str(e)))

        threading.Thread(target=work, daemon=True).start()

    def _on_fetch_done(self, df, config, insights):
        try:
            if df.empty or (df.get("price") is not None and df["price"].isna().all()):
                self.status_var.set("No data received.")
                self.run_btn.config(state=tk.NORMAL)
                messagebox.showwarning("Update", "No data received. Check your connection or Settings.")
                return
            append_to_history(df)
            write_insight_report(insights)
            self.last_insight = insights
            summary = insights.get("summary", "Report ready.")
            if config.get("notifications", {}).get("desktop", True):
                try:
                    from plyer import notification
                    notification.notify(
                        title="HEZI STOCK – Insight ready",
                        message=summary[:200],
                        app_name=APP_NAME,
                        timeout=10,
                    )
                except Exception:
                    pass
            self._refresh_dashboard(insights, df)
            self.status_var.set(f"Updated at {datetime.now().strftime('%H:%M:%S')}  ·  Report saved.")
        except Exception as e:
            self.status_var.set("Error")
            messagebox.showerror("Update", str(e))
        finally:
            self.run_btn.config(state=tk.NORMAL)

    def _on_fetch_error(self, err: str):
        self.status_var.set("Error")
        self.run_btn.config(state=tk.NORMAL)
        messagebox.showerror("Update", err)

    def _refresh_dashboard(self, insights: dict, df):
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, insights.get("summary", "No summary."))
        self.summary_text.config(state=tk.DISABLED)

        rec_list = insights.get("recommendation")
        if isinstance(rec_list, dict):
            rec_list = [rec_list] if rec_list.get("symbol") else []
        self.rec_text.config(state=tk.NORMAL)
        self.rec_text.delete("1.0", tk.END)
        if rec_list:
            for i, rec in enumerate(rec_list[:10], 1):
                sym = rec.get("symbol", "")
                name = rec.get("name") or sym
                rating = rec.get("rating", "?")
                reason = rec.get("reason", "")
                why = rec.get("why_enter_now") or reason
                price = rec.get("price")
                pct = rec.get("change_pct")
                self.rec_text.insert(tk.END, f"{i}. Rating {rating}/10  |  {sym} — {name}\n")
                self.rec_text.insert(tk.END, f"   Reason: {reason}\n")
                self.rec_text.insert(tk.END, f"   Why enter now: {why}\n")
                if price is not None:
                    self.rec_text.insert(tk.END, f"   Price: ${price:.2f}" + (f" ({pct:+.2f}% today)\n" if pct is not None else "\n"))
                self.rec_text.insert(tk.END, "\n")
            self.rec_text.insert(tk.END, "Based on momentum, volume vs average, and analyst rating. Not investment advice. Use your broker to place the order.")
            self.rec_text.insert(tk.END, "\n\n——— Stocks to watch that could continue stronger tomorrow (today's research) ———\n")
            self.rec_text.insert(tk.END, "Based on momentum, volume and analysts — estimate only, not a forecast.\n\n")
            for i, rec in enumerate(rec_list[:10], 1):
                self.rec_text.insert(tk.END, f"  {i}. {rec.get('symbol')} — {rec.get('name') or rec.get('symbol')} (rating {rec.get('rating', '?')}/10). ")
                self.rec_text.insert(tk.END, f"{rec.get('why_enter_now') or rec.get('reason', '')}\n")
            self.rec_text.insert(tk.END, "\nThis is an estimate based on today's data. The market can move the other way.\n")
        else:
            self.rec_text.insert(tk.END, 'Run "Update now" to get up to 10 stock recommendations with rating 1–10 and why to enter now.')
        self.rec_text.config(state=tk.DISABLED)

        for tree in (self.gainers_tree, self.losers_tree, self.all_tree):
            for i in tree.get_children():
                tree.delete(i)

        for r in insights.get("top_gainers", []):
            pct = r.get("change_pct")
            pct_str = f"+{pct:.2f}%" if pct is not None else ""
            self.gainers_tree.insert("", tk.END, values=(
                r.get("symbol", ""),
                (r.get("name") or "")[:20],
                r.get("price"),
                pct_str,
            ))
        for r in insights.get("top_losers", []):
            pct = r.get("change_pct")
            pct_str = f"{pct:.2f}%" if pct is not None else ""
            self.losers_tree.insert("", tk.END, values=(
                r.get("symbol", ""),
                (r.get("name") or "")[:20],
                r.get("price"),
                pct_str,
            ))

        for _, row in df.iterrows():
            if pd.isna(row.get("price")):
                continue
            vol = row.get("volume")
            vol_str = f"{int(vol):,}" if vol is not None and not pd.isna(vol) else ""
            ch = row.get("change_pct")
            ch_str = f"{ch:+.2f}%" if ch is not None and not pd.isna(ch) else ""
            self.all_tree.insert("", tk.END, values=(
                row.get("symbol", ""),
                (str(row.get("name", "")))[:18],
                row.get("price"),
                row.get("previous_close"),
                ch_str,
                vol_str,
            ))

    def _open_reports(self):
        folder = Path(__file__).parent / "reports"
        folder.mkdir(parents=True, exist_ok=True)
        import os
        os.startfile(folder)

    def _on_close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = StockTrackerApp()
    app.run()
