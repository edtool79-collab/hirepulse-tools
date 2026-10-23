# ATS Detector API: Careers Board & Recruiting Platform Finder

> Detect which applicant tracking system any company uses (Greenhouse, Lever, Ashby, Workable, etc.) and extract official careers board endpoints.

## What you get

- Find which applicant tracking system a company uses (Greenhouse, Lever, Ashby, Workable, etc.)
- Automatically locate official public careers and job board URLs
- Prepare recruiting workflows and enrich B2B account records
- Detect career subdomains and custom-hosted job portals

## ATS Detector (`hirepulse/ats-detector`)

**Use it when:** You need to find which ATS a company uses (Greenhouse, Lever, Ashby, Workable, etc.) and extract its job board URL.

**Not for:** Listing individual job postings (use ats-jobs-api for jobs).

- MCP: `https://mcp.apify.com?tools=hirepulse/ats-detector`
- Apify Store: https://apify.com/hirepulse/ats-detector
- Page: https://edtool79-collab.github.io/hirepulse-tools/ats-detector-api/
- Price: $0.005 per domain checked. Undetected boards cost $0.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `domains` | array of strings | required | Company domains to check. |

Example input:

```json
{
  "domains": [
    "linear.app",
    "datadoghq.com"
  ]
}
```

### Output example

Selected fields of one record from a real test run:

```json
{
  "domain": "linear.app",
  "ats_system": "ashby",
  "careers_url": "https://jobs.ashbyhq.com/linear",
  "board_active": true
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges also apply. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/ats-detector-api/
