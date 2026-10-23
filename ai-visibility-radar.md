# AI Search Brand Visibility Radar: AI Crawler Readiness Audit

> Audit website readiness for AI search engines and crawler agents (Perplexity, ChatGPT, Claude). Inspect robots directives, headers, llms.txt, and JSON-LD schema.

## What you get

- Inspect website robots directives, crawler access, and AI engine headers
- Audit llms.txt, JSON-LD structured data, and semantic discoverability
- Assess structural readiness for Perplexity, ChatGPT, and Claude crawlers
- Objective technical diagnostic report for generative engine optimization (GEO)

## AI Search Brand Visibility Radar (`hirepulse/ai-search-brand-visibility-radar`)

**Use it when:** You need to audit a website's robots directives, llms.txt, JSON-LD, and structural readiness for Perplexity, ChatGPT, and Claude crawlers.

**Not for:** Measuring actual citation count or mentions inside LLM chat answers.

- MCP: `https://mcp.apify.com?tools=hirepulse/ai-search-brand-visibility-radar`
- Apify Store: https://apify.com/hirepulse/ai-search-brand-visibility-radar
- Page: https://edtool79-collab.github.io/hirepulse-tools/ai-visibility-radar/
- Price: $0.02 per returned audit report.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `domains` | array of strings | required | Websites to audit for AI crawler readiness. |

Example input:

```json
{
  "domains": [
    "linear.app"
  ]
}
```

### Output example

Selected fields of one record from a real test run:

```json
{
  "domain": "linear.app",
  "robots_ai_crawlable": true,
  "llms_txt_found": true,
  "jsonld_schema_valid": true,
  "readiness_score": 95
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges also apply. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/ai-visibility-radar/
