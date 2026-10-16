# Domain SEO overview API: compare estimated organic traffic

> Compare websites by estimated organic traffic, ranking keywords and traffic value with a simple API call from Python.

"How much organic search traffic does this company get?" is a fundamental question in marketing research, sales qualification, and competitive benchmarking.

When evaluating a single website, typing the URL into a web-based SEO platform works fine. But when you need to benchmark 40 competitors in a weekly dashboard, enrich 500 outbound prospect domains in Clay or HubSpot, or equip an AI agent with live market intelligence, manual lookups become a bottleneck. Furthermore, adding dedicated seats to legacy SEO suites simply to check traffic metrics costs hundreds of dollars per user each month.

The [Domain SEO Overview API](https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api/) solves this by turning domain names into structured search intelligence over a simple HTTP API. You pass target domains, and receive estimated organic search traffic, ranking keyword counts, organic traffic valuations, and organic competitor domains as clean JSON.

## Core intelligence returned per domain

For each submitted website, the API provides high-level search performance metrics:

- **Estimated organic traffic:** Algorithmic monthly visit estimates derived from Google search rankings and keyword click-through curves.
- **Ranking keyword volume:** The total number of organic search queries for which the domain ranks in Google's top 100 positions.
- **Traffic value:** The estimated financial value of the domain's organic search traffic, calculated against equivalent Google Ads CPC bidding costs.
- **Top ranking keywords:** The specific search queries driving the largest share of the domain's organic traffic.
- **Organic competitors:** Other websites competing for the same search keywords, along with the degree of shared keyword overlap.

## Quick start with cURL

You can query a domain overview synchronously via Apify's API endpoint:

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~domain-seo-overview/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "domains": [
    "notion.so"
  ],
  "country": "US"
}'
```

This request inspects `notion.so` within the US search index, returning structured traffic estimates and ranking metrics directly in the HTTP response.

## Building a Python prospect enrichment script

Using `apify-client`, you can enrich a list of domains and rank them by organic search footprint:

```bash
pip install apify-client
```

```python
import os
import json
from pathlib import Path
from apify_client import ApifyClient

# Initialize the client with your Apify token
client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

# Define target domains for evaluation
target_domains = ["notion.so"]

run_input = {
    "domains": target_domains,
    "country": "US"
}

# Call the Domain SEO Overview Actor synchronously
run = client.actor("hirepulse/domain-seo-overview").call(run_input=run_input)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError(f"Actor failed with status: {run.get('status')}")

# Retrieve the dataset records
overview_records = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Retrieved overview data for {len(overview_records)} domain(s).\n")

# Process and format the search metrics
enriched_companies = []
for record in overview_records:
    domain = record.get("domain", "Unknown")
    traffic = record.get("organic_traffic_estimate", 0)
    keywords = record.get("organic_keywords", 0)
    traffic_val = record.get("organic_traffic_value_usd", 0)
    competitors = record.get("competitor_domains", [])

    enriched_companies.append({
        "domain": domain,
        "est_monthly_traffic": traffic,
        "ranking_keywords": keywords,
        "traffic_value_usd": traffic_val,
        "top_competitors": competitors
    })

    print(f"Domain: {domain}")
    print(f"  Est. Organic Traffic: {traffic:,} visits/mo")
    print(f"  Ranking Keywords: {keywords:,}")
    if traffic_val:
        print(f"  Est. Traffic Value: ${traffic_val:,.2f}")
    if competitors:
        print(f"  Competitors: {', '.join(competitors[:4])}")
    print()

# Save enriched data
Path("seo_enrichment.json").write_text(
    json.dumps(enriched_companies, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
```

## Engineering considerations: estimates vs. server logs

When integrating SEO metrics into customer dashboards or sales scoring models, keep these technical principles in mind:

### 1. Organic traffic is an algorithmic estimate
Search volume APIs estimate traffic by combining observed search ranking positions with statistical click-through rate (CTR) curves. They do not measure direct server visits or private Google Analytics pageviews. Use these metrics for relative benchmarking (e.g., "Competitor A has 5x the search footprint of Competitor B"), not as an exact accounting of web traffic.

### 2. Traffic value reflects advertising equivalency
The "traffic value" metric represents what an advertiser would expect to pay in Google Ads clicks to generate the equivalent volume of traffic for those same keywords. It is a benchmark of search commerciality, not the website's revenue.

### 3. Combining domain overviews with keyword lookups
A domain overview reveals *how much* search visibility a site commands and identifies its organic rivals. To analyze specific search queries and CPCs in detail, pipe the domain's top keywords into the [Keyword Search Volume API](https://edtool79-collab.github.io/hirepulse-tools/keyword-search-volume-api/).

## Limitations and pricing

- **Scope:** Provides estimated organic traffic, ranking keyword volumes, traffic valuation, and organic competitors. It does not provide backlink graphs, server log monitoring, or on-page technical SEO audits.
- **Pricing:** Pay per result on the Apify Store (see the tool page for current rates).

## Next steps

- [Open Domain SEO Overview on the Apify Store](https://apify.com/hirepulse/domain-seo-overview)
- Review full input documentation on the [tool page](https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api/)
- For individual keyword volumes and CPC analysis, see [Keyword search volume API](https://edtool79-collab.github.io/hirepulse-tools/guides/keyword-search-volume-api/), or combine SEO data with hiring and advertising intelligence in [Hiring signals for sales](https://edtool79-collab.github.io/hirepulse-tools/guides/hiring-signals-for-sales/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/domain-seo-overview-python/
