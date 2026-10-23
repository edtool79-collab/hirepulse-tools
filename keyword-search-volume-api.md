# Keyword search volume and CPC API (Google)

> Google monthly search volume, CPC and competition for your keywords, plus keyword ideas, in bulk via API.

## What you get

- Search volume, CPC and competition per keyword
- Keyword ideas from a seed keyword
- Optional AI search volume (how often a keyword is asked in AI assistants)
- Many countries and languages

## Keyword Search Volume (`hirepulse/keyword-search-volume`)

**Use it when:** You need Google monthly search volume, CPC, competition or keyword ideas for a list of keywords.

**Not for:** Rank tracking of a website (use hirepulse/domain-seo-overview for a domain's ranking keywords).

- MCP: `https://mcp.apify.com?tools=hirepulse/keyword-search-volume`
- Apify Store: https://apify.com/hirepulse/keyword-search-volume
- Page: https://edtool79-collab.github.io/hirepulse-tools/keyword-search-volume-api/
- Price: $0.03 per lookup + $0.005 per keyword result. Free Apify plan: real volume, CPC and difficulty for the first 3 keywords of each run (depends on availability and can be paused).

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `keywords` | array of strings | required | For example ["running shoes"]. |
| `mode` | string | default "metrics" | metrics, ideas or suggestions. |
| `country` | string | default "US" | Country code. |
| `language` | string | optional |  |
| `max_results` | integer | default 50 |  |
| `min_search_volume` | integer | default 0 |  |
| `include_monthly_searches` | boolean | default false |  |
| `include_ai_search_volume` | boolean | default false |  |

Input of the test run below:

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

### Output example

One record from a real test run on 2026-10-15:

```json
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
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges also apply. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/keyword-search-volume-api/
