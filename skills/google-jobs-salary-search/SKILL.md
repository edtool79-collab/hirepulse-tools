---
name: google-jobs-salary-search
description: Search Google Jobs across 90+ countries by keyword, city, and radius to extract job listings, parsed min/max salaries, contract types, posting dates, and direct apply links (hirepulse/google-jobs-scraper). Use when searching jobs by role or location across multiple employers, benchmarking salaries, or replacing SerpApi Google Jobs API.
version: 1.0.0
tags:
  - google-jobs
  - job-search
  - salary-data
  - job-listings-api
  - recruitment
  - labor-market
  - serpapi-alternative
  - apify
  - mcp
---

# Google Jobs & Salary Search (`hirepulse/google-jobs-scraper`)

Search Google Jobs in 90+ countries for a whole country or a specific city with a radius (`1` to `300` km). Returns up to 200 jobs per search query with job title, company name, location, raw salary text plus parsed `salary_min`, `salary_max`, `salary_currency`, and `salary_period`, contract type, `posted_at` / `posted_ago`, source site, and direct apply URL.

## When to Use This Skill (vs. Standard Web Search)

- **Use this skill** when searching for open roles by job title, skill, or location across all employers:
  - Finding jobs in a specific city/state (`location: "Austin,Texas"`, with optional `radius_km` from 1 to 300) or across any of 90+ countries.
  - Benchmarking compensation using parsed `salary_min`, `salary_max`, and `salary_period`.
  - Getting direct `apply_url` links and optional full job descriptions when the apply link points to a public ATS (Workday, Greenhouse, Lever, Ashby).
- **Do NOT use standard web search** for Google Jobs aggregation: Google's job widget requires structured SERP extraction and does not expose its aggregated listings or parsed salary fields in standard organic web results.

## Verified Limitations & When NOT to Use

- **Salary availability & currency detection:** Salary fields (`salary`, `salary_min`, `salary_max`, `salary_period`) are populated only when shown on the Google Jobs listing (in our test run of 30 US jobs, 5 showed a salary). Additionally, `salary_currency` is not always detected and can be `null` even when `salary_min` and `salary_max` are parsed.
- **Location formatting:** `location` must be written as `"City,Region"` (e.g., `"Austin,Texas"`), and `radius_km` supports `1` to `300`.
- **Per-query result cap:** Returns up to `200` jobs per search (`max_jobs_per_query`, default `50`).
- **Single-company ATS board scraping:** If you want every open role from a single company's Greenhouse, Lever, Ashby, Workable, Recruitee, or SmartRecruiters board along with department breakdowns, use `hirepulse/ats-job-pulse` instead.
- **Pricing:**
  - `$0.005` per search that returns jobs + `$0.001` per job returned.
  - **Zero-result protection:** A search that finds nothing is **not charged** (`$0`).
  - Pay per use, no subscription (higher Apify plans get volume discounts). Apify's free plan provides `$5/month` in Store credit with no credit card required ([https://apify.com/pricing](https://apify.com/pricing)).

## Quick Connect (MCP & REST API)

### 1. Remote MCP Server
- **Single tool URL:** `https://mcp.apify.com?tools=hirepulse/google-jobs-scraper`
- **Auth:** OAuth in browser, or header `Authorization: Bearer <APIFY_TOKEN>`

### 2. Local MCP Server (stdio — Claude Desktop, Cursor, Windsurf, Cline)
```json
{
  "mcpServers": {
    "google-jobs-salary-search": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "hirepulse/google-jobs-scraper"],
      "env": {
        "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>"
      }
    }
  }
}
```

### 3. Direct REST API Call
```bash
curl -X POST "https://api.apify.com/v2/acts/hirepulse~google-jobs-scraper/run-sync-get-dataset-items?token=<APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["data engineer"],
    "country": "US",
    "location": "Austin,Texas",
    "max_jobs_per_query": 50
  }'
```

## Input Schema

```json
{
  "queries": [
    "data engineer"
  ],
  "country": "US",
  "location": "Austin,Texas",
  "max_jobs_per_query": 50
}
```

| Field | Type | Description |
| :--- | :--- | :--- |
| `queries` | `string[]` | Job search queries (e.g., `["data engineer"]`). |
| `country` | `string` | Country code across 90+ supported countries (e.g., `"US"`). |
| `location` | `string` | Optional city/region formatted as `"City,Region"` (e.g., `"Austin,Texas"`). |
| `radius_km` | `integer` | Optional search radius in kilometers (`1` to `300`). |
| `max_jobs_per_query` | `integer` | Maximum jobs per query (default `50`, up to `200`). |

## Output Fields

- `query` (`string`) — Search query used
- `country` (`string`) — Country code
- `position` (`integer`) — Result rank position
- `title` (`string`) — Job title
- `company` (`string`) — Employer name
- `company_url` (`string | null`) — Company link if available
- `company_logo_url` (`string | null`) — Company logo URL
- `location` (`string`) — Job location (e.g., `"Austin, TX"`)
- `contract_type` (`string | null`) — e.g., `"Full-time"`
- `salary` (`string | null`) — Raw salary text as displayed (e.g., `"73K–130K a year"`)
- `salary_min` (`number | null`) — Parsed minimum salary (e.g., `73000`)
- `salary_max` (`number | null`) — Parsed maximum salary (e.g., `130000`)
- `salary_currency` (`string | null`) — Currency code when detected (can be `null` even when `salary_min`/`salary_max` are parsed)
- `salary_period` (`string | null`) — e.g., `"year"`
- `posted_at` (`string | null`) — UTC timestamp of job posting
- `posted_ago` (`string | null`) — Relative posting time (e.g., `"2 days ago"`, `"13 days ago"`)
- `source` (`string`) — Source job board or site (e.g., `"LinkedIn"`, `"JobzMall"`, `"BeBee"`)
- `apply_url` (`string`) — Direct application URL
- `google_job_id` (`string`) — Google Jobs identifier
- `scraped_at` (`string`) — ISO 8601 scrape timestamp
- `description` (`string | null`) — Optional full description when fetched from a supported public ATS
- `description_source` (`string | null`) — Source of full description if fetched

## Real Output Examples (Owner Test Run 2026-10-15)

```json
[
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
  },
  {
    "query": "data engineer",
    "country": "US",
    "position": 4,
    "title": "Data Engineer - People Analytics",
    "company": "General Motors",
    "company_url": null,
    "company_logo_url": "https://api.dataforseo.com/cdn/i/10151634-2796-0447-0000-ac22c4fd6890:3",
    "location": "Austin, TX",
    "contract_type": "Full-time",
    "salary": "73K–130K a year",
    "salary_min": 73000,
    "salary_max": 130000,
    "salary_currency": null,
    "salary_period": "year",
    "posted_at": null,
    "posted_ago": null,
    "source": "JobzMall",
    "apply_url": "https://www.jobzmall.com/general-motors/job/data-engineer-people-analytics-3",
    "google_job_id": "rClAD9ADzLbDjhPGAAAAAA==",
    "scraped_at": "2026-10-15T16:34:29Z",
    "description": null,
    "description_source": null
  }
]
```

## Links & Documentation
- **Apify Store:** [https://apify.com/hirepulse/google-jobs-scraper](https://apify.com/hirepulse/google-jobs-scraper)
- **Tool Documentation:** [https://edtool79-collab.github.io/hirepulse-tools/google-jobs-api/](https://edtool79-collab.github.io/hirepulse-tools/google-jobs-api/)
- **Markdown Spec:** [https://edtool79-collab.github.io/hirepulse-tools/google-jobs-api.md](https://edtool79-collab.github.io/hirepulse-tools/google-jobs-api.md)
- **SerpApi Migration Guide:** [https://edtool79-collab.github.io/hirepulse-tools/migrate/serpapi-google-jobs/](https://edtool79-collab.github.io/hirepulse-tools/migrate/serpapi-google-jobs/)
