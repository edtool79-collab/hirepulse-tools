# Company Intent Signals API: Hiring, Ads & SEO

> Enrich any company domain with live hiring data, active Google ads, SEO traffic and intent scores in a single pay-per-use API call.

## What you get

- Hiring from Greenhouse, Lever, Ashby, Workable, SmartRecruiters and Recruitee boards
- Google ads running now and total ad count
- Organic search traffic estimate and trend
- Email provider from MX records
- 0-100 intent score plus a one-line summary an agent can read

## Company Intent Radar (`hirepulse/company-intent-radar`)

**Use it when:** You need one report per company domain: open jobs and new jobs in the last 30 days, Google ads running now and in total, organic traffic and SEO trend, email provider from MX records, a 0-100 intent score and a one-line summary.

**Not for:** The full list of a company's jobs (use hirepulse/ats-job-pulse for that).

- MCP: `https://mcp.apify.com?tools=hirepulse/company-intent-radar`
- Apify Store: https://apify.com/hirepulse/company-intent-radar
- Page: https://edtool79-collab.github.io/hirepulse-tools/company-intent-signals-api/
- Price: $0.03 per company report, charged only when the full report was produced. Free plan: hiring and email signals for 5 companies.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `domains` | array of strings | required | Company domains, for example ["stripe.com"]. |
| `country` | string | default "US" | Country code. |
| `include_jobs` | boolean | default false | Also return the job list. |

Example input:

```json
{
  "domains": [
    "stripe.com",
    "notion.so"
  ],
  "country": "US"
}
```

### Output example

Selected fields of one record from a real test run:

```json
{
  "domain": "stripe.com",
  "intent_score": 85,
  "open_jobs": 727,
  "ads_running_now": true,
  "email_provider": "Google Workspace"
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges also apply. Inspect an existing run after a timeout before retrying a paid request.

## Call it from your AI agent without Apify

- Endpoint: `POST https://gethirepulse.xyz/v1/company-intent` with a JSON body such as `{"domain":"linear.app"}`
- Price: $0.01 per successful call. The first 5 successful calls per day are free (shared across all gateway tools). No API key required.
- This gateway is a separate service from the Apify Actor: its input, limits and price are its own. Catalog: https://gethirepulse.xyz/v1/catalog

Source page: https://edtool79-collab.github.io/hirepulse-tools/company-intent-signals-api/
