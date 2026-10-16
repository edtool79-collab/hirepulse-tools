---
name: google-ads-competitor-spy
description: Spy on competitor Google Ads by domain using the Google Ads Transparency Center API (hirepulse/google-ads-transparency-scraper). Use when the user asks to see what Google ads a company or competitor is running, check active ad creatives (text, image, video), verify advertisers leading to a domain for brand protection, monitor new competitor ads, or get a domain ad summary without needing Google Advertiser IDs.
version: 1.0.0
tags:
  - google-ads
  - competitor-research
  - ad-transparency
  - ad-spy
  - brand-protection
  - marketing-intelligence
  - apify
  - mcp
---

# Google Ads Competitor Spy (`hirepulse/google-ads-transparency-scraper`)

Extract live Google ads run by any company directly by domain from the Google Ads Transparency Center. Pass a domain (e.g., `nike.com` or `adidas.com`) and receive structured JSON with advertiser details, verification status, ad formats (`text`, `image`, `video`), preview image URLs, ISO 8601 first/last shown timestamps, and days running — no Google Advertiser IDs or Transparency URLs required.

## When to Use This Skill (vs. Standard Web Search)

- **Use this skill** when you need structured, live ad data from the Google Ads Transparency Center for one or more domains:
  - Checking if a company or sales prospect is currently running Google Ads (`summary` mode).
  - Inspecting competitor ad formats (`text`, `image`, `video`), creative previews, and how long specific ads have been running (`days_running`).
  - Brand protection: discovering every advertiser whose ads lead to a target domain.
  - Scheduled competitor monitoring using `"only new ads"` mode.
- **Do NOT use standard web search** for this task: Google Ads Transparency Center pages are heavily client-rendered and cannot be reliably enumerated or filtered by domain via standard search engine queries.

## Verified Limitations & When NOT to Use

- **No ad spend or impression numbers:** Google does not publish spend or impression numbers for commercial ads. Do not use this tool expecting budget or impression metrics.
- **No creative dimensions:** The output does not include `width` or `height` of the creative.
- **Up to 120 recent ads per domain:** In `ads` mode, the tool returns up to the 120 most recent ads per domain.
- **Pricing & Free Plan Notice:**
  - **Ads mode:** `$0.005` per domain checked + `$0.0015` per ad returned.
  - **Summary mode:** `$0.005` per domain only (no per-ad charge; returns one row per domain).
  - **Zero-result protection:** Domains with no ads for your filters, and failed lookups, cost `$0` (not charged).
  - **Important:** There is no free tier or free ad quota specific to this Actor. (However, Apify's free account plan includes `$5` per month in platform credits with no credit card required at https://apify.com/pricing, and higher Apify plans get volume discounts.)

## Quick Connect (MCP & REST API)

### 1. Remote MCP Server
Connect your AI agent directly over HTTP/SSE:
- **Single tool URL:** `https://mcp.apify.com?tools=hirepulse/google-ads-transparency-scraper`
- **Auth:** OAuth in browser, or pass header `Authorization: Bearer <APIFY_TOKEN>`

### 2. Local MCP Server (stdio — Claude Desktop, Cursor, Windsurf, Cline)
Add to your MCP client configuration:
```json
{
  "mcpServers": {
    "google-ads-competitor-spy": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "hirepulse/google-ads-transparency-scraper"],
      "env": {
        "APIFY_TOKEN": "<YOUR_APIFY_TOKEN>"
      }
    }
  }
}
```

### 3. Direct REST API Call
```bash
curl -X POST "https://api.apify.com/v2/acts/hirepulse~google-ads-transparency-scraper/run-sync-get-dataset-items?token=<APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "domains": ["nike.com"],
    "country": "US",
    "max_ads_per_domain": 40,
    "mode": "ads"
  }'
```
> **Apify Free Plan:** Get `$5/month` in free Apify credit (no credit card required) at [https://apify.com/pricing](https://apify.com/pricing).

## Input Schema

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

| Field | Type | Description |
| :--- | :--- | :--- |
| `domains` | `string[]` | List of company domains to inspect (e.g., `["nike.com", "adidas.com"]`). |
| `country` | `string` | Target country ISO code (e.g., `"US"`). |
| `max_ads_per_domain` | `integer` | Maximum number of ads to return per domain in `ads` mode (up to 120 most recent ads). |
| `mode` | `string` | `"ads"` for individual ad records, or `"summary"` for one summary row per domain. Also supports `"only new ads"` monitoring. |

## Output Fields

- `domain` (`string`) — Queried company domain
- `advertiser_name` (`string`) — Official advertiser name in Google Ads Transparency Center
- `advertiser_id` (`string`) — Google Advertiser ID
- `advertiser_verified` (`boolean`) — Whether the advertiser is verified by Google
- `ad_id` (`string`) — Unique creative/ad identifier
- `format` (`string`) — Ad format: `"text"`, `"image"`, or `"video"`
- `first_shown` (`string`) — ISO 8601 timestamp when the ad was first shown
- `last_shown` (`string`) — ISO 8601 timestamp when the ad was last shown
- `days_running` (`integer`) — Total number of days between `first_shown` and `last_shown`
- `last_shown_days_ago` (`integer`) — Days elapsed since the ad was last shown
- `preview_image_url` (`string`) — URL to the ad creative preview image
- `preview_url` (`string`) — Preview URL for the ad creative
- `transparency_url` (`string`) — Direct link to the ad in Google Ads Transparency Center
- `country` (`string`) — Country filter used
- `platform` (`string`) — Target platform

## Real Output Examples

### Individual Ad Record (`mode: "ads"`)
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

### Real Domain Summary Fact (`adidas.com`)
- `adidas.com` summary: `6,000` ads total; sample of `40` = `33` text, `3` image, `4` video.

## Links & Documentation
- **Apify Store:** [https://apify.com/hirepulse/google-ads-transparency-scraper](https://apify.com/hirepulse/google-ads-transparency-scraper)
- **Tool Documentation:** [https://edtool79-collab.github.io/hirepulse-tools/google-ads-transparency-api/](https://edtool79-collab.github.io/hirepulse-tools/google-ads-transparency-api/)
- **Markdown Spec:** [https://edtool79-collab.github.io/hirepulse-tools/google-ads-transparency-api.md](https://edtool79-collab.github.io/hirepulse-tools/google-ads-transparency-api.md)
- **SerpApi Migration Guide:** [https://edtool79-collab.github.io/hirepulse-tools/migrate/serpapi-google-ads-transparency/](https://edtool79-collab.github.io/hirepulse-tools/migrate/serpapi-google-ads-transparency/)
