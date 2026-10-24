# Google Jobs API: Job Listings & Salaries JSON

> Search Google Jobs in 90+ countries. Extract job titles, company names, parsed salaries, contract types and direct apply links as clean JSON.

## What you get

- Any job search, any supported country or city
- Salary text parsed to min, max, currency and period
- Source site and apply link for each job
- Optional full job descriptions when the apply link points to a public ATS (Workday, Greenhouse, Lever, Ashby)
- No proxies or browser

## Google Jobs Scraper (`hirepulse/google-jobs-scraper`)

**Use it when:** You need Google Jobs results for a search in a country, or in one city with a radius: title, company, location, salary text (parsed to min and max when shown), contract type, posting date, source site and apply link.

**Not for:** A company's own job board (use hirepulse/ats-job-pulse). Salary is often missing.

- MCP: `https://mcp.apify.com?tools=hirepulse/google-jobs-scraper`
- Apify Store: https://apify.com/hirepulse/google-jobs-scraper
- Page: https://edtool79-collab.github.io/hirepulse-tools/google-jobs-api/
- Price: $0.005 per search that returns jobs + $0.001 per job.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `queries` | array of strings | required | Job searches, for example ["data engineer"]. |
| `country` | string | default "US" | Country code (90+ countries). |
| `location` | string | optional | A city. |
| `radius_km` | integer | optional | Radius around the location. |
| `max_jobs_per_query` | integer | default 50 |  |
| `employment_types` | array of strings | optional |  |
| `include_descriptions` | boolean | default true |  |
| `language` | string | optional |  |

Input of the test run below:

```json
{
  "queries": [
    "data engineer"
  ],
  "country": "US",
  "location": "Austin,Texas",
  "max_jobs_per_query": 10
}
```

### Output example

One record from a real test run on 2026-10-15:

```json
{
  "query": "data engineer",
  "country": "US",
  "position": 1,
  "title": "Junior Data Engineer",
  "company": "Tech Consulting",
  "company_url": null,
  "company_logo_url": "https://api.dataforseo.com/cdn/i/10151634-2796-0447-0000-ac22c4fd6890:0",
  "location": "Dallas, TX",
  "contract_type": "Full-time",
  "salary": null,
  "salary_min": null,
  "salary_max": null,
  "salary_currency": null,
  "salary_period": null,
  "posted_at": "2026-10-13 16:34:24 +00:00",
  "posted_ago": "2 days ago",
  "source": "LinkedIn",
  "apply_url": "https://www.linkedin.com/jobs/view/junior-data-engineer-at-tech-consulting-4476485669",
  "google_job_id": "uJQyr5_7_sG0aELXAAAAAA==",
  "scraped_at": "2026-10-15T16:34:29Z",
  "description": null,
  "description_source": null
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges apply only where configured. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/google-jobs-api/
