# Moving from DataForSEO Keywords Data to hirepulse/keyword-search-volume

> Field mapping from DataForSEO's Google Ads keywords_data endpoints to the hirepulse Keyword Search Volume tool: task model vs pay-per-lookup, before/after Python, and an honest price comparison with dates.

This page is for teams calling DataForSEO's Keywords Data API (`keywords_data/google_ads/search_volume`) who want to compare it with the [Keyword Search Volume tool](https://apify.com/hirepulse/keyword-search-volume) on Apify. The models differ fundamentally — **per task** vs **per lookup** — so the price math depends on your batch shape, and this page does that math openly.

DataForSEO facts on this page were checked on **October 24, 2026** on [dataforseo.com/pricing/keywords-data/google-ads](https://dataforseo.com/pricing/keywords-data/google-ads) and the official docs. Prices change; re-check both pages before deciding.

## What is different

| | DataForSEO Google Ads keywords_data | hirepulse Keyword Search Volume |
| --- | --- | --- |
| Billing model | **Per task**: one task covers up to 1,000 keywords, same price for 1 or 1,000 | **Per lookup** ($0.03) + **per keyword result** ($0.005) |
| Live mode price | $0.09 per task (standard queue $0.06) | No queue model — synchronous run-sync endpoint |
| Batching | Up to 1,000 keywords in one `keywords` array | Up to 1,000 keywords per lookup ($0.03 flat per lookup call) |
| Output | Search volume, CPC, competition from Google Keyword Planner | Monthly search volume, CPC, competition, `keyword_difficulty`, `search_intent`, trend fields (monthly/quarterly/yearly), plus keyword ideas |
| Free tier | Trial balance (register) | Real volume, CPC and difficulty for the first 3 keywords of each run (availability-dependent, can be paused) |
| Auth | DataForSEO login + API password (basic auth) | Apify token |

## Which model is cheaper for you

DataForSEO wins when you fill the task: 1,000 keywords for $0.09 live ($0.06 queued) — less than $0.0001 per keyword. The Radar wins on small, frequent, agent-shaped calls:

| Shape | DataForSEO (live) | hirepulse Radar |
| --- | --- | --- |
| 20 keywords, daily check | $0.09/day → ~$2.70/month | ~$0.09/run → ~$2.70/month |
| 3 keywords, hourly (24×) | $2.16/day → ~$65/month | $0.09/run → ~$2.16/day ~ $65/month... |
| 5 keyword ideas for one seed | $0.09 | ~$0.055 |
| 1,000 keywords bulk | $0.09 | ~$5.03 |

Real example where the shape matters: an agent making an hourly 3-keyword check pays the same either way at scale, but an agent doing **one-seed keyword expansion** pays 5.5 cents vs 9 cents — and the Radar returns difficulty, intent and trend fields DataForSEO's keywords_data endpoint does not include. For pure bulk-at-1,000, DataForSEO is genuinely ~56× cheaper and this page will not pretend otherwise.

## Field mapping

| DataForSEO field (`keyword_data` result) | Radar field | Notes |
| --- | --- | --- |
| `keyword` | `keyword` | same |
| `search_volume` | `search_volume` | monthly, 12-month average |
| `competition` (0-1 float) | `competition` + `competition_level` (LOW/MEDIUM/HIGH) | Radar adds the categorical tier |
| `cpc` | `cpc_usd` | |
| — | `keyword_difficulty` | Radar-only |
| — | `search_intent` | Radar-only |
| — | `trend_monthly_pct`, `trend_quarterly_pct`, `trend_yearly_pct` | Radar-only trend deltas |
| — | keyword ideas (related phrases) | optional, in the same run |
| `location_code`, `language_code` | `country` | Radar: one country per lookup |

## Before/after Python

### Before (DataForSEO)

```python
import requests

r = requests.post(
    "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live",
    auth=(DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD),
    json=[{
        "keywords": ["running shoes", "trail running shoes"],
        "location_code": 2840,  # United States
        "language_code": "en",
    }],
)
volume_rows = r.json()["tasks"][0]["result"][0]["items"]
```

### After (hirepulse Keyword Search Volume)

```python
import os
import json
from apify_client import ApifyClient

client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

run_input = {"keywords": ["running shoes", "trail running shoes"], "country": "US"}
run = client.actor("hirepulse/keyword-search-volume").call(run_input=run_input)
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())

for row in rows:
    print(f"{row['keyword']:24s} vol={row.get('search_volume'):>9,} "
          f"cpc=${row.get('cpc_usd', 0):.2f} diff={row.get('keyword_difficulty')} intent={row.get('search_intent')}")
```

The first 3 keywords of every run return real metrics free, so a 3-keyword agent loop can run at $0.03/lookup indefinitely on the free edge — validate the field mapping exactly like the before/after blocks above before paying for anything.

## Switching checklist

1. Count your real monthly lookups and their mean keyword count; apply the table above. Bulk-at-scale stays on DataForSEO — say it plainly in your design doc.
2. Map `competition` float → `competition_level` tier (or keep the float if the Radar run returns it).
3. Decide where `keyword_difficulty` / `search_intent` / trends add value — for most content and agent pipelines they replace a second vendor call.
4. Keep the country code simple: `country: "US"` per lookup, no location/language matrices.

Source page: https://edtool79-collab.github.io/hirepulse-tools/migrate/dataforseo-keywords/
