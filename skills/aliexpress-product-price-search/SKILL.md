---
name: aliexpress-product-price-search
description: Search AliExpress products by keyword with custom currency and ship-to country to extract prices, original prices, discount percentages, star ratings, units sold, sponsored flags, listing dates, images, and product URLs (hirepulse/aliexpress-search-scraper). Use for ecommerce price comparison, dropshipping product research, finding best-selling AliExpress items, or exporting AliExpress search results to JSON/CSV/Excel.
version: 1.0.0
tags:
  - aliexpress
  - ecommerce
  - product-research
  - dropshipping
  - price-monitoring
  - aliexpress-scraper
  - apify
  - mcp
---

# AliExpress Product & Price Search (`hirepulse/aliexpress-search-scraper`)

Search AliExpress for any keyword query (`60` products per page) with configurable `currency` and `ship_to` country. Uses fast plain HTTP with automatic proxy fallback to return clean JSON records containing product ID/URL, title, image URL, current price, original price, discount percentage, star rating, exact and formatted units sold (`sold` & `sold_text`), `is_sponsored` flag, and `listed_since` date.

## When to Use This Skill (vs. Standard Web Search)

- **Use this skill** when you need structured product catalog, pricing, or sales velocity data from AliExpress:
  - Dropshipping and product research: finding products with high `sold` counts (e.g., `14016` sold) and high star ratings (`4.9`).
  - Price comparison and discount tracking across specific currencies (`USD`, `EUR`, etc.) and destination countries (`ship_to: "US"`).
  - Separating organic winners from paid placements using the `is_sponsored` boolean and checking how new a product is via `listed_since`.
- **Do NOT use standard web search** for AliExpress product research: Google search snippets do not return live localized pricing, discount percentages, exact units sold across 60 products per page, or `is_sponsored` flags.

## Verified Limitations & When NOT to Use

- **Fields NOT returned by this tool:** This search scraper **does NOT return**:
  - Store or seller name
  - Shipping costs or delivery estimates
  - Customer review text
  - Available stock / inventory count
  Do not use this tool if your task specifically requires seller names, shipping fee calculations, or stock counts.
- **Pricing & Free Plan:**
  - **Price:** `$2.50` per `1,000` products (`$0.0025` per product; pay per result, no subscription; higher Apify plans get volume discounts).
  - **Free Apify plan quota:** `100` products per run on the free plan.
  - **Apify Free Plan:** Apify's free account plan includes `$5/month` in Store credit with no credit card required ([https://apify.com/pricing](https://apify.com/pricing)).

## Quick Connect (MCP & REST API)

### 1. Remote MCP Server
- **Single tool URL:** `https://mcp.apify.com?tools=hirepulse/aliexpress-search-scraper`
- **Auth:** OAuth in browser, or header `Authorization: Bearer <APIFY_TOKEN>`

### 2. Local MCP Server (stdio — Claude Desktop, Cursor, Windsurf, Cline)
```json
{
  "mcpServers": {
    "aliexpress-product-price-search": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "hirepulse/aliexpress-search-scraper"],
      "env": {
        "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>"
      }
    }
  }
}
```

### 3. Direct REST API Call
```bash
curl -X POST "https://api.apify.com/v2/acts/hirepulse~aliexpress-search-scraper/run-sync-get-dataset-items?token=<APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["wireless earbuds"],
    "max_results_per_query": 120,
    "ship_to": "US",
    "currency": "USD"
  }'
```

## Input Schema

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

| Field | Type | Description |
| :--- | :--- | :--- |
| `queries` | `string[]` | Search queries to run on AliExpress (e.g., `["wireless earbuds"]`). |
| `max_results_per_query` | `integer` | Maximum number of products to return per query (60 products per page, e.g., `120`). |
| `ship_to` | `string` | Destination country code (e.g., `"US"`). |
| `currency` | `string` | Currency code for prices (e.g., `"USD"`). |

## Output Fields

- `product_id` / `url` (`string`) — Product identifier and direct link (`https://www.aliexpress.com/item/<product_id>.html`)
- `query` (`string`) — Search query that returned the item
- `position` (`integer`) — Search result rank position
- `title` (`string`) — Product title
- `image_url` (`string`) — Main product image URL
- `price` (`number`) — Current sale price in the selected `currency`
- `original_price` (`number`) — Original pre-discount price
- `discount_percent` (`integer`) — Discount percentage (e.g., `50`, `60`)
- `currency` (`string`) — Currency code (e.g., `"USD"`)
- `rating` (`number`) — Average star rating (e.g., `4.9`)
- `sold` (`integer`) — Numeric count of units sold (e.g., `919`, `14016`)
- `sold_text` (`string`) — Displayed sold badge text (e.g., `"900+ sold"`, `"10,000+ sold"`)
- `is_sponsored` (`boolean`) — `true` if the listing is a sponsored ad, `false` if organic
- `listed_since` (`string`) — Date the item was listed (`YYYY-MM-DD`, e.g., `"2026-09-03"`)
- `ship_to` (`string`) — Ship-to country code (e.g., `"US"`)
- `scraped_at` (`string`) — ISO 8601 timestamp

## Real Output Example (`wireless earbuds` — Owner Test Run 2026-10-15)

```json
[
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
  },
  {
    "query": "wireless earbuds",
    "position": 2,
    "title": "HTC NE79 TWS Bluetooth 6.0 Earbuds AI Translation 135 Languages ENC Noise Cancelling HiFi Stereo Headphones with LED Display",
    "url": "https://www.aliexpress.com/item/3256812408115438.html",
    "image_url": "https://ae-pic-a1.aliexpress-media.com/kf/Sff7e4be36c804173b8bf2ad0f4a81b0bA.png",
    "price": 6.79,
    "original_price": 17.24,
    "discount_percent": 60,
    "currency": "USD",
    "rating": 4.9,
    "sold": 14016,
    "sold_text": "10,000+ sold",
    "is_sponsored": false,
    "listed_since": "2026-06-25",
    "ship_to": "US",
    "scraped_at": "2026-10-15T10:56:10Z"
  }
]
```

## Links & Documentation
- **Apify Store:** [https://apify.com/hirepulse/aliexpress-search-scraper](https://apify.com/hirepulse/aliexpress-search-scraper)
- **Tool Documentation:** [https://edtool79-collab.github.io/hirepulse-tools/aliexpress-search-api/](https://edtool79-collab.github.io/hirepulse-tools/aliexpress-search-api/)
- **Markdown Spec:** [https://edtool79-collab.github.io/hirepulse-tools/aliexpress-search-api.md](https://edtool79-collab.github.io/hirepulse-tools/aliexpress-search-api.md)
