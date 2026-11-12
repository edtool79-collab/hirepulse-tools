# Export AliExpress search results to Excel or CSV (no code, or API)

> Export AliExpress search results to a spreadsheet without coding: product title, price in your currency, original price and discount, rating, units sold, image and product link. 60 products per page. Also as JSON for Python, n8n and AI agents.

## What you get

- Any search query, sorted results, 60 products per page
- Choose ship-to country and currency
- Price, original price, discount %, rating, exact sold count, image gallery and product link
- Shipping indicators: free shipping, delivery estimate, and origin country
- SKU ID for exact listing variant match
- Flags sponsored listings
- Plain HTTP with automatic proxy fallback, so runs are fast and cheap

## New in version 1.1.7 (12 November 2026)

Three optional inputs. None of them adds a charge.

**Compare the same product across countries.** Add `"compare_countries": ["GB", "AU", "DE"]` (up to 10 codes). Each product gets a `country_comparison` object with its listing price in every country where the same product appeared in the search results, the cheapest country and the price spread. In a live run on 12 November 2026 with "yoga mat", 14 of 30 US products were also found in GB, AU or DE. A product missing from another country's results is listed under `not_in_results`; that does not mean it cannot be bought there.

**Track price and sales changes between runs.** Add `"track_changes": true` and run the same search again later, for example on a daily schedule. Each product gets a `changes` object: previous price, price change, units sold since the previous run and whether it is new in the results. The first run only records the baseline. AliExpress shows different products from one request to the next, so use 60 or more products per search.

**Supplier match from a Shopify product link.** Give `"store_product_urls": ["https://store.com/products/product-name"]` (up to 20). The run reads the product's public title and price, searches AliExpress by the title and returns up to 5 listings with `title_similarity` and the price gap. Matching is by title text only: it does not confirm that a listing is the same product, and the gap is not profit. Branded or unique products usually return "no close match" and are not charged.

Every product also has `sold_per_day` (units sold divided by days since the listing date, a lifetime average) and `global_product_id` (the same product has the same ID on every country storefront).

Very low prices such as 1.09 USD can be promotional prices for new visitors. Check the product page before relying on a price.

## Export to Excel or CSV without code

1. Open https://apify.com/hirepulse/aliexpress-search-scraper, click "Try for free" and sign in (free Apify account, no credit card required).
2. In the Input tab, type your search (for example "wireless earbuds"), then click Start. The free Apify plan returns up to 100 products per run.
3. Open the Output tab, click Export and choose Excel or CSV.

Profit calculator with real sample prices: https://edtool79-collab.github.io/hirepulse-tools/dropshipping-profit-calculator/

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
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges apply only where configured. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/aliexpress-search-api/
