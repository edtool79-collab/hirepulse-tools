# HirePulse data tools for AI agents (MCP)

Five hosted data tools that Claude, Cursor and any MCP client can call, with no API keys to manage beyond an Apify account. They run on [Apify](https://apify.com/hirepulse). You pay per result, and each tool has a free preview.

| | Tool | What your agent can ask | Price |
| --- | --- | --- | --- |
| <img src="google-jobs.png" width="40"> | [Google Jobs Scraper](https://apify.com/hirepulse/google-jobs-scraper) | "Which companies in Austin are hiring data engineers, and what do they pay?" | $1 per 1,000 jobs + $0.005 per search |
| <img src="ats-job-pulse.png" width="40"> | [ATS Job Scraper](https://apify.com/hirepulse/ats-job-pulse) | "What did stripe.com and ramp.com open or close this week?" | $0.05 per company |
| <img src="keyword-search-volume.png" width="40"> | [Keyword Search Volume](https://apify.com/hirepulse/keyword-search-volume) | "Monthly Google searches, CPC and difficulty for these 200 keywords in Germany" | $0.03 per lookup + $0.005 per keyword |
| <img src="domain-seo-overview.png" width="40"> | [Domain SEO Overview](https://apify.com/hirepulse/domain-seo-overview) | "How much organic traffic does notion.so get, and who are its competitors?" | $0.02 per lookup + $0.005 per result |
| <img src="youtube-transcript-scraper.png" width="40"> | [YouTube Transcript Scraper](https://apify.com/hirepulse/youtube-transcript-scraper) | "Summarize the last 10 videos of this channel" | $3 per 1,000 transcripts |

## Connect all five at once

Add this server to your MCP client. The first connection opens a browser window to sign in to Apify; a free account is enough to start.

```json
{
  "mcpServers": {
    "hirepulse": {
      "url": "https://mcp.apify.com?tools=hirepulse/google-jobs-scraper,hirepulse/ats-job-pulse,hirepulse/keyword-search-volume,hirepulse/domain-seo-overview,hirepulse/youtube-transcript-scraper"
    }
  }
}
```

Only need one? Keep just that tool in the `tools=` list, for example `https://mcp.apify.com?tools=hirepulse/google-jobs-scraper`.

Clients that cannot sign in through a browser can send an `Authorization: Bearer <your Apify API token>` header instead.

### Claude Code

```bash
claude mcp add --transport http hirepulse "https://mcp.apify.com?tools=hirepulse/google-jobs-scraper,hirepulse/ats-job-pulse,hirepulse/keyword-search-volume,hirepulse/domain-seo-overview,hirepulse/youtube-transcript-scraper"
```

## Use over HTTP instead

Every tool is also a plain API:

```bash
curl -X POST "https://api.apify.com/v2/acts/hirepulse~google-jobs-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"queries": ["data engineer"], "country": "US", "location": "Austin,Texas"}'
```

Each tool's page lists its full input and output.

## Free preview

On Apify's free plan, each run of the three data-API tools returns a small real sample:
- Google Jobs: 10 jobs.
- Keyword Search Volume: metrics for 3 keywords.
- Domain SEO Overview: the traffic overview of one domain.

The YouTube tool returns 3 transcripts per run. The ATS tool works on every plan.

## Listed in the MCP Registry

Each tool is published in the official [MCP Registry](https://registry.modelcontextprotocol.io) as `io.github.edtool79-collab/<tool-name>`.
