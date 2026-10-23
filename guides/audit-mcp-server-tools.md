# Audit an MCP server: tool schemas, token efficiency and x402 evidence

> Grade any public MCP server or x402 endpoint with Python: tool counts, schema typing, token efficiency and payment challenge structure for $0.01 per report.

AI agents are only as reliable as the MCP servers they call. Before pointing Cursor, Claude Desktop or a custom agent runtime at a third-party MCP endpoint, you want evidence: how many tools does it actually expose, are the parameter schemas typed correctly, are descriptions token-efficient, and if the server speaks x402, does its payment challenge carry the right headers and pricing metadata.

Doing this by hand means opening the endpoint, listing tools, eyeballing every JSON schema, and manually checking the 402 response. The [MCP & x402 Server Grader](https://edtool79-collab.github.io/hirepulse-tools/mcp-x402-grader/) automates that audit and returns a structured evidence report for $0.01 per report, with no subscription.

## What the grader inspects

The Actor takes a public server URL and a target type:

```json
{
  "server_url": "https://mcp.deepwiki.com/mcp",
  "target_type": "mcp",
  "auto_fix": true
}
```

For an MCP target it observes and grades:

- **Tool catalog:** the live tool count exposed by the endpoint.
- **Per-tool schema checks:** parameter typing, required-field declarations, and description completeness.
- **Token efficiency:** how many tokens each tool consumes in the model's context, compared to its information value.
- **Review drafts:** suggested fixes for the server owner, exported as evidence. Drafts never modify the remote server.

For an x402 target (`"target_type": "x402"`) with a paid resource URL you are authorized to probe, it records the observed HTTP status and the structural findings of the unpaid payment challenge. The probe does not buy the resource, submit a payment, or prove settlement works.

## Quick start with cURL

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~mcp-x402-server-grader/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "server_url": "https://mcp.deepwiki.com/mcp",
  "target_type": "mcp",
  "auto_fix": true
}'
```

## Production Python audit pipeline

A batch auditor that grades a list of candidate MCP servers and writes the evidence to disk:

```python
import os
import json
from apify_client import ApifyClient

client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

servers = [
    "https://mcp.deepwiki.com/mcp",
    "https://mcp.apify.com",
]

results = []
for url in servers:
    run_input = {
        "server_url": url,
        "target_type": "mcp",
        "auto_fix": True,
    }
    run = client.actor("hirepulse/mcp-x402-server-grader").call(run_input=run_input)

    if not run or run.get("status") != "SUCCEEDED":
        # An unreachable endpoint without observed tools produces diagnostic
        # OUTPUT only and no dataset event - treat it as a skip, not a failure.
        print(f"{url}: no dataset report (unreachable or no tool evidence)")
        continue

    report = next(client.dataset(run["defaultDatasetId"]).iterate_items(), None)
    if report:
        results.append(report)
        print(f"{url}: {report.get('tools_count', '?')} tools observed")

with open("mcp_audit.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

## Architectural considerations

### The grade is a local heuristic

The report grades documentation and schema structure locally. It is not official Glama TDQS, a Glama Grade A certification, an x402scan approval, a penetration test, or a complete security assessment. Use it as a fast triage layer before a human review, not as a replacement for one.

### Charges follow evidence, not attempts

Pricing is $0.01 per returned report via Apify's automatic default-dataset-item event: no start fee and no additional custom charge. A reachable endpoint that fails checks still produces a useful, chargeable diagnostic report. An unreachable endpoint without observed tools or HTTP evidence produces diagnostic `OUTPUT` in key-value storage only and no dataset event, so you are not charged for dead URLs.

### Authorization boundary

Only submit public URLs you are authorized to inspect. The Actor handles no credentials and performs read-only observation; x402 probes never complete a payment.

## Technical limitations and pricing

- **Availability & Source Boundaries:** Reports what the server publicly exposes at call time. Drafts never modify the remote server; missing behavior requires owner review. The grade is a local documentation heuristic, not a certification or security assessment.
- **Pricing:** $0.01 per returned evidence audit report. Unreachable endpoints without observed evidence cost $0. No paid external API is used. Post-run storage access can have separate platform costs; review the live Pricing tab and set a spend limit.

## Next steps

- [Open MCP & x402 Server Grader on the Apify Store](https://apify.com/hirepulse/mcp-x402-server-grader)
- Explore parameters on the [tool documentation page](https://edtool79-collab.github.io/hirepulse-tools/mcp-x402-grader/)
- Related guide: [Give your AI agent live data with MCP](https://edtool79-collab.github.io/hirepulse-tools/guides/ai-agent-live-data-mcp/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/audit-mcp-server-tools/
