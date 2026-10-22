# Website metadata, sitemap and keyword-suggestion API

> Inspect website titles, meta descriptions, sitemap observations and Google Autocomplete suggestions. Native mode does not measure organic traffic, ranking positions, keyword search volumes or CPC; unavailable metrics remain null.

## What you get

- Observed page title and meta description
- Public sitemap observations and sampled URLs
- Autocomplete suggestions, not ranking or search-volume measurements
- Unavailable SEO-database metrics remain null

## Domain SEO Overview (`hirepulse/domain-seo-overview`)

**Use it when:** Inspect website titles, meta descriptions, sitemap observations and Google Autocomplete suggestions. Native mode does not measure organic traffic, ranking positions, keyword search volumes or CPC; unavailable metrics remain null.

**Not for:** Organic traffic estimates, measured search rankings, search volumes or CPC in native mode.

- MCP: `https://mcp.apify.com?tools=hirepulse/domain-seo-overview`
- Apify Store: https://apify.com/hirepulse/domain-seo-overview
- Page: https://edtool79-collab.github.io/hirepulse-tools/domain-seo-overview-api/
- Price: Native/public-evidence mode emits no domain-lookup or domain-result charges. An Actor start event is still listed at $0.00005 per GB (minimum one event), and applicable Apify charges may apply. Review the live Pricing tab. Paid SEO-database events are separate and are not activated by this example.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `domains` | array of strings | required | Public website domains. |
| `country` | string | default US | Country code; not proof of database coverage. |
| `top_keywords` | integer | set 0 for this preview | Autocomplete suggestions are not ranking keywords. |
| `competitors` | integer | set 0 for this preview | No measured competitor SEO dataset is promised. |
| `use_paid_upstream` | boolean | false | Owner opt-in for a separately configured paid upstream; leave false for this preview. |

Input of the test run below:

```json
{
  "domains": [
    "example.com"
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
  "domain": "example.com",
  "country": "US",
  "language": "en",
  "has_data": true,
  "data_source": "public_evidence_engine",
  "public_page_available": null,
  "page_title": "Example Domain",
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
  "meta_description": null,
  "sitemap_present": false,
  "sitemap_urls_found": null,
  "sitemap_urls_sample": null,
  "top_ranking_keywords": [
    {
      "keyword": "example",
      "suggestion_position": 1,
      "search_intent": "navigational",
      "source": "google_autocomplete",
      "search_volume": null,
      "cpc_usd": null,
      "ranking": null
    },
    {
      "keyword": "example cover letter",
      "suggestion_position": 2,
      "search_intent": "navigational",
      "source": "google_autocomplete",
      "search_volume": null,
      "cpc_usd": null,
      "ranking": null
    },
    {
      "keyword": "example resume",
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
