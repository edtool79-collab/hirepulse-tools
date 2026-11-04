# How to scrape AliExpress search results with Python

> Get AliExpress search results as clean JSON with Python: sale prices, original reference prices, discount percentages, exact units ordered, star ratings, free shipping indicators, delivery estimates, SKU IDs, and product gallery images. No browser required, up to 60 products per page.

Start with a product question and a query you can inspect. The AliExpress Search Scraper accepts search terms, a currency and a ship-to country, then returns product search results as JSON. Keep those settings with your output when you compare listings or repeat a collection.

The [AliExpress Search Scraper](https://apify.com/hirepulse/aliexpress-search-scraper) uses plain HTTP with automatic proxy fallback and returns 60 products per page. It does not require a browser. You can inspect the real verified test sample below before running your own query.

Whether you are performing competitor price benchmarking, dropshipping product research, or e-commerce catalog audits, this guide shows you how to query AliExpress search results programmatically using Python.

---

## 1. Quickstart with Python (`apify-client`)

Install the official Apify Python SDK:

```bash
pip install apify-client
```

Run a search with a strict maximum spending cap (`max_total_charge_usd`):

```python
import os
from apify_client import ApifyClient

# Initialize client with your Apify API token
client = ApifyClient(os.environ.get("APIFY_TOKEN"))

# Prepare input: accepts 'queries', or singular 'query', 'keyword', 'search'
run_input = {
    "queries": ["yoga mat"],
    "max_results_per_query": 5,
    "sort": "best_match",
    "ship_to": "US",
    "currency": "USD"
}

# Run the Actor with a spending cap
run = client.actor("hirepulse/aliexpress-search-scraper").call(
    run_input=run_input,
    max_total_charge_usd=0.02
)

# Fetch and print verified dataset results
dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
for item in dataset_items:
    print(f"[{item.get('product_id')}] {item.get('title')[:45]}")
    print(f"  Price: ${item.get('price')} (Original: ${item.get('original_price')}) | Discount: {item.get('discount_percent')}%")
    print(f"  Rating: {item.get('rating')} | Units Ordered: {item.get('sold')}")
    shipping = item.get("shipping", {})
    print(f"  Free Shipping: {shipping.get('free_shipping')} | Delivery: {shipping.get('delivery_estimate')} | Origin: {shipping.get('ship_from')}")
    print(f"  URL: {item.get('url')}\n")
```

---

## 2. Verified Live Sample Output

The following record is an actual verified output captured during live testing on **November 4, 2026** (Run ID: `PliFGdIgFocGejhFS`):

```json
{
  "query": "yoga mat",
  "position": 1,
  "product_id": "3256806808957451",
  "sku_id": "12000061384420702",
  "title": "Yoga Mat Pilates Fitness Mat 3/4/6mm Thicknes Non Slip Yoga Cushion Travel Fitness Exercise Pad for Women Home Gym Floor Workout",
  "url": "https://www.aliexpress.com/item/3256806808957451.html",
  "image_url": "https://ae-pic-a1.aliexpress-media.com/kf/S2519edadb8104a8a914b2c6c1ff4151bZ.jpg",
  "gallery_images": [
    "https://ae-pic-a1.aliexpress-media.com/kf/S2519edadb8104a8a914b2c6c1ff4151bZ.jpg",
    "https://ae-pic-a1.aliexpress-media.com/kf/S098ef04cfd1c4366b55c986374788dfaS.jpg"
  ],
  "price": 5.19,
  "original_price": 13.81,
  "discount_percent": 62,
  "currency": "USD",
  "rating": 4.9,
  "sold": 12315,
  "sold_text": "10K+ sold",
  "shipping": {
    "free_shipping": false,
    "cost": null,
    "delivery_estimate": "Fastest delivery in 7 days",
    "ship_from": "CN"
  },
  "badge": "Dollar Express",
  "tags": [
    "Fastest delivery in 7 days",
    "Gym | Exercise",
    "Save $8.62"
  ],
  "is_sponsored": false,
  "listed_since": "2024-05-16",
  "ship_to": "US",
  "scraped_at": "2026-11-04T06:57:35Z"
}
```

---

## 3. Key Data Fields

| Field Name | Type | Description |
|---|---|---|
| `product_id` | string | Unique, stable AliExpress product identifier. |
| `sku_id` | string | Specific SKU identifier displayed on the search result card. |
| `price` | number | Current sale price in requested currency (e.g. `5.19`). |
| `original_price` | number | Reference price before discount (e.g. `13.81`). |
| `discount_percent` | integer | Calculated percentage savings (e.g. `62`). |
| `sold` | integer | Exact units ordered parsed from backend tracking or badge (e.g. `12315`). |
| `rating` | number | Average customer review rating (out of 5.0). |
| `shipping.free_shipping` | boolean | `true` if free delivery is explicitly offered. |
| `shipping.cost` | number / null | `0.0` if free shipping; `null` if checkout shipping cost varies. |
| `shipping.delivery_estimate` | string | Estimated arrival window (e.g. `"Fastest delivery in 7 days"`). |
| `shipping.ship_from` | string | Origin warehouse country code (`"CN"`, `"US"`, `"PL"`). |
| `gallery_images` | array | Up to 5 additional high-resolution product images. |
| `badge` | string | Promotional channel (e.g. `"Choice"`, `"Dollar Express"`). |

---

## 4. Transparent Economics & Pricing

- **Event Rate:** `$0.0025` per product record returned ($2.50 per 1,000 products).
- **Startup Fee:** `$0.00005` per GB RAM at run launch.
- **Fail-Safe Guarantee:** If AliExpress blocks or returns zero items, zero product result charges occur.
- **Run Duration:** Plain HTTP requests complete in 2–5 seconds per keyword page.
