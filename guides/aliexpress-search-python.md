# How to scrape AliExpress search results with Python

## New in version 1.1.7 (12 November 2026)

Three optional inputs. None of them adds a charge.

**Compare the same product across countries.** Add `"compare_countries": ["GB", "AU", "DE"]` (up to 10 codes). Each product gets a `country_comparison` object with its listing price in every country where the same product appeared in the search results, the cheapest country and the price spread. In a live run on 12 November 2026 with "yoga mat", 14 of 30 US products were also found in GB, AU or DE. A product missing from another country's results is listed under `not_in_results`; that does not mean it cannot be bought there.

**Track price and sales changes between runs.** Add `"track_changes": true` and run the same search again later, for example on a daily schedule. Each product gets a `changes` object: previous price, price change, units sold since the previous run and whether it is new in the results. The first run only records the baseline. AliExpress shows different products from one request to the next, so use 60 or more products per search.

**Supplier match from a Shopify product link.** Give `"store_product_urls": ["https://store.com/products/product-name"]` (up to 20). The run reads the product's public title and price, searches AliExpress by the title and returns up to 5 listings with `title_similarity` and the price gap. Matching is by title text only: it does not confirm that a listing is the same product, and the gap is not profit. Branded or unique products usually return "no close match" and are not charged.

Every product also has `sold_per_day` (units sold divided by days since the listing date, a lifetime average) and `global_product_id` (the same product has the same ID on every country storefront).

Very low prices such as 1.09 USD can be promotional prices for new visitors. Check the product page before relying on a price.

## Compare listing prices in Excel

1. Open the [AliExpress Search Scraper](https://apify.com/hirepulse/aliexpress-search-scraper) and try one keyword, such as `yoga mat`, with a limit of five products.
2. Set a delivery country and currency. Review the [current event prices](https://apify.com/hirepulse/aliexpress-search-scraper/pricing) and set a total charge limit before you start.
3. Open the run's **Output** tab and export **CSV**. Compare listings collected with the same delivery country and currency. Listing prices can change and may exclude shipping and taxes.

You can inspect the [captured November 4 sample](../samples/quickstart-aliexpress-search.json) before running the Actor.

### 中文快速开始（速卖通商品比价）

打开采集工具，输入关键词（例如 `yoga mat`），首次最多取 5 条。选择收货国家和币种，运行前查看计费并设置费用上限。运行后在 Output（输出）中导出 CSV，用 Excel 比较同一收货地、同一币种的商品标价。标价可能不含运费和税费。

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
    shipping = item.get("shipping") or {}
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

Use the [live Pricing tab](https://apify.com/hirepulse/aliexpress-search-scraper/pricing) to check the start event, eligible product event rate and plan discounts. A run can still incur a start charge even if it returns no products. Check the run summary for source errors or partial results.
