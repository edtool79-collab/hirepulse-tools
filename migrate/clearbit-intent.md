# Moving from Clearbit to hirepulse/company-intent-radar

> Field mapping from Clearbit (HubSpot Breeze Intelligence) company intent to the hirepulse Company Intent Radar on Apify: what maps, what differs, and an honest all-in cost comparison with dates.

This page is for teams that used Clearbit's company enrichment and intent data — now sold as HubSpot's Breeze Intelligence — and want a pay-per-use alternative for the intent side. The two products overlap only partially, so this page maps what fits, says plainly what does not, and compares real costs with dates.

Clearbit facts on this page were checked on **October 24, 2026** on [clearbit.com](https://clearbit.com) (now a HubSpot landing page) and third-party pricing analyses published September 2026. HubSpot changes Breeze credit tiers without a stable public pricing page, so confirm current rates in your own HubSpot portal before deciding.

## What is different

| | Clearbit / Breeze Intelligence | hirepulse Company Intent Radar |
| --- | --- | --- |
| Delivery | HubSpot platform feature (credits inside HubSpot) | Standalone Apify Actor, works with any CRM or script |
| Input | A company domain or an email in your HubSpot CRM | A company domain |
| Output | Firmographics + enrichment fields written into CRM records | One JSON report: hiring signals (jobs last 30 days, which ATS), Google Ads presence, organic traffic and SEO trend, email provider from MX records, 0-100 intent score, one-line summary |
| Intent basis | Enrichment data + website visitor identification (IP-based) | Public job posts + live ad activity + traffic trend |
| Requirements | A paid HubSpot subscription on top of credit packs | An Apify account and a token |
| Billing | Credit packs; unused credits expire monthly | $0.03 per company report, charged only when the full report was produced |

The core difference: Clearbit's intent product leans on **who is visiting your website** (deanonymized via IP intelligence), while the Company Intent Radar reads **what the target company is publicly doing right now** — hiring, advertising, growing traffic. Use cases differ: visitor de-anonymization needs Clearbit-class infrastructure; account prioritization and outbound list scoring do not.

## Fields we do not return

Being explicit about gaps: the Radar does not return firmographics (industry, employee count, funding), contact-level enrichment (names, emails, roles), visitor identification, technographic depth at Clearbit's field level (the separate [Website Tech Stack Detector](https://edtool79-collab.github.io/hirepulse-tools/website-tech-stack-api/) covers a subset), or CRM write-back (you wire that yourself, which is one `POST` to your CRM's API).

## Price comparison (checked October 24, 2026)

Third-party analyses of HubSpot's public pricing (September 2026) put Breeze Intelligence at roughly **$45/month for 100 credits** on annual billing, on top of a HubSpot subscription starting around $20/month — a realistic all-in floor near **$65/month (~$780/year)** for 100 enrichments, with unused credits expiring monthly. Workflow automation around enrichment typically assumes **HubSpot Professional (~$800/month)**, putting practical mid-market setups in the $1,000+/month band.

The Radar at **$0.03 per full report** produces the same 100 company reports for **$3.00**, with no subscription, no credit expiry, and no platform requirement. At 1,000 companies: ~$30 vs an estimated ~$450/month credit tier (again plus platform). If you need firmographics and contact graphs, Breeze still earns its cost — but for "which of these 500 domains should sales call first," the difference is three orders of magnitude.

Prices and tiers change. Check HubSpot's portal and the [live Pricing tab on the Apify Store](https://apify.com/hirepulse/company-intent-radar) before you decide.

## Field mapping

| Clearbit / Breeze field | Radar equivalent | Notes |
| --- | --- | --- |
| `company.domain` | `domain` | same |
| — (firmographics: industry, employees, funding) | **not returned** | use a firmographics source if required |
| `company.tech` (partial) | tech signals in report + separate Tech Stack Detector | different depth |
| — (visitor intent) | **not returned** | different data class entirely |
| — (hiring data; not a Clearbit strength) | `jobs`, `new_jobs_30d`, ATS platform | Radar's real edge |
| — (ads running) | `google_ads_total`, ads currently running | Radar's real edge |
| — (SEO trend) | organic traffic trend fields | Radar's real edge |
| intent tier / score | `intent_score` (0-100) + `summary` | explainable inputs |

## Before/after Python

### Before (Clearbit API v2, historical pattern)

```python
import requests

resp = requests.get(
    "https://person.clearbit.com/v2/companies/find",
    params={"domain": "linear.app"},
    auth=(CLEARBIT_API_KEY, ""),
)
company = resp.json()
# firmographics + tags; intent required visitor data product
```

### After (Company Intent Radar)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

domains = ["linear.app", "vercel.com", "notion.so"]
run = client.actor("hirepulse/company-intent-radar").call(run_input={"domains": domains})
reports = list(client.dataset(run["defaultDatasetId"]).iterate_items())

hot = sorted(reports, key=lambda r: r.get("intent_score", 0), reverse=True)
for r in hot:
    print(f"{r['intent_score']:3d} | {r['domain']:18s} | jobs30d={r.get('new_jobs_30d')} | ads={r.get('google_ads_total')} | {r.get('summary')}")
```

Reports are charged only when the full report was produced; the free Apify plan covers hiring and email signals for 5 companies, which is exactly enough to validate the mapping before you switch a workflow over.

## Switching checklist

1. Inventory which Clearbit fields your workflows actually read — most teams use five or fewer.
2. If the list is firmographics-heavy, stay (or add a firmographics source); if it is intent/score-heavy, proceed.
3. Pilot: run your top 20 domains through the Radar (≤$0.60, or free-tier 5 domains), diff the ranking against your current Breeze scores.
4. Wire the CRM write-back yourself — the JSON rows drop into HubSpot/API-based CRM properties directly.

Source page: https://edtool79-collab.github.io/hirepulse-tools/migrate/clearbit-intent/
