# Website Tech Stack API: Technologies, CMS & Pixels

> Enrich company domains with observed website technologies, advertising pixels, frontend frameworks, and DNS email signals in a single API call.

## What you get

- Enrich company records with observed website technologies and advertising pixels
- Detect CMS, frontend frameworks, analytics, ecommerce platforms, and hosting
- Inspect public DNS and MX email signals
- Fast plain-HTTP inspection without running heavy headless browsers

## Website Tech Stack Detector (`hirepulse/website-tech-stack-detector`)

**Use it when:** You need to detect CMS, frameworks, analytics, ecommerce platforms, ad pixels, or MX records for any domain.

**Not for:** Internal source code or private infrastructure not exposed on the public web.

- MCP: `https://mcp.apify.com?tools=hirepulse/website-tech-stack-detector`
- Apify Store: https://apify.com/hirepulse/website-tech-stack-detector
- Page: https://edtool79-collab.github.io/hirepulse-tools/website-tech-stack-api/
- Price: $0.005 per domain checked + $0.001 per detected tech. Domains with no stack cost $0.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `domains` | array of strings | required | Domains to inspect, e.g. ["stripe.com"]. |
| `mode` | string | default "technologies" | technologies, pixels, or full. |

Example input:

```json
{
  "domains": [
    "stripe.com",
    "linear.app"
  ],
  "mode": "technologies"
}
```

### Output example

Selected fields of one record from a real test run:

```json
{
  "domain": "stripe.com",
  "technologies_found": [
    "React",
    "Next.js",
    "Amazon CloudFront",
    "Google Tag Manager",
    "Marketo"
  ],
  "cms": null,
  "email_provider": "Google Workspace"
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges apply only where configured. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/website-tech-stack-api/
