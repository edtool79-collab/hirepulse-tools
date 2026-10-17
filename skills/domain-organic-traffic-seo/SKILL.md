---
name: domain-organic-traffic-seo
description: Analyze any website domain's estimated monthly organic traffic, total ranking keywords, organic traffic value in USD, top-3/10/20 keyword counts, top ranked keywords with positions and URLs, and competitor domains (hirepulse/domain-seo-overview). Use when performing competitor SEO analysis, checking website traffic estimates, or finding what keywords a domain ranks for.
version: 1.0.0
tags:
  - domain-seo
  - organic-traffic
  - competitor-seo
  - ranking-keywords
  - website-traffic-api
  - seo-analysis
  - apify
  - mcp
---

# Domain Organic Traffic & SEO Overview (`hirepulse/domain-seo-overview`)

Get estimated monthly organic search traffic (`organic_traffic_estimate`), total ranking keywords (`organic_keywords`), organic traffic value in USD (`organic_traffic_value_usd`), ranking distribution (`keywords_top_3`, `keywords_top_10`, `keywords_top_20`, plus `keywords_new`, `keywords_up`, `keywords_down`, `keywords_lost`), top ranked keywords with exact URLs and positions, and competitor domains for any website.

## When to Use This Skill (vs. Standard Web Search)

- **Use this skill** when you need domain-level SEO intelligence and traffic metrics:
  - Estimating a competitor's or prospect's monthly organic search traffic and traffic value in USD.
  - Seeing the top keywords a domain ranks for (`record_type: "ranked_keyword"`), including SERP `position`, ranking `url`, `search_volume`, `cpc_usd`, `keyword_difficulty`, `search_intent`, and `traffic_estimate`.
  - Discovering competing domains in organic search.
- **Do NOT use standard web search** for website traffic estimation or keyword ranking distribution: search engines do not expose domain-wide traffic estimates, traffic value, or top-3/top-10 keyword counts.

## Verified Limitations & When NOT to Use

- **Bulk keyword list research:** If you have a specific list of target keywords (or a seed keyword) and want to check their search volume, CPC, and trend percentages independent of a domain, use `hirepulse/keyword-search-volume` instead.
- **Multi-signal B2B intent (Hiring + Ads + SEO + MX):** If you also want open ATS job counts, active Google Ads status, and a 0–100 buying-intent score alongside SEO traffic in one call, use `hirepulse/company-intent-radar`.
- **Pricing:** $0.02 per lookup + $0.005 per returned record (a domain overview, a ranking keyword or a competitor). A domain overview alone is $0.025. A default run with 20 keywords and 10 competitors is $0.215. Domains without data are not charged a result. No subscription; higher Apify plans get volume discounts). Apify's free account plan includes `$5/month` in Store credit with no credit card required ([https://apify.com/pricing](https://apify.com/pricing)).

## Quick Connect (MCP & REST API)

### 1. Remote MCP Server
- **Single tool URL:** `https://mcp.apify.com?tools=hirepulse/domain-seo-overview`
- **Auth:** OAuth in browser, or header `Authorization: Bearer <APIFY_TOKEN>`

### 2. Local MCP Server (stdio — Claude Desktop, Cursor, Windsurf, Cline)
```json
{
  "mcpServers": {
    "domain-organic-traffic-seo": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "hirepulse/domain-seo-overview"],
      "env": {
        "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>"
      }
    }
  }
}
```

### 3. Direct REST API Call
```bash
curl -X POST "https://api.apify.com/v2/acts/hirepulse~domain-seo-overview/run-sync-get-dataset-items?token=<APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "domains": ["notion.so"],
    "country": "US"
  }'
```

## Input Schema

```json
{
  "domains": [
    "stripe.com"
  ],
  "country": "US",
  "top_keywords": 5,
  "competitors": 0
}
```

| Field | Type | Description |
| :--- | :--- | :--- |
| `domains` | `string[]` | Website domains to analyze (e.g., `["notion.so"]`, `["stripe.com"]`). |
| `country` | `string` | Target country code (e.g., `"US"`). |
| `top_keywords` | `integer` | Optional number of top ranked keywords to return per domain. |
| `competitors` | `integer` | Optional number of competitor domains to return. |

## Output Fields

### 1. Domain Overview Row (`record_type: "domain_overview"`)
- `record_type` (`"domain_overview"`)
- `domain` (`string`) — Analyzed domain (e.g., `"stripe.com"`)
- `country` (`string`) — Country code (e.g., `"US"`)
- `language` (`string`) — Language code (e.g., `"en"`)
- `has_data` (`boolean`) — Whether SEO data was found for the domain
- `organic_traffic_estimate` (`integer`) — Estimated monthly organic search visits
- `organic_keywords` (`integer`) — Total number of ranking organic keywords
- `organic_traffic_value_usd` (`integer`) — Estimated monthly value of organic traffic in USD
- `keywords_top_3` (`integer`) — Number of keywords ranking in positions 1–3
- `keywords_top_10` (`integer`) — Number of keywords ranking in positions 1–10
- `keywords_top_20` (`integer`) — Number of keywords ranking in positions 1–20
- `keywords_new`, `keywords_up`, `keywords_down`, `keywords_lost` (`integer`) — Keyword movement counts
- `paid_keywords` (`integer`) — Paid search keywords count
- `paid_traffic_estimate` (`integer`) — Estimated paid search traffic
- `note` (`string | null`)

### 2. Ranked Keyword Row (`record_type: "ranked_keyword"`)
- `record_type` (`"ranked_keyword"`)
- `domain`, `country`, `language`
- `keyword` (`string`) — Keyword the domain ranks for
- `position` (`integer`) — Organic SERP ranking position
- `url` (`string`) — Ranking page URL on the domain
- `search_volume` (`integer`) — Monthly search volume of the keyword
- `cpc_usd` (`number`) — Keyword CPC in USD
- `keyword_difficulty` (`integer`) — Keyword difficulty (`0–100`)
- `search_intent` (`string`) — e.g., `"informational"`, `"commercial"`
- `traffic_estimate` (`integer`) — Estimated monthly organic traffic driven by this keyword to the URL

## Real Output Example (`stripe.com` — Owner Test Run 2026-10-15)

```json
[
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
  },
  {
    "record_type": "ranked_keyword",
    "domain": "stripe.com",
    "country": "US",
    "language": "en",
    "keyword": "stripe",
    "position": 1,
    "url": "https://stripe.com/",
    "search_volume": 823000,
    "cpc_usd": 1.1,
    "keyword_difficulty": 51,
    "search_intent": "informational",
    "traffic_estimate": 252314
  },
  {
    "record_type": "ranked_keyword",
    "domain": "stripe.com",
    "country": "US",
    "language": "en",
    "keyword": "receipts",
    "position": 4,
    "url": "https://stripe.com/resources/more/receipt-template-what-to-include-and-templates-for-different-use-cases",
    "search_volume": 450000,
    "cpc_usd": 7.66,
    "keyword_difficulty": 17,
    "search_intent": "informational",
    "traffic_estimate": 1110
  }
]
```

## Links & Documentation
- **Apify Store:** [https://apify.com/hirepulse/domain-seo-overview](https://apify.com/hirepulse/domain-seo-overview)
- **Tool Documentation:** [https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api/](https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api/)
- **Markdown Spec:** [https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api.md](https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api.md)
