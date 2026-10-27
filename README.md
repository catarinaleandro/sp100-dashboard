# Hundred — S&P 100 Explorer

An accessible, responsive dashboard with individual company charts, price returns (1M, 3M, 6M, YTD and 1Y), sector filters, rankings, breadth, an OEF benchmark and filtered CSV export.

## Run locally

Requires Node 22 or later. No package installation or API key is required.

```sh
npm run dev
```

Open http://127.0.0.1:3000. Run calculation checks with `npm test`.

## Deploy to Vercel

Import this repository, use Other for the framework and `public` for the output directory. No build or install command is needed. The `api/market.js` function runs on Vercel's Node runtime. Configuration is in `vercel.json`.

## Data and methodology

- Holdings and ETF weights: official iShares OEF CSV dated October 26, 2026, linked in `public/companies.json`. Equity holdings proxy the S&P 100 universe. The 100 companies comprise 101 securities because Alphabet has two share classes. Weights are ETF weights, not asserted official index weights.
- Prices: Yahoo Finance daily historical close, fetched into `public/snapshot.json`. Each series stores its own source and price date. Download time is distinct from price time.
- The current New York calendar day is excluded to avoid presenting a partial trading session as a completed daily close. Thus updates on a trading day show the previous trading day's close; the latest session becomes eligible the next calendar day.
- Returns are closing-price returns, excluding dividends and fees, using Yahoo's close series (rather than dividend-adjusted close). Corporate actions follow the provider's close-series treatment.
- YTD starts at the final available close of the previous calendar year. Other periods use the last close on or before the calendar boundary. Missing historical coverage displays unavailable.
- OEF is the ETF benchmark, not the official S&P 100 index level.
- Rankings initially share the saved snapshot. Refreshing a company updates that company only; the interface labels it as refreshed. Refresh does not imply every security or the benchmark refreshed.
- The public Yahoo endpoint can be rate limited or change. Errors preserve the dated saved snapshot; no simulated prices or returns are used. A licensed market-data provider is appropriate for commercial redistribution or guaranteed availability.

Refresh the price snapshot with `npm run refresh` (Python 3.9+, curl, network access), then commit and deploy. This updates prices for the retained holdings list; review the latest official holdings export separately when membership changes.

## Project structure

`public/`: interface, constituent snapshot and historical prices. `api/market.js`: allowlisted same-origin refresh endpoint with timeout and Vercel caching. `scripts/refresh.py`: historical snapshot downloader. `metrics.test.js`: return calculation checks. No secrets are stored in this repository.
