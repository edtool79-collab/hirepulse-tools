# Website metadata, sitemap and keyword-suggestion API

> Inspect website titles, meta descriptions, sitemap observations and Google Autocomplete suggestions. Native mode does not measure organic traffic, ranking positions, keyword search volumes or CPC; unavailable metrics remain null.

## What you get

- Observed page title and meta description
- Public sitemap observations and sampled URLs
- Autocomplete suggestions, not ranking or search-volume measurements
- Unavailable SEO-database metrics remain null

## Domain SEO Overview (`hirepulse/domain-seo-overview`)

![Domain SEO Overview Preview](./domain-seo-overview.png)

**Use it when:** Inspect website titles, meta descriptions, sitemap observations and Google Autocomplete suggestions. Native mode does not measure organic traffic, ranking positions, keyword search volumes or CPC; unavailable metrics remain null.

**Not for:** Organic traffic estimates, measured search rankings, search volumes or CPC in native mode.

- MCP: `https://mcp.apify.com?tools=hirepulse/domain-seo-overview`
- Apify Store: https://apify.com/hirepulse/domain-seo-overview
- Page: https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api/
- Price: Native/public-evidence mode emits no domain-lookup or domain-result charges. An Actor start event is still listed at $0.00005 per GB (minimum one event), and applicable Apify charges may apply. Review the live Pricing tab. Paid SEO-database events are separate and are not activated by this example.

### 💰 Transparent Pricing Explained

- **Apify Store Headline Clarification:** The headline "$4.00 / 1,000" reflects the platform volume tier on `domain-result` events for higher subscription tiers.
- **Standard Free Plan Rate:** On the Apify Free plan, default execution costs **$0.025 per domain** ($0.02 per `domain-lookup` + $0.005 per `domain-result`).
- **Zero Third-Party API Spend in Native Mode:** In default Native mode (`use_paid_upstream: false`), exactly **$0.00** is incurred for third-party SEO databases (DataForSEO, etc.). You get 100% free native data retrieval without burning external credits.
- **Budget Cap Protection:** Always specify `maxTotalChargeUsd: 0.10` via query parameters in REST calls to guarantee hard budget enforcement.

### 📊 Feature Coverage: Public Native Mode vs Paid Upstream

| Feature / Metric | Native Mode (Default) | Paid Upstream Mode | Zero-Spend Guarantee Notes |
| --- | :---: | :---: | --- |
| **Page Title & Meta Description** | ✅ Available ($0.00) | ✅ Available | Direct HTML extraction, zero external API costs. |
| **Sitemap Discovery & Sample URLs** | ✅ Available ($0.00) | ✅ Available | Crawls `robots.txt` and XML sitemaps directly. |
| **Google Autocomplete Suggestions** | ✅ Available ($0.00) | ✅ Available | Live keyword query suggestions with navigational intent. |
| **Chrome Popularity Tier** | ✅ Available ($0.00) | ✅ Available | Public CrUX popularity indicator. |
| **Organic Traffic Estimate** | ❌ `null` | ⚠️ External DB | Intentionally returned as `null` to prevent paid API burn. |
| **CPC & Search Volume** | ❌ `null` | ⚠️ External DB | Intentionally returned as `null` to guarantee $0.00 upstream spend. |
| **Domain Rank & Backlinks** | ❌ `null` | ⚠️ External DB | Requires paid commercial index; `null` in native mode. |

> **Zero-Spend Protection Policy:** Native mode is hardcoded to never trigger billable external SEO database calls. Unavailable enterprise metrics intentionally return `null` instead of charging your account.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `domains` | array of strings | required | Public website domains, for example ["linear.app"]. |
| `country` | string | default US | Country code; not proof of database coverage. |
| `top_keywords` | integer | set 0 for this preview | Autocomplete suggestions are not ranking keywords. |
| `competitors` | integer | set 0 for this preview | No measured competitor SEO dataset is promised. |
| `use_paid_upstream` | boolean | false | Owner opt-in for a separately configured paid upstream; leave false for this preview. |

Input of the test run below:

```json
{
  "domains": [
    "linear.app"
  ],
  "top_keywords": 0,
  "competitors": 0,
  "country": "US",
  "use_paid_upstream": false
}
```

### Output example

One record from a real test run on 2026-10-21 (long text and lists shortened):

```json
{
  "record_type": "domain_overview",
  "domain": "linear.app",
  "country": "US",
  "language": "en",
  "has_data": true,
  "data_source": "public_evidence_engine",
  "public_page_available": null,
  "page_title": "Linear – A better way to build products",
  "http_status": null,
  "organic_traffic_estimate": null,
  "organic_keywords": null,
  "organic_traffic_value_usd": null,
  "keywords_top_3": null,
  "keywords_top_10": null,
  "keywords_top_20": null,
  "keywords_new": null,
  "keywords_up": null,
  "keywords_down": null,
  "keywords_lost": null,
  "paid_keywords": null,
  "paid_traffic_estimate": null,
  "note": "Public evidence only: the page title, meta description, sitemap and the URLs it lists, and keyword suggestions from Google Autocomplete. Organic traffic, domain rank, ranking keywords and indexed pages need a paid SEO database and are null here. Autocomplete position is not an organic ranking. No pa…",
  "provider_mode": "native",
  "free_fallback": true,
  "metrics_available": false,
  "provider_cost_usd": 0,
  "meta_description": "Linear is a purpose-built tool for planning and building products. Streamline issues, projects, and product roadmaps.",
  "sitemap_present": true,
  "sitemap_urls_found": 142,
  "sitemap_urls_sample": [
    "https://linear.app/",
    "https://linear.app/features",
    "https://linear.app/pricing"
  ],
  "top_ranking_keywords": [
    {
      "keyword": "linear",
      "suggestion_position": 1,
      "search_intent": "navigational",
      "source": "google_autocomplete",
      "search_volume": null,
      "cpc_usd": null,
      "ranking": null
    },
    {
      "keyword": "linear app",
      "suggestion_position": 2,
      "search_intent": "navigational",
      "source": "google_autocomplete",
      "search_volume": null,
      "cpc_usd": null,
      "ranking": null
    },
    {
      "keyword": "linear issue tracker",
      "suggestion_position": 3,
      "search_intent": "navigational",
      "source": "google_autocomplete",
      "search_volume": null,
      "cpc_usd": null,
      "ranking": null
    }
  ],
  "domain_rank": null,
  "indexed_pages_estimate": null
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges also apply. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api/
