# AI visibility audit in Python: check if AI crawlers can read your site

> Audit any domain's AI-crawler readiness with Python: robots.txt rules for GPTBot, ClaudeBot, PerplexityBot, llms.txt presence, JSON-LD and headers for $0.02 per report.

AI search engines can only cite what their crawlers can read. GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot and CCBot each follow robots.txt directives — and sites routinely block some of them by accident, via a copy-pasted blocklist or a security plugin, without realizing they are opting out of AI citations.

The [AI Search Brand Visibility Radar](https://edtool79-collab.github.io/hirepulse-tools/ai-visibility-radar/) audits exactly that: one domain in, one structured readiness report out — per-crawler robots.txt directives, response headers, llms.txt observations, JSON-LD schema types, identity links, and a prioritized action list.

## What the audit reports

Input is one primary domain, with optional (up to three) competitors and (up to ten) category phrases:

```json
{
  "domain": "linear.app",
  "competitor_domains": [],
  "category_keywords": [],
  "generate_ready_llms_txt": true
}
```

The report inspects robots.txt directives for eight named crawler tokens: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended and CCBot. It also reads homepage response headers, llms.txt and llms-full.txt presence, JSON-LD schema types and discovered identity links, then produces local readiness scores with the supporting HTTP evidence. With `generate_ready_llms_txt: true`, key-value storage also carries a `RECOMMENDED_LLMS_TXT` draft built from observed site information — review it before publishing; the Actor never changes your website.

## Quick start with cURL

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~ai-search-brand-visibility-radar/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "domain": "linear.app",
  "generate_ready_llms_txt": true
}'
```

## Production Python: audit a portfolio

```python
import os
import json
from apify_client import ApifyClient

client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

domains = ["yourbrand.com", "competitor-one.com", "competitor-two.com"]

reports = []
for domain in domains:
    run = client.actor("hirepulse/ai-search-brand-visibility-radar").call(
        run_input={"domain": domain, "generate_ready_llms_txt": True}
    )
    report = next(client.dataset(run["defaultDatasetId"]).iterate_items(), None)
    if report:
        reports.append(report)
        print(f"{domain}: audit_status={report.get('audit_status', 'ok')}")
    else:
        # Homepage blocked or unavailable -> diagnostics in key-value OUTPUT,
        # no dataset event. Treat as retry/manual, not as a zero score.
        print(f"{domain}: homepage unavailable, no report")

with open("ai_visibility.json", "w", encoding="utf-8") as f:
    json.dump(reports, f, ensure_ascii=False, indent=2)

# Extract the blocked-crawler fix list: which tokens are disallowed?
for r in reports:
    robots = r.get("robots_tokens") or {}
    blocked = [t for t, d in robots.items() if d.get("disallowed")]
    print(f"{r['domain']}: AI crawlers disallowed: {blocked or 'none'}")
```

### Readiness is structural, not citation counting

The report grades structural crawler access: directives, headers, llms.txt, JSON-LD. It does not query paid AI models, does not measure how often you are cited in ChatGPT/Claude/Perplexity answers, does not prove accessibility from real crawler IPs, and does not guarantee rankings. The `ai_answer_citations_verified` field exists so your pipeline never misreads a structural grade as a citation measurement. Grades are local heuristics, not certification.

### The empty-dataset case is signal, not failure

If the homepage is blocked or unavailable, diagnostics land in the `OUTPUT` key-value record with `audit_status=homepage_unavailable` and no billable dataset event. A run can finish SUCCEEDED with an empty dataset — handle that branch explicitly in code (the Python above does) instead of crashing on a missing item.

### Competitive framing, honestly gathered

Optional competitor domains (max 3) and category phrases (max 10) run in the same report so you can compare your robots directives against peers. Start without them for a focused audit; the saved sample being an owner test is disclosed, not a customer endorsement.

## Technical limitations and pricing

- **Availability & Source Boundaries:** Structural crawler-readiness audit across eight AI-crawler tokens: robots directives, headers, llms.txt/llms-full.txt observations, JSON-LD types, identity links, readiness scores with HTTP evidence, prioritized actions, and an optional llms.txt draft. Does not query AI models, measure citations, verify real-crawler fetches, or guarantee rankings. Autocomplete suggestions are not AI citations.
- **Pricing:** $0.02 per returned primary-domain report, charged once via Apify's default-dataset-item event. No Actor start fee, no additional custom charge. Optional comparisons are included in the same report. Homepage-unavailable runs cost $0.

## Next steps

- [Open AI Search Brand Visibility Radar on the Apify Store](https://apify.com/hirepulse/ai-search-brand-visibility-radar)
- Explore parameters on the [tool documentation page](https://edtool79-collab.github.io/hirepulse-tools/ai-visibility-radar/)
- Related guide: [Audit an MCP server: tool schemas, token efficiency and x402 evidence](https://edtool79-collab.github.io/hirepulse-tools/guides/audit-mcp-server-tools/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/ai-visibility-audit-python/
