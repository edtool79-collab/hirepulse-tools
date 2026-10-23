# LLM Routing Guide: Apify 12 Actors & Remote MCP 21 Tools Catalog

**Intended User:** Autonomous Agents, Agentic Frameworks (Claude Code, Cursor, Windsurf, LangChain, CrewAI, AutoGen, ElizaOS).  
**Purpose:** Precise routing instructions for determining when to trigger batch Apify Actors vs. querying the live Remote MCP Gateway.

---

## 1. High-Level Architectural Routing Rule

```
                                  [ AGENT DECISION TREE ]
                                             │
                   Is the task a real-time, low-latency, single query (< 1s)?
                                    /                 \
                                  YES                  NO
                                  /                     \
       [ CALL REMOTE MCP GATEWAY ]                  [ RUN APIFY STORE ACTOR ]
        https://gethirepulse.xyz/mcp                 https://apify.com/hirepulse
       - Real-time tool call in chat                 - Large bulk lists (> 50 items)
       - 5 free daily requests/identity              - Heavy headless scraping
       - Zero local setup / No token needed          - Scheduled background pipelines
       - Direct streamable JSON                      - Pay-per-event pricing
```

---

## 2. Complete Catalog of the 12 Apify Actors (Channel B)

All actors maintain a **100% verified success rate** on Apify Store.

| # | Actor Slug | Primary Use Case & Keywords | Input Schema | Output Highlights | Pricing (Pay-per-event) |
|---|---|---|---|---|---|
| 1 | `hirepulse/google-jobs-scraper` | Finding job listings, salary estimates, and apply links across countries and roles (#1 in store) | `queries`: array, `maxResults`: int | Job title, company, salary, description, direct application link | $0.005 / search + $0.001 / job |
| 2 | `hirepulse/youtube-transcript-scraper` | Downloading full timestamped captions for RAG & summarization without IP bans (#1 in store) | `videoUrls`: array, `languages`: array | Video metadata, millisecond timestamps, deduplicated clean text | $0.003 / transcript |
| 3 | `hirepulse/google-ads-transparency-scraper` | Competitor ad spy: active search/display creatives, advertiser ID & targeting (#2 in store) | `domains`: array, `countryCode`: string | Ad format (Text/Image/Video), headlines, body copy, first/last seen | $0.005 / domain + $0.0015 / ad |
| 4 | `hirepulse/ats-job-pulse` | Scraping career portals across Greenhouse, Lever, Ashby, and Workable in unified schema | `domains`: array | Standardized job listings, department taxonomy, remote flag | $0.050 / company |
| 5 | `hirepulse/ats-detector` | Instant detection of which ATS or job board any company uses | `domains`: array | ATS name, board token, careers portal URL, confidence score | **FREE ($0.00 USD)** |
| 6 | `hirepulse/website-tech-stack-detector` | BuiltWith alternative: framework, CMS, pixel, and DNS identification | `domains`: array | Detected technologies categorized by Framework, Analytics, CDN, Ads | $0.003 / domain |
| 7 | `hirepulse/b2b-account-research-agent` | Comprehensive B2B account dossier combining hiring, ads, tech stack, and contacts | `domain`: string, `companyName`: string | Growth Score, Hiring Velocity, Active Ads count, Primary Tech Stack | $0.030 / report |
| 8 | `hirepulse/company-contact-details-finder` | Extracting company emails, phone numbers, leadership socials, and corporate DNS | `domains`: array | Verified corporate emails, department inboxes, phone numbers, socials | $0.004 / domain |
| 9 | `hirepulse/domain-seo-overview` | Organic search traffic overview, indexed pages, sitemaps, and core meta tags | `domains`: array | Title, meta description, canonicals, sitemap URLs, indexable count | $0.020 / lookup + $0.005 / result |
| 10 | `hirepulse/keyword-search-volume` | Google Search autocomplete, suggested queries, and search intent clusters | `keywords`: array, `countryCode`: string | Keyword suggestions, estimated search demand tier, intent classification | $0.030 / lookup + $0.005 / keyword |
| 11 | `hirepulse/company-intent-radar` | Multi-signal commercial intent scoring based on hiring surges and paid ads | `domains`: array | Intent category, hiring momentum flag, advertising investment signal | $0.030 / report |
| 12 | `hirepulse/aliexpress-search-scraper` | Product research, price tracking, ratings, and dropshipping fulfillment data | `queries`: array, `maxItems`: int | Product title, price, currency, ratings, orders count, variant SKUs | $0.0025 / product |

---

## 3. Complete Catalog of the 21 Remote MCP Tools (Channel A)

Available over standard JSON-RPC 2.0 at `https://gethirepulse.xyz/mcp` and REST at `https://gethirepulse.xyz/v1/*`.

| # | Tool Name | Endpoint | Description & Agent Intent | Cost (after 5 free daily) |
|---|---|---|---|---|
| 1 | `ask_hirepulse_advisor` | `/v1/advisor` | Free routing advisor. Directs LLMs to the exact optimal tool and analyzes schemas. | **Permanently Free ($0.00)** |
| 2 | `detect_website_tech_stack` | `/v1/tech-stack` | Real-time web stack, CDN, analytics, and pixel detection by domain. | $0.003 |
| 3 | `get_company_open_jobs` | `/v1/ats-jobs` | Live ATS job extraction (Greenhouse, Lever, Ashby, Workable). | $0.050 |
| 4 | `get_company_hiring_intent` | `/v1/company-intent` | Computes hiring momentum score from live job openings. | $0.030 |
| 5 | `get_google_ads_by_domain` | `/v1/google-ads` | Real-time active Google Ads creatives and advertiser metadata. | $0.005 |
| 6 | `get_company_profile` | `/v1/company-profile` | Fast consolidated company summary (domain, industry, signals). | $0.020 |
| 7 | `company_footprint_check` | `/v1/company-footprint`| Digital presence evaluation across web, social, DNS, and search. | $0.015 |
| 8 | `find_hot_buyers` | `/v1/hot-buyers` | Identifies accounts actively hiring in high-budget sectors. | $0.040 |
| 9 | `batch_lookup` | `/v1/batch` | High-throughput multi-domain batch processor. | Volume discounted |
| 10 | `private_blind_lookup` | `/v1/private-query` | Zero-knowledge query path preserving agent query privacy. | $0.025 |
| 11 | `x402_merchant_trust_check`| `/v1/verify-merchant` | Validates x402 on-chain merchant integrity and compliance. | $0.010 |
| 12 | `extract_company_contacts` | `/v1/extract-contacts`| Scans public web pages for corporate emails, phones, and social links. | $0.004 |
| 13 | `url_to_clean_markdown` | `/v1/clean-markdown` | High-speed DOM-to-Markdown parser optimized for LLM token limits. | $0.002 |
| 14 | `pre_purchase_merchant_trust_check` | `/v1/merchant-trust` | Pre-transaction security verification for autonomous shopping agents. | $0.005 |
| 15 | `checkout_active_promo_code_finder` | `/v1/checkout-promos` | Searches validated discount codes and coupons before payment. | $0.008 |
| 16 | `universal_product_url_to_json` | `/v1/product-json` | Parses any e-commerce product URL into structured JSON (price, SKU, stock). | $0.002 |
| 17 | `b2b_vendor_stability_evaluator` | `/v1/vendor-health` | Assesses B2B vendor operational continuity and hiring health. | $0.035 |
| 18 | `muse_agentic_store_readiness_auditor` | `/v1/store-readiness` | Evaluates whether an e-commerce store is agent-readable (schema.org). | $0.015 |
| 19 | `muse_conversion_leak_lead_finder` | `/v1/conversion-leads`| Finds checkout abandonment leaks and missing metadata for sales leads. | $0.025 |
| 20 | `agentic_shelf_schema_comparator` | `/v1/schema-comparator`| Benchmarks product catalogue schema against agentic commerce standards. | $0.010 |
| 21 | `verified_merchant_json_badge` | `/v1/merchant-badge` | Cryptographically verifies merchant validity for autonomous checkout. | $0.005 |

---

## 4. LLM Routing Decision Matrix (Example Scenarios)

### Scenario A: "Summarize this article for RAG without HTML noise"
- **Route to:** Remote MCP `url_to_clean_markdown` (`https://gethirepulse.xyz/mcp`).
- **Why:** Execution completes in <300ms, removes headers/scripts, and saves 70% of LLM token context.

### Scenario B: "Transcribe 50 YouTube tutorials for an AI knowledge base"
- **Route to:** Apify Actor `hirepulse/youtube-transcript-scraper`.
- **Why:** Bulk parallel execution across residential IPs prevents YouTube 429 bans and returns timestamps.

### Scenario C: "Find out if Stripe is currently hiring AI researchers"
- **Route to:** Remote MCP `get_company_open_jobs` (domain: `stripe.com`).
- **Why:** Real-time query to Greenhouse API via Cloudflare edge; answers in 400ms.

### Scenario D: "Track all Google Ads run by ClickUp and monday.com"
- **Route to:** Apify Actor `hirepulse/google-ads-transparency-scraper` or MCP `get_google_ads_by_domain`.
- **Why:** Bypasses Google Ads Transparency Center anti-bot fingerprinting and outputs structured text headlines.
