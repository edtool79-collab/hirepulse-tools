# Shopify Competitor Watcher

Track competitor Shopify stores daily: price drops, price increases, back-in-stock, out-of-stock, new and removed products. Built-in saved snapshots, so each run returns only what changed. No database, no browser.

## What it returns

Structured JSON describing each watched company, the change detected
(new roles, closed roles, price moves, stock changes) and the source evidence
used to detect it.

## Price

Pay per changed company or delivered report. Unchanged checks and entities with
no public board are not charged. The live Pricing tab on the Apify Store page is
authoritative.

## Connect an AI agent (MCP)

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/shopify-competitor-watcher`
- REST API: `POST https://api.apify.com/v2/acts/hirepulse~shopify-competitor-watcher/run-sync-get-dataset-items?token=<APIFY_TOKEN>`

## See also

- [All HirePulse tools](https://edtool79-collab.github.io/hirepulse-tools/llms-full.txt)
- [Apify Store](https://apify.com/hirepulse)
