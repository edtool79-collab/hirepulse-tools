# Moving from SerpApi Google Ads Transparency to hirepulse/google-ads-transparency-scraper

> Field mapping from SerpApi's Google Ads Transparency Center API to the hirepulse Google Ads Transparency Scraper on Apify, before/after Python code, and an honest price comparison with dates.

This page is for teams that call SerpApi's Google Ads Transparency Center API (`engine=google_ads_transparency_center`) and want to compare it with the [Google Ads Transparency Scraper](https://apify.com/hirepulse/google-ads-transparency-scraper) on Apify. The field names and date formats are **not** the same, so this page maps every field and says plainly what we do not return.

SerpApi facts on this page were checked on **October 16, 2026** on [serpapi.com/google-ads-transparency-center-api](https://serpapi.com/google-ads-transparency-center-api) and [serpapi.com/pricing](https://serpapi.com/pricing). Prices and fields can change, so check those pages before you decide.

## What is different

| | SerpApi Google Ads Transparency Center API | hirepulse Google Ads Transparency Scraper |
| --- | --- | --- |
| Input | `advertiser_id`, or `text` (often a domain) | `domains`, for example `nike.com`. No advertiser ID needed |
| Ads per request | `num` (default 40), then `next_page_token` | Up to 120 most recent ads per domain (`max_ads_per_domain`, default 40) |
| Dates | `first_shown`, `last_shown` as Unix timestamps | `first_shown`, `last_shown` as ISO 8601 text, plus `days_running` and `last_shown_days_ago` |
| One row per domain | Not a built-in mode | `mode: "summary"`: does the domain advertise, how many ads, formats, latest ad |
| Monitoring | Your own code | `only_new_ads`: returns only ads that earlier runs did not return |
| Billing | Monthly plan with a number of searches | $0.005 per domain checked + $0.0015 per ad returned. Summary mode: $0.005 per domain only |

## Field mapping

Example values come from a real run of the hirepulse tool (nike.com, text ad).

| SerpApi field | hirepulse field | Example value (real run) | Notes |
| --- | --- | --- | --- |
| `advertiser_id` | `advertiser_id` | | Same meaning |
| `advertiser` | `advertiser_name` | "Nike, Inc." | |
| none | `advertiser_verified` | true | Extra field |
| `ad_creative_id` | `ad_id` | | Same meaning |
| `format` | `format` | "text" | text, image or video |
| `first_shown` | `first_shown` | "2023-11-16T21:51:37Z" | **ISO 8601 text, not a Unix timestamp** |
| `last_shown` | `last_shown` | "2026-10-14T15:10:53Z" | Same note |
| `total_days_shown` | `days_running` | 1062 | Closest field. We count days from first to last shown; compare a few rows before you rely on it |
| `details_link` | `transparency_url` | | Link to the ad in the Ads Transparency Center |
| `image` | `preview_image_url` | | For text and image ads. Some video and HTML ads come with `preview_url` instead |
| `width`, `height` | none | | Not returned |
| none | `domain`, `last_shown_days_ago`, `country`, `platform` | | Extra fields |

Neither tool can give spend or impression numbers: Google does not publish them for commercial ads.

## Code before and after

Before (SerpApi):

```python
import requests

params = {
    "engine": "google_ads_transparency_center",
    "text": "nike.com",
    "api_key": "YOUR_SERPAPI_KEY",
}
data = requests.get("https://serpapi.com/search", params=params, timeout=60).json()

for ad in data.get("ad_creatives", []):
    print(ad["advertiser"], ad["format"], ad["first_shown"], ad["last_shown"], ad["details_link"])
```

After (hirepulse on Apify):

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("hirepulse/google-ads-transparency-scraper").call(run_input={
    "domains": ["nike.com"],
    "country": "US",
    "max_ads_per_domain": 40,
})

for ad in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(ad["advertiser_name"], ad["format"], ad["first_shown"], ad["last_shown"], ad["transparency_url"])
```

If your code stores Unix timestamps, convert the dates:

```python
from datetime import datetime

def to_unix(value):
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())
```

## Price comparison

SerpApi plans (checked October 16, 2026): Free $0 for 250 searches per month, Starter $25 for 1,000, Developer $75 for 5,000, Production $150 for 15,000. Cached, errored and failed searches are not counted. The examples below assume **one** SerpApi search per domain, which is the best case for SerpApi (looking up an advertiser first, or paging past `num`, adds searches).

hirepulse: $0.005 per domain checked + $0.0015 per ad returned. Summary mode: $0.005 per domain. No monthly plan. Higher Apify plans get volume discounts, not counted here.

| Use per month | SerpApi (smallest plan that covers it) | hirepulse cost |
| --- | --- | --- |
| 100 domains, 40 ads each | 100 searches: Free ($0) | 100 × ($0.005 + 40 × $0.0015) = **$6.50** |
| 800 domain checks, 40 ads each (200 competitors, weekly) | 800 searches: Starter ($25) | 800 × $0.065 = **$52.00** |
| 800 domain checks, summary only ("do they advertise, how many ads?") | 800 searches: Starter ($25) | 800 × $0.005 = **$4.00** |

**Honest reading:** if you need the full list of ads for many domains every week, a SerpApi plan used near its limit costs less than we do. hirepulse costs less when one row per domain is enough (summary mode), when you only want ads that are new since the last run, or when your usage is irregular and a monthly plan would go unused. For small volumes, SerpApi's free plan costs nothing.

## When to stay on SerpApi

- You need creative `width` and `height`, or SerpApi's political-ads options.
- You check the full ad list of many domains every week and use most of your plan.
- You need SerpApi's other search engines under the same plan.

Source page: https://edtool79-collab.github.io/hirepulse-tools/migrate/serpapi-google-ads-transparency/
