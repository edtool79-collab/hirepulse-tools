# Moving from SerpApi Google Jobs to hirepulse/google-jobs-scraper

> Field-by-field mapping from SerpApi's Google Jobs API to the hirepulse Google Jobs Scraper on Apify, before/after Python code, and an honest price comparison with dates.

This page is for teams that already call SerpApi's Google Jobs API (`engine=google_jobs`) and want to compare it with the [Google Jobs Scraper](https://apify.com/hirepulse/google-jobs-scraper) on Apify. The field names are **not** the same, so this page maps every field, shows what changes in your code, and says plainly what we do not return.

SerpApi facts on this page were checked on **October 16, 2026** on [serpapi.com/google-jobs-api](https://serpapi.com/google-jobs-api) and [serpapi.com/pricing](https://serpapi.com/pricing). Prices and fields can change, so check those pages before you decide.

## What is different

| | SerpApi Google Jobs API | hirepulse Google Jobs Scraper |
| --- | --- | --- |
| How you call it | `GET https://serpapi.com/search?engine=google_jobs` | Apify Actor `hirepulse/google-jobs-scraper` (API, Python/JS client, MCP) |
| Jobs per request | Up to 10 per page, then `next_page_token` | Up to 200 per search (`max_jobs_per_query`, default 50); paging is done for you |
| Location | `location` or `uule` | `country` (90+ countries) plus optional `location` ("City,Region") and `radius_km` |
| Salary | `detected_extensions.salary` (text) | `salary` text plus parsed `salary_min`, `salary_max`, `salary_period` and `salary_currency` when detected |
| Billing | Monthly plan with a number of searches | Pay per use: $0.005 per search that returns jobs + $0.001 per job. No subscription |

## Field mapping

Example values come from a real run of the hirepulse tool on October 15, 2026 (search "data engineer", Austin, Texas).

| SerpApi field | hirepulse field | Example value (real run) | Notes |
| --- | --- | --- | --- |
| `title` | `title` | "Junior Data Engineer" | Same meaning |
| `company_name` | `company` | "Tech Consulting" | |
| `location` | `location` | "Dallas, TX" | |
| `via` | `source` | "LinkedIn" | Name of the site that lists the job |
| `detected_extensions.posted_at` | `posted_ago` | "2 days ago" | We also give `posted_at` as a timestamp when Google shows it ("2026-10-13 16:34:24 +00:00") |
| `detected_extensions.schedule_type` | `contract_type` | "Full-time" | |
| `detected_extensions.salary` | `salary` | "73K–130K a year" | Plus `salary_min` 73000, `salary_max` 130000, `salary_period` "year". `salary_currency` can be null |
| `apply_options[].link` | `apply_url` | a LinkedIn job URL | **One** apply link per job, not a list of options |
| `thumbnail` | `company_logo_url` | an image URL | |
| `description` | `description` | | Only when the apply link is on a Workday, Greenhouse, Lever or Ashby board (`description_source` says which). Otherwise null |
| `job_id` | `google_job_id` | "uJQyr5_7_sG0aELXAAAAAA==" | **Not the same value format.** Do not use it to match records stored from SerpApi |
| `job_highlights` | none | | Not returned |
| `extensions` | none | | Not returned as a raw list |
| `detected_extensions.health_insurance`, `dental_coverage`, `paid_time_off` | none | | Not returned |
| `share_link` | none | | Not returned |
| none | `position`, `query`, `country`, `company_url`, `scraped_at` | | Extra fields |

## Code before and after

Before (SerpApi, paging 10 jobs at a time):

```python
import requests

params = {
    "engine": "google_jobs",
    "q": "data engineer",
    "location": "Austin, Texas, United States",
    "api_key": "YOUR_SERPAPI_KEY",
}
jobs = []
while len(jobs) < 50:
    data = requests.get("https://serpapi.com/search", params=params, timeout=60).json()
    jobs += data.get("jobs_results", [])
    token = data.get("serpapi_pagination", {}).get("next_page_token")
    if not token:
        break
    params["next_page_token"] = token

for job in jobs:
    print(job["title"], job["company_name"], job.get("detected_extensions", {}).get("salary"))
```

After (hirepulse on Apify, one call for up to 200 jobs):

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("hirepulse/google-jobs-scraper").call(run_input={
    "queries": ["data engineer"],
    "country": "US",
    "location": "Austin,Texas",
    "max_jobs_per_query": 50,
})

for job in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(job["title"], job["company"], job["salary"], job["salary_min"], job["salary_max"])
```

If the rest of your code expects SerpApi's shape, a small adapter keeps it working while you migrate:

```python
def to_serpapi_shape(job):
    return {
        "title": job["title"],
        "company_name": job["company"],
        "location": job["location"],
        "via": job["source"],
        "thumbnail": job["company_logo_url"],
        "description": job["description"],
        "detected_extensions": {
            "posted_at": job["posted_ago"],
            "schedule_type": job["contract_type"],
            "salary": job["salary"],
        },
        "apply_options": [{"title": job["source"], "link": job["apply_url"]}] if job["apply_url"] else [],
    }
```

## Price comparison

SerpApi plans (checked October 16, 2026): Free $0 for 250 searches per month, Starter $25 for 1,000, Developer $75 for 5,000, Production $150 for 15,000. Cached, errored and failed searches are not counted. The examples below assume every SerpApi page is full (10 jobs), which is the best case for SerpApi.

hirepulse: $0.005 per search that returns jobs + $0.001 per job. A search that finds nothing is not charged. No monthly plan. Higher Apify plans get volume discounts, not counted here.

| Jobs per month | SerpApi searches needed | Smallest SerpApi plan that covers it | hirepulse cost |
| --- | --- | --- | --- |
| 1,000 (20 searches × 50 jobs) | 100 | Free ($0) | 20 × $0.005 + 1,000 × $0.001 = **$1.10** |
| 20,000 (100 searches × 200 jobs) | 2,000 | Developer ($75) | 100 × $0.005 + 20,000 × $0.001 = **$20.50** |
| 100,000 (500 searches × 200 jobs) | 10,000 | Production ($150) | 500 × $0.005 + 100,000 × $0.001 = **$102.50** |

**Honest reading:** for small volumes, SerpApi's free plan costs nothing and we do not. Above that, the hirepulse cost follows your real usage instead of a monthly plan, and you never pay for a month you did not use. If you also use SerpApi for other Google engines, one plan may cover all of them, which this table does not show.

## When to stay on SerpApi

- You need `job_highlights`, benefits flags (health, dental, paid time off) or several apply options per job.
- You need SerpApi's other search engines under the same plan.
- Your volume fits SerpApi's free plan.

Source page: https://edtool79-collab.github.io/hirepulse-tools/migrate/serpapi-google-jobs/
