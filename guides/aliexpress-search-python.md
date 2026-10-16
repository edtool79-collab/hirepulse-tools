# How to scrape AliExpress search results with Python

> Get AliExpress search results as JSON with Python: titles, prices in your currency, ratings, orders sold and links. No browser, 60 products per page.

Start with a product question and a query you can inspect. The AliExpress Search Scraper accepts search terms, a currency and a ship-to country, then returns product search results as JSON. Keep those settings with your output when you compare listings or repeat a collection.

The [AliExpress Search Scraper](https://edtool79-collab.github.io/hirepulse-tools/aliexpress-search-api/) uses plain HTTP with automatic proxy fallback and returns 60 products per page. It does not require a browser. You can inspect the real ten-product test sample on the tool page before running your own query.

Whether you are performing competitor price benchmarking, dropshipping product research, or e-commerce catalog audits, this guide shows you how to query AliExpress search results programmatically using Python and cURL.

## Data attributes extracted per product

For each matching product listing, the scraper extracts clean commercial and catalog attributes:

- **Identification & links:** The full `title`, the product `url`, the primary `image_url` and a `product_id`.
- **Pricing & discounts:** The active selling `price`, the strikethrough `original_price` and a ready-made `discount_percent`, in your selected `currency`.
- **Social proof & traction:** The listing `rating` and the number of items `sold`.
- **Listing details:** Whether the card is a sponsored placement (`is_sponsored`) and when it was listed (`listed_since`), when shown.
- **Localization:** Prices for your chosen `ship_to` country and `currency`.

## Quick start with cURL

You can execute a search run immediately with a single HTTP POST request. Replace `YOUR_APIFY_TOKEN` with your personal token:

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~aliexpress-search-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "queries": [
    "wireless earbuds"
  ],
  "max_results_per_query": 120,
  "ship_to": "US",
  "currency": "USD"
}'
```

This request queries the term `"wireless earbuds"` localized for shipping to the United States (`US`) with pricing formatted in US Dollars (`USD`), capping results at 120 products (2 pages of 60 items each).

## Building a Python product research pipeline

Using the official `apify-client` package, you can run search queries, compute product discounts, sort items by their returned sold count, and save the dataset to a structured file.

```bash
pip install apify-client
```

```python
import os
import json
from pathlib import Path
from apify_client import ApifyClient

# Initialize the Apify client
client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

# Define search parameters
run_input = {
    "queries": ["wireless earbuds"],
    "max_results_per_query": 120,
    "ship_to": "US",
    "currency": "USD"
}

# Run the Actor and wait for dataset completion
run = client.actor("hirepulse/aliexpress-search-scraper").call(run_input=run_input)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError("Actor did not complete successfully; inspect the run.")

# Iterate over returned dataset items
raw_products = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Retrieved {len(raw_products)} products from AliExpress.\n")

# Process and analyze product records
catalog = []
for p in raw_products:
    title = p.get("title", "Untitled Product")
    price = p.get("price")
    orig_price = p.get("original_price")
    rating = p.get("rating")
    sold_count = p.get("sold") or 0
    listed_discount = p.get("discount_percent")
    link = p.get("url", "")

    # Calculate discount percentage if original price is available
    discount_pct = 0
    if price and orig_price and orig_price > price:
        discount_pct = round(((orig_price - price) / orig_price) * 100, 1)

    catalog.append({
        "title": title,
        "price": price,
        "original_price": orig_price,
        "discount_pct": discount_pct,
        "rating": rating,
        "orders_sold": sold_count,
        "listed_discount_pct": listed_discount,
        "product_url": link
    })

# Sort catalog by total sales volume (descending)
sorted_catalog = sorted(catalog, key=lambda x: x["orders_sold"], reverse=True)

# Display top 5 best-selling items
print("--- Top 5 Best-Selling Listings ---")
for item in sorted_catalog[:5]:
    print(f"[{item['orders_sold']:,} sold | {item['rating']}★] {item['title'][:60]}...")
    print(f"  Price: ${item['price']} (Orig: ${item['original_price']}, -{item['discount_pct']}%)\n")

# Save processed results to JSON
Path("aliexpress_results.json").write_text(
    json.dumps(sorted_catalog, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
```

## Practical tips for e-commerce data engineering

### 1. Consistent localization settings
Keep `ship_to` and `currency` fixed when comparing runs, and record both settings beside the output. The tool returns the requested ship-to country; it does not return shipping costs or delivery estimates. Label collections with different settings separately so a reader can tell which request produced each price.

### 2. Handling missing or zero sales counts
Check the actual returned values before calculating derived metrics. Use Python's `.get()` method when reading optional fields, and preserve an absent value rather than inventing an explanation for it. Keep source values separate from your calculated discount or ranking.

### 3. Rate limiting and pagination
The tool extracts 60 products per page. Setting `max_results_per_query: 120` fetches two pages. For large catalog audits across dozens of queries, keep your batches modular (e.g., 5 to 10 queries per run) so your downstream processing can validate datasets incrementally.

## Limitations and pricing

- **Catalog scope:** This tool is an optimized search results scraper. It captures the public search-card attributes (title, price, original price, discount, rating, sold count, image and URL). It does not return seller/store names, shipping costs or delivery estimates, review text, stock levels or coupon codes.
- **Pricing:** Billed at $2.50 per 1,000 products returned (pay per result, no monthly subscription required). On the free Apify tier, you can test runs up to 100 products.

## Next steps

- [Open AliExpress Search Scraper on the Apify Store](https://apify.com/hirepulse/aliexpress-search-scraper)
- Review input schemas and options on the [tool page](https://edtool79-collab.github.io/hirepulse-tools/aliexpress-search-api/)
- Continue exploring automation pipelines: [Build an n8n data API workflow with a real JSON input](https://edtool79-collab.github.io/hirepulse-tools/guides/n8n-data-api-workflow/) or explore search demand for consumer products in [Keyword search volume API](https://edtool79-collab.github.io/hirepulse-tools/guides/keyword-search-volume-api/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/aliexpress-search-python/
