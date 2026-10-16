# How to see every Google ad a competitor runs

> See every Google ad a competitor runs from just their domain: creative images, text copies and active dates. Python, cURL and alerts.

If you do competitive intelligence, performance marketing, or sales research, Google's Ads Transparency Center is one of the most valuable public data sources on the internet. It indexes every ad running across Google Search, YouTube, Google Shopping, Maps, and the Display Network, along with the first and last dates each creative was seen.

The friction is collecting that data at scale. Opening Google's web UI, manually searching for an advertiser, solving bot challenges, and copy-pasting creative links is manageable for one company. When you need to monitor 50 competitors every week, evaluate 200 prospective accounts before sales calls, or feed live ad creative into an AI agent, manual lookup falls apart.

The [Google Ads Transparency Scraper](https://edtool79-collab.github.io/hirepulse-tools/google-ads-transparency-api/) solves this by taking plain company domains—like `nike.com` or `adidas.com`—and returning structured JSON over a direct HTTP API. There are no headless browsers to configure, no proxy pools to manage, and no need to hunt down obscure Google advertiser IDs.

## What the API provides

The scraper queries the Ads Transparency backend and returns structured ad records directly into your code. Each record includes:

- **Advertiser identity:** The verified company name, advertiser ID, and verification status.
- **Creative format:** Whether the ad is `text`, `image`, or `video`.
- **Active lifespan:** Precise `first_shown` and `last_shown` ISO timestamps, plus computed `days_running`.
- **Visual assets:** Direct URLs to preview images hosted on Google's content servers.
- **Audit trail:** Direct links back to the original creative in Google's Ads Transparency Center.

The tool supports two execution modes depending on your pipeline:
1. `ads` mode: Returns individual creative records—ideal for creative swipe files, messaging analysis, and detecting new marketing campaigns.
2. `summary` mode: Returns a single aggregated row per domain—reporting whether the domain advertises, total ad count, and format breakdowns (text vs. image vs. video). This is built for rapid CRM enrichment, lead scoring, and Clay tables.

Additionally, the scraper features an `only_new_ads: true` flag. When you run recurring weekly or daily jobs, it checks against historical state and returns only newly detected ad creatives.

## Quick start with cURL

You can query the scraper using Apify's synchronous execution endpoint. Replace `YOUR_APIFY_TOKEN` with your personal API token from your Apify account settings.

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~google-ads-transparency-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "domains": [
    "nike.com"
  ],
  "country": "US",
  "max_ads_per_domain": 40,
  "mode": "ads"
}'
```

This request submits `nike.com`, targets the US market, caps results at 40 creatives, and requests detailed ad records. The synchronous endpoint holds the HTTP connection open until execution completes and streams back the resulting dataset items as a JSON array.

## Inspecting real ad records

Here is a verified record returned from an actual test run for `nike.com`:

```json
{
  "domain": "nike.com",
  "advertiser_name": "Nike, Inc.",
  "advertiser_verified": true,
  "format": "text",
  "first_shown": "2023-11-16T21:51:37Z",
  "last_shown": "2026-10-14T15:10:53Z",
  "days_running": 1062
}
```

Notice the `days_running` calculation. A text ad running continuously for 1,062 days represents an evergreen high-converting core asset for the advertiser. When tracking competitors, isolating long-running creatives reveals the positioning and value propositions that consistently generate profitable conversions.

### High-level domain summaries

If you are scoring hundreds of accounts, pulling 40 creatives per domain generates unnecessary payload overhead. Setting `"mode": "summary"` yields high-level intelligence in a single row:

In a real test run for `adidas.com`, summary mode returned:
- Total ads detected: 6,000 ads
- Sample distribution: 33 text ads, 3 image ads, 4 video ads

This compact summary lets your sales automation or lead qualification script instantly categorize whether a target company is an active paid search advertiser.

## Building a Python monitoring pipeline

Using the official `apify-client` package, you can query multiple competitors in parallel and parse their creatives directly into Python data structures:

```bash
pip install apify-client
```

```python
import os
import json
from apify_client import ApifyClient

# Initialize client with your Apify API token
client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

# Define target competitor domains
run_input = {
    "domains": ["nike.com"],
    "country": "US",
    "max_ads_per_domain": 40,
    "mode": "ads"
}

# Execute the Actor and wait for completion
run = client.actor("hirepulse/google-ads-transparency-scraper").call(run_input=run_input)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError(f"Actor run failed with status: {run.get('status')}")

# Fetch the resulting dataset items
dataset_items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

print(f"Retrieved {len(dataset_items)} ads for analysis.\n")

for item in dataset_items:
    domain = item.get("domain")
    advertiser = item.get("advertiser_name")
    ad_format = item.get("format")
    days = item.get("days_running", 0)
    first_seen = item.get("first_shown", "N/A")
    
    print(f"[{domain}] {ad_format.upper()} ad by {advertiser}")
    print(f"  Running for {days} days (first seen: {first_seen})")
```

### Uncovering affiliate and agency entities

One unique advantage of domain-based lookup is entity transparency. Google associates ads with the destination domain, not just the parent holding company. When running competitor audits, you will often find ads pointing to your competitor's domain purchased by third-party affiliates, digital agencies, or subsidiary entities. Tracking these advertiser names provides visibility into external distribution channels and affiliate partner networks.

## Automated weekly monitoring in n8n

For ongoing surveillance, you can schedule an automated alert in n8n without writing custom server infrastructure:

1. **Schedule Trigger:** Set a cron trigger to fire every Monday at 08:00 AM.
2. **HTTP Request Node:** Configure a `POST` request to the Apify synchronous dataset endpoint with `only_new_ads: true`:
   ```json
   {
     "domains": ["competitor1.com", "competitor2.com"],
     "country": "US",
     "only_new_ads": true,
     "max_ads_per_domain": 20,
     "mode": "ads"
   }
   ```
3. **Filter Node:** Filter items where `ad_id` or `format` exists (filtering out status notices when no new ads appeared).
4. **Slack / Discord Node:** Post new creative alerts with format, advertiser name, and the Google Transparency Center link straight to your growth team's channel.

## Technical limitations and boundaries

Understanding the scope of public transparency data ensures you build dependable pipelines:

- **No private financial metrics:** Google Ads Transparency Center is a public accountability repository, not a financial audit. It exposes active creative assets, verification state, and publication date spans. It does not publish private bidding information, total ad spend, impressions, CPC, or conversion numbers.
- **Platform coverage:** The tool captures search, video, and display creatives served through Google. It does not index Meta Ads, LinkedIn Ads, or TikTok Ads.
- **Pay-per-use pricing:** Usage is billed at $0.005 per domain checked plus $0.0015 per ad returned. The free Apify plan supports testing 1 domain with up to 5 ads.

## Next steps

Explore the live tool and technical specifications:

- [Open Google Ads Transparency Scraper on the Apify Store](https://apify.com/hirepulse/google-ads-transparency-scraper)
- Review full parameters on the [tool documentation page](https://edtool79-collab.github.io/hirepulse-tools/google-ads-transparency-api/)
- Continue reading: [Build an n8n data API workflow with a real JSON input](https://edtool79-collab.github.io/hirepulse-tools/guides/n8n-data-api-workflow/) or explore multi-signal account intelligence in [Hiring signals for sales](https://edtool79-collab.github.io/hirepulse-tools/guides/hiring-signals-for-sales/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/competitor-google-ads/
