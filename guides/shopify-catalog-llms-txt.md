# Shopify catalog to llms.txt: make your store readable by AI agents

> Generate llms.txt drafts from a public Shopify or WooCommerce feed with Python: sampled product titles, pricing, variants and specs for $0.02 per report.

AI agents and shopping assistants increasingly browse stores through text indexes, not web pages. A store whose products live only in rendered HTML is invisible to them; a store that publishes a clean `llms.txt` product index is readable at a glance — like `robots.txt` and `sitemap.xml`, but for language models.

The [Store to LLMs Generator](https://edtool79-collab.github.io/hirepulse-tools/store-to-llms-generator/) samples a public Shopify or WooCommerce product feed and produces `llms.txt` drafts for owner review: product titles, pricing, variants and specs, structured as plain markdown.

## What the report contains

Input is the store URL plus a sample cap:

```json
{
  "store_url": "https://www.untuckit.com",
  "max_products": 5
}
```

One report includes `sampled_catalog`, `products_indexed`, `crawl_status`, `http_evidence`, `llms_txt` and `llms_full_txt`. The `LLMS_TXT_DRAFT` file downloads from key-value storage. Products are a sample capped at 100, not a full inventory; currency, policies and contact facts remain unknown unless observed.

A real smoke check (October 22, 2026) returned five products for Untuckit. Allbirds and Bulletproof were blocked in separate container checks — inaccessible public feeds fail honestly with diagnostics instead of partial guesses.

## Quick start with cURL

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~shopify-to-llms-generator/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "store_url": "https://www.untuckit.com",
  "max_products": 5
}'
```

## Production Python: draft and review an llms.txt for a store

```python
import os
import json
import urllib.request
from apify_client import ApifyClient

client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

store_url = "https://www.untuckit.com"

run = client.actor("hirepulse/shopify-to-llms-generator").call(
    run_input={"store_url": store_url, "max_products": 20}
)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError("Actor execution failed; check run logs.")

reports = list(client.dataset(run["defaultDatasetId"]).iterate_items())
if not reports:
    # Blocked or empty feed: diagnostics were saved to key-value OUTPUT,
    # and no dataset event was emitted (no charge). Fetch diagnostics:
    kv = client.key_value_store(run["defaultKeyValueStoreId"])
    diag = kv.get_record("OUTPUT")
    print("No catalog report; diagnostics:", str(diag)[:400])
    raise SystemExit(1)

report = reports[0]
print(f"Store: {store_url}")
print(f"Products indexed: {report.get('products_indexed')}")
print(f"Crawl status: {report.get('crawl_status')}")

# The draft lives in key-value storage for review before publishing.
kv = client.key_value_store(run["defaultKeyValueStoreId"])
draft = kv.get_record("LLMS_TXT_DRAFT")
with open("llms.txt.draft", "wb") as f:
    f.write(draft["value"])
print("Draft saved to llms.txt.draft — review, then publish to your site root.")
```

### Draft, not deployment

The Actor produces a draft for owner review. It does not write to your website, publish files, create checkouts or perform transactions — `ucp_conformant=false` and `deployed=false` are intentional and disclosed. Publishing the reviewed `llms.txt` to your site root is your step, which is exactly the right trust boundary for something AI agents will consume.

### Sampling is by design

The cap (max 100 products sampled) keeps runs fast and cheap at $0.02 per report containing at least one product — one billable dataset event per report, not per product. For an index whose job is agent discoverability, a curated sample of canonical products plus the llms.txt structure is the deliverable; regenerate it as your catalog changes rather than trying to mirror every SKU.

### Blocked feeds fail honestly

Bot-protected or password-protected stores return diagnostics with an empty dataset and no charge. If a target store is blocked, the fix is owner-side (publish an accessible feed), not scraper-side — that is the tool's stated boundary, and it keeps the workflow safe to run against stores you are authorized to access.

## Technical limitations and pricing

- **Availability & Source Boundaries:** Works from accessible public Shopify/WooCommerce storefront feeds; does not bypass bot protection or work on password-protected stores. Samples up to 100 products; currency, policies and contact facts stay unknown unless observed. No checkout, no published files, no transactions.
- **Pricing:** $0.02 per report containing at least one product. Blocked/empty feeds save diagnostics with no billable dataset item. No paid external API used.

## Next steps

- [Open Store to LLMs Generator on the Apify Store](https://apify.com/hirepulse/shopify-to-llms-generator)
- Explore parameters on the [tool documentation page](https://edtool79-collab.github.io/hirepulse-tools/store-to-llms-generator/)
- Related guide: [AI visibility audit in Python: check if AI crawlers can read your site](https://edtool79-collab.github.io/hirepulse-tools/guides/ai-visibility-audit-python/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/shopify-catalog-llms-txt/
