# Company Jobs Watcher

Watch up to 50 company job boards for new and closed roles. Bring previous job IDs or save snapshots for daily monitoring. Pay $0.01 per changed company or first baseline; unchanged and no-board checks are free.

## What it returns

Structured JSON describing each watched company, the change detected
(new roles, closed roles, price moves, stock changes) and the source evidence
used to detect it.

## Price

Pay per changed company or delivered report. Unchanged checks and entities with
no public board are not charged. The live Pricing tab on the Apify Store page is
authoritative.

## Connect an AI agent (MCP)

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/company-jobs-watcher`
- REST API: `POST https://api.apify.com/v2/acts/hirepulse~company-jobs-watcher/run-sync-get-dataset-items?token=<APIFY_TOKEN>`

## See also

- [All HirePulse tools](https://edtool79-collab.github.io/hirepulse-tools/llms-full.txt)
- [Apify Store](https://apify.com/hirepulse)
