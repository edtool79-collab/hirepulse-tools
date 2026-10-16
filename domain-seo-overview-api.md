# Website traffic and SEO overview API for any domain

> Estimated organic traffic, ranking keywords, traffic value and competitor domains for any website, via API.

## What you get

- Organic traffic estimate and ranking keywords
- Top keywords the domain ranks for
- Competitor domains

## Domain SEO Overview (`hirepulse/domain-seo-overview`)

**Use it when:** You need estimated organic traffic, ranking keywords, traffic value and competitor domains for a domain.

**Not for:** Exact analytics. The numbers are estimates; report them as estimates.

- MCP: `https://mcp.apify.com?tools=hirepulse/domain-seo-overview`
- Apify Store: https://apify.com/hirepulse/domain-seo-overview
- Page: https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api/
- Price: See the Apify Store page: https://apify.com/hirepulse/domain-seo-overview

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `domains` | array of strings | required | For example ["notion.so"]. |
| `country` | string | default "US" | Country code. |
| `language` | string | optional |  |
| `top_keywords` | integer | default 20 |  |
| `competitors` | integer | default 10 |  |

Input of the test run below:

```json
{
  "domains": [
    "stripe.com"
  ],
  "top_keywords": 5,
  "competitors": 0
}
```

### Output example

One record from a real test run on 2026-10-15:

```json
{
  "record_type": "domain_overview",
  "domain": "stripe.com",
  "country": "US",
  "language": "en",
  "has_data": true,
  "organic_traffic_estimate": 688494,
  "organic_keywords": 115829,
  "organic_traffic_value_usd": 8338941,
  "keywords_top_3": 19298,
  "keywords_top_10": 50840,
  "keywords_top_20": 78460,
  "keywords_new": 59404,
  "keywords_up": 23927,
  "keywords_down": 22077,
  "keywords_lost": 72928,
  "paid_keywords": 14,
  "paid_traffic_estimate": 128,
  "note": null
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?token=<APIFY_TOKEN>` with the input as the JSON body.
- Every result is billed (pay per use, no subscription). Start with one query or domain, then scale up.

Source page: https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api/
