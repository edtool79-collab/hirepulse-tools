# HirePulse public data tools for AI agents

Sixteen public HirePulse Actors on [Apify](https://apify.com/hirepulse), verified October 24, 2026. Choose a tool by the evidence it returns. Use its current Input and Pricing tabs before running it; this directory does not promise free runs or complete source coverage.

| Actor | Use it for | Important limit |
|---|---|---|
| [TikTok Product Research](https://apify.com/hirepulse/viral-product-radar) | Product-video evidence and same-video growth | Baseline first; six-hour minimum, capped collection opt-in; no sales forecasts |
| [ATS Detector: Find a Company's Job Board (Free)](https://apify.com/hirepulse/ats-detector) | Find a public ATS job-board URL from a company domain. | No Actor fee; Apify platform usage can cost money. Missing boards are not proof that a company is not hiring. [Pricing](https://apify.com/hirepulse/ats-detector/pricing) |
| [ATS Job Scraper: Greenhouse, Lever, Ashby, Workable & More](https://apify.com/hirepulse/ats-job-pulse) | Read supported public ATS boards and return jobs or a company summary. | Coverage depends on supported boards and accessible evidence; missing salary data stays unavailable. [Pricing](https://apify.com/hirepulse/ats-job-pulse/pricing) |
| [Google Jobs Alternative: ATS & Public Job Listings](https://apify.com/hirepulse/google-jobs-scraper) | Search supported public career and ATS job listings by query. | Default public mode is an alternative source route, not measured live Google Jobs SERP coverage. Availability and fields vary. [Pricing](https://apify.com/hirepulse/google-jobs-scraper/pricing) |
| [B2B Account Research Agent: Hiring, Tech, Ads & Contacts](https://apify.com/hirepulse/b2b-account-research-agent) | Combine selected hiring, technology, ads and contact sources into an account dossier. | Source Actor fees and parent fees are separate. Optional connector writes require explicit operations and opt-in; disabled in the example. [Pricing](https://apify.com/hirepulse/b2b-account-research-agent/pricing) |
| [Company Intent Radar: Hiring, Ads & Website Signals](https://apify.com/hirepulse/company-intent-radar) | Combine observed hiring, public ad, website and DNS evidence with an explainable intent estimate. | A score is a heuristic, not proof of buying intent, growth or ad spend. Public mode does not measure SEO traffic. [Pricing](https://apify.com/hirepulse/company-intent-radar/pricing) |
| [Website Tech Stack Detector: BuiltWith Alternative, Bulk API](https://apify.com/hirepulse/website-tech-stack-detector) | Inspect accessible website markup, response headers and DNS for technology signals. | Static observations can miss dynamically loaded technologies; no exhaustive detection guarantee. [Pricing](https://apify.com/hirepulse/website-tech-stack-detector/pricing) |
| [Company Contacts Finder: Emails, Phones, Socials & DNS](https://apify.com/hirepulse/company-contact-details-finder) | Extract available public website emails, phone numbers and social links, with optional DNS checks. | MX records describe domain email infrastructure; they do not verify that a mailbox exists or accepts mail. [Pricing](https://apify.com/hirepulse/company-contact-details-finder/pricing) |
| [Google Ads Transparency Scraper: Competitor Ads by Domain](https://apify.com/hirepulse/google-ads-transparency-scraper) | Look up Google Ads Transparency observations by company domain, as ad rows or a domain summary. | Observations are not ad spend, impressions or proof that an ad is currently serving. [Pricing](https://apify.com/hirepulse/google-ads-transparency-scraper/pricing) |
| [Domain SEO Overview: Metadata, Sitemaps & Keywords](https://apify.com/hirepulse/domain-seo-overview) | Inspect page metadata, sitemap observations, autocomplete suggestions and available CrUX popularity tiers. | Native mode does not measure traffic, Google rankings, search volume or CPC. A CrUX tier is a popularity bucket, not visits. [Pricing](https://apify.com/hirepulse/domain-seo-overview/pricing) |
| [Keyword Research: Google Autocomplete & Suggestions](https://apify.com/hirepulse/keyword-search-volume) | Generate Google autocomplete suggestions and keyword research ideas by seed, country and language. | Native mode does not measure monthly search volume, CPC or difficulty; unavailable measurements remain null. [Pricing](https://apify.com/hirepulse/keyword-search-volume/pricing) |
| [AliExpress Search Scraper: Products, Prices & Sales Data](https://apify.com/hirepulse/aliexpress-search-scraper) | Read accessible AliExpress keyword search results with available prices, ratings and sold-count fields. | Not image search. Fields depend on source availability; no guarantee of seller details, reviews or shipping-cost data. [Pricing](https://apify.com/hirepulse/aliexpress-search-scraper/pricing) |
| [YouTube Transcript Scraper: Bulk Videos, Shorts & Timestamps](https://apify.com/hirepulse/youtube-transcript-scraper) | Fetch available captions and timestamped transcripts for supplied YouTube video URLs. | Videos can be unavailable, blocked or lack captions. Bulk video input is not a promise of channel discovery. [Pricing](https://apify.com/hirepulse/youtube-transcript-scraper/pricing) |
| [MCP & x402 Evidence Grader](https://apify.com/hirepulse/mcp-x402-server-grader) | Inspect observed MCP catalogs or unpaid x402 challenges and produce a heuristic evidence report. | Not official Glama certification. Generated drafts require review; no remote changes or payment is made by the check. [Pricing](https://apify.com/hirepulse/mcp-x402-server-grader/pricing) |
| [AI Crawler Readiness Audit & llms.txt Draft](https://apify.com/hirepulse/ai-search-brand-visibility-radar) | Audit structural AI crawler readiness, including robots rules, metadata and llms.txt observations. | Not measurement of brand citations or ranking inside ChatGPT, Gemini or other AI answers. [Pricing](https://apify.com/hirepulse/ai-search-brand-visibility-radar/pricing) |
| [Store Catalog to llms.txt Draft](https://apify.com/hirepulse/shopify-to-llms-generator) | Generate an llms.txt catalog draft from a store with an accessible public catalog. | Coverage is not universal; blocked stores may be unsupported. Does not write to a Shopify root or deploy the draft. [Pricing](https://apify.com/hirepulse/shopify-to-llms-generator/pricing) |

## Connect through Apify MCP

Configure an MCP client with the Actors you need. The following URL requests all 16; remove entries to narrow the selection. OAuth-capable clients use Apify sign-in. Clients supporting token authentication can send `Authorization: Bearer <APIFY_TOKEN>`; keep credentials out of URLs, source control and logs.

```json
{
  "mcpServers": {
    "hirepulse": {
      "url": "https://mcp.apify.com?tools=hirepulse/ats-detector,hirepulse/ats-job-pulse,hirepulse/google-jobs-scraper,hirepulse/b2b-account-research-agent,hirepulse/company-intent-radar,hirepulse/website-tech-stack-detector,hirepulse/company-contact-details-finder,hirepulse/google-ads-transparency-scraper,hirepulse/domain-seo-overview,hirepulse/keyword-search-volume,hirepulse/aliexpress-search-scraper,hirepulse/youtube-transcript-scraper,hirepulse/mcp-x402-server-grader,hirepulse/ai-search-brand-visibility-radar,hirepulse/shopify-to-llms-generator,hirepulse/viral-product-radar"
    }
  }
}
```

Use [Apify's MCP documentation](https://docs.apify.com/platform/integrations/mcp) for current client setup. The actual server catalog and permissions determine which operations are available; this list is not a runtime certification.

## Run one tool through the API

The following is an example of a paid operation, not a command this documentation has executed. Set a spending limit and inspect the current pricing and schema first.

```bash
curl -X POST "https://api.apify.com/v2/acts/hirepulse~keyword-search-volume/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false" \
  -H "Authorization: Bearer <APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"keywords":["workflow automation"],"country":"US","language":"en","use_paid_upstream":false}'
```

## Costs and unavailable data

Actor event charges, start charges, subscription-tier discounts and platform costs vary by Actor. ATS Detector has no Actor fee, but platform usage may still cost money. Native mode means no optional paid data provider is requested; it does not make Apify execution free. B2B orchestration can also incur fees for its source Actors. This README does not guarantee a free preview or a specific current price.

Missing evidence is unknown, not zero. No native SEO or keyword example measures visits, Google rank, monthly search volume or CPC. A CrUX popularity bucket is not a traffic estimate. Read the selected Actor's input and output documentation for coverage and billing conditions.

## 🔗 Recommended 1-Click Workflows & Tool Pairings

Accelerate agentic and manual workflows by piping complementary tools together:

1. **ATS Hiring Intelligence Pipeline:**
   - **Step 1:** Run [ATS Detector](https://apify.com/hirepulse/ats-detector) (Free actor fee) on company domains (`stripe.com`, `linear.app`) to locate active job board slugs/URLs.
   - **Step 2:** Pipe board slugs into [ATS Job Scraper](https://apify.com/hirepulse/ats-job-pulse) to extract structured roles, salaries, and detected tech stack with 1-click execution.

2. **SEO & Competitor Research Pipeline:**
   - **Step 1:** Run [Domain SEO Overview](https://apify.com/hirepulse/domain-seo-overview) on competitor domains for metadata, sitemaps, and core keywords.
   - **Step 2:** Deep-dive into organic autocomplete and search suggestions with [Keyword Research](https://apify.com/hirepulse/keyword-search-volume).

3. **E-Commerce & Agentic Catalog Pipeline:**
   - **Step 1:** Analyze market pricing and popular goods with [AliExpress Search Scraper](https://apify.com/hirepulse/aliexpress-search-scraper).
   - **Step 2:** Structure store product listings into machine-readable agent context using [Store Catalog to llms.txt Draft](https://apify.com/hirepulse/shopify-to-llms-generator).

## Documentation and discovery

- [Tool summaries and input examples](llms-full.txt)
- [Existing public example-task directory](tasks-directory.md): a published link is a starting configuration, not proof of a successful current run.
- [Documentation site](https://edtool79-collab.github.io/hirepulse-tools/): individual pages can have different update dates; the live Actor page and schema are the source for current behavior and pricing.
- [MCP Registry](https://registry.modelcontextprotocol.io): Each tool is published in the official MCP Registry as `io.github.edtool79-collab/<tool-name>`. Registry publication is a separate step from editing this repository. Do not infer that all 16 individual listings exist from this README.

## ⚡ n8n Workflow Automation Suite

Automate your lead enrichment and intent tracking without burning tokens on raw HTML scraping.
Check out our pre-built, production-ready n8n workflows in the [`/n8n`](./n8n) directory:

1. **[B2B Intent Pre-Filter & Zero-Waste Enrichment](./n8n/1-b2b-intent-prefilter-enrichment.json)**: Enriches domains with Tech Stack, ATS Hiring Intent, and Google Ads spend, pre-filters deterministically with zero AI cost, and cuts LLM prompt token usage by **97.6%**.
2. **[Competitor Ads & Hiring Surge Monitor](./n8n/2-competitor-ads-and-hiring-monitor.json)**: Weekly automated intelligence scanner alerting your team to competitor expansion and paid advertising moves.

👉 **[Explore the n8n Suite Documentation & Quickstart Guide](./n8n/README.md)**  
🧮 **[Interactive n8n AI Token Bleed ROI Calculator](./calculator.html)**: Calculate exact token waste and monthly dollar savings vs. raw scraping.  
📚 **[Cheaper Clay Alternative Guide: $6.15 vs. $200 per 1k leads](./guides/n8n-clay-alternative-cheaper.md)**  
📚 **[Zero-Token B2B Lead Enrichment Benchmark](./guides/zero-token-b2b-lead-enrichment.md)**


## 🧩 Make.com & Activepieces Suites (Clay Alternative)

Build enterprise-grade B2B outbound workflows on Make.com or self-hosted Activepieces for 96% less than Clay or Apollo:
- **Make.com Scenario Blueprint:** [/make/b2b-intent-prefilter-blueprint.json](./make/b2b-intent-prefilter-blueprint.json)
- **Make.com Setup Guide:** [How to Build a Clay Alternative in Make.com for 90% Less Cost](./guides/make-clay-alternative-cheaper.md)
- **Activepieces Flow:** [/activepieces/b2b-intent-prefilter-flow.json](./activepieces/b2b-intent-prefilter-flow.json)

## 📊 Industry Reports & Research Studies

- **[Empirical Study: 500 AI Startups Tech Stacks & Hiring Trends](./guides/viral-data-study-500-startups.md)**: Discover why 34.5% of ad-spending AI startups have 0 open engineering positions, and how deterministic multi-signal extraction saved 96.7% in research data costs.

## 🤖 AI Registries & Ecosystem Directories

- **[MCP & AI Agent Directory Submission Pack](./docs/AI_REGISTRIES_SUBMISSION_PACK.md)**: Ready-to-use profiles and streamable HTTP manifests for Smithery.ai, Glama.ai, PulseMCP, TAAFT, and Futurepedia.
- **[Apify Store SEO & Keyword Strategy](./docs/APIFY_STORE_SEO_KEYWORD_PLAN.md)**: Master keyword matrix and ranking guide for all 16 Actors and 80 Tasks.


## TikTok product research

$0.02 per delivered report; Clockworks collection is separate and capped ($0.04 total by default).

[First-run guide](tiktok-product-research-api/) · [Agent documentation](tiktok-product-research-api.md).
