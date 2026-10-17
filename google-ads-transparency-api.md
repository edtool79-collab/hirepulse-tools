# Google Ads Transparency API: Ads by Domain

> Extract live Google ads by domain from Google Ads Transparency Center. Get ad preview images, formats and first/last shown dates as clean JSON.

## What you get

- Domains in, ads out: no advertiser IDs or Google URLs needed
- Text, image and video ads with preview image and Transparency Center link
- Summary mode: one row per domain (does it advertise, how many ads, formats, latest ad)
- 'Only new ads' mode for scheduled competitor monitoring
- Shows every advertiser whose ads lead to the domain, useful for brand protection

## Google Ads Transparency Scraper (`hirepulse/google-ads-transparency-scraper`)

**Use it when:** You need the Google ads a company runs, by domain: advertiser, verified flag, format (text, image or video), first and last shown dates, preview image and Transparency Center link.

- MCP: `https://mcp.apify.com?tools=hirepulse/google-ads-transparency-scraper`
- Apify Store: https://apify.com/hirepulse/google-ads-transparency-scraper
- Page: https://edtool79-collab.github.io/hirepulse-tools/google-ads-transparency-api/
- Price: $0.005 per domain + $0.0015 per ad. Domains with no ads cost $0.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `domains` | array of strings | required | Company domains, for example ["nike.com"]. |
| `mode` | string | default "ads" | ads or summary (one row per domain). |
| `max_ads_per_domain` | integer | default 40 |  |
| `country` | string | optional | Country code. |
| `platform` | string | default "all" | all, google_search, youtube, google_shopping, google_play or google_maps. |
| `format` | string | default "all" | all, text, image or video. |
| `date_from` | string | optional | Start date. |
| `date_to` | string | optional | End date. |
| `only_new_ads` | boolean | default false | Monitoring: return only ads not seen in earlier runs. |

Example input:

```json
{
  "domains": [
    "nike.com"
  ],
  "country": "US",
  "max_ads_per_domain": 40,
  "mode": "ads"
}
```

### Output example

Selected fields of one record from a real test run:

```json
{
  "domain": "nike.com",
  "advertiser_name": "Nike, Inc.",
  "advertiser_verified": true,
  "format": "text",
  "first_shown": "2023-11-16T21:51:37Z",
  "last_shown": "2026-10-14T15:10:53Z",
  "days_running": 1062
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges also apply. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/google-ads-transparency-api/
