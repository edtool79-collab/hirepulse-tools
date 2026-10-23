# MCP & x402 Server Grader: Live Protocol & Schema Audit

> Benchmark MCP server tools and x402 payment configurations. Audits tool schema descriptions, token efficiency, payment challenges, and Base network readiness.

## What you get

- Inspect live MCP tool catalogs and schema completeness
- Verify x402 payment headers, network compliance, and pricing metadata
- Benchmark tool call token efficiency and schema conciseness
- Automated scoring and draft recommendations for agent developers

## MCP & x402 Server Grader (`hirepulse/mcp-x402-server-grader`)

**Use it when:** You need to evaluate an MCP server endpoint for tool catalog completeness, token brevity, and x402 payment header compliance.

**Not for:** Modifying remote servers or official Glama certification.

- MCP: `https://mcp.apify.com?tools=hirepulse/mcp-x402-server-grader`
- Apify Store: https://apify.com/hirepulse/mcp-x402-server-grader
- Page: https://edtool79-collab.github.io/hirepulse-tools/mcp-x402-grader/
- Price: $0.01 per returned evidence audit report.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `server_url` | string | required | MCP HTTP endpoint to audit. |

Example input:

```json
{
  "server_url": "https://gethirepulse.xyz/mcp"
}
```

### Output example

Selected fields of one record from a real test run:

```json
{
  "server": "https://gethirepulse.xyz/mcp",
  "tools_count": 21,
  "x402_compliant": true,
  "token_efficiency_grade": "A",
  "overall_grade": 98
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges also apply. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/mcp-x402-grader/
