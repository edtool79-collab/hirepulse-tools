---
name: google-keyword-volume-cpc
description: Get Google monthly search volume, CPC (USD), competition, keyword difficulty, search intent, top-of-page bid ranges, monthly/quarterly/yearly trends, and keyword ideas in bulk (hirepulse/keyword-search-volume). Use when doing SEO keyword research, evaluating PPC ad bids, finding keyword ideas from a seed keyword, or checking optional AI search volume.
version: 1.0.0
tags:
  - keyword-research
  - search-volume
  - google-cpc
  - seo
  - ppc
  - keyword-difficulty
  - search-intent
  - apify
  - mcp
---

# Google Keyword Search Volume & CPC (`hirepulse/keyword-search-volume`)

Fetch Google monthly search volume, cost-per-click (`cpc_usd`), competition score, `keyword_difficulty`, `search_intent`, top-of-page bid ranges (`low_top_of_page_bid_usd` / `high_top_of_page_bid_usd`), and trend percentages (`trend_monthly_pct`, `trend_quarterly_pct`, `trend_yearly_pct`) for your keywords in bulk, plus keyword ideas from a seed keyword and optional AI search volume.

## When to Use This Skill (vs. Standard Web Search)

- **Use this skill** when you need quantitative SEO or PPC metrics for keywords:
  - Checking exact monthly search volume (`search_volume`), `cpc_usd`, `keyword_difficulty`, and `search_intent` (`commercial`, `informational`, etc.) before writing content or launching ad campaigns.
  - Generating new keyword ideas from a seed keyword across many countries and languages.
  - Checking optional `ai_search_volume` (how often a keyword is asked in AI assistants).
- **Do NOT use standard web search** for keyword volume or CPC data: search engines do not display monthly search volume numbers, Google Ads bid ranges, or keyword difficulty scores in search results, and LLMs without a keyword tool can only guess search volume.

## Verified Limitations & When NOT to Use

- **Domain-level competitor rankings:** If you want to see all the keywords a specific domain (e.g., `stripe.com` or `notion.so`) already ranks for and its total organic traffic estimate, use `hirepulse/domain-seo-overview` instead.
- **Pricing & Free Plan Notice:**
  - **Price:** `$0.03` per lookup + `$0.005` per keyword result (pay per use, no subscription; higher Apify plans get volume discounts).
  - **Free plan preview:** Provides real volume, CPC, and difficulty for the first `3` keywords of each run; note that the free preview depends on availability and can be paused.
  - **Apify Free Plan:** Apify's free account plan includes `$5/month` in Store credit with no credit card required ([https://apify.com/pricing](https://apify.com/pricing)).

## Quick Connect (MCP & REST API)

### 1. Remote MCP Server
- **Single tool URL:** `https://mcp.apify.com?tools=hirepulse/keyword-search-volume`
- **Auth:** OAuth in browser, or header `Authorization: Bearer <APIFY_TOKEN>`

### 2. Local MCP Server (stdio — Claude Desktop, Cursor, Windsurf, Cline)
```json
{
  "mcpServers": {
    "google-keyword-volume-cpc": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "hirepulse/keyword-search-volume"],
      "env": {
        "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>"
      }
    }
  }
}
```

### 3. Direct REST API Call
```bash
curl -X POST "https://api.apify.com/v2/acts/hirepulse~keyword-search-volume/run-sync-get-dataset-items?token=<APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["running shoes", "trail running shoes"],
    "country": "US"
  }'
```

## Input Schema

```json
{
  "keywords": [
    "keyword research tool",
    "ai agents",
    "web scraping api"
  ],
  "country": "US"
}
```

| Field | Type | Description |
| :--- | :--- | :--- |
| `keywords` | `string[]` | List of keywords to check (e.g., `["running shoes", "trail running shoes"]`). |
| `country` | `string` | Target country code (e.g., `"US"`). |

## Output Fields

- `keyword` (`string`) — Queried or discovered keyword
- `search_volume` (`integer`) — Monthly Google search volume
- `cpc_usd` (`number`) — Cost per click in USD
- `competition` (`number`) — Ad competition score (`0` to `1`)
- `competition_level` (`string`) — e.g., `"LOW"`, `"MEDIUM"`, `"HIGH"`
- `keyword_difficulty` (`integer`) — SEO keyword difficulty score (`0` to `100`)
- `search_intent` (`string`) — e.g., `"commercial"`, `"informational"`
- `low_top_of_page_bid_usd` (`number`) — Low range for top-of-page bid in USD
- `high_top_of_page_bid_usd` (`number`) — High range for top-of-page bid in USD
- `trend_monthly_pct` (`number`) — Monthly search volume trend percentage
- `trend_quarterly_pct` (`number`) — Quarterly search volume trend percentage
- `trend_yearly_pct` (`number`) — Yearly search volume trend percentage
- `ai_search_volume` (`integer | null`) — Optional AI search volume when requested/available
- `country` (`string`) — Country code (e.g., `"US"`)
- `language` (`string`) — Language code (e.g., `"en"`)
- `source` (`string`) — Data source (e.g., `"keyword_database"`)
- `seed_keyword` (`string | null`) — Seed keyword when generating keyword ideas
- `metrics_available` (`boolean`) — Whether metrics were found for this keyword
- `data_updated_at` (`string`) — Timestamp when metrics were last updated
- `note` (`string | null`) — Optional note

## Real Output Example (Owner Test Run 2026-10-15)

```json
[
  {
    "keyword": "keyword research tool",
    "search_volume": 4400,
    "cpc_usd": 15.75,
    "competition": 0.29,
    "competition_level": "LOW",
    "keyword_difficulty": 81,
    "search_intent": "commercial",
    "low_top_of_page_bid_usd": 3.33,
    "high_top_of_page_bid_usd": 17.11,
    "trend_monthly_pct": -57,
    "trend_quarterly_pct": -47,
    "trend_yearly_pct": -81,
    "ai_search_volume": null,
    "country": "US",
    "language": "en",
    "source": "keyword_database",
    "seed_keyword": null,
    "metrics_available": true,
    "data_updated_at": "2026-09-15 12:14:58 +00:00",
    "note": null
  },
  {
    "keyword": "ai agents",
    "search_volume": 49500,
    "cpc_usd": 20.9,
    "competition": 0.46,
    "competition_level": "MEDIUM",
    "keyword_difficulty": 67,
    "search_intent": "commercial",
    "low_top_of_page_bid_usd": 6.58,
    "high_top_of_page_bid_usd": 18.6,
    "trend_monthly_pct": 0,
    "trend_quarterly_pct": 0,
    "trend_yearly_pct": 0,
    "ai_search_volume": null,
    "country": "US",
    "language": "en",
    "source": "keyword_database",
    "seed_keyword": null,
    "metrics_available": true,
    "data_updated_at": "2026-09-13 22:14:16 +00:00",
    "note": null
  },
  {
    "keyword": "web scraping api",
    "search_volume": 1900,
    "cpc_usd": 13.05,
    "competition": 0.28,
    "competition_level": "LOW",
    "keyword_difficulty": 59,
    "search_intent": "informational",
    "low_top_of_page_bid_usd": 4.5,
    "high_top_of_page_bid_usd": 19.2,
    "trend_monthly_pct": -33,
    "trend_quarterly_pct": -33,
    "trend_yearly_pct": -33,
    "ai_search_volume": null,
    "country": "US",
    "language": "en",
    "source": "keyword_database",
    "seed_keyword": null,
    "metrics_available": true,
    "data_updated_at": "2026-09-13 01:17:11 +00:00",
    "note": null
  }
]
```

## Links & Documentation
- **Apify Store:** [https://apify.com/hirepulse/keyword-search-volume](https://apify.com/hirepulse/keyword-search-volume)
- **Tool Documentation:** [https://edtool79-collab.github.io/hirepulse-tools/keyword-search-volume-api/](https://edtool79-collab.github.io/hirepulse-tools/keyword-search-volume-api/)
- **Markdown Spec:** [https://edtool79-collab.github.io/hirepulse-tools/keyword-search-volume-api.md](https://edtool79-collab.github.io/hirepulse-tools/keyword-search-volume-api.md)
