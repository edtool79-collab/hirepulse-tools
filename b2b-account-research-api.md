# B2B Account Research Agent API: Enterprise Dossier & Due Diligence

> Autonomous account intelligence combining careers hiring velocity, web technology stack, Google ads presence, and verified digital footprint into a structured dossier.

## What you get

- Full-funnel enterprise account research combining hiring, tech stack, and ad signals
- Automated vendor due diligence and outbound sales prospecting dossier
- Department distribution from open roles and active advertising presence
- Agent-ready executive summary and structured JSON evidence

## B2B Account Research Agent (`hirepulse/b2b-account-research-agent`)

**Use it when:** You need an autonomous executive dossier combining hiring trends, observed tech stack, Google ads presence, and verified contact channels.

**Not for:** Raw bulk scraping of thousands of unfiltered domains.

- MCP: `https://mcp.apify.com?tools=hirepulse/b2b-account-research-agent`
- Apify Store: https://apify.com/hirepulse/b2b-account-research-agent
- Page: https://edtool79-collab.github.io/hirepulse-tools/b2b-account-research-api/
- Price: $0.05 per company research dossier produced.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `domains` | array of strings | required | Target company domains to investigate. |

Example input:

```json
{
  "domains": [
    "stripe.com",
    "cloudflare.com"
  ]
}
```

### Output example

Selected fields of one record from a real test run:

```json
{
  "domain": "stripe.com",
  "intent_score": 92,
  "hiring_velocity": "High",
  "open_positions": 727,
  "ads_active": true,
  "primary_ats": "greenhouse"
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges apply only where configured. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/b2b-account-research-api/
