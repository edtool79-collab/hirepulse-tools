---
name: greenhouse-lever-ashby-jobs
description: Scrape open jobs, published salary ranges, departments, locations, and detected tech stacks from company ATS job boards including Greenhouse, Lever, Ashby, Workable, Recruitee, and SmartRecruiters (hirepulse/ats-job-pulse). Use when extracting all open roles at specific target companies by domain or board slug, analyzing a company's tech stack from job descriptions, or tracking new and closed job postings.
version: 1.0.0
tags:
  - ats-jobs
  - greenhouse
  - lever
  - ashby
  - workable
  - recruitee
  - smartrecruiters
  - tech-stack-detection
  - hiring-data
  - apify
  - mcp
---

# Greenhouse, Lever & Ashby ATS Jobs Scraper (`hirepulse/ats-job-pulse`)

Extract all open jobs and company hiring summaries directly from a company's **Greenhouse, Lever, Ashby, Workable, Recruitee, or SmartRecruiters** job board. Pass a company domain (such as `stripe.com`, `ramp.com`, or `linear.app`) or board slug — the tool automatically discovers the ATS board, extracts every active job with published salaries and apply links, detects technologies mentioned in job titles and descriptions, and generates a company summary row.

## When to Use This Skill (vs. Standard Web Search)

- **Use this skill** when you need complete, structured job board data for specific companies:
  - Listing all active openings at a company by domain (`stripe.com`, `ramp.com`, `notion.so`) without knowing its ATS URL ahead of time.
  - Extracting a company's engineering and business tech stack (`detected_technologies` & `top_technologies`, e.g., Python, React, Snowflake, Terraform, Salesforce, LLMs) directly from live job descriptions.
  - Getting headcount breakdowns by department (`jobs_by_department`) and location (`top_locations`), plus published salary ranges (`salary`).
  - Tracking only new or closed jobs between runs (`track_diff`).
- **Do NOT use standard web search** for enumerating a company's ATS board: search engines miss newly posted roles, show stale closed roles, and cannot aggregate department counts or full technology frequency tables across 100+ openings.

## Verified Limitations & When NOT to Use

- **Workday is NOT supported:** This tool supports **six ATS platforms only**: Greenhouse, Lever, Ashby, Workable, Recruitee, and SmartRecruiters. **Workday is NOT supported.** (If you need jobs from companies using Workday or broad keyword searches across all employers, use `hirepulse/google-jobs-scraper` instead.)
- **Salary availability:** The `salary` field is populated where the company publishes it on the ATS posting (for example, in the real sample below, `ramp.com` published salaries on 158 of 165 jobs, while `linear.app` published salaries on 0 of 30 jobs, returning `null`).
- **Pricing:** $0.05 per company whose job board was found and processed, however many jobs it has. Companies that are not found, and failed ones, are not charged. No subscription; higher Apify plans get volume discounts). Apify's free plan includes `$5/month` in Store credit with no credit card required at [https://apify.com/pricing](https://apify.com/pricing).

## Quick Connect (MCP & REST API)

### 1. Remote MCP Server
- **Single tool URL:** `https://mcp.apify.com?tools=hirepulse/ats-job-pulse`
- **Combine with Google Jobs:** `https://mcp.apify.com?tools=hirepulse/google-jobs-scraper,hirepulse/ats-job-pulse`
- **Auth:** OAuth in browser, or header `Authorization: Bearer <APIFY_TOKEN>`

### 2. Local MCP Server (stdio — Claude Desktop, Cursor, Windsurf, Cline)
```json
{
  "mcpServers": {
    "greenhouse-lever-ashby-jobs": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "hirepulse/ats-job-pulse"],
      "env": {
        "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>"
      }
    }
  }
}
```

### 3. Direct REST API Call
```bash
curl -X POST "https://api.apify.com/v2/acts/hirepulse~ats-job-pulse/run-sync-get-dataset-items?token=<APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "companies": ["stripe.com", "notion.so"]
  }'
```

## Input Schema

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

| Field | Type | Description |
| :--- | :--- | :--- |
| `companies` | `string[]` | Company domains (e.g., `["stripe.com", "notion.so"]`) or ATS board slugs. |
| `output_mode` | `string` | Optional mode such as `"jobs_and_summary"`. |
| `track_diff` | `boolean` | Optional flag to track new/closed jobs between runs. |
| `max_jobs_per_company` | `integer` | Optional limit on individual job records returned per company. |

## Output Fields

### 1. Job Record (`record_type: "job"`)
- `record_type` (`"job"`)
- `company_domain` (`string`) — e.g., `"ramp.com"`
- `ats_type` (`string`) — Detected ATS platform (e.g., `"ashby"`, `"greenhouse"`, `"lever"`, `"workable"`, `"recruitee"`, `"smartrecruiters"`)
- `job_id` (`string`) — Unique job identifier on the ATS board
- `title` (`string`) — Job title
- `department` (`string`) — Department name (e.g., `"Engineering"`, `"Sales"`, `"Product"`)
- `location` (`string`) — Job location string
- `is_remote` (`boolean`) — Whether the role is flagged as remote
- `posted_date` (`string`) — ISO 8601 posting timestamp
- `salary` (`string | null`) — Published salary range string (e.g., `"$211.4K - $290.6K"`) or `null`
- `apply_url` (`string`) — Direct URL to the ATS job posting
- `detected_technologies` (`string[]`) — Technologies detected in the title and description (e.g., `["AWS", "Azure", "Flask", "GCP", "Python", "Terraform"]`)
- `status` (`string`) — e.g., `"ACTIVE"`
- `scraped_at` (`string`) — ISO 8601 timestamp

### 2. Company Summary Record (`record_type: "company_summary"`)
- `company_domain`, `ats_type`, `board_slug`
- `total_active_jobs`, `remote_jobs`, `jobs_with_salary`, `matching_jobs`
- `is_first_run`, `new_jobs`, `closed_jobs`, `new_job_titles`, `closed_job_titles`
- `jobs_by_department` (`object`) — Map of department names to open job counts
- `top_locations` (`object`) — Map of top locations to open job counts
- `top_technologies` (`object`) — Map of detected technologies to number of jobs mentioning them

## Real Output Example (`ramp.com` — Owner Test Run 2026-10-15)

```json
[
  {
    "record_type": "company_summary",
    "company_domain": "ramp.com",
    "ats_type": "ashby",
    "board_slug": "ramp",
    "total_active_jobs": 165,
    "remote_jobs": 148,
    "jobs_with_salary": 158,
    "is_first_run": null,
    "new_jobs": null,
    "closed_jobs": null,
    "new_job_titles": [],
    "closed_job_titles": [],
    "jobs_by_department": {
      "Sales": 69,
      "Engineering": 36,
      "People & Talent": 14,
      "Product": 8,
      "Marketing": 8,
      "Design": 6,
      "Customer Experience": 5,
      "Data": 5,
      "Finance": 4,
      "Risk": 2
    },
    "top_locations": {
      "New York, NY (HQ)": 127,
      "London, UK": 12,
      "San Francisco, CA": 10,
      "Remote (US)": 10,
      "Toronto, ON": 6
    },
    "top_technologies": {
      "Python": 31,
      "Salesforce": 28,
      "SQL": 24,
      "LLMs": 16,
      "AWS": 13,
      "React": 11,
      "Looker": 11,
      "Snowflake": 10,
      "TypeScript": 9
    },
    "matching_jobs": 165,
    "scraped_at": "2026-10-15T16:33:07+00:00"
  },
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
      "Flask",
      "GCP",
      "Python",
      "Terraform"
    ],
    "status": "ACTIVE",
    "scraped_at": "2026-10-15T16:33:07+00:00"
  }
]
```

## Links & Documentation
- **Apify Store:** [https://apify.com/hirepulse/ats-job-pulse](https://apify.com/hirepulse/ats-job-pulse)
- **Tool Documentation:** [https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api/](https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api/)
- **Markdown Spec:** [https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api.md](https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api.md)
