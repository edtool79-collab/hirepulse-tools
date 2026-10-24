# TikTok Product Research & Video Growth Radar

> Research product-related TikTok videos with source links, creator breadth and history. Measure growth on the same videos after6+ hours; no sales forecasts.

## What you get

- Research product-video evidence and same-video growth across observations
- First collection is a baseline; repeat after at least six hours
- Choose capped Clockworks collection with explicit consent, or import an existing export
- Structured JSON and an HTML research report with blockers and next actions

## TikTok Product Research (`hirepulse/viral-product-radar`)

**Use it when:** You need to research a product-video cohort with source links, creator-account breadth and repeated same-video observations.

**Not for:** Sales or profit forecasts, Shop sales, ad-spend data or complete TikTok discovery. First collection is a baseline; live collection requires capped Clockworks consent.

- MCP: `https://mcp.apify.com?tools=hirepulse/viral-product-radar`
- Apify Store: https://apify.com/hirepulse/viral-product-radar
- Page: https://edtool79-collab.github.io/hirepulse-tools/tiktok-product-research-api/
- Price: $0.02 per delivered report; Clockworks collection is separate and capped ($0.04 total by default).

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `keywords` | string[] | one product recommended | Product keywords. |
| `upstream_source` | string | clockworks | Choose live Clockworks or public for an existing export. |
| `allow_paid_upstream` | boolean | false | Must be explicitly true for live collection. |
| `upstream_max_charge_usd` | number | 0.04 | Total separate provider cap for the whole run. |
| `state_id` | string | default | Reuse after6+ hours for same-video growth. |

Example input:

```json
{
  "keywords": [
    "mini projector"
  ],
  "analysis_mode": "product_videos",
  "upstream_source": "clockworks",
  "allow_paid_upstream": true,
  "upstream_max_charge_usd": 0.04,
  "max_items": 10,
  "state_id": "my-product-research",
  "deliver_all_reports": true
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges apply only where configured. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/tiktok-product-research-api/
