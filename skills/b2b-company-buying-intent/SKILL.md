---
name: b2b-company-buying-intent
description: Enrich B2B company domains with live buying-intent signals, active hiring counts, Google Ads activity, organic SEO traffic, MX email provider, and a 0-100 intent score (hirepulse/company-intent-radar). Use when qualifying sales leads, building AI SDR workflows, enriching domains for Clay or CRM pipelines, or checking if a company is actively growing and spending.
version: 1.0.0
tags:
  - b2b-intent
  - sales-intelligence
  - lead-enrichment
  - ai-sdr
  - hiring-signals
  - company-research
  - apify
  - mcp
---

# B2B Company Buying Intent (`hirepulse/company-intent-radar`)

Enrich any company domain with live buying-intent signals in a single pay-per-use API call. Combines hiring velocity across 6 major ATS platforms, active Google Ads status and total ad count, organic search traffic estimates and SEO trends, MX record email provider detection, a 0–100 intent score, and a concise one-line summary built for AI agents and SDR workflows.

## When to Use This Skill (vs. Standard Web Search)

- **Use this skill** when you need multi-signal B2B qualification or account enrichment for one or more company domains:
  - Scoring accounts (`0-100` intent score) before outreach in AI SDR or CRM workflows.
  - Checking simultaneously whether a prospect is hiring (open jobs & new jobs in the last 30 days), running Google Ads right now, and growing organic search traffic.
  - Identifying a company's email infrastructure (`email_provider` from MX records, e.g., Google Workspace) alongside growth signals.
- **Do NOT use standard web search** when you need consistent, structured numeric signals across multiple domains (ATS job counts, live ad counts, DNS MX resolution, and SEO traffic estimates in one payload).

## Verified Limitations & When NOT to Use

- **ATS coverage for hiring signals:** Hiring signals cover **Greenhouse, Lever, Ashby, Workable, SmartRecruiters, and Recruitee** boards. Companies using unsupported ATS platforms (such as Workday) will not have ATS board jobs counted here.
- **Need full individual job listings or ad creatives?** This tool returns domain-level signals and counts. If you need every individual job description/salary, use `hirepulse/ats-job-pulse`. If you need individual ad creatives and preview links, use `hirepulse/google-ads-transparency-scraper`.
- **Pricing & Free Plan:**
  - **Price:** `$0.03` per company report, charged **only** when the full report was produced (pay per use, no subscription; higher Apify plans get volume discounts).
  - **Free plan preview:** Includes hiring and email signals for 5 companies.
  - **Apify Free Plan:** Apify's free account plan provides `$5` per month to spend in Apify Store with no credit card required ([https://apify.com/pricing](https://apify.com/pricing)).

## Quick Connect (MCP & REST API)

### 1. Remote MCP Server
- **Single tool URL:** `https://mcp.apify.com?tools=hirepulse/company-intent-radar`
- **Auth:** OAuth in browser, or header `Authorization: Bearer <APIFY_TOKEN>`

### 2. Local MCP Server (stdio — Claude Desktop, Cursor, Windsurf, Cline)
```json
{
  "mcpServers": {
    "b2b-company-buying-intent": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "hirepulse/company-intent-radar"],
      "env": {
        "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>"
      }
    }
  }
}
```

### 3. Direct REST API Call
```bash
curl -X POST "https://api.apify.com/v2/acts/hirepulse~company-intent-radar/run-sync-get-dataset-items?token=<APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "domains": ["stripe.com", "notion.so"],
    "country": "US"
  }'
```

## Input Schema

```json
{
  "domains": [
    "stripe.com",
    "notion.so"
  ],
  "country": "US"
}
```

| Field | Type | Description |
| :--- | :--- | :--- |
| `domains` | `string[]` | List of company domains to enrich (e.g., `["stripe.com", "notion.so"]`). |
| `country` | `string` | Target country code for SEO and ad signals (e.g., `"US"`). |

## Output Signals & Fields

Per company domain report:
- `domain` (`string`) — Company domain (e.g., `"stripe.com"`)
- `intent_score` (`integer`) — 0–100 composite buying-intent score
- `open_jobs` (`integer`) — Total open jobs across supported ATS boards (Greenhouse, Lever, Ashby, Workable, SmartRecruiters, Recruitee) alongside new jobs in the last 30 days
- `ads_running_now` (`boolean`) — Whether the company has active Google Ads running now (plus total ads count)
- `email_provider` (`string`) — Email provider detected from MX records (e.g., `"Google Workspace"`)
- Organic traffic estimate and SEO trend
- One-line summary string tailored for AI agents and SDRs

## Real Output Example

Real verified record (`2026-10-15`):
```json
{
  "domain": "stripe.com",
  "intent_score": 85,
  "open_jobs": 727,
  "ads_running_now": true,
  "email_provider": "Google Workspace"
}
```

## Links & Documentation
- **Apify Store:** [https://apify.com/hirepulse/company-intent-radar](https://apify.com/hirepulse/company-intent-radar)
- **Tool Documentation:** [https://edtool79-collab.github.io/hirepulse-tools/company-intent-signals-api/](https://edtool79-collab.github.io/hirepulse-tools/company-intent-signals-api/)
- **Markdown Spec:** [https://edtool79-collab.github.io/hirepulse-tools/company-intent-signals-api.md](https://edtool79-collab.github.io/hirepulse-tools/company-intent-signals-api.md)
