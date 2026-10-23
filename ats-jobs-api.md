# ATS Jobs API: Greenhouse, Lever & Ashby Jobs

> Extract open jobs, published salary ranges and the technologies they mention from Greenhouse, Lever, Ashby, Workable, Recruitee and SmartRecruiters. Pay-per-use ATS data API.

## What you get

- Give a domain like stripe.com, the job board is found automatically
- Six ATS systems supported (not Workday)
- Department, location, remote flag, posting date and apply URL
- Only-new-jobs tracking between runs

## ATS Job Scraper (`hirepulse/ats-job-pulse`)

![ATS Job Pulse Preview](./ats-job-pulse.png)

**Use it when:** You need every open job from a company's Greenhouse, Lever, Ashby, Workable, Recruitee or SmartRecruiters board. Pass a domain such as stripe.com or a board slug.

**Not for:** Companies on Workday or custom career sites.

- MCP: `https://mcp.apify.com?tools=hirepulse/ats-job-pulse`
- Apify Store: https://apify.com/hirepulse/ats-job-pulse
- Page: https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api/
- Price: $0.05 per company whose job board was found and processed, however many jobs it has. Companies that are not found, and failed ones, are not charged.

### 💰 Transparent Pricing Explained

- **Apify Store Headline Clarification:** The headline "from $40.00 / 1,000" on the Apify store reflects the platform volume tier for Gold subscribers ($0.04 per processed company).
- **Standard Free Plan Rate:** Standard pay-per-event pricing on Apify Free plans is **$0.05 per processed company**.
- **Flat Fee per Company:** 1 job or 200 jobs cost exactly the same ($0.05). No per-job microcharges.
- **Zero-Data Guarantee:** If a domain has no supported ATS job board or scraping fails, you are charged **$0.00**.
- **Budget Cap Protection:** Set `maxTotalChargeUsd: 0.10` in your REST API call query parameters to enforce strict budget limits and prevent accidental overages.

### 🔄 How to Track Job Changes (2-Step Guide)

Automate hiring intelligence and track headcount momentum by detecting newly posted and closed positions without re-processing entire boards:

1. **Step 1: Baseline Run (Initial Snapshot)**
   Run with `track_diff: true`, assign a persistent `state_id` (e.g. `"my-targets"`), and set `only_changes: false`. This captures all current openings and establishes the reference baseline.
   ```json
   {
     "companies": ["linear.app"],
     "track_diff": true,
     "state_id": "my-targets",
     "only_changes": false
   }
   ```

2. **Step 2: Monitoring Run (Delta Only)**
   Schedule a recurring check using the same `state_id: "my-targets"` with `track_diff: true` and `only_changes: true`. The output will strictly contain newly published (`NEW`) or archived (`CLOSED`) postings since the last run.
   ```json
   {
     "companies": ["linear.app"],
     "track_diff": true,
     "state_id": "my-targets",
     "only_changes": true
   }
   ```

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `companies` | array of strings | required | Company domains or board slugs, for example ["linear.app"]. |
| `output_mode` | string | default "jobs_and_summary" | jobs_and_summary, summary_only or jobs_only. |
| `track_diff` | boolean | default true | Mark new and closed jobs between runs. |
| `only_changes` | boolean | default false | Return only changes since the last run. |
| `state_id` | string | optional | Persistent identifier to maintain diff history across multiple runs. |
| `extract_tech_keywords` | boolean | default true | Detect technologies mentioned in job titles and descriptions. |
| `title_keywords` | array of strings | optional | Filter by words in the job title. |
| `departments` | array of strings | optional | Filter by department name. |
| `locations` | array of strings | optional | Filter by location string. |
| `technologies` | array of strings | optional | Filter by detected technology keywords. |
| `remote_only` | boolean | default false | Return only remote-friendly positions. |
| `max_jobs_per_company` | integer | default 0 | 0 means no limit. |

Input of the test run below:

```json
{
  "companies": [
    "linear.app"
  ],
  "output_mode": "jobs_and_summary",
  "track_diff": false,
  "max_jobs_per_company": 3
}
```

### Output Example

Concise breakdown of key job fields extracted per position:

| Field | Type | Description | Example |
| --- | --- | --- | --- |
| `title` | string | Normalized job role title | `"Security Engineer, Cloud"` |
| `salary` | string / null | Extracted published compensation range | `"$211.4K - $290.6K"` |
| `apply_url` | string | Direct URL to ATS job application page | `"https://jobs.ashbyhq.com/linear/..."` |
| `detected_technologies` | array | Tech stack keywords detected in job description | `["AWS", "Azure", "Flask"]` |
| `is_remote` | boolean | Remote work eligibility flag | `true` |

One record from a real test run on 2026-10-15 (long text and lists shortened):

```json
{
  "record_type": "job",
  "company_domain": "linear.app",
  "ats_type": "ashby",
  "job_id": "34413f8d-26bf-4bbc-8ade-eb309a0e2245",
  "title": "Security Engineer, Cloud",
  "department": "Engineering",
  "location": "New York, NY (HQ)",
  "is_remote": true,
  "posted_date": "2026-04-07T17:12:35.753+00:00",
  "salary": "$211.4K - $290.6K",
  "apply_url": "https://jobs.ashbyhq.com/linear/34413f8d-26bf-4bbc-8ade-eb309a0e2245",
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
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges also apply. Inspect an existing run after a timeout before retrying a paid request.

## Call it from your AI agent without Apify

- Endpoint: `POST https://gethirepulse.xyz/v1/ats-jobs` with a JSON body such as `{"domain":"linear.app"}`
- Price: $0.01 per successful call. The first 5 successful calls per day are free (shared across all gateway tools). No API key required.
- This gateway is a separate service from the Apify Actor: its input, limits and price are its own. Catalog: https://gethirepulse.xyz/v1/catalog

Source page: https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api/
