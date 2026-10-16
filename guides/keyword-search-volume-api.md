# Keyword search volume API: bulk volume and CPC in Python

> Get Google search volume, CPC and competition for keywords in bulk with Python, plus keyword ideas. Pay per lookup, no SEO tool subscription.

Most keyword research in software development and marketing is not exploratory browsing; it is batch data validation. You have a list of 50 feature concepts, 200 blog topic candidates, or a catalog of products, and you need reliable monthly search volume, estimated CPC, and advertiser competition scores to prioritize roadmap items or ad campaigns.

The usual alternatives come with significant drawbacks:
- Enterprise SEO suites (Ahrefs, Semrush) require expensive monthly subscriptions often running $150 to $400+ per month for a single seat, which is wasteful if you only need occasional bulk lookups.
- Google Ads Keyword Planner is free to access but requires an active Google Ads account, returns frustratingly broad volume ranges (like "10K - 100K") unless you maintain active ad spend, and lacks a simple developer API for automation.

The [Keyword Search Volume API](https://edtool79-collab.github.io/hirepulse-tools/keyword-search-volume-api/) provides exact, programmatic Google keyword metrics on a pure pay-per-use basis. You pass a list of target phrases and a country code, and receive clean, structured JSON metrics.

## What metrics the API returns

For each submitted keyword, the API provides core search demand attributes:

- **Monthly search volume:** The average monthly Google search queries over the past 12 months.
- **Cost Per Click (CPC):** The estimated cost per click in USD for Google Ads placements.
- **Competition index:** The competitive intensity among advertisers bidding on the keyword (e.g., `LOW`, `MEDIUM`, `HIGH`).
- **Keyword ideas:** The ability to discover related long-tail search phrases from a seed term.
- **Optional AI search volume:** An emerging metric capturing search frequency across AI conversational assistants.

Because you only pay for what you query ($0.03 per lookup + $0.005 per keyword result), processing a batch of 100 keywords costs about $0.53, making programmatic research cost-effective for automated pipelines.

## Quick start with cURL

You can query search metrics using Apify's synchronous execution endpoint:

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~keyword-search-volume/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "keywords": [
    "running shoes",
    "trail running shoes"
  ],
  "country": "US"
}'
```

This request submits two seed phrases, evaluates search activity in the United States, and synchronously returns the resulting dataset items as a JSON array.

## Building a Python prioritization pipeline

Using `apify-client`, you can submit lists of keywords from your database, filter for high-value targets, and export the analysis to a local file:

```bash
pip install apify-client
```

```python
import os
import json
from pathlib import Path
from apify_client import ApifyClient

# Initialize the client
client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

# Define keywords to analyze
keywords_to_check = [
    "running shoes",
    "trail running shoes"
]

run_input = {
    "keywords": keywords_to_check,
    "country": "US"
}

# Run the keyword search volume Actor
run = client.actor("hirepulse/keyword-search-volume").call(run_input=run_input)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError(f"Actor run failed with status: {run.get('status')}")

# Iterate through dataset items
results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Retrieved metrics for {len(results)} keywords.\n")

# Process and evaluate keyword data
evaluated = []
for item in results:
    kw = item.get("keyword", "")
    vol = item.get("search_volume", 0)
    cpc = item.get("cpc_usd") or item.get("cpc", 0.0)
    competition = item.get("competition", "N/A")

    evaluated.append({
        "keyword": kw,
        "search_volume": vol,
        "cpc_usd": cpc,
        "competition": competition
    })

    print(f"Keyword: '{kw}'")
    print(f"  Monthly Volume: {vol:,} | Est. CPC: ${cpc:.2f} | Competition: {competition}\n")

# Save processed results to JSON
Path("keyword_metrics.json").write_text(
    json.dumps(evaluated, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
```

## Best practices for keyword data engineering

### 1. Batching lookups efficiently
Each lookup operation carries a base cost of $0.03, plus $0.005 per keyword with data. It is far more economical to send batches of 50 to 500 keywords in a single API call rather than calling the endpoint 500 times with one keyword each.

### 2. Differentiating search volume from traffic guarantees
Search volume measures historical query volume on Google. It indicates user demand; it does not guarantee that creating a page will capture that traffic. To estimate realistic organic traffic, combine search volume with ranking difficulty and click-through curve models.

### 3. Preserving market context
Search behavior is heavily localized. A phrase with 50,000 monthly searches in the US (`country: "US"`) may have entirely different search volumes, CPC rates, and competition in the UK (`country: "GB"`). Always store the target country code alongside the returned metrics.

## Technical limitations and pricing

- **Scope:** The API returns Google search volume, CPC, advertiser competition, and keyword ideas. It does not provide backlink counts, technical site health audits, or domain authority scores.
- **Pricing:** Billed at $0.03 per lookup + $0.005 per keyword result. The free Apify plan lets you test real metrics on the first 3 keywords of your run.

## Next steps

- [Open Keyword Search Volume on the Apify Store](https://apify.com/hirepulse/keyword-search-volume)
- View input options and schema details on the [tool page](https://edtool79-collab.github.io/hirepulse-tools/keyword-search-volume-api/)
- Compare overall website search footprints with [Domain SEO overview API](https://edtool79-collab.github.io/hirepulse-tools/guides/domain-seo-overview-python/), or connect search tools to autonomous LLMs with [Give your AI agent live data with MCP](https://edtool79-collab.github.io/hirepulse-tools/guides/ai-agent-live-data-mcp/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/keyword-search-volume-api/
