# AliExpress search results as JSON (Python, n8n, API)

> Get AliExpress search results as clean JSON: product title, price in your currency, original price and discount, rating, sold count, image and product URL. 60 products per page, no browser.

## What you get

- Any search query, sorted results, 60 products per page
- Choose ship-to country and currency
- Price, original price, discount %, rating, sold count, image and product link
- Flags sponsored listings
- Plain HTTP with automatic proxy fallback, so runs are fast and cheap

## AliExpress Search Scraper (`hirepulse/aliexpress-search-scraper`)

**Use it when:** You need AliExpress search results for a keyword as JSON: title, price in a chosen currency, original price, discount, rating, units sold, image and product link.

**Not for:** Store or seller names, shipping costs or delivery estimates, reviews or stock. The tool does not return them.

- MCP: `https://mcp.apify.com?tools=hirepulse/aliexpress-search-scraper`
- Apify Store: https://apify.com/hirepulse/aliexpress-search-scraper
- Page: https://edtool79-collab.github.io/hirepulse-tools/aliexpress-search-api/
- Price: $2.50 per 1,000 products. Free Apify plan: 100 products per run.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `queries` | array of strings | required | Search terms, for example ["wireless earbuds"]. |
| `max_results_per_query` | integer | default 60 | 60 products per page. |
| `sort` | string | default "best_match" | best_match, orders, price_low or price_high. |
| `currency` | string | default "USD" | For example USD, EUR, GBP or ILS. |
| `ship_to` | string | default "US" | Ship-to country code. |
| `min_price` | integer | optional | Lowest price. |
| `max_price` | integer | optional | Highest price. |

Example input:

```json
{
  "queries": [
    "wireless earbuds"
  ],
  "max_results_per_query": 120,
  "ship_to": "US",
  "currency": "USD"
}
```

### Output example

First record of a real test run (search "wireless earbuds", October 15, 2026):

```json
{
  "query": "wireless earbuds",
  "position": 1,
  "title": "TWS True Wireless Stereo Headset Touch Contro With Charging Case Wireless Earphones  In-ear Smart Earbuds  With Microphone",
  "url": "https://www.aliexpress.com/item/3256812924699567.html",
  "image_url": "https://ae-pic-a1.aliexpress-media.com/kf/Sb52dc1abf75e4777a2df3294034572d2X.jpg",
  "price": 7.89,
  "original_price": 15.78,
  "discount_percent": 50,
  "currency": "USD",
  "rating": 4.9,
  "sold": 919,
  "sold_text": "900+ sold",
  "is_sponsored": false,
  "listed_since": "2026-09-03",
  "ship_to": "US",
  "scraped_at": "2026-10-15T10:56:10Z"
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?token=<APIFY_TOKEN>` with the input as the JSON body.
- Every result is billed (pay per use, no subscription). Start with one query or domain, then scale up.

Source page: https://edtool79-collab.github.io/hirepulse-tools/aliexpress-search-api/
