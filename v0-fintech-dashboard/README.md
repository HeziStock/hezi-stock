# v0-fintech-dashboard-redesign

This is a [Next.js](https://nextjs.org) project bootstrapped with [v0](https://v0.app).

## Built with v0

This repository is linked to a [v0](https://v0.app) project. You can continue developing by visiting the link below -- start new chats to make changes, and v0 will push commits directly to this repo. Every merge to `main` will automatically deploy.

[Continue working on v0 →](https://v0.app/chat/projects/prj_MWUjXOWJa9iZPR0RvA8nGoYHez80)

## HEZI STOCK integration

This UI is part of **HEZI STOCK**. The dashboard at `/dashboard` loads the **Top 10 recommendations** from the Flask portal API. For real data:

1. Start the Flask portal (project root): `python app.py`
2. In the portal, click **Run now** to run a scan
3. Start this app: `npm run dev` — open http://localhost:3000/dashboard to see the same 10 stocks

Optional: copy `.env.example` to `.env.local` and set `NEXT_PUBLIC_HEZI_STOCK_API` if the portal runs on another URL.

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

## Learn More

To learn more, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
- [v0 Documentation](https://v0.app/docs) - learn about v0 and how to use it.

<a href="https://v0.app/chat/api/kiro/clone/HeziStock/v0-fintech-dashboard-redesign" alt="Open in Kiro"><img src="https://pdgvvgmkdvyeydso.public.blob.vercel-storage.com/open%20in%20kiro.svg?sanitize=true" /></a>
