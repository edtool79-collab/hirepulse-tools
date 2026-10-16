# Google Jobs API: get job listings as JSON with Python

> Pull Google Jobs listings as JSON with Python: title, company, location, parsed salary, source and apply link, for any search and country.

Google Jobs is one of the largest job indexes on the web. It brings together postings from job boards such as LinkedIn and Indeed and from company career sites into a single search interface.

Building reliable scrapers for Google Jobs has traditionally been painful. Puppeteer or Playwright browser scrapers frequently trigger CAPTCHAs, consume excessive CPU and RAM, and fail when Google updates DOM class names. Worse, running browsers through residential proxies pushes scraping costs up to several dollars per hundred listings.

The [Google Jobs Scraper](https://edtool79-collab.github.io/hirepulse-tools/google-jobs-api/) takes a different approach: it fetches search listings directly through a high-performance backend API without headless browsers or proxy configuration. You submit search queries and receive structured JSON records with normalized salary ranges, apply URLs, and posting dates.

## What the job record contains

When you run a search, the scraper returns an array of structured job items. Each listing provides clean, typed data points:

- **Position metadata:** Job `title`, hiring `company`, and job `location` (city, state, or remote).
- **Parsed compensation:** When an employer publishes a compensation range, the tool provides both the raw salary string (e.g., `"$140K–$180K a year"`) and parsed attributes: `salary_min`, `salary_max`, `salary_currency`, and `salary_period`.
- **Employment type:** Standardized contract tags like `Full-time`, `Part-time`, `Contractor`, or `Internship`.
- **Source site and apply links:** The origin portal (e.g., `LinkedIn`, `Greenhouse`) and the direct `apply_url`.
- **Posting recency:** Relative timestamps indicating when the role was indexed (e.g., `2 days ago`).

Additionally, when an apply link points to a supported public applicant tracking system (ATS)—such as Greenhouse, Lever, Ashby, or Workday—the scraper can optionally pull the complete job description text directly from the target board.

## Quick start with cURL

You can execute a search query with a single `POST` request to Apify's synchronous dataset endpoint. Replace `YOUR_APIFY_TOKEN` with your API token.

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~google-jobs-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "queries": [
    "data engineer"
  ],
  "country": "US",
  "max_jobs_per_query": 50
}'
```

This request queries Google Jobs for `"data engineer"` roles across the United States and limits the response to the top 50 listings.

## Inspecting the JSON output

Below is the shape of a record returned by the scraper (illustrative placeholder values, real field names):

```json
{
  "query": "data engineer",
  "country": "US",
  "position": 1,
  "title": "Senior Data Engineer",
  "company": "Acme Corp",
  "location": "Austin, TX",
  "contract_type": "Full-time",
  "salary": "$140K–$180K a year",
  "salary_min": 140000,
  "salary_max": 180000,
  "salary_currency": "USD",
  "salary_period": "year",
  "posted_ago": "2 days ago",
  "source": "LinkedIn",
  "apply_url": "https://www.linkedin.com/jobs/view/..."
}
```

The parsed salary fields make numerical filtering trivial. Instead of writing complex regex patterns to parse strings like `"$140k - $180k/yr"`, you can filter directly on `salary_min >= 120000`.

## Building a Python job aggregator

With the `apify-client` package, you can query multiple titles and locations, handle optional fields gracefully, and export the dataset to JSON or CSV:

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

# Configure search parameters
run_input = {
    "queries": ["data engineer", "analytics engineer"],
    "country": "US",
    "max_jobs_per_query": 50
}

# Run the Google Jobs Actor synchronously
run = client.actor("hirepulse/google-jobs-scraper").call(run_input=run_input)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError(f"Actor failed with status: {run.get('status')}")

# Retrieve job records from the dataset
jobs = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Collected {len(jobs)} total job listings.")

# Process and format the listings
processed_jobs = []
for job in jobs:
    title = job.get("title", "Unknown Title")
    company = job.get("company", "Unknown Company")
    location = job.get("location", "Remote")
    salary_str = job.get("salary")
    min_sal = job.get("salary_min")
    max_sal = job.get("salary_max")
    apply_url = job.get("apply_url", "")

    # Format compensation display
    if min_sal and max_sal:
        comp_display = f"${min_sal:,.0f} - ${max_sal:,.0f} ({job.get('salary_period', 'yr')})"
    elif salary_str:
        comp_display = salary_str
    else:
        comp_display = "Not specified"

    processed_jobs.append({
        "title": title,
        "company": company,
        "location": location,
        "compensation": comp_display,
        "apply_url": apply_url
    })

    print(f"- {title} at {company} ({location}) | {comp_display}")

# Save clean results to a local JSON file
Path("jobs_output.json").write_text(
    json.dumps(processed_jobs, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
print("\nSaved processed listings to jobs_output.json")
```

### Handling missing salary data

In real-world job data, only a subset of employers disclose compensation upfront. In our own test run of 30 US jobs, 5 showed a salary. Expect the share to vary by role, country and local pay-transparency laws.

When consuming this API in automated workflows, always access salary fields using safe dictionary retrieval (`job.get("salary_min")`) rather than direct indexing (`job["salary_min"]`). Never replace missing salary values with arbitrary numbers or zeros; treat null as an unspecified compensation range.

## Automated digests with n8n

You can turn this scraper into a daily morning alert that writes new open roles to a Google Sheet or triggers team notifications:

1. **Schedule Node:** Trigger every morning at 07:30 AM.
2. **HTTP Request Node:** Make a POST request to Apify's `run-sync-get-dataset-items` endpoint with your target queries and location:
   ```json
   {
     "queries": ["senior python engineer"],
     "country": "US",
     "max_jobs_per_query": 25
   }
   ```
3. **Google Sheets / Notion Node:** Append each returned job row with title, company, salary, and direct application URL.
4. **Email / Slack Node:** If high-priority target companies appear in the dataset, trigger an instant alert for your recruitment or sales team.

## Limitations and pricing

- **Compensation availability:** The API extracts and parses salary text whenever it is provided by the employer or job board. It does not synthesize hypothetical salaries for postings where compensation was omitted.
- **Search-driven scope:** Google Jobs queries discover listings matching specific search phrases. If your goal is to audit every single opening at a specific company (regardless of title), use the [ATS Job Scraper](https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api/) instead, which directly crawls company career boards.
- **Pricing:** Billed at $0.005 per search that returns jobs plus $0.001 per returned job record. Searches returning zero results incur no per-job charge.

## Next steps

- [Open Google Jobs Scraper on the Apify Store](https://apify.com/hirepulse/google-jobs-scraper)
- View full API schema and parameters on the [tool page](https://edtool79-collab.github.io/hirepulse-tools/google-jobs-api/)
- For company-targeted ATS crawling, see [Greenhouse, Lever and Ashby jobs API](https://edtool79-collab.github.io/hirepulse-tools/guides/greenhouse-lever-ashby-jobs-api/), or learn how to track hiring velocity in [Hiring signals for sales](https://edtool79-collab.github.io/hirepulse-tools/guides/hiring-signals-for-sales/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/google-jobs-json-python/
