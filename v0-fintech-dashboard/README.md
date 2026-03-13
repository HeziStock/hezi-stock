# v0 Fintech Dashboard (exported)

Exported from [v0 – fintech dashboard redesign](https://v0.app/chat/fintech-dashboard-redesign-mxxuLbgGu3f).

## Run locally

Dependencies are already installed (via `npm install`). If you need to reinstall:

```bash
npm install
```

Start the dev server:

```bash
npm run dev
```

Then open **http://localhost:3000**. Use **http://localhost:3000/dashboard** for the stock dashboard (top 10, export CSV).

## Structure

- **`/`** – Landing page
- **`/dashboard`** – Stock dashboard with mock top 10, “Run scan”, and CSV export
- **`components/dashboard/`** – Header, stats, watchlist, charts, AI insights, etc.
- **`components/landing/`** – Navbar, hero, features, footer
- **`components/ui/`** – shadcn/ui components

## Integrate with HEZI STOCK backend

To wire this UI to your Flask app (`app.py`), either:

1. **Proxy**: Run Next.js on a port and have Flask proxy `/dashboard` to it, or
2. **API**: Add a REST or fetch call in the dashboard to your Flask API (e.g. `/api/top10` or existing report endpoint) and replace the mock data in `app/dashboard/page.tsx`.
