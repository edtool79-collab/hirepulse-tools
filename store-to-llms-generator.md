# Store to LLMs Generator: Ecommerce Catalog to llms.txt

> Sample product catalogs from accessible public store feeds and draft an agent-ready llms.txt format with structured product attributes, prices, and variants.

## What you get

- Transform public store feeds and product collections into clean llms.txt format
- Extract key product specs, variants, pricing, and availability as structured text
- Make ecommerce inventory discoverable by AI agents and shopping assistants
- No store admin access needed; works from public storefronts

## Store to LLMs Generator (`hirepulse/shopify-to-llms-generator`)

**Use it when:** You need to transform public store product feeds into a structured, agent-readable llms.txt markdown document.

**Not for:** Full bulk sync of private warehouse inventory or checkout execution.

- MCP: `https://mcp.apify.com?tools=hirepulse/shopify-to-llms-generator`
- Apify Store: https://apify.com/hirepulse/shopify-to-llms-generator
- Page: https://edtool79-collab.github.io/hirepulse-tools/store-to-llms-generator/
- Price: $0.02 per generated catalog document report.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `store_url` | string | required | Public storefront URL. |

Example input:

```json
{
  "store_url": "https://untuckit.com"
}
```

### Output example

Selected fields of one record from a real test run:

```json
{
  "store": "untuckit.com",
  "catalog_format": "llms.txt",
  "products_cataloged": 5,
  "status": "ready"
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges also apply. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/store-to-llms-generator/
