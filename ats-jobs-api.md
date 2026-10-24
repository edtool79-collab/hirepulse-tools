# ATS Jobs API: Greenhouse, Lever & Ashby Jobs

> Extract open jobs, published salary ranges and the technologies they mention from Greenhouse, Lever, Ashby, Workable, Recruitee and SmartRecruiters. Pay-per-use ATS data API.

## What you get

- Give a domain like stripe.com, the job board is found automatically
- Six ATS systems supported (not Workday)
- Department, location, remote flag, posting date and apply URL
- Only-new-jobs tracking between runs

## ATS Job Scraper (`hirepulse/ats-job-pulse`)

**Use it when:** You need every open job from a company's Greenhouse, Lever, Ashby, Workable, Recruitee or SmartRecruiters board. Pass a domain such as stripe.com or a board slug.

**Not for:** Companies on Workday or custom career sites.

- MCP: `https://mcp.apify.com?tools=hirepulse/ats-job-pulse`
- Apify Store: https://apify.com/hirepulse/ats-job-pulse
- Page: https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api/
- Price: $0.05 per company whose job board was found and processed, however many jobs it has. Companies that are not found, and failed ones, are not charged.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `companies` | array of strings | required | Company domains or board slugs, for example ["stripe.com"]. |
| `output_mode` | string | default "jobs_and_summary" | jobs_and_summary, summary_only or jobs_only. |
| `track_diff` | boolean | default true | Mark new and closed jobs between runs. |
| `only_changes` | boolean | default false | Return only changes since the last run. |
| `extract_tech_keywords` | boolean | default true | Detect technologies mentioned in job titles and descriptions. |
| `title_keywords` | array of strings | optional | Filter by words in the job title. |
| `departments` | array of strings | optional |  |
| `locations` | array of strings | optional |  |
| `technologies` | array of strings | optional |  |
| `remote_only` | boolean | default false |  |
| `max_jobs_per_company` | integer | default 0 | 0 means no limit. |

Input of the test run below:

```json
{
  "companies": [
    "linear.app",
    "ramp.com"
  ],
  "output_mode": "jobs_and_summary",
  "track_diff": false,
  "max_jobs_per_company": 5
}
```

### Output example

One record from a real test run on 2026-10-15 (long text and lists shortened):

```json
{
  "record_type": "job",
  "company_domain": "ramp.com",
  "ats_type": "ashby",
  "job_id": "34413f8d-26bf-4bbc-8ade-eb309a0e2245",
  "title": "Security Engineer, Cloud",
  "department": "Engineering",
  "location": "New York, NY (HQ)",
  "is_remote": true,
  "posted_date": "2026-04-07T17:12:35.753+00:00",
  "salary": "$211.4K - $290.6K",
  "apply_url": "https://jobs.ashbyhq.com/ramp/34413f8d-26bf-4bbc-8ade-eb309a0e2245",
  "detected_technologies": [
    "AWS",
    "Azure",
    "Flask"
  ],
  "status": "ACTIVE",
  "scraped_at": "2026-10-15T16:33:07+00:00"
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges apply only where configured. Inspect an existing run after a timeout before retrying a paid request.

## Call it from your AI agent without Apify

- Endpoint: `POST https://gethirepulse.xyz/v1/ats-jobs` with a JSON body such as `{"domain":"linear.app"}`
- Price: $0.01 per successful call. The first 5 successful calls per day are free (shared across all gateway tools). No API key required.
- This gateway is a separate service from the Apify Actor: its input, limits and price are its own. Catalog: https://gethirepulse.xyz/v1/catalog

Source page: https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api/
